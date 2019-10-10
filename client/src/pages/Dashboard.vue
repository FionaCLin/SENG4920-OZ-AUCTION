<template>
  <q-page padding class="bg-grey-1 q-pa-none q-ma-none">
    <NewAuction />
    <MyAuctionsList />
    <MyBidsList />
  </q-page>
</template>

<script>
import NewAuction from "../components/NewAuctionsList";
import MyAuctionsList from "../components/MyAuctionsList";
import MyBidsList from "../components/MyBidsList";

export default {
  name: "Dashboard",
  components: {
    NewAuction,
    MyAuctionsList,
    MyBidsList
  }
};
</script>
