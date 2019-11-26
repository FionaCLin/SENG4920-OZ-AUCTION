<template>
  <q-page>
    <MyAuctionsList
      :loading="loading"
      :alink="`myBiddings`"
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
      myAuction_items: [],
      loading: true,
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
        .get(`/account/get_user_biddings/${this.$data.user}`)
        .then(res => {
          this.$store.commit("auction/updateMyBiddings", res.data.data);
          this.$data.myAuction_items = this.$store.state.auction.myBids;
          this.$data.loading = false;
        })
        .catch(err => console.log(err));
    }
  }
};
</script>
