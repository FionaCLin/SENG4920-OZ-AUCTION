<template>
  <q-page padding class="bg-grey-1 q-pa-none q-ma-none">
    <NewAuction />
    <MyAuctionsList :items="myAuction_items" />
    <MyBidsList />
  </q-page>
</template>

<script>
import NewAuction from "../components/dashboard/NewAuctionsList";
import MyAuctionsList from "../components/dashboard/MyAuctionsList";
import MyBidsList from "../components/dashboard/MyBidsList";

export default {
  name: "Dashboard",
  components: {
    NewAuction,
    MyAuctionsList,
    MyBidsList
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
