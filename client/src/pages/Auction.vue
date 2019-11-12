<template>
  <q-page>
    <div class="row">
      <div class="col-xs-10 col-sm-6 col-md-5 col-lg-6 q-pa-md">
        <ItemDetail :auction="auction" />
        <div class="q-ma-lg">
          <q-btn class="q-ma-lg" color="green-4" flat>
            <q-icon name="check" />Accept
          </q-btn>
          <q-btn class="q-ma-lg" color="red-4" flat>
            <q-icon name="clear" />Decline
          </q-btn>
        </div>
      </div>
      <div class="col-xs-10 col-sm-5 col-md-4 col-lg-5 q-pa-sm q-ma-lg">
        <q-img :src="auction.image" class="q-ma-sm" />
        <div>
          <q-btn flat :to="`edit/${id}`"> <q-icon name="edit" />Update </q-btn>
        </div>
      </div>
      <div class="col-sm-12">
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
  methods: {}
};
</script>
