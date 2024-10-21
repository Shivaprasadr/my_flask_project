import os
import logging
from cryptography.fernet import Fernet

# Configure logging to overwrite the log file for each run
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='encrypt_env.log', filemode='w')

def encrypt_file_in_place(file_path, key):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        
        with open(file_path, 'wb') as f:
            f.write(encrypted)
        
        logging.info(f"Successfully encrypted {file_path}")
    except Exception as e:
        logging.error(f"Failed to encrypt {file_path}: {e}")
        raise

# Load the secret key from an environment variable
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    logging.error("SECRET_KEY environment variable not set")
    raise ValueError("SECRET_KEY environment variable not set")

key = secret_key.encode()

# List of environments
environments = ['development', 'workflow', 'production']

# Encrypt the .env files for each environment in place
# Commented out as per your request
# for env in environments:
#     file_path = f'.env.{env}'
#     if os.path.exists(file_path):
#         encrypt_file_in_place(file_path, key)
#     else:
#         logging.warning(f"{file_path} does not exist")

# Encrypt any file starting with .env or named creds.txt in the repo directory in place
repo_directory = '.'
for root, dirs, files in os.walk(repo_directory):
    for file in files:
        file_path = os.path.join(root, file)
        if file.startswith('.env') or file == 'creds.txt':
            logging.info(f"Found file to encrypt: {file_path}")
            try:
                encrypt_file_in_place(file_path, key)
            except Exception as e:
                logging.error(f"Error encrypting file {file_path}: {e}")
        else:
            logging.debug(f"Skipping file: {file_path}")