<template>
  <q-page padding class="row justify-center bg-grey-1">
    <q-card
      class="col-xs-12 col-sm-11 col-md-10 col-lg-9"
      style="min-width: 300px;"
    >
      <q-item>
        <q-item-section avatar class="flex flex-center">
          <q-avatar class="self-center" size="100px" font-size="52px">
            <q-img v-if="userProfile.avatar" :src="userProfile.avatar" />
            <q-icon v-else name="person" />
          </q-avatar>
          <q-card-actions>
            <q-btn flat @click="updatePhoto">Upload</q-btn>
          </q-card-actions>
        </q-item-section>
        <q-item-section>
          <ProfileDisplay
            v-if="!edit && userProfile.first_name"
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
    <q-dialog v-model="dialog">
      <!-- <q-avatar icon="" color="primary" text-color="white" /> -->
      <div class="text-center">
        <q-uploader
          label="Avatar Images Upload"
          batch
          :factory="upload"
          style="width:100%"
          persistent
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
      dialog: false,
      imgsupload: false
    };
  },
  computed: {
    userProfile: {
      get() {
        return this.$store.state.user;
      },
      set(data) {
        this.userProfile = data;
      }
    }
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
      if (this.userProfile["first_name"] !== "") {
        return;
      }
      this.$store.dispatch("user/updateUserDetail");
    },
    updateDetail(data) {
      console.log(data);
      this.userProfile.set(data);
    },
    updatePhoto() {
      this.$data.dialog = true;
    },
    async upload(file) {
      this.$data.imgsupload = true;
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
          this.userProfile.avatar = res;
          let data = { avatar: res };
          await this.$store
            .dispatch("user/updateProfile", data)
            .then(res => {
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
    },
    dismiss() {}
  }
};
</script>
