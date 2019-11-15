<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
  created() {
    this.$store.dispatch("auction/getAllAuctions");
    this.$store.dispatch(
      "auction/getMyAuctions",
      this.$store.state.user.user_id
    );
    this.$store.dispatch("auction/getMyBiddings", 2);
    this.$store.dispatch("auction/getMyFavorite", 1);
  }
};
</script>
