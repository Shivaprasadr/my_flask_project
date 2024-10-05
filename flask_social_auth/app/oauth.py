import os
from flask import session
from flask_login import current_user, login_user
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.github import github, make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from app.models import db, OAuth, User
import logging

logging.basicConfig(level=logging.DEBUG)

# Create the GitHub OAuth blueprint with comprehensive scopes
github_blueprint = make_github_blueprint(
    client_id=os.getenv("GITHUB_ID"),
    client_secret=os.getenv("GITHUB_SECRET"),
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
    redirect_to=None,
)

@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    if token:
        logging.debug(f"GitHub OAuth token: {token}")
    else:
        logging.error("GitHub token exchange failed")
        session.pop('github_oauth_token', None)
        return

    # Fetch user info from GitHub
    info = github.get("/user")
    if info.ok:
        try:
            account_info = info.json()
            logging.debug(f"GitHub user data: {account_info}")

            # Fetch standard and additional user details
            username = account_info.get("login", "")
            github_id = str(account_info.get("id", ""))
            avatar_url = account_info.get("avatar_url", "")
            name = account_info.get("name", "")
            bio = account_info.get("bio", "")
            company = account_info.get("company", "")
            location = account_info.get("location", "")
            blog = account_info.get("blog", "")
            followers = account_info.get("followers", 0)
            following = account_info.get("following", 0)
            created_at = account_info.get("created_at", "")
            profile_url = account_info.get("html_url", "")
            email = account_info.get("email", "")
            google_id = None  # Set to None for OAuth users

            # Check if the user exists in the database
            query = User.query.filter_by(username=username)
            try:
                user = query.one()

                # Update existing user's details if missing or changed
                user.github_id = github_id if github_id not in [None, ""] else user.github_id
                user.avatar_url = avatar_url if avatar_url not in [None, ""] else user.avatar_url
                user.profile_url = profile_url if profile_url not in [None, ""] else user.profile_url
                user.created_at = created_at if created_at not in [None, ""] else user.created_at
                user.name = name if name not in [None, ""] else user.name
                user.bio = bio if bio not in [None, ""] else user.bio
                user.company = company if company not in [None, ""] else user.company
                user.location = location if location not in [None, ""] else user.location
                user.blog = blog if blog not in [None, ""] else user.blog
                user.followers = followers if followers not in [None, "", 0] else user.followers
                user.following = following if following not in [None, "", 0] else user.following
                
                # Only update email if it is new or the user doesn't have one
                if not user.email or user.email != email:
                    user.email = email
                
                # Set password to None for OAuth users
                user.password = None
                
                db.session.commit()

            except NoResultFound:
                # Create a new user with all available details
                user = User(
                    username=username,
                    github_id=github_id,
                    email=email,
                    avatar_url=avatar_url,
                    name=name,
                    bio=bio,
                    company=company,
                    location=location,
                    blog=blog,
                    followers=followers,
                    following=following,
                    created_at=created_at,
                    profile_url=profile_url,
                    google_id=google_id,
                    password=None  # Password is None for OAuth users
                )
                db.session.add(user)
                db.session.commit()
            
            # Log in the user
            login_user(user)

            # Optionally clear OAuth token after successful login
            session.pop('github_oauth_token', None)

        except Exception as e:
            logging.error(f"Error processing GitHub user data: {e}")
    else:
        logging.error(f"Failed to fetch GitHub user info: {info.status_code}, {info.text}")

# Create the Google OAuth blueprint with required scopes
google_blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
    redirect_to=None,
)

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if token:
        logging.debug(f"Google OAuth token: {token}")
    else:
        logging.error("Google token exchange failed")
        session.pop('google_oauth_token', None)
        return

    # Fetch user info from Google
    info = google.get("/oauth2/v2/userinfo")
    if info.ok:
        try:
            account_info = info.json()
            logging.debug(f"Google user data: {account_info}")

            # Fetch standard user details
            username = account_info.get("name", "")
            google_id = str(account_info.get("id", ""))
            avatar_url = account_info.get("picture", "")
            name = account_info.get("name", "")
            email = account_info.get("email", "")
            profile_url = f"https://plus.google.com/{google_id}"
            created_at = ""
            github_id = ""
            bio = ""
            company = ""
            location = ""
            blog = ""
            followers = ""
            following = ""

            # Check if the user exists in the database
            query = User.query.filter_by(username=username)
            try:
                user = query.one()

                # Update existing user's details if missing or changed
                user.google_id = google_id if google_id not in [None, ""] else user.google_id
                user.avatar_url = avatar_url if avatar_url not in [None, ""] else user.avatar_url
                user.profile_url = profile_url if profile_url not in [None, ""] else user.profile_url
                user.created_at = created_at if created_at not in [None, ""] else user.created_at
                user.name = name if name not in [None, ""] else user.name
                user.bio = bio if bio not in [None, ""] else user.bio
                user.company = company if company not in [None, ""] else user.company
                user.location = location if location not in [None, ""] else user.location
                user.blog = blog if blog not in [None, ""] else user.blog
                user.followers = followers if followers not in [None, "", 0] else user.followers
                user.following = following if following not in [None, "", 0] else user.following

                # Only update email if it is new or the user doesn't have one
                if not user.email or user.email != email:
                    user.email = email
                
                # Set password to None for OAuth users
                user.password = None
                
                db.session.commit()

            except NoResultFound:
                # Create a new user with all available details
                user = User(
                    username=username,
                    google_id=google_id,
                    email=email,
                    avatar_url=avatar_url,
                    name=name,
                    created_at=created_at,
                    profile_url=profile_url,
                    github_id=github_id,
                    bio=bio,
                    company=company,
                    location=location,
                    blog=blog,
                    followers=followers,
                    following=following,
                    password=None  # Password is None for OAuth users
                )
                db.session.add(user)
                db.session.commit()
            
            # Log in the user
            login_user(user)

            # Optionally clear OAuth token after successful login
            session.pop('google_oauth_token', None)

        except Exception as e:
            logging.error(f"Error processing Google user data: {e}")
    else:
        logging.error(f"Failed to fetch Google user info: {info.status_code}, {info.text}")
