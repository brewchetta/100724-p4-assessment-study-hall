#!/usr/bin/env python3

from config import app, db
# from models import ???
from faker import Faker
from random import choice as random_choice

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        print("Seeding complete!")