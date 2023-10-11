from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartments_table'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)

    #Add relationshps
    leases = db.relationship("Lease", backref="apartment")

    #Add serialization rules

    def __repr__(self):
        return f'<Apartment {self.id}: {self.number}>'

class Tenant(db.Model, SerializerMixin):
    __tablename__ = 'tenants_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    
    #Add relationshps
    leases = db.relationship("Lease", backref="tenant")
    #Add serialization rules

    #Add validation
    @validates('age')
    def validate_age(self, key, age):
        if not age >= 18:
            raise ValueError('Age must be 18 or over!')
        return age

    def __repr__(self):
        return f'<Tenant {self.id}: {self.name}: {self.age}>'

class Lease(db.Model, SerializerMixin):
    __tablename__ = 'leases_table'

    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.Integer, nullable=False)
    
    #Add relationshps
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants_table.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments_table.id'))

    #Add serialization rules
    serialize_rules = ('-tenant', '-apartment')

    def __repr__(self):
        return f'<Lease {self.id}>'