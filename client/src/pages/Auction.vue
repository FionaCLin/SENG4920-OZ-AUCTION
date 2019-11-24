<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-xs-10 col-sm-6 col-md-5 col-lg-6 q-pa-md">
        <ItemDetail :auction="auction" />
      </div>
      <div class="col-xs-10 col-sm-5 col-md-4 col-lg-5 q-pa-sm q-ma-lg">
        <ImagesDisplay :image="auction.image" />
        <div class="row">

          <q-item-section>
            <div v-if="auction.status === 'BIDDING'">
              <div v-if="auction.bidding_info.length" class="row">
                <q-btn flat :to="`edit/${id}`"> <q-icon name="edit" />Update </q-btn>
                <q-btn v-if="isDelable()" flat @click="confirm = !confirm">
                  <q-icon name="delete_forever" />Delete
                </q-btn>
                <q-btn class="q-px-md" color="green-4" flat @click="accept = true">
                  <q-icon name="check" />Accept
                </q-btn>
                <q-btn class="q-px-md" color="red-4" flat @click="decline = true">
                  <q-icon name="clear" />Decline
                </q-btn>

                <q-dialog v-model="accept" persistent>
                  <q-card>
                    <q-card-section class="row items-center">
                      <span class="q-ml-sm">Are you sure to accept the auction?
                                            You cannot change after clicking confirm.
                      </span>
                    </q-card-section>

                    <q-card-actions align="right">
                      <q-btn flat label="Cancel" color="primary" @click="accept = false" v-close-popup />
                      <q-btn flat label="Confirm" color="primary" @click="acceptBid" v-close-popup />
                    </q-card-actions>
                  </q-card>
                </q-dialog>
                <q-dialog v-model="decline" persistent>
                  <q-card>
                    <q-card-section class="row items-center">
                      <span class="q-ml-sm">Are you sure to decline the auction?
                                            You cannot change after clicking confirm.
                      </span>
                    </q-card-section>

                    <q-card-actions align="right">
                      <q-btn flat label="Cancel" color="primary" @click="decline = false" v-close-popup />
                      <q-btn flat label="Confirm" color="primary" @click="declineBid" v-close-popup />
                    </q-card-actions>
                  </q-card>
                </q-dialog>

              </div>
            </div>
            <div v-else-if="auction.status === 'ACCEPTED'">
              <q-chip size="lg" icon="bookmark">
                {{ auction.status }}
              </q-chip>
            </div>
            <div v-else-if="auction.status === 'DECLINED'">
              <q-chip size="lg" icon="bookmark">
                {{ auction.status }}
              </q-chip>
            </div>
          </q-item-section>
        </div>
      </div>
    </div>
    <div v-if="auction.bidding_info.length" class="col-12">
      <BidDetail :biddings="auction.bidding_info" />
    </div>
    <Confirmation
      :state="confirm"
      @confirm="delItem"
      @toggle="confirm = !confirm"
    />
  </q-page>
</template>

<script>
import ItemDetail from "../components/auctionItem/ItemDetail";
import BidDetail from "../components/auctionItem/BidDetail";
import ImagesDisplay from "../components/auctionItem/ImagesDisplay";
import Confirmation from "../components/Confirmation";

export default {
  name: "AuctionPage",
  components: {
    ItemDetail,
    BidDetail,
    Confirmation,
    ImagesDisplay
  },
  data() {
    return {
      auction: this.auction_item,
      confirm: false,
      accept: false,
      decline: false,
      id: null,
      status: null
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
        this.$router
          .push({
            name: "myauctions",
            items: this.$store.state.auction.myAuctions
          })
          .catch(err => console.log(err));
      });
    },
    acceptBid() {
      console.log(this.$store.state.user.user_id);
      console.log(this.id);
      this.$axios
        .put('/bidding/operations',{
          "user_id": this.$store.state.user.user_id,
          "item_id": this.id,
          "operation": "accept"
        })
        .then(res => {
          console.log(res);
          this.status = "ACCEPTED";
          this.$store.commit("auction/updateMyAuctionStatus", {
            id: this.id,
            status: this.status
          });
        });
    },
    declineBid() {
      this.$axios
        .put('/bidding/operations',{
          "user_id": this.$store.state.user.user_id,
          "item_id": this.id,
          "operation": "decline"
        })
        .then(res => {
          console.log(res);
          this.status = "DECLINED";
          this.$store.commit("auction/updateMyAuctionStatus", {
            id: this.id,
            status: this.status
          });
        });
    }
  }
};
</script>
