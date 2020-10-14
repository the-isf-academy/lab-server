from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
