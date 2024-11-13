import os
import sys
import logging
from cryptography.fernet import Fernet

# Configure logging
log_file_path = 'C:\\Temp\\decrypt_env.log'  # Specify the log file path
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def decrypt_file_in_place(file_path, key):
    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        with open(file_path, 'wb') as f:
            f.write(decrypted_data)
        
        logging.info(f"Successfully decrypted {file_path}")
    except Exception as e:
        logging.error(f"Failed to decrypt {file_path}: {e}")
        raise

# Load the secret key from an environment variable
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    logging.error("SECRET_KEY environment variable not set")
    raise ValueError("SECRET_KEY environment variable not set")

key = secret_key.encode()

# Get the file path from the command line arguments
if len(sys.argv) < 2:
    logging.error("No file path specified for decryption")
    raise ValueError("Please specify a file path to decrypt.")

file_path = sys.argv[1]

# Decrypt the specified file if it matches the required pattern
if os.path.exists(file_path) and (file_path.endswith('.env') or file_path.endswith('creds.txt')):
    logging.info(f"Found file to decrypt: {file_path}")
    try:
        decrypt_file_in_place(file_path, key)
    except Exception as e:
        logging.error(f"Error decrypting file {file_path}: {e}")
else:
    logging.warning(f"{file_path} does not exist or does not match the required pattern")
