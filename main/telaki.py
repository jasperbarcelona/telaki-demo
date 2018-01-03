import flask, flask.views
from flask import url_for, request, session, redirect, jsonify, Response, make_response, current_app
from jinja2 import environment, FileSystemLoader
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean
from sqlalchemy import or_
from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import Admin, BaseView, expose
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
import schedule
from werkzeug.utils import secure_filename
from tasks import blast_sms, send_reminders, upload_contacts
import db_conn
from db_conn import db, app
from models import *
import xlrd

IPP_URL = 'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/%s/requests'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])
UPLOAD_FOLDER = 'static/records'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class IngAdmin(sqla.ModelView):
    column_display_pk = True

class SchoolAdmin(sqla.ModelView):
    column_display_pk = True
    column_include_list = ['api_key', 'name', 'url', 'address', 'city', 'email', 'tel']

class StudentAdmin(sqla.ModelView):
    column_display_pk = True
    column_searchable_list = ['first_name', 'last_name', 'middle_name', 'id_no']

admin = Admin(app, name='raven')
admin.add_view(SchoolAdmin(Client, db.session))
admin.add_view(SchoolAdmin(AdminUser, db.session))
admin.add_view(SchoolAdmin(Contact, db.session))
admin.add_view(SchoolAdmin(Batch, db.session))
admin.add_view(SchoolAdmin(ReminderBatch, db.session))
admin.add_view(SchoolAdmin(OutboundMessage, db.session))
admin.add_view(SchoolAdmin(ReminderMessage, db.session))
admin.add_view(SchoolAdmin(Conversation, db.session))
admin.add_view(SchoolAdmin(ConversationItem, db.session))
admin.add_view(SchoolAdmin(Group, db.session))
admin.add_view(SchoolAdmin(ContactGroup, db.session))

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET','POST'])
@nocache
def index():
    if not session:
        return redirect('/login')
    session['conversation_limit'] = 50
    total_entries = Conversation.query.filter_by(client_no=session['client_no']).count()
    conversations = Conversation.query.filter_by(client_no=session['client_no']).order_by(Conversation.created_at.desc()).slice(session['conversation_limit'] - 50, session['conversation_limit'])
    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name)
    contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name)
    if total_entries < 50:
        return flask.render_template(
        'index.html',
        client_name=session['client_name'],
        user_name=session['user_name'],
        conversations=conversations,
        groups=groups,
        contacts=contacts,
        limit=total_entries,
        total_entries=total_entries,
        prev_btn='disabled',
        next_btn='disabled',
    )
    return flask.render_template(
        'index.html',
        client_name=session['client_name'],
        user_name=session['user_name'],
        conversations=conversations,
        groups=groups,
        contacts=contacts,
        limit=session['conversation_limit'],
        total_entries=total_entries,
        prev_btn='disabled',
        next_btn='enabled',
    )


@app.route('/login',methods=['GET','POST'])
@nocache
def login_page():
    if session:
        return redirect('/')
    return flask.render_template('login.html')


@app.route('/user/authenticate',methods=['GET','POST'])
def authenticate_user():
    data = flask.request.form.to_dict()
    client = Client.query.filter_by(client_no=data['client_no']).first()
    if not client or client == None:
        return jsonify(status='failed', error='Invalid client number.')
    user = AdminUser.query.filter_by(email=data['user_email'],password=data['user_password']).first()
    if not user or user == None:
        return jsonify(status='failed', error='Invalid email or password.')
    if user.client_no != client.client_no:
        return jsonify(status='failed', error='Not authorized.')
    if user.status != 'Active':
        return jsonify(status='failed', error='Your account has been deactivated.')
    session['user_name'] = user.name
    session['user_id'] = user.id
    session['client_no'] = client.client_no
    session['client_name'] = client.name
    return jsonify(status='success', error=''),200


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/login')


