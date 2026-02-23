# # D:\SmartQuizzer\backend\app.py

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# # Allow cross-origin requests from the Vue.js frontend
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     # Ensure email is unique and indexed for fast lookups
#     users_collection.create_index("email", unique=True)
#     print("Successfully connected to MongoDB and ensured 'email' index.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     # Exit or handle gracefully if DB connection fails
#     exit(1)

# # --- API Endpoints: Module 1 ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     if users_collection.find_one({"email": email}):
#         return jsonify({"msg": "User with this email already exists"}), 409

#     # Hash the password for secure storage
#     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

#     # Default profile settings
#     user_data = {
#         "email": email,
#         "password": hashed_password,
#         "subjects_of_interest": [],
#         "difficulty_level": "Beginner",
#         "performance_history": [],
#         "created_at": datetime.now()
#     }
    
#     users_collection.insert_one(user_data)
    
#     # Log the user in immediately after registration
#     access_token = create_access_token(identity=email)
#     return jsonify(access_token=access_token), 201

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     user = users_collection.find_one({"email": email})

#     if user and bcrypt.check_password_hash(user['password'], password):
#         # Create a JWT for the user
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     # Get the user's identity from the JWT
#     current_user_email = get_jwt_identity() 
    
#     # Retrieve user data, excluding the sensitive password hash
#     user = users_collection.find_one({"email": current_user_email}, {"password": 0})
    
#     if user:
#         # Convert MongoDB's ObjectId to a string for JSON serialization
#         user['_id'] = str(user['_id'])
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Filter for valid, updatable fields
#     updatable_fields = {}
#     if 'subjects_of_interest' in data:
#         # Simple validation: expect a list of strings
#         if isinstance(data['subjects_of_interest'], list):
#             updatable_fields['subjects_of_interest'] = [s.strip() for s in data['subjects_of_interest'] if s.strip()]
#     if 'difficulty_level' in data and data['difficulty_level'] in ["Beginner", "Intermediate", "Expert"]:
#         updatable_fields['difficulty_level'] = data['difficulty_level']

#     if not updatable_fields:
#         return jsonify({"msg": "No valid fields provided for update"}), 400

#     # Update the user document in MongoDB
#     result = users_collection.update_one(
#         {"email": current_user_email},
#         {"$set": updatable_fields}
#     )

#     if result.modified_count == 1:
#         return jsonify({"msg": "Profile updated successfully"}), 200
    
#     # Return 200 even if no fields were modified, as the request was technically valid
#     return jsonify({"msg": "User found but no changes applied"}), 200


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)





# D:\SmartQuizzer\backend\app.py

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os # Included for file handling

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}
# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] # <-- NEW COLLECTION
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) # <-- MODIFIED
#     ai_service = AIService() # <-- NEW SERVICE
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     title = request.form.get('title', 'Untitled Content')
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title,
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)







# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random # <-- Added for Route 8

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] # <-- NEW COLLECTION
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) # <-- MODIFIED
#     ai_service = AIService() # <-- NEW SERVICE
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     title = request.form.get('title', 'Untitled Content')
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title,
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3)
# # CRITICAL FIX: Method is POST and uses content_id from the path.
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json() # Get the data from the POST body
#     question_type = data.get('question_type') # Retrieves the question type
    
#     # Check if essential parameters are present
#     if not question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400
    
#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     # 2. Select a Random Knowledge Chunk
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     random_chunk = random.choice(knowledge_chunks) 
    
#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=random_chunk, 
#         question_type=question_type, # Pass the type from the frontend POST body
#         subject=subject, 
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = random_chunk
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         # This occurs if the LLM call fails (e.g., bad API key, rate limit, JSON parsing failure)
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)







# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 # MODULE 4: Added for reliable chunk hashing

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json() 
#     question_type = data.get('question_type') 
    
#     if not question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400
    
#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     # 2. Select a Random Knowledge Chunk
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     random_chunk = random.choice(knowledge_chunks) 
    
#     # 3. Get Preferences
#     # FIX: Ensure we extract the specific title for the subject prompt
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=random_chunk, 
#         question_type=question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = random_chunk
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)








# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 # MODULE 4: Added for reliable chunk hashing

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService # <-- NEW IMPORT
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # <-- Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection) # <-- NEW SERVICE INSTANTIATED
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     # 1. Identify Weakest Chunk: (Placeholder for now, using random for MVP)
#     weakest_chunk_data = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weakest_chunk_data and weakest_chunk_data.get('correct_rate', 1.0) < 0.7:
#         # NOTE: In a complete implementation, we'd use the chunk_hash to find the exact text
#         print(f"ADAPTIVE: Targeting chunk with correct rate: {weakest_chunk_data['correct_rate'] * 100:.2f}%")
#     else:
#         print("ADAPTIVE: No significant weakness found, selecting random chunk.")
    
#     # FIX: We use a simple random choice for now, as the full adaptive logic requires mapping hash back to text.
#     random_chunk = random.choice(knowledge_chunks) 
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=random_chunk, 
#         question_type=requested_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = random_chunk
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)













# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService # <-- NEW IMPORT
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # <-- Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) # <-- CRITICAL FIX: Pass BOTH collections
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting weakness (Score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=requested_question_type, 
#         subject=subject, 
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)






# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 # MODULE 4: Added for reliable chunk hashing

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService # <-- NEW IMPORT
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # <-- Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) # <-- CRITICAL FIX: Pass BOTH collections
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)









# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 # MODULE 4: Added for reliable chunk hashing

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService # <-- NEW IMPORT
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # <-- Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) # CRITICAL FIX: Pass BOTH collections
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)









# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService # <-- NEW IMPORT
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # <-- Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) # CRITICAL FIX: Pass BOTH collections
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201

# # --- API Endpoints: Module 6 (Analytics) ---

# ## 10. Get User Performance History for Analytics (Module 6)
# @app.route('/api/analytics/performance', methods=['GET'])
# @jwt_required()
# def get_performance_analytics():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch the last 20 answers submitted by the user (chronological order)
#     performance_data = list(db["quiz_history"].find(
#         {"user_id": user['_id']},
#         # Sort by timestamp (most recent first), and limit to the last 20 interactions
#     ).sort("timestamp", -1).limit(20))

#     # 2. Process data for visualization (reverse to show oldest to newest)
#     processed_data = []
    
#     for log in reversed(performance_data):
#         processed_data.append({
#             "is_correct": log['is_correct'],
#             "question_type": log['question_type'],
#             "time_taken_ms": log.get('time_taken_ms', 0),
#             "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
#         })

#     return jsonify(processed_data), 200

# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)









# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService 
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] 
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) 
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201

# # --- API Endpoints: Module 6 (Analytics) ---

# ## 10. Get User Performance History for Analytics (Module 6)
# @app.route('/api/analytics/performance', methods=['GET'])
# @jwt_required()
# def get_performance_analytics():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch the last 20 answers submitted by the user (chronological order)
#     performance_data = list(db["quiz_history"].find(
#         {"user_id": user['_id']},
#         # Sort by timestamp (most recent first), and limit to the last 20 interactions
#     ).sort("timestamp", -1).limit(20))

#     # 2. Process data for visualization (reverse to show oldest to newest)
#     processed_data = []
    
#     for log in reversed(performance_data):
#         processed_data.append({
#             "is_correct": log['is_correct'],
#             "question_type": log['question_type'],
#             "time_taken_ms": log.get('time_taken_ms', 0),
#             "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
#         })

#     return jsonify(processed_data), 200

# # --- API Endpoints: Module 7 (Voice Coaching) ---

# ## 11. Generate Voice Suggestion Text (Module 7)
# @app.route('/api/coaching/suggest', methods=['POST'])
# @jwt_required()
# def generate_coaching_suggestion():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     quiz_results = data.get('quiz_results') # Array of questions from the store
#     total_correct = data.get('total_correct')
#     total_answered = data.get('total_answered')

#     if not quiz_results or total_answered == 0:
#         return jsonify({"msg": "No quiz data provided for analysis."}), 400

#     # 1. Summarize Weaknesses (Top 3 failed topics/chunks)
#     # We'll rely on the frontend sending the simple summary.
    
#     # 2. Extract specific failure points (e.g., failed on chunk X, Y, Z)
#     failure_data = []
#     for q in quiz_results:
#         # Check if the question was answered (isCorrect field exists) and if it was False
#         if 'isCorrect' in q and q['isCorrect'] == False: 
#             failure_data.append({
#                 'type': q['type'],
#                 'chunk_preview': q['content_chunk'][:40] + '...',
#                 'question': q['question']
#             })

#     # 3. Call the AI Service to generate personalized text
    
