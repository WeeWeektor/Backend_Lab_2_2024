from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from app.routes import init_routes
        from app.errors import init_errors

        init_routes(app)
        init_errors(app)

    return app
