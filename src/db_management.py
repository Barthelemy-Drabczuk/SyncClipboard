import os
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

from clip_user import ClipUser
from clip_object import ClipObject


class MongoCRUD:
    """MongoDB CRUD operations for clipboard synchronization"""

    def __init__(self) -> None:
        """Initialize MongoDB connection and collections"""
        # Support Docker environment variables
        mongo_host = os.getenv('MONGODB_HOST', 'localhost')
        mongo_port = int(os.getenv('MONGODB_PORT', '27017'))

        connection_string = f"mongodb://{mongo_host}:{mongo_port}/"
        self.client = MongoClient(connection_string)
        self.prod_env = self.client['prod_env']
        self.users = self.prod_env['users']
        self.transactions = self.prod_env['transactions']

    def get_db(self) -> MongoClient:
        return self.client

    def insert_user(self, user: ClipUser):
        """Insert a new user into the database

        Args:
            user (ClipUser): The user object to insert

        Returns:
            MongoCRUD: self for chaining
        """
        self.users.insert_one(user.to_json())
        return self

    def insert_transaction(self, user_id: int, obj: ClipObject):
        """Insert a clipboard transaction for a user

        Args:
            user_id (int): The user's ID
            obj (ClipObject): The clipboard object to store

        Returns:
            MongoCRUD: self for chaining
        """
        transaction = {
            "user_id": user_id,
            "content": obj.get_content(),
            "content_type": obj.get_content_type(),
            "image_data": obj.get_image_data(),
            "timestamp": time.time()
        }
        self.transactions.insert_one(transaction)
        return self

    def get_user(self, username: str, password: str) -> ClipUser:
        """Get a user by username and password

        Args:
            username (str): The username
            password (str): The password (will be hashed)

        Returns:
            ClipUser: The user object or None if not found
        """
        user_data = self.users.find_one({"username": username, "password": hash(password)})
        if user_data:
            return ClipUser(user_data["username"], password, user_data["email"])
        return None

    def get_user_by_id(self, user_id: int) -> ClipUser:
        """Get a user by their ID

        Args:
            user_id (int): The user's ID

        Returns:
            ClipUser: The user object or None if not found
        """
        user_data = self.users.find_one({"id": user_id})
        if user_data:
            return ClipUser(user_data["username"], "", user_data["email"])
        return None

    def get_last_user_transaction(self, user_id: int) -> dict:
        """Get the last clipboard transaction for a user

        Args:
            user_id (int): The user's ID

        Returns:
            dict: The transaction data or empty dict if none found
        """
        transaction = self.transactions.find_one(
            {"user_id": user_id},
            sort=[("timestamp", -1)]
        )
        return transaction if transaction else dict()

    def get_n_last_user_transaction(self, user_id: int, n: int) -> list[dict]:
        """Get the last N clipboard transactions for a user

        Args:
            user_id (int): The user's ID
            n (int): Number of transactions to retrieve

        Returns:
            list[dict]: List of transaction data
        """
        transactions = self.transactions.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(n)
        return list(transactions)

    def update_user(self, user_id: int, update_data: dict):
        """Update user information

        Args:
            user_id (int): The user's ID
            update_data (dict): Dictionary of fields to update

        Returns:
            MongoCRUD: self for chaining
        """
        self.users.update_one({"id": user_id}, {"$set": update_data})
        return self

    def update_transaction(self, transaction_id: str, update_data: dict):
        """Update a transaction

        Args:
            transaction_id (str): The transaction's ID
            update_data (dict): Dictionary of fields to update

        Returns:
            MongoCRUD: self for chaining
        """
        self.transactions.update_one({"_id": ObjectId(transaction_id)}, {"$set": update_data})
        return self

    def delete_user(self, user_id: int):
        """Delete a user and all their transactions

        Args:
            user_id (int): The user's ID

        Returns:
            MongoCRUD: self for chaining
        """
        self.users.delete_one({"id": user_id})
        self.transactions.delete_many({"user_id": user_id})
        return self

    def delete_transaction(self, transaction_id: str):
        """Delete a specific transaction

        Args:
            transaction_id (str): The transaction's ID

        Returns:
            MongoCRUD: self for chaining
        """
        self.transactions.delete_one({"_id": ObjectId(transaction_id)})
        return self
