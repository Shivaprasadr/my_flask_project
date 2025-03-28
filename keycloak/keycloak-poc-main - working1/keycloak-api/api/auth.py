import json
import os
from urllib.request import urlopen
import time
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.jose.rfc7517.jwk import JsonWebKey
from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.oauth2.rfc6750.errors import InvalidTokenError
import logging

from api.models import verify_user

# Configure logging
logger = logging.getLogger("auth_logger")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
KEYCLOAK_REALM_NAME = os.getenv("KEYCLOAK_REALM_NAME")

KEYCLOAK_ISSUER = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM_NAME}"


from authlib.jose import jwt
from flask import request, jsonify

class ClientCredsTokenValidator(JWTBearerTokenValidator):
    def __init__(self, issuer):
        logger.info(f"Initializing ClientCredsTokenValidator with issuer: {issuer}")
        try:
            jsonurl = urlopen(f"{issuer}/protocol/openid-connect/certs")
            public_key = JsonWebKey.import_key_set(json.loads(jsonurl.read()))
            super(ClientCredsTokenValidator, self).__init__(public_key)
            self.claims_options = {
                "exp": {"essential": True},
                "iss": {"essential": True, "value": issuer},
            }
            logger.info("Successfully initialized ClientCredsTokenValidator")
        except Exception as e:
            logger.error(f"Failed to initialize ClientCredsTokenValidator: {e}")
            raise

    def authenticate_token(self, token_string):
        logger.info(f"Authenticating token: {token_string}")
        try:
            decoded_token = jwt.decode(token_string, self.public_key, claims_options=self.claims_options)
            logger.debug(f"Decoded Token: {decoded_token}")

            # Explicitly check the 'azp' claim
            if decoded_token.get("azp") != "client-web":
                logger.error(f"Token 'azp' claim mismatch. Expected 'client-web', got '{decoded_token.get('azp')}'")
                raise InvalidTokenError(description="Unauthorized azp claim")

            return decoded_token
        except Exception as e:
            logger.error(f"Failed to authenticate token: {e}")
            return None

    def validate_token(self, token, scopes, request):
        logger.info("Starting token validation")
        if not token:
            logger.error("Token is None. Validation cannot proceed.")
            raise InvalidTokenError(realm=self.realm, extra_attributes=self.extra_attributes)
        # Ensure the token has the required method
        if not hasattr(token, "exp"):
            logger.error("Token object does not have an exp in token")
            raise TypeError("Invalid token object: missing exp details in token")

        logger.info("Token successfully validated")


require_auth = ResourceProtector()# Log the public key in a readable format
validator = ClientCredsTokenValidator(KEYCLOAK_ISSUER)
require_auth.register_token_validator(validator)