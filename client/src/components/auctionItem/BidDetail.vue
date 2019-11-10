<template>
  <div>
    <div
      v-for="(i, k) in biddings"
      :key="k"
      class="q-ma-auto q-pa-lg row justify-center item-center"
    >
      <!-- {{ i }} -->
      <div
        class="q-ma-xs col-xs-10 col-sm-2 col-md-2 col-lg-3 q-ma-auto column justify-center item-center"
      >
        <q-avatar size="68px" font-size="32px">
          <img :src="user_avatar(i.user_id)" />
        </q-avatar>
      </div>
      <div
        class="q-ma-xs col-xs-10 col-sm-3 col-md-3 col-lg-3 q-ma-auto column justify-center item-center"
      >
        <span class="text-weight-bold">{{ getUser(i.user_id).name }}</span>
        <div caption>{{ getUser(i.user_id).location }}</div>
        <div caption>
          <q-icon
            v-for="n in user_rating(i.user_id)"
            :key="n"
            name="star"
          ></q-icon>
        </div>
      </div>
      <div
        class="q-ma-xs col-xs-10 col-sm-5 col-md-6 col-lg-4 q-ma-auto column justify-center item-center"
      >
        <div class="text-h6">${{ i.price }}</div>
        <div class="text-subtitle1">{{ i.created }}</div>
      </div>
      <!-- <q-item-section
        avatar
        class="col-xs-1 col-sm-4 col-md-3 col-lg-2 q-ma-auto column justify-center item-center"
      >
        <q-avatar size="68px" font-size="32px">
          <img :src="user_avatar(i.user_id)" />
        </q-avatar>
      </q-item-section>

      <q-item-section side class="col-xs-3mcol-sm-4 col-md-3 col-lg-2 ">
        <q-item-label>
          <span class="text-weight-bold">{{
            getUser(i.user_id).name
          }}</span></q-item-label
        >
        <q-item-label caption>{{ getUser(i.user_id).location }}</q-item-label>
        <q-item-label caption>
          <q-icon
            v-for="n in user_rating(i.user_id)"
            :key="n"
            name="star"
          ></q-icon>
        </q-item-label>
      </q-item-section>
      <q-item-section side class="col-xs-4">
        <q-item-label class="text-h4">${{ i.price }}</q-item-label>
        <q-item-label class="text-body1">{{ i.created }}</q-item-label>
      </q-item-section>-->
    </div>
  </div>
</template>
<script>
export default {
  name: "BidItem",
  props: ["biddings"],
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
    }
  }
};
</script>
