from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration to Set up a database with MariaDB in Linux. Works different on windows and apple. 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_password@localhost/mydb'
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

if __name__ == '__main__':
    app.run(debug=True)