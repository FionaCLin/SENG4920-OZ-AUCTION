<template>
  <q-layout view="hHh lpR lFf">
    <q-header elevated class="bg-light-green-8 text-white" height-hint="98">
      <q-toolbar>
        <q-btn flat :to="logged ? '/dashboard' : '/'" push>
          <q-icon name="img:statics/bid.gif" :ratio="1" size="40px"></q-icon>
        </q-btn>
        <q-toolbar-title>Pro Auction Bidder</q-toolbar-title>
      </q-toolbar>

      <q-tabs align="left">
        <q-route-tab icon="send" to="/login" label="Login" />
        <q-route-tab icon="people_outline" to="/register" label="Register" />
      </q-tabs>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "Index",
  props: ["logged"]
};
</script>
