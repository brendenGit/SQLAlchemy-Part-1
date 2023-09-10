"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
brenden = User(first_name='Brenden', last_name='Arias')
sage = User(first_name='Sage', last_name='Arias-Hart', profile_picture='https://cf.ltkcdn.net/dogs/puppies/images/orig/326566-1600x1066-guide-great-pyrenees-puppies.jpg')
meghan = User(first_name='Meghan', last_name='Hart')

# Add new objects to session, so they'll persist
db.session.add(brenden)
db.session.add(sage)
db.session.add(meghan)

# Commit--otherwise, this never gets saved!
db.session.commit()
