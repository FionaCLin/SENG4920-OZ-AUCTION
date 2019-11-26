<template>
  <q-page class="bg-grey-1">
    <a name="newAuctions">
      <NewAuction />
    </a>

    <MyAuctionsList
      :alink="`auctions`"
      :items="auctions"
    />
  </q-page>
</template>

<script>
import NewAuction from "../components/dashboard/NewAuctionsList";
import MyAuctionsList from "../components/dashboard/MyAuctionsList";

export default {
  name: "Dashboard",
  components: {
    NewAuction,
    MyAuctionsList
  },
  computed: {
    auctions: {
      get() {
        return this.$store.state.auction.auctions;
      }
    },
    myBids: {
      get() {
        console.log(this.$store.state.auction.myBids);

        return this.$store.state.auction.myBids;
      }
    },
    myWishs: {
      get() {
        console.log(this.$store.state.auction.myWishList);

        return this.$store.state.auction.myWishList;
      }
    }
  },
  created() {
    this.$store.dispatch("auction/getAllAuctions");
    this.$store.dispatch(
      "auction/getMyAuctions",
      this.$store.state.user.user_id
    );
    this.$store.dispatch("auction/getMyBiddings", 2);
    this.$store.dispatch("auction/getMyFavorite", 1);
  }
};
</script>
