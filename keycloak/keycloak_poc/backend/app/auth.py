from flask import request, jsonify
from functools import wraps
import requests

KEYCLOAK_SERVER_URL = "http://keycloak:8080"
REALM_NAME = "myrealm"
CLIENT_ID = "client-api"

def verify_token(token):
    """Verify the access token with Keycloak."""
    url = f"{KEYCLOAK_SERVER_URL}/realms/{REALM_NAME}/protocol/openid-connect/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def require_auth():
    """Decorator to enforce authentication on routes."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid token"}), 401

            token = auth_header.split(" ")[1]
            user_info = verify_token(token)
            if not user_info:
                return jsonify({"error": "Invalid or expired token"}), 401

            request.user = user_info  # Attach user info to the request object
            return f(*args, **kwargs)

        return wrapper

    return decorator
