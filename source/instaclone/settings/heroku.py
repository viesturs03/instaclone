import os

from instaclone.settings.core import *

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
