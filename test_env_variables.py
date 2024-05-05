import os

# Check if environment variables are set
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = os.getenv('MYSQL_PORT')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_db = os.getenv('MYSQL_DB')

mysql_test_host = os.getenv('MYSQL_TEST_HOST')
mysql_test_port = os.getenv('MYSQL_TEST_PORT')
mysql_test_user = os.getenv('MYSQL_TEST_USER')
mysql_test_password = os.getenv('MYSQL_TEST_PASSWORD')
mysql_test_db = os.getenv('MYSQL_TEST_DB')

print("Development Configuration:")
print(f"MYSQL_HOST: {mysql_host}")
print(f"MYSQL_PORT: {mysql_port}")
print(f"MYSQL_USER: {mysql_user}")
print(f"MYSQL_PASSWORD: {mysql_password}")
print(f"MYSQL_DB: {mysql_db}")

print("\nTesting Configuration:")
print(f"MYSQL_TEST_HOST: {mysql_test_host}")
print(f"MYSQL_TEST_PORT: {mysql_test_port}")
print(f"MYSQL_TEST_USER: {mysql_test_user}")
print(f"MYSQL_TEST_PASSWORD: {mysql_test_password}")
print(f"MYSQL_TEST_DB: {mysql_test_db}")
