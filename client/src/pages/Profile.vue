<template>
  <q-page padding>
    <h5>Profile</h5>
    <q-card class="my-card">
      <q-item>
        <q-item-section avatar>
          <q-avatar class="self-center" size="100px" font-size="52px">
            <img :src="user.Avatar" />
          </q-avatar>
          <q-card-actions>
            <q-btn flat>Upload</q-btn>
            <q-btn flat>Remove</q-btn>
          </q-card-actions>
        </q-item-section>
        <q-item-section>
          <div class="q-gutter-y-md col-auto q-ma-md">
            <q-field
              v-for="(val, index) in user.detail"
              :key="index"
              filled
              :label="`${index}: `"
              stack-label
            >
              <template v-if="index !== 'Avatar'" v-slot:control>
                <div
                  v-if="index == 'Password'"
                  class="self-center full-width no-outline text-left"
                  tabindex="0"
                >
                  {{ val.replace(/./g, "*") }}
                </div>
                <div
                  v-else
                  class="self-center full-width no-outline text-left"
                  tabindex="0"
                >
                  {{ val }}
                </div>
              </template>
            </q-field>
          </div>
          <q-card-actions>
            <q-btn label="Submit" type="submit" color="green" flat />
            <q-space />

            <!-- <q-btn label="Reset" type="reset" color="warning" flat />
            <q-space /> -->

            <q-btn label="Cancel" type="cancel" color="red" flat />
          </q-card-actions>
        </q-item-section>
      </q-item>
    </q-card>
  </q-page>
</template>

<script>
let user = {
  Avatar: "https://cdn.quasar.dev/img/boy-avatar.png",
  detail: {
    "First Name": "Fiona",
    "Last Name": "Lin",
    "E-mail": "fiona.lin@student.unsw.edu.au",
    Password: "Bitmd?",
    Seller: true
  }
};

export default {
  name: "Profile",
  data() {
    return {
      user
    };
  }
};
</script>
