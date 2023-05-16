<template>
  <div class="container">
    <div class="row">
        <div class="col">
          <button @click="logout" class="btn btn-outline-primary" style="float: right;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-lock" viewBox="0 0 16 16">
          <path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm0 5.996V14H3s-1 0-1-1 1-4 6-4c.564 0 1.077.038 1.544.107a4.524 4.524 0 0 0-.803.918A10.46 10.46 0 0 0 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h5ZM9 13a1 1 0 0 1 1-1v-1a2 2 0 1 1 4 0v1a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1v-2Zm3-3a1 1 0 0 0-1 1v1h2v-1a1 1 0 0 0-1-1Z"/>
          </svg> Se déconnecter</button>
        </div>
    </div>
  </div>
  <TableauParticipantAdmin/>
  <div class="container">
      <div class="row">
        <div class="col">
          <h1 class="titre text-center my-3">Liste des questions</h1>
          <table>
            <tr>
              <th><b>Position</b></th>
              <th><b>Titre</b></th>
              <th><b>Question</b></th>
              <th><b>Supprimer</b></th>
              <th><b>Modifier</b></th>
            </tr>
            <tr v-for="question in questions" v-bind:key="question.id">
              <td>{{ question.position }}</td>
              <td>{{ question.title }}</td>
              <td>{{ question.text }}</td>
              <td><button class="btn btn-outline-danger" @click="deleteQuestionById(question.id)"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
              <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
              <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
              </svg></button></td>
              <td><button class="btn btn-outline-success" @click="saveQuestionToUpdate(question)"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
              <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"/>
              </svg></button></td>
            </tr>
          </table>
          <div class="text-center py-5">
            <button @click="deleteQuestionsAll()" class="btn btn-outline-danger">Supprimer les questions</button>
            <button @click="this.$router.push('/admin/add-question')" class="btn btn-outline-success" style="margin-left: 50px;">Ajouter une question</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
import TableauParticipantAdmin from '../../components/TableauParticipantAdmin.vue';
import participationStorageService from '../../services/ParticipationStorageService';
import quizApiService from '../../services/QuizApiService';
export default {
data() {
    return {
      questions: [],
    };
  },
  components: {
    TableauParticipantAdmin,
}, 
  async created() {
    await this.loadQuestions();
  },
  methods: {
    async loadQuestions() {
      await quizApiService.getAllQuestions().then((value)=>{
        this.questions = value.data.questions
      }
      )
      .catch((error) => {
          console.log(error);
        });
    },
    async reload() {
      await this.loadQuestions();
    },
    async deleteQuestionsAll() {
      await quizApiService
        .deleteQuestionsAll()
        .then(() => {
          this.reload();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async deleteQuestionById(id) {
      await quizApiService
        .deleteQuestionById(id)
        .then(() => {
          this.reload();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    saveQuestionToUpdate(question){
      participationStorageService.saveQuestionToUpdate(question);
      this.$router.push("/admin/update-question");
    },
    logout(){
      quizApiService.deconnected();
      this.$router.push('/');
    }
  },
};
</script>
