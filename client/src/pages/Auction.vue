<template>
  <q-page>
    <div class="row">
      <div class="my-card col-sm-12"></div>
      <div class="my-card col-sm-6">
        <ItemDetail :auction="auction" />
      </div>
      <div class="col-sm-6 q-pa-md">
        <q-list class="my-card col-sm-6 fit column  justify-center ">
          <q-img :src="auction.image" style="width: 60%;" />
          <q-item>
            <q-btn flat :to="`edit/${id}`">
              <q-icon name="edit" />Update
            </q-btn>
          </q-item>
        </q-list>
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