#     # Generate the prompt for the AI
#     prompt = (
#         f"You are a supportive, insightful learning coach. Analyze the user's recent quiz performance. "
#         f"Overall Score: {total_correct}/{total_answered}. "
#         f"Primary Difficulty Level: {user.get('difficulty_level', 'Intermediate')}. "
#         f"Based on the following {len(failure_data)} failure points, generate a brief (max 100 words) motivational suggestion. "
#         f"Your response must include:\n"
#         f"1. A motivational opening.\n"
#         f"2. A summary of their mistake area (e.g., 'You struggled with Fill-in-the-Blank questions on topic X').\n"
#         f"3. A clear, actionable suggestion on what specific topic or question type to focus on next. "
#         f"FAILURE DATA: {failure_data}"
#     )

#     # Call the AI service (using the existing generation function, but simplifying the JSON schema request)
#     try:
#         response_text = ai_service.generate_coaching_text(prompt)
#     except Exception as e:
#         print(f"Coaching AI call failed: {e}")
#         return jsonify({"msg": "AI coaching generation failed."}), 500

#     return jsonify({"suggestion_text": response_text}), 200


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)


















































# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService # <-- NEW IMPORT
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # <-- Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) # CRITICAL FIX: Pass BOTH collections
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201

# # --- API Endpoints: Module 6 (Analytics) ---

# ## 10. Get User Performance History for Analytics (Module 6)
# @app.route('/api/analytics/performance', methods=['GET'])
# @jwt_required()
# def get_performance_analytics():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch the last 20 answers submitted by the user (chronological order)
#     performance_data = list(db["quiz_history"].find(
#         {"user_id": user['_id']},
#         # Sort by timestamp (most recent first), and limit to the last 20 interactions
#     ).sort("timestamp", -1).limit(20))

#     # 2. Process data for visualization (reverse to show oldest to newest)
#     processed_data = []
    
#     for log in reversed(performance_data):
#         processed_data.append({
#             "is_correct": log['is_correct'],
#             "question_type": log['question_type'],
#             "time_taken_ms": log.get('time_taken_ms', 0),
#             "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
#         })

#     return jsonify(processed_data), 200

# # --- API Endpoints: Module 7 (Voice Coaching) ---

# ## 11. Generate Voice Suggestion Text (Module 7)
# @app.route('/api/coaching/suggest', methods=['POST'])
# @jwt_required()
# def generate_coaching_suggestion():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     quiz_results = data.get('quiz_results') # Array of questions from the store
#     total_correct = data.get('total_correct')
#     total_answered = data.get('total_answered')

#     if not quiz_results or total_answered == 0:
#         return jsonify({"msg": "No quiz data provided for analysis."}), 400

#     # 1. Summarize Weaknesses (Top 3 failed topics/chunks)
#     # We'll rely on the frontend sending the simple summary.
    
#     # 2. Extract specific failure points (e.g., failed on chunk X, Y, Z)
#     failure_data = []
#     for q in quiz_results:
#         # Check if the question was answered (isCorrect field exists) and if it was False
#         if 'isCorrect' in q and q['isCorrect'] == False: 
#             failure_data.append({
#                 'type': q['type'],
#                 'chunk_preview': q['content_chunk'][:40] + '...',
#                 'question': q['question']
#             })

#     # 3. Call the AI Service to generate personalized text
    
#     # Generate the prompt for the AI
#     prompt = (
#         f"You are a supportive, insightful learning coach. Analyze the user's recent quiz performance. "
#         f"Overall Score: {total_correct}/{total_answered}. "
#         f"Primary Difficulty Level: {user.get('difficulty_level', 'Intermediate')}. "
#         f"Based on the following {len(failure_data)} failure points, generate a brief (max 100 words) motivational suggestion. "
#         f"Your response must include:\n"
#         f"1. A motivational opening.\n"
#         f"2. A summary of their mistake area (e.g., 'You struggled with Fill-in-the-Blank questions on topic X').\n"
#         f"3. A clear, actionable suggestion on what specific topic or question type to focus on next. "
#         f"FAILURE DATA: {failure_data}"
#     )

#     # Call the AI service (using the existing generation function, but simplifying the JSON schema request)
#     try:
#         response_text = ai_service.generate_coaching_text(prompt)
#     except Exception as e:
#         print(f"Coaching AI call failed: {e}")
#         return jsonify({"msg": "AI coaching generation failed."}), 500

#     return jsonify({"suggestion_text": response_text}), 200


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)



































# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService 
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] 
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) 
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201

# # --- API Endpoints: Module 6 (Analytics) ---

# ## 10. Get User Performance History for Analytics (Module 6)
# @app.route('/api/analytics/performance', methods=['GET'])
# @jwt_required()
# def get_performance_analytics():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch the last 20 answers submitted by the user (chronological order)
#     performance_data = list(db["quiz_history"].find(
#         {"user_id": user['_id']},
#         # Sort by timestamp (most recent first), and limit to the last 20 interactions
#     ).sort("timestamp", -1).limit(20))

#     # 2. Process data for visualization (reverse to show oldest to newest)
#     processed_data = []
    
#     for log in reversed(performance_data):
#         processed_data.append({
#             "is_correct": log['is_correct'],
#             "question_type": log['question_type'],
#             "time_taken_ms": log.get('time_taken_ms', 0),
#             "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
#         })

#     return jsonify(processed_data), 200

# # --- API Endpoints: Module 7 (Voice Coaching) ---

# ## 11. Generate Voice Suggestion Text (Module 7)
# @app.route('/api/coaching/suggest', methods=['POST'])
# @jwt_required()
# def generate_coaching_suggestion():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     quiz_results = data.get('quiz_results') # Array of questions from the store
#     total_correct = data.get('total_correct')
#     total_answered = data.get('total_answered')

#     if not quiz_results or total_answered == 0:
#         return jsonify({"msg": "No quiz data provided for analysis."}), 400

#     # 1. Summarize Weaknesses (Top 3 failed topics/chunks)
#     # We'll rely on the frontend sending the simple summary.
    
#     # 2. Extract specific failure points (e.g., failed on chunk X, Y, Z)
#     failure_data = []
#     for q in quiz_results:
#         # Check if the question was answered (isCorrect field exists) and if it was False
#         if 'isCorrect' in q and q['isCorrect'] == False: 
#             failure_data.append({
#                 'type': q['type'],
#                 'chunk_preview': q['content_chunk'][:40] + '...',
#                 'question': q['question']
#             })

#     # 3. Call the AI Service to generate personalized text
    
#     # Generate the prompt for the AI
#     prompt = (
#         f"You are a supportive, insightful learning coach. Analyze the user's recent quiz performance. "
#         f"Overall Score: {total_correct}/{total_answered}. "
#         f"Primary Difficulty Level: {user.get('difficulty_level', 'Intermediate')}. "
#         f"Based on the following {len(failure_data)} failure points, generate a brief (max 100 words) motivational suggestion. "
#         f"Your response must include:\n"
#         f"1. A motivational opening.\n"
#         f"2. A summary of their mistake area (e.g., 'You struggled with Fill-in-the-Blank questions on topic X').\n"
#         f"3. A clear, actionable suggestion on what specific topic or question type to focus on next. "
#         f"FAILURE DATA: {failure_data}"
#     )

#     # Call the AI service (using the existing generation function, but simplifying the JSON schema request)
#     try:
#         response_text = ai_service.generate_coaching_text(prompt)
#     except Exception as e:
#         print(f"Coaching AI call failed: {e}")
#         return jsonify({"msg": "AI coaching generation failed."}), 500

#     return jsonify({"suggestion_text": response_text}), 200


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)










# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService 
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) 
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201

# # --- API Endpoints: Module 6 (Analytics) ---

# ## 10. Get User Performance History for Analytics (Module 6)
# @app.route('/api/analytics/performance', methods=['GET'])
# @jwt_required()
# def get_performance_analytics():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch the last 20 answers submitted by the user (chronological order)
#     performance_data = list(db["quiz_history"].find(
#         {"user_id": user['_id']},
#         # Sort by timestamp (most recent first), and limit to the last 20 interactions
#     ).sort("timestamp", -1).limit(20))

#     # 2. Process data for visualization (reverse to show oldest to newest)
#     processed_data = []
    
#     for log in reversed(performance_data):
#         processed_data.append({
#             "is_correct": log['is_correct'],
#             "question_type": log['question_type'],
#             "time_taken_ms": log.get('time_taken_ms', 0),
#             "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
#         })

#     return jsonify(processed_data), 200

# # --- API Endpoints: Module 7 (Voice Coaching) ---

# ## 11. Generate Voice Suggestion Text (Module 7)
# @app.route('/api/coaching/suggest', methods=['POST'])
# @jwt_required()
# def generate_coaching_suggestion():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     quiz_results = data.get('quiz_results') # Array of questions from the store
#     total_correct = data.get('total_correct')
#     total_answered = data.get('total_answered')

