import psycopg2
from ..config import SQLALCHEMY_DATABASE_URI

conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
