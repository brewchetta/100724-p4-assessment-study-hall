#!/usr/bin/env python3

from flask import request
from config import app, db
from models import Landlord

@app.get('/')
def index():
    return "Hello world"


# POST REQUEST TO MAKE A NEW LANDLORD
@app.post('/landlords')
def create_new_landlord():
    # 1. parse the body
    body = request.json

    try:

        # 2. create a new landlord instance using the parsed body
        new_landlord = Landlord(
            associated_llcs=body.get('associated_llcs'), 
            violations=body.get('violations'), 
            currently_in_litigation=body.get('currently_in_litigation')
        )

        # 3. add and commit the new landlord
        db.session.add( new_landlord )
        db.session.commit()

        # 4. transform landlord into a dictionary and return the dictionary in the response
        landlord_dict = {
            "id": new_landlord.id,
            "associated_llcs": new_landlord.associated_llcs,
            "violations": new_landlord.violations,
            "currently_in_litigation": new_landlord.currently_in_litigation
        }

        return landlord_dict, 201
    
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