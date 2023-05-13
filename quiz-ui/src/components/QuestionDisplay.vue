<script>
export default {
  data () {
    return { }
  },
  props : {
    question: {
      type: Object,
      required: true,
    }
  },
  emits: ["answer-selected"],
  methods: {
    answerClicked(positionOfAnswerSelected){
      this.$emit('answer-selected', positionOfAnswerSelected)
    }
  }
}
</script>

<template>
<div class="container">
  <div class="row justify-content-center">
    <div class="col-md-8 text-center">
      <h1 class="title">{{ question.title }}</h1>
      <h4 class="texte">{{ question.text }}</h4>
      <img v-if="question.image" :src="question.image" class="mx-auto img-fluid image"/>
      <div v-for="(answer, index) in question.possibleAnswers" :key="answer.id" style="margin-top: 20px;">
        <button @click="answerClicked(index + 1)" class="btn btn-outline-success large-button">{{ answer.text }}</button>
      </div>
    </div>
  </div>
</div>
</template>

<style>
.image{
  max-width: 60%; 
  margin-top: 30px;
  margin-bottom: 10px;
}
.large-button{
  width: 70%
}
.title{
  font-weight: bold
}
.texte{
  margin-top: 30px
}
</style>