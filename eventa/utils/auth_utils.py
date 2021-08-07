import os
from dotenv import load_dotenv
from itsdangerous import URLSafeSerializer
load_dotenv()

SECRET_KEY = os.environ.get('SECRET', os.urandom(16).hex())
s_auth = URLSafeSerializer(SECRET_KEY, salt="auth")
