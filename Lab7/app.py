from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import re 

app = Flask(__name__)
conn = sqlite3.connect('credentials.db', check_same_thread = False)

@app.route('/', methods=['POST','GET'])
def signUp():
    if request.method =='POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['pwd']
        confirm_password = request.form['cpwd']

        if password == confirm_password:
            print("Password matches")
            

            validation_errors = validate_password(password)
            if not validation_errors:
                print("Password is valid!")
                with conn:
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM credentials WHERE email = ?",(email,))
                    users = cur.fetchone()
                    if users:
                        return render_template('signup.html',userStatus="User Already exists.")
                        
                    else:
                        cur.execute("INSERT INTO credentials(fname,lname,email,password) values (?,?,?,?)", (fname,lname,email,password))
                        return render_template('signupSucc.html')
            else:
                print("Password is invalid. Errors:")
                for error in validation_errors:
                    print(error)
                return render_template('signup.html',pwdFailures=validation_errors)
        else:
            print('Password did not match')
            return render_template('signup.html',passwordError="Password is not matching")

    else:
        return render_template('signup.html')


def validate_password(password):
    min_length = 8
    has_uppercase = re.compile(r'[A-Z]')
    has_lowercase = re.compile(r'[a-z]')
    has_number = re.compile(r'\d')

    errors = []

    if len(password) < min_length:
        errors.append("Password must be at least 8 characters long.")

    if not has_uppercase.search(password):
        errors.append("Password must contain at least one uppercase letter.")

    if not has_lowercase.search(password):
        errors.append("Password must contain at least one lowercase letter.")

    if not has_number.search(password):
        errors.append("Password must contain at least one number.")

    return errors

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['pwd']
        print('email',email)
        print('password',password)
        connection = sqlite3.connect("credentials.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM credentials WHERE email = ? AND password = ?",(email,password))
        users = cursor.fetchall()
        if users:
            connection.close()
            return render_template('loginSucc.html')
        else:
            connection.close()
            return render_template('login.html',userStatus="Username or password missmatch")
    else:
        return render_template('login.html')
    

if __name__ == "__main__":
    with conn:
        crsr = conn.cursor()
        crsr.execute('''CREATE TABLE IF NOT EXISTS credentials (
            id integer primary key autoincrement,
            fname varchar(20) not null,
            lname varchar(20) not null,
            email varchar(20) not null,
            password varchar(20) not null

        )''')
    app.run(debug=True)