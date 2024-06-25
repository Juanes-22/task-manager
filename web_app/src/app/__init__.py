from flask import Flask, render_template

def create_app(app_config: object = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    if not app_config:
        from .config import DevelopmentConfig

        app_config = DevelopmentConfig

    app.config.from_object(app_config)

    from .tasks.views import web_bp
    from .tasks.routes import tasks_bp
    from .auth.routes import auth_bp
    from .auth.views import auth_web_bp
    from .common.error_handlers import errors_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(auth_web_bp)
    app.register_blueprint(errors_bp)

    from .extensions import db, ma, jwt, migrate

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    return app
