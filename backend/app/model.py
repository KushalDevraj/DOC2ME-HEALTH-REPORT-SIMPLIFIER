from transformers import AutoTokenizer, T5ForConditionalGeneration

from utils import relative_path, Logger
from joblib import dump, load
import os
import re

# Document loaders, embeddings, vectorstores
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Text splitting
from langchain_text_splitters import TokenTextSplitter, RecursiveCharacterTextSplitter

from langchain.chains import LLMChain, ConversationChain
from langchain.chains import RetrievalQA
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain

# Prompts & prompting utilities
# Prompts & prompting utilities (correct paths)
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder


# Messages
from langchain_core.messages import HumanMessage, AIMessage

# Memory
from langchain.memory import ConversationBufferMemory

# Ollama LLM support
from langchain_community.llms import Ollama



logger = Logger()
logger.info("Model module loaded")

class Model:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_path = relative_path(f"/models/{model_name}/model")
        self.tokenizer_path = relative_path(f"/models/{model_name}/tokenizer")
        if not os.path.exists(self.model_path):
            self.download_model()
            logger.info(f"Model {model_name} downloaded successfully")
        elif not os.path.exists(self.tokenizer_path) or os.path.exists(self.model_path):
            self.download_model()
            logger.info(f"Model {model_name} downloaded successfully")
        else:
            self.load_model()
            logger.info(f"Model {model_name} loaded successfully")
    
    def __str__(self) -> str:
        return f"Model Name: {self.model_name}\nModel Path: {self.model_path}\nTokenizer Path: {self.tokenizer_path}"
    
    def __repr__(self) -> str:
        self.__str__()

    def refresh_model(self):
        self.download_model()

    def download_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        self.tokenizer.save_pretrained(self.tokenizer_path)
        self.model.save_pretrained(self.model_path)

    def load_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)

    def generate_response(self, input_text: str):
        input_text = "simplify: " + input_text
        inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(inputs.input_ids, max_length=1080, num_beams=4, early_stopping=True)
        ret = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Response generated for input: {input_text}")
        logger.info(f"Response: {ret}")
        return ret

