<template>
<div class="container">
    <div class="row">
      <div class="col">
        <h1 class="titre text-center my-3">Bienvenue sur le Quiz !</h1>
        <h3 class="titre text-center my-3 mt-5">Classement des participants</h3>
        <table>
          <tr>
            <th><b>Rang</b></th>
            <th><b>Nom</b></th>
            <th><b>Score</b></th>
            <th><b>Date</b></th>
          </tr>
          <tr v-for="(scoreEntry, index) in registeredScores" v-bind:key="scoreEntry.date">
            <td>{{ index + 1}}</td>
            <td>{{ scoreEntry.playerName }}</td>
            <td>{{ scoreEntry.score }}</td>
            <td>{{ scoreEntry.date }}</td>
          </tr>
        </table>
        <div class="text-center py-5">
          <router-link to="/new-quiz-page" class="btn btn-outline-primary">Démarrer le quiz !</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from '../../services/QuizApiService';

export default {
  name: "HomePage",
  data() {
    let registeredScores = []
    return { 
      registeredScores
    };
  },
  async created() {
    await quizApiService.getQuizInfo().then((value) => {
      this.registeredScores = value.data.scores
    })
    .catch((error)=>{
      console.log(error)
    })
  }
};
</script>

<style>
th,
td {
  border: 1px solid grey;
  text-align: center;
}
table{
  width:50% ; 
  margin: auto
}
</style>