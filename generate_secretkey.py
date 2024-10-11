import os
from cryptography.fernet import Fernet
import subprocess

# Check if the SECRET_KEY environment variable already exists
existing_key = os.getenv('SECRET_KEY')

if existing_key:
    print("SECRET_KEY environment variable already exists. Renewing the key...")

# Generate a new key
key = Fernet.generate_key()

# Print the new key
print(f"Generated new key: {key.decode()}")

# Set the new key as a system environment variable
key_str = key.decode()
subprocess.run(["setx", "SECRET_KEY", key_str], shell=True)

print("restart system to see SECRET_KEY has been renewed and set as a system environment variable.")

# Set the ENVIRONMENT variable to development
subprocess.run(["setx", "ENVIRONMENT", "development"], shell=True)

print("restart the system to see ENVIRONMENT has been set to development as a system environment variable. ")
