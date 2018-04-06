from functools import wraps
from flask import Flask, render_template, jsonify, abort
from flask import make_response, request
from flask import g, redirect, url_for

app = Flask(__name__)
app.config.from_object('settings')


# Middleware
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):                
        api_key = request.headers.get('x-api-key', None)

        if api_key is None:            
            return make_response(
                jsonify({'error': 'missing api key. check if `x-api-key` is defined in your header'}), 403
            )

        if api_key.lower() != app.config['API_KEY'].lower():
            return make_response(
                jsonify({'error': 'Unauthorized access. Invalid api key please check in wiith admin.'}), 401
            )
        
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function