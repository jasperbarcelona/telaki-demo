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

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blast_id = db.Column(db.Integer())
    msisdn = db.Column(db.String(30))
    status = db.Column(db.String(30),default='pending')
    content = db.Column(db.Text)
    timestamp = db.Column(db.String(50))

class Blast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer())
    batch_size = db.Column(db.Integer())
    done = db.Column(db.Integer(),default=0)
    pending = db.Column(db.Integer(),default=0)
    failed = db.Column(db.Integer(),default=0)
    sender_name = db.Column(db.String(60))
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    timestamp = db.Column(db.String(50))

class AdminUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(60))
    password = db.Column(db.String(20))
    name = db.Column(db.String(100))
    status = db.Column(db.String(8), default='Active')
    added_by_id = db.Column(db.Integer)
    added_by_name = db.Column(db.String(100))
    join_date = db.Column(db.String(50))
    timestamp = db.Column(db.String(50))