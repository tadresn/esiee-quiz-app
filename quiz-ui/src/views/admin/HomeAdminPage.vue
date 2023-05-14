<template>
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
            </tr>
            <tr v-for="question in questions" v-bind:key="question.id">
              <td>{{ question.position }}</td>
              <td>{{ question.title }}</td>
              <td>{{ question.text }}</td>
              <td><button class="btn btn-outline-danger" @click="deleteQuestionById(question.id)"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
              <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
              <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
              </svg></button></td>
            </tr>
          </table>
          <div class="text-center py-5">
            <button @click="deleteQuestionsAll()" class="btn btn-outline-danger">Supprimer les questions</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
import TableauParticipantAdmin from '../../components/TableauParticipantAdmin.vue';
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
      await quizApiService
        .getQuizInfo()
        .then((value) => {
          const size = value.data.size;
          if (size > 0) {
            const promises = [];
            for (let i = 1; i <= size; i++) {
              promises.push(
                quizApiService.getQuestion(i).then((value) => value.data)
              );
            }
            return Promise.all(promises);
          } else {
            return [];
          }
        })
        .then((data) => {
          this.questions = data;
        })
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
  },
};
</script>
