# D:\SmartQuizzer\backend\services\ai_service.py (FINAL WORKING GEMINI CODE)
# D:\SmartQuizzer\backend\services\ai_service.py (FINAL WORKING GEMINI CODE)

# import os
# import json
# import requests 
# import PyPDF2 
# import nltk
# from nltk.tokenize import sent_tokenize 
# from bs4 import BeautifulSoup
# import io 
# import random

# # --- IMPORT Gemini SDK ---
# import google.generativeai as genai 
# from google.generativeai import types

# # Define a SAFE exception class for error handling 
# class GeminiAPIError(Exception):
#     """Placeholder for APIError."""
#     pass
# # -------------------------

# # --- NLP DEPENDENCY CHECK ---
# try:
#     nltk.data.find('tokenizers/punkt')
# except nltk.downloader.DownloadError:
#     print("Downloading NLTK 'punkt' data...")
#     nltk.download('punkt')
# # ----------------------------

# class AIService:
    
#     def __init__(self):
#         # Initializes the GenerativeModel object directly. 
#         # The key is automatically read from the GEMINI_API_KEY environment variable.
#         self.model = genai.GenerativeModel('gemini-2.5-flash') 

#     # --- MODULE 2: CONTENT INGESTION & PARSING (Retained) ---
    
#     def process_content(self, raw_text: str):
#         """ Cleans and segments raw text into knowledge chunks (sentences). """
#         cleaned_text = ' '.join(raw_text.split()).strip()
#         if not cleaned_text or len(cleaned_text) < 30:
#             return []
#         sentences = sent_tokenize(cleaned_text)
#         return sentences

#     def extract_text_from_pdf(self, file_stream) -> str:
#         """Extracts text from a PDF file stream."""
#         text = ""
#         try:
#             reader = PyPDF2.PdfReader(file_stream)
#             for page in reader.pages:
#                 text += page.extract_text() or ""
#         except Exception as e:
#             print(f"Error reading PDF: {e}")
#             return ""
#         return text

#     def fetch_and_extract_text_from_url(self, url: str) -> str:
#         """Fetches a URL, scrapes the main content, and returns clean text."""
#         try:
#             headers = {'User-Agent': 'Mozilla/5.0'}
#             response = requests.get(url, headers=headers, timeout=15)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.content, 'html.parser')
#             main_content = soup.find('main') or soup.find('article') or soup.body
            
#             if main_content:
#                 text = main_content.get_text(separator=' ', strip=True)
#             else:
#                 text = soup.body.get_text(separator=' ', strip=True) if soup.body else ""
                
#             return text.strip()
        
#         except requests.exceptions.RequestException as e:
#             print(f"Error fetching URL: {e}")
#             return ""


#     # --- MODULE 3: AI QUESTION GENERATION (Gemini Implementation) ---

#     def generate_quiz_question(self, content_chunk: str, question_type: str, subject: str, difficulty: str):
#         """
#         Uses Gemini to generate a single structured question based on a chunk.
#         """
        
