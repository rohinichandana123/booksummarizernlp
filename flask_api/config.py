class Config:
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://Rohini:npg_JcO2svwTMoG5"
        "@ep-snowy-fire-a1kfltuo-pooler.ap-southeast-1.aws.neon.tech"
        "/book_summarizer"
        "?sslmode=require"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,   # ✅ fixes closed SSL connections
        "pool_recycle": 300      # ✅ prevents Neon idle timeout issues
    }

    SECRET_KEY = "my12345"
