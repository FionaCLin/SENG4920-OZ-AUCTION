<template>
  <q-page class="bg-grey-1 q-pa-none q-ma-none">
    <a name="newAuctions">
      <NewAuction />
    </a>

    <MyAuctionsList
      :alink="`auctions`"
      :title="`My Auctions`"
      :items="myAuction_items"
    />

    <MyAuctionsList
      :alink="`bids`"
      :title="`My Bids`"
      :items="myAuction_items"
    />
    <MyAuctionsList
      :alink="`favorites`"
      :title="`My Favorites`"
      :items="myAuction_items"
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
    myAuction_items: {
      get() {
        console.log(this.$store.state.auction.myAuctions);
        let items = [...this.$store.state.auction.myAuctions.auction_items];
        items.map(
          x =>
            (x.location = this.$store.state.auction.myAuctions.sellers.location)
        );
        return items;
      }
    }
  }
};
</script>
