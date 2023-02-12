from pymongo import MongoClient
from pprint import pprint

from clip_user import ClipUser
from clip_object import ClipObject

class MongoCRUD:
    """_summary_
    """
    
    
    def __init__(self) -> None:
        """_summary_
        """
        pass

    """
    " CREATE part
    """
    def insert_user(self, user: ClipUser) -> MongoCRUD:
        """_summary_

        Args:
            user (ClipUser): _description_

        Returns:
            MongoCRUD: _description_
        """
        return self


    def insert_transaction(self, user: ClipUser, obj: ClipObject) -> MongoCRUD:
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
    def update_user(self, user_id: str) -> MongoCRUD:
        return self

    
    def update_transaction(self, user_id: str, transaction_id: str) -> MongoCRUD:
        return self

    
    """
    " DELETE part
    """
    def delete_user(self, user_id: str) -> MongoCRUD:
        return self
    

    def delete_transaction(self, transaction_id: str) -> MongoCRUD:
        return self