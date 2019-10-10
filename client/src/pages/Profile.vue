<template>
  <q-page padding>
    <h5>Profile</h5>
    <div class="q-gutter-y-md column">
      <q-field
        v-for="(val, index) in userDetail"
        :key="index"
        filled
        :value="key"
        :prefix="(index == 'Avatar') ?  '' : `${index}: `"
      >
        <template v-if="index == 'Avatar'" v-slot:control>
          <q-avatar size="100px" font-size="52px">
            <img :src="val" />
          </q-avatar>
          <q-space />
          <q-btn>Upload</q-btn>
          <q-space />
          <q-btn>Remove</q-btn>
        </template>
        <template v-else v-slot:control>
          <div
            v-if="index == 'Password'"
            class="self-center full-width no-outline text-right"
            tabindex="0"
          >{{val.replace(/./g, '*')}}</div>
          <div v-else class="     -center full-width no-outline text-right" tabindex="0">{{val}}</div>
        </template>
      </q-field>
    </div>
    <p></p>
    <p>Submit Button</p>
    <p>Reset Button</p>
    <p>Cancel button</p>
  </q-page>
</template>

<script>
let userDetail = {
  Avatar: "https://cdn.quasar.dev/img/avatar.png",
  "First Name": "Fiona",
  "Last Name": "Lin",
  'E-mail': "fiona.lin@student.unsw.edu.au",
  Password: "Bitmd?",
  Seller: true
};
export default {
  name: "Profile",
  data() {
    return {
      userDetail
    };
  }
};
</script>
