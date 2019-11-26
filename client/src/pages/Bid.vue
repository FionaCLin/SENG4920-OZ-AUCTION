<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-xs-10 col-sm-5 col-md-4 col-lg-5 q-ma-lg">
        <div>
          <ImagesDisplay
            v-if="auction && auction.image"
            :image="auction.image"
          />
        </div>
        <div v-if="auction && auction.status === 'BIDDING'">
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
        <div v-if="auction && auction.status === 'ACCEPTED'">
          <q-chip size="lg" icon="bookmark"
            >AUCTION FINISHED: {{ auction.status }}</q-chip
          >
        </div>
        <div v-if="auction && auction.status === 'DECLINED'">
          <q-chip size="lg" icon="bookmark"
            >AUCTION FINISHED: {{ auction.status }}</q-chip
          >
        </div>
      </div>
      <div class="col-xs-10 col-sm-6 col-md-5 col-lg-6 q-pa-md">
        <ItemDetail v-if="auction" :auction="auction" />
      </div>
      <div class="col-10 q-ma-md fit column justify-center item-center">
        <!--  this part will contain the images -->
        <!-- Indicators -->
        <BidDetail
          v-if="auction && auction.bidding_info.length"
          :biddings="auction.bidding_info"
        />
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
    this.id = this.$route.params.id;
    this.from = this.$route.params.from;
    this.fetch();
  },
  methods: {
    addFavorite() {
      this.$axios
        .put("/auction/favorite/set", {
          user_id: this.$store.state.user.user_id,
          auction_id: this.id
        })
        .then(res => {
          this.$store.commit("user/addFavorite", this.id);

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
      this.$axios
        .put("/auction/favorite/unset", {
          user_id: this.$store.state.user.user_id,
          auction_id: this.id
        })
        .then(res => {
          this.$store.commit("user/removeFavorite", this.id);

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
    async fetch() {
      let bidding = await this.$axios
        .get(`/auction/${this.id}`)
        .then(res => {
          console.log(res.data.data);
          this.$data.auction = res.data.data;
          return res.data.data.bidding_info;
        })
        .catch(err => console.log(err));
      return bidding;
    },
    placeBid() {
      let max = this.$data.auction.price;
      if (this.$data.auction.bidding_info) {
        max = Math.max.apply(
          Math,
          this.$data.auction.bidding_info.map(function(e) {
            return e.proposal_price;
          })
        );
      }

      if (this.$data.bidPrice > max) {
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
            if (res.status == 200) {
              this.$q.notify({
                color: "green-4",
                textColor: "white",
                icon: "cloud_done",
                message: res.data.message
              });
            } else {
              this.$q.notify({
                color: "red-4",
                textColor: "white",
                icon: "warning",
                message: res.data.message
              });
            }
            this.fetch();
          })
          .catch(() => {
            // this.$data.error = err;
            // if (err && err.response) {
            //   let message = err.response.data.message;
            //   this.$data.error = message.slice(message.indexOf(":") + 1);
            // }
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