#         # 1. Define the dynamic output schema based on question type
#         if question_type == "MCQ":
#             json_schema = {
#                 "type": "object",
#                 "properties": {
#                     "type": {"type": "string", "enum": ["MCQ"]},
#                     "question": {"type": "string"},
#                     "options": {"type": "array", "items": {"type": "string"}}, 
#                     "answer": {"type": "string", "description": "The text of the correct option."},
#                     "explanation": {"type": "string"}
#                 },
#                 "required": ["type", "question", "options", "answer", "explanation"]
#             }
#         elif question_type == "True/False":
#             json_schema = {
#                 "type": "object",
#                 "properties": {
#                     "type": {"type": "string", "enum": ["True/False"]},
#                     "question": {"type": "string", "description": "A statement to be judged true or false."},
#                     "answer": {"type": "string", "enum": ["True", "False"]},
#                     "explanation": {"type": "string"}
#                 },
#                 "required": ["type", "question", "answer", "explanation"]
#             }
#         elif question_type == "Fill-up":
#             json_schema = {
#                 "type": "object",
#                 "properties": {
#                     "type": {"type": "string", "enum": ["Fill-up"]},
#                     "question": {"type": "string", "description": "Sentence with a single blank space, indicated by [BLANK]."},
#                     "answer": {"type": "string", "description": "The single word or short phrase that fills the blank."},
#                     "explanation": {"type": "string"}
#                 },
#                 "required": ["type", "question", "answer", "explanation"]
#             }
#         elif question_type == "Short Answer":
#              json_schema = {
#                 "type": "object",
#                 "properties": {
#                     "type": {"type": "string", "enum": ["Short Answer"]},
#                     "question": {"type": "string", "description": "A direct, open-ended question."},
#                     "answer": {"type": "string", "description": "The concise, factual answer (max 5 words)."},
#                     "explanation": {"type": "string"}
#                 },
#                 "required": ["type", "question", "answer", "explanation"]
#             }
#         else:
#             return None 

#         # 2. Map Difficulty and Craft the Prompt (Bloom's Taxonomy)
#         bloom_mapping = {
#             "Beginner": "Recall or Comprehension (Bloom's Taxonomy Level 1-2).",
#             "Intermediate": "Application or Analysis (Bloom's Taxonomy Level 3-4).",
#             "Expert": "Evaluation or Creation (Bloom's Taxonomy Level 5-6).",
#         }
#         bloom_level = bloom_mapping.get(difficulty, "Application")

#         prompt = (
#             f"Generate one high-quality, {question_type} question based ONLY on the text chunk provided. "
#             f"Subject: '{subject}'. Difficulty: '{difficulty}' ({bloom_level}). "
#             f"Ensure the question tests the required Bloom's level. "
#             f"Text Chunk: \"{content_chunk}\" "
#             f"Output must be a single JSON object."
#         )
        
#         try:
#             # 3. Call the Gemini API using the model object
#             response = self.model.generate_content(
#                 contents=prompt,
#                 # FIX: Use the 'generation_config' dictionary to pass structured output parameters
#                 generation_config={
#                     "response_mime_type": "application/json",
#                     "response_schema": json_schema
#                 }
#             )
            
#             # The response text is guaranteed to be a valid JSON string matching the schema
#             return json.loads(response.text)
            
#         except Exception as e:
#             # Catch all errors (e.g., API key invalid, rate limit)
#             print(f"Gemini API Error: {e}")
#             return None








# D:\SmartQuizzer\backend\services\ai_service.py (FINAL WORKING GEMINI CODE)

import os
import json
import requests 
import PyPDF2 
import nltk
from nltk.tokenize import sent_tokenize 
from bs4 import BeautifulSoup
import io 
import random

# --- IMPORT Gemini SDK ---
import google.generativeai as genai 
from google.generativeai import types

# Define a SAFE exception class for error handling 
class GeminiAPIError(Exception):
    """Placeholder for APIError."""
    pass
# -------------------------

# --- NLP DEPENDENCY CHECK ---
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    print("Downloading NLTK 'punkt' data...")
    nltk.download('punkt')
# ----------------------------

