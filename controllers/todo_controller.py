from flask import Blueprint, make_response, request
from models.todo import Todo
from services.todo_service import *
todo_controller = Blueprint("todo_controller", __name__,  url_prefix="/api/todos")


@todo_controller.route("", methods=["GET"])
def list():
    todos = list_todos()
    return make_response({
        "message": "todo has been listed successfully",
        "data": todos
    }), 200


@todo_controller.route("/<id>", methods=["GET"])
def retrieve(id):

    try:
        todo = retrieve_todo(id).to_dict()

        return make_response({
            "message": "todo has been retrieved successfully",
            "data": todo
        }), 200

    except Exception as e:
        return make_response({
            "message": str(e),
        }), 404


@todo_controller.route("", methods=["POST"])
def create():
    try:
        title = request.json["title"]

        if not title:
            raise Exception("title must be empty")

        todo = create_todo(title).to_dict()

        return make_response({
            "message": "todo has been created successfully",
            "data": todo
        }), 201
    
    except Exception as e:
        return make_response({
                "message": str(e),
            }), 400


@todo_controller.route("/<id>", methods=["PUT"])
def update(id):
    try:

        title=request.json["title"]
        completed=request.json["completed"]

        if not title or completed == None:
            raise Exception("title and completed are mandatory fields.")

        todo = Todo(title, completed=completed)

        todo = update_todo(id, todo).to_dict()

        return make_response({
            "message": "todo has been updated successfully",
            "data": todo
        }), 200
    
    except Exception as e:
        return make_response({
            "message": str(e),
        }), 400


@todo_controller.route("/<id>", methods=["DELETE"])
def delete(id):
    try:
        todo = delete_todo(id).to_dict()

        return make_response({
            "message": "todo has been deleted successfully",
            "data": todo
        }), 200

    except Exception as e:
        return make_response({
            "message": str(e),
        }), 404
