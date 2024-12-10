#!/usr/bin/env python3

from config import app, db
from models import Landlord
from faker import Faker

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        print("Seeding complete!")