@app.route('/conversations',methods=['GET','POST'])
def all_conversations():
    slice_from = flask.request.args.get('slice_from')
    prev_btn = 'enabled'
    if slice_from == 'reset':
        session['conversation_limit'] = 50
        prev_btn = 'disabled'
    total_entries = Conversation.query.filter_by(client_no=session['client_no']).count()
    conversations = Conversation.query.filter_by(client_no=session['client_no']).order_by(Conversation.created_at.desc()).slice(session['conversation_limit'] - 50, session['conversation_limit'])
    if total_entries < 50:
        showing='1 - %s' % total_entries
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['conversation_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['conversation_limit'] - 49),str(session['conversation_limit']))
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['conversation_limit'] - 49),str((session['conversation_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return flask.render_template(
        'conversations.html',
        conversations=conversations,
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
    )


@app.route('/conversations/next',methods=['GET','POST'])
def next_conversations():
    session['conversation_limit'] += 50
    total_entries = Conversation.query.filter_by(client_no=session['client_no']).count()
    conversations = Conversation.query.filter_by(client_no=session['client_no']).order_by(Conversation.created_at.desc()).slice(session['conversation_limit'] - 50, session['conversation_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['conversation_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['conversation_limit'] - 49),str(session['conversation_limit']))
            prev_btn = 'enabled'
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['conversation_limit'] - 49),str((session['conversation_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'conversations_result.html',
            conversations=conversations)
        )


@app.route('/conversations/prev',methods=['GET','POST'])
def prev_conversations():
    session['conversation_limit'] -= 50
    total_entries = Conversation.query.filter_by(client_no=session['client_no']).count()
    conversations = Conversation.query.filter_by(client_no=session['client_no']).order_by(Conversation.created_at.desc()).slice(session['conversation_limit'] - 50, session['conversation_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        showing = '%s - %s' % (str(session['conversation_limit'] - 49),str(session['conversation_limit']))
        if session['conversation_limit'] <= 50:
            prev_btn = 'disabled'
            next_btn='enabled'
        else:
            prev_btn = 'enabled'
            next_btn='enabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'conversations_result.html',
            conversations=conversations)
        )


@app.route('/blasts',methods=['GET','POST'])
def all_blasts():
    slice_from = flask.request.args.get('slice_from')
    prev_btn = 'enabled'
    if slice_from == 'reset':
        session['blast_limit'] = 50
        prev_btn = 'disabled'
    total_entries = Batch.query.filter_by(client_no=session['client_no']).count()
    blasts = Batch.query.filter_by(client_no=session['client_no']).order_by(Batch.created_at.desc()).slice(session['blast_limit'] - 50, session['blast_limit'])
    if total_entries < 50:
        showing='1 - %s' % total_entries
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['blast_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['blast_limit'] - 49),str(session['blast_limit']))
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['blast_limit'] - 49),str((session['blast_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return flask.render_template(
        'blasts.html',
        blasts=blasts,
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
    )


@app.route('/blast',methods=['GET','POST'])
def get_blast():
    batch_id = flask.request.args.get('batch_id')
    batch = Batch.query.filter_by(id=batch_id).first()
    success = OutboundMessage.query.filter_by(batch_id=batch_id, status='success').all()
    failed = OutboundMessage.query.filter_by(batch_id=batch_id, status='failed').all()
    return flask.render_template('blast_info.html',batch=batch,success=success,failed=failed)


@app.route('/blasts/next',methods=['GET','POST'])
def next_blasts():
    session['blast_limit'] += 50
    total_entries = Batch.query.filter_by(client_no=session['client_no']).count()
    blasts = Batch.query.filter_by(client_no=session['client_no']).order_by(Batch.created_at.desc()).slice(session['blast_limit'] - 50, session['blast_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['blast_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['blast_limit'] - 49),str(session['blast_limit']))
            prev_btn = 'enabled'
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['blast_limit'] - 49),str((session['blast_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'blasts_result.html',
            blasts=blasts)
        )


@app.route('/blasts/prev',methods=['GET','POST'])
def prev_blasts():
    session['blast_limit'] -= 50
    total_entries = Batch.query.filter_by(client_no=session['client_no']).count()
    blasts = Batch.query.filter_by(client_no=session['client_no']).order_by(Batch.created_at.desc()).slice(session['blast_limit'] - 50, session['blast_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        showing = '%s - %s' % (str(session['blast_limit'] - 49),str(session['blast_limit']))
        if session['blast_limit'] <= 50:
            prev_btn = 'disabled'
            next_btn='enabled'
        else:
            prev_btn = 'enabled'
            next_btn='enabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'blasts_result.html',
            blasts=blasts)
        )


@app.route('/reminders',methods=['GET','POST'])
def payment_reminders():
    slice_from = flask.request.args.get('slice_from')
    prev_btn = 'enabled'
    if slice_from == 'reset':
        session['reminder_limit'] = 50
        prev_btn = 'disabled'
    total_entries = ReminderBatch.query.filter_by(client_no=session['client_no']).count()
    reminders = ReminderBatch.query.filter_by(client_no=session['client_no']).order_by(ReminderBatch.created_at.desc()).slice(session['reminder_limit'] - 50, session['reminder_limit'])
    if total_entries < 50:
        showing='1 - %s' % total_entries
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['reminder_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['reminder_limit'] - 49),str(session['reminder_limit']))
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['reminder_limit'] - 49),str((session['reminder_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return flask.render_template(
        'reminders.html',
        reminders=reminders,
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
    )


@app.route('/reminder',methods=['GET','POST'])
def view_reminder():
    reminder_id = flask.request.args.get('reminder_id')
    reminder = ReminderBatch.query.filter_by(id=reminder_id).first()
    file_loc = '%s/%s' % (UPLOAD_FOLDER, reminder.file_name)
    success = ReminderMessage.query.filter_by(batch_id=reminder.id,status='success')
    failed = ReminderMessage.query.filter_by(batch_id=reminder.id,status='failed')
    return flask.render_template('view_reminder.html', file_loc=file_loc, batch=reminder, success=success, failed=failed)


@app.route('/reminders/next',methods=['GET','POST'])
def next_reminders():
    session['reminder_limit'] += 50
    total_entries = ReminderBatch.query.filter_by(client_no=session['client_no']).count()
    reminders = ReminderBatch.query.filter_by(client_no=session['client_no']).order_by(ReminderBatch.created_at.desc()).slice(session['reminder_limit'] - 50, session['reminder_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['reminder_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['reminder_limit'] - 49),str(session['reminder_limit']))
            prev_btn = 'enabled'
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['reminder_limit'] - 49),str((session['reminder_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'reminders_result.html',
            reminders=reminders)
        )


@app.route('/reminders/prev',methods=['GET','POST'])
def prev_reminders():
    session['reminder_limit'] -= 50
    total_entries = ReminderBatch.query.filter_by(client_no=session['client_no']).count()
    reminders = ReminderBatch.query.filter_by(client_no=session['client_no']).order_by(ReminderBatch.created_at.desc()).slice(session['reminder_limit'] - 50, session['reminder_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        showing = '%s - %s' % (str(session['reminder_limit'] - 49),str(session['reminder_limit']))
        if session['reminder_limit'] <= 50:
            prev_btn = 'disabled'
            next_btn='enabled'
        else:
            prev_btn = 'enabled'
            next_btn='enabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'reminders_result.html',
            reminders=reminders)
        )


@app.route('/contacts',methods=['GET','POST'])
def contacts():
    slice_from = flask.request.args.get('slice_from')
    prev_btn = 'enabled'
    if slice_from == 'reset':
        session['contact_limit'] = 50
        prev_btn = 'disabled'
    total_entries = Contact.query.filter_by(client_no=session['client_no']).count()
    contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name).slice(session['contact_limit'] - 50, session['contact_limit'])
    if total_entries < 50:
        showing='1 - %s' % total_entries
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['contact_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['contact_limit'] - 49),str(session['contact_limit']))
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['contact_limit'] - 49),str((session['contact_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return flask.render_template(
        'contacts.html',
        contacts=contacts,
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
    )


@app.route('/contacts/next',methods=['GET','POST'])
def next_contacts():
    session['contact_limit'] += 50
    total_entries = Contact.query.filter_by(client_no=session['client_no']).count()
    contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name).slice(session['contact_limit'] - 50, session['contact_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['contact_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['contact_limit'] - 49),str(session['contact_limit']))
            prev_btn = 'enabled'
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['contact_limit'] - 49),str((session['contact_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'contacts_result.html',
            contacts=contacts)
        )


@app.route('/contacts/prev',methods=['GET','POST'])
def prev_contacts():
    session['contact_limit'] -= 50
    total_entries = Contact.query.filter_by(client_no=session['client_no']).count()
    contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name).slice(session['contact_limit'] - 50, session['contact_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        showing = '%s - %s' % (str(session['contact_limit'] - 49),str(session['contact_limit']))
        if session['contact_limit'] <= 50:
            prev_btn = 'disabled'
            next_btn='enabled'
        else:
            prev_btn = 'enabled'
            next_btn='enabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'contacts_result.html',
            contacts=contacts)
        )


@app.route('/groups',methods=['GET','POST'])
def groups():
    slice_from = flask.request.args.get('slice_from')
    prev_btn = 'enabled'
    if slice_from == 'reset':
        session['group_limit'] = 50
        prev_btn = 'disabled'
    total_entries = Group.query.filter_by(client_no=session['client_no']).count()
    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name).slice(session['group_limit'] - 50, session['group_limit'])
    if total_entries < 50:
        showing='1 - %s' % total_entries
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['group_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['group_limit'] - 49),str(session['group_limit']))
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['group_limit'] - 49),str((session['group_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return flask.render_template(
        'groups.html',
        groups=groups,
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
    )


@app.route('/groups/next',methods=['GET','POST'])
def next_groups():
    session['group_limit'] += 50
    total_entries = Group.query.filter_by(client_no=session['client_no']).count()
    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name).slice(session['group_limit'] - 50, session['group_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['group_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['group_limit'] - 49),str(session['group_limit']))
            prev_btn = 'enabled'
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['group_limit'] - 49),str((session['group_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'groups_result.html',
            groups=groups)
        )


@app.route('/groups/prev',methods=['GET','POST'])
def prev_groups():
    session['group_limit'] -= 50
    total_entries = Group.query.filter_by(client_no=session['client_no']).count()
    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name).slice(session['group_limit'] - 50, session['group_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        showing = '%s - %s' % (str(session['group_limit'] - 49),str(session['group_limit']))
        if session['group_limit'] <= 50:
            prev_btn = 'disabled'
            next_btn='enabled'
        else:
            prev_btn = 'enabled'
            next_btn='enabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'groups_result.html',
            groups=groups)
        )


@app.route('/groups/save',methods=['GET','POST'])
def add_group():
    name = flask.request.form.get('name')
    exists = Group.query.filter_by(name=name).first()
    if exists or exists != None:
        return jsonify(
            status='error',
            message='Duplicate group name.'
            )
    new_group = Group(
        client_no=session['client_no'],
        name=name,
        created_by_id=session['user_id'],
        created_by_name=session['user_name'],
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )
    db.session.add(new_group)
    db.session.commit()
    prev_btn = 'enabled'
    total_entries = Group.query.filter_by(client_no=session['client_no']).count()
    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name).slice(session['group_limit'] - 50, session['group_limit'])
    if total_entries < 50:
        showing='1 - %s' % total_entries
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['group_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['group_limit'] - 49),str(session['group_limit']))
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['group_limit'] - 49),str((session['group_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return jsonify(
        status='success',
        template=flask.render_template(
                'groups.html',
                groups=groups,
                showing=showing,
                total_entries=total_entries,
                prev_btn=prev_btn,
                next_btn=next_btn,
            )
        )


@app.route('/contacts/upload', methods=['GET', 'POST'])
def prepare_contacts_upload():
    file = flask.request.files['contactsFile']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if file and allowed_file(file.filename):
        path = '%s/%s' % (UPLOAD_FOLDER, filename)
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        rows = sheet.nrows;
        cols = 3

        new_contact_upload = ContactBatch(
            client_no=session['client_no'],
            uploader_id=session['user_id'],
            uploader_name=session['user_name'],
            batch_size=rows,
            date=datetime.datetime.now().strftime('%B %d, %Y'),
            time=time.strftime("%I:%M %p"),
            file_name=filename,
            created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
        db.session.add(new_contact_upload)
        db.session.commit()

        upload_contacts.delay(new_contact_upload.id, session['client_no'],session['user_id'], session['user_name'])      

        existing = Contact.query.filter_by(batch_id=str(new_contact_upload.id)).count()
        new_contact_upload.pending = new_contact_upload.batch_size - existing
        db.session.commit()

        return jsonify(
            status='success',
            pending=new_contact_upload.pending,
            batch_id=new_contact_upload.id,
            template=flask.render_template('contact_upload_status.html', batch=new_contact_upload)
            )

    return jsonify(
        status = 'failed',
        message = 'Invalid file.'
        )


@app.route('/reminder/upload', methods=['GET', 'POST'])
def upload_file():
    file = flask.request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if file and allowed_file(file.filename):
        path = '%s/%s' % (UPLOAD_FOLDER, filename)
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        rows = sheet.nrows;
        cols = 2
        new_reminder = ReminderBatch(
            client_no=session['client_no'],
            sender_id=session['user_id'],
            batch_size=rows,
            sender_name=session['user_name'],
            date=datetime.datetime.now().strftime('%B %d, %Y'),
            time=time.strftime("%I:%M %p"),
            file_name=filename,
            created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
        db.session.add(new_reminder)
        db.session.commit()

        for row in range(rows):
            vals = []
            for col in range(cols):
                cell = sheet.cell(row,col)
                if cell.value == '':
                    vals.append(None)
                else:
                    vals.append(cell.value)

            contact = Contact.query.filter_by(msisdn='0%s'%vals[0][-10:]).first()
            if contact or contact != None:
                new_message = ReminderMessage(
                    batch_id=new_reminder.id,
                    contact_name=contact.name,
                    msisdn=contact.msisdn,
                    content=vals[1],
                    date=new_reminder.date,
                    time=new_reminder.time,
                    )
            else:
                new_message = ReminderMessage(
                    batch_id=new_reminder.id,
                    msisdn='0%s'%vals[0][-10:],
                    content=vals[1],
                    date=new_reminder.date,
                    time=new_reminder.time,
                    )
            db.session.add(new_message)
            db.session.commit()
            new_reminder.pending = ReminderMessage.query.filter_by(batch_id=new_reminder.id,status='pending').count()
            db.session.commit()

        send_reminders.delay(new_reminder.id,new_reminder.date,new_reminder.time,session['client_no'])

        return jsonify(
            status='success',
            pending=new_reminder.pending,
            batch_id=new_reminder.id,
            template=flask.render_template('reminder_status.html', batch=new_reminder)
            )

        # prev_btn = 'enabled'
        # total_entries = ReminderBatch.query.filter_by(client_no=session['client_no']).count()
        # reminders = ReminderBatch.query.filter_by(client_no=session['client_no']).order_by(ReminderBatch.created_at.desc()).slice(session['reminder_limit'] - 50, session['reminder_limit'])
        # if total_entries < 50:
        #     showing='1 - %s' % total_entries
        #     prev_btn = 'disabled'
        #     next_btn='disabled'
        # else:
        #     diff = total_entries - (session['reminder_limit'] - 50)
        #     if diff > 50:
        #         showing = '%s - %s' % (str(session['reminder_limit'] - 49),str(session['reminder_limit']))
        #         next_btn='enabled'
        #     else:
        #         showing = '%s - %s' % (str(session['reminder_limit'] - 49),str((session['reminder_limit']-50)+diff))
        #         prev_btn = 'enabled'
        #         next_btn='disabled'

        # return jsonify(
        #     status='success',
        #     template=flask.render_template(
        #             'reminders.html',
        #             reminders=reminders,
        #             showing=showing,
        #             total_entries=total_entries,
        #             prev_btn=prev_btn,
        #             next_btn=next_btn
        #         )
        #     )

    return jsonify(
        status = 'failed',
        message = 'Invalid file.'
        )


@app.route('/progress/existing',methods=['GET','POST'])
def check_existing_progress():
    blast = Batch.query.filter(Batch.sender_id==session['user_id'],Batch.pending!=0).first()
    if blast or blast != None:
        return jsonify(
            in_progress='blast',
            pending=blast.pending,
            batch_id=blast.id,
            template=flask.render_template('blast_status.html', batch=blast)
            )
    reminder = ReminderBatch.query.filter(ReminderBatch.sender_id==session['user_id'],ReminderBatch.pending!=0).first()
    if reminder or reminder != None:
        return jsonify(
            in_progress='reminder',
            pending=reminder.pending,
            batch_id=reminder.id,
            template=flask.render_template('reminder_status.html', batch=reminder)
            )
    return jsonify(in_progress='none')



@app.route('/conversation',methods=['GET','POST'])
def open_conversation():
    conversation_id = flask.request.args.get('conversation_id')
    session['conversation_id'] = conversation_id
    conversation = Conversation.query.filter_by(id=conversation_id).first()
    if conversation.status == 'unread':
        conversation.status = 'read'
        db.session.commit()
    messages = ConversationItem.query.filter_by(conversation_id=conversation_id).order_by(ConversationItem.created_at)
    return flask.render_template(
        'conversation.html',
        conversation=conversation,
        messages=messages 
        ),200


@app.route('/conversation/reply',methods=['GET','POST'])
def send_reply():
    message_content = flask.request.form.get('content')
    conversation = Conversation.query.filter_by(id=session['conversation_id']).first()
    client = Client.query.filter_by(client_no=session['client_no']).first()
    message_options = {
        'app_id': client.app_id,
        'app_secret': client.app_secret,
        'message': message_content,
        'address': conversation.msisdn,
        'passphrase': client.passphrase,
    }
    try:
        r = requests.post(IPP_URL%client.shortcode,message_options)
        if r.status_code != 201:
            return jsonify(status='failed')

        reply = ConversationItem(
            conversation_id=conversation.id,
            message_type='outbound',
            date=datetime.datetime.now().strftime('%B %d, %Y'),
            time=time.strftime("%I:%M %p"),
            content=message_content,
            outbound_sender_id=session['user_id'],
            outbound_sender_name=session['user_name'],
            created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
        db.session.add(reply)
        db.session.commit()
        conversation.latest_content = message_content
        conversation.latest_date = reply.date
        conversation.latest_time = reply.time
        db.session.commit()
        return jsonify(
            status='success',
            template=flask.render_template(
                'reply.html',
                conversation=conversation,
                message=reply 
                )
            )   
    except requests.exceptions.ConnectionError as e:
        return jsonify(status='failed')


@app.route('/contact/edit',methods=['GET','POST'])
def edit_contact():
    data = flask.request.form.to_dict()
    groups = flask.request.form.getlist('groups[]')
    contact = Contact.query.filter_by(msisdn=session['contact_msisdn']).first()
    contact.name = data['name'].title()
    contact.contact_type = data['contact_type']
    contact.msisdn = '0%s'%data['msisdn'][-10:]

    existing_contact_groups = ContactGroup.query.filter_by(contact_id=contact.id).delete()

    for item in groups:
        group = Group.query.filter_by(id=int(item)).first()
        contact_group = ContactGroup(
            contact_id = contact.id,
            group_id = int(item)
            )
        db.session.add(contact_group)
        group_size = ContactGroup.query.filter_by(group_id=int(item)).count()
        group.size = group_size

    conversation = Conversation.query.filter_by(msisdn=data['msisdn']).first()
    if conversation or conversation != None:
        conversation.contact_name = data['name'].title()

    db.session.commit()

    if data['type'] == 'from_convo':
        messages = ConversationItem.query.filter_by(conversation_id=conversation.id).order_by(ConversationItem.created_at)
        return flask.render_template(
            'conversation.html',
            conversation=conversation,
            messages=messages 
            ),201

    if session['contact_msisdn'] != data['msisdn']:
        old_conversation = Conversation.query.filter_by(msisdn=session['contact_msisdn']).first()
        if old_conversation or old_conversation != None:
            old_conversation.contact_name = None
            db.session.commit()

    total_entries = Contact.query.filter_by(client_no=session['client_no']).count()
    contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name).slice(session['contact_limit'] - 50, session['contact_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['contact_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['contact_limit'] - 49),str(session['contact_limit']))
            prev_btn = 'enabled'
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['contact_limit'] - 49),str((session['contact_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return flask.render_template(
            'contacts.html',
            contacts=contacts,
            showing=showing,
            total_entries=total_entries,
            prev_btn=prev_btn,
            next_btn=next_btn
            ),201


@app.route('/contact/save',methods=['GET','POST'])
def save_contact():
    data = flask.request.form.to_dict()
    groups = flask.request.form.getlist('groups[]')
    new_contact = Contact(
        client_no=session['client_no'],
        contact_type=data['contact_type'].title(),
        name=data['name'].title(),
        msisdn='0%s'%data['msisdn'][-10:],
        added_by=session['user_id'],
        added_by_name=session['user_name'],
        join_date=datetime.datetime.now().strftime('%B %d, %Y'),
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    db.session.add(new_contact)
    db.session.commit()

    for item in groups:
        group = Group.query.filter_by(id=int(item)).first()
        contact_group = ContactGroup(
            contact_id = new_contact.id,
            group_id = int(item)
            )
        db.session.add(contact_group)
        group_size = ContactGroup.query.filter_by(group_id=int(item)).count()
        group.size = group_size
    
    conversation = Conversation.query.filter_by(msisdn=data['msisdn']).first()
    if conversation or conversation != None:
        conversation.contact_name = data['name'].title()

    db.session.commit()

    if data['type'] == 'save':
        messages = ConversationItem.query.filter_by(conversation_id=conversation.id).order_by(ConversationItem.created_at)
        return flask.render_template(
            'conversation.html',
            conversation=conversation,
            messages=messages 
            ),201
    prev_btn='enabled'
    total_entries = Contact.query.filter_by(client_no=session['client_no']).count()
    contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name).slice(session['contact_limit'] - 50, session['contact_limit'])
    if total_entries < 50:
        showing='1 - %s' % total_entries
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['contact_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['contact_limit'] - 49),str(session['contact_limit']))
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['contact_limit'] - 49),str((session['contact_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return flask.render_template(
        'contacts.html',
        contacts=contacts,
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
    )


@app.route('/contact',methods=['GET','POST'])
def get_contact_info():
    data = flask.request.args.to_dict()
    session['contact_msisdn'] = data['msisdn']
    contact = Contact.query.filter_by(msisdn=data['msisdn']).first()
    contact_groups = [r.group_id for r in db.session.query(ContactGroup.group_id).filter_by(contact_id=contact.id).all()]
    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name)

    return flask.render_template(
        'contact_info.html',
        type=data['type'],
        contact=contact,
        groups=groups,
        contact_groups=contact_groups
        ),200


@app.route('/recipients/add', methods=['GET', 'POST'])
def add_recipients():
    individual_recipients_name = flask.request.form.getlist('individual_recipients_name[]')
    group_recipients_name = flask.request.form.getlist('group_recipients_name[]')
    return flask.render_template(
        'recipients.html',
        individual_recipients=individual_recipients_name,
        group_recipients=group_recipients_name,
        )


@app.route('/blast/send', methods=['GET', 'POST'])
def send_text_blast():
    group_recipient_ids = flask.request.form.getlist('group_recipients[]')
    individual_recipient_ids = flask.request.form.getlist('individual_recipients[]')
    individual_recipients_name = flask.request.form.getlist('individual_recipients_name[]')
    group_recipients_name = flask.request.form.getlist('group_recipients_name[]')
    data = flask.request.form.to_dict()
    new_batch = Batch(
        client_no=session['client_no'],
        message_type='custom',
        sender_id=session['user_id'],
        sender_name=session['user_name'],
        recipient=', '.join(group_recipients_name+individual_recipients_name),
        date=datetime.datetime.now().strftime('%B %d, %Y'),
        time=time.strftime("%I:%M %p"),
        content=data['content'],
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )
    db.session.add(new_batch)
    db.session.commit()

    for group_id in group_recipient_ids:
        contact_group = ContactGroup.query.filter_by(group_id=group_id).all()
        for item in contact_group:
            contact = Contact.query.filter_by(id=item.contact_id).first()
            in_list = OutboundMessage.query.filter_by(batch_id=new_batch.id,msisdn=contact.msisdn).first()
            if not in_list or in_list == None:
                new_message = OutboundMessage(
                    batch_id=new_batch.id,
                    date=new_batch.date,
                    time=new_batch.time,
                    contact_name=contact.name,
                    msisdn=contact.msisdn
                    )
                db.session.add(new_message)
        db.session.commit()

    for individual_id in individual_recipient_ids:
        contact = Contact.query.filter_by(id=individual_id).first()
        in_list = OutboundMessage.query.filter_by(batch_id=new_batch.id,msisdn=contact.msisdn).first()
        if not in_list or in_list == None:
            new_message = OutboundMessage(
                batch_id=new_batch.id,
                date=new_batch.date,
                time=new_batch.time,
                contact_name=contact.name,
                msisdn=contact.msisdn
                )
            db.session.add(new_message)
    db.session.commit()

    new_batch.batch_size = OutboundMessage.query.filter_by(batch_id=new_batch.id).count()
    new_batch.pending = OutboundMessage.query.filter_by(batch_id=new_batch.id,status='pending').count()
    db.session.commit()

    blast_sms.delay(new_batch.id,new_batch.date,new_batch.time,data['content'],session['client_no'])
    return jsonify(
        pending=new_batch.pending,
        batch_id=new_batch.id,
        template=flask.render_template('blast_status.html', batch=new_batch)
        )

    # total_entries = Batch.query.filter_by(client_no=session['client_no']).count()
    # blasts = Batch.query.filter_by(client_no=session['client_no']).order_by(Batch.created_at.desc()).slice(session['blast_limit'] - 50, session['blast_limit'])
    # prev_btn = 'enabled'
    # if total_entries < 50:
    #     showing='1 - %s' % total_entries
    #     prev_btn = 'disabled'
    #     next_btn='disabled'
    # else:
    #     diff = total_entries - (session['blast_limit'] - 50)
    #     if diff > 50:
    #         showing = '%s - %s' % (str(session['blast_limit'] - 49),str(session['blast_limit']))
    #         next_btn='enabled'
    #     else:
    #         showing = '%s - %s' % (str(session['blast_limit'] - 49),str((session['blast_limit']-50)+diff))
    #         prev_btn = 'enabled'
    #         next_btn='disabled'
    # return flask.render_template(
    #     'blasts.html',
    #     blasts=blasts,
    #     showing=showing,
    #     total_entries=total_entries,
    #     prev_btn=prev_btn,
    #     next_btn=next_btn,
    # )


@app.route('/blast/progress', methods=['GET', 'POST'])
def get_blast_progress():
    batch_id = flask.request.form.get('batch_id')
    batch = Batch.query.filter_by(id=batch_id).first()
    return jsonify(
        pending=batch.pending,
        template=flask.render_template('blast_status.html', batch=batch)
        )


@app.route('/reminder/progress', methods=['GET', 'POST'])
def get_reminder_progress():
    batch_id = flask.request.form.get('batch_id')
    batch = ReminderBatch.query.filter_by(id=batch_id).first()
    return jsonify(
        pending=batch.pending,
        template=flask.render_template('reminder_status.html', batch=batch)
        )


@app.route('/contacts/progress', methods=['GET', 'POST'])
def get_contact_upload_progress():
    batch_id = flask.request.form.get('batch_id')
    batch = ContactBatch.query.filter_by(id=batch_id).first()
    return jsonify(
        pending=batch.pending,
        template=flask.render_template('contact_upload_status.html', batch=batch)
        )


@app.route('/blast/summary', methods=['GET', 'POST'])
def display_blast_summary():
    batch_id = flask.request.form.get('batch_id')
    batch = Batch.query.filter_by(id=batch_id).first()
    return flask.render_template('blast_report.html', batch=batch)


@app.route('/reminder/summary', methods=['GET', 'POST'])
def display_reminder_summary():
    batch_id = flask.request.form.get('batch_id')
    batch = ReminderBatch.query.filter_by(id=batch_id).first()
    return flask.render_template('reminder_report.html', batch=batch)


@app.route('/contacts/summary', methods=['GET', 'POST'])
def display_contact_upload_summary():
    batch_id = flask.request.form.get('batch_id')
    batch = ContactBatch.query.filter_by(id=batch_id).first()
    return flask.render_template('contact_report.html', batch=batch)


@app.route('/db/rebuild',methods=['GET','POST'])
def rebuild_database():
    db.drop_all()
    db.create_all()

    client = Client(
        client_no='at-ic2017',
        name='Alson\'s Trading',
        app_id='MEoztReRyeHzaiXxaecR65HnqE98tz9g',
        app_secret='01c5d1f8d3bfa9966786065c5a2d829d7e84cf26fbfb4a47c91552cb7c091608',
        passphrase='PF5H8S9t7u',
        shortcode='21586853',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    client1 = Client(
        client_no='jm-ic2017',
        name='Jayson Marketing',
        app_id='x65gtry7b7u7oT5dAbi7oKudp6AptkGA',
        app_secret='72755ee33c36657daaa38a57a50728f8ef2b00189577a0f5fb432f8549386239',
        passphrase='PF5H8S9t7u',
        shortcode='21587460',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    admin = AdminUser(
        client_no='at-ic2017',
        email='hello@pisara.tech',
        password='ratmaxi8',
        name='Super Admin',
        join_date='November 14, 2017',
        added_by_name='None',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    admin1 = AdminUser(
        client_no='jm-ic2017',
        email='hello@pisara.tech',
        password='ratmaxi8',
        name='Super Admin',
        join_date='November 14, 2017',
        added_by_name='None',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    contact = Contact(
        client_no='at-ic2017',
        contact_type='Customer',
        name='ABAC, AILYN-AGN',
        msisdn='09994282203',
        added_by=1,
        added_by_name='Super Admin',
        join_date='November 14, 2017',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    conversations = Conversation(
        client_no='at-ic2017',
        contact_name='ABAC, AILYN-AGN'.title(),
        msisdn='09994282203',
        status='read',
        latest_content='This is a sample message.',
        latest_date='November 14, 2017',
        latest_time='11:36 AM',
        created_at='2017-11-14 11:36:49:270418',
        )

    conversations1 = Conversation(
        client_no='at-ic2017',
        msisdn='09176214704',
        status='unread',
        latest_content='This is another sample message.',
        latest_date='November 13, 2017',
        latest_time='12:23 PM',
        created_at='2017-11-13 12:23:49:270418',
        )

    message = ConversationItem(
        conversation_id=1,
        message_type='inbound',
        date='November 14, 2017',
        time='11:30 AM',
        content='This is another sample message.',
        created_at='2017-11-14 11:30:49:270418'
        )

    message2 = ConversationItem(
        conversation_id=2,
        message_type='inbound',
        date='November 13, 2017',
        time='12:10 PM',
        content='This is another sample message.',
        created_at='2017-11-13 12:10:49:270418'
        )

    blast = Batch(
        client_no='at-ic2017',
        message_type='custom',
        sender_id=1,
        batch_size=3,
        sender_name='Super Admin',
        recipient='AGN, ANB, JNC',
        date='November 14, 2017',
        time='07:36 AM',
        content='This is a sample text blast.',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        ) 

    reminder = ReminderBatch(
        client_no='at-ic2017',
        sender_id=1,
        batch_size=3,
        sender_name='Super Admin',
        date='November 14, 2017',
        time='11:36 AM',
        file_name='payment_reminders.xls',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    contact = Contact(
        client_no='at-ic2017',
        contact_type='Customer',
        name='ABAC, AILYN-AGN'.title(),
        msisdn='09994282203',
        added_by=1,
        added_by_name='Super Admin',
        join_date='November 10, 2017',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    contact1 = Contact(
        client_no='at-ic2017',
        contact_type='Customer',
        name='ABAD, LANDELINA ORCIGA-ANB'.title(),
        msisdn='09183132539',
        added_by=1,
        added_by_name='Super Admin',
        join_date='November 10, 2017',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    contact2 = Contact(
        client_no='at-ic2017',
        contact_type='Customer',
        name='ABAD, NELSON M.-JNC'.title(),
        msisdn='09071755339',
        added_by=1,
        added_by_name='Super Admin',
        join_date='November 10, 2017',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    new_group = Group(
        client_no='at-ic2017',
        name='AGN',
        size=1,
        created_by_id=1,
        created_by_name='Super Admin',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    new_group1 = Group(
        client_no='at-ic2017',
        name='ANB',
        size=1,
        created_by_id=1,
        created_by_name='Super Admin',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    new_group2 = Group(
        client_no='at-ic2017',
        name='JNC',
        size=1,
        created_by_id=1,
        created_by_name='Super Admin',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    contact_group = ContactGroup(
        group_id=1,
        user_id=1
        )

    contact_group1 = ContactGroup(
        group_id=2,
        user_id=2
        )

    contact_group2 = ContactGroup(
        group_id=3,
        user_id=3
        )
    
    db.session.add(client)
    db.session.add(client1)
    db.session.add(admin)
    db.session.add(admin1)
    db.session.add(contact)
    db.session.add(conversations)
    db.session.add(conversations1)
    db.session.add(message)
    db.session.add(message2)

    db.session.add(blast)
    db.session.add(reminder)
    db.session.add(contact)
    db.session.add(contact1)
    db.session.add(contact2)
    db.session.add(new_group)
    db.session.add(new_group1)
    db.session.add(new_group2)
    db.session.add(contact_group)
    db.session.add(contact_group1)
    db.session.add(contact_group2)

    db.session.commit()

    return jsonify(
        status = 'success'
        ), 201

if __name__ == '__main__':
    app.run(port=5000,debug=True,host='0.0.0.0')
    # port=int(os.environ['PORT']), host='0.0.0.0'