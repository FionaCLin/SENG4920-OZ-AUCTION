<template>
  <q-page>
    <div class="row">
      <div class="col-xs-10 col-sm-6 col-md-5 col-lg-6 q-pa-md">
        <ItemDetail :auction="auction" />
        <div v-if="auction.bidding_info.length" class="q-ma-lg">
          <q-btn class="q-ma-lg" color="green-4" flat>
            <q-icon name="check" />Accept
          </q-btn>
          <q-btn class="q-ma-lg" color="red-4" flat>
            <q-icon name="clear" />Decline
          </q-btn>
        </div>
      </div>
      <div class="col-xs-10 col-sm-5 col-md-4 col-lg-5 q-pa-sm q-ma-lg">
        <ImagesDisplay :image="auction.image" />
        <div>
          <q-btn flat :to="`edit/${id}`"> <q-icon name="edit" />Update </q-btn>
          <q-btn v-if="isDelable()" flat @click="delItem">
            <q-icon name="delete_forever" />Delete
          </q-btn>
        </div>
      </div>
    </div>
    <div v-if="auction.bidding_info.length" class="col-12">
      <BidDetail :biddings="auction.bidding_info" />
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
      auction: this.auction_item
    };
  },
  computed: {
    auction_item: {
      get() {
        return this.$store.state.auction.myAuctions.find(
          x => x.id == this.$route.params.id
        );
      }
    }
  },
  beforeMount() {
    this.fetch();
  },
  created() {
    console.log("to", this.$route.params.id);
    console.log("to", this.$route.params.item);
    this.id = this.$route.params.id;
    this.$data.auction = this.$route.params.item;
    this.fetch();
  },
  methods: {
    isDelable() {
      if (
        this.$data.auction.bidding_info &&
        this.$data.auction.bidding_info.length
      ) {
        return false;
      } else {
        return true;
      }
    },
    fetch() {
      let item;
      if (this.$data.auction) {
        return;
      }
      this.$axios
        .get(`/auction/${this.id}`)
        .then(res => {
          item = res.data.data;
          this.$data.auction = item;
        })
        .catch(err => console.log(err));
    },
    delItem() {
      console.log("@@@");
      this.$store.dispatch("auction/deleteAuction", this.id).then(res => {
        console.log(res);
        this.$router.push("/myauctions").catch(err => console.log(err));
      });
    }
  }
};
</script>
