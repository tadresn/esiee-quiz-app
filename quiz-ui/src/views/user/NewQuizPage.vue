<template>
<div class="d-flex justify-content-center">
    <div class="card card-custom text-center">
      <div class="card-body">
        <div class="form-container my-5">
          <div class="d-flex flex-column">
            <h5 for="username" class="card-title">Saisissez votre nom</h5>
            <input type="text" id="username" v-model="username" placeholder="Username" class="mt-4"/>
          </div>
          <button @click="launchNewQuiz" class="btn btn-outline-primary mt-5">GO !</button>
          <div class="text-danger" v-if="errorMessage">{{ errorMessage }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import participationStorageService from "../../services/ParticipationStorageService";
import quizApiService from "../../services/QuizApiService";

export default {
  data(){
    return {
      username: '',
      errorMessage: '',
      size:0,
    }
  },
  async created() {
    await quizApiService.getQuizInfo().then((value) => {
      this.size = value.data.size
    })
    .catch((error)=>{
      console.log(error)
    })
  },
  methods:{
    launchNewQuiz(){
      if(this.username === ''){
        this.errorMessage = 'Le nom est obligatoire';
      }
      if(this.size === 0){
        this.errorMessage = "Il n'y a pas de quiz créé. Veuillez patienter qu'un administrateur crée un quiz."
      }
      else{
        participationStorageService.savePlayerName(this.username);
        this.$router.push('/questions');
      }
    },
  }
}
</script>


<style>
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
