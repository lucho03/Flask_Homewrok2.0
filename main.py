from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'p\xee\xeb>\x077\xef\x0e\x87P\xbe\xbcV\xcaVv\x90\xc2\xe8\x1eB*C\xf5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from database import User, Post
from forms import Registration, Login

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Unsuccessfull login!', 'danger')
    return render_template('login.html', form=form)