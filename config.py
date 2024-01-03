import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DATABASE_URI','sqlite:///grocery.db')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    CELERY_IMPORTS = ('backend.applicaiton.task')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY= 'thisissecter'
    SECURITY_PASSWORD_SALT="daykdhudtashkyfuh"
    SECURITY_TOKEN_AUTHENTICATION_KEY='auth_token'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
