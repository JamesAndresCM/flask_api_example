import os
from ConfigParser import SafeConfigParser
config = SafeConfigParser(os.environ)

config.read('db_conf.conf')

class developmentConfig(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://' + config.get('DB', 'user') + ':' + config.get('DB', 'password') + '@' + config.get('DB', 'host') + '/' + config.get('DB', 'db')
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_POOL_SIZE = 100
	SQLALCHEMY_POOL_RECYCLE = 280