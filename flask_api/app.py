print("app.py file is executing")

from flask import Flask
from flask_cors import CORS
from config import Config
from db import db
from routes.auth import auth_bp
from routes.books import books_bp
from routes.summary import summary_bp

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

# Register routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(books_bp, url_prefix="/api/books")
app.register_blueprint(summary_bp, url_prefix="/api/summary")

if __name__ == "__main__":
    print("Flask API is starting...")
    app.run(debug=True)
