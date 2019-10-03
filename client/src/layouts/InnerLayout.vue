<template>
  <q-layout view="hHh lpR lFf">
    <q-header elevated class="bg-light-green-8 text-white" height-hint="98">
      <q-toolbar class="GPL__toolbar">
        <q-btn flat to="/dashboard" push>
          <q-icon name="img:statics/bid.gif" :ratio="1" size="40px"></q-icon>
        </q-btn>
        <q-toolbar-title>Bid Your Way Auction</q-toolbar-title>

        <q-toolbar-title>
          <q-input
            class="bg-white text-grey-8 GPL__toolbar-input"
            dense
            standout="bg-primary"
            v-model="search"
            placeholder="Search"
          >
            <template v-slot:prepend>
              <q-icon v-if="search === ''" name="search" />
              <q-icon
                v-else
                name="clear"
                class="cursor-pointer"
                @click="search = ''"
              />
            </template>
          </q-input>
        </q-toolbar-title>
        <q-space />
        <div class="q-gutter-sm row items-center no-wrap">
          <!-- <q-btn round dense flat color="text-grey-7" icon="apps">
            <q-tooltip>Google Apps</q-tooltip>
          </q-btn>-->
          <q-btn round dense flat color="grey-8" icon="notifications">
            <q-badge color="red" text-color="white" floating>2</q-badge>
            <q-tooltip>Notifications</q-tooltip>
          </q-btn>
          <q-btn round flat to="/profile">
            <q-avatar size="26px">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
            </q-avatar>
            <q-tooltip>Account</q-tooltip>
          </q-btn>
        </div>
      </q-toolbar>

      <q-tabs align="left">
        <q-route-tab icon="home" to="/dashboard" replace label="Dashboard" />
        <q-route-tab icon="gavel" to="/auctions" replace label="My Auction" />
        <q-route-tab
          icon="search"
          to="/search"
          replace
          label="Search Auctions"
        />
      </q-tabs>
    </q-header>
    <q-page-container>
      <!-- This is where pages get injected -->
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "HomeLayout",

  data() {
    return {
      search: null,
      leftDrawer: true
    };
  }
};
</script>
