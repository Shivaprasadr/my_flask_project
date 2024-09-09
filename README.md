# my_flask_project


venv\Scripts\activate
(this db initialize should be done in new db creation if this is being run after the project was running good, Remove the query comment in sql file -- ALTER TABLE post DROP FOREIGN KEY post_ibfk_1;)
flask --app flaskr init-db 
flask --app flaskr run --debug
pytest -s tests/test_factory.py -v
pytest -s tests/test_db.py -v
pytest -s tests/test_auth.py -v
mysql -h localhost -P 3306 -u flask_user -p user123

### starting /stopping app from docker compose
docker-compose up
sto the dockare compose and delete containers = docker-compose down -v 
run in backgorund command =  docker-compose up -d 
 
### docker issues 
172.17.0.2

127.0.0.1
{{range .NetworkSettings.Networks}}{{.IPAddress}}{end}}
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{end}}' fdf8a3c49268
#### ISSUES ####
###### flask command to initiate DB
flask --app flaskr init-db

###### Db schema to rerun freshly
Error: mysql.connector.errors.DatabaseError: 3730 (HY000): Cannot drop table 'user' referenced by a foreign key constraint 'post_ibfk_1' on table 'post'.
Solution: run this in workbench "ALTER TABLE post DROP FOREIGN KEY post_ibfk_1;" and than run flask --app flaskr init-db

##### sql error when starting the app in browser.
mysql.connector.errors.ProgrammingError: 1146 (42S02): Table 'my_database.post' doesn't exist

### OS type of the app
# cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"




tests:
Not able to see the cookie for the login page 
#####################################################################

TO DO TASKS
0> remove flask session -
 completed
1>test scripts or code coverage - completed
2>docker image to be created for project - completed
3> create a github actions for buildng - completed
4> create a docker launch in the docker desktop - completed
1> need to a best login method to the project.
(That type of login is called Social Login or OAuth (Open Authorization) Login.
flask-google-login: Handles Google login specifically.
flask-microsoft: Integrates Microsoft login for your Flask app.
)
2>try to create a projct structure so that we can add any aditional files/web pages  when required to the project easily.
3> remove the pwds and clean code.
4> flash messsage are not working for register page /login in borwsers (https://stackoverflow.com/questions/30497236/python-flask-flash-not-working-correctly/30497806) (https://flask.palletsprojects.com/en/2.3.x/patterns/flashing/)(https://stackoverflow.com/questions/48847430/flash-messaging-not-working-in-flask)
5> when usesrs increase we need to add the session cache to redis (from cachelib.redis import RedisCache)currently using from cachelib.file import FileSystemCache

Testcases to do tasks
1>

######################################################
for running the test coverage we need to create the database as its not created when the db docker was started
login to the db with root access 

CREATE DATABASE my_test_database;

SELECT user FROM mysql.user;
SELECT user, host FROM mysql.user WHERE host = '%';

CREATE USER 'flask_user'@'%' IDENTIFIED BY 'user123';

GRANT SELECT, INSERT, UPDATE, DELETE ON my_test_database.* TO 'flask_user'@'%';

GRANT ALL PRIVILEGES ON my_test_database.* TO 'flask_user'@'%';
#####################################################
### Docker #####

```markdown
## Clean Up Docker Resources

Docker Compose typically cleans up these resources, but you can manually remove any lingering ones. 

### Remove Unused Volumes

```sh
docker volume prune -f
```

### Remove Unused Networks

```sh
docker network prune -f
```

### Remove Unused Images

```sh
docker image prune -f
```

### Confirm Removal

You can list Docker networks, volumes, and images to confirm they have been removed:

```sh
docker network ls
docker volume ls
docker images
docker-compose up
docker-compose down -v 
docker-compose pull && docker-compose up

```
```

##########
