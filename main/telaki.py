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
ALSONS_APP_ID = 'MEoztReRyeHzaiXxaecR65HnqE98tz9g'
ALSONS_APP_SECRET = '01c5d1f8d3bfa9966786065c5a2d829d7e84cf26fbfb4a47c91552cb7c091608'
ALSONS_PASSPHRASE = 'PF5H8S9t7u'
ALSONS_SHORTCODE = '21586853'

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
admin.add_view(SchoolAdmin(ContactBatch, db.session))

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

def search_conversations(**kwargs):
    query = 'Conversation.query.filter(Conversation.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Conversation.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Conversation.created_at.desc())'
    return eval(query)

def search_conversations_count(**kwargs):
    query = 'Conversation.query.filter(Conversation.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Conversation.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').count()'
    return eval(query)

def search_blasts(**kwargs):
    query = 'Batch.query.filter(Batch.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Batch.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Batch.created_at.desc())'
    return eval(query)

def search_blasts_count(**kwargs):
    query = 'Batch.query.filter(Batch.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Batch.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').count()'
    return eval(query)

def search_reminders(**kwargs):
    query = 'ReminderBatch.query.filter(ReminderBatch.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'ReminderBatch.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(ReminderBatch.created_at.desc())'
    return eval(query)

def search_reminders_count(**kwargs):
    query = 'ReminderBatch.query.filter(ReminderBatch.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'ReminderBatch.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').count()'
    return eval(query)

def search_contacts(**kwargs):
    query = 'Contact.query.filter(Contact.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Contact.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Contact.name)'
    return eval(query)


def search_contacts_count(**kwargs):
    query = 'Contact.query.filter(Contact.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Contact.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').count()'
    return eval(query)

def search_users(**kwargs):
    query = 'AdminUser.query.filter(AdminUser.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'AdminUser.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(AdminUser.name)'
    return eval(query)

def search_users_count(**kwargs):
    query = 'AdminUser.query.filter(AdminUser.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'AdminUser.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').count()'
    return eval(query)

def search_groups(**kwargs):
    query = 'Group.query.filter(Group.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Group.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Group.name)'
    return eval(query)

def search_groups_count(**kwargs):
    query = 'Group.query.filter(Group.client_no.ilike("'+session['client_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Group.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').count()'
    return eval(query)


@app.route('/',methods=['GET','POST'])
@nocache
def index():
    if not session:
        return redirect('/login')
    session['conversation_limit'] = 50
    session['group_recipients'] = []
    session['individual_recipients'] = []
    session['group_recipients_name'] = []
    session['individual_recipients_name'] = []
    session['number_recipients'] = []
    total_entries = Conversation.query.filter_by(client_no=session['client_no']).count()
    conversations = Conversation.query.filter_by(client_no=session['client_no']).order_by(Conversation.created_at.desc()).slice(session['conversation_limit'] - 50, session['conversation_limit'])
    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name)
    contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name)
    contact_count = Contact.query.filter_by(client_no=session['client_no']).count()
    customers_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Customer').count()
    staff_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Staff').count()

    user = AdminUser.query.filter_by(id=session['user_id']).first()
    if user.password == user.temp_pw:
        change_pw = 'yes'
    else:
        change_pw = 'no'

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
        contact_count=contact_count,
        customers_count=customers_count,
        staff_count=staff_count,
        change_pw=change_pw
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
        contact_count=contact_count,
        customers_count=customers_count,
        staff_count=staff_count,
        change_pw=change_pw
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
    session['user_name'] = user.name
    session['user_id'] = user.id
    session['client_no'] = client.client_no
    session['client_name'] = client.name

    return jsonify(status='success', error=''),200


