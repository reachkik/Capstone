# Casting-Agency

## Project Description
This is the capstone project for Full-Stack Udacity Nanodegree. Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. There are three different roles in the company Casting Assistant, Casting Director, and Executive Producer. Each of them has a different set of permissions to view, add, update and delete movies and actors in the databse.

Though the front-end is very simple, most of the work are done in the back-end. I wrote Restful APIs, built a database using SQLAlchemey, secured the application using Auth0, tested the application using unit tests and via Postman, and finally deploy the application to Heroku.

## Project Result
Render: TBD

Localhost: http://127.0.0.1:5000/

## Tech Stack
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Auth0** for authentication management
* **Render Cloud** for deployment


## Getting Started

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```
  This will install all of the required packages we selected within the `requirements.txt` file.

3. run ```source setup.sh``` to set the user jwts, auth0 credentials

3. Database Setup

  ```
  psql capstone < capstone.sql
  ```

4. Run the development server:
  ```
  $ export FLASK_APP=app
  $ export FLASK_ENV=development # enables debug mode
  flask run
  ```

## Testing
To run the tests, run 
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone_test.sql
python -m unittest test_app.py
```

## API Reference

### Endpoints

#### GET '/movies'
- General:
    - Return all movies in the database
    - Role Authorized: Casting Assistant, Casting Director, Executive Producer
- Example: ```curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/movies```
```
{
    "movies": [
        {
            "id": 2,
            "release_date": "Fri, 07 Feb 2020 00:00:00 GMT",
            "title": "Birds of Prey"
        },
        {
            "id": 3,
            "release_date": "Sun, 10 Mar 2013 00:00:00 GMT",
            "title": "The Great Gatsby"
        },
        {
            "id": 4,
            "release_date": "Fri, 20 May 2011 00:00:00 GMT",
            "title": "Pirates of the Caribbean: On Stranger Tides"
        },
        {
            "id": 6,
            "release_date": "Wed, 24 Jul 2019 00:00:00 GMT",
            "title": "once upon a time in hollywood"
        }
    ],
    "success": true
}
```
#### GET '/actors'
- General:
    - Return all actors in the database
    - Role Authorized: Casting Assistant, Casting Director, Executive Producer
- Example: ```curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/actors```
```
{
    "actors": [
        {
            "age": 30,
            "gender": "F",
            "id": 2,
            "movie_id": 2,
            "name": "Margot Robbie"
        },
        {
            "age": 45,
            "gender": "M",
            "id": 3,
            "movie_id": 3,
            "name": "Leonardo DiCaprio"
        },
        {
            "age": 35,
            "gender": "F",
            "id": 4,
            "movie_id": 3,
            "name": "Carey Mulligan"
        },
        {
            "age": 57,
            "gender": "M",
            "id": 5,
            "movie_id": 4,
            "name": "Johnny Depp"
        }
    ],
    "success": true
}
```

#### POST '/movies'
- General:
    - Add a new movie. The new movie must have all four information. 
    - Role Authorized: Executive Producer
- Example: ```curl -X POST - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"title": "Call Me by Your Name", "release_date": "2017-10-20"}' http://127.0.0.1:5000/movies```
```
{
    "movie": {
        "id": 16,
        "release_date": "Fri, 20 Oct 2017 00:00:00 GMT",
        "title": "Call Me by Your Name"
    },
    "success": true
}
```

#### POST '/actors'
- General:
    - Add a new actor. The new movie must have all four information. 
    - Role Authorized: Casting Director, Executive Producer
- Example: ```curl -X POST - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"name": "Timothée Chalamet", "age": 24, "gender": "M", "movie_id": 6}' http://127.0.0.1:5000/actors```

```
{
    "actor": {
        "age": 24,
        "gender": "M",
        "id": 11,
        "movie_id": 6,
        "name": "Timothée Chalamet"
    },
    "success": true
}
```

#### PATCH '/movies/<int:id>'
- General:
    - Update some information of a movie based on a payload.
    - Roles authorized : Casting Director, Executive Producer.
- Example: ```curl http://127.0.0.1:5000/movies/3 -X PATCH -H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{ "title": "", "release_date": "2020-11-01" }'```
```
{
  "movie": {
    "id": 3,
    "release_date": "Sun, 01 NOV 2020 00:00:00 GMT",
    "title": "The Great Gatsby"
  },
  "success": true
}
```

#### PATCH '/actors/<int:id>'
- General:
    - Update some information of an actor based on a payload.
    - Roles authorized : Casting Director, Executive Producer
- Example: ```curl -X PATCH - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"name": "", "age": 88, "": "M", "movie_id": }' http://127.0.0.1:5000/actors/3```
```
{
  "actor": {"age": 88,
    "gender": "M",
    "id": 3,
    "movie_id": 3,
    "name": "Leonardo DiCaprio"
  }, 
  "success": true
}
```

#### DELETE '/movis/<int:id>'
- General:
    - Deletes a movie by id form the url parameter.
    - Roles authorized : Executive Producer.
- Example: ```curl -H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -X DELETE http://127.0.0.1:5000/movies/2```
```
{
  "success": true, 
  "delete": 2
}
```

#### DELETE '/actors/<int:id>'
- General:
    - Deletes a movie by id form the url parameter.
    - Roles authorized : Casting Director, Executive Producer.
- Example: ```curl -H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -X DELETE http://127.0.0.1:5000/actors/2```
```
{
    "success": "True",
    "deleted": 2
}
```

### Error Handling
Errors are returned in the following json format:
```
{
    'success': False,
    'error': 404,
    'message': 'resource not found'
}
```
The API returns 6 types of errors:
- 400: bad request
- 401: Token Expired
- 403: Unauthorized
- 404: resource not found
- 405: method not allowed
- 422: unprocessable
- AuthError
