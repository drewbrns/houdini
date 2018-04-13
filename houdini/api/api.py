import os
import time
from flask import Flask, render_template, jsonify, abort
from flask import make_response, request, session
from flask import g, redirect, url_for
from flask_session import Session
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

from middleware import authenticate, login_required
from helpers import login_user, json_response

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object('settings')

SESSION_TYPE = 'mongodb'
app.config.from_object(__name__)
Session(app)

MONGODB_URI = app.config['MONGODB_URI']
SECRET_KEY = app.config['SECRET_KEY']

### Routes

@app.before_request
def before_request():
    g.user = session.get('username', None)

# Index Page
@app.route('/')
@login_required   # Uncomment this when you implement login action
@authenticate
def home():

    mongo_client = MongoClient(MONGODB_URI)
    db = mongo_client.houdini_db

    data = {}
    data['count'] = db.data_lake.find({}).count()

    pawords = db.pa_words.find({})
    data['pawords'] = [ entry['word'].lower() for entry in pawords ]

    powords = db.po_words.find({})
    data['powords'] = [ entry['word'].lower() for entry in powords ]

    page = int(request.args.get('page', 0))
    limit = 10 
    skip = page * limit
    records = db.data_lake.find({}).skip(skip).limit(limit)
    records = list(records)
    data['records'] = json_util.dumps(records)
    page = page + 1
    data['page'] = page

    mongo_client.close()
                
    return render_template('home.html', data=data, records=records, username= g.user)

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
            session['jwt'] = user['jwt']
            return redirect(url_for('home'))
        except Exception as e:
            return render_template(
                'login.html', data={
                    'error': str(e), 
                    'username': username
                    }
                )
    else:      
        return render_template('login.html')
         

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('jwt', None)
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
            json_util.dumps(records), 
            200
        )
        resp.mimetype = 'application/json'
        return resp
    except Exception as e:
        return make_response(
            jsonify({'error': str(e)}), 400
        )


@app.route('/api/v1/stats', methods=['GET'])
@authenticate
def get_stats():
    try:
        mongo_client = MongoClient(MONGODB_URI)
        db = mongo_client.houdini_db
        count = db.data_lake.find({}).count()        
        mongo_client.close()

        return json_response(
            {'stats': {'count': count}},
            200
        )     
    except Exception as e:
        return json_response(
            {'error': str(e)},
            400
        )


@app.route('/api/v1/pawords', methods=['GET'])
@authenticate
def get_pa_words():
    try:
        mongo_client = MongoClient(MONGODB_URI)
        db = mongo_client.houdini_db
        words = db.pa_words.find({})
        words = [ entry['word'].lower() for entry in words ]        
        return json_response(
            {'pa_words': words},
            200
        )
    except Exception as e:        
        return make_response(
            jsonify({'error': str(e)}), 400
        )   


@app.route('/api/v1/pawords', methods=['POST', 'DELETE'])
@authenticate
def pa_word():
    mongo_client = MongoClient(MONGODB_URI)
    db = mongo_client.houdini_db
    
    if request.method == 'POST':
        word = request.form.get('word', None)
    else:
        word = request.args.get('word', None)

    if word:
        word = word.strip().lower()    
    
        stored_word = db.pa_words.find_one({
            'word': word
        })

        if request.method == 'POST':
            if stored_word is None:
                db.pa_words.insert_one({'word': word})
                return json_response(
                    {'word': word},
                    201
                )            
            else:
                return json_response(
                    {'error': '{} could not be saved, because it already exists.'.format(word)},
                    400
                )
        else:
            if stored_word is not None:
                db.pa_words.remove({'word': word})
                return json_response(
                    {'': ''},
                    204
                )
            else:
                return json_response(
                    {'error': '{} could not be removed, because it does not exist.'.format(word)},
                    400
                )
    else:
        return json_response(
            {'error': 'parameter `word` is required.'},
            400
        )            


@app.route('/api/v1/powords', methods=['GET'])
@authenticate
def get_po_words():
    try:
        mongo_client = MongoClient(MONGODB_URI)
        db = mongo_client.houdini_db
        words = db.po_words.find({})
        words = [ entry['word'].lower() for entry in words ]
        return json_response(
            {'po_words': words},
            200
        )
    except Exception as e:
        return make_response(
            jsonify({'error': str(e)}), 400
        )   



@app.route('/api/v1/powords', methods=['POST', 'DELETE'])
@authenticate
def po_word():
    mongo_client = MongoClient(MONGODB_URI)
    db = mongo_client.houdini_db

    if request.method == 'POST':
        word = request.form.get('word', None)
    else:
        word = request.args.get('word', None)

    if word:
        word = word.strip().lower()
        stored_word = db.po_words.find_one({
            'word': word
        })

        if request.method == 'POST':
            if stored_word is None:
                db.po_words.insert_one({'word': word})
                return json_response(
                    {'word': word},
                    201
                )            
            else:
                return json_response(
                    {'error': '{} could not be saved, because it already exists.'.format(word)},
                    400
                )
        else:
            if stored_word is not None:
                db.po_words.remove({'word': word})
                return json_response(
                    {'': ''},
                    204
                )
            else:
                return json_response(
                    {'error': '{} could not be removed, because it does not exist.'.format(word)},
                    400
                )
    else:
        return json_response(
            {'error': 'parameter `word` is required.'},
            400
        )


@app.route('/api/v1/annotate/<doc_id>', methods=['POST'])
@authenticate
def annotate(doc_id):
    mongo_client = MongoClient(MONGODB_URI)
    db = mongo_client.houdini_db
    a_class = request.form.get('class', None)

    if doc_id and a_class:
        a_class = a_class.strip()        
        db.data_lake.update_one({'_id':ObjectId(doc_id)}, {'$set': {'class': a_class}})
        return json_response({'': ''}, 204)        
    else:
        return json_response({'error': 'parameter `class` is required.'}, 400)



@app.template_filter('readable_date')
def readable_date_filter(value):
    return time.strftime('%a, %b %d %Y | %-I:%M:%S %p', time.localtime(value))

@app.errorhandler(404)
def not_found(error):
    return json_response(
        {'error': 'Not found'},
        404
    )    


if __name__ == '__main__':
    python_env = os.environ.get('PYTHON_ENV', None)
    if python_env == 'development':
        app.run(host='0.0.0.0', debug = True)
    else:
        app.run(host='0.0.0.0', debug = False)