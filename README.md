<h1 align="center">Hi there, We are 13`th Team!
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

# WEB-sevice Online Cinema

## How to run
1. Install Makefile plugin
2. Create and fill the file fastapi-solution/src/core/.env. You have an example .env.example
```
PROJECT_NAME=<Project name>
POSTGRES_USER=<Database user>
POSTGRES_PASSWORD=<Database password>
POSTGRES_HOST=<Database host>
POSTGRES_PORT=<Database port>
ELASTIC_HOST=<Elasticsearch host>
ELASTIC_PORT=<Elasticsearch port>
SERVER_HOST=<Server host>
SERVER_PORT=<Server port>
CACHE_EXPIRE_IN_SECONDS=<time of starting a new cycle>
```
3. Create and fill the file fastapi-solution/src/etl/postgres_to_es/.env. You have an example .env.example
```
POSTGRES_DB=<Database name>
POSTGRES_USER=<Database user>
POSTGRES_PASSWORD=<Database password>
POSTGRES_HOST=<Database host>
POSTGRES_PORT=<Database port>
ELASTIC_HOST=<Elasticsearch host+port>
SQLITE_DB_PATH=<Path to DB, movies_dmp.sql>
TIME_LOOP=<time of starting a new cycle>
BULK_SIZE=<bull of data>
```
4. Use this command to build containers
```
make run
```
Wait for building.
Elasticsearch is available at the [link](http://localhost:9200/)

4. Use this commands to open bash in a container
```
make postgresql         - postgresql container controls
make elasticsearch      - elasticsearch container controls
make etl                - etl container controls
make redis              - redis container controls
make shows_async        - async-container controls
```
5. Use this command to stop containers
```
make stop
```

### How to run tests

1. Download the [Postman](https://www.postman.com/)
2. Make a postman tests file and import it to Postman
3. Run postman tests after running the app

### 

Have a nice day