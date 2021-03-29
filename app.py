# # Flask web framework
# from flask import Flask, render_template, request, g, redirect, session, url_for, flash
# # Database
# # Regular Expressions
# import re
#
# # Initialize
# app = Flask(__name__)
# app.secret_key = 'hello' # secretkey for session
#
# ################################################################################
# # Database Configuration and Helpers
#
# # SQLite database storage file
# DATABASE = 'database.db'
#
# # Connect to SQLite and return dicts from db
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#
#     def make_dicts(cursor, row):
#         return dict((cursor.description[idx][0], value)
#                     for idx, value in enumerate(row))
#
#     db.row_factory = make_dicts
#     return db
#
#
# # Query helper function
# def query_db(query, args=(), one=False):
#     cur = get_db().execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv
#
#
# # Db connection close helper function
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
#
#
# # Db schema and data initializer
# def init_db():
#     with app.app_context():
#         db = get_db()
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()
#
# init_db()
#
#
# ################################################################################
# # Routes
#
# # Show db values on home page
# @app.route('/')
# def home_page():
#     users = query_db('SELECT * FROM user')
#     return render_template('index.html', users = users)
#
#
#
# # Validate data format is correct
# def validate(text, pattern):
#     regex = re.compile(pattern, re.I)
#     match = regex.match(request.form[text])
#     return bool(match)
#
# # Show signup form and process and save returned form data
# @app.route('/signup', methods=['GET', 'POST'])
# def signup_page():
#     if request.method == 'GET':
#         return render_template('signup.html')
#
#     elif request.method == 'POST':
#         if (validate('name', '(\w| )+')
#             and validate('email', '.+\@.+\..+')
#             # and validate('password', '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
#         ):
#             db = get_db()
#             db.execute('INSERT INTO user (name, email, password) VALUES (?, ?, ?)',
#                     tuple([request.form[val] for val in ['name', 'email', 'password']]))
#             db.commit()
#
#             return 'Vaild info has been sent to Flask'
#         else:
#             return 'Invalid info has been sent to Flask'
#
#
# # Show signin form and return user if found
# @app.route('/signin', methods=['GET', 'POST'])
# def signin_page():
#     if request.method == 'GET':
#         return render_template('signin.html')
#
#     elif request.method == 'POST':
#         if (validate('email', '.+\@.+\..+')
#             # and validate('password', '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
#         ):
#             user = query_db('SELECT * FROM user WHERE email = ? AND password = ?',
#                     (request.form['email'], request.form['password']), one=True)
#             session['user'] = user
#             print(session['user'], "user to session")
#             if user is None:
#                 return 'User does not exist'
#             else:
#                 # return user
#                 return  redirect(url_for('home_page'))
#         else:
#             return 'Invalid info has been sent to Flask'
#
#
# # Could be used as a own quiz page
# @app.route('/user')
# def user():
#     if 'user' in session:
#         user = session['user']
#         return render_template('logged_in.html', user=user)
#     else:
#         return redirect(url_for('signin_page'))
#
# # logout session
# @app.route('/logout')
# def logout():
#     # print(session['user'], "before logout")
#     session['user'] = None # {..., 'user' : None}
#     flash("You have been logged out", "success")
#     return redirect(url_for('home_page'))
#
#
#
#
# # Initialize application
from app import create_app

if __name__ == '__main__':
    create_app().run()



