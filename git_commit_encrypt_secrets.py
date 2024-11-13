import os
import sys
import logging
from cryptography.fernet import Fernet

# Configure logging to log to both console and a file
log_file_path = 'C:\\Temp\\encrypt_env.log'  # Specify the log file path

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler(log_file_path, mode='w')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

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

# Get the file path from the command line arguments
if len(sys.argv) < 2:
    logging.error("No file path specified for encryption")
    raise ValueError("Please specify a file path to encrypt.")

file_path = sys.argv[1]

# Encrypt the specified file if it exists and matches the pattern
if os.path.exists(file_path) and (file_path.endswith('.env') or file_path.endswith('creds.txt')):
    logging.info(f"Found file to encrypt: {file_path}")
    try:
        encrypt_file_in_place(file_path, key)
    except Exception as e:
        logging.error(f"Error encrypting file {file_path}: {e}")
else:
    logging.warning(f"{file_path} does not exist or does not match the required pattern")
