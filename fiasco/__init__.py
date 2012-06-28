# extensions installed
# http://elsdoerfer.name/docs/flask-assets/
# http://packages.python.org/Flask-Bcrypt/
# http://packages.python.org/Flask-Mail/
# http://packages.python.org/Flask-SeaSurf/
# http://packages.python.org/Flask-WTF/
# to check:
# http://packages.python.org/Flask-Login/
# http://packages.python.org/Flask-OAuth/
# http://packages.python.org/Flask-OpenID/

from flask import Flask
#from flask import render_template
#from flask import Flask, request, session, g, redirect, url_for, \
#	abort, render_template, flash
from flaskext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('settings')
bcrypt = Bcrypt(app)

#import econo.views
from fiasco import views
from database import Database

app.db = Database()
app.db.connect_db(app.config['DB_USER'], app.config['DB_PASS'], app.config['DATABASE'], app.config['DB_HOST'])
app.db.init_db()

@app.teardown_request
def shutdown_session(exception=None):
	app.db.db_session.remove()
	app.db.db_session.close()

