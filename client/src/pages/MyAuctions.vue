<template>
  <q-page>
    <MyAuctionsList
      :alink="`myAuctions`"
      :tool="true"
      :items="myAuction_items"
    />
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
      myAuction_items: this.$store.state.auction.myAuctions
    };
  },
  created() {
    this.$data.myAuction_items = this.$store.state.auction.myAuctions;
  }
};
</script>
