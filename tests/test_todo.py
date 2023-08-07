import unittest
import json
from flask import Flask
from configs.database import db
from app import todo_controller
from models.todo import Todo
from os import getenv
import uuid

class TodoAppIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.register_blueprint(todo_controller)
        self.client = self.app.test_client()

        self.app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URL")
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_with_empty_mandatory_fields(self):
        new_todo = {"title": ""}
        response = self.client.post("/api/todos", json=new_todo)
        self.assertEqual(400, response.status_code)
        self.assertEqual("title must be not empty", json.loads(response.data)["message"])

    def test_retrieve_with_wrong_id(self):
        id = uuid.uuid4()
        response = self.client.get(f"/api/todos/{id}")

        self.assertEqual(404, response.status_code)
        self.assertEqual("todo not found", json.loads(response.data)["message"])

    def test_create_and_retrieve_todo(self):
        new_todo_data = {"title": "New Todo"}
        response = self.client.post("/api/todos", json=new_todo_data)
        self.assertEqual(response.status_code, 201)
        created_todo = json.loads(response.data)["data"]
        self.assertIsNotNone(created_todo["id"])
        self.assertEqual(new_todo_data["title"], created_todo["title"])
        self.assertFalse(created_todo["completed"])

        response = self.client.get(f"/api/todos/{created_todo['id']}")
        self.assertEqual(200, response.status_code)
        retrieved_todo = json.loads(response.data)["data"]
        self.assertEqual(created_todo, retrieved_todo)

    def test_list_todos(self):
        sample_todos = [
            {"title": "Todo 1"},
            {"title": "Todo 2"},
            {"title": "Todo 3"},
        ]
        with self.app.app_context():
            for todo_data in sample_todos:
                todo = Todo(**todo_data)
                db.session.add(todo)
            db.session.commit()

        response = self.client.get("/api/todos")
        self.assertEqual(200, response.status_code)
        todos_list = json.loads(response.data)["data"]
        self.assertEqual(len(sample_todos), len(todos_list))
        for todo_data, retrieved_todo in zip(sample_todos, todos_list):
            self.assertEqual(retrieved_todo["title"], todo_data["title"])
            self.assertFalse(retrieved_todo["completed"])

    def test_update_with_empty_mandatory_fields(self):
        new_todo_data = {"title": "New Todo"}
        response = self.client.post("/api/todos", json=new_todo_data)
        self.assertEqual(201, response.status_code)
        created_todo = json.loads(response.data)["data"]

        created_todo["title"] = ""

        response = self.client.put(f"/api/todos/{created_todo['id']}", json=created_todo)
        self.assertEqual(400, response.status_code)
        self.assertEqual("title and completed are mandatory fields.", json.loads(response.data)["message"])

    def test_update_and_delete_todo(self):
        new_todo_data = {"title": "New Todo"}
        response = self.client.post("/api/todos", json=new_todo_data)
        self.assertEqual(201, response.status_code)
        created_todo = json.loads(response.data)["data"]

        update_data = {"title": "Updated Todo", "completed": True}
        response = self.client.put(f"/api/todos/{created_todo['id']}", json=update_data)
        self.assertEqual(200, response.status_code)
        updated_todo = json.loads(response.data)["data"]
        self.assertEqual(created_todo["id"], updated_todo["id"])
        self.assertEqual(update_data["title"], updated_todo["title"])
        self.assertTrue(updated_todo["completed"])

        response = self.client.delete(f"/api/todos/{created_todo['id']}")
        self.assertEqual(200, response.status_code)

        response = self.client.get(f"/api/todos/{created_todo['id']}")
        self.assertEqual(404, response.status_code)

if __name__ == "__main__":
    unittest.main()
