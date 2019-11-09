<template>
  <q-list>
    <q-item v-for="i in biddings" :key="i" class="q-ma-auto q-pa-lg">
      <q-item-section
        avatar
        class="col-1 q-ma-auto column justify-center item-center"
      >
        <q-avatar size="60px" font-size="52px">
          <img :src="user_avatar(i.user_id)" />
        </q-avatar>
      </q-item-section>

      <q-item-section side class="col-3">
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
      <q-item-section side class="col-3">
        <q-item-label class="text-h4">${{ i.price }}</q-item-label>
        <q-item-label class="text-body1">{{ i.created }}</q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
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
