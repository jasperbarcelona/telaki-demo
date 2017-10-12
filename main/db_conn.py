import flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean

app = flask.Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = '0129383hfldcndidvs98r9t9438953894534k545lkn3kfnac98'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:temppass@db/telaki'
# sqlite:///local.db
# postgresql://admin:temppass@db/telaki'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)