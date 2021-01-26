from flask import Flask, render_template, url_for, flash, redirect
from forms import Registration, Login
app = Flask(__name__)

app.config['SECRET_KEY'] = '812bdubdqwpojdoiqd'

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
        flash(f'{form.username.data} is  created susccessfully!', 'success')
        return redirect(url_for('home'))
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