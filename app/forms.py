from wtforms import Form, BooleanField, StringField, PasswordField, validators, FieldList, SelectField, FormField, IntegerField
from copy import copy


class ChoiceForm(Form):
    content = StringField("Content", [validators.Length(min=1, max=500)])


class QuestionForm(Form):
    correct_answer = StringField("Correct Answer", [validators.Length(min=1, max=500)])
    content = StringField("Content", [validators.Length(min=1, max=500)])
    choices = FieldList(FormField(ChoiceForm))


class QuizForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=300)])
    access_code = StringField('Access Code', [validators.Length(min=0, max=20)])
    limited_time = IntegerField('Limited Time(Minutes)', [validators.number_range(min=0, max=500)])
    visibility = SelectField('Visibility', choices=["Public", "Private"])
    questions = FieldList(FormField(QuestionForm))


NEW_QUESTION = {
    "correct_answer": "",
    "choices": [
        {
            "content": ""
        }, {
            "content": ""
        }, {
            "content": ""
        }
    ]
}
NEW_QUIZ = {
    "title": "",
    "access_code": "",
    "visibility": "Public",
    "questions": [
        copy(NEW_QUESTION)
    ],
}
EDITING_QUIZ: dict = {}

