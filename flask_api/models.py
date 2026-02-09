from db import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Extended registration fields
    gender = db.Column(db.String(20))
    age = db.Column(db.Integer)
    qualification = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    country = db.Column(db.String(100))
    
    # Role-based access
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    books = db.relationship("Book", backref="user", lazy=True, cascade="all, delete-orphan")
    logs = db.relationship("Log", backref="user", lazy=True, cascade="all, delete-orphan")


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)  # raw_text renamed to content to match SQL
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Additional metadata fields
    file_type = db.Column(db.String(10))  # txt, pdf
    tags = db.Column(db.String(500))  # comma-separated tags
    
    # Relationships
    summaries = db.relationship("Summary", backref="book", lazy=True, cascade="all, delete-orphan")
    logs = db.relationship("Log", backref="book", lazy=True, cascade="all, delete-orphan")


class Summary(db.Model):
    __tablename__ = "summaries"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    summary_text = db.Column(db.Text)
    summary_type = db.Column(db.String(20), default="auto")  # auto, manual, custom
    length_setting = db.Column(db.String(20), default="medium")  # short, medium, long
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=True)
    action = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
