from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration to Set up a database with MariaDB in Linux. Works different on windows and apple. 
# Where it says "Here_you_write_your_password", you need to write your password. 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Here_you_write_your_password@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/my_status', methods=['GET', 'POST'])
def my_status():
    user_input = ""
    if request.method == 'POST':
        user_input = request.form.get('xss_input', '')
    return render_template('my_status.html', user_input=user_input)

@app.route('/log_in_page', methods=['GET', 'POST'])
def log_in_page():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        query_stmt = f"SELECT username FROM users WHERE username='{username}' AND password= '{password}'"

        result = db.engine.execute(query_stmt)
        user = result.fetchone()
        
        # Not safe to use 
        #user = result.fetchall()

        if user:
            message = f"Welcome, {username}"
        else:
            message = "Incorrect username or password"
    
    return render_template('log_in_page.html', message=message)

# Make a blacklist for some characters that may be harmful for the security of your database.
bad_chars = ["'", ",", ";", "-", "_"]

def black_list(uname):
    for char in bad_chars:
        if char in uname.lower():
            return True
    return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if black_list(username):
            message = "No Hacking please"
            return render_template('register.html', message=message)

        check_query = "SELECT username FROM users WHERE username=%s"
        user_exists = db.engine.execute(check_query, (username,)).fetchone()

        if user_exists:
            message = "Username already exists!"
        else:
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            db.engine.execute(insert_query, (username, password))

            message = "Registration successful!"

    return render_template('register.html', message=message)

@app.route('/redirect', methods=['GET'])
def redirect_page():
    return render_template('redirect.html')



if __name__ == '__main__':
    app.run(debug=True)