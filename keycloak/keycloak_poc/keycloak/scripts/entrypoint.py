import subprocess
import sys

def run_script(script_name):
    try:
        print(f"Starting {script_name}...")
        result = subprocess.run(["python", script_name], check=True)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {script_name} failed with exit code {e.returncode}.")
        sys.exit(e.returncode)

def main():
    run_script("keycloak_config.py")
    run_script("keycloak_clients_config.py")
    print("Both scripts executed successfully.")

if __name__ == "__main__":
    main()
