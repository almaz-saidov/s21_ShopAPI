from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from config import settings


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL

    from application.api.addresses.routes import bp as addresses_bp
    from application.api.clients.routes import bp as clients_bp
    from application.api.images.routes import bp as images_bp
    from application.api.products.routes import bp as products_bp
    from application.api.suppliers.routes import bp as suppliers_bp

    app.register_blueprint(addresses_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(suppliers_bp)

    SWAGGER_URL = '/swagger/index.html'
    API_URL = '/static/swagger.yaml'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': 'Shop API'}
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
