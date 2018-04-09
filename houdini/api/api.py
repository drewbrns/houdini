import os
from flask import Flask, render_template, jsonify, abort
from flask import make_response, request, session
from flask import g, redirect, url_for
from pymongo import MongoClient
from bson import json_util

from middleware import authenticate, login_required
from helpers import login_user


app = Flask(__name__)
app.config.from_object('settings')

MONGODB_URI = app.config['MONGODB_URI']
SECRET_KEY = app.config['API_KEY']

### Routes

@app.before_request
def before_request():
    g.user = session.get('username', None)


# Index Page
@app.route('/')
# @login_required   # Uncomment this when you implement login action
def home():
    return render_template('home.html')    


# Login on GET Request 
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        
        try:
            user = login_user(username, password)
            g.user = user['username']
            session['username'] = user['username']
            return redirect(url_for('home'))
        except Exception as e:
            return render_template(
                'login.html', result={
                    'error': e, 
                    'username': username
                    }
                )
    else:      
        return render_template('login.html')
         

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('login'))


# API
@app.route('/api/v1/data', methods=['GET'])
@authenticate
def get_data():
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))

        mongo_client = MongoClient(MONGODB_URI)
        db = mongo_client.houdini_db

        records = db.data_lake.find({}).skip(skip).limit(limit)
        records = list(records)
        
        mongo_client.close()

        resp = make_response(
            json_util.dumps(records), 200
        )
        resp.mimetype = 'application/json'
        return resp
    except Exception as e:
        return make_response(
            jsonify({'error': e}), 400
        )

@app.route('/api/v1/stats', methods=['GET'])
@authenticate
def get_stats():
    try:
        mongo_client = MongoClient(MONGODB_URI)
        db = mongo_client.houdini_db

        count = db.data_lake.find({}).count()
        
        mongo_client.close()

        resp = make_response(
            jsonify({'stats': {'count': count}}), 200
        )
        resp.mimetype = 'application/json'
        return resp        
    except Exception as e:
        return make_response(
            jsonify({'error': e}), 400
        )    


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    python_env = os.environ.get('PYTHON_ENV', None)
    if python_env == 'development':
        app.run(host='0.0.0.0', debug = True)
    else:
        app.run(host='0.0.0.0', debug = False)