from celery import Celery
import db_conn
from db_conn import db
from models import *
import requests
import uuid
from dateutil.parser import parse as parse_date
import datetime
import time
from time import sleep
from flask import jsonify

app = Celery('tasks', broker='amqp://admin:password@rabbitmq/telaki')

IPP_URL = 'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/21586853/requests'
PASSPHRASE = 'PF5H8S9t7u'
APP_ID = 'MEoztReRyeHzaiXxaecR65HnqE98tz9g'
APP_SECRET = '01c5d1f8d3bfa9966786065c5a2d829d7e84cf26fbfb4a47c91552cb7c091608'

# os.environ['DATABASE_URL']
# 'postgresql://admin:sgbsaints@db/sgb'
# 'sqlite:///local.db'

@app.task
def send_messages(message_id):
    batch = Blast.query.filter_by(id=message_id).first()
    messages = Message.query.filter_by(blast_id=message_id).all()

    for message in messages:

        message_options = {
            'app_id': APP_ID,
            'app_secret': APP_SECRET,
            'message': message.content,
            'address': message.msisdn,
            'passphrase': PASSPHRASE,
        }

        try:
            r = requests.post(IPP_URL,message_options)           
            if r.status_code == 201:
                message.status = 'success'
                message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                db.session.commit()

            elif r.json()['error'] == 'Invalid address.':
                message.status = 'invalid address'
                message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                db.session.commit()

            else:
                message.status = 'failed'
                message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                db.session.commit()

        except requests.exceptions.ConnectionError as e:
            message.status = 'failed'
            message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            db.session.commit()
        
        batch.done = Message.query.filter_by(blast_id=message_id,status='success').count()
        batch.pending = Message.query.filter_by(blast_id=message_id,status='pending').count()
        batch.failed = Message.query.filter_by(blast_id=message_id,status='failed').count()
        db.session.commit()
    return