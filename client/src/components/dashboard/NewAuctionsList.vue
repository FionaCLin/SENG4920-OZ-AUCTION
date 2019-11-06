<template>
  <div class="q-pa-md">
    <div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
      <q-carousel
        v-model="slide"
        class="col"
        animated
        navigation
        infinite
        autoplay
        transition-prev="slide-right"
        transition-next="slide-left"
        q-pa-none
        q-ma-none
      >
        <q-carousel-slide
          v-for="(item, index) in items"
          :key="index"
          :name="index"
          :img-src="item.url"
          @click="auctionItem(item.id)"
        >
          <div class="absolute-bottom custom-caption">
            <div class="text-overline">
              {{ item.title }}
            </div>
            <div class="text-caption text-italic">{{ item.description }}</div>
          </div>
        </q-carousel-slide>
      </q-carousel>
    </div>
  </div>
</template>

<script>
export default {
  name: "NewAuction",
  props: ["newAuctions"],
  data() {
    return {
      slide: 1,
      items: this.$store.state.auction.myAuctions.auction_items.map(x => {
        return {
          title: x.title,
          description: x.description,
          url: x.image,
          id: x.id
        };
      })
    };
  },
  methods: {
    auctionItem: function(id) {
      console.log("from", id);
      this.$router.push({
        name: "auctiionItem",
        params: {
          id: id
        }
      });
    }
  }
};
</script>

<style lang="sass" scoped>
.custom-caption
  text-align: center
  padding: 12px
  color: white
  background-color: rgba(0, 0, 0, .3)
</style>
