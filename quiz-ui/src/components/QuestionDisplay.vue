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
  <p>{{ question.title }}</p>
  <p> {{ question.text }} </p>
  <img v-if="question.image" :src="question.image" />
  <div v-for="(answer, index) in question.possibleAnswers" :key="answer.id">
  <button @click="answerClicked(index + 1)">{{ answer.text }}</button>
</div>

</template>