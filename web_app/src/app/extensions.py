from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

ma = Marshmallow()

csrf = CSRFProtect()

jwt = JWTManager()

migrate = Migrate()
