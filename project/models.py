from flask_login import UserMixin
from datetime import datetime
from . import db

class User(UserMixin, db.Model):
    """
    User model for the application.

    Attributes:
    id (int): Unique identifier for the user.
    name (str): Name of the user.
    email (str): Email of the user.
    password (str): Password of the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Todo(db.Model):
    """
    Todo model for the application.

    Attributes:
    id (int): Unique identifier for the todo.
    title (str): Title of the todo.
    user_id (int): Identifier of the user who owns the todo.
    date (date): The date on which the todo is created.
    created_at (datetime): The datetime when the todo is created.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
