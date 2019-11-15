<template>
  <q-page>
    <MyAuctionsList :tool="true" :items="myAuction_items" />
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
        console.log("my auctions", this.$store.state.auction.myAuctions);
        return this.$store.state.auction.myAuctions;
      }
    }
  }
};
</script>
