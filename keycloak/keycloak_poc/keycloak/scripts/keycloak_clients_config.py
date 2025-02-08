from keycloak import KeycloakAdmin
import sys
import time

# Keycloak server details
KEYCLOAK_URL = "http://keycloak:8080/"
PERM_ADMIN_USERNAME = "permanent_admin"
PERM_ADMIN_PASSWORD = "strong_permanent_password"
REALM_NAME = "pocrealm"
CLIENTS = [
    {
        "client_id": "client-web",
        "redirect_uris": ["*"],
        "post_logout_redirect_uris": ["*"],
        "web_origins": ["*"],
        "capabilities": {"standardFlowEnabled": True, "directAccessGrantsEnabled": True},
    },
    {
        "client_id": "client-api",
        "redirect_uris": ["*"],
        "capabilities": {"standardFlowEnabled": True, "directAccessGrantsEnabled": True},
    },
]

def login_to_keycloak_realm(username, password, realm, userrealm):
    """Wait until Keycloak is reachable and return an authenticated KeycloakAdmin instance."""
    for _ in range(20):  # Retry 20 times
        try:
            admin = KeycloakAdmin(
                server_url=KEYCLOAK_URL,
                username=username,
                password=password,
                realm_name=realm,
                user_realm_name=userrealm,
                verify=True,
            )
            print(f"Keycloak is ready! Logged in as '{username}' on realm '{realm}'.")
            return admin
        except Exception as e:
            print(f"Waiting for Keycloak to become available... Error: {e}")
            time.sleep(10)
    print("Keycloak did not become ready in time.", file=sys.stderr)
    sys.exit(1)
def configure_clients(admin):
    """Create and configure clients in the target realm."""
    try:
        admin.realm_name = REALM_NAME  # Switch to the target realm
        for client in CLIENTS:
            existing_clients = admin.get_clients()
            existing_client = next((c for c in existing_clients if c["clientId"] == client["client_id"]), None)

            if not existing_client:
                admin.create_client(
                    {
                        "clientId": client["client_id"],
                        "redirectUris": client["redirect_uris"],
                        "webOrigins": client.get("web_origins", []),
                        "publicClient": True,
                        "attributes": {
                            "post.logout.redirect.uris": " ".join(client.get("post_logout_redirect_uris", [])),
                        },
                        **client.get("capabilities", {}),
                    }
                )
                print(f"Client '{client['client_id']}' created in realm '{REALM_NAME}'.")
            else:
                print(f"Client '{client['client_id']}' already exists in realm '{REALM_NAME}'. Updating...")
                admin.update_client(
                    existing_client["id"],
                    {
                        "redirectUris": client["redirect_uris"],
                        "webOrigins": client.get("web_origins", []),
                        "attributes": {
                            "post.logout.redirect.uris": " ".join(client.get("post_logout_redirect_uris", [])),
                        },
                        **client.get("capabilities", {}),
                    },
                )
                print(f"Client '{client['client_id']}' updated in realm '{REALM_NAME}'.")
    except Exception as e:
        print(f"Error configuring clients in realm '{REALM_NAME}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Log in as permanent admin to master realm
    permanent_admin = login_to_keycloak_realm(PERM_ADMIN_USERNAME, PERM_ADMIN_PASSWORD,"pocrealm","master")

    # Ensure the realm exists
    try:
        realms = permanent_admin.get_realms()
        if not any(realm["realm"] == REALM_NAME for realm in realms):
            permanent_admin.create_realm({"realm": REALM_NAME, "enabled": True})
            print(f"Realm '{REALM_NAME}' created.")
        else:
            print(f"Realm '{REALM_NAME}' already exists.")
    except Exception as e:
        print(f"Error creating or checking realm '{REALM_NAME}': {e}", file=sys.stderr)
        sys.exit(1)

    # Configure clients in the target realm
    configure_clients(permanent_admin)
    print("Client configuration in target realm complete.")

if __name__ == "__main__":
    main()
