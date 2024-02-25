import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Actors, Movies
from auth import AuthError, requires_auth
import json

def create_app(db_uri="", test_config=None):
    # create and configure the app

    app = Flask(__name__)
    if db_uri:
        setup_db(app, db_uri)
    else:        
        setup_db(app)
    CORS(app)

    '''
    CORS Headers
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    
    '''
    endpoint GET /actors
        it will get list of all actors
        requires 'get:actors' permission
    returns status code 200 and json {"success": True, "actors": actors, 
    total_actors:total_actors where total_actors is the count}
        or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['GET'])
    #@requires_auth(permission='get:actors')
    def get_actors(payload):
        try:
            actors = Actors.query.order_by(Actors.id).all()
            actors_formatted=[a.format() for a in actors]
            return jsonify(
                {
                    'success': True,
                    'actors': actors_formatted,
                    'total_actors': len(actors)                    
                }
            ), 200
        except:
            abort(422)

    '''
    Endpoint GET /movies
        it will get list of all movies
        requires 'get:movies' permission
    returns status code 200 and json {"success": True, "movies": movies, 
    total_movies:total_movies where total_movies is the count}
        or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.order_by(Movies.id).all()
            movies_formatted=[m.format() for m in movies]
            return jsonify(
                {
                    'success': True,
                    'movies': movies_formatted,
                    'total_movies': len(movies)                    
                }
            ), 200
        except:
            abort(422) 

    '''
    Endpoint POST /actors
        it creates a new row in the actors table
        it require the 'post:actors' permission        
    returns status code 200 and json {"success": True, 
    "actors_id_added": new_actor.id}
    or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def post_actors(payload):
        body = request.get_json()
        if not ('name' in body and 'gender' in body and 'age' in body):
            abort(422)
        try:
            new_actor = Actors(name=body.get('name'), gender=body.get('gender'),age=body.get('age'))
            new_actor.insert()

            return jsonify(
                {
                    "success": True,
                    "actor_id_added": new_actor.id
                }
            ), 200

        except Exception:
            abort(422)

    '''
    Endpoint POST /movies
        Creates a new row in the Movies table
        Require the 'post:movies' permission
        returns status code 200 and json {"success": True,
        "movie_id_added": new_movie.id} 
        or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_movies(payload):
        body = request.get_json()
        if not ('title' in body and 'release_date' in body):
            abort(422)
        try:
            new_movie = Movies(title=body.get('title'), release_date=body.get('release_date'))
            new_movie.insert()

            return jsonify(
                {
                    "success": True,
                    "movie_id_added": new_movie.id
                }
            ), 200

        except Exception:
            abort(422)

    '''
    Endpoint PATCH /actors/<id>
        where <id> is the existing actors id
        responds with a 404 error if <id> is not found
        updates the corresponding row for <id>
        requires the 'patch:actors' permission
        returns status code 200 and json {"success": True,
            "actor_id_updated": actor.id} 
        or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def patch_actor(payload,id):
        body = request.get_json()
        actor = Actors.query.filter(Actors.id == id).one_or_none()

        if not actor:
            abort(404)

        if body is None:
            abort(422)

        try:
            name = body.get('name')
            if name:
                actor.name = name

            gender = body.get('gender')
            if gender:
                actor.gender = gender

            age = body.get('age')
            if age:
                actor.age = age

            actor.update()

            return jsonify(
                {
                    "success": True,
                    "actor_id_updated": actor.id
                }
            ), 200

        except Exception:
            abort(422)

    '''
    Endpoint PATCH /movies/<id>
        where <id> is the existing movies id
        responds with a 404 error if <id> is not found
        updates the corresponding row for <id>
        requires the 'patch:movies' permission
        returns status code 200 and json {"success": True,
            "movies_id_updated": movie.id} 
        or appropriate status code indicating reason for failure
    '''

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def patch_movie(payload, id):
        body = request.get_json()
        movie = Movies.query.filter(Movies.id == id).one_or_none()

        if not movie:
            abort(404)

        if body is None:
            abort(422)

        try:
            title = body.get('title')
            if title:
                movie.title = title

            release_date = body.get('release_date')
            if release_date:
                movie.release_date = release_date

            movie.update()

            return jsonify(
                {
                    "success": True,
                    "movie_id_updated": movie.id
                }
            ), 200

        except Exception:
            abort(422)

    '''
    Endpoint DELETE /actors/<id>
        where <id> is the existing actors id
        responds with a 404 error if <id> is not found
        deletes the corresponding row for <id>
        requires the 'delete:actors' permission
        returns status code 200 and json {"success": True, "delete": id} 
        or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, id):
        actor = Actors.query.filter(Actors.id == id).one_or_none()

        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": actor.id
                }
            )

        except Exception:
            abort(422)

    '''
    Endpoint DELETE /movies/<id>
        where <id> is the existing movies id
        responds with a 404 error if <id> is not found
        deletes the corresponding row for <id>
        requires the 'delete:movies' permission
        returns status code 200 and json {"success": True,
            "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movies(payload, id):
        movie = Movies.query.filter(Movies.id == id).one_or_none()

        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": movie.id
                }
            ), 200

        except Exception:
            abort(422)

  # Error Handling for 401, 403, 404, 405, 422, 400 and AuthError
    @app.errorhandler(401)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 401,
                "message": "Token Expired"
            }
        ), 401
    
    @app.errorhandler(403)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 403,
                "message": "Unauthorized"
            }
        ), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
        ), 404
    
    @app.errorhandler(405)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }
        ), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable entity"
            }
        ), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request"
            }
        ), 400

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(
            {
                "success": False,
                "error": e.status_code,
                "message": e.error
            }
        ), e.status_code

    return app
app = create_app()
if __name__ == '__main__':
    #    app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)
