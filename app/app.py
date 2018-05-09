#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin 
from models import db
from models import Persona
from models import Pet
from config import developmentConfig
from validators import *

app = Flask(__name__)
app.config.from_object(developmentConfig)

@app.route("/")
def hello():  
	response = ["Endpoints","GET Persona /v1/personas","POST /v1/persona persona_edad=EDAD persona_nombre=NOMBRE persona_apellido=APELLIDO persona_ciudad=CIUDAD","DELETE /v1/persona/id",
	"PATCH /v1/persona/id persona_edad=EDAD persona_nombre=NOMBRE persona_apellido=APELLIDO persona_ciudad=CIUDAD", "GET /v1/persona/id",
	"GET /v1/pets", "POST /v1/pet pet_edad=EDAD pet_nombre=NOMBRE owner=PERSONA.ID","GET /v1/pet/id","PATCH /v1/pet/id pet_edad=EDAD pet_nombre=NOMBRE owner=PERSONA.id","DELETE /v1/pet/id"]
	return jsonify(data=response)

@app.route('/v1/personas', methods=['GET'])
@cross_origin()

def get_Persona():  
	data = Persona.query.all()
	data_all = []

	if data:
		for persona in data:
			res = toResponse(persona)
			data_all.append(res) 
		return jsonify(data=data_all,status_code=200)
	else:
		return jsonify(data="[] data not found",status_code=200)

@app.route('/v1/pets', methods=['GET'])
@cross_origin()

def get_Pet():
	data = Pet.query.join(Persona).add_columns(Pet.pet_nombre, Pet.id_pet,Pet.pet_edad,Persona.persona_nombre,Persona.persona_apellido, Pet.created_date)
	if data:
		res = toResponsePet(data)
		if res:
			return jsonify(data=res,status_code=200)
		else:
			return jsonify(data="[] data not found",status_code=200)

@app.route("/v1/pet/<int:id_pet>", methods=["GET"])
@cross_origin()

def pet_detail(id_pet):
	pet = Pet.query.filter_by(id_pet=id_pet).first()
	data = []
	if pet:
		res = toResponsePetDetail(pet)
		data.append(res)
		return jsonify(data=data,status_code=200)
	else:
		return jsonify(data=["El registro %s no existe " % str(id_pet)],status_code=404)

@app.route("/v1/persona/<int:id_persona>", methods=["GET"])
@cross_origin()

def user_detail(id_persona):
	persona = Persona.query.filter_by(id_persona=id_persona).first()
	data = []

	if persona:
		res = toResponse(persona)
		data.append(res)
		return jsonify(data=data,status_code=200)
	else:
		return jsonify(data=["El registro %s no existe " % str(id_persona)],status_code=404)

@app.route('/v1/persona/<int:id_persona>', methods=['DELETE'])
@cross_origin()

def delete_Persona(id_persona):

	curr_session = db.session
	p = Persona.query.filter_by(id_persona=id_persona).delete()
	curr_session.commit()
	if p:
		return jsonify(data=["El registro %s ha sido eliminado" % str(id_persona)],status_code=200)
	else:
		return jsonify(data=["Error no existe el registro %s " % str(id_persona)],status_code=404)


@app.route('/v1/pet/<int:id_pet>', methods=['DELETE'])
@cross_origin()

def delete_Pet(id_pet):

	curr_session = db.session
	p = Pet.query.filter_by(id_pet=id_pet).delete()
	curr_session.commit()
	if p:
		return jsonify(data=["El registro %s ha sido eliminado" % str(id_pet)],status_code=200)
	else:
		return jsonify(data=["Error no existe el registro %s " % str(id_pet)],status_code=404)


@app.route('/v1/persona', methods=['POST'])
@cross_origin()

def create_Persona():
	if request.headers['Content-Type'] == 'application/json':
		req_data = request.get_json(force=True)
		persona_edad = req_data['persona_edad']
		persona_nombre = req_data['persona_nombre']
		persona_apellido = req_data['persona_apellido']
		persona_ciudad = req_data['persona_ciudad']
		
		element = []
		element.extend([persona_edad, persona_nombre, persona_apellido, persona_ciudad])
		
		resp_val = validate_fields(element)
		if resp_val == True:
			persona = Persona(persona_edad=persona_edad, persona_nombre=persona_nombre, persona_apellido=persona_apellido, persona_ciudad=persona_ciudad)
			curr_session = db.session 
			try:
				curr_session.add(persona) 
				curr_session.commit() 
			except:
				curr_session.rollback()
				curr_session.flush() 
			id_persona = persona.id_persona
			data = Persona.query.filter_by(id_persona=id_persona).first()
			res = toResponse(persona)
	
			return jsonify(data=res, status_code=200)
		else:
			return resp_val
	else:
		return jsonify(data="Unsupported media only content-type application/json")


