from flask import Flask
from flask_cors import CORS

from config import config
from app.database import init_db
from app.routes import api_bp, page_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(config["development"])

    CORS(app)

    with app.app_context():
        init_db()

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(page_bp)

    @app.route("/health")
    def health():
        return {
            "basari": True,
            "mesaj": "Earthseed backend aktif"
        }

    return app