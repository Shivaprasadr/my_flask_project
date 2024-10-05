from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from . import db
from sqlalchemy import UniqueConstraint

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    
    # Allow github_id and google_id to be nullable for users who only use one login method
    github_id = db.Column(db.String(100), nullable=True)  
    google_id = db.Column(db.String(100), nullable=True)  
    
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=True)  # Password field for local users
    avatar_url = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(150), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    company = db.Column(db.String(150), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    blog = db.Column(db.String(250), nullable=True)
    followers = db.Column(db.Integer, nullable=True)
    following = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.String(100), nullable=True)
    profile_url = db.Column(db.String(250), nullable=True)

    # Unique constraints to ensure no two users have the same github_id or google_id
    __table_args__ = (
        UniqueConstraint('github_id', name='unique_github_id', deferrable=True),
        UniqueConstraint('google_id', name='unique_google_id', deferrable=True),
    )

    def __repr__(self):
        return f"<User {self.username}>"

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
