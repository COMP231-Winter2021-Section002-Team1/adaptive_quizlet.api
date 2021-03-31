from flask import Blueprint, abort, render_template, request, g, redirect, session, url_for, flash

import re
from jinja2 import TemplateNotFound
from app.models import User, Question, Quiz, Choice
from app import db
from datetime import datetime

main = Blueprint('main', __name__,
                 template_folder='templates')


@main.route('/', defaults={'page': 'index'})
@main.route('/<page>')
def index(page):
    db.drop_all()
    db.create_all()
    admin = User(name='Hassan', email='hassan149367@gmail.com', password='password')
    guest = User(name='guest', email='a@a.a', password='123')
    db.session.add(admin)
    db.session.add(guest)
    quiz = Quiz(title="Quiz 1", limited_time=12, posted_at=datetime.now(),)
    choice1 = Choice(content="1", question_id=1)
    choice2 = Choice(content="2", question_id=1, correct=True)
    choice3 = Choice(content="3", question_id=1)
    choice4 = Choice(content="4", question_id=1)
    question = Question(content="1+1=?", quiz_id=choice2.id, actual_answer=2, choices=[choice1, choice2, choice3, choice4])
    quiz.questions = [question]
    db.session.add(quiz)
    admin.user_quizzes.append(quiz)
    db.session.commit()
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
                validate('name', '(\w| )+')
                and validate('email', '.+\@.+\..+')
                and
                validate('password', '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
        ):
            guest = User.create(tuple([request.form[val] for val in ['name', 'email', 'password']]))
            db.session.add(guest)
            db.session.commit()
            # choice1 = Choice()

            return 'Vaild info has been sent to Flask'
        else:
            return 'Invalid info has been sent to Flask'


# Show signin form and return user if found
# Show signup form and process and save returned form data
@main.route('/signin', defaults={'page': 'signin'}, methods=['GET', 'POST'])
def signin_page(page):
    if request.method == 'GET':
        return render_template('signin.html')

    elif request.method == 'POST':
        if (validate('email', '.+\@.+\..+')
                # and validate('password', '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
        ):
            user = User.query.filter_by(email=request.form['email'], password=request.form['password']).first()
            session['user'] = user
            if user is None:
                return 'User does not exist'
            else:
                return  render_template('%s.html' % 'user_profile', user=user)
        else:
            return 'Invalid info has been sent to Flask'


# logout session
@main.route('/logout', defaults={'page': 'logout'})
def logout(page):
    # print(session['user'], "before logout")
    session['user'] = None # {..., 'user' : None}
    flash("You have been logged out", "success")
    return redirect(url_for('main.index'))


# logout session
@main.route('/available_quizzes', defaults={'page': 'available_quizzes'})
def available_quizzes(page):
    if 'user' in session and session['user']:
        return render_template('%s.html' % page, user=session['user'])
    return redirect(url_for('main.logout'))


# Validate data format is correct
def validate(text, pattern):
    regex = re.compile(pattern, re.I)
    match = regex.match(request.form[text])
    return bool(match)
