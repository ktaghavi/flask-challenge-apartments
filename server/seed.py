from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Apartment,Tenant,Lease

fake = Faker()

def create_apartments():
    apartments = []
    for _ in range(25):
        p = Apartment(
            number=str(randint(1, 100)),
        )
        apartments.append(p)
    return apartments

def create_tenant():
    tenants = []
    for _ in range(25):
        s = Tenant(
            name=fake.name(),
            age=randint(18, 50),
        )
        tenants.append(s)
    return tenants

def create_lease(apartments,tenants):
    leases = []
    for _ in range(20):
        m = Lease(
            rent=randint(2000, 5000),
            tenant_id=rc(tenants).id,
            apartment_id=rc(apartments).id
        )
        leases.append(m)
    return leases

if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        Tenant.query.delete()
        Apartment.query.delete()
        Lease.query.delete()

        print("Seeding Apartments...")
        apartments = create_apartments()
        db.session.add_all(apartments)
        db.session.commit()

        print("Seeding Tenants...")
        tenants = create_tenant()
        db.session.add_all(tenants)
        db.session.commit()

        print("Seeding Leases...")
        leases = create_lease(apartments, tenants)
        db.session.add_all(leases)
        db.session.commit()

        print("Done seeding!")
