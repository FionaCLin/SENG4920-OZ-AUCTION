<template>
  <q-page padding>
    <q-toolbar>
      <q-btn to="/create"> <q-icon name="add" />Create Auction </q-btn>
    </q-toolbar>
    <MyAuctionsList :items="myAuction_items" />
  </q-page>
</template>

<script>
import MyAuctionsList from "../components/dashboard/MyAuctionsList";

export default {
  name: "AuctionsPages",
  components: {
    MyAuctionsList
  },
  computed: {
    myAuction_items: {
      get() {
        console.log(this.$store.state.auction.myAuctions);
        return this.$store.state.auction.myAuctions.auction_items;
      }
    }
  }
};
</script>
