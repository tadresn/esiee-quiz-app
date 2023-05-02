from flask import Flask, request
from flask_cors import CORS
import jwt_utils
import db_utils

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def PostLogin():
	payload = request.get_json()
	if payload['password'] == "flask2023":
		token = jwt_utils.build_token()
		return {"token":token}, 200
	return {"error": "Unauthorized"}, 401

@app.route('/questions', methods=['POST'])
def PostQuestion():
	auth_header = request.headers.get('Authorization')
	if auth_header is None:
		return {"error": "Authorization header missing"}, 401
	
	auth_token = auth_header.split(" ")[1]
	user = jwt_utils.decode_token(auth_token)
	if(user != "quiz-app-admin"):
		return {"error": "Unauthorized"}, 401
	
	payload = request.get_json()
	question_id =  db_utils.DataBase().insert_db(db_utils.Question().dict_to_question(payload))
	return {"id":question_id}, 200

@app.route('/rebuild-db', methods=['POST'])
def PostRebuildDB():
	db = db_utils.DataBase()
	db.rebuild_db()
	return "Ok", 200

if __name__ == "__main__":
    app.run()