# This is my Milky Galaxy, a sample news application that uses different technologies. 
This is a Django-based web service that provides several RESTFul APIs for creating, deleting and getting channels and articles as well as doing registration and login. 

## Installation
First, `cd news/`, then:
### With Docker
Make sure that you have Docker in your machine. Now, run the following commands:
```
docker-compose build
docker-compose up -d
```
### Without Docker
Make sure that you have Python, Pip and Redis installed in your machine. 
Then install the requirements:
```
pip install -r requirements.txt
```
Then, run the celery workers at the background:
```
celery -A news worker --loglevel=debug --concurrency=4 --detach
```
And finally run the project:
```
python manage.py runserver
```

## Running the tests
With Docker:
```
docker-compose run web pytest
```

or without Docker:
```
pytest
```


## Admin panel
First, create a superuser:

### With Docker
```
 docker-compose run web python manage.py createsuperuser
 ```
### Without Docker
```
python manage.py createsuperuser
```

Then, go to admin panel via: 127.0.0.1:8000/admin 


## APIs list with Swagger
You can have the access to Swagger on the following address:
```
http://127.0.0.1:8000/swagger/
```

## How to use?
In order to add a new channel or article, first you need to create a new user, and then add the access token to the header of the related request. 

**For more details about APIs input and output, please check the Swagger page mentioned above.

### Example
#### 1- Add a new user:
`/api/account/register/`

#### 2- Get the access token:
You must provid `username` and `password` in the body of the post request.

`http://127.0.0.1:8001/api/token/`

#### 3- Add a new article
You must add a param in the header as `Authorization` with the value of `Bearer access_token`

`http://127.0.0.1:8001/api/articles/`

**For more details about APIs input and output, please check the Swagger page mentioned above.
