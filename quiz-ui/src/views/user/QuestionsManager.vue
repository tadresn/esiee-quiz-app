<script>
import QuestionDisplay from '../../components/QuestionDisplay.vue';
import quizApiService from '../../services/QuizApiService';
import participationStorageService from "../../services/ParticipationStorageService";

export default {
  data () {
    return {
      currentQuestionPosition:1,
      totalNumberOfQuestion: 0,
      answersOfPlayer: [],
      currentQuestion:{}
    }
  },
  components: {
    QuestionDisplay
  },
  async created() {
    await quizApiService.getQuizInfo().then((value) => {
      this.totalNumberOfQuestion = value.data.size
    })
    .catch((error)=>{
      console.log(error)
    })
    this.loadQuestionByPosition()
  },
  methods: {
    async loadQuestionByPosition() {
      await quizApiService.getQuestion(this.currentQuestionPosition).then((value) => {
        this.currentQuestion = value.data
      })
      .catch((error)=>{
        console.log(error)
      })
    },
    async answerClickedHandler(positionOfAnswerSelected){
      this.answersOfPlayer[this.currentQuestionPosition - 1] = positionOfAnswerSelected
      if(this.currentQuestionPosition < this.totalNumberOfQuestion){
        this.currentQuestionPosition += 1
        this.loadQuestionByPosition()
      }
      else {
        this.endQuiz()
      }
    },
    async endQuiz(){
      await quizApiService
      .postParticipation(participationStorageService.getPlayerName(), this.answersOfPlayer)
      .then((value)=>{
        participationStorageService.saveParticipationScore(value.data.score)
        participationStorageService.saveParticipationAnswersSummaries(value.data.answersSummaries)
      })
      .catch((error)=>{
        console.log(error)
      })
      this.$router.push('/score-page')
    }
  }
  

}
</script>

<template>
  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
</template>