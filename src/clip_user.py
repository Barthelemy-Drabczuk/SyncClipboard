class ClipUser:
    """_summary_
    """

    def __init__(self, username: str, password: str, email: str) -> None:
        """_summary_

        Args:
            username (str): _description_
            password (str): _description_
            email (str): _description_
        """
        self.username: str = username
        self.password: int = hash(password)
        self.email: str = email
        self.hash :int = hash(self.username \
            + str(self.password) \
            + self.email
            )

    def get_username(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self.username


    def get_password(self) -> int:
        return self.password


    def get_email(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self.email


    def get_id(self) -> int:
        return self.hash


    def to_json(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        return {
            "id": self.hash,
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }


    def __str__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return str(self.to_json())