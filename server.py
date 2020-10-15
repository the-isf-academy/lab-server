# Server file for server lab (server.py)
# By: Will Chau

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os.path
from sqlalchemy.exc import SQLAlchemyError
from models import db, Message, User

#error codes
SUCCESS = "1"
USER_EXISTS_IN_DB = "10"
USER_DOES_NOT_EXIST = "11"
AUTHENTICATION_FAILED = "12"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messges_db.sqlite'
db.init_app(app)

if not os.path.isfile('messges_db.sqlite'):
    db.create_all()
    db.session.commit()

def check_username_password(username, password):
    '''Given a username and password, will return a SUCCESS code if
    the username and password is correct, otherwise will return a
    PASSWORD_INCORRECT code'''
    try:
        query = User.query.filter_by(username=username, password=password).first()
        #if not found in db
        if query is not None:
            return SUCCESS
        else:
            return AUTHENTICATION_FAILED

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def save_message_to_db(sender, recipient, message, timestamp):
    '''Given a sender, recipient, message and timestamp, adds a message
    record to the database. Returns a SUCCESS code if it was successful,
    otherwise, it will return a SQLAlchemy error'''
    try:
        query = Message(sender=sender, recipient=recipient, message=message,timestamp=timestamp)
        db.session.add(query)
        db.session.commit()
        return SUCCESS

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def register_user_to_db(username, password):
    '''Given a username and password, adds a user record in the database.
    Returns a SUCCESS code if it was successful, otherwise, it will
    return a SQLAlchemy error'''
    try:
        query = User(username=username, password=password)
        db.session.add(query)
        db.session.commit()
        return SUCCESS

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def find_user_from_db(username):
    '''Given a username, finds that username in the database. If the
    username is not found, returns false, otherwise, it will return a SQLAlchemy error'''
    try:
        query = User.query.filter_by(username=username).first()
        if not query:
            return USER_DOES_NOT_EXIST
        else:
            return USER_EXISTS_IN_DB

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def get_messages_from_db(person):
    '''Give a person's username, gets all the messages sent to that
    person and returns a list of messages even if there are no messages.
    Each message is stored in a dictionary based on the Message Model.'''
    try:
        query = Message.query.filter_by(recipient=person).all()
        messageList = []
        for row in query:
            row_as_dict = row.__dict__
            row_as_dict.pop('_sa_instance_state', None)
            messageList.append(row_as_dict)
        return {"messages": messageList}

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

#WRITE CODE FOR PART D.1 HERE
    

#WRITE CODE FOR PART D.2 HERE


#WRITE CODE FOR PART D.3 HERE


#WRITE CODE FOR PART D.4 HERE


