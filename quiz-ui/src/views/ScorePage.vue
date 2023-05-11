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
  <div class="container">
  <p>Félicitation {{ playerName }} !</p>
  <p>Tu as terminé le Quiz avec un score de {{ score }}.</p>
  <p>Si tu veux connaître ton classement rend toi sur la page d'accueil.</p>
  <RouterLink to="/" class="lien">Retourner à l'accueil</RouterLink>
</div>
</template>