#     if not quiz_results or total_answered == 0:
#         return jsonify({"msg": "No quiz data provided for analysis."}), 400

#     # 1. Summarize Weaknesses (Top 3 failed topics/chunks)
#     # We'll rely on the frontend sending the simple summary.
    
#     # 2. Extract specific failure points (e.g., failed on chunk X, Y, Z)
#     failure_data = []
#     for q in quiz_results:
#         # Check if the question was answered (isCorrect field exists) and if it was False
#         if 'isCorrect' in q and q['isCorrect'] == False: 
#             failure_data.append({
#                 'type': q['type'],
#                 'chunk_preview': q['content_chunk'][:40] + '...',
#                 'question': q['question']
#             })

#     # 3. Call the AI Service to generate personalized text
    
#     # Generate the prompt for the AI
#     prompt = (
#         f"You are a supportive, insightful learning coach. Analyze the user's recent quiz performance. "
#         f"Overall Score: {total_correct}/{total_answered}. "
#         f"Primary Difficulty Level: {user.get('difficulty_level', 'Intermediate')}. "
#         f"Based on the following {len(failure_data)} failure points, generate a brief (max 100 words) motivational suggestion. "
#         f"Your response must include:\n"
#         f"1. A motivational opening.\n"
#         f"2. A summary of their mistake area (e.g., 'You struggled with Fill-in-the-Blank questions on topic X').\n"
#         f"3. A clear, actionable suggestion on what specific topic or question type to focus on next. "
#         f"FAILURE DATA: {failure_data}"
#     )

#     # Call the AI service (using the existing generation function, but simplifying the JSON schema request)
#     try:
#         response_text = ai_service.generate_coaching_text(prompt)
#     except Exception as e:
#         print(f"Coaching AI call failed: {e}")
#         return jsonify({"msg": "AI coaching generation failed."}), 500

#     return jsonify({"suggestion_text": response_text}), 200


# # --- API Endpoints: Module 6 (Admin Dashboard) ---

# ## 12. Get Admin-Level System Statistics (Module 6)
# @app.route('/api/admin/stats', methods=['GET'])
# @jwt_required()
# def get_admin_stats():
#     # NOTE: In a real application, you would add logic here to check if the user 
#     # making the request has an 'admin' role. For MVP, we skip the role check.

#     try:
#         # 1. Total User Count
#         total_users = db["users"].count_documents({})

#         # 2. Total Quizzes/Interactions Logged
#         total_interactions = db["quiz_history"].count_documents({})
        
#         # 3. Total Content Chunks Uploaded
#         total_content = user_service.contents_collection.count_documents({})

#         # 4. Overall Accuracy (Requires aggregation - simplified here for speed)
#         # We perform a quick aggregate to get the count of correct vs total attempts
#         accuracy_pipeline = [
#             {"$group": {
#                 "_id": None,
#                 "total_answered": {"$sum": 1},
#                 "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
#             }}
#         ]
#         accuracy_result = list(db["quiz_history"].aggregate(accuracy_pipeline))

#         overall_accuracy = 0
#         if accuracy_result and accuracy_result[0]['total_answered'] > 0:
#             overall_accuracy = round(
#                 (accuracy_result[0]['total_correct'] / accuracy_result[0]['total_answered']) * 100
#             )

#         return jsonify({
#             "total_users": total_users,
#             "total_interactions": total_interactions,
#             "total_content_items": total_content,
#             "overall_accuracy_percent": overall_accuracy
#         }), 200

#     except Exception as e:
#         print(f"Admin stats error: {e}")
#         return jsonify({"msg": "Failed to fetch admin stats."}), 500

# # --- API Endpoints: Module 6 (Admin Feedback) ---

# ## 13. Log Question Feedback/Flagging (Module 6)
# @app.route('/api/feedback/flag', methods=['POST'])
# @jwt_required()
# def log_question_flag():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS for moderation
#     question_id = data.get('question_id') # The ObjectId of the content chunk used
#     reason = data.get('reason', 'Inappropriate/Broken Content')
    
#     if not question_id:
#         return jsonify({"msg": "Missing question ID."}), 400

#     # 1. Prepare flag document
#     flag_data = {
#         "user_id": user['_id'],
#         "question_content_id": question_id,
#         "reason": reason,
#         "status": "Pending Review",
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated collection for moderation
#     db["moderation_queue"].insert_one(flag_data)
    
#     return jsonify({"msg": "Question flagged for review. Thank you for your feedback."}), 201


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)












# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService 
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) 
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Query MongoDB for contents belonging to this user
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ))

#     # Format the ObjectId and datetime for JSON serialization
#     for content in content_list:
#         # Convert ObjectId to string for JSON serialization
#         content['_id'] = str(content['_id'])
#         # Convert datetime object to string format
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201

# # --- API Endpoints: Module 6 (Analytics) ---

# ## 10. Get User Performance History for Analytics (Module 6)
# @app.route('/api/analytics/performance', methods=['GET'])
# @jwt_required()
# def get_performance_analytics():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch the last 20 answers submitted by the user (chronological order)
#     performance_data = list(db["quiz_history"].find(
#         {"user_id": user['_id']},
#         # Sort by timestamp (most recent first), and limit to the last 20 interactions
#     ).sort("timestamp", -1).limit(20))

#     # 2. Process data for visualization (reverse to show oldest to newest)
#     processed_data = []
    
#     for log in reversed(performance_data):
#         processed_data.append({
#             "is_correct": log['is_correct'],
#             "question_type": log['question_type'],
#             "time_taken_ms": log.get('time_taken_ms', 0),
#             "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
#         })

#     return jsonify(processed_data), 200

# # --- API Endpoints: Module 7 (Voice Coaching) ---

# ## 11. Generate Voice Suggestion Text (Module 7)
# @app.route('/api/coaching/suggest', methods=['POST'])
# @jwt_required()
# def generate_coaching_suggestion():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     quiz_results = data.get('quiz_results') # Array of questions from the store
#     total_correct = data.get('total_correct')
#     total_answered = data.get('total_answered')

#     if not quiz_results or total_answered == 0:
#         return jsonify({"msg": "No quiz data provided for analysis."}), 400

#     # 1. Summarize Weaknesses (Top 3 failed topics/chunks)
#     # We'll rely on the frontend sending the simple summary.
    
#     # 2. Extract specific failure points (e.g., failed on chunk X, Y, Z)
#     failure_data = []
#     for q in quiz_results:
#         # Check if the question was answered (isCorrect field exists) and if it was False
#         if 'isCorrect' in q and q['isCorrect'] == False: 
#             failure_data.append({
#                 'type': q['type'],
#                 'chunk_preview': q['content_chunk'][:40] + '...',
#                 'question': q['question']
#             })

#     # 3. Call the AI Service to generate personalized text
    
#     # Generate the prompt for the AI
#     prompt = (
#         f"You are a supportive, insightful learning coach. Analyze the user's recent quiz performance. "
#         f"Overall Score: {total_correct}/{total_answered}. "
#         f"Primary Difficulty Level: {user.get('difficulty_level', 'Intermediate')}. "
#         f"Based on the following {len(failure_data)} failure points, generate a brief (max 100 words) motivational suggestion. "
#         f"Your response must include:\n"
#         f"1. A motivational opening.\n"
#         f"2. A summary of their mistake area (e.g., 'You struggled with Fill-in-the-Blank questions on topic X').\n"
#         f"3. A clear, actionable suggestion on what specific topic or question type to focus on next. "
#         f"FAILURE DATA: {failure_data}"
#     )

#     # Call the AI service (using the existing generation function, but simplifying the JSON schema request)
#     try:
#         response_text = ai_service.generate_coaching_text(prompt)
#     except Exception as e:
#         print(f"Coaching AI call failed: {e}")
#         return jsonify({"msg": "AI coaching generation failed."}), 500

#     return jsonify({"suggestion_text": response_text}), 200


# # --- API Endpoints: Module 6 (Admin Dashboard) ---

# ## 12. Get Admin-Level System Statistics (Module 6)
# @app.route('/api/admin/stats', methods=['GET'])
# @jwt_required()
# def get_admin_stats():
#     # NOTE: In a real application, you would add logic here to check if the user 
#     # making the request has an 'admin' role. For MVP, we skip the role check.

#     try:
#         # 1. Total User Count
#         total_users = db["users"].count_documents({})

#         # 2. Total Quizzes/Interactions Logged
#         total_interactions = db["quiz_history"].count_documents({})
        
#         # 3. Total Content Chunks Uploaded
#         total_content = user_service.contents_collection.count_documents({})

