from flask import Blueprint, request, jsonify
from db import db
from models import Book, Summary, Log
from summarizer import summarize_text

summary_bp = Blueprint("summary", __name__)

@summary_bp.route("/generate", methods=["POST"])
def generate_summary():
    try:
        # Check if it's a file upload
        if 'pdf' in request.files or 'text_file' in request.files:
            if 'pdf' in request.files:
                file = request.files['pdf']
                from summarizer import extract_text_from_pdf
                text = extract_text_from_pdf(file.read())
            else:
                file = request.files['text_file']
                text = file.read().decode('utf-8')

            user_id = request.form.get("user_id")
            length_setting = request.form.get("length_setting", "medium")
        else:
            data = request.json
            book_id = data.get("book_id")
            text = data.get("text")
            length_setting = data.get("length_setting", "medium")
            user_id = data.get("user_id")

            # Case 1: Summary from existing book
            if book_id:
                book = Book.query.get_or_404(book_id)
                summary_text = summarize_text(book.content)

                # Create summary record
                summary = Summary(
                    book_id=book.id,
                    summary_text=summary_text,
                    summary_type="auto",
                    length_setting=length_setting
                )
                db.session.add(summary)

                # Log the action
                log = Log(
                    user_id=book.user_id,
                    book_id=book.id,
                    action=f"Generated summary for: {book.title}"
                )
                db.session.add(log)
                db.session.commit()

                return jsonify({
                    "message": "Summary generated successfully",
                    "book_id": book.id,
                    "summary_id": summary.id,
                    "summary": summary_text
                })

        # Case 2: Summary from direct text or uploaded file
        if text:
            summary_text = summarize_text(text)

            # Log if user_id provided
            if user_id:
                log = Log(
                    user_id=user_id,
                    action="Generated summary from direct source"
                )
                db.session.add(log)
                db.session.commit()

            return jsonify({"summary": summary_text})

        else:
            return jsonify({"error": "book_id, text, or file required"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@summary_bp.route("/book/<int:book_id>", methods=["GET"])
def get_book_summaries(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        summaries = Summary.query.filter_by(book_id=book_id).order_by(Summary.created_at.desc()).all()

        output = [{
            "id": s.id,
            "summary_text": s.summary_text,
            "summary_type": s.summary_type,
            "length_setting": s.length_setting,
            "created_at": s.created_at.isoformat() if s.created_at else None
        } for s in summaries]

        return jsonify(output)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
