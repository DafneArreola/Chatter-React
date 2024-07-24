from flask import Flask
from backend.config import Config
from backend.database import db, migrate


def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)



    with app.app_context():
        db.create_all()
    
    def timestamp_to_hms(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    app.jinja_env.filters['timestamp_to_hms'] = timestamp_to_hms

    from backend.routes import main
    app.register_blueprint(main)

    return app

