class ClipObject:
    def __init__(self, content: str) -> None:
        self.content = content

    
    def to_json(self) -> dict:
        return {"content": self.content}
    

    def get_content(self) -> str:
        return self.content