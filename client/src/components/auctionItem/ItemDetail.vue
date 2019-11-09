<template>
  <q-list class="q-pa-md">
    <q-item v-for="(f, k) in fields" :key="k">
      <q-item-section>
        <q-item-label>{{ k }}</q-item-label>
        <q-item-label v-if="k === 'Start Price'" caption
          >${{ auction[f] }}</q-item-label
        >
        <q-item-label v-else caption>{{ auction[f] }}</q-item-label>
      </q-item-section>
    </q-item>

    <q-item>
      <q-item-section @click="userProfile(auction.seller_id)">
        <q-item-label>Seller</q-item-label>
        <q-item-section avatar>
          <q-avatar size="60px" font-size="52px">
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
</template>

<script>
export default {
  name: "AuctionItem",
  props: ["auction"],
  data() {
    return {
      fields: {
        Title: "title",
        Description: "description",
        "Start Price": "price",
        "Create Time": "created",
        "End Time": "end_time",
        Location: "location"
      }
    };
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
    }
  }
};
</script>
