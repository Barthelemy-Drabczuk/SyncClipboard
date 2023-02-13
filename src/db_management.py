from pymongo import MongoClient, CursorType

from clip_user import ClipUser
from clip_object import ClipObject

class MongoCRUD:
    """_summary_
    """
    
    
    def __init__(self) -> None:
        """_summary_
        """
        self.client = MongoClient()
        self.prod_env = self.client['prod_env']
        self.users = self.prod_env['users']
        self.transactions = self.prod_env['transactions']

    def get_db(self) -> MongoClient:
        return self.client

    """
    " CREATE part
    """
    def insert_user(self, user: ClipUser):
        """_summary_

        Args:
            user (ClipUser): _description_

        Returns:
            MongoCRUD: _description_
        """
        self.users.insert_one(user)
        return self


    def insert_transaction(self, user: ClipUser, obj: ClipObject):
        """_summary_

        Args:
            user (ClipUser): _description_
            obj (ClipObject): _description_

        Returns:
            MongoCRUD: _description_
        """
        return self

    
    """
    " READ part
    """
    def get_user(self, username: str, password: str) -> ClipUser:
        """_summary_

        Args:
            username (str): _description_
            password (str): _description_

        Returns:
            ClipUser: _description_
        """
        return ClipUser()


    def get_last_user_transaction(self, user_id: str) -> dict:
        """_summary_

        Args:
            user_id (str): _description_

        Returns:
            dict: _description_
        """
        return dict()

    
    def get_n_last_user_transaction(self, user_id: str, n: int) -> dict:
        """_summary_

        Args:
            user_id (str): _description_
            n (int): _description_

        Returns:
            dict: _description_
        """
        return dict()

    
    """
    " UPDATE part
    """
    def update_user(self, user_id: str):
        return self

    
    def update_transaction(self, user_id: str, transaction_id: str):
        return self

    
    """
    " DELETE part
    """
    def delete_user(self, user_id: str):
        return self

    
    """
    " DELETE part
    """
    def delete_user(self, user_id: str):
        return self

    
    """
    " DELETE part
    """
    def delete_user(self, user_id: str) -> MongoCRUD:
        return self
    

    def delete_transaction(self, transaction_id: str):
        return self