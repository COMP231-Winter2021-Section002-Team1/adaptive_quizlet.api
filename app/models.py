from . import db
from datetime import datetime


class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    @staticmethod
    def create(*args):
        return User(name=args[0], email=args[1], password=args[2])


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    limited_time = db.Column(db.Integer, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    questions = db.relationship("Question",
                             primaryjoin="and_(Quiz.id==Question.quiz_id,)")

    def __repr__(self):
        return '<Post %r>' % self.title


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    choices = db.relationship("Choice", primaryjoin="and_(Question.id==Choice.question_id,)")


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    correct = db.Column(db.Boolean, default=False)
