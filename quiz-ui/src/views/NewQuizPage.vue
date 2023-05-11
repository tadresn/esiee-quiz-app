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
    </div>
  </div>
</div>
</div>
</template>

<script>
import participationStorageService from "../services/ParticipationStorageService";

export default {
  data(){
    return {
      username: '',
    }
  },
  methods:{
    launchNewQuiz(){
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
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
