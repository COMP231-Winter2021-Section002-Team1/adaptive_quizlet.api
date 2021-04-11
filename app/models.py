from . import db
from datetime import datetime

available_quizzes = db.Table('available_quizzes',
                             db.Column("user_email", db.String(120), db.ForeignKey('user.email'), primary_key=True),
                             db.Column("quiz_id", db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
                             )


class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    user_quizzes = db.relationship('Quiz', secondary=available_quizzes, lazy='subquery',
                                   backref=db.backref('user', lazy=True))

    @staticmethod
    def create(args):
        return User(name=args[0], email=args[1], password=args[2])


#
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    correct = db.Column(db.Boolean, default=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    choices = db.relationship("Choice", backref='quiz', lazy=True)
    actual_answer = db.Column(db.Integer)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    limited_time = db.Column(db.Integer, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    questions = db.relationship("Question", backref='quiz', lazy=True)

    def __repr__(self):
        return '<Post %r>' % self.title
