import unittest
import json
from flask import Flask
from configs.database import db
from app import todo_controller  # Import the Flask blueprint from app.py
from models.todo import Todo
from os import getenv

class TodoAppIntegrationTest(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app for testing
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.register_blueprint(todo_controller)
        self.client = self.app.test_client()

        # Set up an in-memory SQLite database for testing
        self.app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URL")
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_and_retrieve_todo(self):
        # Test creating a Todo item
        new_todo_data = {"title": "New Todo"}
        response = self.client.post("/api/todos", json=new_todo_data)
        self.assertEqual(response.status_code, 201)
        created_todo = json.loads(response.data)["data"]
        self.assertIsNotNone(created_todo["id"])
        self.assertEqual(created_todo["title"], new_todo_data["title"])
        self.assertFalse(created_todo["completed"])

        # Test retrieving the created Todo item
        response = self.client.get(f"/api/todos/{created_todo['id']}")
        self.assertEqual(response.status_code, 200)
        retrieved_todo = json.loads(response.data)["data"]
        self.assertEqual(retrieved_todo, created_todo)

    def test_list_todos(self):
        # Create some sample Todo items in the database
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

        # Test listing all Todo items
        response = self.client.get("/api/todos")
        self.assertEqual(response.status_code, 200)
        todos_list = json.loads(response.data)["data"]
        self.assertEqual(len(todos_list), len(sample_todos))
        for todo_data, retrieved_todo in zip(sample_todos, todos_list):
            self.assertEqual(todo_data["title"], retrieved_todo["title"])
            self.assertFalse(retrieved_todo["completed"])

    def test_update_and_delete_todo(self):
        # Create a Todo item to update and delete
        new_todo_data = {"title": "New Todo"}
        response = self.client.post("/api/todos", json=new_todo_data)
        self.assertEqual(response.status_code, 201)
        created_todo = json.loads(response.data)["data"]

        # Test updating the Todo item
        update_data = {"title": "Updated Todo", "completed": True}
        response = self.client.put(f"/api/todos/{created_todo['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_todo = json.loads(response.data)["data"]
        self.assertEqual(updated_todo["id"], created_todo["id"])
        self.assertEqual(updated_todo["title"], update_data["title"])
        self.assertTrue(updated_todo["completed"])

        # Test deleting the Todo item
        response = self.client.delete(f"/api/todos/{created_todo['id']}")
        self.assertEqual(response.status_code, 200)

        # Test retrieving the deleted Todo item (should return 404)
        response = self.client.get(f"/api/todos/{created_todo['id']}")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
