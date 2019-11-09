<template>
  <q-page>
    <div class="row">
      <div class="my-card col-sm-12"></div>

      <div class="col-sm-6 q-pa-md">
        <q-list class="my-card col-sm-6 fit column justify-center item-center">
          <q-img :src="auction.image" style="width: 60%;" />
          <q-item>
            <q-btn v-if="favorite" flat @click="removeFavorite">
              <q-icon name="favorite_border" />
            </q-btn>
            <q-btn v-else flat @click="addFavorite">
              <q-icon name="favorite" />
            </q-btn>
          </q-item>
        </q-list>
      </div>
      <div class="my-card col-sm-6">
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
