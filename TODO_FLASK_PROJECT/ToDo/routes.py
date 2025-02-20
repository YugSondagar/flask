from ToDo import app, db, bcrypt
from flask import render_template, flash, redirect, url_for, request,abort
from ToDo.forms import RegistrationForm, LoginForm, UpdateForm, newTask
from ToDo.models import User,Task
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:  #CHECKS IF THE USER IS LOGGED IN
        tasks = Task.query.filter_by(user_id=current_user.id).all()
    else:
        tasks = []  
    return render_template('home.html',title='Home',tasks=tasks)

@app.route("/about")
def about():
    email="yug.sondagar11@gmail.com"
    return render_template('about.html',title='About', email=email)

@app.route("/register",methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data,email = form.email.data,password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('User Added Successfully', 'success')
        return redirect(url_for('login'))

    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash("You have been successfully","success")
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessfull","danger")

    return render_template('login.html',title='Login',form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account",methods=["POST","GET"])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated","success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html',title='Account',form = form)

@app.route("/task/new", methods=['POST', 'GET'])
@login_required
def new_task():
    form = newTask()
    if form.validate_on_submit():
        task = Task(context=form.context.data, user_id=current_user.id)  
        db.session.add(task)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('home'))
    return render_template('newtask.html', title='New Task', form=form, legend='New Task')





