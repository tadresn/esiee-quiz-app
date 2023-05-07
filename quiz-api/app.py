from flask import Flask, request
from flask_cors import CORS
import jwt_utils
import db_utils
import models

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	db = db_utils.DataBase()
	size = db.count_questions()
	score = db.get_participation_results()
	return {"size": size, "scores": score}, 200

@app.route('/login', methods=['POST'])
def PostLogin():
	payload = request.get_json()
	if payload['password'] == "flask2023":
		token = jwt_utils.build_token()
		return {"token":token}, 200
	return {"error": "Unauthorized"}, 401
	
@app.route('/questions', methods=['POST'])
def PostQuestion():
	if(jwt_utils.is_unauthorizated(request.headers.get('Authorization'))):
		return {"error": "Unauthorized"}, 401
	
	payload = request.get_json()
	question = models.Question(payload["position"], payload["title"], payload["text"], payload["image"], payload["possibleAnswers"])
	db =  db_utils.DataBase()
	question_id = db.insert_question(question)
	return {"id":question_id}, 200

@app.route('/rebuild-db', methods=['POST'])
def PostRebuildDB():
	db = db_utils.DataBase()
	db.rebuild_db()
	return "Ok", 200

@app.route('/questions/all', methods=['DELETE'])
def DeleteAllQuestions():
	if(jwt_utils.is_unauthorizated(request.headers.get('Authorization'))):
		return {"error": "Unauthorized"}, 401
	db = db_utils.DataBase()
	db.delete_all_questions()
	return "OK", 204

@app.route('/participations/all', methods=['DELETE'])
def DeleteAllParticipations():
	if(jwt_utils.is_unauthorizated(request.headers.get('Authorization'))):
		return {"error": "Unauthorized"}, 401
	db = db_utils.DataBase()
	db.delete_all_participations()
	return "OK", 204

if __name__ == "__main__":
    app.run()