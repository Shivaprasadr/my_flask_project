import os
from cryptography.fernet import Fernet

def encrypt_file_in_place(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    
    with open(file_path, 'wb') as f:
        f.write(encrypted)

# Load the secret key from an environment variable
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise ValueError("SECRET_KEY environment variable not set")

key = secret_key.encode()

# List of environments
environments = ['development', 'workflow', 'production']

# Encrypt the .env files for each environment in place
for env in environments:
    file_path = f'.env.{env}'
    if os.path.exists(file_path):
        encrypt_file_in_place(file_path, key)

# Encrypt any file starting with .env or named creds.txt in the repo directory in place
repo_directory = '.'
for root, dirs, files in os.walk(repo_directory):
    for file in files:
        if file.startswith('.env') or file == 'creds.txt':
            file_path = os.path.join(root, file)
            encrypt_file_in_place(file_path, key)