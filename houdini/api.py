import os
from flask import Flask, jsonify, abort
from flask import make_response, request
from pymongo import MongoClient
from bson import json_util


API_KEY = os.environ.get('HOUDINI_API_KEY', None)
MONGODB_URI = os.environ.get('MONGODB_URI', None)


app = Flask(__name__)


@app.route('/api/v1/data', methods=['GET'])
def get_data():
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 10)
    api_key = request.headers.get('x-api-key', None)

    if api_key is not None and API_KEY is not None:
        if api_key.lower() == API_KEY.lower():
            mongo_client = MongoClient(MONGODB_URI)
            db = mongo_client.houdini_db
            records = db.data_lake.find({}).skip(skip).limit(limit)
            records = list(records)
            mongo_client.close()
            return make_response(
                json_util.dumps(records), 200
            )
        else:
            return make_response(jsonify({'error': 'unauthorized access'}), 401)

    return make_response(
        jsonify({'error': 'authorization error. check if `x-api-key` is defined in your header'}), 401
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