@app.route('/v1/pet', methods=['POST'])
@cross_origin()

def create_pet():
	if request.headers['Content-Type'] == 'application/json':
		req_data = request.get_json(force=True)
		pet_edad = req_data['pet_edad']
		pet_nombre = req_data['pet_nombre']
		owner_req = req_data['owner']

		owner_bd = check_owner(owner_req)
	
		if owner_bd:
			owner = owner_bd
			element = []
			element.extend([pet_edad, pet_nombre, owner_req])
			resp_val = validate_pet(element)
			
			if resp_val == True:
				#print owner
				pet = Pet(pet_nombre=pet_nombre, pet_edad=pet_edad, owner=owner)
				curr_session = db.session
				try:
					curr_session.add(pet)
					curr_session.commit()
				except:
					curr_session.rollback()
					curr_session.flush()
				id_pet = pet.id_pet
				data = Pet.query.filter_by(id_pet=id_pet).first()
				res = toResponsePetDetail(pet)
				return jsonify(data=res, status_code=200)	
			else:
				return resp_val
		else:
			return jsonify(data="no existe owner %s" % (owner_req))
	else:
		return jsonify(data="Unsupported media only content-type application/json")

@app.route('/v1/pet/<int:id_pet>', methods=['PATCH']) 
@cross_origin()

def update_Pet(id_pet):
	if request.headers['Content-Type'] == 'application/json':
		req_data = request.get_json(force=True)
		pet_edad = req_data['pet_edad']
		pet_nombre = req_data['pet_nombre']
		owner_req = req_data['owner']

		owner_bd = check_owner(owner_req)

		if owner_bd:
			owner = owner_bd
			element = []
			element.extend([pet_edad, pet_nombre, owner_req])
			resp_val = validate_pet(element)
			if resp_val == True:
				try:
					curr_session = db.session()
					pet = Pet.query.filter_by(id_pet=id_pet).first()
					pet.pet_edad = pet_edad
					pet.pet_nombre =  pet_nombre
					pet.owner_id = owner_req
					curr_session.commit()
				except:
					curr_session.rollback()
					curr_session.flush()
					return jsonify(data="error not found id %s" % (id_pet),status_code=400)
				id_pet = pet.id_pet
				data = Pet.query.filter_by(id_pet=id_pet).first()
				res = toResponsePetDetail(pet)
				return jsonify(data=res,status_code=200)
			else:
				return resp_val
		else:
			return jsonify(data="no existe owner %s" % (owner_req))
	else:
		return jsonify(data="Unsupported media only content-type application/json")


@app.route('/v1/persona/<int:id_persona>', methods=['PATCH']) 
@cross_origin()

def update_Persona(id_persona):
	if request.headers['Content-Type'] == 'application/json':
		req_data = request.get_json(force=True)
		persona_edad = req_data['persona_edad']
		persona_nombre = req_data['persona_nombre']
		persona_apellido = req_data['persona_apellido']
		persona_ciudad = req_data['persona_ciudad']
		element = []
		element.extend([persona_edad, persona_nombre, persona_apellido, persona_ciudad])

		resp_val = validate_fields(element)
		if resp_val == True:	
			curr_session = db.session()

			try:
				persona = Persona.query.filter_by(id_persona=id_persona).first()
				persona.persona_edad = persona_edad
				persona.persona_nombre =  persona_nombre
				persona.persona_apellido = persona_apellido
				persona.persona_ciudad = persona_ciudad
				curr_session.commit()
			except:
				curr_session.rollback()
				curr_session.flush()
				return jsonify(data="error not found id %s" % (id_persona),status_code=400)
				
			id_persona = persona.id_persona
			data = Persona.query.filter_by(id_persona=id_persona).first()
			res = toResponse(persona)
			return jsonify(data=res,status_code=200)
		else:
			return resp_val
	else:
		return jsonify(data="Unsupported media only content-type application/json")

@app.errorhandler(404)
def not_found(error=None):
	message = {'status': 404,'message': 'Not Found: %s ' % (request.url),}
	resp = jsonify(message)
	resp.status_code = 404
	return resp

@app.errorhandler(405)
def method_not_allowed(e):
	message = {'status': 405,'message': 'Method not allowed: %s ' % (request.url),}
	resp = jsonify(message)
	resp.status_code = 405
	return resp

if __name__ == "__main__":
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.run(host='0.0.0.0')