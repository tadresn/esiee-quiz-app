<script>
import participationStorageService from '../services/ParticipationStorageService';

export default {
  computed: {
    playerName: participationStorageService.getPlayerName,
    score: participationStorageService.getParticipationScore
  }
}
</script>

<template>
<div class="d-flex justify-content-center">
<div class="card card-custom text-center">
  <div class="card-body">
    <div class="form-container my-5">
      <div class="d-flex flex-column">
        <h5 class="card-title">Félicitation {{ playerName }} !</h5>
        <p class="mt-5">Tu as terminé le Quiz avec un score de {{ score }}.</p>
        <p>Si tu veux connaître ton classement rends-toi sur la page d'accueil.</p>
      </div>
      <RouterLink to="/" class="btn btn-outline-primary mt-5">Retourner à l'accueil</RouterLink>
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