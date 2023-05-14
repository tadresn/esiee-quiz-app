<!-- eslint-disable vue/multi-word-component-names -->
<script>
import QuizApiService from '../../services/QuizApiService';

export default {
  watch: {
    '$route.name': function () {
      if(!QuizApiService.isAuthorized()){
        this.$router.push('/admin/login-page')
      }
    }
  }
}
</script>
<template><router-view /></template>