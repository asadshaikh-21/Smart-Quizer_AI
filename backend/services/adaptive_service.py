# # D:\SmartQuizzer\backend\services\adaptive_service.py

# from bson.objectid import ObjectId
# from collections import defaultdict

# class AdaptiveService:
    
#     def __init__(self, quiz_history_collection):
#         """Initializes the service with the MongoDB quiz_history collection."""
#         self.history = quiz_history_collection

#     def get_weakest_chunk(self, user_id: str, content_id: str):
#         """
#         Analyzes the user's history for a specific content document 
#         and returns the hash of the chunk they struggled with the most.
        
#         Prioritizes:
#         1. Chunks that have never been answered.
#         2. Chunks with the lowest correct percentage.
        
#         Returns: A dictionary {'chunk_hash': str, 'correct_rate': float} or None.
#         """
        
#         # 1. Aggregate performance data for the given user and content
#         pipeline = [
#             # Filter by user and content
#             {"$match": {"user_id": user_id, "content_id": content_id}},
#             # Group by unique chunk (hash) and calculate performance metrics
#             {"$group": {
#                 "_id": "$chunk_hash",
#                 "total_attempts": {"$sum": 1},
#                 "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
#             }},
#             # Calculate the correctness rate
#             {"$project": {
#                 "chunk_hash": "$_id",
#                 "correct_rate": {"$divide": ["$total_correct", "$total_attempts"]}
#             }},
#             # Sort to find the lowest performing chunk first
#             {"$sort": {"correct_rate": 1, "total_attempts": -1}}
#         ]
        
#         # Execute the aggregation
#         weakest_chunks = list(self.history.aggregate(pipeline))
        
#         if weakest_chunks:
#             # Return the chunk with the lowest score
#             return weakest_chunks[0]
        
#         # If no history exists, return None (calling function will handle random selection)
#         return None

#     def get_worst_performing_question_type(self, user_id: str, content_id: str):
#         """
#         Calculates which question type (MCQ, T/F, etc.) the user scores lowest on.
#         Returns: The question type string or None.
#         """
#         pipeline = [
#             {"$match": {"user_id": user_id, "content_id": content_id}},
#             {"$group": {
#                 "_id": "$question_type",
#                 "total_attempts": {"$sum": 1},
#                 "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
#             }},
#             {"$project": {
#                 "question_type": "$_id",
#                 "correct_rate": {"$divide": ["$total_correct", "$total_attempts"]}
#             }},
#             {"$sort": {"correct_rate": 1, "total_attempts": -1}},
#             {"$limit": 1} # Get only the lowest performing type
#         ]
        
#         worst_type_result = list(self.history.aggregate(pipeline))
        
#         return worst_type_result[0]['question_type'] if worst_type_result else None









# D:\SmartQuizzer\backend\services\adaptive_service.py

from bson.objectid import ObjectId
# import collections is unnecessary as defaultdict is not used in the final version
import hashlib # CRITICAL: Imported for sha256 hashing

class AdaptiveService:
    
    def __init__(self, quiz_history_collection, contents_collection): # <--- MODIFIED CONSTRUCTOR
        """Initializes the service with both history and content collections."""
        self.history = quiz_history_collection
        self.contents = contents_collection # <-- Content collection for chunk text lookup

    def get_weakest_chunk(self, user_id: str, content_id: str):
        """
        Analyzes the user's history for a specific content document, 
        identifies the chunk with the lowest score (below 70%), and retrieves its text.
        
        Returns: A dictionary {'chunk_text': str, 'correct_rate': float} or None.
        """
        
        # 1. Aggregate performance data to find the worst-performing chunk hash
        pipeline = [
            # Filter by user and content
            {"$match": {"user_id": user_id, "content_id": content_id}},
            # Group by unique chunk (hash) and calculate performance metrics
            {"$group": {
                "_id": "$chunk_hash",
                "total_attempts": {"$sum": 1},
                "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
            }},
            # Calculate the correctness rate
            {"$project": {
                "chunk_hash": "$_id",
                "correct_rate": {"$divide": ["$total_correct", "$total_attempts"]}
            }},
            # Sort to find the lowest performing chunk first
            {"$sort": {"correct_rate": 1, "total_attempts": -1}},
            {"$limit": 1}
        ]
        
        weakest_chunks = list(self.history.aggregate(pipeline))
        
        if not weakest_chunks:
            return None # No history yet
            
        weakest_data = weakest_chunks[0]
        correct_rate = weakest_data['correct_rate']
        weak_chunk_hash = weakest_data['chunk_hash']

        # 2. Check if weakness is severe enough (Mastery Threshold)
        # Only prioritize chunks below 70% mastery
        if correct_rate >= 0.70:
            return None 

        # 3. Find the exact chunk text (CRITICAL STEP)
        # Query the original content document to find the text that matches the hash.
        try:
            content_doc = self.contents.find_one({"_id": ObjectId(content_id)})
        except Exception:
            # Handle case where content_id is not a valid ObjectId (shouldn't happen here, but safe)
            return None

        if content_doc and content_doc.get('chunks'):
            
            for chunk_text in content_doc['chunks']:
                # Hash each chunk and compare it to the weak hash from history
                if hashlib.sha256(chunk_text.encode()).hexdigest() == weak_chunk_hash:
                    # Found the weak text chunk!
                    return {
                        'chunk_text': chunk_text,
                        'correct_rate': correct_rate
                    }
        
        return None # Fallback if chunk text cannot be located


    def get_worst_performing_question_type(self, user_id: str, content_id: str):
        """
        Calculates which question type (MCQ, T/F, etc.) the user scores lowest on.
        Returns: The question type string or None.
        """
        pipeline = [
            {"$match": {"user_id": user_id, "content_id": content_id}},
            {"$group": {
                "_id": "$question_type",
                "total_attempts": {"$sum": 1},
                "total_correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
            }},
            {"$project": {
                "question_type": "$_id",
                "correct_rate": {"$divide": ["$total_correct", "$total_attempts"]}
            }},
            {"$sort": {"correct_rate": 1, "total_attempts": -1}},
            {"$limit": 1} # Get only the lowest performing type
        ]
        
        worst_type_result = list(self.history.aggregate(pipeline))
        
        return worst_type_result[0]['question_type'] if worst_type_result else None