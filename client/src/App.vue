<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="navbar">
    <router-link :to="{name:'dashboard'}" class="navbar-item">Dashboard</router-link>
    <router-link :to="{name:'information'}" class="navbar-item">Information</router-link>
  </div>
  <RouterView />
</template>

<style scoped>
.navbar{
  display: flex;
  background: rgb(118, 128, 184);
}
a{
  padding: 10px 20px;
  color: white;
  text-decoration: none;
}
a.router-link-active{
  background: rgb(70 87 175);
  border-radius: 5px;
}
</style>
