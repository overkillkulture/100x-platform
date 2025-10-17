"""ABSOLUTE MINIMAL FLASK TEST"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "FLASK IS WORKING!"

if __name__ == '__main__':
    print("Starting minimal Flask test on port 5002...")
    app.run(host='0.0.0.0', port=5002, debug=False)