#         # 4. Overall Accuracy (Requires aggregation - simplified here for speed)
#         # We perform a quick aggregate to get the count of correct vs total attempts
#         accuracy_pipeline = [
#             {"$group": {
#                 "_id": None,
#                 "total_answered": {"$sum": 1},
#                 "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
#             }}
#         ]
#         accuracy_result = list(db["quiz_history"].aggregate(accuracy_pipeline))

#         overall_accuracy = 0
#         if accuracy_result and accuracy_result[0]['total_answered'] > 0:
#             overall_accuracy = round(
#                 (accuracy_result[0]['total_correct'] / accuracy_result[0]['total_answered']) * 100
#             )

#         return jsonify({
#             "total_users": total_users,
#             "total_interactions": total_interactions,
#             "total_content_items": total_content,
#             "overall_accuracy_percent": overall_accuracy
#         }), 200

#     except Exception as e:
#         print(f"Admin stats error: {e}")
#         return jsonify({"msg": "Failed to fetch admin stats."}), 500

# # --- API Endpoints: Module 6 (Admin Feedback) ---

# ## 13. Log Question Feedback/Flagging (Module 6)
# @app.route('/api/feedback/flag', methods=['POST'])
# @jwt_required()
# def log_question_flag():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS for moderation
#     question_id = data.get('question_id') # The ObjectId of the content chunk used
#     reason = data.get('reason', 'Inappropriate/Broken Content')
    
#     if not question_id:
#         return jsonify({"msg": "Missing question ID."}), 400

#     # 1. Prepare flag document
#     flag_data = {
#         "user_id": user['_id'],
#         "question_content_id": question_id,
#         "reason": reason,
#         "status": "Pending Review",
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated collection for moderation
#     db["moderation_queue"].insert_one(flag_data)
    
#     return jsonify({"msg": "Question flagged for review. Thank you for your feedback."}), 201


# ## 14. Get Question Moderation Queue (Module 6)
# @app.route('/api/admin/moderation/queue', methods=['GET'])
# @jwt_required()
# def get_moderation_queue():
#     # NOTE: In a production app, we would enforce an 'admin' role check here.
    
#     try:
#         # Fetch all flagged items, newest first
#         queue_data = list(db["moderation_queue"].find(
#             {"status": "Pending Review"} # Filter for items needing attention
#         ).sort("timestamp", -1)) 

#         # Format ObjectIds and datetime for JSON serialization
#         for item in queue_data:
#             # We assume user_id is already a string here from the logging process
#             item['_id'] = str(item['_id'])
#             item['user_id'] = str(item.get('user_id', 'N/A')) # Use get to avoid crash if field is missing
#             item['timestamp'] = item['timestamp'].strftime("%Y-%m-%d %H:%M:%S")

#         return jsonify(queue_data), 200

#     except Exception as e:
#         print(f"Moderation queue fetch error: {e}")
#         return jsonify({"msg": "Failed to fetch moderation queue."}), 500


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)











# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService 
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) # CRITICAL FIX: Pass BOTH collections
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch content, sorting by 'created_at' descending (-1)
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ).sort("created_at", -1)) # <--- FIX: Sort by creation date

#     # 2. Process data for visualization (no change here)
#     for content in content_list:
#         content['_id'] = str(content['_id'])
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201

# # --- API Endpoints: Module 6 (Analytics) ---

# ## 10. Get User Performance History for Analytics (Module 6)
# @app.route('/api/analytics/performance', methods=['GET'])
# @jwt_required()
# def get_performance_analytics():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch the last 20 answers submitted by the user (chronological order)
#     performance_data = list(db["quiz_history"].find(
#         {"user_id": user['_id']},
#         # Sort by timestamp (most recent first), and limit to the last 20 interactions
#     ).sort("timestamp", -1).limit(20))

#     # 2. Process data for visualization (reverse to show oldest to newest)
#     processed_data = []
    
#     for log in reversed(performance_data):
#         processed_data.append({
#             "is_correct": log['is_correct'],
#             "question_type": log['question_type'],
#             "time_taken_ms": log.get('time_taken_ms', 0),
#             "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
#         })

#     return jsonify(processed_data), 200

# # --- API Endpoints: Module 7 (Voice Coaching) ---

# ## 11. Generate Voice Suggestion Text (Module 7)
# @app.route('/api/coaching/suggest', methods=['POST'])
# @jwt_required()
# def generate_coaching_suggestion():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     quiz_results = data.get('quiz_results') # Array of questions from the store
#     total_correct = data.get('total_correct')
#     total_answered = data.get('total_answered')

#     if not quiz_results or total_answered == 0:
#         return jsonify({"msg": "No quiz data provided for analysis."}), 400

#     # 1. Summarize Weaknesses (Top 3 failed topics/chunks)
#     # We'll rely on the frontend sending the simple summary.
    
#     # 2. Extract specific failure points (e.g., failed on chunk X, Y, Z)
#     failure_data = []
#     for q in quiz_results:
#         # Check if the question was answered (isCorrect field exists) and if it was False
#         if 'isCorrect' in q and q['isCorrect'] == False: 
#             failure_data.append({
#                 'type': q['type'],
#                 'chunk_preview': q['content_chunk'][:40] + '...',
#                 'question': q['question']
#             })

#     # 3. Call the AI Service to generate personalized text
    
#     # Generate the prompt for the AI
#     prompt = (
#         f"You are a supportive, insightful learning coach. Analyze the user's recent quiz performance. "
#         f"Overall Score: {total_correct}/{total_answered}. "
#         f"Primary Difficulty Level: {user.get('difficulty_level', 'Intermediate')}. "
#         f"Based on the following {len(failure_data)} failure points, generate a brief (max 100 words) motivational suggestion. "
#         f"Your response must include:\n"
#         f"1. A motivational opening.\n"
#         f"2. A summary of their mistake area (e.g., 'You struggled with Fill-in-the-Blank questions on topic X').\n"
#         f"3. A clear, actionable suggestion on what specific topic or question type to focus on next. "
#         f"FAILURE DATA: {failure_data}"
#     )

#     # Call the AI service (using the existing generation function, but simplifying the JSON schema request)
#     try:
#         response_text = ai_service.generate_coaching_text(prompt)
#     except Exception as e:
#         print(f"Coaching AI call failed: {e}")
#         return jsonify({"msg": "AI coaching generation failed."}), 500

#     return jsonify({"suggestion_text": response_text}), 200


# # --- API Endpoints: Module 6 (Admin Dashboard) ---

# ## 12. Get Admin-Level System Statistics (Module 6)
# @app.route('/api/admin/stats', methods=['GET'])
# @jwt_required()
# def get_admin_stats():
#     # NOTE: In a real application, you would add logic here to check if the user 
#     # making the request has an 'admin' role. For MVP, we skip the role check.

#     try:
#         # 1. Total User Count
#         total_users = db["users"].count_documents({})

#         # 2. Total Quizzes/Interactions Logged
#         total_interactions = db["quiz_history"].count_documents({})
        
#         # 3. Total Content Chunks Uploaded
#         total_content = user_service.contents_collection.count_documents({})

#         # 4. Overall Accuracy (Requires aggregation - simplified here for speed)
#         # We perform a quick aggregate to get the count of correct vs total attempts
#         accuracy_pipeline = [
#             {"$group": {
#                 "_id": None,
#                 "total_answered": {"$sum": 1},
#                 "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
#             }}
#         ]
#         accuracy_result = list(db["quiz_history"].aggregate(accuracy_pipeline))

#         overall_accuracy = 0
#         if accuracy_result and accuracy_result[0]['total_answered'] > 0:
#             overall_accuracy = round(
#                 (accuracy_result[0]['total_correct'] / accuracy_result[0]['total_answered']) * 100
#             )

#         return jsonify({
#             "total_users": total_users,
#             "total_interactions": total_interactions,
#             "total_content_items": total_content,
#             "overall_accuracy_percent": overall_accuracy
#         }), 200

#     except Exception as e:
#         print(f"Admin stats error: {e}")
#         return jsonify({"msg": "Failed to fetch admin stats."}), 500

# # --- API Endpoints: Module 6 (Admin Feedback) ---

# ## 13. Log Question Feedback/Flagging (Module 6)
# @app.route('/api/feedback/flag', methods=['POST'])
# @jwt_required()
# def log_question_flag():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS for moderation
#     question_id = data.get('question_id') # The ObjectId of the content chunk used
#     reason = data.get('reason', 'Inappropriate/Broken Content')
    
#     if not question_id:
#         return jsonify({"msg": "Missing question ID."}), 400

#     # 1. Prepare flag document
#     flag_data = {
#         "user_id": user['_id'],
#         "question_content_id": question_id,
#         "reason": reason,
#         "status": "Pending Review",
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated collection for moderation
#     db["moderation_queue"].insert_one(flag_data)
    
