### adaptive_quizlet.api
##### Run project steps on Windows 10
1. Open command prompt at project folder
2. Activate python virtual environment(venv), run
```cmd
set FLASK_APP=app.py
pip install -r requirements.txt
flask run
```

##### Using Flask framework for backend development 
https://flask.palletsprojects.com/en/1.1.x/

##### Using Jinja2 framework for backend development 
https://jinja.palletsprojects.com/en/2.11.x/

##### Project Members
- Maanas Arora, 301104048
- Hassan Shabbir, 301031788
- Kangle Jiang, 300952654
- Hossain Nahid, 300711226
- Shota Ito, 301103095
- Sarmad Siddiqi, 300978624
- Dharun Raju, 301030187

### Schemas
#### Quiz 
field|type|
---|--- |
id|int| 
questions|list| 
title|str| 
limited_time|int| 
posted_at|datetime|

#### Question
field|type|
---|--- |
id | int|
quiz_id|int|
choices|list|
content| str|

#### Choice
field|type|
---|--- |
id | int|
question_id|int|
content| str|
correct| bool|
