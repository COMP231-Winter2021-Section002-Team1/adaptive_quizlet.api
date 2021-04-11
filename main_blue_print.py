import re
from datetime import datetime

from flask import Blueprint, abort, render_template, request, redirect, session, url_for, flash

from app import db
from app.models import User, Question, Quiz, Choice, QuizResult, UserChoice

main = Blueprint('main', __name__,
                 template_folder='templates')


@main.route('/', defaults={'page': 'index'})
@main.route('/<page>')
def index(page):
    try:
        db.drop_all()
        db.create_all()
        # create quiz maker
        quiz_maker = User(name='Hassan', email='hassan149367@gmail.com', password='password')
        # create quiz with single-choice questions
        quiz = Quiz(title="Quiz 1", limited_time=12, posted_at=datetime.now())
        # create and add question for the quiz
        question = Question(content="1+1=?", correct_answer=2, choices=[
            Choice(content="1"),
            Choice(content="2"),
            Choice(content="3"),
            Choice(content="4"),
        ])
        quiz.questions.append(question)
        quiz.questions.append(Question(content="1+2=?", correct_answer=3, choices=[
            Choice(content="1"),
            Choice(content="2"),
            Choice(content="3"),
            Choice(content="4"),
        ]))
        # add created quiz to quiz maker's created quizzes list
        quiz_maker.created_quizzes.append(quiz)


        # create quiz taker
        quiz_taker = User(name='guest', email='a@a.a', password='123')
        # quiz taker take a quiz, create user quiz result
        quiz_result = QuizResult(quiz=quiz)
        # add quiz result to the taker
        quiz_taker.quizzes_results.append(quiz_result)
        # set quiz taker's answer for question[0] in the quiz, here user choose the second choice which is at index 1
        user_choice = quiz.questions[0].choices[1]
        # create a user choice,
        user_answer = UserChoice(choice=user_choice, answer_right=True)
        # add the user answer to the quiz result
        quiz_result.user_choices.append(user_answer)
        quiz_result.user_choices.append(UserChoice(choice=quiz.questions[1].choices[1], answer_right=False))
        # add and commit changes
        db.session.add(quiz_maker)
        db.session.add(quiz_taker)
        db.session.commit()
        # query all users
        users = User.query.all()
        print(users[1].quizzes_results[0])
        return render_template('%s.html' % page, users=users)
    except Exception as ex:
        print(ex)
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
                return render_template('%s.html' % 'user_profile', user=user)
        else:
            return 'Invalid info has been sent to Flask'


# logout session
@main.route('/logout', defaults={'page': 'logout'})
def logout(page):
    # print(session['user'], "before logout")
    session['user'] = None  # {..., 'user' : None}
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
