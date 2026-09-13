from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Tüm route'lara ve tüm origin'lere kesin CORS izni ver
    CORS(app, resources={r"/*": {"origins": "*"}})

    from app.routes import api_bp, page_bp
    
    # Blueprint kayıtları
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(page_bp)

    return app