#!/usr/bin/env python3

from config import app, db
from models import Landlord, Violation
from faker import Faker
import secrets
from random import choice as random_choice

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        Landlord.query.delete()
        Violation.query.delete()

        print("Creating landlords...")

        for _ in range(3):
            new_landlord = Landlord(associated_llcs=faker.name())
            db.session.add(new_landlord)

        db.session.commit()

        print("Creating violations...")

        for _ in range(70):
            random_landlord = random_choice( Landlord.query.all() )

            new_violation = Violation(
                case_number=secrets.token_hex(8),
                description=faker.sentence(),
                landlord_id=random_landlord.id
            )

            db.session.add(new_violation)

        db.session.commit()

        print("Seeding complete!")