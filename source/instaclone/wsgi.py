import os

from instaclone.application import create_application

configuration = os.environ['APPLICATION_CONFIG_FILE']

application = create_application(configuration=configuration)