class AIService:
    
    def __init__(self):
        # Initializes the GenerativeModel object directly. 
        self.model = genai.GenerativeModel('gemini-2.5-flash') 

    # --- MODULE 2: CONTENT INGESTION & PARSING (Retained) ---
    
    def process_content(self, raw_text: str):
        """ Cleans and segments raw text into knowledge chunks (sentences). """
        cleaned_text = ' '.join(raw_text.split()).strip()
        if not cleaned_text or len(cleaned_text) < 30:
            return []
        sentences = sent_tokenize(cleaned_text)
        return sentences

    def extract_text_from_pdf(self, file_stream) -> str:
        """Extracts text from a PDF file stream."""
        text = ""
        try:
            reader = PyPDF2.PdfReader(file_stream)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
        return text

    def fetch_and_extract_text_from_url(self, url: str) -> str:
        """Fetches a URL, scrapes the main content, and returns clean text."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            main_content = soup.find('main') or soup.find('article') or soup.body
            
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
            else:
                text = soup.body.get_text(separator=' ', strip=True) if soup.body else ""
                
            return text.strip()
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return ""


    # --- MODULE 3: AI QUESTION GENERATION (Structured Output) ---

    def generate_quiz_question(self, content_chunk: str, question_type: str, subject: str, difficulty: str):
        """
        Uses Gemini to generate a single structured question based on a chunk.
        """
        
        # 1. Define the dynamic output schema based on question type
        if question_type == "MCQ":
            json_schema = {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["MCQ"]},
                    "question": {"type": "string"},
                    "options": {"type": "array", "items": {"type": "string"}}, 
                    "answer": {"type": "string", "description": "The text of the correct option."},
                    "explanation": {"type": "string"}
                },
                "required": ["type", "question", "options", "answer", "explanation"]
            }
        elif question_type == "True/False":
            json_schema = {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["True/False"]},
                    "question": {"type": "string", "description": "A statement to be judged true or false."},
                    "answer": {"type": "string", "enum": ["True", "False"]},
                    "explanation": {"type": "string"}
                },
                "required": ["type", "question", "answer", "explanation"]
            }
        elif question_type == "Fill-up":
            json_schema = {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["Fill-up"]},
                    "question": {"type": "string", "description": "Sentence with a single blank space, indicated by [BLANK]."},
                    "answer": {"type": "string", "description": "The single word or short phrase that fills the blank."},
                    "explanation": {"type": "string"}
                },
                "required": ["type", "question", "answer", "explanation"]
            }
        elif question_type == "Short Answer":
             json_schema = {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["Short Answer"]},
                    "question": {"type": "string", "description": "A direct, open-ended question."},
                    "answer": {"type": "string", "description": "The concise, factual answer (max 5 words)."},
                    "explanation": {"type": "string"}
                },
                "required": ["type", "question", "answer", "explanation"]
            }
        else:
            return None 

        # 2. Map Difficulty and Craft the Prompt (Bloom's Taxonomy)
        bloom_mapping = {
            "Beginner": "Recall or Comprehension (Bloom's Taxonomy Level 1-2).",
            "Intermediate": "Application or Analysis (Bloom's Taxonomy Level 3-4).",
            "Expert": "Evaluation or Creation (Bloom's Taxonomy Level 5-6).",
        }
        bloom_level = bloom_mapping.get(difficulty, "Application")

        prompt = (
            f"Generate one high-quality, {question_type} question based ONLY on the text chunk provided. "
            f"Subject: '{subject}'. Difficulty: '{difficulty}' ({bloom_level}). "
            f"Ensure the question tests the required Bloom's level. "
            f"Text Chunk: \"{content_chunk}\" "
            f"Output must be a single JSON object."
        )
        
        try:
            # 3. Call the Gemini API using the model object
            response = self.model.generate_content(
                contents=prompt,
                # FIX: Use the 'generation_config' dictionary to pass structured output parameters
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": json_schema
                }
            )
            
            # The response text is guaranteed to be a valid JSON string matching the schema
            return json.loads(response.text)
            
        except Exception as e:
            # Catch all errors (e.g., API key invalid, rate limit)
            print(f"Gemini API Error: {e}")
            return None

    # --- MODULE 7: VOICE COACHING TEXT GENERATION ---

    def generate_coaching_text(self, prompt: str) -> str:
        """
        Uses Gemini to generate free-form text output (the coaching message).
        Returns the text response.
        """
        try:
            # Call the Gemini API without structured JSON constraints
            response = self.model.generate_content(
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            # Re-raise the exception so the calling Flask route can handle the 500 error
            raise e