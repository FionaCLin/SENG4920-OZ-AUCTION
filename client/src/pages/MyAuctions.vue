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
  created() {
    console.log(JSON.parse(localStorage.getItem('user')).user_id);
    axiosInstance
      .get(`/account/${JSON.parse(localStorage.getItem('user')).user_id}`)
      .then(res => {
        console.log(res.data.auctions);
        console.log(this.$store.state.auction.myAuctions.auction_items);
        this.$store.dispatch(
          "auction/getMyAuctions",
          this.$store.state.user.user_id
        );
        this.$data.my_auctions = res.data.auctions;
      });
      //.catch(err => console.log(err));
  },
  computed: {
    myAuction_items: {
      get() {
        //console.log("my auctions", this.$store.state.auction.myAuctions);
        return this.$store.state.auction.myAuctions;
      }
    }
  }
};
</script>
