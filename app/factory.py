from flask import Flask
from .DB.db import db
from flask_migrate import Migrate
from app.DB.database import init_db

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        init_db()

        from app.Models import UserModel, CategoryModel, CurrencyModel, RecordModel
        from app.routes import init_routes
        from app.errors import init_errors

        init_routes(app)
        init_errors(app)

    return app
