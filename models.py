from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

def connect_db(app):
    """Connect the db"""
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png') 

    posts = db.relationship('Post', backref='users', cascade='all')

    def __repr__(self):
        """Respresentation of self; user"""
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Post Model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now()) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

    def __repr__(self):
        """Respresentation of self; date & time of post creation"""
        return f'{self.created_at}'

class PostTag(db.Model):
    """Tags on a Post Model"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    """Tag Model"""

    __tablename__ = 'tags'

    post_tags = db.relationship('Post', secondary='posts_tags', backref='tags', cascade='all')
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        """Respresentation of self; tag name"""
        return f'{self.name}'
