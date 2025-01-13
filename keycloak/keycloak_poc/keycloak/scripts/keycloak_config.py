from keycloak import KeycloakAdmin
import time
import sys

# Keycloak server details
KEYCLOAK_URL = "http://keycloak:8080/"
TEMP_ADMIN_USERNAME = "admin"
TEMP_ADMIN_PASSWORD = "admin_password"
PERM_ADMIN_USERNAME = "permanent_admin"
PERM_ADMIN_PASSWORD = "strong_permanent_password"
REALM_NAME = "myrealm"
CLIENT_ID = "client-api"
CLIENT_SECRET = "secret"

def wait_for_keycloak(username, password):
    """Wait until Keycloak is reachable."""
    for _ in range(20):  # Retry 20 times
        try:
            admin = KeycloakAdmin(
                server_url=KEYCLOAK_URL,
                username=username,
                password=password,
                realm_name="master",
                verify=True,
            )
            print("Keycloak is ready!")
            return admin
        except Exception as e:
            print(f"Waiting for Keycloak to become available... Error: {e}")
            time.sleep(10)
    print("Keycloak did not become ready in time.", file=sys.stderr)
    sys.exit(1)

def create_permanent_admin(temp_admin):
    """Create a permanent admin account and assign necessary roles."""
    try:
        users = temp_admin.get_users({"username": PERM_ADMIN_USERNAME})
        if not users:
            temp_admin.create_user(
                {
                    "username": PERM_ADMIN_USERNAME,
                    "enabled": True,
                    "credentials": [
                        {
                            "type": "password",
                            "value": PERM_ADMIN_PASSWORD,
                            "temporary": False,
                        }
                    ],
                }
            )
            print(f"Permanent admin '{PERM_ADMIN_USERNAME}' created.")

            # Assign realm-admin roles to the permanent admin
            user_id = temp_admin.get_user_id(PERM_ADMIN_USERNAME)
            realm_roles = temp_admin.get_realm_roles()
            realm_admin_role = next(
                (role for role in realm_roles if role["name"] == "admin"), None
            )
            if realm_admin_role:
                temp_admin.assign_realm_roles(user_id, [realm_admin_role])
                print(f"Realm-admin role assigned to '{PERM_ADMIN_USERNAME}'.")
        else:
            print(f"Permanent admin '{PERM_ADMIN_USERNAME}' already exists.")
    except Exception as e:
        print(f"Error creating permanent admin: {e}", file=sys.stderr)
        sys.exit(1)

def delete_temporary_admin(temp_admin):
    """Delete the temporary admin account."""
    try:
        users = temp_admin.get_users({"username": TEMP_ADMIN_USERNAME})
        if users:
            temp_admin_id = temp_admin.get_user_id(TEMP_ADMIN_USERNAME)
            temp_admin.delete_user(temp_admin_id)
            print(f"Temporary admin '{TEMP_ADMIN_USERNAME}' deleted.")
        else:
            print(f"Temporary admin '{TEMP_ADMIN_USERNAME}' does not exist.")
    except Exception as e:
        print(f"Error deleting temporary admin: {e}", file=sys.stderr)
        sys.exit(1)

def configure_keycloak(permanent_admin):
    """Configure Keycloak with realms, clients, and admin user."""
    try:
        # Create Realm
        if not any(realm["realm"] == REALM_NAME for realm in permanent_admin.get_realms()):
            permanent_admin.create_realm({"realm": REALM_NAME, "enabled": True})
            print(f"Realm '{REALM_NAME}' created.")
        else:
            print(f"Realm '{REALM_NAME}' already exists.")

        # Update Realm Settings to Enable User Registration
        permanent_admin.update_realm(
            REALM_NAME,
            {
                "enabled": True,
                "registrationAllowed": True,
                "registrationEmailAsUsername": False,
                "duplicateEmailsAllowed": False,
            },
        )
        print(f"User registration enabled for realm '{REALM_NAME}'.")

        # Create Client
        permanent_admin.realm_name = REALM_NAME  # Update realm for client operations
        clients = permanent_admin.get_clients()
        if not any(client["clientId"] == CLIENT_ID for client in clients):
            permanent_admin.create_client(
                {
                    "clientId": CLIENT_ID,
                    "redirectUris": ["http://localhost:5000/*"],
                    "publicClient": True,
                    "secret": CLIENT_SECRET,
                }
            )
            print(f"Client '{CLIENT_ID}' created.")
        else:
            print(f"Client '{CLIENT_ID}' already exists.")

    except Exception as e:
        print(f"Error configuring Keycloak: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Log in as temporary admin
    temp_admin = wait_for_keycloak(TEMP_ADMIN_USERNAME, TEMP_ADMIN_PASSWORD)
    
    # Create the permanent admin user
    create_permanent_admin(temp_admin)
    
    # Log in as permanent admin
    permanent_admin = wait_for_keycloak(PERM_ADMIN_USERNAME, PERM_ADMIN_PASSWORD)
    
    # Configure Keycloak using the permanent admin
    configure_keycloak(permanent_admin)
    
    # Delete the temporary admin account
    delete_temporary_admin(permanent_admin)
    
    print("Keycloak configuration complete.")

if __name__ == "__main__":
    main()
