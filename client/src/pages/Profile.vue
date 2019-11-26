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
            <q-btn flat @click="updatePhoto">Upload</q-btn>
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
    <q-dialog v-model="dialog" persistent>
      <!-- <q-avatar icon="" color="primary" text-color="white" /> -->
      <div class="text-center">
        <q-uploader
          label="Avatar Images Upload"
          batch
          :factory="upload"
          style="width:100%"
        >
        </q-uploader>
      </div>
    </q-dialog>
  </q-page>
</template>

<script>
import ProfileDisplay from "../components/Profile/ProfileDisplay";
import ProfileEdit from "../components/Profile/ProfileEdit";
import { uploadImage, warning } from "../helper";

export default {
  name: "Profile",
  components: {
    ProfileDisplay,
    ProfileEdit
  },
  data() {
    return {
      edit: false,
      userProfile: this.$store.state.user,
      dialog: false,
      imgsupload: false
    };
  },
  beforeMount() {
    this.fetch();
  },
  created() {
    this.id = this.$store.state.user.user_id;
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
          console.log(res.data);
          this.$data.userProfile = res.data.data;
        })
        .catch(err => console.log(err));
    },
    updateDetail(data) {
      console.log(data);
      this.$data.userProfile = this.$store.state.user;
    },
    updatePhoto() {
      this.$data.dialog = true;
    },
    async upload(file) {
      console.log(this.$data.imgsupload, 1, file);
      this.$data.imgsupload = true;
      console.log(this.$data.imgsupload, 2);
      // let ps = [];
      // file.forEach(f => {
      let p = new Promise(function(resolve, reject) {
        uploadImage(file[0], (err, res) => {
          if (err) {
            reject(err.message);
          } else {
            resolve(res.Location);
          }
        });
      });
      await p
        .then(async res => {
          this.$data.userProfile.avatar = res;
          let data = { avatar: res };
          await this.$store
            .dispatch("user/updateProfile", data)
            .then(res => {
              console.log(res);
              this.$emit("updateEdit", false);
              this.$emit("editDetail", data);
              return res;
            })
            .catch(err => {
              warning.message = err.data.message;
              this.$q.notify(warning);
            });
        })
        .finally(() => {
          this.$data.imgsupload = false;
          this.$data.dialog = false;
        });
    }
  }
};
</script>
