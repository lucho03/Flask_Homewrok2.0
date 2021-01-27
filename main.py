from flask import Flask, render_template, url_for, flash, redirect
from forms import Registration, Login
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '0\xa5\x87-\xad\xa2z\x10d\xaf\x9br\xf8\x9f\x0c\xcbt\xe5\x83\x98'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from database import User, Post

posts = [
    {
        'author': 'Az',
        'title': 'Proba',
        'content': 'nqkwo sydyrzhanie',
        'date': '26.01.2021'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About you')

@app.route('/register', methods=['GET', 'POST'])
def regiter():
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} is  created susccessfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        if form.username.data:
            flash('You are logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Unsuccessfull login!', 'danger')
    return render_template('login.html', form=form)