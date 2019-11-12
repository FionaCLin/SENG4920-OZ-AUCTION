<template>
  <q-layout view="hhh Lpr fff">
    <q-header elevated class="shadow-2 myColor" height-hint="98">
      <q-toolbar class="glossy myToolbar">
        <q-icon
          name="img:statics/logo.png"
          :ratio="16 / 9"
          class="myLogo"
        ></q-icon>
      </q-toolbar>
    </q-header>

    <q-footer elevated class="myColor">
      <q-toolbar>
        <q-toolbar-title class="myFooter"
          >Copyright © 2019 Awesome Group Co. All Rights
          Reserved.</q-toolbar-title
        >
      </q-toolbar>
    </q-footer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "Index",
  data() {
    return {
      drawer: false,
      miniState: true
    };
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
