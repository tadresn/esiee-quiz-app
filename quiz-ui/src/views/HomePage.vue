<template>
  <h1>Home page</h1>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
  {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
</template>

<script>
//import quizApiService from "@/services/QuizApiService";
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