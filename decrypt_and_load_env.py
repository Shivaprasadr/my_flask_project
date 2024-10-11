import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        encrypted = f.read()
    
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    
    with open(output_file, 'wb') as f:
        f.write(decrypted)

# Load the secret key
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise ValueError("SECRET_KEY environment variable not set")
key = secret_key.encode()

# Decrypt all .env files and creds.txt files
repo_directory = '.'
for root, dirs, files in os.walk(repo_directory):
    for file in files:
        if file.startswith('.env') or file == 'creds.txt':
            input_file = os.path.join(root, file)
            output_file = os.path.join(root, file)
            decrypt_file(input_file, output_file, key)

# Commented out environment-based decryption
# Determine the environment
# environment = os.getenv('ENVIRONMENT', 'development')

# Decrypt the appropriate .env file
# if environment == 'production':
#     decrypt_file('.env.production.enc', '.env', key)
# else:
#     decrypt_file('.env.development.enc', '.env', key)

# Load the .env file
load_dotenv('.env')