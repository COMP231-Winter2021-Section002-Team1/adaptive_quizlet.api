import re
import json
from datetime import datetime

from flask import Blueprint, abort, render_template, request, redirect, session, url_for, flash
import app.forms as f
from app import db
from app.models import User, Question, Quiz, Choice, QuizResult, UserChoice, QuizVisibility
from copy import copy

main = Blueprint('main', __name__, template_folder='templates')


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
        # print(users[1].quizzes_results[0])
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
            print(tuple([request.form[val]
                         for val in ['name', 'email', 'password']]))
            guest = User.create(tuple([request.form[val]
                                       for val in ['name', 'email', 'password']]))
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
            user = User.query.filter_by(
                email=request.form['email'], password=request.form['password']).first()
            session['user'] = user
            if user is None:
                return 'User does not exist'
            else:
                return redirect(url_for('main.user_profile'))
        else:
            return 'Invalid info has been sent to Flask'


@main.route('/user_profile', defaults={'page': 'user_profile'}, )
def user_profile(page):
    if 'user' in session and session['user']:
        return render_template('user_profile.html', user=session['user'])
    else:
        return redirect(url_for('main.signin_page'))


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
        quizzes = Quiz.query.filter_by(visibility=QuizVisibility.Public).all()
        return render_template('%s.html' % page, user=session['user'], quizzes=quizzes)

    return redirect(url_for('main.logout'))


# logout session
@main.route('/created_quizzes', )
def created_quizzes():
    if 'user' in session and (user := session['user']):
        quizzes = Quiz.query.filter_by(user_email=user.email).all()
        return render_template('created_quizzes.html', user=session['user'], quizzes=quizzes)
    return redirect(url_for('main.logout'))


# logout session
@main.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if 'user' in session and (user := session['user']):
        form = f.QuizForm(request.form)
        if request.method == 'POST' and form.validate():
            user = User.query.filter_by(email=user.email).first()
            quiz = Quiz(user=user, limited_time=int(form.limited_time.data), title=form.title.data,
                        access_code=form.access_code.data, visibility=form.visibility.data,
                        questions=[Question(correct_answer=i['correct_answer'], content=i['content'],
                                            choices=[Choice(content=c["content"]) for c in i['choices']]) for i in
                                   form.questions.data])
            user.created_quizzes.append(quiz)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.user_profile'))
        session['quiz'] = {
            "title": "",
            "access_code": "",
            "limited_time": "",
            "visibility": "Public",
            "questions": [],
        }
        form = f.QuizForm(data=session["quiz"])
        return render_template('create_quiz.html', form=form, get_index=get_index, get_index_int=get_index_int)
    return redirect(url_for('main.logout'))


def get_index(question):
    return int(question.name.split('-')[-1]) + 1


def get_index_int(question):
    return int(question.name.split('-')[-1])


@main.route('/clear_quiz')
def clear_quiz():
    session['quiz'] = {
        "title": "",
        "access_code": "",
        "limited_time": "",
        "visibility": "Public",
        "questions": [],
    }
    form = f.QuizForm(data=session["quiz"])
    return render_template('create_quiz.html', form=form, get_index=get_index, get_index_int=get_index_int)


@main.route('/add_question', methods=["PUT"])
def add_question():
    form = f.QuizForm(request.form)
    form.questions.append_entry(copy(f.NEW_QUESTION))
    return render_template('questions_form.html', form=form, get_index=get_index, get_index_int=get_index_int)


@main.route('/search_quizzes/<keywords>')
def search_quizzes(keywords):
    if 'user' in session and (user := session['user']):
        if keywords:
            # quizzes = Quiz.query.filter(Quiz.title.like(f"{keywords}%")).all()
            # quizzes = Quiz.query.filter(Quiz.title.startswith(keywords)).all()
            # quizzes = db.session.query(Quiz).filter(Quiz.title.op('regexp')(".*t.*"))
            quizzes = Quiz.query.filter(Quiz.title.startswith(keywords)).all()
            print(len(quizzes))
            return render_template('quizzes.html', user=user, quizzes=quizzes)
        else:
            return render_template('search_quizzes.html', user=user, quizzes=[])
    return redirect(url_for('main.logout'))


