### adaptive_quizlet.api

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

### Schemes
#### Quiz 
field|type|
---|--- |
id|int| 
taker_id|int| 
maker_id|int| 
question_id|int| 
title|str| 
limited_time|int| 
posted_at|datetime|

#### Question
field|type|
---|--- |
id | int|
quiz_id|int|
answer_id|int|
content| str|

#### Answer
field|type|
---|--- |
id | int|
question_id|int|
content| str|
