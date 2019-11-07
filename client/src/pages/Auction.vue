<template>
  <q-page>
    <div class="row">
      <div class="my-card col-sm-12"></div>
      <div class="my-card col-sm-6">
        <q-list class="q-pa-md">
          <q-item v-for="(f, k) in fields" :key="k">
            <q-item-section>
              <q-item-label>{{ k }}</q-item-label>
              <q-item-label v-if="k === 'Price'" caption
                >${{ auction[f] }}</q-item-label
              >
              <q-item-label v-else caption>{{ auction[f] }}</q-item-label>
            </q-item-section>
          </q-item>

          <q-item v-if="pageTitle !== 'My Auctions'">
            <q-item-section @click="userProfile(auction.seller_id)">
              <q-item-label side>Seller</q-item-label>
              <q-item-section avatar>
                <q-avatar>
                  <img :src="user_avatar(auction.seller_id)" />
                </q-avatar>
              </q-item-section>
              <q-item-section class="q-ma-xs">
                <q-item-label>{{ auction.seller_name }}</q-item-label>
                <q-item-label caption>
                  <q-icon
                    v-for="n in user_rating(auction.seller_id)"
                    :key="n"
                    name="star"
                  ></q-icon>
                </q-item-label>
              </q-item-section>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
      <div class="col-sm-6 q-pa-md">
        <q-list class="my-card col-sm-6">
          <q-item>
            <q-img :src="auction.image" style="width: 60%;" />
          </q-item>

          <q-item>
            <q-btn flat :to="`edit/${id}`"> <q-icon name="edit" />Update</q-btn>
          </q-item>
        </q-list>
      </div>
      <div class="col-sm-12">
        <!--  this part will contain the images -->
        <!-- Indicators -->
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "AuctionPage",
  props: ["pageTitle"],
  data() {
    return {
      fields: {
        Title: "title",
        Description: "description",
        Price: "price",
        "Create Time": "created",
        "End Time": "end_time",
        Location: "location"
      },
      auction: this.$store.state.auction.myAuctions.auction_items.find(
        x => x.id === this.$route.params.id
      )
    };
  },
  mounted: function() {},
  created() {
    console.log("to", this.$route.params.id);
    this.id = this.$route.params.id;
  },
  methods: {
    user_avatar(id) {
      console.log(id, 9999999);
      return this.$store.state.auction.myAuctions.sellers.avatar;
    },
    user_rating(id) {
      console.log(id, 9999999);
      return this.$store.state.auction.myAuctions.sellers.rating;
    },
    userProfile: function(id) {
      console.log("from", id);
      this.$router.push({
        name: "userProfile",
        params: {
          id: id
        }
      });
    }
  }
};
</script>
