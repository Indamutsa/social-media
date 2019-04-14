import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

	#Configuring the email
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

	#app.config['SECRET_KEY'] = '85a556b0d7d14b731dbb14d2ca75c8d1'
	#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'