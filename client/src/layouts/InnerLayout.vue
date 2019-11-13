<template>
  <q-layout view="hhh Lpr fff">
    <q-header elevated class="shadow-2 myColor" height-hint="98">
      <q-toolbar class="glossy myToolbar">
        <q-btn flat round dense icon="menu" @click="drawer = !drawer" />
        <q-icon
          push
          name="img:statics/logo.png"
          :ratio="16 / 9"
          class="myLogo"
          @click="$router.replace('/dashboard')"
        ></q-icon>

        <q-space />
        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn round dense flat color="grey-8" icon="notifications">
            <q-badge color="red" text-color="white" floating>2</q-badge>
            <q-tooltip>Notifications</q-tooltip>
          </q-btn>

          <q-btn round flat>
            <q-avatar size="26px">
              <img
                v-if="avatarUrl"
                src="https://seng4920album.s3.amazonaws.com/-1573553221037-Capture1.PNG"
              />
              <q-icon name="person" />
            </q-avatar>
            <q-tooltip>Account</q-tooltip>
            <q-menu transition-show="flip-right" transition-hide="flip-left">
              <q-img
                class="absolute-top"
                src="https://cdn.quasar.dev/img/material.png"
                style="height: 150px"
              >
                <div class="absolute-bottom bg-transparent">
                  <q-avatar size="56px" class="q-mb-sm">
                    <img
                      src="https://seng4920album.s3.amazonaws.com/-1573553221037-Capture1.PNG"
                    />
                  </q-avatar>
                  <div class="text-weight-bold">Razvan Stoenescu</div>
                  <div>@rstoenescu</div>
                </div>
              </q-img>

              <q-list
                style="min-width: 200px; height: calc(100% - 150px); margin-top: 150px;"
              >
                <q-separator />

                <q-btn-group spread>
                  <q-btn label="Profile" to="/profile" />
                  <q-btn label="Signout" />
                </q-btn-group>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <q-footer elevated class="myColor">
      <q-toolbar>
        <q-toolbar-title class="myFooter">
          Copyright © 2019 Awesome Group Co. All Rights Reserved.
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>

    <q-drawer
      v-model="drawer"
      show-if-above
      :mini="miniState"
      :width="200"
      :breakpoint="500"
      bordered
      content-class="bg-grey-3"
      @mouseover="miniState = false"
      @mouseout="miniState = true"
    >
      <q-list padding>
        <q-item
          v-ripple
          clickable
          :active="selected === 'dashboard'"
          push
          @click="
            selected = 'dashboard';
            $router.replace('/dashboard');
          "
        >
          <q-item-section avatar>
            <q-icon name="show_chart" />
          </q-item-section>

          <q-item-section>Dashboard</q-item-section>
        </q-item>

        <q-item
          v-ripple
          clickable
          :active="selected === 'gavel'"
          push
          @click="
            selected = 'gavel';
            $router.replace('/user/myAuctions');
          "
        >
          <q-item-section avatar>
            <q-icon name="gavel" />
          </q-item-section>

          <q-item-section>My Auctions</q-item-section>
        </q-item>

        <q-item
          v-ripple
          clickable
          :active="selected === 'collections_bookmark'"
          push
          @click="
            selected = 'collections_bookmark';
            $router.replace('/user/myBiddings');
          "
        >
          <q-item-section avatar>
            <q-icon name="collections_bookmark" />
          </q-item-section>

          <q-item-section>My Biddings</q-item-section>
        </q-item>

        <q-item
          v-ripple
          clickable
          :active="selected === 'favorite'"
          push
          @click="
            selected = 'favorite';
            $router.replace('/user/myWishlist');
          "
        >
          <q-item-section avatar>
            <q-icon name="favorite" />
          </q-item-section>

          <q-item-section>My Wishlist</q-item-section>
        </q-item>

        <q-item
          v-ripple
          clickable
          :active="selected === 'search'"
          push
          @click="
            selected = 'search';
            $router.replace('/search');
          "
        >
          <q-item-section avatar>
            <q-icon name="search" />
          </q-item-section>

          <q-item-section>Search</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
// import Nav from "../components/DashboardSideNav";
// import mapState from "vuex";

export default {
  name: "HomeLayout",
  props: ["menu"],
  data() {
    console.log(this.$route.path);
    console.log(this.$store.state.user.avatar);
    return {
      drawer: false,
      miniState: true,
      search: null,
      avatarUrl: this.$store.state.user.avatar,
      selected: ""
    };
  },
  created() {
    this.$store.dispatch("auction/getAllAuctions");
    this.$store.dispatch(
      "auction/getMyAuctions",
      this.$store.state.user.user_id
    );
    this.$store.dispatch("auction/getMyBiddings", 2);
    this.$store.dispatch("auction/getMyFavorite", 1);
  }
};
</script>

<style scoped>
.myColor {
  background-color: rgba(0, 0, 0, 0.7);
}

.myToolbar {
  margin-top: 10px 0px;
  padding: 12px 10px;
}

.myLogo {
  height: 60px;
  width: 210px;
  margin-left: 10px;
  padding: 5px 5px;
}

.myFooter {
  text-align: center;
  font-size: 0.9em;
}
</style>
