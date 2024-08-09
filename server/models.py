from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from config import db

from datetime import datetime

# USER MODEL

class User(db.Model, SerializerMixin):
    
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, nullable=False, unique=True) # database constraints
    email = db.Column(db.String)
    address = db.Column(db.String)
    phone_number = db.Column(db.String)
    age = db.Column(db.Integer)
    vip = db.Column(db.Boolean)
    year_joined = db.Column(db.Integer) # range between 2000 and 2024

    @validates('year_joined')
    def validate_year_joined(self, key, value):
        # get current year bc we fancy
        current_year = datetime.now().year

        if not type(value) == int:
            raise ValueError('year_joined must be an integer') 
        # if the validation doesnt pass we raise an error
        if value not in range(2000, current_year + 1):
            raise ValueError(f'year_joined must be between 2000 and {current_year}')
        # if the validation passes we return the value
        return value
    

    @validates('email')
    def validate_email(self, key, value):
        if value.count('@') != 1: # if not exaclty 1 @ sign
            raise ValueError('Invalid email format')
        
        return value.lower()
    
    @validates('phone_number')
    def validate_phone_number(self, k, value):
        # remove any dashes
        cleaned_value = value.replace('-', '')

        if len(cleaned_value) != 10:
            raise ValueError("phone_number must be 10 digits long")
        
        if not all(char.isdigit() for char in cleaned_value):
            raise ValueError("phone_number must consist of digits")
        
        return cleaned_value
    
    @validates('address')
    def validate_address(self, k, value):

        if not any(pattern in value for pattern in ["Street", "Avenue", "Road"]):
            raise ValueError("address must include 'Street', 'Avenue', or 'Road'")
        
        if not all(char.isdigit() for char in value[-5:]):
            raise ValueError('address must include a 5 digit zipcode')
        
        return value