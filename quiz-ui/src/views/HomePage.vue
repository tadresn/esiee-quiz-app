<template>
  <div class = "container">
  <h1 class="titre">Home page</h1>
  <table>
    <tr>
      <th><b>Nom</b></th>
      <th><b>Score</b></th>
      <th><b>Date</b></th>
    </tr>
    <tr v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
      <td>{{ scoreEntry.playerName }}</td>
      <td>{{ scoreEntry.score }}</td>
      <td>{{ scoreEntry.date }}</td>
    </tr>
  </table>
  <div>
  <router-link to="/start-new-quiz-page" class="lien">Démarrer le quiz !</router-link>
  </div>
</div>
</template>

<script>
import QuizApiService from '../services/QuizApiService';

export default {
  name: "HomePage",
  data() {
    let registeredScores = []
    return { registeredScores
    };
  },
  async created() {
    await QuizApiService.getQuizInfo().then((value) => {
      this.registeredScores = value.data.scores
    })
		console.log("Composant Home page 'created'");
  }
};
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 70vh;
}
table,
th,
td {
  border: 1px solid grey;
  text-align: center;
}
table{
  width:50% ; 
  margin: auto
}
.titre {
  text-align: center;
  margin-top: 50px;
}
.lien {
  text-align: center;
  display: inline-block;
  padding: 10px 20px;
  background-color: #3a3a3a;
  color: hsla(160, 100%, 37%, 1);
  text-decoration: none;
  border: 2px solid hsla(160, 100%, 37%, 1);
  border-radius: 5px;
}
.lien:hover{
  background-color: rgb(83, 83, 83);
  color: hsla(160, 100%, 37%, 1);
  cursor: pointer;
}
th {
  background-color: #404040;
}
</style>