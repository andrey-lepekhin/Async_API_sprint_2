# Адрес репозитория:
https://github.com/andrey-lepekhin/Async_API_sprint_2/

<h1 align="center">Hi there, We are 13`th Team!
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

# Online Cinema API
Sprint 5 in Practicum middle-python course.  
Teamwork of
* [Andrey Lepekhin](https://github.com/andrey-lepekhin)
* [Polina Vasileva](https://github.com/Polinavas95)

## How to run
```
make first_run  # will create .env files from examples and launch containers
```
Wait ~1 min for building and ETL to spin up.  
FastAPI docs are available at [http://127.0.0.1/api/openapi](http://127.0.0.1/api/openapi)

### Generate fake data
```
make generate_data
```
Will generate and add 1 mln fake persons, 100 fake genres and 400 000 fake shows. It will take up 10 minutes and ~1 GB of space.

### To stop
```
make stop
```

### More commands
```
make run                - start without rewriting env files
make postgresql         - postgresql container console
make elasticsearch      - elasticsearch container console
make etl                - etl container console
make redis              - redis container console
make shows_async        - async-container console
```


Have a nice day :)
