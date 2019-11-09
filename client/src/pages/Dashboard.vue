<template>
  <q-page class="bg-grey-1">
    <a name="newAuctions">
      <NewAuction />
    </a>

    <MyAuctionsList
      :alink="`auctions`"
      :title="`My Auctions`"
      :items="myAuction_items"
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
    },
    myBids: {
      get() {
        console.log(this.$store.state.auction.myBids);
        let items = [...this.$store.state.auction.myBids.auction_items];
        items.map(
          x => (x.location = this.$store.state.auction.myBids.sellers.location)
        );
        return items;
      }
    },
    myWishs: {
      get() {
        console.log(this.$store.state.auction.myWishList);
        let items = [...this.$store.state.auction.myWishList.auction_items];
        items.map(
          x =>
            (x.location = this.$store.state.auction.myWishList.sellers.location)
        );
        return items;
      }
    }
  }
};
</script>
