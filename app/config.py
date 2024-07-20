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
