from flask import Flask
from flask.cli import with_appcontext

from .auth.models import User, Role
from .extensions import db

def create_users_and_roles():
    admin_role = Role(name="Admin", slug="admin")
    user_role = Role(name="User", slug="user")
    
    db.session.add(admin_role)
    db.session.add(user_role)
    db.session.commit()

    admin = User(username="admin", email="admin@example.com", password="password1")
    user1 = User(username="user1", email="user1@example.com", password="password2")
    user2 = User(username="user2", email="user2@example.com", password="password3")

    admin.hash_password()
    user1.hash_password()
    user2.hash_password()

    admin.roles.extend([admin_role, user_role])
    user1.roles.append(user_role)

    db.session.add(admin)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()


def register_commands(app: Flask):
    @app.cli.command("seed")
    @with_appcontext
    def seed():
        """Seed the database with initial data."""
        create_users_and_roles()
        print("Added 3 users to the database and roles ['admin', 'user'].")
