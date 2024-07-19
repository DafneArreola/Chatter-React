from flask import Flask
from backend.config import Config
from backend.database import db

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from backend.routes import main
        app.register_blueprint(main)
        db.create_all()

    return app

