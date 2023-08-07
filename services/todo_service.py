from configs.database import db
from models.todo import Todo

def list_todos() -> list[Todo]:
    todos:list[Todo] = db.session.query(Todo).all()
    todo_list = [todo.to_dict() for todo in todos]
    return todo_list

def retrieve_todo(id: str) -> Todo | None:
    todo = db.session.get(Todo, id)
    
    if not todo:
        raise Exception("todo not found")
    
    return todo

def create_todo(title: str) -> Todo:
    todo = Todo(title=title)
    db.session.add(todo)
    db.session.commit()
    return todo

def update_todo(id: str, todo: Todo) -> Todo:
    searched_todo = retrieve_todo(id)
    searched_todo.title = todo.title
    searched_todo.completed = todo.completed
    db.session.commit()
    return searched_todo
    

def delete_todo(id: str) -> Todo:
    todo = retrieve_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return todo

