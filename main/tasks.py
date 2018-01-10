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
UPLOAD_FOLDER = 'static/records'
# os.environ['DATABASE_URL']
# 'postgresql://admin:sgbsaints@db/sgb'
# 'sqlite:///local.db'

@app.task
def blast_sms(batch_id,date,time,message_content,client_no):
    client = Client.query.filter_by(client_no=client_no).first()
    batch = Batch.query.filter_by(client_no=client_no,id=batch_id).first()
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
def upload_contacts(batch_id,client_no,user_id,user_name):
    batch = ContactBatch.query.filter_by(id=batch_id).first()
    
    path = '%s/%s' % (UPLOAD_FOLDER, batch.file_name)
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows;
    cols = 3

    for row in range(rows):
        vals = []
        for col in range(cols):
            cell = sheet.cell(row,col)
            if cell.value == '':
                vals.append(None)
            else:
                vals.append(cell.value)

        contact = Contact.query.filter_by(msisdn='0%s'%str(vals[0])[-10:]).first()
        group = Group.query.filter_by(name=vals[2]).first()
        if contact or contact != None:
            contact.name = vals[1].title()
            db.session.commit()
        else:
            contact = Contact(
                batch_id=batch.id,
                client_no=client_no,
                contact_type='Customer',
                name=vals[1].title(),
                msisdn='0%s'%str(vals[0])[-10:],
                added_by=user_id,
                added_by_name=user_name,
                join_date=datetime.datetime.now().strftime('%B %d, %Y'),
                created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                )
            db.session.add(contact)
            db.session.commit()

        conversation = Conversation.query.filter_by(msisdn=contact.msisdn).first()
        if conversation or conversation != None:
            conversation.contact_name = contact.name
            conversation.display_name = contact.name

        db.session.commit()

        if not group or group == None:
            group = Group(
                client_no=client_no,
                name=vals[2],
                created_by_id=user_id,
                created_by_name=user_name,
                created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                )
            db.session.add(group)
            db.session.commit()

        contact_group = ContactGroup.query.filter_by(contact_id=contact.id,group_id=group.id).first()
        if not contact_group or contact_group == None:
            new_contact_group = ContactGroup(
                contact_id=contact.id,
                group_id=group.id
                )
            db.session.add(new_contact_group)
            db.session.commit()
            group.size = ContactGroup.query.filter_by(group_id=group.id).count()
            db.session.commit()

        existing = Contact.query.filter_by(batch_id=str(batch.id)).count()
        batch.pending = batch.batch_size - existing
        db.session.commit()
    return

@app.task
def send_reminders(batch_id,date,time,client_no):
    client = Client.query.filter_by(client_no=client_no).first()
    batch = ReminderBatch.query.filter_by(client_no=client_no,id=batch_id).first()
    messages = ReminderMessage.query.filter_by(batch_id=batch_id).all()

    for message in messages:
        message_options = {
            'app_id': client.app_id,
            'app_secret': client.app_secret,
            'message': message.content,
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
        
        batch.done = ReminderMessage.query.filter_by(batch_id=batch.id,status='success').count()
        batch.pending = ReminderMessage.query.filter_by(batch_id=batch.id,status='pending').count()
        batch.failed = ReminderMessage.query.filter_by(batch_id=batch.id,status='failed').count()
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
