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
          @click="$router.replace('/dashboard').catch(() => {})"
        ></q-icon>

        <q-space />
        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn round dense flat color="grey-8" icon="notifications">
            <q-badge color="red" text-color="white" floating>2</q-badge>
            <q-tooltip>Notifications</q-tooltip>
          </q-btn>

          <q-btn round flat>
            <q-avatar size="26px">
              <img v-if="user.avatar" :src="user.avatar" />
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
                    <img :src="user.avatar" />
                  </q-avatar>
                  <div class="text-weight-bold">
                    {{ user.first_name }} {{ user.last_name }}
                  </div>
                  <div>@{{ user.location }}</div>
                </div>
              </q-img>

              <q-list
                style="min-width: 200px; height: calc(100% - 150px); margin-top: 150px;"
              >
                <q-separator />
                <q-btn-group spread>
                  <q-btn label="Profile" to="/profile" />
                  <q-btn label="Signout" @click="signout" />
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
            $router.replace('/dashboard').catch(() => {});
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
            $router.replace('/myauctions').catch(() => {});
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
            $router.replace('/mybiddings').catch(() => {});
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
            $router.replace('/mywishlist').catch(() => {});
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
      <div v-if="ready">
        <router-view />
      </div>

      <div v-else class="flex flex-center">
        <q-circular-progress indeterminate size="150px" class="q-ma-md" />
      </div>
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
    return {
      drawer: false,
      miniState: true,
      search: null,
      user: this.$store.state.user,
      selected: "",
      ready: false,
      token: ""
    };
  },
  created() {
    // if (!localStorage.getItem("token") || !this.$store.state.user.token) {
    //   this.$router.push("/login").catch(() => {});
    // }

    let promises = [
      this.$store.dispatch("auction/getAllAuctions"),
      this.$store.dispatch(
        "auction/getMyAutions",
        this.$store.state.user.user_id
      ),
      this.$store.dispatch(
        "auction/getMyBiddings",
        this.$store.state.user.user_id
      ),
      this.$store.dispatch(
        "auction/getMyFavorite",
        this.$store.state.user.user_id
      )
    ];
    Promise.all(promises).then(res => {
      this.$data.ready = true;
      console.log(res, this.$data.ready, "ready");
    });
  },
  methods: {
    signout() {
      this.token = localStorage.getItem("token");
      console.log(this.token);
      this.$axios.delete(`/account/signout/${this.token}`).then(res => {
        console.log(res);
        localStorage.removeItem("token");
        this.$router.push("/");
      });
    }
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
