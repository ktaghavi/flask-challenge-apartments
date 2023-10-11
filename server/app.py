from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )

@app.route('/')
def home():
    return ''

@app.get('/apartments')
def get_all_apartments():
    apartments = Apartment.query.all()
    data = [apartment.to_dict(rules=('-leases',)) for apartment in apartments]

    return make_response(
        jsonify(data),
        200
    )

@app.post('/apartments')
def post_apartment():
    data = request.get_json()

    try:
        new_apartment = Apartment(
            number=data.get("number")
        )
        db.session.add(new_apartment)
        db.session.commit()

        return make_response(
            jsonify(new_apartment.to_dict(rules=('-leases',))),
            201
        )
    except ValueError:
        return make_response(
            jsonify({'error': ['validation errors']}),
            406
        )

@app.patch('/apartments/<int:id>')
def patch_apartment_by_id(id):
    apartment = Apartment.query.filter(Apartment.id == id).first()
    data = request.get_json()

    if not apartment:
        return make_response(
            jsonify({'error': ['validation errors']}),
            404
        )

    try:
        for field in data:
            setattr(apartment, field, data[field])
        db.session.add(apartment)
        db.session.commit()

        return make_response(
            jsonify(apartment.to_dict(rules=('-leases',))),
            202
        )
    except ValueError:
        return make_response(
            jsonify({'error': ['validation errors']}),
            406
        )

@app.delete('/apartments/<int:id>')
def delete_apartment(id):
    apartment = Apartment.query.filter(Apartment.id == id).first()

    if not apartment:
        return make_response(
            jsonify({'error': ['Activity not found']}),
            404
        )
    db.session.delete(apartment)
    db.session.commit()

    return make_response(jsonify({}), 204)

################################################################

@app.get('/tenants')
def get_all_tenants():
    tenants = Tenant.query.all()
    data = [tenant.to_dict(rules=('-leases',)) for tenant in tenants]

    return make_response(
        jsonify(data),
        200
    )

@app.post('/tenants')
def post_tenant():
    data = request.get_json()

    try:
        new_tenant = Tenant(
            name=data.get("name"),
            age=data.get("age")
        )
        db.session.add(new_tenant)
        db.session.commit()

        return make_response(
            jsonify(new_tenant.to_dict(rules=('-leases',))),
            201
        )
    except ValueError:
        return make_response(
            jsonify({'error': ['validation errors']}),
            406
        )

@app.patch('/tenants/<int:id>')
def patch_tenant_by_id(id):
    tenant = Tenant.query.filter(Tenant.id == id).first()
    data = request.get_json()

    if not tenant:
        return make_response(
            jsonify({'error': ['validation errors']}),
            404
        )

    try:
        for field in data:
            setattr(tenant, field, data[field])
        db.session.add(tenant)
        db.session.commit()

        return make_response(
            jsonify(tenant.to_dict(rules=('-leases',))),
            202
        )
    except ValueError:
        return make_response(
            jsonify({'error': ['validation errors']}),
            406
        )

@app.delete('/tenants/<int:id>')
def delete_tenant(id):
    tenant = Tenant.query.filter(Tenant.id == id).first()

    if not tenant:
        return make_response(
            jsonify({'error': ['Activity not found']}),
            404
        )
    db.session.delete(tenant)
    db.session.commit()

    return make_response(jsonify({}), 204)

###################################################################

@app.post('/lease')
def post_lease():
    data = request.get_json()

    try:
        new_lease = Lease(
            rent=data.get("rent"),
            tenant_id=data.get("tenant_id"),
            apartment_id=data.get("apartment_id")
        )
        db.session.add(new_lease)
        db.session.commit()

        return make_response(
            jsonify(new_lease.to_dict(rules=('tenant', 'apartment', '-tenant.lease', '-apartment.lease'))),
            201
        )
    except ValueError:
        return make_response(
            jsonify({'error': ['validation errors']}),
            406
        )

@app.delete('/lease/<int:id>')
def delete_lease(id):
    lease = Lease.query.filter(Lease.id == id).first()

    if not lease:
        return make_response(
            jsonify({'error': ['Activity not found']}),
            404
        )
    db.session.delete(lease)
    db.session.commit()

    return make_response(jsonify({}), 204)

if __name__ == '__main__':
    app.run( port = 3000, debug = True )