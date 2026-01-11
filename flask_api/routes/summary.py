from flask import Blueprint, request, jsonify
from db import db
from models import Book
from summarizer import summarize_text

summary_bp = Blueprint("summary", __name__)

@summary_bp.route("/generate", methods=["POST"])
def generate_summary():
    data = request.json

    book_id = data.get("book_id")
    text = data.get("text")

    # Case 1: Summary from existing book
    if book_id:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404

        summary = summarize_text(book.raw_text)
        book.summary = summary

    # Case 2: Summary from direct text
    elif text:
        summary = summarize_text(text)
        return jsonify({"summary": summary}), 200

    else:
        return jsonify({"error": "book_id or text required"}), 400

    db.session.commit()

    return jsonify({
        "message": "Summary generated successfully",
        "book_id": book.id,
        "summary": summary
    }), 200
