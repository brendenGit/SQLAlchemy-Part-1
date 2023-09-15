"""Seed file to make sample data for pets db."""

from models import User, Post, db, Tag, PostTag
from app import app


db.drop_all()
db.create_all()

User.query.delete()

brenden = User(first_name='Brenden', last_name='Arias')
sage = User(first_name='Sage', last_name='Arias-Hart', profile_picture='https://cf.ltkcdn.net/dogs/puppies/images/orig/326566-1600x1066-guide-great-pyrenees-puppies.jpg')
meghan = User(first_name='Meghan', last_name='Hart')

db.session.add(brenden)
db.session.add(sage)
db.session.add(meghan)

db.session.commit()

post1 = Post(title='Brenden Test Post', 
             content='Brenden Test Post Content', 
             user_id=1)
post2 = Post(title='Sage the Dog Test Post', 
             content='Sage the Dog Test Post Content',
             user_id=2)
post3 = Post(title='Meghan the lady Test Post', 
             content='Meghan the lady Test Post Content', 
             user_id=3)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

db.session.commit()

tag1 = Tag(tag_name='Funny',
           posts=[PostTag(post_id=post3.id)])
tag2 = Tag(tag_name='Serious',
           posts=[PostTag(post_id=post1.id),
                 PostTag(post_id=post2.id)])
tag3 = Tag(tag_name='Cuhrazzy',
           posts=[PostTag(post_id=post1.id),
                 PostTag(post_id=post2.id)])

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

db.session.commit()
