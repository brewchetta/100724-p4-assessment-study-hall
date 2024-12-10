#!/usr/bin/env python3

from flask import request
from config import app, db
from models import db

@app.get('/')
def index():
    return "Hello world"


# RUN ##########################

if __name__ == '__main__':
    app.run(port=5555, debug=True)