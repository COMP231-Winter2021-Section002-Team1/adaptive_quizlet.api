from flask import Flask, render_template, request, g, current_app
import sqlite3
import re

app = Flask(__name__)

################################################################################
# Database Configuration

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

init_db()

################################################################################

@app.route('/')
def home_page():
    users = query_db('SELECT * FROM user')
    return render_template('index.html', users = users)



def validate(text, pattern):
    regex = re.compile(pattern, re.I)
    match = regex.match(text)
    return bool(match)

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('signup.html')

    elif request.method == 'POST':
        if (validate(request.form['name'], '(\w| )+')
            and validate(request.form['email'], '.+\@.+\..+') 
            and validate(request.form['password'], '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
        ):
            db = get_db()
            db.execute('INSERT INTO user (name, email, password) VALUES (?, ?, ?)', 
                    tuple([request.form[val] for val in ['name', 'email', 'password']]))
            db.commit()

            return 'Vaild info has been sent to Flask'
        else:
            return 'Invalid info has been sent to Flask'



@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
    if request.method == 'GET':
        return render_template('signin.html')

    elif request.method == 'POST':
        if (validate(request.form['email'], '.+\@.+\..+') 
            and validate(request.form['password'], '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
        ):
            user = query_db('SELECT * FROM user WHERE email = ? AND password = ?', (request.form['email'], request.form['password']), one=True)
            if user is None:
                return 'User does not exist'
            return user
        else:
            return 'Invalid info has been sent to Flask'



if __name__ == '__main__':
    app.run()
