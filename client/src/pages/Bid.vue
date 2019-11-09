<template>
  <q-page>
    <div class="row">
      <div class="my-card col-sm-12"></div>

      <div class="col-sm-6 q-pa-md">
        <q-list class="my-card col-sm-6 flex flex-center">
          <q-img :src="auction.image" style="width: 60%;" />
          <q-item>
            <q-btn v-if="favorite" flat @click="removeFavorite">
              <q-icon name="favorite_border" />
            </q-btn>
            <q-btn v-else flat @click="addFavorite">
              <q-icon name="favorite" />
            </q-btn>
          </q-item>
        </q-list>
      </div>
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

          <q-item>
            <q-item-section @click="userProfile(auction.seller_id)">
              <q-item-label>Seller</q-item-label>
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
      auction: null,
      fields: {
        Title: "title",
        Description: "description",
        Price: "price",
        "Create Time": "created",
        "End Time": "end_time",
        Location: "location"
      },
      favorite: this.$store.state.user.favorites.indexOf(this.id) !== -1
    };
  },
  mounted: function() {},
  created() {
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
  methods: {
    getUser(id) {
      let auctions = this.$store.state.auction.auctions.find(
        x => x.sellers.seller_id === id
      );
      console.log(auctions);
      let user = auctions.sellers;
      user.name = auctions.auction_items[0].seller_name;
      return user;
    },
    user_avatar(id) {
      let user = this.getUser(id);
      return user.avatar;
    },
    user_rating(id) {
      let user = this.getUser(id);
      return user.rating;
    },
    userProfile: function(id) {
      console.log("from", id);
      this.$router.push({
        name: "userProfile",
        params: {
          id: id
        }
      });
    },
    addFavorite: function() {
      this.$store.state.user.favorites.push(this.id);
    },
    removeFavorite: function() {
      this.$store.state.user.favorites.slice(
        this.$store.state.user.favorites.indexOf(this.id)
      );
    }
    // ...mapActions(["addFavorite", "removeFavorite"])
  }
};
</script>
