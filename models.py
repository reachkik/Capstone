#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
import os
from sqlalchemy import Integer, Column, String, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
import json

#Comment next line to run locally
DATABASE_PATH = os.environ['DATABASE_URL']

#Uncomment below to execute locally
'''
load_dotenv()

db_user=os.getenv("DB_USERNAME")
db_password=os.getenv("DB_PASSWORD")
db_hostname=os.getenv("DB_HOSTNAME")

database_name = 'capstone'
DATABASE_PATH = 'postgresql://{}:{}@{}/{}'.format(db_user,db_password,db_hostname, database_name)
'''   

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    # db.create_all()

"""
actors table: Id, name, gender and age
"""

class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name' : self.name,
            'gender': self.gender,
            'age': self.age
            }
    
"""
movies table: title, release_date
"""
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title' : self.title,
            'release_date': self.release_date
            }