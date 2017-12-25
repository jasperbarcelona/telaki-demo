from celery import Celery
import db_conn
from db_conn import db
from models import *
import requests
import uuid
from cStringIO import StringIO
from dateutil.parser import parse as parse_date
import datetime
import time
from time import sleep
from flask import jsonify
import xlrd

app = Celery('tasks', broker='amqp://admin:password@rabbitmq/telaki')

IPP_URL = 'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/%s/requests'

# os.environ['DATABASE_URL']
# 'postgresql://admin:sgbsaints@db/sgb'
# 'sqlite:///local.db'

@app.task
def blast_sms(batch_id,date,time,message_content,client_no):
    client = Client.query.filter_by(client_no=client_no).first()
    batch = Batch.query.filter_by(id=batch_id).first()
    messages = OutboundMessage.query.filter_by(batch_id=batch_id).all()

    for message in messages:
        message_options = {
            'app_id': client.app_id,
            'app_secret': client.app_secret,
            'message': message_content,
            'address': message.msisdn,
            'passphrase': client.passphrase,
        }

        try:
            r = requests.post(IPP_URL%client.shortcode,message_options)           
            if r.status_code == 201:
                message.status = 'success'
                message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            else:
                message.status = 'failed'
                message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')

            db.session.commit()

        except requests.exceptions.ConnectionError as e:
            message.status = 'failed'
            message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            db.session.commit()
        
        batch.done = OutboundMessage.query.filter_by(batch_id=batch.id,status='success').count()
        batch.pending = OutboundMessage.query.filter_by(batch_id=batch.id,status='pending').count()
        batch.failed = OutboundMessage.query.filter_by(batch_id=batch.id,status='failed').count()
        db.session.commit()

    return


@app.task
def send_message(log_id, type, message, msisdn, action):
    log = Log.query.filter_by(id=log_id).first()

    message_options = {
            'app_id': APP_ID,
            'app_secret': APP_SECRET,
            'message': message,
            'address': msisdn,
            'passphrase': PASSPHRASE,
        }

    try:
        r = requests.post(IPP_URL,message_options)           
        if r.status_code == 201:
            if action == 'entered':
                log.time_in_notification_status='Success'
            else:
                log.time_out_notification_status='Success'
            db.session.commit()
            return

        if r.json()['error'] == 'Invalid address.':
            if action == 'entered':
                log.time_in_notification_status='Invalid address'
            else:
                log.time_out_notification_status='Invalid address'
            db.session.commit()
            return

        if action == 'entered':
            log.time_in_notification_status='Failed'
        else:
            log.time_out_notification_status='Failed'
        db.session.commit()
        return

    except requests.exceptions.ConnectionError as e:
        if action == 'entered':
            log.time_in_notification_status='Failed'
        else:
            log.time_out_notification_status='Failed'
        db.session.commit()
        return
