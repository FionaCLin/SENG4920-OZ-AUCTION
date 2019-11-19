<template>
  <div id="q-app">
    <div v-if="ready">
      <router-view />
    </div>

    <div v-else class="flex flex-center">
      <q-circular-progress indeterminate size="150px" class="q-ma-md" />
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      ready: false
    };
  },
  created() {
    let promises = [
      this.$store.dispatch("auction/getAllAuctions"),
      this.$store.dispatch(
        "auction/getMyAutions",
        this.$store.state.user.user_id
      ),
      this.$store.dispatch(
        "auction/getMyBiddings",
        this.$store.state.user.user_id
      ),
      this.$store.dispatch(
        "auction/getMyFavorite",
        this.$store.state.user.user_id
      )
    ];
    Promise.all(promises).then(res => {
      this.$data.ready = true;
      console.log(res, "ready");
    });
  }
};
</script>
