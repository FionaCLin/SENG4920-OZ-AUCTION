<template>
  <q-page class="bg-grey-1">
    <div v-if="ready">
      <NewAuction :new-auctions="newAuctions" />

      <MyAuctionsList :alink="`auctions`" :items="auctions" />
    </div>
    <q-page-container v-else class="flex flex-center">
      <q-circular-progress indeterminate size="150px" class="q-ma-md" />
    </q-page-container>
  </q-page>
</template>

<script>
import NewAuction from "../components/dashboard/NewAuctionsList";
import MyAuctionsList from "../components/dashboard/MyAuctionsList";

export default {
  name: "Dashboard",
  components: {
    NewAuction,
    MyAuctionsList
  },
  data() {
    return {
      ready: this.$store.state.auction.auctions.length
    };
  },
  computed: {
    auctions: {
      get() {
        return this.$store.state.auction.auctions;
      }
    },
    newAuctions: {
      get() {
        return this.$store.state.auction.auctions.map(x => {
          return {
            title: x.title,
            description: x.description,
            url: x.image[0],
            id: x.id
          };
        });
      }
    }
  },
  created() {}
};
</script>
