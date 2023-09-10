"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    first_name = db.Column(db.String(30),
                           nullable=False)
    
    last_name = db.Column(db.String(30),
                          nullable=False)
    
    profile_picture = db.Column(db.String,
                                nullable=False,
                                default='/static/df_prof_pic.PNG')