@app.route('/user/add',methods=['GET','POST'])
def add_user():
    data = flask.request.form.to_dict()

    new_user = AdminUser(
        client_no=session['client_no'],
        email=data['email'],
        password=data['temp_pw'],
        temp_pw=data['temp_pw'],
        name=data['name'].title(),
        role=data['role'],
        added_by_id=session['user_id'],
        added_by_name=session['user_name'],
        join_date=datetime.datetime.now().strftime('%B %d, %Y'),
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    db.session.add(new_user)
    db.session.commit()

    total_entries = AdminUser.query.filter_by(client_no=session['client_no']).count()
    users = AdminUser.query.filter_by(client_no=session['client_no']).order_by(AdminUser.name).slice(session['user_limit'] - 50, session['user_limit'])
    if total_entries < 50:
        showing='1 - %s' % total_entries
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['user_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['user_limit'] - 49),str(session['user_limit']))
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['user_limit'] - 49),str((session['user_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return flask.render_template(
        'users.html',
        users=users,
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
    )


@app.route('/user/password/save',methods=['GET','POST'])
def save_password():
    password = flask.request.form.get('password')
    user = AdminUser.query.filter_by(id=session['user_id']).first()
    user.password = password
    db.session.commit()
    return jsonify(status='success', message='')


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


@app.route('/users',methods=['GET','POST'])
def users():
    slice_from = flask.request.args.get('slice_from')
    prev_btn = 'enabled'
    if slice_from == 'reset':
        session['user_limit'] = 50
        prev_btn = 'disabled'
    total_entries = AdminUser.query.filter_by(client_no=session['client_no']).count()
    users = AdminUser.query.filter_by(client_no=session['client_no']).order_by(AdminUser.name).slice(session['user_limit'] - 50, session['user_limit'])
    if total_entries < 50:
        showing='1 - %s' % total_entries
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['user_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['user_limit'] - 49),str(session['user_limit']))
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['user_limit'] - 49),str((session['user_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return flask.render_template(
        'users.html',
        users=users,
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
    )


@app.route('/users/next',methods=['GET','POST'])
def next_users():
    session['user_limit'] += 50
    total_entries = AdminUser.query.filter_by(client_no=session['client_no']).count()
    users = AdminUser.query.filter_by(client_no=session['client_no']).order_by(AdminUser.name).slice(session['user_limit'] - 50, session['user_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        diff = total_entries - (session['user_limit'] - 50)
        if diff > 50:
            showing = '%s - %s' % (str(session['user_limit'] - 49),str(session['user_limit']))
            prev_btn = 'enabled'
            next_btn='enabled'
        else:
            showing = '%s - %s' % (str(session['user_limit'] - 49),str((session['user_limit']-50)+diff))
            prev_btn = 'enabled'
            next_btn='disabled'

    return jsonify(
        showing=showing,
        total_entries=total_entries,
        prev_btn=prev_btn,
        next_btn=next_btn,
        template=flask.render_template(
            'users_result.html',
            users=users)
        )


@app.route('/users/prev',methods=['GET','POST'])
def prev_users():
    session['user_limit'] -= 50
    total_entries = AdminUser.query.filter_by(client_no=session['client_no']).count()
    users = AdminUser.query.filter_by(client_no=session['client_no']).order_by(AdminUser.name).slice(session['user_limit'] - 50, session['user_limit'])
    if total_entries < 50:
        showing = '1 - %s' % str(total_entries)
        prev_btn = 'disabled'
        next_btn='disabled'
    else:
        showing = '%s - %s' % (str(session['user_limit'] - 49),str(session['user_limit']))
        if session['user_limit'] <= 50:
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
            'users_result.html',
            users=users)
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

    complete_groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name)
    contact_count = Contact.query.filter_by(client_no=session['client_no']).count()
    customers_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Customer').count()
    staff_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Staff').count()
    return jsonify(
        status='success',
        template=flask.render_template(
                'groups.html',
                groups=groups,
                showing=showing,
                total_entries=total_entries,
                prev_btn=prev_btn,
                next_btn=next_btn,
            ),
        group_template=flask.render_template('add_contact_groups.html',groups=complete_groups),
        recipient_template=flask.render_template(
            'group_recipients_refresh.html',
            groups=complete_groups,
            contact_count=contact_count,
            customers_count=customers_count,
            staff_count=staff_count,
            selected_groups=session['group_recipients']
            )
        )


@app.route('/recipients/groups/refresh', methods=['GET', 'POST'])
def refresh_group_recipients():
    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name)
    contact_count = Contact.query.filter_by(client_no=session['client_no']).count()
    customers_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Customer').count()
    staff_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Staff').count()
    return flask.render_template(
        'group_recipients_refresh.html',
        groups=groups,
        contact_count=contact_count,
        customers_count=customers_count,
        staff_count=staff_count,
        selected_groups=session['group_recipients']
        )


@app.route('/recipients/individual/refresh', methods=['GET', 'POST'])
def refresh_individual_recipients():
    contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name)
    return flask.render_template(
        'individual_recipients_refresh.html',
        contacts=contacts,
        selected_contacts=session['individual_recipients']
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
        msisdn_list = []
        for row in range(rows):
            repeated_msisdn = 0
            cell = sheet.cell(row,0)
            if cell.value in msisdn_list:
                repeated_msisdn += 1
            else:
                existing_contact = Contact.query.filter_by(msisdn='0%s'%str(cell.value)[-10:]).first()
                if existing_contact or existing_contact != None:
                    repeated_msisdn += 1
                else:
                    msisdn_list.append(cell.value)
            

        new_contact_upload = ContactBatch(
            client_no=session['client_no'],
            uploader_id=session['user_id'],
            uploader_name=session['user_name'],
            batch_size=rows - repeated_msisdn,
            date=datetime.datetime.now().strftime('%B %d, %Y'),
            time=time.strftime("%I:%M %p"),
            file_name=filename,
            created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
         
        db.session.add(new_contact_upload)
        db.session.commit()

        upload_contacts.delay(new_contact_upload.id,session['client_no'],session['user_id'],session['user_name'])      

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
    contact = ContactBatch.query.filter(ContactBatch.uploader_id==session['user_id'],ContactBatch.pending!=0).first()  
    if contact or contact != None:
        return jsonify(
            in_progress='contact',
            pending=contact.pending,
            batch_id=contact.id,
            template=flask.render_template('contact_upload_status.html', batch=contact)
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


@app.route('/conversation/receive',methods=['GET','POST'])
def receive_message():
    data = request.json['inboundSMSMessageList']['inboundSMSMessage'][0]
    contact = Contact.query.filter_by(msisdn='0%s'%data['senderAddress'][-10:]).first()
    conversation = Conversation.query.filter_by(msisdn='0%s'%data['senderAddress'][-10:]).first()
    if not conversation or conversation == None:
        if contact:
            conversation = Conversation(
                client_no='at-ic2017',
                contact_name=contact.name,
                msisdn=contact.msisdn,
                display_name=contact.name,
                )
        else:
            conversation = Conversation(
                client_no='at-ic2017',
                msisdn='0%s'%data['senderAddress'][-10:],
                display_name='0%s'%data['senderAddress'][-10:],
                )
        db.session.add(conversation)
        db.session.commit()

    message = ConversationItem(
        conversation_id=conversation.id,
        message_type='inbound',
        date=datetime.datetime.now().strftime('%B %d, %Y'),
        time=time.strftime("%I:%M %p"),
        content=data['message'],
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    db.session.add(message)
    db.session.commit()

    conversation.status='unread'
    conversation.latest_content=message.content
    conversation.latest_date=message.date
    conversation.latest_time=message.time
    conversation.created_at=message.created_at
    db.session.commit()

    content = 'Thank you for using our hotline. We will try to get back to you as soon as possible.'
    message_options = {
            'app_id': ALSONS_APP_ID,
            'app_secret': ALSONS_APP_SECRET,
            'message': content,
            'address': conversation.msisdn,
            'passphrase': ALSONS_PASSPHRASE,
        }
    r = requests.post(IPP_URL%ALSONS_SHORTCODE,message_options)  
    if r.status_code != 201:
        reply = ConversationItem(
            conversation_id=conversation.id,
            message_type='outbound',
            date=datetime.datetime.now().strftime('%B %d, %Y'),
            time=time.strftime("%I:%M %p"),
            content=content,
            outbound_sender_name='System',
            created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
        db.session.add(reply)
        db.session.commit()
        conversation.latest_content = content
        conversation.latest_date = reply.date
        conversation.latest_time = reply.time
        conversation.created_at = reply.created_at
        db.session.commit()

    return jsonify(
        status='success'
        ),201


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
        conversation.created_at = reply.created_at
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

    if contact.msisdn != data['msisdn']:
        existing_conversation = Conversation.query.filter_by(msisdn=contact.msisdn).first()
        if existing_conversation or existing_conversation != None:
            existing_conversation.contact_name = None
            existing_conversation.display_name = existing_conversation.msisdn
            db.session.commit()

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

    groups_to_recount = Group.query.filter_by(client_no=session['client_no'])
    for _ in groups_to_recount:
        group_size = ContactGroup.query.filter_by(group_id=_.id).count()
        _.size = group_size

    conversation = Conversation.query.filter_by(msisdn=data['msisdn']).first()
    if conversation or conversation != None:
        conversation.contact_name = data['name'].title()
        conversation.display_name = data['name'].title()
    db.session.commit()

    if data['type'] == 'from_convo':
        messages = ConversationItem.query.filter_by(conversation_id=conversation.id).order_by(ConversationItem.created_at)
        groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name)
        complete_contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name)
        contact_count = Contact.query.filter_by(client_no=session['client_no']).count()
        customers_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Customer').count()
        staff_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Staff').count()
        return jsonify(
            template = flask.render_template(
                'conversation.html',
                conversation=conversation,
                messages=messages 
                ),
            groups_template = flask.render_template(
                'group_count_update.html',
                contact_count=contact_count,
                customers_count=customers_count,
                staff_count=staff_count,
                groups=groups
                ),
            recipient_template=flask.render_template(
                'individual_recipients_refresh.html',
                contacts=complete_contacts,
                selected_contacts=session['individual_recipients']
                )
            ),201

    if session['contact_msisdn'] != data['msisdn']:
        old_conversation = Conversation.query.filter_by(msisdn=session['contact_msisdn']).first()
        if old_conversation or old_conversation != None:
            old_conversation.contact_name = None
            db.session.commit()

    total_entries = Contact.query.filter_by(client_no=session['client_no']).count()
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

    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name)
    contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name).slice(session['contact_limit'] - 50, session['contact_limit'])
    complete_contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name)
    contact_count = Contact.query.filter_by(client_no=session['client_no']).count()
    customers_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Customer').count()
    staff_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Staff').count()

    return jsonify(
        template = flask.render_template(
            'contacts.html',
            contacts=contacts,
            showing=showing,
            total_entries=total_entries,
            prev_btn=prev_btn,
            next_btn=next_btn
            ),
        groups_template = flask.render_template(
            'group_count_update.html',
            contact_count=contact_count,
            customers_count=customers_count,
            staff_count=staff_count,
            groups=groups
            ),
        recipient_template=flask.render_template(
            'individual_recipients_refresh.html',
            contacts=complete_contacts,
            selected_contacts=session['individual_recipients']
            )
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
    
    conversation = Conversation.query.filter_by(msisdn=new_contact.msisdn).first()
    if conversation or conversation != None:
        conversation.contact_name = new_contact.name
        conversation.display_name = new_contact.name

    db.session.commit()

    complete_contacts = Contact.query.filter_by(client_no=session['client_no']).order_by(Contact.name)

    complete_groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name)
    contact_count = Contact.query.filter_by(client_no=session['client_no']).count()
    customers_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Customer').count()
    staff_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Staff').count()

    if data['type'] == 'save':
        messages = ConversationItem.query.filter_by(conversation_id=conversation.id).order_by(ConversationItem.created_at)
        return jsonify(
                template=flask.render_template(
                    'conversation.html',
                    conversation=conversation,
                    messages=messages 
                    ),
                recipient_template=flask.render_template(
                    'individual_recipients_refresh.html',
                    contacts=complete_contacts,
                    selected_contacts=session['individual_recipients']
                    ),
                group_template=flask.render_template(
                    'group_recipients_refresh.html',
                    groups=complete_groups,
                    contact_count=contact_count,
                    customers_count=customers_count,
                    staff_count=staff_count,
                    selected_groups=session['group_recipients']
                    )
            )
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

    return jsonify(
        template=flask.render_template(
            'contacts.html',
            contacts=contacts,
            showing=showing,
            total_entries=total_entries,
            prev_btn=prev_btn,
            next_btn=next_btn,
        ),
        recipient_template=flask.render_template(
            'individual_recipients_refresh.html',
            contacts=complete_contacts,
            selected_contacts=session['individual_recipients']
            ),
        group_template=flask.render_template(
            'group_recipients_refresh.html',
            groups=complete_groups,
            contact_count=contact_count,
            customers_count=customers_count,
            staff_count=staff_count,
            selected_groups=session['group_recipients']
            )
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


@app.route('/group',methods=['GET','POST'])
def get_group_info():
    group_id = flask.request.args.get('group_id')
    session['open_group_id'] = group_id
    group = Group.query.filter_by(id=group_id).first()
    members = Contact.query.join(ContactGroup, Contact.id==ContactGroup.contact_id).add_columns(Contact.id, Contact.name, Contact.contact_type, Contact.msisdn).filter(Contact.id == ContactGroup.contact_id).filter(ContactGroup.group_id == group_id).all()
    return flask.render_template('group_info.html',group=group,members=members)


@app.route('/group/edit',methods=['GET','POST'])
def edit_group_info():
    group = Group.query.filter_by(id=session['open_group_id']).first()
    group.name = flask.request.form.get('group_name')
    db.session.commit()
    return jsonify(status='success'),201


@app.route('/group/members/delete/get',methods=['GET','POST'])
def get_delete_members():
    session['member_id'] = flask.request.form.get('member_id')
    session['group_id'] = flask.request.form.get('group_id')
    return jsonify(status='success'),201


@app.route('/group/members/delete',methods=['GET','POST'])
def delete_members():
    group = Group.query.filter_by(id=session['group_id']).first()
    contact_group = ContactGroup.query.filter_by(contact_id=session['member_id'], group_id=session['group_id']).first()
    db.session.delete(contact_group)
    db.session.commit()
    group.size = ContactGroup.query.filter_by(group_id=group.id).count()
    db.session.commit()
    members = Contact.query.join(ContactGroup, Contact.id==ContactGroup.contact_id).add_columns(Contact.id, Contact.name, Contact.contact_type, Contact.msisdn).filter(Contact.id == ContactGroup.contact_id).filter(ContactGroup.group_id == session['group_id']).all()
    return flask.render_template('group_info.html',group=group,members=members)


@app.route('/recipients/add', methods=['GET', 'POST'])
def add_recipients():
    special = flask.request.form.get('special')
    group_recipients_name = []
    individual_recipients_name = []
    number_recipients = []
    for group_recipient in session['group_recipients']:
        group = Group.query.filter_by(client_no=session['client_no'],id=group_recipient).first()
        group_recipients_name.append(group.name)
    for individual_recipient in session['individual_recipients']:
        contact = Contact.query.filter_by(client_no=session['client_no'],id=individual_recipient).first()
        individual_recipients_name.append(contact.name)
    for number_recipient in session['number_recipients']:
        number_recipients.append(number_recipient)
    return flask.render_template(
        'recipients.html',
        special=special,
        individual_recipients=individual_recipients_name,
        group_recipients=group_recipients_name,
        number_recipients=number_recipients
        )


@app.route('/recipients/clear', methods=['GET', 'POST'])
def clear_recipients():
    session['group_recipients'] = []
    session['individual_recipients'] = []
    session['number_recipients'] = []
    return '',201


@app.route('/blast/send', methods=['GET', 'POST'])
def send_text_blast():
    data = flask.request.form.to_dict()
    if ('special' in data) and (data['special'] != None or data['special'] != ''):
        if session['number_recipients']:
            number_recipients = ', '.join(session['number_recipients'])
            new_batch = Batch(
                client_no=session['client_no'],
                message_type='custom',
                sender_id=session['user_id'],
                sender_name=session['user_name'],
                recipient='%s, %s' % (data['special'],number_recipients),
                date=datetime.datetime.now().strftime('%B %d, %Y'),
                time=time.strftime("%I:%M %p"),
                content=data['content'],
                created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                )
        else :
            new_batch = Batch(
                client_no=session['client_no'],
                message_type='custom',
                sender_id=session['user_id'],
                sender_name=session['user_name'],
                recipient=data['special'],
                date=datetime.datetime.now().strftime('%B %d, %Y'),
                time=time.strftime("%I:%M %p"),
                content=data['content'],
                created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                )
        db.session.add(new_batch)
        db.session.commit()

        if data['special'] == 'Everyone':
            contacts = Contact.query.filter_by(client_no=session['client_no']).all()
        elif data['special'] == 'All Customers':
            contacts = Contact.query.filter_by(client_no=session['client_no'],contact_type='Customer').all()
        elif data['special'] == 'All Staff':
            contacts = Contact.query.filter_by(client_no=session['client_no'],contact_type='Staff').all()

        for contact in contacts:
            new_message = OutboundMessage(
                batch_id=new_batch.id,
                date=new_batch.date,
                time=new_batch.time,
                contact_name=contact.name,
                msisdn=contact.msisdn
                )
            db.session.add(new_message)
        db.session.commit()
        if session['number_recipients']:
            for msisdn in session['number_recipients']:
                number_message = OutboundMessage(
                    batch_id=new_batch.id,
                    date=new_batch.date,
                    time=new_batch.time,
                    msisdn=msisdn
                    )
                db.session.add(number_message)
            db.session.commit()

        new_batch.batch_size = OutboundMessage.query.filter_by(batch_id=new_batch.id).count()
        new_batch.pending = OutboundMessage.query.filter_by(batch_id=new_batch.id,status='pending').count()
        db.session.commit()

        blast_sms.delay(new_batch.id,new_batch.date,new_batch.time,data['content'],session['client_no'])
        
        session['group_recipients'] = []
        session['individual_recipients'] = []
        session['group_recipients_name'] = []
        session['individual_recipients_name'] = []
        session['number_recipients'] = []

        return jsonify(
            pending=new_batch.pending,
            batch_id=new_batch.id,
            template=flask.render_template('blast_status.html', batch=new_batch)
            )

    if session['number_recipients']:
        recipient_string = ', '.join(session['group_recipients_name']+session['individual_recipients_name'])
        number_recipients = ', '.join(session['number_recipients'])
        new_batch = Batch(
            client_no=session['client_no'],
            message_type='custom',
            sender_id=session['user_id'],
            sender_name=session['user_name'],
            recipient='%s, %s' % (recipient_string,number_recipients),
            date=datetime.datetime.now().strftime('%B %d, %Y'),
            time=time.strftime("%I:%M %p"),
            content=data['content'],
            created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
    else:
        new_batch = Batch(
            client_no=session['client_no'],
            message_type='custom',
            sender_id=session['user_id'],
            sender_name=session['user_name'],
            recipient=', '.join(session['group_recipients_name']+session['individual_recipients_name']),
            date=datetime.datetime.now().strftime('%B %d, %Y'),
            time=time.strftime("%I:%M %p"),
            content=data['content'],
            created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
    db.session.add(new_batch)
    db.session.commit()

    for group_id in session['group_recipients']:
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

    for individual_id in session['individual_recipients']:
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

    if session['number_recipients']:
        for msisdn in session['number_recipients']:
            number_message = OutboundMessage(
                batch_id=new_batch.id,
                date=new_batch.date,
                time=new_batch.time,
                msisdn=msisdn
                )
            db.session.add(number_message)
        db.session.commit()


    new_batch.batch_size = OutboundMessage.query.filter_by(batch_id=new_batch.id).count()
    new_batch.pending = OutboundMessage.query.filter_by(batch_id=new_batch.id,status='pending').count()
    db.session.commit()

    blast_sms.delay(new_batch.id,new_batch.date,new_batch.time,data['content'],session['client_no'])
    session['group_recipients'] = []
    session['individual_recipients'] = []
    session['group_recipients_name'] = []
    session['individual_recipients_name'] = []
    session['number_recipients'] = []
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
    batch = ContactBatch.query.filter_by(id=int(batch_id)).first()
    return jsonify(
        batch_id=batch.id,
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


@app.route('/conversations/search',methods=['GET','POST'])
def search_from_conversations():
    data = flask.request.args.to_dict()
    result = search_conversations(latest_date=data['date'], latest_content=data['content'],display_name=data['name'])
    count = search_conversations_count(latest_date=data['date'], latest_content=data['content'],display_name=data['name'])
    return jsonify(
        count = count,
        template = flask.render_template('conversations_result.html',conversations=result)
        )


@app.route('/blasts/search',methods=['GET','POST'])
def search_from_blasts():
    data = flask.request.args.to_dict()
    result = search_blasts(sender_name=data['sender'], content=data['content'],date=data['date'])
    count = search_blasts_count(sender_name=data['sender'], content=data['content'],date=data['date'])
    return jsonify(
        count = count,
        template = flask.render_template('blasts_result.html',blasts=result)
        )


@app.route('/reminders/search',methods=['GET','POST'])
def search_from_reminders():
    data = flask.request.args.to_dict()
    result = search_reminders(sender_name=data['sender'], file_name=data['filename'],date=data['date'])
    count = search_reminders_count(sender_name=data['sender'], file_name=data['filename'],date=data['date'])
    return jsonify(
        count = count,
        template = flask.render_template('reminders_result.html',reminders=result)
        )


@app.route('/contacts/search',methods=['GET','POST'])
def search_from_contacts():
    data = flask.request.args.to_dict()
    result = search_contacts(name=data['name'], contact_type=data['contact_type'],msisdn=data['msisdn'])
    count = search_contacts_count(name=data['name'], contact_type=data['contact_type'],msisdn=data['msisdn'])
    return jsonify(
        count = count,
        template = flask.render_template('contacts_result.html',contacts=result)
        )


@app.route('/users/search',methods=['GET','POST'])
def search_from_users():
    data = flask.request.args.to_dict()
    result = search_users(name=data['name'], role=data['role'],email=data['email'])
    count = search_users_count(name=data['name'], role=data['role'],email=data['email'])
    return jsonify(
        count = count,
        template = flask.render_template('users_result.html',users=result)
        )


@app.route('/groups/search',methods=['GET','POST'])
def search_from_groups():
    data = flask.request.args.to_dict()
    result = search_groups(name=data['name'])
    count = search_groups_count(name=data['name'])
    return jsonify(
        count = count,
        template = flask.render_template('groups_result.html',groups=result)
        )


@app.route('/contacts/groups/search',methods=['GET','POST'])
def search_group_recipients():
    group_name = flask.request.form.get('group_name')
    if group_name and group_name != '': 
        groups = Group.query.filter(Group.name.ilike('%'+group_name+'%')).filter(Group.client_no==session['client_no']).order_by(Group.name)
        return flask.render_template('group_recipients_result.html',groups=groups,selected_groups=session['group_recipients'])

    groups = Group.query.filter_by(client_no=session['client_no']).order_by(Group.name)
    contact_count = Contact.query.filter_by(client_no=session['client_no']).count()
    customers_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Customer').count()
    staff_count = Contact.query.filter_by(client_no=session['client_no'], contact_type='Staff').count()
    return flask.render_template(
        'group_recipients_refresh.html',
        groups=groups,
        contact_count=contact_count,
        customers_count=customers_count,
        staff_count=staff_count,
        selected_groups=session['group_recipients']
        )


@app.route('/contacts/indiv/search',methods=['GET','POST'])
def search_indiv_recipients():
    name = flask.request.form.get('name')
    contacts = Contact.query.filter(Contact.name.ilike('%'+name+'%')).filter(Contact.client_no==session['client_no']).order_by(Contact.name)
    return flask.render_template('indiv_recipients_result.html',contacts=contacts, selected_contacts=session['individual_recipients'])


@app.route('/conversations/delete',methods=['GET','POST'])
def delete_conversations():
    conversation_ids = flask.request.form.getlist('selected_conversations[]')
    for conversation_id in conversation_ids:
        conversation = Conversation.query.filter_by(client_no=session['client_no'],id=conversation_id).first()
        db.session.delete(conversation)
        db.session.commit()
    return jsonify(status='success'),201


@app.route('/blasts/delete',methods=['GET','POST'])
def delete_blasts():
    blast_ids = flask.request.form.getlist('selected_blasts[]')
    for blast_id in blast_ids:
        blast = Batch.query.filter_by(client_no=session['client_no'],id=blast_id).first()
        db.session.delete(blast)
        db.session.commit()
    return jsonify(status='success'),201


@app.route('/reminders/delete',methods=['GET','POST'])
def delete_reminders():
    reminder_ids = flask.request.form.getlist('selected_reminders[]')
    for reminder_id in reminder_ids:
        reminder_batch = ReminderBatch.query.filter_by(client_no=session['client_no'],id=reminder_id).first()
        db.session.delete(reminder_batch)
        db.session.commit()
    return jsonify(status='success'),201


@app.route('/contacts/delete',methods=['GET','POST'])
def delete_contacts():
    contact_ids = flask.request.form.getlist('selected_contacts[]')
    for contact_id in contact_ids:
        contact = Contact.query.filter_by(client_no=session['client_no'],id=contact_id).first()
        db.session.delete(contact)
        db.session.commit()
    return jsonify(status='success'),201


@app.route('/groups/delete',methods=['GET','POST'])
def delete_groups():
    group_ids = flask.request.form.getlist('selected_groups[]')
    for group_id in group_ids:
        group = Group.query.filter_by(client_no=session['client_no'],id=group_id).first()
        db.session.delete(group)
        db.session.commit()
    return jsonify(status='success'),201


@app.route('/recipients/number/add',methods=['GET','POST'])
def add_number_recipient():
    recipient = flask.request.form.get('recipient')
    session['number_recipients'].append(recipient)
    return flask.render_template('number_recipients.html',recipient=recipient)


@app.route('/recipients/group/add',methods=['GET','POST'])
def add_group_recipient():
    recipient_id = flask.request.form.get('recipient_id')
    session['group_recipients'].append(recipient_id)
    group = Group.query.filter_by(client_no=session['client_no'],id=recipient_id).first()
    session['group_recipients_name'].append(group.name)
    return jsonify(
        size = group.size,
        template = flask.render_template('group_recipients.html', group=group)
        )


@app.route('/recipients/group/remove',methods=['GET','POST'])
def remove_group_recipient():
    recipient_id = flask.request.form.get('recipient_id')
    session['group_recipients'].remove(recipient_id)
    group = Group.query.filter_by(client_no=session['client_no'],id=recipient_id).first()
    session['group_recipients_name'].remove(group.name)
    return jsonify(
        size = group.size
        )

@app.route('/recipients/individual/add',methods=['GET','POST'])
def add_individual_recipient():
    recipient_id = flask.request.form.get('recipient_id')
    session['individual_recipients'].append(recipient_id)
    recipient = Contact.query.filter_by(client_no=session['client_no'],id=recipient_id).first()
    session['individual_recipients_name'].append(recipient.name)
    return jsonify(
        template = flask.render_template('individual_recipients.html', recipient=recipient)
        )


@app.route('/recipients/individual/remove',methods=['GET','POST'])
def remove_individual_recipient():
    recipient_id = flask.request.form.get('recipient_id')
    session['individual_recipients'].remove(recipient_id)
    recipient = Contact.query.filter_by(client_no=session['client_no'],id=recipient_id).first()
    session['individual_recipients_name'].remove(recipient.name)
    return '',201


@app.route('/recipients/number/remove',methods=['GET','POST'])
def remove_number_recipient():
    msisdn = flask.request.form.get('msisdn')
    session['number_recipients'].remove(msisdn)
    return '',201


@app.route('/recipients/special/add',methods=['GET','POST'])
def add_special_recipient():
    session['group_recipients'] = []
    session['individual_recipients'] = []
    session['group_recipients_name'] = []
    session['individual_recipients_name'] = []
    return jsonify(
        size = len(session['number_recipients'])
        ),201


@app.route('/db/rebuild',methods=['GET','POST'])
def rebuild_database():
    db.drop_all()
    db.create_all()

    client = Client(
        client_no='qpdc',
        name='Quezon Province Dental Chapter',
        app_id='EGXMuB5eEgCMLTKxExieqkCGeGeGuBon',
        app_secret='f3e1ab30e23ea7a58105f058318785ae236378d1d9ebac58fe8b42e1e239e1c3',
        passphrase='24BUubukMQ',
        shortcode='21588479',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    admin = AdminUser(
        client_no='qpdc',
        email='hello@pisara.tech',
        password='ratmaxi8',
        name='Super Admin',
        role='Administrator',
        join_date=datetime.datetime.now().strftime('%B %d, %Y'),
        added_by_name='None',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    admin1 = AdminUser(
        client_no='qpdc',
        email='cy.lucero@yahoo.com',
        password='clinic123',
        name='Cyril Lucero',
        role='Administrator',
        join_date=datetime.datetime.now().strftime('%B %d, %Y'),
        added_by_name='None',
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    # client = Client(
    #     client_no='at-ic2017',
    #     name='Alson\'s Trading',
    #     app_id='MEoztReRyeHzaiXxaecR65HnqE98tz9g',
    #     app_secret='01c5d1f8d3bfa9966786065c5a2d829d7e84cf26fbfb4a47c91552cb7c091608',
    #     passphrase='PF5H8S9t7u',
    #     shortcode='21586853',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # client1 = Client(
    #     client_no='jm-ic2017',
    #     name='Jayson Marketing',
    #     app_id='x65gtry7b7u7oT5dAbi7oKudp6AptkGA',
    #     app_secret='72755ee33c36657daaa38a57a50728f8ef2b00189577a0f5fb432f8549386239',
    #     passphrase='PF5H8S9t7u',
    #     shortcode='21587460',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # # for _ in range(1000):
    # #     admin = AdminUser(
    # #         client_no='at-ic2017',
    # #         email='hello@pisara.tech',
    # #         password='ratmaxi8',
    # #         name='Admin%s' % _,
    # #         role='Administrator',
    # #         join_date='November 14, 2017',
    # #         added_by_name='None',
    # #         created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    # #         )
    # #     db.session.add(admin)
    # #     db.session.commit()

    # admin = AdminUser(
    #     client_no='at-ic2017',
    #     email='hello@pisara.tech',
    #     password='ratmaxi8',
    #     name='Super Admin',
    #     role='Administrator',
    #     join_date='November 14, 2017',
    #     added_by_name='None',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # admin1 = AdminUser(
    #     client_no='jm-ic2017',
    #     email='hello@pisara.tech',
    #     password='ratmaxi8',
    #     name='Super Admin',
    #     role='Administrator',
    #     join_date='November 14, 2017',
    #     added_by_name='None',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # admin2 = AdminUser(
    #     client_no='at-ic2017',
    #     email='ballesteros.alan@gmail.com',
    #     password='password',
    #     name='Alan Ballesteros',
    #     role='Administrator',
    #     join_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'),
    #     added_by_name='Super Admin',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # contact = Contact(
    #     client_no='at-ic2017',
    #     contact_type='Customer',
    #     name='Alan Ballesteros',
    #     msisdn='09176214704',
    #     added_by=1,
    #     added_by_name='Super Admin',
    #     join_date='November 14, 2017',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # conversations = Conversation(
    #     client_no='at-ic2017',
    #     contact_name='Alan Ballesteros'.title(),
    #     msisdn='09176214704',
    #     display_name='Alan Ballesteros'.title(),
    #     status='unread',
    #     latest_content='This is a sample incoming message. You can try to reply to it',
    #     latest_date='November 14, 2017',
    #     latest_time='11:36 AM',
    #     created_at='2017-11-14 11:36:49:270418',
    #     )

    # conversations1 = Conversation(
    #     client_no='at-ic2017',
    #     msisdn='09159484200',
    #     display_name='09159484200',
    #     status='unread',
    #     latest_content='This is a sample incoming message. You can try to reply to it',
    #     latest_date='November 14, 2017',
    #     latest_time='11:37 AM',
    #     created_at='2017-11-14 11:37:49:270418',
    #     )

    # conversations2 = Conversation(
    #     client_no='at-ic2017',
    #     msisdn='09189123948',
    #     display_name='09189123948',
    #     status='unread',
    #     latest_content='This is a sample incoming message. You can try to reply to it',
    #     latest_date='November 14, 2017',
    #     latest_time='11:38 AM',
    #     created_at='2017-11-14 11:38:49:270418',
    #     )

    # # conversations1 = Conversation(
    # #     client_no='at-ic2017',
    # #     msisdn='09176214704',
    # #     display_name='09176214704',
    # #     status='unread',
    # #     latest_content='This is another sample message.',
    # #     latest_date='November 13, 2017',
    # #     latest_time='12:23 PM',
    # #     created_at='2017-11-13 12:23:49:270418',
    # #     )

    # message = ConversationItem(
    #     conversation_id=1,
    #     message_type='inbound',
    #     date='November 14, 2017',
    #     time='11:36 AM',
    #     content='This is a sample incoming message. You can try to reply to it.',
    #     created_at='2017-11-14 11:30:49:270418'
    #     )

    # message1 = ConversationItem(
    #     conversation_id=2,
    #     message_type='inbound',
    #     date='November 14, 2017',
    #     time='11:37 AM',
    #     content='This is a sample incoming message. You can try to reply to it.',
    #     created_at='2017-11-14 11:30:49:270418'
    #     )

    # message2 = ConversationItem(
    #     conversation_id=3,
    #     message_type='inbound',
    #     date='November 14, 2017',
    #     time='11:38 AM',
    #     content='This is a sample incoming message. You can try to reply to it.',
    #     created_at='2017-11-14 11:30:49:270418'
    #     )

    # # message2 = ConversationItem(
    # #     conversation_id=2,
    # #     message_type='inbound',
    # #     date='November 13, 2017',
    # #     time='12:10 PM',
    # #     content='This is another sample message.',
    # #     created_at='2017-11-13 12:10:49:270418'
    # #     )

    # blast = Batch(
    #     client_no='at-ic2017',
    #     message_type='custom',
    #     sender_id=1,
    #     batch_size=3,
    #     sender_name='Jasper Barcelona',
    #     recipient='AGN, ANB, JNC',
    #     date='November 14, 2017',
    #     time='07:36 AM',
    #     content='This is a sample text blast.',
    #     done=3,
    #     failed=0,
    #     pending=0,
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     ) 

    # blast_message = OutboundMessage(
    #     batch_id=1,
    #     date='November 14, 2017',
    #     time='07:36 AM',
    #     contact_name='ABAC, AILYN-AGN'.title(),
    #     msisdn='09994282203',
    #     status='success',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )
    
    # blast_message1 = OutboundMessage(
    #     batch_id=1,
    #     date='November 14, 2017',
    #     time='07:36 AM',
    #     contact_name='ABAD, LANDELINA ORCIGA-ANB'.title(),
    #     msisdn='09183132539',
    #     status='success',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # blast_message2 = OutboundMessage(
    #     batch_id=1,
    #     date='November 14, 2017',
    #     time='07:36 AM',
    #     contact_name='ABAD, NELSON M.-JNC'.title(),
    #     msisdn='09071755339',
    #     status='success',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # reminder = ReminderBatch(
    #     client_no='at-ic2017',
    #     sender_id=1,
    #     batch_size=3,
    #     sender_name='Super Admin',
    #     date='November 14, 2017',
    #     time='11:36 AM',
    #     file_name='payment_reminders.xls',
    #     done=3,
    #     failed=0,
    #     pending=0,
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # reminder_message = ReminderMessage(
    #     batch_id=1,
    #     date='November 14, 2017',
    #     time='11:36 AM',
    #     contact_name='ABAC, AILYN-AGN'.title(),
    #     content='This is a sample payment reminder.',
    #     msisdn='09994282203',
    #     status='success',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # reminder_message1 = ReminderMessage(
    #     batch_id=1,
    #     date='November 14, 2017',
    #     time='11:36 AM',
    #     contact_name='ABAD, LANDELINA ORCIGA-ANB'.title(),
    #     content='This is a sample payment reminder.',
    #     msisdn='09183132539',
    #     status='success',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # reminder_message2 = ReminderMessage(
    #     batch_id=1,
    #     date='November 14, 2017',
    #     time='11:36 AM',
    #     contact_name='ABAD, NELSON M.-JNC'.title(),
    #     content='This is a sample payment reminder.',
    #     msisdn='09071755339',
    #     status='success',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # # contact = Contact(
    # #     client_no='at-ic2017',
    # #     contact_type='Customer',
    # #     name='ABAC, AILYN-AGN'.title(),
    # #     msisdn='09994282203',
    # #     added_by=1,
    # #     added_by_name='Super Admin',
    # #     join_date='November 10, 2017',
    # #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    # #     )

    # # contact1 = Contact(
    # #     client_no='at-ic2017',
    # #     contact_type='Customer',
    # #     name='ABAD, LANDELINA ORCIGA-ANB'.title(),
    # #     msisdn='09183132539',
    # #     added_by=1,
    # #     added_by_name='Super Admin',
    # #     join_date='November 10, 2017',
    # #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    # #     )

    # # contact2 = Contact(
    # #     client_no='at-ic2017',
    # #     contact_type='Customer',
    # #     name='ABAD, NELSON M.-JNC'.title(),
    # #     msisdn='09071755339',
    # #     added_by=1,
    # #     added_by_name='Super Admin',
    # #     join_date='November 10, 2017',
    # #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    # #     )

    # # for _ in range(1000):
    # #     new_group = Group(
    # #         client_no='at-ic2017',
    # #         name='AGN%s' % _,
    # #         size=0,
    # #         created_by_id=1,
    # #         created_by_name='Super Admin',
    # #         created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    # #         )
    # #     db.session.add(new_group)
    # #     db.session.commit()

    # new_group = Group(
    #     client_no='at-ic2017',
    #     name='AGN',
    #     size=0,
    #     created_by_id=1,
    #     created_by_name='Super Admin',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # new_group1 = Group(
    #     client_no='at-ic2017',
    #     name='ANB',
    #     size=0,
    #     created_by_id=1,
    #     created_by_name='Super Admin',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # new_group2 = Group(
    #     client_no='at-ic2017',
    #     name='JNC',
    #     size=0,
    #     created_by_id=1,
    #     created_by_name='Super Admin',
    #     created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     )

    # # contact_group = ContactGroup(
    # #     group_id=1,
    # #     contact_id=1
    # #     )

    # # contact_group1 = ContactGroup(
    # #     group_id=2,
    # #     contact_id=2
    # #     )

    # # contact_group2 = ContactGroup(
    # #     group_id=3,
    # #     contact_id=3
    # #     )
    
    db.session.add(client)
    # db.session.add(client1)
    db.session.add(admin)
    db.session.add(admin1)
    # db.session.add(admin2)
    # db.session.add(contact)
    # db.session.add(conversations)
    # db.session.add(conversations1)
    # db.session.add(conversations2)
    # db.session.add(message)
    # db.session.add(message1)
    # db.session.add(message2)

    # db.session.add(blast)
    # db.session.add(reminder)
    # db.session.add(contact)
    # # db.session.add(contact1)
    # # db.session.add(contact2)
    # db.session.add(new_group)
    # db.session.add(new_group1)
    # db.session.add(new_group2)
    # # db.session.add(contact_group)
    # # db.session.add(contact_group1)
    # # db.session.add(contact_group2)

    # db.session.add(blast_message)
    # db.session.add(blast_message1)
    # db.session.add(blast_message2)
    # db.session.add(reminder_message)
    # db.session.add(reminder_message1)
    # db.session.add(reminder_message2)

    db.session.commit()

    return jsonify(
        status = 'success'
        ), 201

if __name__ == '__main__':
    app.run(port=5000,debug=True,host='0.0.0.0')
    # port=int(os.environ['PORT']), host='0.0.0.0'