import os
import math
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, assigning,db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    ITEMS_PER_PAGE = 15

    def paging(data, page):
        start = ITEMS_PER_PAGE*(page-1)
        end = (start + ITEMS_PER_PAGE)
        d = data[start:end]
        return d

    @app.route('/actors')
    def get_actors():
        page = request.args.get('page', 1, type=int)
        print(page)
        actors_data = Actor.query.order_by(Actor.id).all()
        if page > (len(actors_data)//ITEMS_PER_PAGE):
            page = (len(actors_data)//ITEMS_PER_PAGE)
            if (len(actors_data) % ITEMS_PER_PAGE) !=0:
                page += 1
        print(page)
        actors = [q.format() for q in actors_data]
        ap = paging(actors, page)
        return jsonify({
            'success': True,
            'actors': ap,
            'totalActors': len(actors)
        })

    @app.route('/movies')
    def get_movies():
        page = request.args.get('page', 1, type=int)
        movies_data = Movie.query.order_by(Movie.id).all()
        if page > (len(movies_data)//ITEMS_PER_PAGE):
            page = (len(movies_data)//ITEMS_PER_PAGE)
            if (len(movies_data) % ITEMS_PER_PAGE) !=0:
                page += 1
        movies = [q.format() for q in movies_data]
        mp = paging(movies, page)
        return jsonify({
            'success': True,
            'movies': mp,
            'totalMovies': len(movies)
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        q = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if q is None:
            abort(404)
        q.delete()
        return jsonify({

            'success': True,
            'deleted': actor_id,
            'totalActors': len(Actor.query.all())
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        q = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if q is None:
            abort(404)
        q.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id,
            'totalMovies': len(Movie.query.all())
        })

    @app.route('/actors', methods=['POST'])
    def add_actor():

        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
         
        actor = Actor(name, age, gender)
        actor.insert()
        return jsonify({
            'success': True,
        }), 200

    @app.route('/movies', methods=['POST'])
    def add_movie():
        try:
            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release_date', None)
            movie = Movie(title, release_date)
            movie.insert()
            return jsonify({
                'success': True,
            }), 200
        except:
            abort(500)

    @app.route('/movies/<int:movie_id>/edit', methods=['PATCH'])
    def update_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        # for k in body.keys():
        #    movie[k]=body[k]
        if 'title' in body.keys():
            movie.title = body['title']
        if 'release_date' in body.keys():
            movie.release_date = body['release_date']
        movie.update()
        m = []
        m.append(movie.format())
        return jsonify({
            'success': True,
            "movie": m
        }), 200

    @app.route('/actors/<int:actor_id>/edit', methods=['PATCH'])
    def update_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        body = request.get_json()
        # for k in body.keys():
        #    movie[k]=body[k]
        if 'name' in body.keys():
            actor.name = body['name']
        if 'age' in body.keys():
            actor.age = body['age']
        if 'gender' in body.keys():
            actor.gender = body['gender']
        actor.update()
        a = []
        a.append(actor.format())
        return jsonify({
            'success': True,
            'actor': a
        }), 200

    @app.route('/actors/<int:actor_id>/movies')
    def get_actor_movies(actor_id):
        page = request.args.get('page', 1, type=int)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(403)
        am = [m.format() for m in actor.movies]
        return jsonify({
            'success': True,
            'movies': paging(am, page)
        }), 200

    @app.route('/movies/<int:movie_id>/actors')
    def get_movie_actors(movie_id):
        page = request.args.get('page', 1, type=int)
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        ma = [a.format() for a in movie.actors]
        return jsonify({
            'success': True,
            'actors': paging(ma, page)
        }), 200

    @app.route('/assigning', methods=['POST'])
    def assign_actor_to_movie():
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == body['actor_id']).one_or_none()
        movie = Movie.query.filter(Movie.id == body['movie_id']).one_or_none()
        if movie is None or actor is None:
            abort(404)
        if body["method"] == "assign":
            actor.movies.append(movie)
        elif body["method"] == "unassign":
            actor.movies.remove(movie)
        db.session.commit()
        return jsonify({
            'success': True,
            'actor': body['actor_id'],
            'movie': body['movie_id']
        }), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
