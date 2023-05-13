<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <RouterLink to="/">Accueil</RouterLink>
        <RouterLink to="/admin">Admin</RouterLink>
      </nav>
  </header>

  <main>
    <router-view />
  </main>

  <footer>
      <p>Développé par ESCAFFRE Robin & TADRES Nicolas</p>
  </footer>
</template>

<style scoped>
header {
  position: relative;
  top: 0;
  left: 0;
  right: 0;
  height: 50px;
  background-color: transparent;
  z-index: 100;
}
main {
  padding-top: 50px; 
  padding-bottom: 50px;
  min-height: calc(100vh - 150px);
}
footer {
  position: relative;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100px;
  background-color: rgba(0, 0, 0, 0.293);
  display: flex;
  justify-content: center;
  align-items: center;
}
nav {
  width: 100%;
  font-size: 17px;
  text-align: center;
  margin-top: 1rem;
}

nav a.router-link-exact-active {
  color: white;
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid white;
}

nav a:first-of-type {
  border: 0;
}
</style>
