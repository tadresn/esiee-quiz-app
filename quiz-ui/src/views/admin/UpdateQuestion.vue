<template>
  <button @click="logout" class="btn btn-outline-primary" style="float: right;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-lock" viewBox="0 0 16 16">
  <path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm0 5.996V14H3s-1 0-1-1 1-4 6-4c.564 0 1.077.038 1.544.107a4.524 4.524 0 0 0-.803.918A10.46 10.46 0 0 0 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h5ZM9 13a1 1 0 0 1 1-1v-1a2 2 0 1 1 4 0v1a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1v-2Zm3-3a1 1 0 0 0-1 1v1h2v-1a1 1 0 0 0-1-1Z"/>
  </svg> Se déconnecter</button>
  <div class="quiz-form-container">
    <h5>Modifer la question</h5>
    <form @submit.prevent="submitForm">
      <label>Position</label>
      <input type="number" v-model="position" placeholder="Position" required>
      <label>Titre</label>
      <input type="text" v-model="title" placeholder="Titre" required>
      <label>Texte</label>
      <input type="text" v-model="text" placeholder="Texte" required>
      <label>Image</label>
      <ImageUpload @file-change="imageFileChangedHandler"/>
      <div class="possible-answers-container">
        <label class="text-center">Réponse possible</label>
        <div v-for="(answer, index) in possibleAnswers" :key="index" style="margin-left: 20px; margin-right: 20px;">
          <label>Réponse {{index + 1}}</label>
          <input type="text" v-model="answer.text" placeholder="Reponse" required>
          <label>
            Est-ce que c'est la réponse correct ?
            <input type="radio" v-model="correctAnswerIndex" :value="index" :checked="answer.isCorrect">
            
          </label>
          <div class="supp-answer-btn">
          <button type="button" @click="removeAnswer(index)" class="btn btn-outline-danger">Supprimer la réponse</button>
        </div>
        </div>
        <div class="add-answer-btn">
          <button type="button" @click="addAnswer" class="btn btn-outline-success mb-3">Ajouter une réponse</button>
        </div>
      </div>
      <div style="text-align: center;">
      <button type="submit" class="btn btn-outline-primary">Modifier</button>
      </div>
      <div v-if="error" class="text-danger">{{ error }}</div>
    </form>
  </div>
  </template>
  
  <script>
  import ImageUpload from '../../components/ImageUpload.vue';
import participationStorageService from '../../services/ParticipationStorageService';
  import quizApiService from '../../services/QuizApiService';
  
  export default {
    components: {
      ImageUpload
    },
    data() {
      return {
        id: null,
        position: null,
        title: null,
        text: null,
        image: null,
        possibleAnswers: [
          {text: '', isCorrect: false},
          {text: '', isCorrect: false}
        ],
        correctAnswerIndex: null,
        error: null
      };
    },
    created(){
      const questionStorage = participationStorageService.getQuestionToUpdate();
      const questionToUpdate = JSON.parse(questionStorage)
      this.id = questionToUpdate.id;
      this.position = questionToUpdate.position;
      this.title = questionToUpdate.title;
      this.text = questionToUpdate.text;
      this.image = questionToUpdate.image;
      this.possibleAnswers = questionToUpdate.possibleAnswers;
      for (let i = 0; i < this.possibleAnswers.length; i++) {
      if (this.possibleAnswers[i].isCorrect) {
        this.correctAnswerIndex = i;
        break;
      }
  }
    },
    methods: {
      addAnswer() {
        this.possibleAnswers.push({text: '', isCorrect: false});
      },
      removeAnswer(index) {
        this.possibleAnswers.splice(index, 1);
        if (this.correctAnswerIndex === index) {
          this.correctAnswerIndex = null;
        }
      },
      imageFileChangedHandler(b64String) {
        this.image = b64String;
      },
      async submitForm() {
        if (this.correctAnswerIndex === null) {
          this.error = "Il faut au moins deux réponses possible et sélectionner une seule bonne réponse.";
          return;
        }
        let size = 0;
        await quizApiService.getQuizInfo().then((value)=>{
          size = value.data.size;
        })
  
        if (this.position <= 0 || this.position > size + 1) {
          this.error = "La position doit être supérieure à zéro et inférieure ou égale au nombre de questions total + 1";
          return;
        }
        const correctAnswer = this.possibleAnswers[this.correctAnswerIndex];
        const possibleAnswers = this.possibleAnswers.map(answer => {
          return {text: answer.text, isCorrect: answer === correctAnswer};
        });

        if(possibleAnswers.length < 2){
          this.error = "Il faut au moins deux réponses possible et sélectionner une seule bonne réponse."
          return
      }
        
        const question = {
          id: this.id,
          position: this.position,
          title: this.title,
          text: this.text,
          image: this.image,
          possibleAnswers: possibleAnswers
        };
  
        await quizApiService.updateQuestion(question).then(()=>{
          // Reset form fields
          this.position = null;
          this.title = null;
          this.text = null;
          this.image = null;
          this.possibleAnswers = [
            {text: '', isCorrect: false},
            {text: '', isCorrect: false}
          ];
          this.correctAnswerIndex = null;
          this.error = null;
          this.$router.push('/admin');
        })
        .catch((error)=>{
          console.log(error);
        })
      },
      logout(){
      quizApiService.deconnected();
      this.$router.push('/');
    }
    }
  };
  </script>
  
  <style>
  .quiz-form-container h5{
    text-align: center; 
    color: blueviolet;
    margin-bottom: 40px;
  }
  .quiz-form-container {
    width: 500px;
    padding: 20px;
    margin: 0 auto;
    background-color: rgba(73, 73, 73, 0.559);
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0 0 5px #ddd;
  }
  
  .quiz-form-container label {
    display: block;
    margin-bottom: 5px;
    margin-top: 20px;
  }
  
  .quiz-form-container input[type="text"],
  .quiz-form-container input[type="number"] {
    width: 100%;
    padding: 5px;
    border-radius: 3px;
    border: 1px solid #ddd;
  }
  
  .quiz-form-container label input[type="radio"] {
    margin-right: 5px;
  }
  
  .quiz-form-container .possible-answers-container {
    width: 100%;
    margin-bottom: 10px;
    margin-top: 30px;
    background-color: rgba(31, 31, 31, 0.559);
  }
  
  .quiz-form-container .possible-answers-container label {
    display: block;
    margin-bottom: 5px;
  }
  
  .quiz-form-container .possible-answers-container label input[type="text"] {
    width: calc(100% - 30px);
    margin-right: 5px;
  }
  
  .quiz-form-container .possible-answers-container label button {
    margin-right: 5px;
  }
  
  .quiz-form-container .add-answer-btn {
    margin-top: 50px;
    margin-bottom: 30px;
    text-align: center;
  }
  
  .quiz-form-container .supp-answer-btn {
    margin-top: 20px;
    margin-bottom: 30px;
    text-align: center;
  }
  </style>
  