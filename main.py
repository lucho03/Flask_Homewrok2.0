from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import secrets
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'p\xee\xeb>\x077\xef\x0e\x87P\xbe\xbcV\xcaVv\x90\xc2\xe8\x1eB*C\xf5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

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

def save_image(form_image):
    random = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_image.filename)
    image_fn = random + f_ext
    image_path = os.path.join(app.root_path, 'static/pics', image_fn)
    form_image.save(image_path)
    return image_fn

@app.route('/register', methods=['GET', 'POST'])
def regiter():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.image.data:
            image = save_image(form.image.data)
            user = User(username=form.username.data, password=hashed_password, image=image)
        else:
            user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} is  created susccessfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Unsuccessfull login!', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename='pics/' + current_user.image)
    return render_template('account.html', image_file=image_file)
