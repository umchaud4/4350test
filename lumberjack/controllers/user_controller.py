from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from lumberjack import app, login_manager, open_id
from lumberjack.models.user import User
from lumberjack.forms import LoginForm

@app.route("/login", methods=['GET', 'POST'])
@open_id.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home_index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        session['username'] = form.username.data
        return open_id.try_login(form.openid.data, ask_for = ['email'])
    return render_template('users/login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route("/")
def home_index():
    return render_template("test.html")

@app.route("/users/")
def users_index():
    users = User.all()
    output = ""
    for user in users:
        output += user.user_name + "\n"
    return output

@app.route("/users/new")
def new_user():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
    return render_template('users/new.html', form=form)

@login_manager.user_loader
def load_user(id):
    return User.find_by_id(int(id))

@app.before_request
def before_request():
    g.user = current_user

@open_id.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.find_by_email(resp.email)
    user_name = session['username']
    if user is None:
        user = User(user_name = user_name, email = resp.email, password = "temp")
        User.save_to_db(user)
    else:
        if user.user_name != user_name:
            flash('Username does not match open id. Try again.')
            return redirect(url_for('login'))

    session.pop('username', None)
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
