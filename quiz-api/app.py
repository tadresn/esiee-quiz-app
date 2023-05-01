from flask import Flask, request
from flask_cors import CORS
import jwt_utils

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


if __name__ == "__main__":
    app.run()