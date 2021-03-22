from flask import Blueprint, render_template, abort, request
import re
from jinja2 import TemplateNotFound
from app.models import User
from app import db

main = Blueprint('main_page', __name__,
                 template_folder='templates')


@main.route('/', defaults={'page': 'index'})
@main.route('/<page>')
def show(page):
    # users = query_db('SELECT * FROM user')
    # admin = User(name='admin', email='admin@example.com', password='123')
    # guest = User(name='guest', email='guest@example.com', password='123')
    # db.session.add(admin)
    # db.session.add(guest)
    # db.session.commit()
    users = User.query.all()
    try:
        return render_template('%s.html' % page, users=users)
    except TemplateNotFound:
        abort(404)


# Show signup form and process and save returned form data
@main.route('/signup', defaults={'page': 'signup'}, methods=['GET', 'POST'])
def signup_page(page):
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        if (
            #     validate('name', '(\w| )+')
            # and validate('email', '.+\@.+\..+')
            # and
            validate('password', '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
        ):
            # guest = User.create(tuple([request.form[val] for val in ['name', 'email', 'password']]))
            # db.session.add(guest)
            # db.session.commit()

            return 'Vaild info has been sent to Flask'
        else:
            return 'Invalid info has been sent to Flask'


# Show signin form and return user if found
# Show signup form and process and save returned form data
@main.route('/signin',  defaults={'page': 'signin'}, methods=['GET', 'POST'])
def signin_page(page):
    if request.method == 'GET':
        return render_template('signin.html')

    elif request.method == 'POST':
        if (validate('email', '.+\@.+\..+')
            # and validate('password', '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
        ):
            user = User.query.filter_by(email=request.form['email'], password=request.form['password']).first()
            if user is None:
                return 'User does not exist'
            else:
                return user.email
        else:
            return 'Invalid info has been sent to Flask'




# Validate data format is correct
def validate(text, pattern):
    regex = re.compile(pattern, re.I)
    match = regex.match(request.form[text])
    return bool(match)
