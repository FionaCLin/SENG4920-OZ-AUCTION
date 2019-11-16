<template>
  <q-page>
    <MyAuctionsList  :items="searchResult" />
  </q-page>
</template>

<script>
import MyAuctionsList from "../components/dashboard/MyAuctionsList";
import { axiosInstance } from "boot/axios";

export default {
  name: "SearchResult",
  components: {
    MyAuctionsList
  },
  data() {
    return {
      searchResult: null
    };
  },
  // computed: {
  //   myAuction_items: {
  //     get() {
  //       console.log("my auctions", this.$store.state.auction.myAuctions);
  //       return this.$store.state.auction.myAuctions;
  //     }
  //   }
  // },
  created() {
    // axiosInstance
    //   .get(`/account/${JSON.parse(localStorage.getItem("user")).user_id}`)
    //   .then(res => {
    //     console.log(res.data.auctions);
    //     console.log(this.$store.state.auction.myAuctions.auction_items);
    //     this.$data.my_auctions = res.data.auctions;
    //   });
    //.catch(err => console.log(err));
  }
};
</script>
