import enum
from datetime import datetime

from . import db


class QuizVisibility(enum.Enum):
    Public = "Public"
    Private = "Private"

    def __str__(self):
        return self.value


class UserChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_email = db.Column(db.String(120), db.ForeignKey('take_quiz_history.user_email'), primary_key=True),
    quiz_result_id = db.Column(db.Integer, db.ForeignKey('quiz_result.id'))
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'))
    answer_right = db.Column(db.Boolean, nullable=False)


class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    created_quizzes = db.relationship("Quiz", backref='user', lazy=True)
    quizzes_results = db.relationship("QuizResult", backref='user', lazy=True)

    @staticmethod
    def create(args):
        return User(name=args[0], email=args[1], password=args[2])


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_choices = db.relationship("UserChoice", backref='choice', lazy=True)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    choices = db.relationship("Choice", backref='question', lazy=True)
    correct_answer = db.Column(db.Text, nullable=False)


class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_choices = db.relationship("UserChoice", backref='quiz_result', lazy=True)

    def __str__(self):
        return f"{self.quiz.title} quiz result is {len([x for x in self.user_choices if x.answer_right]) / len(self.user_choices) * 100}%."


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    access_code = db.Column(db.String(80))
    limited_time = db.Column(db.Integer)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    questions = db.relationship("Question", backref='quiz', lazy=True)
    num_of_questions = db.Column(db.Integer, default=0)
    visibility = db.Column(db.Enum(QuizVisibility), default=QuizVisibility.Public)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), )
    quiz_results = db.relationship("QuizResult", backref='quiz', lazy=False)

    @property
    def posted_at_string(self):
        return self.posted_at.strftime("%B %d, %Y %H:%M:%S")

    @property
    def questions_count(self):
        return len(self.questions)

    @property
    def questions_dict(self):
        return [
            {
                "content": i.content,
                "correct_answer": i.correct_answer,
                "choices": [
                    {
                        "content": i.choices[0].content
                    }, {
                        "content": i.choices[1].content
                    }, {
                        "content": i.choices[2].content
                    }
                ]
            }
            for i in self.questions
        ] if self.questions else {}

    def __repr__(self):
        return '<Post %r>' % self.title
