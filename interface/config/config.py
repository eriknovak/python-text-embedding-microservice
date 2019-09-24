# Configuration script
# Retrieves the hidden variables from the .env
# file and creates the configuration objects -
# one for each environment.

from dotenv import load_dotenv
load_dotenv()

import os
import ast

class Config(object):
    DEBUG = False
    TESTING = False
    CORS = {
        'origins': os.getenv('CORS_ORIGINS').split(',') if os.getenv('CORS_ORIGINS') else None
    }


class ProductionConfig(Config):
    """Production configuration"""
    ENV='production'
    SECRET_KEY=os.getenv('PROD_SECRET_KEY'),


class DevelopmentConfig(Config):
    """Development configuration"""
    ENV='development'
    DEBUG = True
    SECRET_KEY=os.getenv('DEV_SECRET_KEY')
    PROXY=ast.literal_eval(os.getenv('DEV_PROXY')) if os.getenv('DEV_PROXY') else None


class TestingConfig(Config):
    """Testing configuration"""
    ENV='testing'
    TESTING = True
    SECRET_KEY=os.getenv('TEST_SECRET_KEY')
    PROXY=ast.literal_eval(os.getenv('TEST_PROXY')) if os.getenv('TEST_PROXY') else None
