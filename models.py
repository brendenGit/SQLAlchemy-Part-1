"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class"""

    def __repr__(self):
        return f"User_id={self.id}, first_name={self.first_name}, last_name={self.last_name}"


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
    
    #relationship: post -> tags through post_tags
    tags = db.relationship('Tag', secondary='post_tags', backref='associated_posts')


class Tag(db.Model):
    """Tag class"""

    __tablename__ = 'tags'

    tag_name = db.Column(db.String(20),
                    primary_key=True,
                    nullable=False,
                    unique=True)
    
    #relationship: tag -> posts through post_tags
    posts = db.relationship('PostTag', backref='tags')

    def __repr__(self):
        return f"Tag Name={self.tag_name}"
    

class PostTag(db.Model):
    """Mapping of tags to posts"""

    __tablename__ = 'post_tags'

    tag_name = db.Column(db.Text,
                       db.ForeignKey("tags.tag_name"),
                       primary_key=True)

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    
    def __repr__(self):
        return f"Tag Name={self.tag_name}, Post ID={self.post_id}, Post Title={self.posts_associated.title}"