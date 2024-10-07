from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
HASHSALT = os.environ.get('HASHSALT')

S3KID = os.environ.get('S3KID')
S3KEY = os.environ.get('S3KEY')
S3BUCKET = os.environ.get('S3BUCKET')

COOKIE_KEY = '_at'