#     return jsonify({"msg": "Question flagged for review. Thank you for your feedback."}), 201


# ## 14. Get Question Moderation Queue (Module 6)
# @app.route('/api/admin/moderation/queue', methods=['GET'])
# @jwt_required()
# def get_moderation_queue():
#     # NOTE: In a production app, we would enforce an 'admin' role check here.
    
#     try:
#         # Fetch all flagged items, newest first
#         queue_data = list(db["moderation_queue"].find(
#             {"status": "Pending Review"} # Filter for items needing attention
#         ).sort("timestamp", -1)) 

#         # Format ObjectIds and datetime for JSON serialization
#         for item in queue_data:
#             item['_id'] = str(item['_id'])
#             item['user_id'] = str(item.get('user_id', 'N/A')) 
#             item['timestamp'] = item['timestamp'].strftime("%Y-%m-%d %H:%M:%S")

#         return jsonify(queue_data), 200

#     except Exception as e:
#         print(f"Moderation queue fetch error: {e}")
#         return jsonify({"msg": "Failed to fetch moderation queue."}), 500


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)









# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import os 
# import random 
# from hashlib import sha256 

# # --- IMPORT NEW SERVICES (CRITICAL) ---
# from services.user_service import UserService 
# from services.ai_service import AIService 
# from services.adaptive_service import AdaptiveService 
# # --------------------------------------

# # Load environment variables (from .env file)
# load_dotenv()

# app = Flask(__name__)
# CORS(app) 

# # --- Configuration & Setup ---

# # JWT and Security Configuration
# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# # Database Configuration
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# # Configuration for temporary file storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# # Helper function for file type checks (optional, but good practice)
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# try:
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     users_collection = db["users"]
#     contents_collection = db["contents"] 
#     quiz_history_collection = db["quiz_history"] # Get history collection
    
#     # Instantiate Services
#     user_service = UserService(users_collection, contents_collection, bcrypt) 
#     ai_service = AIService() 
#     adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) # CRITICAL FIX: Pass BOTH collections
    
#     # Ensure email index is unique for fast lookups
#     users_collection.create_index("email", unique=True)
    
#     print("Successfully connected to MongoDB.")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # --- API Endpoints: Module 1 (User Management) ---

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

# ## 1. User Registration (Signup)
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing email or password"}), 400

#     # Use service layer
#     new_user_email = user_service.register_user(email, password)

#     if new_user_email:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 201
#     else:
#         return jsonify({"msg": "User with this email already exists"}), 409

# ## 2. User Login
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     # Use service layer
#     user_data = user_service.check_password(email, password)

#     if user_data:
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401

# ## 3. Profile Management (Get Profile)
# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_email = get_jwt_identity() 
#     user = user_service.find_user_by_email(current_user_email)
    
#     if user:
#         return jsonify(user), 200
    
#     return jsonify({"msg": "User not found"}), 404

# ## 4. Profile Management (Update Profile)
# @app.route('/api/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_email = get_jwt_identity()
#     data = request.get_json()

#     # Use service layer
#     was_modified = user_service.update_profile(current_user_email, data)

#     if was_modified:
#         return jsonify({"msg": "Profile updated successfully"}), 200
#     else:
#         if user_service.find_user_by_email(current_user_email):
#             return jsonify({"msg": "User found but no valid changes applied"}), 200
#         else:
#             return jsonify({"msg": "User not found"}), 404

# # --- API Endpoints: Module 2 (Content Ingestion) ---

# ## 6. Content Ingestion (Module 2)
# @app.route('/api/content/upload', methods=['POST'])
# @jwt_required()
# def upload_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # Check for User existence
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # Data is now retrieved from request.form (for text fields) and request.files (for files)
#     # The 'title' will be the subject for the AI
#     title = request.form.get('title', 'General Knowledge') 
#     method = request.form.get('method')
    
#     raw_text = ""
    
#     # --- 1. Extract Text based on Ingestion Method ---
#     if method == 'paste':
#         raw_text = request.form.get('raw_text', '')
#         source_type = "Pasted Text"
        
#     elif method == 'url':
#         content_url = request.form.get('content_url', '')
#         if not content_url:
#             return jsonify({"msg": "URL not provided."}), 400
#         # Use AI Service for web fetching and scraping
#         raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
#         source_type = "Analyzed URL"
#         if not raw_text:
#              return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

#     elif method == 'file':
#         if 'file' not in request.files:
#             return jsonify({"msg": "No file part in the request."}), 400
            
#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             return jsonify({"msg": "No selected file."}), 400
        
#         if not allowed_file(uploaded_file.filename):
#             return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

#         # Read file content directly from the stream (for PyPDF2 compatibility)
#         raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
#         source_type = f"Uploaded File ({uploaded_file.filename})"
        
#         if not raw_text:
#             return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
#     else:
#         return jsonify({"msg": "Invalid ingestion method."}), 400

#     # --- 2. Process and Save Chunks (Common Logic) ---
#     # Use AI Service for cleaning and segmentation (NLP)
#     knowledge_chunks = ai_service.process_content(raw_text)

#     if not knowledge_chunks:
#         return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
#     content_data = {
#         "user_id": user['_id'],
#         "title": title, # Uses the user-provided title (e.g., "Physics")
#         "source_type": source_type,
#         "chunks": knowledge_chunks,
#         "chunk_count": len(knowledge_chunks),
#         "created_at": datetime.now()
#     }
    
#     # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
#     content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
#     return jsonify({
#         "msg": "Content processed and saved successfully.",
#         "content_id": str(content_id),
#         "chunk_count": len(knowledge_chunks)
#     }), 201

# # --- API Endpoints: Module 3 (Quiz Logic) ---

# ## 7. Get List of User Content
# @app.route('/api/content/list', methods=['GET'])
# @jwt_required()
# def list_user_content():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch content, sorting by 'created_at' descending (-1)
#     content_list = list(user_service.contents_collection.find(
#         {"user_id": user['_id']},
#         {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
#     ).sort("created_at", -1)) # <--- FIX: Sort by creation date

#     # 2. Process data for visualization (no change here)
#     for content in content_list:
#         content['_id'] = str(content['_id'])
#         content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

#     return jsonify(content_list), 200

# ## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
# @app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
# @jwt_required()
# def generate_question(content_id):
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     # 1. Input Validation and Data Retrieval
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     requested_question_type = data.get('question_type')
    
#     if not requested_question_type:
#         return jsonify({"msg": "Question type is missing from request body."}), 400

#     # Fetch the selected content chunks
#     try:
#         content_document = user_service.contents_collection.find_one(
#             {"_id": ObjectId(content_id), "user_id": user['_id']}
#         )
#     except Exception:
#         return jsonify({"msg": "Invalid content ID format."}), 400

#     if not content_document:
#         return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
#     knowledge_chunks = content_document.get('chunks', [])
#     if not knowledge_chunks:
#         return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
#     # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
#     selected_chunk_text = None
    
#     # 1. Check for weakness: Prioritize chunks the user has failed
#     weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

#     if weak_chunk_result:
#         # We know the text is returned now by the service
#         selected_chunk_text = weak_chunk_result['chunk_text'] 
#         print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
#         # 2. Check for Weakest Question Type (Bias the question type)
#         worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
#         if worst_type and random.random() < 0.5: # 50% chance to override
#             final_question_type = worst_type
#             print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
#         else:
#             final_question_type = requested_question_type
#     else:
#         # 2. Fallback: Select a random chunk if no weakness is severe enough
#         selected_chunk_text = random.choice(knowledge_chunks)
#         final_question_type = requested_question_type
#         print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
#     # --- END ADAPTIVE SELECTION LOGIC ---

#     # 3. Get Preferences
#     subject = content_document.get('title', 'General Knowledge Topic') 
#     difficulty = user.get('difficulty_level', 'Intermediate') 
    
#     # 4. Call the AI service to generate the structured question
#     question_data = ai_service.generate_quiz_question(
#         content_chunk=selected_chunk_text, 
#         question_type=final_question_type, 
#         subject=subject, # Use the dynamic title as the subject context
#         difficulty=difficulty
#     )
    
#     if question_data:
#         question_data['content_chunk'] = selected_chunk_text 
#         question_data['content_id'] = content_id
        
#         return jsonify(question_data), 200
#     else:
#         return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# # --- API Endpoints: Module 4 (Adaptive Logging) ---

# ## 9. Log User Performance (Module 4)
# @app.route('/api/quiz/log-answer', methods=['POST'])
# @jwt_required()
# def log_user_answer():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS
#     content_id = data.get('content_id')
#     chunk_text = data.get('content_chunk')
#     is_correct = data.get('is_correct')
#     question_type = data.get('question_type')
#     time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
#     if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
#         return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

