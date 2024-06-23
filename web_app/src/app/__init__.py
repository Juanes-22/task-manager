from flask import Flask, render_template

def create_app(app_config: object = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    if not app_config:
        from .config import DevelopmentConfig

        app_config = DevelopmentConfig

    app.config.from_object(app_config)

    from .routes.web import web_bp
    from .routes.tasks import tasks_bp
    from .routes.auth import auth_bp
    from .routes.errors import errors_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(errors_bp)

    from .extensions import db, ma, jwt

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app
