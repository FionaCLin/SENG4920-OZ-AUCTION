<template>
  <q-list class="q-ma-lg">
    <q-item v-for="(f, k) in fields" :key="k">
      <q-item-section>
        <q-item-label>{{ k }}</q-item-label>
      </q-item-section>

      <!-- <q-item-section
        v-if="k === 'Seller'"
        @click="userProfile(auction.seller_id)"
      >
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
      </q-item-section> -->

      <q-item-section>
        <!-- <q-item-section v-else> -->
        <q-item-label v-if="k === 'Start Price'" caption>{{
          auction[f] | currency
        }}</q-item-label>
        <q-item-label v-else-if="k === 'Current Price'" caption>{{
          auction[f] | current_price | currency
        }}</q-item-label>
        <q-item-label v-else caption>{{ auction[f] }}</q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script>
export default {
  name: "AuctionItem",
  filters: {
    currency: function(value) {
      return "$" + Number.parseFloat(value).toFixed(2);
    },
    current_price: function(biddings) {
      if (!biddings) return 0;
      let max = Math.max.apply(
        Math,
        biddings.map(function(e) {
          return e.price;
        })
      );
      return max;
    }
  },
  props: ["auction"],
  data() {
    return {
      fields: {
        Title: "title",
        Description: "description",
        Seller: "",
        Location: "location",
        "Create Time": "created",
        "End Time": "end_time",
        "Start Price": "price",
        "Current Price": "biddings"
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
