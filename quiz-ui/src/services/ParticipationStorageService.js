export default {
  clear() {
		window.localStorage.clear()
  },
  savePlayerName(playerName) {
		window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {		
		return window.localStorage.getItem("playerName");
  },
  saveParticipationScore(participationScore) {
		window.localStorage.setItem("participationScore", participationScore);
  },
  getParticipationScore() {
		return window.localStorage.getItem("participationScore");
  },
  saveParticipationAnswersSummaries(answersSummaries){
    window.localStorage.setItem("answersSummaries", JSON.stringify(answersSummaries));
  },
  getParticipationAnswersSummaries(){
    return window.localStorage.getItem("answersSummaries");
  },
  saveQuestionToUpdate(question){
    window.localStorage.setItem("question", JSON.stringify(question));
  },
  getQuestionToUpdate(){
    return window.localStorage.getItem("question");
  }
};