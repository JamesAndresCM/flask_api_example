import os
import ConfigParser

config = ConfigParser.ConfigParser()  
config.read('db_conf.conf')

class developmentConfig(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://' + config.get('DB', 'user') + ':' + config.get('DB', 'password') + '@' + config.get('DB', 'host') + '/' + config.get('DB', 'db')
	SQLALCHEMY_TRACK_MODIFICATIONS = True