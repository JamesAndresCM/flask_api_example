# Flask_api_example

Set user and password host to bd (mysql)

- file `.env (username, password, host,db)`

Install requirements

- `pip -r app/requirements.txt`

Execute app

- python app.py

Or use Docker
***
- Create container bd
* `docker run -d --name=db -e SET_CONTAINER_TIMEZONE=true -e CONTAINER_TIMEZONE=America/Santiago 
-e MYSQL_DATABASE=persona_example -e MYSQL_USER=user_api -e MYSQL_PASSWORD=api_test -e MYSQL_ROOT_PASSWORD=test 
--publish=3306:3306 mariadb`

- Build Dockerfile for flask
* `docker build -t flask_api .`

- Create container flask_api
* `docker run -d --log-driver=json-file --log-opt max-file=3 --log-opt max-size=50m --name=api_flask_persona 
--link=db:db --publish=5000:5000 -e HOST_DB=db -e DATABASE_DB=persona_example -e USER_DB=user_api 
-e PASSWD_USER_DB=api_test flask_api`

## Endpoints

### All personas
* `http :5000/v1/personas`

### Create persona
* `http POST :5000/v1/persona persona_edad=EDAD persona_nombre=NOMBRE persona_apellido=APELLIDO persona_ciudad=CIUDAD`

### Detail persona
* `http :5000/v1/persona/id`

### Update persona
* `http PATCH :5000/v1/persona/id persona_edad=EDAD persona_nombre=NOMBRE persona_apellido=APELLIDO persona_ciudad=CIUDAD`

### Delete persona
* `httpd DELETE :5000/v1/persona/id`

### All pets
* `http :5000/v1/pets`

### Create pet
* `http POST :5000/v1/pet pet_edad=EDAD pet_nombre=NOMBRE owner=PERSONA.ID`

### Detail pet
* `http :5000/v1/pet/id`

### Update pet
* `http PATCH :5000/v1/pet/id pet_edad=EDAD pet_nombre=NOMBRE owner=PERSONA.id`

### Delete pet
* `http DELETE :5000/v1/pet/id`
