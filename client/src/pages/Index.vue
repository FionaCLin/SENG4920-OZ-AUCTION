<template>
  <q-page class="flex flex-center">
    <!-- <img alt="Quasar logo" src="~assets/quasar-logo-full.svg" /> -->
    <h1>This is Landing Page!! You are NOT authenticated!</h1>
    <router-link class="absolute-center" to="/login">Login</router-link>
  </q-page>
</template>

<script>
export default {
  name: "PageIndex"
};
</script>
