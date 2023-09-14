"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    
    #post relationship 1 to many
    posts = db.relationship( 'Post', backref='user')
    
class Post(db.Model):
    """Post class"""

    def __repr__(self):
        return f"Post_id={self.id}, title={self.title}, created_at={self.created_at}"

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    title = db.Column(db.String(100),
                           nullable=False)
    
    content = db.Column(db.String,
                          nullable=False)
    
    created_at = db.Column(db.DateTime, 
                           default=datetime.utcnow,
                           nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))