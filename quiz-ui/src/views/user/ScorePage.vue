<script>
import participationStorageService from '../../services/ParticipationStorageService';
import quizApiService from '../../services/QuizApiService';

export default {
  data(){
    return {
      questions:[],
      answersSummaries: []
    }
  },
  computed: {
    playerName: participationStorageService.getPlayerName,
    score: participationStorageService.getParticipationScore,
    
  }, 
  async created(){
    const answers = participationStorageService.getParticipationAnswersSummaries()
    const answerJSON = JSON.parse(answers)
    this.answersSummaries = answerJSON
    await quizApiService.getAllQuestions().then((value)=>{
      this.questions = value.data.questions
    })
    .catch((error)=>{
      console.log(error)
    })
  }
}
</script>

<template>
<div class="d-flex justify-content-center">
<div class="card card-custom text-center">
  <div class="card-body">
    <div class="form-container my-5">
      <div class="d-flex flex-column">
        <h5 class="card-title">Félicitation {{ playerName }} !</h5>
        <p class="mt-5">Tu as terminé le Quiz avec un score de {{ score }}.</p>
        <p>Si tu veux connaître ton classement rends-toi sur la page d'accueil.</p>
      </div>
      <RouterLink to="/" class="btn btn-outline-primary mt-5">Retourner à l'accueil</RouterLink>
    </div>
  </div>
</div>
</div>
<div class="container">
    <div class="row">
      <div class="col">
        <h1 class="titre text-center my-3">Vos résultats</h1>
        <table>
          <tr>
            <th><b>Question</b></th>
            <th><b>Réponse</b></th>
          </tr>
          <tr v-for="(question, index) in questions" v-bind:key="question.id" v-bind:class="{ 'green-row': answersSummaries[index].was_correct, 'red-row': !answersSummaries[index].was_correct }">
            <td>{{ question.text }}</td>
            <td>{{ answersSummaries[index].correctAnswerPosition }}</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<style>
.green-row {
  background-color: rgba(70, 178, 70, 0.873);
}

.red-row {
  background-color: rgba(187, 50, 50, 0.873);
}
.card-custom{
max-width: 500px;
max-height: 500px;
background-color: rgba(73, 73, 73, 0.559);
}
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-container input {
  width: 300px;
}
</style>