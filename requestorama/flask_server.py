"""flask_server.py: A simple Flask server"""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    print("flask server start")
    app.run(port=8082)