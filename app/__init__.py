import os

from flask import Flask
from flask_cors import CORS

from config import DevelopmentConfig, ProductionConfig
from app.database import init_db
from app.routes import api, pages


def create_app():

    app = Flask(__name__)

    # Render üzerinde production ayarlarını,
    # bilgisayarımızda development ayarlarını kullan.
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    CORS(app)

    with app.app_context():
        init_db()

    app.register_blueprint(pages)

    app.register_blueprint(
        api,
        url_prefix="/api"
    )

    @app.route("/health")
    def health():

        return {
            "basari": True,
            "mesaj": "İZDEN API aktif."
        }

    return app