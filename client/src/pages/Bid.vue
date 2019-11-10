<template>
  <q-page>
    <div class="row">
      <div class="col-xs-10 col-sm-5 col-md-4 col-lg-5 q-pa-sm q-ma-lg">
        <div class="col-sm-6 fit column justify-center item-center">
          <q-img :src="auction.image" style="width: 60%;" class="q-ma-lg" />
          <q-btn v-if="favorite" flat @click="removeFavorite">
            <q-icon name="favorite_border" />
          </q-btn>
          <q-btn v-else flat @click="addFavorite">
            <q-icon name="favorite" />
          </q-btn>
        </div>
      </div>
      <div class="col-xs-10 col-sm-6 col-md-5 col-lg-6 q-pa-md">
        <ItemDetail :auction="auction" />
      </div>
      <div class="col-10 q-ma-md fit column justify-center item-center">
        <!--  this part will contain the images -->
        <!-- Indicators -->
        <BidDetail :biddings="auction.biddings" />
      </div>
    </div>
  </q-page>
</template>

<script>
import ItemDetail from "../components/auctionItem/ItemDetail";
import BidDetail from "../components/auctionItem/BidDetail";

export default {
  name: "AuctionPage",
  components: {
    ItemDetail,
    BidDetail
  },
  data() {
    return {
      auction: null
    };
  },
  computed: {
    favorite: {
      get() {
        return this.$store.state.user.favorites.indexOf(this.id) !== -1;
      }
    }
  },
  beforeMount() {
    console.log("to", this.$route.params.id);
    console.log(this.$store.state.user);
    this.id = this.$route.params.id;

    for (let i of this.$store.state.auction.auctions) {
      let auction = i.auction_items.find(x => x.id === this.id);
      console.log(i, auction);
      if (auction) {
        this.$data.auction = auction;
        break;
      }
    }
  },
  methods: {
    addFavorite: function() {
      this.$store.commit("user/addFavorite", this.id);
    },
    removeFavorite: function() {
      this.$store.commit("user/removeFavorite", this.id);
    }
    // ...mapActions(["addFavorite", "removeFavorite"])
  }
};
</script>
