<template>
  <div class="container">
      <div class="row">
        <div class="col">
          <h1 class="titre text-center my-3">List des participants</h1>
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
            <button @click="deleteParticipationsAll()" to="/new-quiz-page" class="btn btn-outline-danger">Supprimer les participants</button>
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
      return { registeredScores
      };
    },
    methods: {
      async created() {
      await quizApiService.getQuizInfo().then((value) => {
        this.registeredScores = value.data.scores
      })
      .catch((error)=>{
        console.log(error)
      })
    },
    async deleteParticipationsAll(){
      await quizApiService.deleteParticipationsAll().then(()=>{
        this.created()
      });
    }
  },
  created(){
    this.created();
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