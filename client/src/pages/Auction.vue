<template>
  <q-page padding>
    <q-toolbar>
      <q-btn to="/create"> <q-icon name="add" />Create Auction </q-btn>
    </q-toolbar>
    {{ auction }}
  </q-page>
</template>

<script>
export default {
  name: "AuctionPage",
  data() {
    return {
      auction: this.$store.state.auction.myAuctions.auction_items.find(
        x => x.id === this.$route.params.id
      )
    };
  },
  created() {
    console.log("to", this.$route.params.id);
  }
};
</script>
