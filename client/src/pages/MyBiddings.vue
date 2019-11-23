<template>
  <q-page>
    <MyAuctionsList :title="``" :items="myAuction_items" />
  </q-page>
</template>

<script>
import MyAuctionsList from "../components/dashboard/MyAuctionsList";

export default {
  name: "AuctionsPages",
  components: {
    MyAuctionsList
  },
  data() {
    return {
      myAuction_items: this.$store.state.auction.myBids
    };
  },
  created() {
    this.$data.myAuction_items = this.$store.state.auction.myBids;
  }
};
</script>
