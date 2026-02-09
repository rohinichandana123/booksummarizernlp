from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User, Log

auth_bp = Blueprint("auth", __name__)

# ================= REGISTER =================
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        
        # Check if user already exists
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 400
        
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "Username already taken"}), 400
        
        user = User(
            username=data["username"],
            email=data["email"],
            password=generate_password_hash(data["password"]),
            gender=data.get("gender"),
            age=data.get("age"),
            qualification=data.get("qualification"),
            occupation=data.get("occupation"),
            country=data.get("country"),
            role=data.get("role", "user")  # ✅ ADDED (user/admin)
        )
        
        db.session.add(user)
        db.session.flush()
        
        # Log registration
        log = Log(
            user_id=user.id,
            action="User registered"
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({"message": "Registered successfully"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ================= LOGIN =================
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        user = User.query.filter_by(email=data["email"]).first()
        
        if not user or not check_password_hash(user.password, data["password"]):
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Log login
        log = Log(
            user_id=user.id,
            action="User logged in"
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            "user_id": user.id,
            "username": user.username,
            "role": user.role   # ✅ already correct
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= ADMIN: GET ALL USERS =================
@auth_bp.route("/users", methods=["GET"])
def get_users():
    try:
        admin_id = request.args.get("admin_id")
        admin = User.query.get(admin_id)

        # ✅ ADMIN CHECK
        if not admin or admin.role != "admin":
            return jsonify({"error": "Unauthorized access"}), 403
        
        users = User.query.all()
        output = [{
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "book_count": len(u.books)
        } for u in users]
        
        return jsonify(output)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= USER LOGS =================
@auth_bp.route("/logs/<int:user_id>", methods=["GET"])
def get_user_logs(user_id):
    try:
        logs = Log.query.filter_by(user_id=user_id)\
                        .order_by(Log.created_at.desc())\
                        .limit(50).all()
        
        output = [{
            "id": l.id,
            "action": l.action,
            "book_id": l.book_id,
            "created_at": l.created_at.isoformat() if l.created_at else None
        } for l in logs]
        
        return jsonify(output)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@auth_bp.route("/history/<int:user_id>", methods=["GET"])
def upload_history(user_id):
    try:
        logs = (
            Log.query
            .filter_by(user_id=user_id)
            .order_by(Log.created_at.desc())
            .all()
        )

        return jsonify([{
            "action": l.action,
            "book_id": l.book_id,
            "created_at": l.created_at.isoformat()
        } for l in logs])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= ALL SYSTEM LOGS (ADMIN) =================
@auth_bp.route("/logs/all", methods=["GET"])
def get_all_logs():
    """
    Admin endpoint to fetch all system logs with user information
    """
    try:
        # Get all logs with user information
        logs = db.session.query(Log, User).join(User, Log.user_id == User.id)\
                         .order_by(Log.created_at.desc())\
                         .limit(500).all()  # Limit to 500 most recent logs
        
        output = []
        for log, user in logs:
            output.append({
                "id": log.id,
                "action": log.action,
                "book_id": log.book_id,
                "user_id": log.user_id,
                "username": user.username,
                "created_at": log.created_at.isoformat() if log.created_at else None
            })
        
        return jsonify(output)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
