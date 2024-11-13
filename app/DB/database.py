from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Models import BaseModel
from ..config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import text
from .connection import conn
from pathlib import Path


engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    cur = conn.cursor()

    db_init_file = Path(__file__).parent / 'init_db.sql'
    with open(db_init_file, 'r') as f:
        sql = f.read()
        cur.execute(sql)
    conn.commit()
    cur.close()

    BaseModel.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        result = db.execute(text("SELECT 1 FROM \"Currency\" WHERE currency_name = :currency_name LIMIT 1"),
                            {'currency_name': "USD"}).fetchone()

        if not result:
            db.execute(text("INSERT INTO \"Currency\" (currency_name) VALUES (:currency_name)"),
                       {'currency_name': "USD"})
            db.commit()
        db.close()

    except Exception as e:
        print(f"Error while inserting default data: {e}")
        db.rollback()
        db.close()
