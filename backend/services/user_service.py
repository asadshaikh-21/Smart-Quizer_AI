# D:\SmartQuizzer\backend\services\user_service.py

from datetime import datetime
from bson.objectid import ObjectId

# This class handles all direct interaction with the MongoDB 'users' and 'contents' collections.
class UserService:
    
    def __init__(self, users_collection, contents_collection, bcrypt):
        """
        Initializes the UserService with the MongoDB collection objects 
        and the bcrypt hashing tool.
        """
        self.users_collection = users_collection
        self.contents_collection = contents_collection # <-- Collection for Module 2 content
        self.bcrypt = bcrypt

    # --- USER MANAGEMENT (MODULE 1) ---

    def register_user(self, email, password):
        """
        Hashes the password and creates a new user document.
        Returns the email if registration is successful, None otherwise.
        """
        if self.users_collection.find_one({"email": email}):
            return None  # User already exists

        # Hash the password for secure storage
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')

        user_data = {
            "email": email,
            "password": hashed_password,
            "subjects_of_interest": [],
            "difficulty_level": "Beginner",
            "performance_history": [],
            "created_at": datetime.now()
        }
        
        self.users_collection.insert_one(user_data)
        return email

    def find_user_by_email(self, email, include_password=False):
        """
        Finds a user by email. Excludes the password hash by default.
        """
        projection = {} if include_password else {"password": 0}
        user = self.users_collection.find_one({"email": email}, projection)
        
        if user:
            # Convert MongoDB's ObjectId to a string for JSON serialization in Flask
            user['_id'] = str(user['_id'])
        return user

    def check_password(self, email, password):
        """
        Finds the user and verifies the given password against the stored hash.
        Returns the full user profile (without hash) on success, None on failure.
        """
        user = self.users_collection.find_one({"email": email}, {"password": 1})
        if user and self.bcrypt.check_password_hash(user['password'], password):
            # Password is correct. Return the full user profile (without hash).
            return self.find_user_by_email(email)
        return None

    def update_profile(self, email, data):
        """
        Updates the user's subjects of interest and difficulty level.
        Returns True if the profile was modified, False otherwise.
        """
        updatable_fields = {}
        
        if 'subjects_of_interest' in data and isinstance(data['subjects_of_interest'], list):
            updatable_fields['subjects_of_interest'] = [s.strip() for s in data['subjects_of_interest'] if s.strip()]
            
        if 'difficulty_level' in data and data['difficulty_level'] in ["Beginner", "Intermediate", "Expert"]:
            updatable_fields['difficulty_level'] = data['difficulty_level']

        if not updatable_fields:
            return False  # Nothing valid to update

        result = self.users_collection.update_one(
            {"email": email},
            {"$set": updatable_fields}
        )

        return result.modified_count == 1