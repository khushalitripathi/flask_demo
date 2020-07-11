import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

# blueprint created for form
bp = Blueprint('form', __name__, url_prefix='/form')


# user registration method
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
    	# get all form fields value
        username = request.form['username']
        address = request.form['address']
        marital_status = request.form['marital_status']
        salary = request.form['salary']
        # connect db
        db = get_db()
        error = None

        # validation for all required fields
        # validation for salary only contains numeric value
        if not username:
            error = 'Username is required.'
        elif not address:
            error = 'Address is required.'
        elif not salary:
        	error = 'Salary is required.'
        elif salary:
        	try:
        		salary = int(salary)
        	except ValueError as e:
        		error = 'Only numeric value allowed in salary field.'

        # validation for already registered user using same username
        user_exists = db.cursor().execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone()

        # if user with same username exists then show error message
        if user_exists is not None:
        	error = 'User {} is already registered.'.format(username)

        # if form is validated then store those values in db
        if error is None:
            db.execute(
                'INSERT INTO user (username, address, marital_status, salary) VALUES (?, ?, ?, ?)',
                (username, address, marital_status, salary)
            )
            db.commit()
            # after storing values redirect to success html page
            return redirect(url_for('form.success'))

        # display validation error
        flash(error)

    # if any error found then display the same form page
    return render_template('form/register.html')


# method to display registered users details in html table
@bp.route('/success', methods=('GET', 'POST'))
def success():
	db = get_db()
	c = db.cursor()
	c.execute( 'SELECT * FROM user' )
	rows = c.fetchall()
	return render_template('form/success.html', items=rows)