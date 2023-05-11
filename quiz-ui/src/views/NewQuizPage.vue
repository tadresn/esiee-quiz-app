<template>
  <div class="container">
        <p for="username" class="text-center">Saisissez votre nom :</p>
        <input type="text" id="username" v-model="username" placeholder="Username"/>
        <button class="lien" @click="launchNewQuiz">GO !</button>
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
      console.log("Launch new quiz with", this.username);
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    },
  }
}
</script>


<style>
input {
  background-color : #000000; 
  border: 2px solid rgb(167, 167, 167);
  margin: 0px 0px 20px 0px;
  border-radius: 5px;
  color: white;
}
</style>
