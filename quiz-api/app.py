from flask import Flask, request
from flask_cors import CORS
import jwt_utils
import db_utils
import models
from flask import jsonify

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
	question = models.Question(None, payload["position"], payload["title"], payload["text"], payload["image"], payload["possibleAnswers"])
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

@app.route("/questions/all", methods=["GET"])
def GetAllQuestions():
	db = db_utils.DataBase()
	questions = db.get_all_questions()
	return {"questions": questions}, 200


@app.route('/questions/<int:id>', methods=['GET'])
def GetQuestionById(id):
	db = db_utils.DataBase()
	question = db.get_question_and_possible_answers_by_id(id)
	if question is None:
		return {"error": "Not found"}, 404
	return jsonify(question.question_to_dict()), 200

@app.route('/questions', methods=['GET'])
def GetQuestionByPosition():
	position = request.args.get('position')
	db = db_utils.DataBase()
	question = db.get_question_and_possible_answers_by_position(position)
	if question is None:
		return {"error": "Not found"}, 404
	return jsonify(question.question_to_dict()), 200

@app.route('/questions/<int:id>', methods=['PUT'])
def PutQuestionById(id):
	if(jwt_utils.is_unauthorizated(request.headers.get('Authorization'))):
		return {"error": "Unauthorized"}, 401
	payload = request.get_json()
	question = models.Question(id, payload["position"], payload["title"], payload["text"], payload["image"], payload["possibleAnswers"])
	db = db_utils.DataBase()
	if db.get_question_and_possible_answers_by_id(question.id) is None:
		return {"error": "Not found"}, 404
	db.put_question_and_possible_answers_by_id(question)
	return "Ok", 204

@app.route('/questions/<int:id>', methods=['DELETE'])
def DeleteQuestionById(id):
	if(jwt_utils.is_unauthorizated(request.headers.get('Authorization'))):
		return {"error": "Unauthorized"}, 401
	db = db_utils.DataBase()
	if db.get_question_and_possible_answers_by_id(id) is None:
		return {"error": "Not found"}, 404
	db.delete_question_by_id(id)
	return "Ok", 204

@app.route('/participations', methods=['POST'])
def PostParticipation():
	payload =  request.get_json()
	answers = payload["answers"]
	db = db_utils.DataBase()
	if len(answers) != db.count_questions():
		return {"error": "Incorrect number of answers"}, 400
	player_name, score, answersSummaries = db.post_participation(payload["playerName"], answers)
	return {"answersSummaries": answersSummaries, "playerName": player_name, "score": score}, 200

if __name__ == "__main__":
    app.run()