import os

from dotenv import load_dotenv
from flask import Flask, jsonify, session
from flask_cors import CORS
from werkzeug.security import check_password_hash
from utils import s_auth
from routes import auth_route
from flask_httpauth import HTTPBasicAuth

load_dotenv()
app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()


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

if __name__ == "__main__":
    app.run(port=5050, debug=True)
