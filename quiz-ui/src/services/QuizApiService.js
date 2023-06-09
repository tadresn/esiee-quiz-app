import axios from "axios";

const instance = axios.create({
	baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    return this.call("get", `questions?position=${position}`)
  },
  postParticipation(playerName, answers){
    return this.call("post", "participations", {playerName, answers})
  },
  async postLogin(password){
    const value = await this.call("post", "login", {password})
    instance.defaults.headers.common.Authorization = `Bearer ${value.data.token}`
  },
  isAuthorized(){
    if(instance.defaults.headers.common.Authorization){
      return true;
    }
    else{
      return false;
    }
  },
  deconnected(){
    delete instance.defaults.headers.common.Authorization;
  },
  deleteParticipationsAll(){
    return this.call("delete", 'participations/all')
  },
  deleteQuestionsAll(){
    return this.call("delete", "questions/all")
  },
  deleteQuestionById(id){
    return this.call("delete", `questions/${id}`)
  },
  addQuestion(question){
    return this.call("post", "questions", question)
  },
  updateQuestion(question){
    return this.call("put", `questions/${question.id}`, question)
  },
  getAllQuestions(){
    return this.call('get', "questions/all")
  }
};