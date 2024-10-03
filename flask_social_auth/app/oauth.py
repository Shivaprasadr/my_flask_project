import os
from flask import session
from flask_login import current_user, login_user
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.github import github, make_github_blueprint
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
        logging.debug(f"OAuth token: {token}")
    else:
        logging.error("Token exchange failed")
        # Clear the session token if token exchange fails
        session.pop('github_oauth_token', None)
        return

    # Fetch user info from GitHub
    info = github.get("/user")
    if info.ok:
        try:
            account_info = info.json()
            logging.debug(f"User data: {account_info}")

            # Fetch standard and additional user details
            username = account_info.get("login", "")
            github_id = str(account_info.get("id", ""))
            avatar_url = account_info.get("avatar_url", "")
            name = account_info.get("name", "")
            bio = account_info.get("bio", "")
            company = account_info.get("company", "")
            location = account_info.get("location", "")
            blog = account_info.get("blog", "")
            followers = account_info.get("followers", "")
            following = account_info.get("following", "")
            created_at = account_info.get("created_at", "")
            profile_url = account_info.get("html_url", "")
            email = account_info.get("email", "")
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
                user.followers = followers if followers not in [None, ""] else user.followers
                user.following = following if following not in [None, ""] else user.following
                # Only update email if it is new or the user doesn't have one
                if not user.email or user.email != email:
                    user.email = email
                
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
                    profile_url=profile_url
                )
                db.session.add(user)
                db.session.commit()
            
            # Log in the user
            login_user(user)

            # Optionally clear OAuth token after successful login
            session.pop('github_oauth_token', None)

        except Exception as e:
            logging.error(f"Error processing user data: {e}")
    else:
        logging.error(f"Failed to fetch user info: {info.status_code}, {info.text}")
