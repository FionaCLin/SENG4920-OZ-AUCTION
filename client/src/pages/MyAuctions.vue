<template>
  <q-page>
    <MyAuctionsList :tool="true" :items="myAuction_items" />
  </q-page>
</template>

<script>
import MyAuctionsList from "../components/dashboard/MyAuctionsList";
import { axiosInstance } from "boot/axios";

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
        console.log("my auctions", this.$store.state.auction.myAuctions);
        return this.$store.state.auction.myAuctions;
      }
    }
  },
  created() {
    console.log(JSON.parse(localStorage.getItem("user")).user_id);
    axiosInstance
      .get(`/account/get_user_auctions/${JSON.parse(localStorage.getItem("user")).user_id}`)
      .then(res => {
        console.log(JSON.parse(localStorage.getItem("user")).user_id);
        console.log(res.data.data.auctions);
        console.log(this.$store.state.auction.myAuctions.auction_items);
        this.$store.commit("auction/updateMyAuctions", res.data.data.auctions);
        this.$data.my_auctions = res.data.data.auctions;
      });
    //.catch(err => console.log(err));
  }
};
</script>
