<template>
  <q-page padding class="row justify-center bg-grey-1">
    <q-card
      class="col-xs-12 col-sm-11 col-md-10 col-lg-9"
      style="min-width: 300px;"
    >
      <q-card-seciont>
        <q-item>
          <q-item-section avatar>
            <q-avatar class="self-center" size="100px" font-size="52px">
              <img :src="userProfile.avatar" />
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label>
              <ProfileDisplay :detail="userProfile" />
            </q-item-label>
            <q-item-label caption
              ><q-icon
                v-for="n in userProfile.rating"
                :key="n"
                name="star"
                style="font-size: 3em;"
              />
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-card-seciont>
    </q-card>
  </q-page>
</template>

<script>
import ProfileDisplay from "../components/Profile/UserDisplay";

export default {
  name: "UserProfile",
  components: {
    ProfileDisplay
  },
  data() {
    return {
      userProfile: null
    };
  },
  beforeMount() {
    this.fetch();
  },
  created() {
    this.id = this.$route.params.id;
    this.fetch();
  },
  methods: {
    fetch() {
      if (this.$data.userProfile) {
        return;
      }
      this.$axios
        .get(`/account/manage_profile/${this.id}`)
        .then(res => {
          this.$data.userProfile = res.data.data;
        })
        .catch(err => console.log(err));
    }
  }
};
</script>
