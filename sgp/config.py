import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
#Comentario al pedo
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:sgp@localhost/sgp'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
