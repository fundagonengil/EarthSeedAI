from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Wix ve tüm dış kaynaklardan gelen isteklere (CORS) izin ver
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Blueprint'leri içe aktar ve kaydet
    from app.routes import api_bp, page_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(page_bp)

    return app