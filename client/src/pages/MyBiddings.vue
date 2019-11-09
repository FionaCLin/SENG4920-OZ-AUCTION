<template>
  <q-page>
    <MyAuctionsList :title="``" :tool="true" :items="myAuction_items" />
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
        console.log(this.$store.state.auction.myBids);
        return this.$store.state.auction.myBids.auction_items;
      }
    }
  }
};
</script>
