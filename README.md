# my_flask_project


venv\Scripts\activate
flask --app flaskr init-db
flask --app flaskr run --debug
pytest -s tests/test_factory.py -v
pytest -s tests/test_db.py -v
pytest -s tests/test_auth.py -v
mysql -h localhost -P 3306 -u flask_user -p user123


172.17.0.2

127.0.0.1
{{range .NetworkSettings.Networks}}{{.IPAddress}}{end}}
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{end}}' fdf8a3c49268

###### flask command to initiate DB
flask --app flaskr init-db

###### Db schema to rerun freshly
Error: mysql.connector.errors.DatabaseError: 3730 (HY000): Cannot drop table 'user' referenced by a foreign key constraint 'post_ibfk_1' on table 'post'.
Solution: run this in workbench "ALTER TABLE post DROP FOREIGN KEY post_ibfk_1;" and than run flask --app flaskr init-db

tests:
Not able to see the cookie for the login page 
#####################################################################

TO DO TASKS
1>test scripts or code coverage - completed
2>docker image to be created fo project
3> create a github actions for buildng
4> create a docker launch in the docker desktop
5>try to create a projct structure so that we can add any aditional files/web pages  when required to the project easily.
6>(best login type) 2 factor authentication

######################################################
mysql> SELECT user FROM mysql.user;
SELECT user, host FROM mysql.user WHERE host = '%';

CREATE USER 'flask_user'@'%' IDENTIFIED BY 'user123';

GRANT SELECT, INSERT, UPDATE, DELETE ON my_test_database.* TO 'flask_user'@'%';

GRANT ALL PRIVILEGES ON my_test_database.* TO 'flask_user'@'%';
#####################################################



