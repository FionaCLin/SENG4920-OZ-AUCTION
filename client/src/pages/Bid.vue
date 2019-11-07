<template>
  <q-page>
    <div class="row">
      <div class="my-card col-sm-12">
        <div class="q-pa-lg text-subtitle">{{ pageTitle }}</div>
      </div>
      <div class="my-card col-sm-6">
        <q-list class="q-pa-md">
          <q-item>
            <q-item-section>
              <q-item-label>Title</q-item-label>
              <q-item-label caption>{{ auction.title }}</q-item-label>
            </q-item-section>
          </q-item>

          <q-item>
            <q-item-section>
              <q-item-label>Price</q-item-label>
              <q-item-label caption>${{ auction.price }}</q-item-label>
            </q-item-section>
          </q-item>

          <q-item>
            <q-item-section>
              <q-item-label>Create Time</q-item-label>
              <q-item-label caption>{{ auction.created }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label>End Time</q-item-label>
              <q-item-label caption>{{ auction.end_time }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label side>Location</q-item-label>
              <q-item-label caption>{{ auction.location }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
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
            <img :src="auction.image" />
          </q-item>

          <q-item>
            <q-btn flat :disable="!favorite"> <q-icon name="favorite"/></q-btn>
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
    initializePlayer: function() {
      console.log("here");
      // var cld = cloudinary.Cloudinary.new({ cloud_name: "og-tech", secure: true});
      //var demoplayer = cld.videoPlayer('video-player');
    },
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
