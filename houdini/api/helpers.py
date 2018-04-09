import jwt
from flask import Flask
from flask import jsonify, make_response

from flask_bcrypt import Bcrypt
from pymongo import MongoClient

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.from_object('settings')

MONGODB_URI = app.config['MONGODB_URI']
SECRET_KEY = app.config['SECRET_KEY']


def hash_password(password):
    return bcrypt.generate_password_hash(password)


def verify_password(hashed_password, plain_password):
    return bcrypt.check_password_hash(hashed_password, plain_password)


def create_user(username, password):
    user = {
        "username": username.lower(),
        "password": hash_password(password)
    }
    mongo_client = MongoClient(MONGODB_URI)
    db = mongo_client.houdini_db
    found = db.users.find_one({'username': user['username']})

    if found is not None:
        mongo_client.close()
        raise Exception('User already exists')
    else:
        db.users.insert_one(user)
        print("User account successfully created!")
        mongo_client.close()



def login_user(username, password):

    mongo_client = MongoClient(MONGODB_URI)
    db = mongo_client.houdini_db
    # user = db.users.find_one({
    #     'username': username.lower(), 
    #     'password': hash_password(password)
    # })

    user = db.users.find_one({
        'username': username.lower()
    })
    stored_password = user['password']
    verify_password(stored_password, password)

    if user is not None:
        encoded = jwt.encode({'username': username.lower()}, SECRET_KEY, algorithm='HS256')
        return {
            'username': username.title(),
            'jwt': encoded
        }
    else:
        raise Exception('invalid username / password')


def json_response(data, status):
    resp = make_response(
        jsonify(data), status
    )
    resp.mimetype = 'application/json'
    return resp     