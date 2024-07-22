from flask import Flask
from backend.config import Config
from backend.database import db, migrate



def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from backend.routes import main
        app.register_blueprint(main)
        db.create_all()

    # Register the custom Jinja2 filter
    @app.template_filter('string_padding')
    def string_padding(value, length, char='0'):
        return str(value).zfill(length)


    return app

