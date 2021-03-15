from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return 'This is the signup page'
    elif request.method == 'POST':
        return 'You have posted to the signup page'

@app.route('/signin')
def signin_page():
    return 'This is the signin page'

if __name__ == '__main__':
    app.run()
