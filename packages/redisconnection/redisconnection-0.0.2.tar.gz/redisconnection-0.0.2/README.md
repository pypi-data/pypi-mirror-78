SQL Adapter for Connection and Query Handling


## System Dependency

* Python 3.6.9
* pipenv


## Development Setup

1) Clone the repo 
2) cd redisconnection
3) pipenv install
4) pipenv shell

Start developing

# Package sqlconnection

python version must be 3.6.9
### Build

python setup.py build

### Distribute
python setup.py sdist

### Upload 
twine upload dist/*

### Python Dependency
* redis==3.4.1
* python-dotenv==0.12.0



### Use 
It wil load environment variable automatically, so all you need to do is make sure these environment variables are present. 
It will also autoload .env ( example .env.dist , rename it to .env) file before running, so you can also put these variables in your .env file. 

Needed Environment variables are 

```
# Application
APP_NAME=redisconnection
LOG_LEVEL=DEBUG
ENVIRONMENT=dev
REGION=mex

# REDIS
REDIS_USER=redis
REDIS_PASSWORD=redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6432
REDIS_DATABASE=0


```

```
from redisconnection import redis_connection
rc = redis_connection.RedisConnection()
conn = rc.connection

```




