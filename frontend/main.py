from flask import Flask, request, jsonify, render_template, send_file
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import requests
import pytesseract
from PIL import Image
import io
from time import sleep
import markdown2 as md
import csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import fitz  # PyMuPDF

def extract_text_from_file(file):
    # Check if it's a PDF
    if file.filename.lower().endswith('.pdf'):
        text = ""
        # Read the file data into memory
        file_bytes = file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
        # Reset file pointer just in case
        file.seek(0)
        return text
    else:
        # Assume it's an image
        img = Image.open(file)
        text = pytesseract.image_to_string(img)
        return text

@app.route('/reports', methods=['GET'])
def reports():
    return render_template('reports.html')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/text', methods=['GET'])
def text_simplifier():
    return render_template('text.html')

@app.route('/chat', methods=['GET'])
def chat():
    rest_api_url = 'http://127.0.0.1:8000/simplify_reset_context'
    response = requests.get(rest_api_url)
    return render_template('chat.html')

@app.route('/chat-interaction/', methods=['POST'])
def chat_interaction():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        def generate():
            rest_api_url = 'http://127.0.0.1:8000/simplify_text_llm_stream'
            with requests.post(rest_api_url, json={'input': user_message}, stream=True) as r:
                for chunk in r.iter_content(chunk_size=None):
                    if chunk:
                        yield chunk.decode('utf-8')
        
        return app.response_class(generate(), mimetype='text/plain')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload-pdf/', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        extracted_text = extract_text_from_file(file)
        
        rest_api_url = 'http://127.0.0.1:8000/simplify_report_llm'
        response = requests.post(rest_api_url, json={'input': extracted_text})

        if response.status_code == 200:
            return jsonify({'simplified_text': md.markdown(response.json())})
        else:
            return jsonify({'error': 'Failed to get simplified text'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload-text/', methods=['POST'])
def upload_text():
    data = request.get_json()
    medical_text = data.get('medical_text')

    if not medical_text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        rest_api_url = 'http://127.0.0.1:8000/simplify_data'
        response = requests.post(rest_api_url, json={'input': medical_text})

        if response.status_code == 200:
            return jsonify({'simplified_text': md.markdown(response.json())})
        else:
            return jsonify({'error': 'Failed to get simplified text'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/jargon', methods=['GET'])
def jargon():
    try:
        rest_api_url = 'http://127.0.0.1:8000/feedback_random'
        response = requests.get(rest_api_url)
        data = response.json()
        return render_template('jargon.html', data=data)
    except Exception as e:
        return render_template('jargon.html')

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    feedback = data.get('feedback')
    uuid = data.get('uuid')

    if not feedback or not uuid:
        return jsonify({'error': 'Feedback or UUID not provided'}), 400
    try:
        rest_api_url = 'http://127.0.0.1:8000/get_feedback'
        response = requests.get(rest_api_url, params={'feedback': feedback, 'uuid': uuid})
        if response.status_code == 200:
            return jsonify({'message': 'Feedback submitted successfully'})
        else:
            return jsonify({'error': 'Failed to submit feedback'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/translate-and-speak/', methods=['POST'])
def translate_and_speak():
    data = request.get_json()
    text_to_translate = data.get('text', '')
    target_language = 'ne'  # Nepali as the default target language

    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        translated_text = translator.translate(text_to_translate)

        tts = gTTS(text=translated_text, lang=target_language)
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)

        return send_file(audio_file, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
