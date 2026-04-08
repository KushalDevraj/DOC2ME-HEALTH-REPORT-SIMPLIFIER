from fastapi import FastAPI, File, UploadFile
from utils import variables, set_variable, relative_path
from utils.logger import Logger
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.model import Chatbot, Model
from PIL import Image
from services import db as database
import re


db = database(variables["database_file"])

model = Model(variables["t5_model_name"]) 
chatbot = Chatbot(
    model_name=variables["model_name"],
    csv_file=variables["model_embedding_csv_file"],
    embedding_file=variables["model_embedding_file"],
    chunks_file=variables["model_chunks_file"],
    fass_index_file=variables["model_faiss_index_file"],
)

logger = Logger(log_dir=relative_path("/logs"))
logger.info("Imported the required modules")
logger.info("Starting the application")

medicalsearch = FastAPI()

@medicalsearch.on_event("startup")
async def startup_event():
    logger.info("Pre-warming Chatbot RAG chain...")
    _ = chatbot.rag_chain
    logger.info("Chatbot pre-warmed and ready.")


class SearchPrompt(BaseModel):
    input: str


class ConversationPrompt(BaseModel):
    input: str

class Feedback(BaseModel):
    feedback: str
    uuid: str


# Configure CORS settings
origins = [
    "http://127.0.0.1:5173",
]

medicalsearch.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@medicalsearch.get("/")
async def root():
    return {"message": "Hello World"}


# @medicalsearch.post("/set_account_details")
# async def get_account_details(account: GetAccountDetail):
#     set_variable("bucket_url", account.bucket_url)
#     set_variable("bucket_key", account.bucket_key)
#     set_variable("bucket_secret", account.bucket_secret)
#     set_variable("bucket_name", account.bucket_name)
#     return {"message": "Account details updated"}


@medicalsearch.post("/simplify_data")
def search_image(simplify: SearchPrompt):
    # Enable persisting input for expert review
    try:
        uuid = db.insert_input(simplify.input)
    except Exception as e:
        logger.error(f"Database error while inserting input: {e}")
        uuid = None

    # Using Chatbot (Llama3) instead of Model (T5) to avoid hallucinations (e.g., Fever as skin condition)
    response = chatbot.get_text_simplification(simplify.input)
    
    if uuid:
        try:
            db.insert_output(uuid, response, "text")
        except Exception as e:
            logger.error(f"Database error while inserting output: {e}")
            
    return response


@medicalsearch.post("/simplify_text_llm")
def conversation(conv: ConversationPrompt):
    # Enable persisting input for expert review
    try:
        uuid = db.insert_input(conv.input)
    except Exception as e:
        logger.error(f"Database error while inserting input: {e}")
        uuid = None

    response = chatbot.get_text_simplification(conv.input)
    
    if uuid:
        try:
            db.insert_output(uuid, response, "text")
        except Exception as e:
            logger.error(f"Database error while inserting output: {e}")
            
    return response


@medicalsearch.post("/simplify_report_llm")
def simplify_report(prompt: ConversationPrompt):
    input_text = prompt.input
    try:
        uuid = db.insert_input(input_text)
    except Exception as e:
        logger.error(f"Database error while inserting input: {e}")
        uuid = None
    response = chatbot.get_report_simplification(input_text)
    if uuid:
        try:
            db.insert_output(uuid, response, "text")
        except Exception as e:
            logger.error(f"Database error while inserting output: {e}")
    return response


@medicalsearch.post("/simplify_image_report_llm")
def simplify_image_report(simplify: SearchPrompt ):
    # uuid = db.insert_input(simplify.input)
    response = chatbot.get_report_simplification(simplify.input)
    # db.insert_output(uuid, response, "ocr")
    return response

@medicalsearch.post("/simplify_text_llm_context")
def simplify_text_llm_context(simplify: SearchPrompt):
    try:
        uuid = db.insert_input(simplify.input)
    except Exception as e:
        logger.error(f"Database error while inserting input: {e}")
        uuid = None

    response = chatbot.get_chatbot_answer_with_context(simplify.input)

    if uuid:
        try:
            db.insert_output(uuid, response, "text")
        except Exception as e:
            logger.error(f"Database error while inserting output: {e}")

    return response

from fastapi.responses import StreamingResponse

@medicalsearch.post("/simplify_text_llm_stream")
async def simplify_text_llm_stream(prompt: ConversationPrompt):
    input_text = prompt.input
    # We don't insert input here yet as it's a stream, or deal with it later
    return StreamingResponse(chatbot.get_chatbot_answer_with_context_stream(input_text), media_type="text/event-stream")

@medicalsearch.get("/simplify_reset_context")
def reset_context():
    chatbot.reset_conversation()
    return {"message": "Context reset"}

@medicalsearch.get("/feedback_random")
def feedback():
    random_input = db.get_latest_input()
    if not random_input:
        return {"error": "No data available"}
    output = db.get_output_from_input(random_input[0])
    if not output:
        return {"error": "No output found for input"}
    
    # Scrub PII from input display
    input_text = random_input[1]
    input_text = re.sub(r'(PATIENT NAME\s*:\s*)([^ \n|]+)', r'\1Patient', input_text, flags=re.IGNORECASE)
    input_text = re.sub(r'(Mrs\.|Mr\.|Ms\.)\s*([A-Z][a-zA-Z]+)', r'Patient', input_text, flags=re.IGNORECASE)
    
    return {"input": input_text, "output": output[1], "uuid": output[0]}

@medicalsearch.get("/get_feedback")
def get_feedback(feedback: str, uuid: str):
    db.insert_feedback(uuid, feedback, "doctor")
    
    # Store feedback as new training data
    try:
        # 1. Fetch original input_uuid from the output table
        # We need to find which input this output belongs to
        output_record = db.get_output_record(uuid)
        if output_record:
            input_uuid = output_record[3] # input_uuid is the 4th column
            input_data = db.get_input(input_uuid) 
            if input_data:
                original_term = input_data[0]
            
            # 2. Append to CSV
            # Format: title, text, index
            # We use the original term as title, and the approved feedback as the text explanation
            import csv
            csv_file = relative_path(variables["model_embedding_csv_file"])
            
            # Sanitize strings for CSV
            clean_term = original_term.replace('"', '""').replace('\n', ' ')
            clean_def = feedback.replace('"', '""').replace('\n', ' ')
            
            # Append safely
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Using a large index dummy or just next incremental is fine, 
                # but typically pandas puts an index. We'll use '999999' or similar to indicate user-added
                writer.writerow([clean_term, clean_def, "999999"])
                
            logger.info(f"Learned new term: {clean_term} -> {clean_def}")
            
    except Exception as e:
        logger.error(f"Failed to learn from feedback: {e}")

    return {"message": "Feedback received and learned"}
    
    