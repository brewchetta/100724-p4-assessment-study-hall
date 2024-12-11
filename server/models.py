from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from config import db


# Landlord --< Violation >-- Tenant


class Landlord(db.Model, SerializerMixin):

    __tablename__ = 'landlords_table'

    id = db.Column(db.Integer, primary_key=True)
    associated_llcs = db.Column(db.String, nullable=False)

    violations = db.relationship('Violation', back_populates='landlord', cascade='all, delete-orphan')

    tenants = association_proxy('violations', 'tenant')

    serialize_rules = ('-violations.landlord', 'tenants', '-tenants.landlords', '-tenants.violations',)

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

    serialize_rules = ('-landlord.violations', '-tenant.violations')

class Tenant(db.Model, SerializerMixin):

    __tablename__ = 'tenants_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="Anonymous")

    violations = db.relationship('Violation', back_populates='tenant')

    landlords = association_proxy('violations','landlord')

    serialize_rules = ('-violations.tenant', 'landlords', '-landlords.tenants', '-landlords.violations',)