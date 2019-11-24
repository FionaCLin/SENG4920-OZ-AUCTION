<template>
  <q-page>
    <MyAuctionsList :alink="`myWishlist`" :items="myAuction_items" />
  </q-page>
</template>

<script>
import MyAuctionsList from "../components/dashboard/MyAuctionsList";

export default {
  name: "AuctionsPages",
  components: {
    MyAuctionsList
  },
  // computed: {
  //   myAuction_items: {
  //     get() {
  //       return this.$store.state.auction.myWishList;
  //     }
  //   }
  // },
  data() {
    return {
      myAuction_items: null,
      user: null
    };
  },
  created() {
    this.$data.user = this.$store.state.user.user_id;
  },
  mounted() {
    this.fetch();
  },
  methods: {
    fetch() {
      return this.$axios
        .get(`/account/get_user_favorites/${this.$data.user}`)
        .then(res => {
          this.$store.commit('auction/updateMyWishList', res.data.data);
          console.log(this.$store.state.auction.myWishList);
          this.$data.myAuction_items = this.$store.state.auction.myWishList;
        })
        .catch(err => console.log(err));
    }
  }
};
</script>
