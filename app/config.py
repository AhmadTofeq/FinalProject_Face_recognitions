from dotenv import load_dotenv
import os

# Get the base directory of the current file
basedir = os.path.abspath(os.path.dirname(__file__))

# Load the environment variables from the .env file located two directories above
load_dotenv(os.path.join(basedir, '..', '..', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:@localhost/soran_face'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security enhancements
    SESSION_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent client-side scripts from accessing the session cookie
    SESSION_COOKIE_SAMESITE = 'Lax'  # Mitigate CSRF attacks

    # CSRF protection (requires Flask-WTF)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or 'another-secure-random-string'
