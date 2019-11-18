<template>
  <q-page>
    <MyAuctionsList :tool="true" :items="myAuction_items" />
  </q-page>
</template>

<script>
import MyAuctionsList from "../components/dashboard/MyAuctionsList";
// import { axiosInstance } from "boot/axios";

export default {
  name: "AuctionsPages",
  components: {
    MyAuctionsList
  },
  data() {
    return {
      my_auctions: null
    };
  },
  computed: {
    myAuction_items: {
      get() {
        console.log(
          "my auctions!!!!!!!!",
          this.$store.state.auction.myAuctions
        );
        return this.$store.state.auction.myAuctions.auction_items;
      }
    }
  },
  created() {
    this.$store.state.dispatch(
      "auction/getMyAuctions",
      `${JSON.parse(localStorage.getItem("user")).user_id}`
    );
  }
};
</script>
