import re
from flask import jsonify
from models import Persona

def validate_fields(data_field):
	edad = False
	nombre = False
	apellido = False
	ciudad = False

	if data_field:
		if str(data_field[0]).isdigit():
			edad = True
		else:
			value = "el valor %s no es valido como edad" % (data_field[0])
		if re.match('[a-zA-Z]', data_field[1]):
			nombre = True
		else:
			value = "el valor %s no es valido como nombre" % (data_field[1])
		if re.match('[a-zA-Z]', data_field[2]):
			apellido = True
		else:
			value = "el valor %s no es valido como apellido" % (data_field[2])
		if re.match('[a-zA-Z]', data_field[3]):
			ciudad = True
		else:
			value = "el valor %s no es valido como ciudad" % (data_field[3])
		if edad == True and nombre == True and apellido == True and ciudad == True:
			return True
		else:
			return jsonify(data=value,status_code=400)

def validate_pet(data_field):
	edad = False
	nombre = False
	owner = False

	if data_field:
		if str(data_field[0]).isdigit():
			edad = True
		else:
			value = "el valor %s no es valido como edad" % (data_field[0])
		if re.match('[a-zA-Z]', data_field[1]):
			nombre = True
		else:
			value = "el valor %s no es valido como nombre" % (data_field[1])
		if str(data_field[2]).isdigit():
			owner = True
		else:
			value = "el valor %s no es valido como id_owner" % (data_field[2])

		if edad == True and nombre == True and owner == True:
			return True
		else:
			return jsonify(data=value,status_code=400)

def toResponse(persona):
	response = {
		'id_persona': persona.id_persona,
		'persona_edad': persona.persona_edad,
		'persona_nombre': persona.persona_nombre,
		'persona_apellido': persona.persona_apellido,
		'persona_ciudad': persona.persona_ciudad,
		'created_date': persona.created_date,
	}
	return response


def toResponsePetDetail(pet):
	owner_name = ("%s %s") % (pet.owner.persona_nombre, pet.owner.persona_apellido)
	response = {
		'id_pet': pet.id_pet,
		'pet_edad': pet.pet_edad,
		'pet_nombre': pet.pet_nombre,
		'created_date': pet.created_date,
		'owner': owner_name
	}
	return response

def toResponsePet(data_pet):
	data_all = {}
	final = []

	if data_pet:
		for pet in data_pet:
			#values = [pet.persona_nombre,pet.persona_apellido]
			data_all["pet_edad"] = pet.pet_edad
			data_all["id_pet"] = pet.id_pet
			data_all["pet_nombre"] = pet.pet_nombre
			data_all["created_at"] = pet.created_date
			data_all["owner"] = ("%s %s") % (pet.persona_nombre ,pet.persona_apellido)
			final.append(data_all.copy())
		return final

def check_owner(name):
	owner = Persona.query.filter_by(id_persona=name).first()
	if owner:
		return owner
	else:
		return False
