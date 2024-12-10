#!/usr/bin/env python3

from flask import request
from config import app, db
from models import Landlord

@app.get('/')
def index():
    return "Hello world"


# GET REQUEST TO GET ALL LANDLORDS
@app.get('/landlords')
def get_all_landlords():
    all_landlords = Landlord.query.all()

    landlord_dicts = [ 
        landlord.to_dict(rules=['-violations']) 
        for landlord 
        in all_landlords
    ]

    return landlord_dicts, 200
    # return [ l.to_dict() for l in Landlord.query.all() ], 200


# GET REQUEST TO GET A LANDLORD BY ID
@app.get('/landlords/<int:landlord_id>')
def get_landlord_by_id(landlord_id):
    # 1. find the landlord with that id
    found_landlord = Landlord.query.where(Landlord.id == landlord_id).first()

    if found_landlord:
        # 2. send it to the client if it exists (the client is whatever is making the request)
        return found_landlord.to_dict(), 200

    else:
        # 3. send a 404 if it doesn't exist
        return { "status": 404, "message": "Not found" }, 404


# POST REQUEST TO MAKE A NEW LANDLORD
@app.post('/landlords')
def create_new_landlord():
    # 1. parse the body
    body = request.json

    try:

        # 2. create a new landlord instance using the parsed body
        new_landlord = Landlord( associated_llcs=body.get('associated_llcs') )

        # 3. add and commit the new landlord
        db.session.add( new_landlord )
        db.session.commit()

        # 4. transform landlord into a dictionary and return the dictionary in the response
        return new_landlord.to_dict(), 201
    
    # 5. return an error message for errors
    except Exception as error:

        return {
            "status": 400,
            "message": "Something went really wrong... do you have an associated_llcs?",
            "error_text": str(error)
        }, 400


# RUN ##########################

if __name__ == '__main__':
    app.run(port=5555, debug=True)