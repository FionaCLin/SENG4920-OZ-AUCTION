<template>
  <q-page>
    <div class="row">
      <div class="my-card col-sm-12">
        <q-btn flat :to="`edit/${id}`"> <q-icon name="edit" />Update</q-btn>
      </div>
      <div class="my-card col-sm-6">
        <q-list class="q-ma-md">
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
              <q-item-label>Location</q-item-label>
              <q-item-label caption>{{ auction.location }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
      <div class="col-sm-6">
        <q-list class="my-card col-sm-6">
          <q-item>
            <img :src="auction.image" />
          </q-item>
          <q-item v-ripple clickable @click="userProfile(auction.seller_id)">
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
          </q-item>
        </q-list>
      </div>
      <div class="col-sm-12">
        <!--  this part will contain the images -->
        <div id="demo" class="carousel slide" data-ride="carousel">
          <!-- Indicators -->
          <q-list class="carousel-indicators">
            <q-list-item
              v-for="single_media in media"
              :key="single_media.id"
              data-target="#demo"
              :data-slide-to="single_media.id"
            ></q-list-item>
          </q-list>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "AuctionPage",
  data() {
    return {
      auction: this.$store.state.auction.myAuctions.auction_items.find(
        x => x.id === this.$route.params.id
      ),
      media: [],
      product_name: "",
      product_desc: "",
      product_price: ""
    };
  },
  mounted: function() {
    // now we get all the related infomation for the particular product id
    //axios.get(`http://localhost:3128/getProductInfo/${this.$route.params.id}`)
    //.then( res => {
    //  console.log(res.data)
    this.media = [
      {
        id: "0",
        type: "image",
        url: "https://static.pexels.com/photos/265631/pexels-photo-265631.jpeg"
      },
      {
        id: "1",
        type: "image",
        url: `https://static.pexels.com/photos/265631/pexels-photo-265631.jpeg`
      },
      {
        id: "2",
        type: "image",
        url: `https://static.pexels.com/photos/265631/pexels-photo-265631.jpeg`
      },
      {
        id: "3",
        type: "video",
        url: `https://static.pexels.com/photos/265631/pexels-photo-265631.jpeg`
      }
    ];
    this.product_name = "hello";
    this.product_desc = "hello";
    this.product_price = "123";

    //})
  },
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.carousel-inner {
  height: 500px;
}
.carousel-item {
  height: 100%;
}
.single-image {
  width: 100%;
  height: 100%;
  object-fit: fill;
}
#demo {
  margin-left: 30px;
  margin-right: 30px;
}
</style>
