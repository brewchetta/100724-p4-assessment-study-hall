from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from config import db
from sqlalchemy.orm import validates


# Landlord --< Violation >-- Tenant


class Landlord(db.Model, SerializerMixin):

    __tablename__ = 'landlords_table'

    id = db.Column(db.Integer, primary_key=True)
    associated_llcs = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, default=1)
    mgmt_company = db.Column(db.String(20))

    violations = db.relationship('Violation', back_populates='landlord', cascade='all, delete-orphan')

    tenants = association_proxy('violations', 'tenant')

    serialize_rules = ('-violations.landlord', 'tenants', '-tenants.landlords', '-tenants.violations',)

    # VALIDATIONS

    @validates('rating')
    def validate_rating(self, key, new_value):
        if type(new_value) != int:
            raise ValueError('Landlord rating must be an integer')

        if not 1 <= new_value <= 5:
            raise ValueError('Landlord rating must be between 1 and 5 inclusive')

        return new_value


    @validates('associated_llcs')
    def validate_llc(self, key, new_value):
        if type(new_value) != str:
            raise ValueError('Landlord associated_llcs must be a string')

        if not "llc" in new_value.lower():
            raise ValueError('LLC must be part of the name for associated_llcs')

        return new_value


class Violation(db.Model, SerializerMixin):

    __tablename__ = 'violations_table'

    id = db.Column(db.Integer, primary_key=True)
    currently_in_litigation = db.Column(db.Boolean, default=True)
    case_number = db.Column(db.String)
    description = db.Column(db.String)

    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords_table.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants_table.id'))

    landlord = db.relationship('Landlord', back_populates='violations')
    tenant = db.relationship('Tenant', back_populates='violations')
    
    def litigation_for_violation(self):
        if self.currently_in_litigation:
            return "Currently in litigation"
        else:
            return "Not currently in litigation"

    serialize_rules = ('-landlord.violations', '-tenant.violations', 'litigation_for_violation')

class Tenant(db.Model, SerializerMixin):

    __tablename__ = 'tenants_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="Anonymous")

    violations = db.relationship('Violation', back_populates='tenant')

    landlords = association_proxy('violations','landlord')

    serialize_rules = ('-violations.tenant', 'landlords', '-landlords.tenants', '-landlords.violations',)