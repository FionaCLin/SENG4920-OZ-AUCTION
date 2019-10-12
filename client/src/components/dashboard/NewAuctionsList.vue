<template>
  <div class="q-pa-md">
    <h5>
      <a name="newAuctions">New Auctions</a>
    </h5>

    <div
      class="fit row wrap justify-start items-start content-start  q-gutter-sm"
    >
      <NewAuctionItem v-for="n in 5" :key="n" />
    </div>
  </div>
</template>
<script>
import NewAuctionItem from "./NewItem";
export default {
  name: "NewAuction",
  components: {
    NewAuctionItem
  },
  data() {
    return {
      slide: 1
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
