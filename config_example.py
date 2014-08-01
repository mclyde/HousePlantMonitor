<<<<<<< HEAD
import os

#Pinnocio
PINOCCIO_API = 'https://api.pinocc.io/v1/'
SECURITY_TOKEN = 'YOUR PINOCC.IO API SECURITY TOKEN HERE'

#CSRF
SECRET_KEY = 'mySecretKey'

#Database
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Twitter
TWITTER_TOKEN = 'YOUR TWITTER ACCESS TOKEN'
TWITTER_TOKEN_KEY = 'YOUR TWITTER ACCESS TOKEN SECRET'
TWITTER_CON_SEC = 'YOUR TWITTER API KEY'
TWITTER_CON_SEC_KEY = 'YOUR TWITTER API SECRET'

# Email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'YOUR USERNAME'
MAIL_PASSWORD = 'YOUR PASSWORD'
ADMIN = '<YOUR USERNAME>@gmail.com'
MAIL_DEFAULT_SENDER = 'House Plant Monitor'
