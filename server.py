from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os.path
from sqlalchemy.ext.serializer import dumps

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messges_db.sqlite'
db = SQLAlchemy(app)

#error codes
SUCCESS = "1"
USER_EXISTS_IN_DB = "10"
PASSWORD_INCORRECT = "11"

#Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(120), nullable=False)
    recipent = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.Float(120), unique=True, nullable=False)

#User/Password Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),  nullable=False)

if not os.path.isfile('messges_db.sqlite'):
    db.create_all()

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    query = User.query.filter_by(user=data["user"], password=data["password"]).first()
    #if not found in db
    if query is not None:
        return SUCCESS
    else:
        return PASSWORD_INCORRECT

@app.route('/', methods=['POST'])
def save_message():
    data = request.get_json()
    query = Message(sender=data["sender"], recipent=data["recipent"], message=data["message"],timestamp=data["timestamp"])
    db.session.add(query)
    db.session.commit()
    return SUCCESS

@app.route('/get_messages', methods=['POST'])
def get_messages():
    data = request.get_json()
    query = Message.query.filter_by(recipent=data["user"]).all()
    serialized = dumps(query)
    return serialized

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    query = User.query.filter_by(user=data["user"]).first()
    #if not found in db
    if not query:
        query = User(user=data["user"], password=data["password"])
        db.session.add(query)
        db.session.commit()
        return SUCCESS
    else:
        return USER_EXISTS_IN_DB
