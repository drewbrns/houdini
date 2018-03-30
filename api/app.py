from flask import Flask, jsonify, abort, make_response


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/start')
def start_houdini():
    return "Hello, World!"

@app.route('/stop')
def stop_houdini():
    return ""

@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'error': 'Not found'}), 
        404
        )


if __name__ == '__main__':
    app.run(debug = True)