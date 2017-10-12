import flask, flask.views
from flask import url_for, request, session, redirect, jsonify, Response, make_response, current_app
from jinja2 import environment, FileSystemLoader
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean
from flask.ext import admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from dateutil.parser import parse as parse_date
from flask import render_template, request
from flask import session, redirect
from datetime import timedelta
from datetime import datetime
from functools import wraps, update_wrapper
import threading
from threading import Timer
from multiprocessing.pool import ThreadPool
import calendar
from calendar import Calendar
from time import sleep
import requests
import datetime
from datetime import date
import time
import json
import uuid
import random
import string
import smtplib
from email.mime.text import MIMEText as text
import os
import db_conn
from db_conn import db, app
from models import Message, Blast, AdminUser
from werkzeug.utils import secure_filename
from tasks import send_messages
import xlrd

IPP_URL = 'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/21586853/requests'
PASSPHRASE = 'PF5H8S9t7u'
APP_ID = 'MEoztReRyeHzaiXxaecR65HnqE98tz9g'
APP_SECRET = '01c5d1f8d3bfa9966786065c5a2d829d7e84cf26fbfb4a47c91552cb7c091608'

UPLOAD_FOLDER = 'static/records'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

now = datetime.datetime.now()

class IngAdmin(sqla.ModelView):
    column_display_pk = True

admin = Admin(app, name='telaki')
admin.add_view(IngAdmin(Message, db.session))
admin.add_view(IngAdmin(Blast, db.session))

def compose_messages(filename):
    path = '%s/%s' % (UPLOAD_FOLDER, filename)

    book = xlrd.open_workbook(path)
 
    # get the first worksheet
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows;
    cols = 2
    print 'xxxxxxxxxxxxxxxxxxx'
    print rows

    new_blast = Blast(
        sender_id=session['user_id'],
        batch_size=rows,
        sender_name=session['user_name'],
        date=time.strftime("%B %d, %Y"),
        time=time.strftime("%I:%M %p"),
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )
    db.session.add(new_blast)
    db.session.commit()
 
    for row in range(rows):
        vals = []
        for col in range(cols):
            cell = sheet.cell(row,col)
            if cell.value == '':
                vals.append(None)
            else:
                vals.append(cell.value)

        new_message = Message(
            blast_id=new_blast.id,
            msisdn=vals[0],
            content=vals[1]
            )
        db.session.add(new_message)
        db.session.commit()
        new_blast.pending = Message.query.filter_by(id=new_blast.id,status='pending').count()
        db.session.commit()
    return new_blast.id

# def send_messages(message_id):
#     batch = Blast.query.filter_by(id=message_id).first()
#     messages = Message.query.filter_by(blast_id=message_id).all()

#     for message in messages:

#         message_options = {
#             'app_id': APP_ID,
#             'app_secret': APP_SECRET,
#             'message': message.content,
#             'address': message.msisdn,
#             'passphrase': PASSPHRASE,
#         }

#         try:
#             r = requests.post(IPP_URL,message_options)           
#             if r.status_code == 201:
#                 message.status = 'success'
#                 message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
#                 db.session.commit()

#             elif r.json()['error'] == 'Invalid address.':
#                 message.status = 'invalid address'
#                 message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
#                 db.session.commit()

#             else:
#                 message.status = 'failed'
#                 message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
#                 db.session.commit()

#         except requests.exceptions.ConnectionError as e:
#             message.status = 'failed'
#             message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
#             db.session.commit()
        
#         batch.done = Message.query.filter_by(blast_id=message_id,status='success').count()
#         batch.pending = Message.query.filter_by(blast_id=message_id,status='pending').count()
#         batch.failed = Message.query.filter_by(blast_id=message_id,status='failed').count()
#         db.session.commit()

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)

def authenticate_user(email, password):
    user = AdminUser.query.filter_by(email=email,password=password).first()
    if not user or user == None:
        return jsonify(status='failed', error='Invalid email or password')
    if user.status != 'Active':
        return jsonify(status='failed', error='Your account has been deactivated')
    session['user_id'] = user.id
    session['user_name'] = user.name
    return jsonify(status='success', error=''),200


@app.route('/', methods=['GET', 'POST'])
@nocache
def dashboard():
    if not session:
        return redirect('/login')
    return flask.render_template('index.html',user_name=session['user_name'])


@app.route('/login', methods=['GET', 'POST'])
@nocache
def login():
    if session:
        return redirect('/')
    return flask.render_template('login.html')


@app.route('/user/authenticate', methods=['GET', 'POST'])
@nocache
def authenticate():
    if session:
        return redirect('/')
    login_data = flask.request.form.to_dict()
    return authenticate_user(login_data['user_email'], login_data['user_password'])


@app.route('/logout', methods=['GET', 'POST'])
@nocache
def logout():
    session.clear()
    return redirect('/login')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = flask.request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    message_id = compose_messages(file.filename)
    send_messages.delay(message_id)
    batch = Blast.query.filter_by(id=message_id).first()
    return flask.render_template('poc_status.html', batch=batch),201


@app.route('/db/rebuild', methods=['GET', 'POST'])
def rebuild_database():
    db.drop_all()
    db.create_all()
    admin_user = AdminUser(
        email = 'ballesteros.alan@gmail.com',
        password = 'password',
        name = 'Alan Ballesteros',
        added_by_id = None,
        added_by_name = None,
        join_date = time.strftime("%B %d, %Y"),
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )
    db.session.add(admin_user)
    db.session.commit()
    return jsonify(status='success'),201


if __name__ == '__main__':
    app.run(port=8000,debug=True,host='0.0.0.0')
    # port=int(os.environ['PORT']), host='0.0.0.0'