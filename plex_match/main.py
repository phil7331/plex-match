from flask import Flask, render_template, jsonify, request, redirect, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv
from plexapi.server import PlexServer

from plex_match.repository import init_admin_user, find_user_in_db

load_dotenv()
app = Flask(__name__)

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'ea32dbef1a435a4542da8a2994619bda1b4a01cc17e6dbfa4ef0798f6976fbac'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Store JWT in cookies
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF protection for simplicity
jwt = JWTManager(app)

users = {"asd": {"password": "asd"}}


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return redirect('/login', code=302)


@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    return redirect('/login', code=302)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = find_user_in_db(username=username, password=password)

        # Create JWT and store it in a cookie
        access_token = create_access_token(identity=user["username"])
        resp = make_response(redirect('/'))
        resp.set_cookie('access_token_cookie', access_token)

        return resp

    return render_template('login.html')


@app.route('/')
@jwt_required()  # JWT will be taken from the cookie automatically
def match():
    token = os.getenv("TOKEN")
    url = os.getenv("URL")
    plex = PlexServer(url, token)
    movies = plex.library.section("Movies").search(unwatched=True)

    movies_posters = []
    for movie in movies:
        movie_title = movie.title
        movies_posters.append({"title": movie_title, "poster_url": movie.posterUrl})
    current_user = get_jwt_identity()
    return render_template('index.html', context=movies_posters)


if __name__ == '__main__':
    if False:
        init_admin_user()
    app.run(debug=True)
