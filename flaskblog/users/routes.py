from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post

from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                                 RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
       
        #Hashing the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        #Populating the object we about to enter in the database
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        #Commit the changes       
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now logged in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    #If the current user is logged in, there is no way her can log in again
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #This method can log us in and take care of the sessio data to remember the user
            login_user(user, remember=form.remember.data)

            #Getting the next in the url
            next_page = request.args.get('next')
            return redirect(next_page) if  next_page else redirect(url_for('main.home'))

        else:
            flash('Login unsuccessful, Please check your credentials!', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user() #It takes no argument, because it knows the current session
    return redirect(url_for('users.login'))



@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    
    #This return the just filled form
    form = UpdateAccountForm()

    #If the form validates || if none is missing on the validation defined at this class
    if form.validate_on_submit():

        #If we have the form data
        if form.picture.data:
            #We will save the picture on the browser session data
            picture_file = save_picture(form.picture.data)

            #We will assign the current user image to the picture_file
            current_user.image_file = picture_file

        #We assign again the username and email to the current_user session
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        #We save it in the database
        db.session.commit()
        
        flash('Your account has been updated!', 'success')

        #If He has successfully update we will redirect him to call the account function
        return redirect(url_for('users.account'))

    #If form is not validated
    elif request.method == 'GET':
        #The form will continue to show the current_user info
        form.username.data = current_user.username
        form.email.data = current_user.email
    #Image file will continue to be the image of the current user
    image_file = url_for('static', filename=current_user.image_file)
    #We will render the account page / pretty much he will stay where he is, we will pass in form data and image_file and 
    #It will surely throw an error
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
           .order_by(Post.date_posted.desc())\
           .paginate(page=page, per_page=5)

    return render_template('user_posts.html', posts=posts, user=user)




#--------------------------------------- Reseting password---------------------------------------------------------

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    #If the current user is logged in, there is no way her can log in again
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        print(form.email.data)
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<string:token>", methods=['GET', 'POST'])
def reset_token(token):
    #If the current user is logged in, there is no way her can log in again
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
   
        #Hashing the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash(f'Your password has been updated! You are now logged in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

