from flask import Flask
from os import getenv
from controllers.todo_controller import todo_controller
from configs.database import db, migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URL")
db.init_app(app)
migrate.init_app(app=app, db=db)
with app.app_context():
    db.create_all()


app.register_blueprint(todo_controller)
