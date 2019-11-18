<template>
  <q-page class="bg-grey-1">
    <a name="newAuctions">
      <NewAuction />
    </a>

    <MyAuctionsList :alink="`auctions`" :items="auctions" />
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
    }
  },
  created() {
    this.$store.dispatch("auction/getAllAuctions");
    this.$store.dispatch(
      "auction/getMyAuctions",
      this.$store.state.user.user_id
    );
  }
};
</script>
