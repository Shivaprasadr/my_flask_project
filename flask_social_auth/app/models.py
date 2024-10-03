from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    github_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=True)
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

    def __repr__(self):
        return f"<User {self.username}>"

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
