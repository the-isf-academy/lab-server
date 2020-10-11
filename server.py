# Server file for server lab (server.py)
# By: Will Chau

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os.path
from sqlalchemy.exc import SQLAlchemyError

#error codes
SUCCESS = "1"
USER_EXISTS_IN_DB = "10"
USER_DOES_NOT_EXIST = "11"
AUTHENTICATION_FAILED = "12"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messges_db.sqlite'
db = SQLAlchemy(app)

#Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(120), nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.Float(120), unique=True, nullable=False)

#User/Password Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),  nullable=False)

if not os.path.isfile('messges_db.sqlite'):
    db.create_all()
    db.session.commit()


def check_username_password(username, password):
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
    try:
        query = Message(sender=sender, recipient=recipient, message=message,timestamp=timestamp)
        db.session.add(query)
        db.session.commit()
        return SUCCESS

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def register_user_to_db(username, password):
    try:
        query = User(username=username, password=password)
        db.session.add(query)
        db.session.commit()
        return SUCCESS

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def find_user_from_db(username):
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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if find_user_from_db(username) == USER_DOES_NOT_EXIST:
        register_user_to_db(username, password)
        return SUCCESS
    else:
        return USER_EXISTS_IN_DB

@app.route('/auth', methods=['GET'])
def authenticate():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if find_user_from_db(username) == USER_DOES_NOT_EXIST:
        return USER_DOES_NOT_EXIST
    else:
        return check_username_password(username, password)

@app.route('/', methods=['POST'])
def save_message():
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']
    timestamp = data['timestamp']
    return save_message_to_db(sender, recipient, message, timestamp)

@app.route('/get_messages', methods=['GET'])
def get_messages():
    data = request.get_json()
    person = data['username']
    return get_messages_from_db(person)
