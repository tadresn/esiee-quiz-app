<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <RouterLink to="/">Accueil</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
  </header>

  <main style="padding-top: 60px;">
  <RouterView />
  </main>

  <footer>
      <p>Développé par ESCAFFRE Robin & TADRES Nicolas</p>
  </footer>
</template>

<style scoped>
footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 50px; 
  text-align: center;
}
p{
  text-align: center;
}
header {
  position: fixed;
  top: 0;
  width: 100%;
  height: 50px; 
  line-height: 1.5;
  max-height: 100vh;
  z-index: 1000;
}
nav {
  width: 100%;
  font-size: 17px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>
