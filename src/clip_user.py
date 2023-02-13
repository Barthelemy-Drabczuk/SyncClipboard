class ClipUser:
    """_summary_
    """

    def __init__(self, username: str, password: str, email: str) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.hash = hash(self.username \
            + self.password \
            + self.email
            )


    def to_json(self) -> dict:
        return {
            "id": self.hash,
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }


    def __str__(self) -> str:
        return str(self.to_json())