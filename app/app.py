import os

from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from time import sleep

APP = Flask(__name__)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

port = '5432'

try:
    port = os.environ['DBPORT']

except:
    pass
    

APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (
    # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
    os.environ['DBUSER'], os.environ['DBPASS'], os.environ['DBHOST'], port, os.environ['DBNAME']
)

# initialize the database connection
DB = None
while DB is None:
    try:
        DB = SQLAlchemy(APP)
    
    except Exception as e:
        print(e)
        sleep(3)

# initialize database migration management
MIGRATE = Migrate(APP, DB)

from models import *


@APP.route('/')
def view_registered_guests():
    guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)


@APP.route('/register', methods = ['GET'])
def view_registration_form():
    return render_template('guest_registration.html')


@APP.route('/register', methods = ['POST'])
def register_guest():
    name = request.form.get('name')
    email = request.form.get('email')

    guest = Guest(name, email)
    DB.session.add(guest)
    DB.session.commit()

    return render_template('guest_confirmation.html',
        name=name, email=email)
    
