from flask import Blueprint, request, jsonify
from db import db
from models import Book, Log
import PyPDF2
import io
from datetime import datetime

books_bp = Blueprint("books", __name__)

# ───────────────── UPLOAD BOOK (TEXT) ─────────────────
@books_bp.route("/upload", methods=["POST"])
def upload_book():
    try:
        data = request.json

        book = Book(
            title=data["title"],
            author=data.get("author", ""),
            content=data["content"],
            user_id=data["user_id"],
            file_type=data.get("file_type", "txt"),
            tags=data.get("tags", "")
        )

        db.session.add(book)
        db.session.flush()

        log = Log(
            user_id=data["user_id"],
            book_id=book.id,
            action=f"Uploaded book: {book.title}"
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({"message": "Book uploaded successfully", "book_id": book.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ───────────────── LIST BOOKS (✅ MODIFIED) ─────────────────
@books_bp.route("/list/<int:user_id>", methods=["GET"])
def list_books(user_id):
    try:
        search = request.args.get("search", "")
        author_filter = request.args.get("author", "")
        tag_filter = request.args.get("tag", "")

        query = Book.query.filter_by(user_id=user_id)

        if search:
            query = query.filter(Book.title.ilike(f"%{search}%"))
        if author_filter:
            query = query.filter(Book.author.ilike(f"%{author_filter}%"))
        if tag_filter:
            query = query.filter(Book.tags.ilike(f"%{tag_filter}%"))

        books = query.order_by(Book.created_at.desc()).all()

        # ✅ ONLY CHANGE IS HERE
        output = [{
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "tags": b.tags,
            "file_type": b.file_type,
            "created_at": b.created_at.isoformat() if b.created_at else None,

            # ✅ Summary data for Dashboard Overview
            "has_summary": len(b.summaries) > 0,
            "latest_summary": (
                b.summaries[-1].summary_text if b.summaries else None
            ),
            "summary_word_count": (
                len(b.summaries[-1].summary_text.split())
                if b.summaries else 0
            )
        } for b in books]

        return jsonify(output)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ───────────────── BOOK DETAIL ─────────────────
@books_bp.route("/detail/<int:book_id>", methods=["GET"])
def get_book_detail(book_id):
    try:
        book = Book.query.get_or_404(book_id)

        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "content": book.content,
            "tags": book.tags,
            "file_type": book.file_type,
            "created_at": book.created_at.isoformat() if book.created_at else None,
            "summaries": [{
                "id": s.id,
                "summary_text": s.summary_text,
                "summary_type": s.summary_type,
                "length_setting": s.length_setting,
                "created_at": s.created_at.isoformat() if s.created_at else None
            } for s in book.summaries]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ───────────────── UPDATE BOOK ─────────────────
@books_bp.route("/update/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        data = request.json

        if "title" in data:
            book.title = data["title"]
        if "author" in data:
            book.author = data["author"]
        if "tags" in data:
            book.tags = data["tags"]

        log = Log(
            user_id=book.user_id,
            book_id=book.id,
            action=f"Updated book: {book.title}"
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({"message": "Book updated successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ───────────────── DELETE BOOK ─────────────────
@books_bp.route("/delete/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        title = book.title
        user_id = book.user_id

        log = Log(
            user_id=user_id,
            action=f"Deleted book: {title}"
        )
        db.session.add(log)

        db.session.delete(book)
        db.session.commit()

        return jsonify({"message": "Book deleted successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ───────────────── UPLOAD PDF ─────────────────
@books_bp.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text_content = ""

        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"

        title = request.form.get("title", file.filename)
        author = request.form.get("author", "")
        user_id = request.form.get("user_id")
        tags = request.form.get("tags", "")

        if not user_id:
            return jsonify({"error": "User ID required"}), 400

        book = Book(
            title=title,
            author=author,
            content=text_content,
            user_id=int(user_id),
            file_type="pdf",
            tags=tags
        )

        db.session.add(book)
        db.session.flush()

        log = Log(
            user_id=int(user_id),
            book_id=book.id,
            action=f"Uploaded PDF: {book.title}"
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({"message": "PDF uploaded successfully", "book_id": book.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ───────────────── GET ALL BOOKS (ADMIN) ─────────────────
@books_bp.route("/all", methods=["GET"])
def get_all_books():
    """
    Admin endpoint to fetch all books in the system with user information
    """
    try:
        from models import User
        
        # Get all books with user information
        books = db.session.query(Book, User).join(User, Book.user_id == User.id)\
                          .order_by(Book.created_at.desc()).all()
        
        output = []
        for book, user in books:
            output.append({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "tags": book.tags,
                "file_type": book.file_type,
                "created_at": book.created_at.isoformat() if book.created_at else None,
                "user_id": book.user_id,
                "username": user.username,
                "has_summary": len(book.summaries) > 0,
                "summary_count": len(book.summaries)
            })
        
        return jsonify(output)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
