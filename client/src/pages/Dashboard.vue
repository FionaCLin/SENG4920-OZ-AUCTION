<template>
  <q-page class="bg-grey-1">
    <a name="newAuctions">
      <NewAuction />
    </a>

    <MyAuctionsList
      :alink="`auctions`"
      :title="`My Auctions`"
      :items="myAuctions"
    />

    <MyAuctionsList :alink="`bids`" :title="`My Bids`" :items="myBids" />
    <MyAuctionsList
      :alink="`favorites`"
      :title="`My Favorites`"
      :items="myWishs"
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
    myAuctions: {
      get() {
        console.log(this.$store.state.auction.myAuctions);
        return this.$store.state.auction.myAuctions;
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
