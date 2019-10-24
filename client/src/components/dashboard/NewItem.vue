<template>
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
    >
      <div class="absolute-bottom custom-caption">
        <div class="text-h2">{{ item.title }}</div>
        <!-- <div class="text-subtitle1">{{ item.subtitle }}</div> -->
      </div>
    </q-carousel-slide>
  </q-carousel>
</template>

<script>
export default {
  name: "NewAuctionItem",
  props: ["newAuctions"],
  data() {
    return {
      slide: 1,
      items: [
        {
          title: "First Auction",
          subtitle: "Mountains",
          url: "https://cdn.quasar.dev/img/mountains.jpg"
        },
        {
          title: "Second Auction",
          subtitle: "Famous City",
          url: "https://cdn.quasar.dev/img/parallax1.jpg"
        },
        {
          title: "Third Auction",
          subtitle: "Famous Bridge",
          url: "https://cdn.quasar.dev/img/parallax2.jpg"
        }
      ]
    };
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
