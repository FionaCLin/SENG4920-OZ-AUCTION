<template>
  <q-page>
    <div class="row">
      <div class="col-xs-10 col-sm-5 col-md-4 col-lg-5 q-ma-lg">
        <div>
          <ImagesDisplay :image="auction.image" />
        </div>
        <div class="q-pa-sm">
          <q-btn v-if="favorite" class="q-ml-lg" flat @click="removeFavorite">
            <q-icon name="favorite_border" />
          </q-btn>
          <q-btn v-else class="q-ml-lg" flat @click="addFavorite">
            <q-icon name="favorite" />
          </q-btn>
        </div>
        <div class="q-ma-lg row">
          <q-input v-model="bidPrice" class="q-ml-lg" type="number" />
          <q-btn class="q-ml-xs" @click="placeBid">
            <q-icon name="gavel" />Place Bid
          </q-btn>
          <div class="q-ml-lg text-red">{{ error }}</div>
        </div>
      </div>
      <div class="col-xs-10 col-sm-6 col-md-5 col-lg-6 q-pa-md">
        <ItemDetail :auction="auction" />
      </div>
      <div class="col-10 q-ma-md fit column justify-center item-center">
        <!--  this part will contain the images -->
        <!-- Indicators -->
        <BidDetail :biddings="auction.bidding_info" />
      </div>
    </div>
  </q-page>
</template>

<script>
import ItemDetail from "../components/auctionItem/ItemDetail";
import BidDetail from "../components/auctionItem/BidDetail";
import ImagesDisplay from "../components/auctionItem/ImagesDisplay";

export default {
  name: "AuctionPage",
  components: {
    ItemDetail,
    BidDetail,
    ImagesDisplay
  },
  data() {
    return {
      auction: null,
      bidPrice: 0,
      error: ""
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
    this.fetch();
  },
  created() {
    console.log("to", this.$route.params.id);
    console.log(this.$store.state.user);
    this.id = this.$route.params.id;
    this.$data.auction = this.$route.params.item;
  },
  methods: {
    fetch() {
      let item;
      this.$axios
        .get(`/auctions/${this.id}`)
        .then(res => {
          item = res.data.data;
          this.$axios
            .get(`/account/manage_profile/${res.data.data.seller_id}`)
            .then(res => {
              item["user"] = res.data.data;
              this.$data.auction = item;
            });
        })
        .catch(err => console.log(err));
    },
    placeBid() {
      let max = Math.max.apply(
        Math,
        this.$data.auction.biddings.map(function(e) {
          return e.price;
        })
      );
      if (this.$data.bidPrice > max) {
        console.log(this.$data.auction.id);
        console.log(this.$data.bidPrice);
        console.log(this.$store.state.user.id);
        this.$store.dispatch("auction/placeBidding", {
          auction_id: this.$data.auction.id,
          price: this.$data.bidPrice,
          user_id: this.$store.state.user.id
        });
      } else {
        this.$data.error = "* Bidding price must greater than current price.";
      }
    }
  }
};
</script>
