# Couriers service
Rest api service to manage delivery service via couriers and orders \
Task description can be found here: https://disk.yandex.ru/d/TbWKTZbnOST80Q?w=1 

---
## External dependencies description
1. [aiohttp](https://docs.aiohttp.org/en/stable/) - Asynchronous HTTP Client/Server for asyncio 
   and Python. In the project used as a library for asynchronous style of code
2. [sqlalchemy](https://www.sqlalchemy.org/) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper 
   that gives application developers the full power and flexibility of SQL. In the project used as orm for more comfortable work with database
3. [requests](https://docs.python-requests.org/en/master/) - Requests is a Python HTTP library, released under the Apache License 2.0. The goal of the project is to make HTTP requests simpler and more human-friendly.
   In the project used as means to test code   
4. [psycopg2](https://www.psycopg.org/docs/) - Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Database driver for async postgresql.
5. [pytest](https://docs.pytest.org/en/stable/) - The framework that makes it easy to 
   write. In the project used to test code. 
   small tests, yet scales to support complex functional testing for applications and libraries.
6. pytest-aiohttp and pytest-asyncio are plugins for pytest in order to test 
   asynchronous python code    
   
---
## Tests
To run tests you need (it is supposed you are in root dir):
```text
cd tests
pytest [optional: filename.py]
```
---

## Getting started & Deploy
1. connect to a server via ssh or another protocol
2. follow the next commands 
```text
git clone https://github.com/Nwke/rest-api-couriers-service.git
cd rest-api-couriers-service/

sudo apt update
sudo apt install python3-pip

sudo pip3 install -r requirements.txt

sudo apt install postgresql
```
then you need to setup a password for postgres user
for postgresql

```text
sudo -u postgres psql postgres
\password postgres
```
You will enter a password twice

After it you need to create a database
with name yandex_backend_school \
if you want another name for database
you need to open courier_service/db/schema.py
find there a "postgresql+asyncpg://postgres:root@localhost/yandex_backend_school"
and replace yandex_backend_school to your database name

You must do the same for the password (switch default root pass to your pass)

to create the database
```text
sudo -u postgres psql postgres
CREATE DATABASE yandex_backend_school;
```
You should see in console
"CREATE DATABASE"

```text
# if you want to connect to the database
\c yandex_backend_school
```

next step is to create tables
get into the root dir
```text
cd courier_service/db
sudo python3 schema.py
```
Now the tables should be created (structure
of tables you can find in db/schema.py)

The final step is to up the server: \
(suppose you are in root dir)
```text 
sudo python3 -m courier_serivce.api
```
The server is on
