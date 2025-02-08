from keycloak import KeycloakAdmin
import time
import sys

# Keycloak server details
KEYCLOAK_URL = "http://keycloak:8080/"
TEMP_ADMIN_USERNAME = "admin"
TEMP_ADMIN_PASSWORD = "admin_password"
PERM_ADMIN_USERNAME = "permanent_admin"
PERM_ADMIN_PASSWORD = "strong_permanent_password"
REALM_NAME = "pocrealm"

def wait_for_keycloak(username, password, realm="master"):
    """Wait until Keycloak is reachable and return an authenticated KeycloakAdmin instance."""
    for _ in range(20):  # Retry 20 times
        try:
            admin = KeycloakAdmin(
                server_url=KEYCLOAK_URL,
                username=username,
                password=password,
                realm_name=realm,
                verify=True,
            )
            print(f"Keycloak is ready! Logged in as '{username}' on realm '{realm}'.")
            return admin
        except Exception as e:
            print(f"Waiting for Keycloak to become available... Error: {e}")
            time.sleep(10)
    print("Keycloak did not become ready in time.", file=sys.stderr)
    sys.exit(1)

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
def create_user(userinstance, username, password, realmname):
    """Create a user on mentioned realm"""
    try:
        users = userinstance.get_users({"username": username})
        if not users:
            userinstance.create_user(
                {
                    "username": username,
                    "enabled": True,
                    "credentials": [
                        {"type": "password", "value": password, "temporary": False}
                    ],
                }
            )
            print(f"user '{username}' created on realm '{realmname}'.")
        else:
            print(f"user '{username}' already exists.")

    except Exception as e:
        print(f"Error creating permanent admin: {e}", file=sys.stderr)
        sys.exit(1)

def assign_user_role(userinstance, username, userrole):
    """Assign the 'realm-admin' role to the permanent admin in the new realm."""
    try:
            # Get the user ID of the permanent admin
        user_id = userinstance.get_user_id(username)
        
        # Assign the 'admin' role for the master realm
        master_realm_roles = userinstance.get_realm_roles()
        master_realm_admin_role = next(
            (role for role in master_realm_roles if role["name"] == userrole), None
        )
        if master_realm_admin_role:
            userinstance.assign_realm_roles(user_id, [master_realm_admin_role])
            print(f"Master realm-admin role assigned to '{username}'.")

    
    except Exception as e:
        print(f"Error assigning user role: {e}", file=sys.stderr)
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

        # Wait for the realm to be fully available
        time.sleep(5)  

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

    except Exception as e:
        print(f"Error configuring Keycloak: {e}", file=sys.stderr)
        sys.exit(1)

def ensure_realm_management_client(instance):
    """Ensure the 'realm-management' client exists in the specific logged in realm."""
    try:
        #instance.realm_name = REALM_NAME
        clients = instance.get_clients()
        realm_mgmt_client = next(
            (client for client in clients if client["clientId"] == "realm-management"), None
        )

        if not realm_mgmt_client:
            # Realm-management client does not exist, create it
            instance.create_client(
                {
                    "clientId": "realm-management",
                    "enabled": True,
                    "publicClient": False,
                    "protocol": "openid-connect",
                    "serviceAccountsEnabled": True,
                    "directAccessGrantsEnabled": True,
                }
            )
            print(f"'realm-management' client created in '{REALM_NAME}'.")
        else:
            print(f"'realm-management' client already exists in '{REALM_NAME}'.")

    except Exception as e:
        print(f"Error ensuring 'realm-management' client: {e}", file=sys.stderr)
        sys.exit(1)

def ensure_realm_management_roles(realm_admin):
    """Ensure required roles exist in the realm-management client."""
    try:
        clients = realm_admin.get_clients()
        realm_mgmt_client = next(
            (client for client in clients if client["clientId"] == "realm-management"), None
        )
        if not realm_mgmt_client:
            print(f"Error: 'realm-management' client not found in '{REALM_NAME}'!", file=sys.stderr)
            sys.exit(1)

        realm_mgmt_client_id = realm_mgmt_client["id"]
        realm_roles = realm_admin.get_client_roles(realm_mgmt_client_id)

        required_roles = ["realm-admin", "manage-users", "manage-clients"]
        existing_roles = [role["name"] for role in realm_roles]

        for role_name in required_roles:
            if role_name not in existing_roles:
                realm_admin.create_client_role(realm_mgmt_client_id, {"name": role_name})
                print(f"Created role '{role_name}' in 'realm-management' client of '{REALM_NAME}'.")

    except Exception as e:
        print(f"Error ensuring realm management roles: {e}", file=sys.stderr)
        sys.exit(1)
def main():
    # Step 1: Log in as temporary admin
    temp_admin = wait_for_keycloak(TEMP_ADMIN_USERNAME, TEMP_ADMIN_PASSWORD)

    # Step 2: Create the permanent admin user (Master realm admin)
    create_user(temp_admin, PERM_ADMIN_USERNAME, PERM_ADMIN_PASSWORD, "master")

    # Step 3: assign user role to the permanent admin in the master realm
    assign_user_role(temp_admin, PERM_ADMIN_USERNAME, "admin")

    # Step 4: Log in as permanent admin
    permanent_admin = login_to_keycloak_realm(PERM_ADMIN_USERNAME, PERM_ADMIN_PASSWORD,"pocrealm","master")

    # Step 5: Configure Keycloak (create the realm, update settings)
    configure_keycloak(permanent_admin)

    # Step 6: Create pocrealm admin user in pocrealm and assign roles its not required but simple tested and it worked.
    create_user(permanent_admin, "pocrealm_adminuser", "pocrealm_admin_password", "of no use because its only used in print")

    # Step 7: Ensure realm-management client exists
    ensure_realm_management_client(permanent_admin)

    # Step 8: Delete the temporary admin account
    delete_temporary_admin(temp_admin)

    print("Keycloak configuration complete.")

if __name__ == "__main__":
    main()
