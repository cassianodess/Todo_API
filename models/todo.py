import uuid
from sqlalchemy import Column, String, Boolean, UUID
from configs.database import db

class Todo(db.Model):
    __tablename__= "todos"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    def __init__(self, title: str, id = None, completed: bool = False) -> None:
        self.id = uuid.uuid4()
        self.title = title
        self.completed = completed

    def __repr__(self) -> str:
        return f"Todo(id={self.id}, title={self.title}, completed={self.completed})"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed
        }
    
    def dict_to_class(id, title, completed):
        return Todo(title=title, id=id, completed=completed)