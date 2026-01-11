from flask import Blueprint, request, jsonify
from db import db
from models import Book

books_bp = Blueprint("books", __name__)

@books_bp.route("/upload", methods=["POST"])
def upload_book():
    data = request.json

    book = Book(
        title=data["title"],
        author=data["author"],
        content=data["content"],
        user_id=data["user_id"]
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({"message": "Book uploaded!", "book_id": book.id})


@books_bp.route("/list/<int:user_id>", methods=["GET"])
def list_books(user_id):
    books = Book.query.filter_by(user_id=user_id).all()
    output = [{"id": b.id, "title": b.title, "author": b.author} for b in books]
    return jsonify(output)

@books_bp.route("/add", methods=["POST"])
def add_book():
    data = request.json

    book = Book(
        title=data["title"],
        author=data["author"],
        raw_text=data["text"],
        summary=data["summary"],
        user_id=data["user_id"]
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({"message": "Book saved"})

@books_bp.route("/user/<int:user_id>")
def user_books(user_id):
    books = Book.query.filter_by(user_id=user_id).all()

    return jsonify([
        {"title": b.title, "summary": b.summary}
        for b in books
    ])


