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
  computed: {
    myAuction_items: {
      get() {
        console.log(this.$store.state.auction.myWishList);
        return this.$store.state.auction.myWishList.auction_items;
      }
    }
  }
};
</script>
