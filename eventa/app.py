import os

from dotenv import load_dotenv
from flask import Flask, jsonify, session
from flask_cors import CORS
from werkzeug.security import check_password_hash

from utils import s_auth
from routes import auth_route, events_route, users_route
from flask_httpauth import HTTPBasicAuth



def create_app():
    load_dotenv()
    UPLOAD_FOLDER = os.environ.get('IMAGES_UPLOAD', '/images/')
    ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    app = Flask(__name__, static_url_path='/static')
    cors = CORS(app, supports_credentials=True, resources={"*":{"origins":"http://localhost:3000"}})

    auth = HTTPBasicAuth()

    app.config["IMAGES_UPLOAD"] = UPLOAD_FOLDER
    app.config['CORS_HEADERS'] = 'content-Type'
    app.secret_key = os.environ.get('SECRET', os.urandom(16).hex())

    @auth.verify_password
    def verify_password(user_id, password):
        if s_auth.loads(session.get('X-Authenticated')) == user_id and \
                check_password_hash(os.environ['PASS_HASH'], password):
            return True
        session['X-Authenticated'] = None
        session.modified = True
        return None

    @auth.error_handler
    def unauthorized():
        return jsonify(error='unauthorized access'), 403

    app.register_blueprint(auth_route, url_prefix="/auth")
    app.register_blueprint(events_route, url_prefix="/events")
    app.register_blueprint(users_route, url_prefix="/users")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(port=5050, debug=True)
