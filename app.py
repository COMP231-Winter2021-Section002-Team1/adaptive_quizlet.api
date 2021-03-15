from flask import Flask, render_template, request, g, current_app
import sqlite3

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
    user = query_db('SELECT * from user', one=True)
    return render_template('index.html', user = user)

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        # TODO insert request.form['name'] into database
        return 'You have posted to the signup page'

@app.route('/signin')
def signin_page():
    return 'This is the signin page'

if __name__ == '__main__':
    app.run()
