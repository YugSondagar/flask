import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm,LoginForm,UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskblog.models_blog import User, Post
from flask_login import login_user, current_user, logout_user,login_required
from flask_mail import Message

@app.route("/")
@app.route("/home_blog")
def home():
    page = request.args.get('page',1,type=int) #yaha pe 1 default parameter hai
    # posts = Post.query.all() 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) 
    return render_template('home_blog.html',posts = posts,title='Home') 

@app.route("/about_blog")
def about():
    email = "yug.sondagar11@gmail.com"
    return render_template('about_blog.html',title= 'About',email = email)

@app.route("/register_blog",methods=['GET','POST'])  #what does method do agar hamlog register karne ke liye form bhej rhe hai tho ek method not found vala error aarha hai this is bcoz it is submitting the post request back to the same register route with form data but we are not allowing to do so.
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))   #it will redirect to the login page 
    return render_template('register_blog.html',title='register',form = form)

@app.route("/login_blog",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember = form.remember.data)   #iska defination models_blog.py mein hai
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))      #This line is used in Flask to get a query parameter from the URL.

 
        else:
            flash('Login Unsuccessful' , 'danger')

    return render_template('login_blog.html',title= 'login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hx = secrets.token_hex(8)  #in order to prevent the picture from being saved with the same name
    
    # in order to grap the file extension from the file that they uploaded we can use the os module
    _, f_ext = os.path.splitext(form_picture.filename)  
    # os.path.splitext() is a Python function from the os.path module that splits a filename into two parts:
    # The main filename (without extension)
    # The file extension (including the dot .)

    picture_fn = random_hx + f_ext  #picture file name variable
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)  #picture path variable

    #image resizing from pillow package  --> why we need to do it ? it will save lots of space in the file system 
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)    
    i.save(picture_path)

    return picture_fn


@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated','success')
        redirect(url_for('account'))
    elif request.method == 'GET':    #it will help in updating the form fields with the current user's data
    #A GET request is one of the HTTP methods used to retrieve data from a server
        form.username.data = current_user.username
        form.email.data = current_user.email
        

    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account_blog.html',title='Account',image_file = image_file, form = form)


@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_posts():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data,author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been addedd ','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Posts',form=form , legend = 'New Post')

#creating routes that will take us to a specific post
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)  #get_or_404 matlab agar id exist kar rha hai tho post de do varna 404 error de do
    #when we have integer always prefer using get  
    return render_template('post.html',title=post.title,post=post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title = 'update post',form = form, legend = 'Update Post')
  # we are not going to create a seprate route for update post because we are going to use the same form as we used in creating a post so we are going to pass legend that will update from new post to update post

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))

#function to send password on email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='your_email@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('reset_token', token = token, _external = True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
#why _external = True --->> In order to get absolute url rather than relative url
    mail.send(msg)

@app.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent.', 'info')
        return redirect(url_for(login))
    return render_template('reset_request.html',title='Reset Password', form=form)
#it is the route where user will send the request to resend the password

#this is the route where the user will actually resend the password   
#email ke link pe click karne ke baad ye vala aayega
@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_resent_token(token)
    if not user:
        flash('Invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset Password', form=form)