#     # 1. Prepare log document
#     log_data = {
#         "user_id": user['_id'],
#         "content_id": content_id,
#         "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
#         "is_correct": bool(is_correct),
#         "question_type": question_type,
#         "difficulty_level": user.get('difficulty_level', 'Intermediate'),
#         "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated history collection
#     db["quiz_history"].insert_one(log_data)
    
#     return jsonify({"msg": "Performance logged successfully."}), 201

# # --- API Endpoints: Module 6 (Analytics) ---

# ## 10. Get User Performance History for Analytics (Module 6)
# @app.route('/api/analytics/performance', methods=['GET'])
# @jwt_required()
# def get_performance_analytics():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     # 1. Fetch the last 20 answers submitted by the user (chronological order)
#     performance_data = list(db["quiz_history"].find(
#         {"user_id": user['_id']},
#         # Sort by timestamp (most recent first), and limit to the last 20 interactions
#     ).sort("timestamp", -1).limit(20))

#     # 2. Process data for visualization (reverse to show oldest to newest)
#     processed_data = []
    
#     for log in reversed(performance_data):
#         processed_data.append({
#             "is_correct": log['is_correct'],
#             "question_type": log['question_type'],
#             "time_taken_ms": log.get('time_taken_ms', 0),
#             "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
#         })

#     return jsonify(processed_data), 200

# # --- API Endpoints: Module 7 (Voice Coaching) ---

# ## 11. Generate Voice Suggestion Text (Module 7)
# @app.route('/api/coaching/suggest', methods=['POST'])
# @jwt_required()
# def generate_coaching_suggestion():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404

#     data = request.get_json()
#     quiz_results = data.get('quiz_results') # Array of questions from the store
#     total_correct = data.get('total_correct')
#     total_answered = data.get('total_answered')

#     if not quiz_results or total_answered == 0:
#         return jsonify({"msg": "No quiz data provided for analysis."}), 400

#     # 1. Summarize Weaknesses (Top 3 failed topics/chunks)
#     # We'll rely on the frontend sending the simple summary.
    
#     # 2. Extract specific failure points (e.g., failed on chunk X, Y, Z)
#     failure_data = []
#     for q in quiz_results:
#         # Check if the question was answered (isCorrect field exists) and if it was False
#         if 'isCorrect' in q and q['isCorrect'] == False: 
#             failure_data.append({
#                 'type': q['type'],
#                 'chunk_preview': q['content_chunk'][:40] + '...',
#                 'question': q['question']
#             })

#     # 3. Call the AI Service to generate personalized text
    
#     # Generate the prompt for the AI
#     prompt = (
#         f"You are a supportive, insightful learning coach. Analyze the user's recent quiz performance. "
#         f"Overall Score: {total_correct}/{total_answered}. "
#         f"Primary Difficulty Level: {user.get('difficulty_level', 'Intermediate')}. "
#         f"Based on the following {len(failure_data)} failure points, generate a brief (max 100 words) motivational suggestion. "
#         f"Your response must include:\n"
#         f"1. A motivational opening.\n"
#         f"2. A summary of their mistake area (e.g., 'You struggled with Fill-in-the-Blank questions on topic X').\n"
#         f"3. A clear, actionable suggestion on what specific topic or question type to focus on next. "
#         f"FAILURE DATA: {failure_data}"
#     )

#     # Call the AI service (using the existing generation function, but simplifying the JSON schema request)
#     try:
#         response_text = ai_service.generate_coaching_text(prompt)
#     except Exception as e:
#         print(f"Coaching AI call failed: {e}")
#         return jsonify({"msg": "AI coaching generation failed."}), 500

#     return jsonify({"suggestion_text": response_text}), 200


# # --- API Endpoints: Module 6 (Admin Dashboard) ---

# ## 12. Get Admin-Level System Statistics (Module 6)
# @app.route('/api/admin/stats', methods=['GET'])
# @jwt_required()
# def get_admin_stats():
#     # NOTE: In a real application, you would add logic here to check if the user 
#     # making the request has an 'admin' role. For MVP, we skip the role check.

#     try:
#         # 1. Total User Count
#         total_users = db["users"].count_documents({})

#         # 2. Total Quizzes/Interactions Logged
#         total_interactions = db["quiz_history"].count_documents({})
        
#         # 3. Total Content Chunks Uploaded
#         total_content = user_service.contents_collection.count_documents({})

#         # 4. Overall Accuracy (Requires aggregation - simplified here for speed)
#         # We perform a quick aggregate to get the count of correct vs total attempts
#         accuracy_pipeline = [
#             {"$group": {
#                 "_id": None,
#                 "total_answered": {"$sum": 1},
#                 "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
#             }}
#         ]
#         accuracy_result = list(db["quiz_history"].aggregate(accuracy_pipeline))

#         overall_accuracy = 0
#         if accuracy_result and accuracy_result[0]['total_answered'] > 0:
#             overall_accuracy = round(
#                 (accuracy_result[0]['total_correct'] / accuracy_result[0]['total_answered']) * 100
#             )

#         return jsonify({
#             "total_users": total_users,
#             "total_interactions": total_interactions,
#             "total_content_items": total_content,
#             "overall_accuracy_percent": overall_accuracy
#         }), 200

#     except Exception as e:
#         print(f"Admin stats error: {e}")
#         return jsonify({"msg": "Failed to fetch admin stats."}), 500

# # --- API Endpoints: Module 6 (Admin Feedback) ---

# ## 13. Log Question Feedback/Flagging (Module 6)
# @app.route('/api/feedback/flag', methods=['POST'])
# @jwt_required()
# def log_question_flag():
#     current_user_email = get_jwt_identity()
#     user = user_service.find_user_by_email(current_user_email)
    
#     if not user:
#         return jsonify({"msg": "User not found."}), 404
    
#     data = request.get_json()
    
#     # CRITICAL DATA POINTS for moderation
#     question_id = data.get('question_id') # The ObjectId of the content chunk used
#     reason = data.get('reason', 'Inappropriate/Broken Content')
    
#     if not question_id:
#         return jsonify({"msg": "Missing question ID."}), 400

#     # 1. Prepare flag document
#     flag_data = {
#         "user_id": user['_id'],
#         "question_content_id": question_id,
#         "reason": reason,
#         "status": "Pending Review",
#         "timestamp": datetime.now()
#     }
    
#     # 2. Insert into a new dedicated collection for moderation
#     db["moderation_queue"].insert_one(flag_data)
    
#     return jsonify({"msg": "Question flagged for review. Thank you for your feedback."}), 201


# ## 14. Get Question Moderation Queue (Module 6)
# @app.route('/api/admin/moderation/queue', methods=['GET'])
# @jwt_required()
# def get_moderation_queue():
#     # NOTE: In a production app, we would enforce an 'admin' role check here.
    
#     try:
#         # Fetch all flagged items, newest first
#         queue_data = list(db["moderation_queue"].find(
#             {"status": "Pending Review"} # Filter for items needing attention
#         ).sort("timestamp", -1)) 

#         # Format ObjectIds and datetime for JSON serialization
#         for item in queue_data:
#             item['_id'] = str(item['_id'])
#             item['user_id'] = str(item.get('user_id', 'N/A')) 
#             item['timestamp'] = item['timestamp'].strftime("%Y-%m-%d %H:%M:%S")

#         return jsonify(queue_data), 200

#     except Exception as e:
#         print(f"Moderation queue fetch error: {e}")
#         return jsonify({"msg": "Failed to fetch moderation queue."}), 500


# if __name__ == '__main__':
#     # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
#     app.run(debug=True, port=5000)





























from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
import os 
import random 
from hashlib import sha256 

# --- IMPORT NEW SERVICES (CRITICAL) ---
from services.user_service import UserService 
from services.ai_service import AIService 
from services.adaptive_service import AdaptiveService 
# --------------------------------------

# Load environment variables (from .env file)
load_dotenv()

app = Flask(__name__)
CORS(app) 

# --- Configuration & Setup ---

# JWT and Security Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_SECRET_KEY", "YOUR_VERY_SECRET_KEY_FOR_JWT_AND_SESSIONS")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7) 

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Database Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartQuizzerDB")

# Configuration for temporary file storage
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# Helper function for file type checks (optional, but good practice)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    users_collection = db["users"]
    contents_collection = db["contents"] 
    quiz_history_collection = db["quiz_history"] # Get history collection
    
    # Instantiate Services
    user_service = UserService(users_collection, contents_collection, bcrypt) 
    ai_service = AIService() 
    adaptive_service = AdaptiveService(quiz_history_collection, contents_collection) # CRITICAL FIX: Pass BOTH collections
    
    # Ensure email index is unique for fast lookups
    users_collection.create_index("email", unique=True)
    
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

