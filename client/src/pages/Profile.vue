<template>
  <q-page padding class="row justify-center bg-grey-1">
    <q-card
      class="col-xs-12 col-sm-11 col-md-10 col-lg-9"
      style="min-width: 300px;"
    >
      <q-item>
        <q-item-section avatar>
          <q-avatar class="self-center" size="100px" font-size="52px">
            <img :src="avatar" />
          </q-avatar>
          <q-card-actions>
            <q-btn flat>Upload</q-btn>
            <q-btn flat>Remove</q-btn>
          </q-card-actions>
        </q-item-section>
        <q-item-section>
          <ProfileDisplay
            v-if="!edit"
            :detail="user"
            :avatarurl="avatar"
            @updateEdit="edit = $event"
          />
          <ProfileEdit
            v-else
            :detail="user"
            :avatarurl="avatar"
            @updateEdit="edit = $event"
          />
        </q-item-section>
      </q-item>
    </q-card>
  </q-page>
</template>

<script>
const user = {
  Avatar: "https://cdn.quasar.dev/img/boy-avatar.png",
  detail: {
    "First Name": "Fiona",
    "Last Name": "Lin",
    "E-mail": "fiona.lin@student.unsw.edu.au",
    Password: "Bitmd?",
    Age: 18,
    Seller: true
  }
};

import ProfileDisplay from "../components/Profile/ProfileDisplay";
import ProfileEdit from "../components/Profile/ProfileEdit";

export default {
  name: "Profile",
  components: {
    ProfileDisplay,
    ProfileEdit
  },
  props: {
    userDetail: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      edit: false,
      user: user.detail,
      avatar: user.Avatar
    };
  },
  methods: {
    onUpdate(val) {
      console.log(val, "Profile");
    }
  }
};
</script>
