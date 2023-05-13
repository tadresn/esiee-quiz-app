<script>
import quizApiService from '../../services/QuizApiService'
export default {
  data() {
    return {
      password: '',
      errorMessage: ''
    }
  },
  methods:{
    async login(){
      if(this.password === ''){
        this.errorMessage = 'Le mot de passe est obligatoire';
      }
      else{
        await quizApiService.postLogin(this.password).then(()=>{
          this.$router.push('/admin');
        })
        .catch((error)=>{
          this.errorMessage = "Mot de passe incorrect.";
          this.password = "";
          console.log(error);
        })
      }
    }
  }
}
</script>

<template>
  <div class="d-flex justify-content-center">
      <div class="card card-custom text-center">
        <div class="card-body">
          <div class="form-container my-5">
            <div class="d-flex flex-column">
              <h5 for="password" class="card-title">Saisissez votre mot de passe</h5>
              <input type="password" id="password" v-model="password" placeholder="Password" class="mt-4"/>
              <div class="text-danger" v-if="errorMessage">{{ errorMessage }}</div>
            </div>
            <button @click="login" class="btn btn-outline-primary mt-5">Login</button>
          </div>
        </div>
      </div>
    </div>
  </template>

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