# --- API Endpoints: Module 1 (User Management) ---

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Smart Quizzer Backend Running on Flask!"})

## 1. User Registration (Signup)
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    # Use service layer
    new_user_email = user_service.register_user(email, password)

    if new_user_email:
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 201
    else:
        return jsonify({"msg": "User with this email already exists"}), 409

## 2. User Login
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Use service layer
    user_data = user_service.check_password(email, password)

    if user_data:
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

## 3. Profile Management (Get Profile)
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_email = get_jwt_identity() 
    user = user_service.find_user_by_email(current_user_email)
    
    if user:
        return jsonify(user), 200
    
    return jsonify({"msg": "User not found"}), 404

## 4. Profile Management (Update Profile)
@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_email = get_jwt_identity()
    data = request.get_json()

    # Use service layer
    was_modified = user_service.update_profile(current_user_email, data)

    if was_modified:
        return jsonify({"msg": "Profile updated successfully"}), 200
    else:
        if user_service.find_user_by_email(current_user_email):
            return jsonify({"msg": "User found but no valid changes applied"}), 200
        else:
            return jsonify({"msg": "User not found"}), 404

# --- API Endpoints: Module 2 (Content Ingestion) ---

## 6. Content Ingestion (Module 2)
@app.route('/api/content/upload', methods=['POST'])
@jwt_required()
def upload_content():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    # Check for User existence
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    # Data is now retrieved from request.form (for text fields) and request.files (for files)
    # The 'title' will be the subject for the AI
    title = request.form.get('title', 'General Knowledge') 
    method = request.form.get('method')
    
    raw_text = ""
    
    # --- 1. Extract Text based on Ingestion Method ---
    if method == 'paste':
        raw_text = request.form.get('raw_text', '')
        source_type = "Pasted Text"
        
    elif method == 'url':
        content_url = request.form.get('content_url', '')
        if not content_url:
            return jsonify({"msg": "URL not provided."}), 400
        # Use AI Service for web fetching and scraping
        raw_text = ai_service.fetch_and_extract_text_from_url(content_url)
        source_type = "Analyzed URL"
        if not raw_text:
             return jsonify({"msg": "Failed to fetch or extract text from the URL. Check URL validity."}), 500

    elif method == 'file':
        if 'file' not in request.files:
            return jsonify({"msg": "No file part in the request."}), 400
            
        uploaded_file = request.files['file']
        
        if uploaded_file.filename == '':
            return jsonify({"msg": "No selected file."}), 400
        
        if not allowed_file(uploaded_file.filename):
            return jsonify({"msg": "Invalid file type. Only PDF and TXT are supported."}), 400

        # Read file content directly from the stream (for PyPDF2 compatibility)
        raw_text = ai_service.extract_text_from_pdf(uploaded_file.stream) 
        
        source_type = f"Uploaded File ({uploaded_file.filename})"
        
        if not raw_text:
            return jsonify({"msg": "Failed to extract text from the file (is it a valid PDF/TXT?)."}), 500
            
    else:
        return jsonify({"msg": "Invalid ingestion method."}), 400

    # --- 2. Process and Save Chunks (Common Logic) ---
    # Use AI Service for cleaning and segmentation (NLP)
    knowledge_chunks = ai_service.process_content(raw_text)

    if not knowledge_chunks:
        return jsonify({"msg": "Content too short or invalid after cleaning/parsing. Text length was too small."}), 400
    
    content_data = {
        "user_id": user['_id'],
        "title": title, # Uses the user-provided title (e.g., "Physics")
        "source_type": source_type,
        "chunks": knowledge_chunks,
        "chunk_count": len(knowledge_chunks),
        "created_at": datetime.now()
    }
    
    # Save the processed content to the 'contents' collection via the user service (which holds the collection reference)
    content_id = user_service.contents_collection.insert_one(content_data).inserted_id
    
    return jsonify({
        "msg": "Content processed and saved successfully.",
        "content_id": str(content_id),
        "chunk_count": len(knowledge_chunks)
    }), 201

# --- API Endpoints: Module 3 (Quiz Logic) ---

## 7. Get List of User Content
@app.route('/api/content/list', methods=['GET'])
@jwt_required()
def list_user_content():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    # 1. Fetch content, sorting by 'created_at' descending (-1)
    content_list = list(user_service.contents_collection.find(
        {"user_id": user['_id']},
        {"title": 1, "chunk_count": 1, "created_at": 1} # Only fetch necessary fields
    ).sort("created_at", -1)) # <--- FIX: Sort by creation date

    # 2. Process data for visualization (no change here)
    for content in content_list:
        content['_id'] = str(content['_id'])
        content['created_at'] = content['created_at'].strftime("%Y-%m-%d %H:%M")

    return jsonify(content_list), 200

## 8. AI Question Generation & Delivery (Module 3/5 - ADAPTIVE)
@app.route('/api/quiz/generate/<content_id>', methods=['POST']) 
@jwt_required()
def generate_question(content_id):
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    # 1. Input Validation and Data Retrieval
    if not user:
        return jsonify({"msg": "User not found."}), 404

    data = request.get_json()
    requested_question_type = data.get('question_type')
    
    if not requested_question_type:
        return jsonify({"msg": "Question type is missing from request body."}), 400

    # Fetch the selected content chunks
    try:
        content_document = user_service.contents_collection.find_one(
            {"_id": ObjectId(content_id), "user_id": user['_id']}
        )
    except Exception:
        return jsonify({"msg": "Invalid content ID format."}), 400

    if not content_document:
        return jsonify({"msg": "Content not found or does not belong to user."}), 404
        
    knowledge_chunks = content_document.get('chunks', [])
    if not knowledge_chunks:
        return jsonify({"msg": "Content contains no usable chunks for quizzing."}), 400
        
    # --- ADAPTIVE SELECTION LOGIC (Module 5) ---
    
    selected_chunk_text = None
    
    # 1. Check for weakness: Prioritize chunks the user has failed
    weak_chunk_result = adaptive_service.get_weakest_chunk(user['_id'], content_id)

    if weak_chunk_result:
        # We know the text is returned now by the service
        selected_chunk_text = weak_chunk_result['chunk_text'] 
        print(f"ADAPTIVE: Targeting chunk with score: {weak_chunk_result['correct_rate'] * 100:.2f}%)")
        
        # 2. Check for Weakest Question Type (Bias the question type)
        worst_type = adaptive_service.get_worst_performing_question_type(user['_id'], content_id)
        
        if worst_type and random.random() < 0.5: # 50% chance to override
            final_question_type = worst_type
            print(f"ADAPTIVE: Biasing question type towards WORST PERFORMING: {worst_type}")
        else:
            final_question_type = requested_question_type
    else:
        # 2. Fallback: Select a random chunk if no weakness is severe enough
        selected_chunk_text = random.choice(knowledge_chunks)
        final_question_type = requested_question_type
        print("ADAPTIVE: No severe weakness found, selecting random chunk.")
    
    # --- END ADAPTIVE SELECTION LOGIC ---

    # 3. Get Preferences
    subject = content_document.get('title', 'General Knowledge Topic') 
    difficulty = user.get('difficulty_level', 'Intermediate') 
    
    # 4. Call the AI service to generate the structured question
    question_data = ai_service.generate_quiz_question(
        content_chunk=selected_chunk_text, 
        question_type=final_question_type, 
        subject=subject, # Use the dynamic title as the subject context
        difficulty=difficulty
    )
    
    if question_data:
        question_data['content_chunk'] = selected_chunk_text 
        question_data['content_id'] = content_id
        
        return jsonify(question_data), 200
    else:
        return jsonify({"msg": "Failed to generate question from AI. Check API Key or LLM service."}), 500

# --- API Endpoints: Module 4 (Adaptive Logging) ---

## 9. Log User Performance (Module 4)
@app.route('/api/quiz/log-answer', methods=['POST'])
@jwt_required()
def log_user_answer():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    data = request.get_json()
    
    # CRITICAL DATA POINTS
    content_id = data.get('content_id')
    chunk_text = data.get('content_chunk')
    is_correct = data.get('is_correct')
    question_type = data.get('question_type')
    time_taken_ms = data.get('time_taken_ms') # <-- NEW DATA POINT
    
    if not all([content_id, chunk_text, is_correct is not None, question_type, time_taken_ms is not None]):
        return jsonify({"msg": "Missing required data (ID, chunk, result, type, time)."}), 400

    # 1. Prepare log document
    log_data = {
        "user_id": user['_id'],
        "content_id": content_id,
        "chunk_hash": sha256(chunk_text.encode()).hexdigest(), # Use sha256 for reliable chunk lookup
        "is_correct": bool(is_correct),
        "question_type": question_type,
        "difficulty_level": user.get('difficulty_level', 'Intermediate'),
        "time_taken_ms": time_taken_ms, # <-- NEW DATA POINT SAVED
        "timestamp": datetime.now()
    }
    
    # 2. Insert into a new dedicated history collection
    db["quiz_history"].insert_one(log_data)
    
    return jsonify({"msg": "Performance logged successfully."}), 201

