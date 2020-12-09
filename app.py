import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)
load_dotenv()


@app.route('/')
def index():
    return render_template(
        'index.html'
    )

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
