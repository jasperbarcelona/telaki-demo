import flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean
from db_conn import db, app
import json

class Serializer(object):
  __public__ = None

  def to_serializable_dict(self):
    dict = {}
    for public_key in self.__public__:
      value = getattr(self, public_key)
      if value:
        dict[public_key] = value
    return dict

class SWEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Serializer):
      return obj.to_serializable_dict()
    if isinstance(obj, (datetime)):
      return obj.isoformat()
    return json.JSONEncoder.default(self, obj)

def SWJsonify(*args, **kwargs):
  return app.response_class(json.dumps(dict(*args, **kwargs), cls=SWEncoder, 
         indent=None if request.is_xhr else 2), mimetype='application/json')
        # from https://github.com/mitsuhiko/flask/blob/master/flask/helpers.py

class Client(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    client_no = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(50))
    app_id = db.Column(db.Text())
    app_secret = db.Column(db.Text())
    passphrase = db.Column(db.Text())
    shortcode = db.Column(db.String(30))
    created_at = db.Column(db.String(50))

class AdminUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    client_no = db.Column(db.String(32))
    email = db.Column(db.String(60))
    password = db.Column(db.String(20))
    api_key = db.Column(db.String(32))
    temp_pw = db.Column(db.String(20))
    name = db.Column(db.String(100))
    role = db.Column(db.String(30))
    added_by_id = db.Column(db.Integer)
    added_by_name = db.Column(db.String(100))
    join_date = db.Column(db.String(50))
    created_at = db.Column(db.String(50))

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_no = db.Column(db.String(32))
    message_type = db.Column(db.String(60))
    sender_id = db.Column(db.Integer())
    batch_size = db.Column(db.Integer())
    done = db.Column(db.Integer(),default=0)
    pending = db.Column(db.Integer(),default=0)
    failed = db.Column(db.Integer(),default=0)
    sender_name = db.Column(db.String(60))
    recipient = db.Column(db.Text())
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    content = db.Column(db.Text)
    created_at = db.Column(db.String(50))

class ReminderBatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_no = db.Column(db.String(32))
    sender_id = db.Column(db.Integer())
    batch_size = db.Column(db.Integer())
    done = db.Column(db.Integer(),default=0)
    pending = db.Column(db.Integer(),default=0)
    failed = db.Column(db.Integer(),default=0)
    sender_name = db.Column(db.String(100))
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    file_name = db.Column(db.Text)
    created_at = db.Column(db.String(50))

class ContactBatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_no = db.Column(db.String(32))
    uploader_id = db.Column(db.Integer())
    uploader_name = db.Column(db.String(100))
    batch_size = db.Column(db.Integer())
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    file_name = db.Column(db.Text)
    done = db.Column(db.Integer(),default=0)
    pending = db.Column(db.Integer(),default=0)
    failed = db.Column(db.Integer(),default=0)
    created_at = db.Column(db.String(50))

class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    batch_id = db.Column(db.String(30),default='N/A')
    client_no = db.Column(db.String(32))
    contact_type = db.Column(db.String(32))
    name = db.Column(db.String(100))
    msisdn = db.Column(db.String(20))
    added_by = db.Column(db.Integer())
    added_by_name = db.Column(db.String(100))
    join_date = db.Column(db.String(50))
    created_at = db.Column(db.String(50))

class OutboundMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer())
    bill_id = db.Column(db.Integer())
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    contact_name = db.Column(db.String(100))
    msisdn = db.Column(db.String(30))
    content = db.Column(db.Text())
    characters = db.Column(db.Integer())
    cost = db.Column(db.String(10))
    status = db.Column(db.String(30),default='pending')
    created_at = db.Column(db.String(50))

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(60))
    used = db.Column(db.Integer())
    available = db.Column(db.Integer())
    price = db.Column(db.String(30),default='1299.00')
    created_at = db.Column(db.String(50))

class ReminderMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer())
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    contact_name = db.Column(db.String(100), default='Unknown')
    content = db.Column(db.Text())
    msisdn = db.Column(db.String(30))
    status = db.Column(db.String(30),default='pending')
    created_at = db.Column(db.String(50))

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_no = db.Column(db.String(32))
    contact_name = db.Column(db.String(100), default=None)
    msisdn = db.Column(db.String(30))
    display_name = db.Column(db.String(100))
    status = db.Column(db.String(30),default='unread')
    latest_content = db.Column(db.Text())
    latest_date = db.Column(db.String(20))
    latest_time = db.Column(db.String(10))
    created_at = db.Column(db.String(50))

class ConversationItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer())
    message_type = db.Column(db.String(30))
    outbound_sender_id = db.Column(db.Integer())
    outbound_sender_name = db.Column(db.String(100))
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    content = db.Column(db.Text)
    created_at = db.Column(db.String(50))

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_no = db.Column(db.String(32))
    name = db.Column(db.String(32))
    size = db.Column(db.Integer(),default=0)
    created_by_id = db.Column(db.Integer())
    created_by_name = db.Column(db.String(100))
    created_at = db.Column(db.String(50))

class ContactGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer())
    contact_id = db.Column(db.Integer())