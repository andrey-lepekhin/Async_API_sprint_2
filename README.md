<h1 align="center">Hi there, We are 13`th Team!
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

# WEB-sevice Online Cinema

## How to run
1. Use this command to build containers
```
make first_run
```
Wait for building.
Elasticsearch is available at the [link](http://localhost:9200/)

2. Use this commands to open bash in a container
```
make run         - rebuild containers
make postgresql         - postgresql container controls
make elasticsearch      - elasticsearch container controls
make etl                - etl container controls
make redis              - redis container controls
make shows_async        - async-container controls
```
3. Use this command to stop containers
```
make stop
```

### 

Have a nice day