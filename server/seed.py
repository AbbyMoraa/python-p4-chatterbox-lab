#!/usr/bin/env python3

from random import choice as rc
from faker import Faker

from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():
    # Clear existing messages
    Message.query.delete()
    
    messages = []

    # Add the specific test message
    hello_msg = Message(
        body="Hello 👋",
        username="Duane"
    )
    messages.append(hello_msg)

    # Add 20 random messages
    for i in range(20):
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)

    db.session.add_all(messages)
    db.session.commit()        

if __name__ == '__main__':
    with app.app_context():
        make_messages()