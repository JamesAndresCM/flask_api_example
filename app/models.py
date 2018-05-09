from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy()

class Persona(db.Model):  
	__tablename__ = 'personas'
	id_persona = db.Column(db.Integer, primary_key=True)
	persona_edad = db.Column(db.Integer, nullable=False)
	persona_nombre = db.Column(db.String(128), nullable=False)
	persona_apellido = db.Column(db.String(128), nullable=False)
	persona_ciudad = db.Column(db.String(128), nullable=False)
	created_date = db.Column(db.DateTime, default=datetime.datetime.now)
	pets = db.relationship('Pet', backref='owner',passive_deletes=True)

	def __repr__(self):
		return '<Persona (%s, %s, %s, %s) >' % (self.persona_edad, self.persona_nombre, self.persona_apellido, self.persona_ciudad)

class Pet(db.Model):
	__tablename__ = 'pets'
	id_pet = db.Column(db.Integer, primary_key=True)
	pet_nombre = db.Column(db.String(128), nullable=False)
	pet_edad = db.Column(db.Integer, nullable=False)
	owner_id = db.Column(db.Integer, db.ForeignKey('personas.id_persona',ondelete='CASCADE'))
	created_date = db.Column(db.DateTime, default=datetime.datetime.now)

	def __repr__(self):
		return '<Pet (%s, %s, %s, %s) >' % (self.pet_nombre, self.pet_edad,self.owner_id,self.created_date)