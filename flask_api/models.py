from db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # 🔹 Basic auth fields
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # 🔹 Extended registration fields (6–7 parameters)
    gender = db.Column(db.String(20))
    age = db.Column(db.Integer)
    qualification = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    country = db.Column(db.String(100))

    # 🔹 Role-based access
    role = db.Column(db.String(20), default="user")  # user / admin

    # 🔹 Relationships
    books = db.relationship("Book", backref="user", lazy=True)
    logs = db.relationship("SummaryLog", backref="user", lazy=True)


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150))
    raw_text = db.Column(db.Text)
    summary = db.Column(db.Text)

    # 🔹 Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 🔹 Relationship
    logs = db.relationship("SummaryLog", backref="book", lazy=True)


class SummaryLog(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
