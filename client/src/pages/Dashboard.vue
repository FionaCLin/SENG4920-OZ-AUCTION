<template>
  <q-page padding class="row q-pa-sm q-ma-sm bg-grey-1 q-gutter-xl">
    <div class="col-2">
      <SideNav />
    </div>
    <q-page-container class="col-9">
      <div>
        <h3>Lastest Created Auctions</h3>
        <NewAuction />
      </div>
      <div>
        <h3>My Auctions List</h3>
        <MyAuctionsList />
      </div>
      <div>
        <h3>My Bids List</h3>
        <MyAuctionsList />
      </div>
    </q-page-container>
  </q-page>
</template>

<script>
import SideNav from "../components/DashboardSideNav";
import NewAuction from "../components/NewAuctionsList";
import MyAuctionsList from "../components/MyAuctionsList";

export default {
  name: "Dashboard",
  components: {
    SideNav,
    NewAuction,
    MyAuctionsList
  }
};
</script>
