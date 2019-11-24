<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-xs-10 col-sm-5 col-md-4 col-lg-5 q-ma-lg">
        <div>
          <ImagesDisplay :image="auction.image" />
        </div>
        <div  v-if="auction.status === 'BIDDING'">
          <div class="q-px-md row">
            <div class="col-10 row">
              <q-input
                v-model="bidPrice"
                prefix="AUD$"
                class="col-6"
                type="number"
              />
              <q-btn class="col-6" @click="placeBid">
                <q-icon name="gavel" />Place Bid
              </q-btn>
              <div class="q-ml-lg text-red">{{ error }}</div>
            </div>
            <div class="col-2" style="position: relative;">
              <q-btn
                v-if="favorite"
                class="myFavorite"
                flat
                @click="removeFavorite"
              >
                <q-icon name="favorite" />
                <q-tooltip>Remove from My Wishlist</q-tooltip>
              </q-btn>
              <q-btn v-else class="myFavorite" flat @click="addFavorite">
                <q-icon name="favorite_border" />
                <q-tooltip>Add to My Wishlist</q-tooltip>
              </q-btn>
            </div>
          </div>
        </div>
        <div v-else-if="auction.status === 'ACCEPTED'">
          <q-chip size="lg" icon="bookmark">
            AUCTION FINISHED:  {{ auction.status }}
          </q-chip>
        </div>
        <div v-else-if="auction.status === 'DECLINED'">
          <q-chip size="lg" icon="bookmark">
            AUCTION FINISHED:  {{ auction.status }}
          </q-chip>
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
      bidPrice: 0,
      error: "",
      id: "",
      auction: null
    };
  },
  computed: {
    favorite: {
      get() {
        return this.$store.state.user.favorites.indexOf(Number(this.id)) !== -1;
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
    this.from = this.$route.params.from;
    this.fetch();
  },
  methods: {
    addFavorite() {
      console.log("Add");
      this.$axios
        .put("/auction/favorite/set", {
          user_id: this.$store.state.user.user_id,
          auction_id: this.id
        })
        .then(res => {
          this.$store.commit("user/addFavorite", this.id);
          this.$store.commit("auction/addWishList", this.id);
          this.favorite.get;
          console.log(this.$store.state.user.favorites);
          this.$q.notify({
            color: "green-4",
            textColor: "white",
            position: "top",
            icon: "cloud_done",
            message: res.data.message
          });
        })
        .catch(err => console.log(err));
    },
    removeFavorite() {
      console.log("remove");
      console.log(this.$store.state.user.user_id);
      this.$axios
        .put("/auction/favorite/unset", {
          user_id: this.$store.state.user.user_id,
          auction_id: this.id
        })
        .then(res => {
          this.$store.commit("user/removeFavorite", this.id);
          this.$store.commit("auction/removeWishList", this.id);

          this.favorite.get;
          console.log(this.$store.state.user.favorites);
          this.$q.notify({
            color: "green-4",
            textColor: "white",
            position: "top",
            icon: "cloud_done",
            message: res.data.message
          });
        })
        .catch(err => console.log(err));
    },
    fetch() {
      let item;
      return this.$axios
        .get(`/auction/${this.id}`)
        .then(res => {
          item = res.data.data;
          this.$data.auction = item;
          console.log("new auction is ", this.$data.auction);
        })
        .catch(err => console.log(err));
    },
    placeBid() {
      console.log(this.$data.auction);
      let max = Math.max.apply(
        Math,
        this.$data.auction.bidding_info.map(function(e) {
          return e.proposal_price;
        })
      );

      if (this.$data.bidPrice > max) {
        console.log(this.$data.auction.id);
        console.log(this.$data.bidPrice);
        console.log(this.$store.state.user.user_id, "==========");

        let buyer = {
          user_id: this.$store.state.user["user_id"],
          first_name: this.$store.state.user["first_name"],
          last_name: this.$store.state.user["last_name"],
          avatar: this.$store.state.user["avatar"],
          location: this.$store.state.user["location"],
          rating: this.$store.state.user["rating"]
        };
        let bid = {
          item_id: this.$data.auction.id,
          proposal_price: Number(this.$data.bidPrice),
          user_id: this.$store.state.user.user_id
        };
        this.$store
          .dispatch("auction/placeBidding", { bid, buyer })
          .then(res => {
            console.log(res);
            this.fetch();
          })
          .catch(err => {
            this.$data.error = err;
          });
      } else {
        this.$data.error = `* Bidding price $ ${this.$data.bidPrice} must greater than current price $ ${max}.`;
      }
    }
  }
};
</script>

<style scoped>
.myFavorite {
  padding: 10%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