# --- API Endpoints: Module 6 (Analytics) ---

## 10. Get User Performance History for Analytics (Module 6)
@app.route('/api/analytics/performance', methods=['GET'])
@jwt_required()
def get_performance_analytics():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    # 1. Fetch the last 20 answers submitted by the user (chronological order)
    performance_data = list(db["quiz_history"].find(
        {"user_id": user['_id']},
        # Sort by timestamp (most recent first), and limit to the last 20 interactions
    ).sort("timestamp", -1).limit(20))

    # 2. Process data for visualization (reverse to show oldest to newest)
    processed_data = []
    
    for log in reversed(performance_data):
        processed_data.append({
            "is_correct": log['is_correct'],
            "question_type": log['question_type'],
            "time_taken_ms": log.get('time_taken_ms', 0),
            "timestamp": log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(processed_data), 200

# --- API Endpoints: Module 7 (Voice Coaching) ---

## 11. Generate Voice Suggestion Text (Module 7)
@app.route('/api/coaching/suggest', methods=['POST'])
@jwt_required()
def generate_coaching_suggestion():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404

    data = request.get_json()
    quiz_results = data.get('quiz_results') # Array of questions from the store
    total_correct = data.get('total_correct')
    total_answered = data.get('total_answered')

    if not quiz_results or total_answered == 0:
        return jsonify({"msg": "No quiz data provided for analysis."}), 400

    # 1. Summarize Weaknesses (Top 3 failed topics/chunks)
    # We'll rely on the frontend sending the simple summary.
    
    # 2. Extract specific failure points (e.g., failed on chunk X, Y, Z)
    failure_data = []
    for q in quiz_results:
        # Check if the question was answered (isCorrect field exists) and if it was False
        if 'isCorrect' in q and q['isCorrect'] == False: 
            failure_data.append({
                'type': q['type'],
                'chunk_preview': q['content_chunk'][:40] + '...',
                'question': q['question']
            })

    # 3. Call the AI Service to generate personalized text
    
    # Generate the prompt for the AI
    prompt = (
        f"You are a supportive, insightful learning coach. Analyze the user's recent quiz performance. "
        f"Overall Score: {total_correct}/{total_answered}. "
        f"Primary Difficulty Level: {user.get('difficulty_level', 'Intermediate')}. "
        f"Based on the following {len(failure_data)} failure points, generate a brief (max 100 words) motivational suggestion. "
        f"Your response must include:\n"
        f"1. A motivational opening.\n"
        f"2. A summary of their mistake area (e.g., 'You struggled with Fill-in-the-Blank questions on topic X').\n"
        f"3. A clear, actionable suggestion on what specific topic or question type to focus on next. "
        f"FAILURE DATA: {failure_data}"
    )

    # Call the AI service (using the existing generation function, but simplifying the JSON schema request)
    try:
        response_text = ai_service.generate_coaching_text(prompt)
    except Exception as e:
        print(f"Coaching AI call failed: {e}")
        return jsonify({"msg": "AI coaching generation failed."}), 500

    return jsonify({"suggestion_text": response_text}), 200


# --- API Endpoints: Module 6 (Admin Dashboard) ---

## 12. Get Admin-Level System Statistics (Module 6)
@app.route('/api/admin/stats', methods=['GET'])
@jwt_required()
def get_admin_stats():
    # NOTE: In a real application, you would add logic here to check if the user 
    # making the request has an 'admin' role. For MVP, we skip the role check.

    try:
        # 1. Total User Count
        total_users = db["users"].count_documents({})

        # 2. Total Quizzes/Interactions Logged
        total_interactions = db["quiz_history"].count_documents({})
        
        # 3. Total Content Chunks Uploaded
        total_content = user_service.contents_collection.count_documents({})

        # 4. Overall Accuracy (Requires aggregation - simplified here for speed)
        # We perform a quick aggregate to get the count of correct vs total attempts
        accuracy_pipeline = [
            {"$group": {
                "_id": None,
                "total_answered": {"$sum": 1},
                "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
            }}
        ]
        accuracy_result = list(db["quiz_history"].aggregate(accuracy_pipeline))

        overall_accuracy = 0
        if accuracy_result and accuracy_result[0]['total_answered'] > 0:
            overall_accuracy = round(
                (accuracy_result[0]['total_correct'] / accuracy_result[0]['total_answered']) * 100
            )

        return jsonify({
            "total_users": total_users,
            "total_interactions": total_interactions,
            "total_content_items": total_content,
            "overall_accuracy_percent": overall_accuracy
        }), 200

    except Exception as e:
        print(f"Admin stats error: {e}")
        return jsonify({"msg": "Failed to fetch admin stats."}), 500

# --- API Endpoints: Module 6 (Admin Feedback) ---

## 13. Log Question Feedback/Flagging (Module 6)
@app.route('/api/feedback/flag', methods=['POST'])
@jwt_required()
def log_question_flag():
    current_user_email = get_jwt_identity()
    user = user_service.find_user_by_email(current_user_email)
    
    if not user:
        return jsonify({"msg": "User not found."}), 404
    
    data = request.get_json()
    
    # CRITICAL DATA POINTS for moderation
    question_id = data.get('question_id') # The ObjectId of the content chunk used
    reason = data.get('reason', 'Inappropriate/Broken Content')
    
    if not question_id:
        return jsonify({"msg": "Missing question ID."}), 400

    # 1. Prepare flag document
    flag_data = {
        "user_id": user['_id'],
        "question_content_id": question_id,
        "reason": reason,
        "status": "Pending Review",
        "timestamp": datetime.now()
    }
    
    # 2. Insert into a new dedicated collection for moderation
    db["moderation_queue"].insert_one(flag_data)
    
    return jsonify({"msg": "Question flagged for review. Thank you for your feedback."}), 201


## 14. Get Question Moderation Queue (Module 6)
@app.route('/api/admin/moderation/queue', methods=['GET'])
@jwt_required()
def get_moderation_queue():
    # NOTE: In a production app, we would enforce an 'admin' role check here.
    
    try:
        # Fetch all flagged items, newest first
        queue_data = list(db["moderation_queue"].find(
            {"status": "Pending Review"} # Filter for items needing attention
        ).sort("timestamp", -1)) 

        # Format ObjectIds and datetime for JSON serialization
        for item in queue_data:
            item['_id'] = str(item['_id'])
            item['user_id'] = str(item.get('user_id', 'N/A')) 
            item['timestamp'] = item['timestamp'].strftime("%Y-%m-%d %H:%M:%S")

        return jsonify(queue_data), 200

    except Exception as e:
        print(f"Moderation queue fetch error: {e}")
        return jsonify({"msg": "Failed to fetch moderation queue."}), 500


# --- API Endpoints: Module 6 (Admin Feedback) ---

## 15. Resolve Flag (Mark as Reviewed/Resolved)
@app.route('/api/admin/moderation/resolve/<flag_id>', methods=['PATCH'])
@jwt_required()
def resolve_flag(flag_id):
    # In a production app, verify admin role here.
    try:
        # Update the status of the flagged item
        result = db["moderation_queue"].update_one(
            {"_id": ObjectId(flag_id)},
            {"$set": {"status": "Resolved", "reviewed_at": datetime.now()}}
        )
        if result.modified_count == 1:
            return jsonify({"msg": f"Flag {flag_id} resolved successfully."}), 200
        return jsonify({"msg": "Flag not found."}), 404
    except Exception as e:
        return jsonify({"msg": f"Error resolving flag: {e}"}), 500

## 16. Delete Flag (Remove from queue/database)
@app.route('/api/admin/moderation/delete/<flag_id>', methods=['DELETE'])
@jwt_required()
def delete_flag(flag_id):
    # In a production app, verify admin role here.
    try:
        # Delete the flagged item entirely
        result = db["moderation_queue"].delete_one({"_id": ObjectId(flag_id)})
        
        if result.deleted_count == 1:
            return jsonify({"msg": f"Flag {flag_id} deleted successfully."}), 200
        return jsonify({"msg": "Flag not found."}), 404
    except Exception as e:
        return jsonify({"msg": f"Error deleting flag: {e}"}), 500


if __name__ == '__main__':
    # Ensure you are running MongoDB Atlas and have set your MONGO_URI in .env
    app.run(debug=True, port=5000)