from flask import Flask
from flask_jwt_extended import JWTManager
from .DB.db import db
from flask_migrate import Migrate
from app.DB.database import init_db

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    jwt = JWTManager(app)

    with app.app_context():
        init_db()

        from app.Models import UserModel, CategoryModel, CurrencyModel, RecordModel
        from app.routes import init_routes
        from app.errors import init_errors
        from app.JWTManager import JWT_Manager

        init_routes(app)
        init_errors(app)
        JWT_Manager(app, jwt)

    return app
