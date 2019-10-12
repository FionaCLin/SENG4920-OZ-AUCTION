<template>
  <q-page padding class="bg-grey-1 q-pa-none q-ma-none">
    <NewAuction />
    <MyAuctionsList />
    <MyBidsList />
  </q-page>
</template>

<script>
import NewAuction from "../components/dashboard/NewAuctionsList";
import MyAuctionsList from "../components/dashboard/MyAuctionsList";
import MyBidsList from "../components/dashboard/MyBidsList";

export default {
  name: "Dashboard",
  components: {
    NewAuction,
    MyAuctionsList,
    MyBidsList
  }
};
</script>