@main.route('/quizzes/<quiz_id>/settings', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    if 'user' in session and (user := session['user']):
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        form = f.QuizForm(request.form)
        if request.method == 'POST':
            user = User.query.filter_by(email=user.email).first()
            quiz.id = quiz.id
            quiz.title = form.title.data
            quiz.access_code = form.access_code.data
            quiz.visibility = form.visibility.data
            quiz.limited_time = int(form.limited_time.data)
            for i, question in enumerate(quiz.questions):
                try:
                    question.content = form.questions.data[i]['content']
                    question.correct_answer = form.questions.data[i]['correct_answer']
                    for ci, choice in enumerate(question.choices):
                        try:
                            choice.content = form.questions.data[i]['choices'][ci]['content']
                        except:
                            db.session.delete(choice)
                except:
                    db.session.delete(question)
            if len(quiz.questions) < len(form.questions.data):
                start = len(form.questions.data) - len(quiz.questions)
                for i in range(start, len(form.questions.data)):
                    quiz.questions.append(Question(
                        content=form.questions.data[i]['content'],
                        correct_answer=form.questions.data[i]['correct_answer'],
                        choices=[
                            Choice(content=c['content']) for c in form.questions.data[i]['choices']
                        ]
                    ))
            db.session.add(quiz)

            db.session.commit()
            return redirect(url_for('main.user_profile'))
        session["quiz"] = {
            "title": quiz.title,
            "access_code": quiz.access_code,
            "visibility": quiz.visibility,
            "questions": quiz.questions_dict,
            "limited_time": quiz.limited_time,
        }
        form = f.QuizForm(data=session["quiz"])
        return render_template('create_quiz.html', quiz=quiz, form=form, get_index=get_index,
                               get_index_int=get_index_int, is_editing=True)
    return redirect(url_for('main.logout'))


@main.route('/quizzes/<quiz_id>/questions', methods=['GET', 'POST'])
def edit_quiz_questions(quiz_id):
    if not 'user' in session or not session['user']:
        return redirect(url_for('main.logout'))

    if request.method == 'GET':
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        return render_template('quiz_questions.html', quiz_name=quiz.title, quiz_id=quiz.id)
    # elif request.method == 'POST':
    # return "Edit Quiz Questions"


@main.route('/quizzes/<quiz_id>/attempt', methods=['GET', 'POST'])
def attempt_quiz(quiz_id):
    if not 'user' in session or not session['user']:
        return redirect(url_for('main.logout'))

    if request.method == 'GET':
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        
        questions_json = [{'text': question.content,
                           'question_id': question.id} for
                          question in questions]

        for question, question_json in zip(questions, questions_json):
            question_id = question.id
            choices = Choice.query.filter_by(question_id=question_id)
            question_json['choices'] = [{'content': choice.content,
                                         'choice_id': choice.id} for choice in choices]

        questions_json = json.dumps(questions_json, sort_keys=True)

        return render_template('quiz_attempt.html', questions = questions_json)
    elif request.method == 'POST':    
        user = session['user']
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        quiz_result = QuizResult(user_email = user.email, quiz_id = quiz_id, user_choices = [])

        f = request.form
        for key in f.keys():
            if key.startswith('question_'):
                choice_id = f[key]
                choice = Choice.query.filter_by(id=choice_id).first()
                quiz_result.user_choices.append(
                    UserChoice(choice_id=choice_id, answer_right=False)
                )

        db.session.add(quiz_result)
        db.session.commit()

        return 'Attempt submitted'

# Validate data format is correct šäguöräñ
def validate(text, pattern):
    regex = re.compile(pattern, re.I)
    match = regex.match(request.form[text])
    return bool(match)
