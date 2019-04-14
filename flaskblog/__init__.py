# Importing the flask class
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


#----------------------------------- Extesnsions  -------------------------------------------

#The database we are using here
db = SQLAlchemy()

#This help us hash the password
bcrypt = Bcrypt()

#This will help us use the current session information
login_manager = LoginManager()

#This will redirect the user to login if he is not logged in
login_manager.login_view = 'users.login'

#This will avoid to let the default image be printed
login_manager.login_message_category = 'info'


mail = Mail()


#-------------------------------------------  The function that creates our app ------------------------------------------------------------

def create_app(confi_class=Config):
	app = Flask(__name__)  # the name is the name of the module

	#Importing the environment variables
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	from flaskblog.errors.handlers import errors


	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app

