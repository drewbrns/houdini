import os
from flask import Flask, jsonify, abort
from flask import make_response, request
from pymongo import MongoClient
from bson import json_util

from functools import wraps


API_KEY = os.environ.get('HOUDINI_API_KEY', None)
MONGODB_URI = os.environ.get('MONGODB_URI', None)


app = Flask(__name__)

# Middleware
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):                
        api_key = request.headers.get('x-api-key', None)

        if api_key is None:            
            return make_response(
                jsonify({'error': 'missing api key. check if `x-api-key` is defined in your header'}), 403
            )

        if api_key.lower() != API_KEY.lower():
            return make_response(
                jsonify({'error': 'Unauthorized access. Invalid api key please check in wiith admin.'}), 401
            )
        
        return f(*args, **kwargs)
    return decorated_function


# Routes

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