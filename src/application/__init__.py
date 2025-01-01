from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import settings


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL

    from application.api.addresses.routes import bp as addresses_bp
    from .api.clients.routes import bp as clients_bp
    from .api.images.routes import bp as images_bp
    from .api.products.routes import bp as products_bp
    from .api.suppliers.routes import bp as suppliers_bp

    app.register_blueprint(addresses_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(suppliers_bp)

    return app


