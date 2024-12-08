from flask import Flask
import weather_api

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'
