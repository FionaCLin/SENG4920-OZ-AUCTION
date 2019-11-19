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
        <q-img :src="auction.image[0]" class="q-ma-sm" />
        <div>
          <q-btn flat :to="`edit/${id}`"> <q-icon name="edit" />Update </q-btn>
          <q-btn v-if="isDelable()" flat @click="delItem">
            <q-icon name="cross" />Delete
          </q-btn>
        </div>
      </div>
      <div class="col-sm-12">
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
    this.fetch();
  },
  created() {
    console.log("to", this.$route.params.id);
    console.log("to", this.$route.params.item);
    this.id = this.$route.params.id;
    this.$data.auction = this.$route.params.item;
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
    delItem() {
      //todo move to actiuon and mutation my auctions to remove tghe item
      this.$axios
        .delete(`/auctions/${this.id}`)
        .then(res => {
          console.log(res);
          this.$router.push("/myauctions").catch(err => console.log(err));
        })
        .catch(err => {
          console.log(err.response);
        });
    }
  }
};
</script>