class Chatbot:
    def __init__(self, model_name: str, csv_file: str, embedding_file: str, chunks_file: str,fass_index_file:str):
        self.model_name = model_name
        self._llm = None
        self.csv_file = relative_path(csv_file)
        self.embedding_file = relative_path(embedding_file)
        self.chunks_file = relative_path(chunks_file)
        self.fass_index_file = relative_path(fass_index_file)
        self.embeddings_saved = False
        self.chunks_saved = False
        self.faiss_index_saved = False
        self._db = None
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.TEXT_PROMPT_TEMPLATE = """You are a helpful clinical assistant. Your goal is to simplify medical terminology in plain language.

        STRICT RULES:
        1. NO PREDICTIONS: Do not predict outcomes or health recovery.
        2. NO SOLUTIONS: Do not suggest treatments or medicines.
        3. PURE SIMPLIFICATION: Only explain what the terms mean in simple words.
        4. ALWAYS end with: "Doctor recommendation is required for better understanding".

        PRIVACY: Replace any names with "Patient".
        
        USER INPUT:
        {question}
        """
        self.TEXT_PROMPT = PromptTemplate.from_template(self.TEXT_PROMPT_TEMPLATE)
        
        self.REPORT_PROMPT_TEMPLATE = """You are a helpful clinical assistant. Your goal is to explain and simplify medical reports.

        CRITICAL PRIVACY RULE (VIOLATION IS STRICTLY FORBIDDEN):
        - You MUST replace ANY person's name (e.g., "Mrs. Indira", "John Doe") with the word "Patient".
        - NEVER include a real name in your summary or explanation.
        - If you see a header like "Patient Name: X", you must refer to X as "Patient".

        STRICT RULES:
        1. NO PREDICTIONS: Do not predict outcomes or health recovery.
        2. NO SOLUTIONS: Do not suggest treatments or medicines.
        3. ALWAYS end with: "Doctor recommendation is required for better understanding".

        RESPONSE FORMAT:
        Your response MUST follow this structure:
        
        ### Report Overview
        [Explain what this report is about. Use "Patient" instead of real names.]

        ### Simplified Medical Terms
        [List and explain each complex term found in the report]

        Doctor recommendation is required for better understanding.
        
        REPORT TEXT:
        {question}
        """
        self.REPORT_PROMPT = PromptTemplate.from_template(self.REPORT_PROMPT_TEMPLATE)
        
        self._text_qa_chain = None
        self._report_qa_chain = None
        self._text_qa_chain = None
        self._report_qa_chain = None
        self.chat_history = []

    def reset_conversation(self):
        self.chat_history = []
        logger.info("Chatbot: Conversation history reset")

    def scrub_pii(self, text: str) -> str:
        """
        Aggressively removes PII using regex patterns before the AI sees it.
        """
        # Scrub "Mr/Mrs/Dr Name" patterns
        text = re.sub(r'(Mr\.|Mrs\.|Ms\.|Dr\.)\s*[A-Z][a-z]+', 'Patient', text)
        
        # Scrub "Patient Name: X" patterns
        text = re.sub(r'(Patient Name|Name)\s*[:\-]\s*[A-Za-z\s]+', 'Patient Name: Patient', text, flags=re.IGNORECASE)
        
        # Scrub specific patterns seen in reports like "Mrs.INDIRA"
        text = re.sub(r'Mrs\.[A-Z]+', 'Patient', text)

        # Scrub "REF BY :DR.X"
        text = re.sub(r'REF BY\s*[:\-]\s*DR\.[A-Z\s]+', 'REF BY: DOCTOR', text, flags=re.IGNORECASE)

        # Scrub age
        text = re.sub(r'AGE\s*[:\-]\s*\d+\s*YRS', 'AGE: [REDACTED]', text, flags=re.IGNORECASE)

        # Scrub phone numbers (various formats)
        text = re.sub(r'(Phone|Ph|Mobile|Mob|Cell)\s*[:\-]\s*[\d\-\+\s]+', 'Phone: [REDACTED]', text, flags=re.IGNORECASE)
        text = re.sub(r'\+?\d{2,4}[-\s]?\d{3,5}[-\s]?\d{4,6}', '[PHONE REDACTED]', text)

        # Scrub emails
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL REDACTED]', text)

        # Scrub signatures
        text = re.sub(r'(Signature|Sign|Sd/-)\s*[:\-]?\s*[A-Za-z\s\.]+', '[SIGNATURE REDACTED]', text, flags=re.IGNORECASE)
        
        return text


    @property
    def llm(self):
        if self._llm is None:
            logger.info("Loading LLM")
            self._llm = Ollama(model=self.model_name, num_ctx=2048)
            logger.info("LLM loaded successfully")
        return self._llm
    
    @property
    def db(self):
        if self._db is None:
            logger.info("Loading and chunking documents")
            self._db = self.load_and_chunk_documents()
            logger.info("Documents loaded and chunked successfully")
        return self._db
    
    @property
    def text_qa_chain(self):
        if self._text_qa_chain is None:
            self._text_qa_chain = LLMChain(llm=self.llm, prompt=self.TEXT_PROMPT)
        return self._text_qa_chain

    @property
    def report_qa_chain(self):
        if self._report_qa_chain is None:
            self._report_qa_chain = LLMChain(llm=self.llm, prompt=self.REPORT_PROMPT)
        return self._report_qa_chain
    
    def load_and_chunk_documents(self):
        """
        Load documents from CSV file, chunk them, and create FAISS index.

        Args:
        - csv_file (str): Path to the CSV file containing documents.

        Returns:
        - FAISS: FAISS index containing chunked documents.
        """
        # Load documents from CSV
        if os.path.exists(self.embedding_file):
            logger.info(f"Loading embeddings from pickle file: {self.embedding_file}")
            with open(self.embedding_file, "rb") as f:
                embeddings = load(f)
            self.embeddings_saved = True
            logger.info(f"Embeddings loaded successfully")
        
        if os.path.exists(self.chunks_file):
            logger.info(f"Loading chunks from pickle file: {self.chunks_file}")
            with open(self.chunks_file, "rb") as f:
                chunks = load(f)
            self.chunks_saved = True
            logger.info(f"Chunks loaded successfully")
        
        if not self.embeddings_saved or not self.chunks_saved:
            logger.info(f"Loading documents from CSV file: {self.csv_file}")
            loader = CSVLoader(file_path=self.csv_file)
            data = loader.load()

            # Chunk documents
            if not self.chunks_saved:
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=128, chunk_overlap=50)
                chunks = text_splitter.split_documents(data)
                logger.info(f"Documents chunked successfully")
                with open(self.chunks_file, "wb") as f:
                    dump(chunks, f)
                logger.info(f"Chunks saved to file: {self.chunks_file}")

            # Create embeddings
            if not self.embeddings_saved:
                from utils import variables
                device = variables.get("device", "cpu")
                logger.info(f"Creating embeddings using device: {device}")
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={"device": device}
                )
                with open (self.embedding_file, "wb") as f:
                    dump(embeddings, f)
                logger.info(f"Embeddings saved to file: {self.embedding_file}")
        # Build FAISS index
        if os.path.exists(self.fass_index_file):
            logger.info(f"Loading FAISS index from file: {self.fass_index_file}")
            db = FAISS.load_local(self.fass_index_file,embeddings=embeddings,allow_dangerous_deserialization=True)
            self.faiss_index_saved = True
            logger.info(f"FAISS index loaded successfully")
        else:
            logger.info("Building FAISS index")
            db = FAISS.from_documents(chunks, embeddings)
            db.save_local(self.fass_index_file)
            logger.info(f"FAISS index saved to file: {self.fass_index_file}")
        return db
    
    def get_text_simplification(self, user_input: str):
        # Scrub PII
        user_input = self.scrub_pii(user_input)
        result = self.text_qa_chain.invoke({"question": user_input})
        return result['text']

    def get_report_simplification(self, user_input: str):
        # Pre-process text to remove PII
        scrubbed_input = self.scrub_pii(user_input)
        logger.info(f"Scrubbed PII from report input. Original length: {len(user_input)}, Scrubbed length: {len(scrubbed_input)}")
        
        result = self.report_qa_chain.invoke({"question": scrubbed_input})
        return result['text']
    
    @property
    def rag_chain(self):
        if not hasattr(self, '_rag_chain') or self._rag_chain is None:
            logger.info("Chatbot: Initializing RAG chain")
            retriever = self.db.as_retriever(search_kwargs={"k": 3})
            
            contextualize_q_system_prompt = """Given a chat history and the latest user question \
            which might reference context in the chat history, formulate a standalone question \
            which can be understood without the chat history. Do NOT answer the question, \
            just reformulate it if needed and otherwise return it as is."""
            contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", contextualize_q_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
            
            history_aware_retriever = create_history_aware_retriever(
                self.llm, retriever, contextualize_q_prompt)
            
            qa_system_prompt = """
            You are a helpful clinical assistant. Your role is to answer questions and explain medical terms simply, based ONLY on the provided context.

            STRICT MEDICAL ETHICS RULES:
            1. NO PREDICTIONS: Do not predict future health outcomes.
            2. NO SOLUTIONS: Do not suggest medical treatments.
            3. PURE EXPLANATION: Focus on simplifying information for the user.
            4. ALWAYS end with: "Doctor recommendation is required for better understanding".

            PRIVACY RULE: 
            - Replace any real names with "Patient".

            KNOWLEDGE CONTEXT:
            {context}
            """
            qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", qa_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
            
            question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
            self._rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
            logger.info("Chatbot: RAG chain initialized successfully")
        return self._rag_chain

    def get_chatbot_answer_with_context(self, question):
        import time
        import traceback
        start_time = time.time()
        try:
            # Scrub PII
            question = self.scrub_pii(question)
            logger.info(f"Chatbot: Processing question: {question}")
            
            # Using the cached rag_chain property
            rag_chain = self.rag_chain
            
            logger.info(f"Chatbot: Invoking RAG chain...")
            invoke_start = time.time()
            ai_msg_1 = rag_chain.invoke({"input": question, "chat_history": self.chat_history})
            logger.info(f"Chatbot: RAG chain invocation took {time.time() - invoke_start:.2f}s")
            
            self.chat_history.extend([HumanMessage(content=question), AIMessage(content=str(ai_msg_1["answer"]))])
            logger.info(f"Chatbot: Total processing time: {time.time() - start_time:.2f}s")
            return ai_msg_1["answer"]
        except Exception as e:
            logger.info(f"Chatbot: ERROR - {str(e)}")
            logger.info(traceback.format_exc())
            return f"Error occurred while processing your request: {str(e)}"

    async def get_chatbot_answer_with_context_stream(self, question):
        import traceback
        try:
            # Scrub PII
            question = self.scrub_pii(question)
            logger.info(f"Chatbot: Starting stream for question: {question}")
            # Ensure rag_chain is initialized
            _ = self.rag_chain
            
            full_response = ""
            async for chunk in self.rag_chain.astream({"input": question, "chat_history": self.chat_history}):
                if "answer" in chunk:
                    answer_chunk = chunk["answer"]
                    full_response += answer_chunk
                    yield answer_chunk
            
            self.chat_history.extend([HumanMessage(content=question), AIMessage(content=str(full_response))])
            logger.info("Chatbot: Stream completed")
        except Exception as e:
            logger.info(f"Chatbot: Stream ERROR - {str(e)}")
            logger.info(traceback.format_exc())
            yield f"Error: {str(e)}"
    
