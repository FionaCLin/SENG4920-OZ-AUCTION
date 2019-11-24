<template>
  <q-list class="q-ma-lg">
    <q-item v-for="(f, k) in fields" :key="k">
      <q-item-section>
        <q-item-label>{{ k }}</q-item-label>
      </q-item-section>

      <q-item-section
        v-if="k === 'Seller'"
        @click="userProfile(auction.seller)"
      >
        <div class="row">
          <q-item-section avatar>
            <q-avatar size="60px" font-size="52px">
              <q-img :src="auction.seller.avatar" />
              <q-icon name="person" />
            </q-avatar>
          </q-item-section>
          <q-item-section class="q-ma-xs">
            <q-item-label>{{ auction.seller_name }}</q-item-label>
            <q-item-label caption>
              <q-icon
                v-for="n in auction.seller.rating"
                :key="n"
                name="star"
              ></q-icon>
            </q-item-label>
          </q-item-section>
        </div>
      </q-item-section>
      <q-item-section v-else>
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
      if (!biddings || biddings.length === 0) return 0;
      let max = Math.max.apply(
        Math,
        biddings.map(function(e) {
          return e.proposal_price;
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
        Seller: "seller_name",
        Location: "location",
        Category: "category",
        "Create Time": "created",
        "End Time": "end_time",
        "Start Price": "price",
        "Current Price": "bidding_info"
      }
    };
  },
  methods: {
    userProfile: function(user) {
      this.$router
        .push({
          name: "userProfile",
          params: {
            id: user.user_id,
            user: user
          }
        })
        .catch(err => console.log(err));
    }
  }
};
</script>
