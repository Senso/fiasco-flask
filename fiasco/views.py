from flask import Flask, session, redirect, url_for, escape, request
from flask import abort, render_template, flash
from wtforms import TextField
from fiasco import app
from fiasco import models
from fiasco import bcrypt
from fiasco import utils
from fiasco import detail
from fiasco import fforms

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/settings')
def index():
	if not utils.logged_in(session):
		return redirect(url_for('login'))
	return render_template('settings.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if utils.logged_in(session):
		return redirect(url_for('index'))

	error = None
	if request.method == 'POST':
		u = models.User()

		if not request.form['username']:
			error = 'Missing username'
		elif not request.form['email']:
			error = 'Missing email'
		elif not request.form['password1'] or not request.form['password2']:
			error = 'Missing password'
		elif u.user_exists(request.form['username']):
			error = 'Username is already taken'
		elif request.form['password1'] != request.form['password2']:
			error = 'Passwords do not match'
		else:
			# let's assume everything is ok, will need more work obviously
			salt = utils.make_salt()
			pw = bcrypt.generate_password_hash(request.form['password1'] + salt)
			new_user = models.User(request.form['username'], request.form['email'], pw, salt)
			app.db.db_session.add(new_user)
			app.db.db_session.commit()
			flash('Registered successfully!')
			return render_template('login.html')

	return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if utils.logged_in(session):
		return redirect(url_for('index'))
	error = None

	if request.method == 'POST':
		if not request.form['username'] or not request.form['password']:
			return render_template('login.html', error='Missing field')

		#u = models.User()
		valid_user = models.User.query.filter(models.User.username == request.form['username']).first()
		if not valid_user:
			return render_template('login.html', error='Invalid username or password')

		
		if bcrypt.check_password_hash(valid_user.password, request.form['password'] + valid_user.salt):
			session['logged_in'] = True
			session['username'] = valid_user.username
			session['uid'] = valid_user.id
			flash('You were logged in')
			return redirect(url_for('index'))
		else:
			return render_template('login.html', error='Invalid username or password')
		
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)
	session.pop('uid', None)
	flash('You were logged out')
	return redirect(url_for('index'))

@app.route('/new_playset', methods=['GET', 'POST'])
def new_playset():
	if not utils.logged_in(session):
		return redirect(url_for('login'))
	error = None

	from fiasco import fforms
	form = fforms.NewPlayset(request.form)

	if request.method == 'POST' and form.validate():
		# check if playset name is unique
		playset = models.Playset(name=form.name.data, desc=form.description.data)
		app.db.db_session.add(playset)
		app.db.db_session.commit()

		# Create default Detail object
		need_detail = detail.Detail()
		obj_detail = detail.Detail()
		loc_detail = detail.Detail()
		rel_detail = detail.Detail()

		n_table = models.Details(playset.id, 'need', need_detail)
		o_table = models.Details(playset.id, 'object', obj_detail)
		l_table = models.Details(playset.id, 'location', loc_detail)
		r_table = models.Details(playset.id, 'relationship', rel_detail)
		app.db.db_session.add(n_table)
		app.db.db_session.add(o_table)
		app.db.db_session.add(l_table)
		app.db.db_session.add(r_table)
		app.db.db_session.commit()

		flash('Playset added successfully!')

		return redirect('/edit_playset/' + str(playset.id))

	return render_template('new_playset.html', error=error, form=form)

@app.route('/playsets', methods=['GET'])
def playsets():
	error = None
	playsets = models.Playset().list_playsets()
	return render_template('playsets.html', error=error, all_playsets=playsets)	

@app.route('/playset/<pl_id>', methods=['GET'])
def show_playset(pl_id):
	error = None

	playset = models.Playset()
	derp = playset.get_playset(pl_id)

	return render_template('playset.html', error=error, playset_data=derp)

@app.route('/edit_playset/<pl_id>', methods=['GET', 'POST'])
def edit_playset(pl_id):
	if not utils.logged_in(session):
		flash('You need to login first.')
		return redirect(url_for('login'))
	error = None

	# Need to check if user is playset owner

	playset = models.Playset()
	pl_data = playset.get_playset(pl_id)
	if not pl_data:
		flash('Wrong Playset.')
		return redirect(url_for('playsets'))

	details = models.Details.query.filter(models.Details.playset_id == pl_id).all()

	if request.method == 'POST' and form.validate():
		pl_data.name = form.name.data
		pl_data.description = form.description.data

		app.db.db_session.commit()
		flash('Playset edited successfully!')

	elif request.method == 'GET':
		class Derp(fforms.EditPlayset):
			pass

		for det in details:
			detail = det.data
			detail.unpack()
			if det.detail_type == 'relationship':
				blarg = detail.unpacked
				for d in detail.unpacked.items():
					setattr(Derp, d[0], TextField(label=label))

		form = Derp(request.form)
		form.name.data = pl_data.name
		form.description.data = pl_data.description

		for det in details:
			detail = det.data
			if det.detail_type == 'relationship':
				for e in detail.unpacked.items():
					form[e[0]].data = e[1]

	return render_template('edit_playset.html', error=error, form=form, blarg=blarg)
	
@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
	if not utils.logged_in(session):
		flash('You need to login first.')
		return redirect(url_for('login'))
	error = None

	from fiasco import fforms
	form = fforms.NewGame(request.form)
	form.playset.choices = [(g.id, g.name) for g in models.Playset().query.order_by('name')]

	if request.method == 'POST' and form.validate():
		flash('placeholder!')

	return render_template('new_game.html', error=error, form=form)


