<template>
  <q-page padding class="row justify-center bg-grey-1">
    <q-card
      class="col-xs-12 col-sm-11 col-md-10 col-lg-9"
      style="min-width: 300px;"
    >
      <q-item>
        <q-item-section avatar>
          <q-avatar class="self-center" size="100px" font-size="52px">
            <img :src="userProfile.avatar" />
          </q-avatar>
          <q-card-actions>
            <q-btn flat>Upload</q-btn>
            <q-btn flat>Remove</q-btn>
          </q-card-actions>
        </q-item-section>
        <q-item-section>
          <ProfileDisplay
            v-if="!edit"
            :detail="userProfile"
            @updateEdit="edit = $event"
          />
          <ProfileEdit
            v-else
            :detail="userProfile"
            @updateEdit="edit = $event"
            @editDetail="updateDetail"
          />
        </q-item-section>
      </q-item>
    </q-card>
  </q-page>
</template>

<script>
import ProfileDisplay from "../components/Profile/ProfileDisplay";
import ProfileEdit from "../components/Profile/ProfileEdit";

export default {
  name: "Profile",
  components: {
    ProfileDisplay,
    ProfileEdit
  },
  data() {
    return {
      edit: false
    };
  },
  computed: {
    userProfile: {
      get() {
        // this.$store.state.user.foreach(element => console.log(element));
        console.log(typeof this.$store.state.user);
        return Object.keys(this.$store.state.user)
          .filter(k => !["logged", "token"].includes(k))
          .reduce((obj, key) => {
            obj[key] = this.$store.state.user[key];
            return obj;
          }, {});
      }
    }
  },
  methods: {
    onUpdate(val) {
      console.log(val, "Profile");
    },
    updateDetail(val) {
      Object.keys(val).forEach(k => {
        if (val[k] !== this.$store.state.user[k]) {
          // todo add mutation method to update user state
          console.log(k, val[k], this.$store.state.user[k]);
        }
      });
    }
  }
};
</script>
