<template>
  <q-page padding class="myPage">
    <div class="row myFlex" style="justify-content:flex-start">
      <q-card class="col-4" style="min-width: 200px;">
        <q-card-section>
          <div class="text-h6">Login</div>
        </q-card-section>
        <q-separator />
        <q-separator />
        <q-card-section>
          <q-form ref="LoginForm" class="q-gutter-md" @submit="onSubmit">
            <q-input
              v-model="email"
              filled
              type="email"
              label="Your email"
              hint="Email"
              lazy-rules
              :rules="[
                val =>
                  (val && val.length > 5 && value.includes('@')) ||
                  'Please enter valid Email'
              ]"
            ></q-input>
            <q-input
              v-model="password"
              filled
              :type="isPwd ? 'password' : 'text'"
              label="Login password"
              hint="Password with toggle"
              :rules="[
                val =>
                  (val && val.length > 8) ||
                  'Password must be at least 8 characters'
              ]"
            >
              <template v-slot:append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>

            <div style="overflow:hidden">
              New user?
              <q-btn flat text-color="primary" to="/register" push class="myRe"
                >Register</q-btn
              >here.
              <q-btn
                label="Login"
                type="submit"
                color="primary"
                style="float:right;"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { axiosInstance } from "boot/axios";

export default {
  data() {
    return {
      name: null,
      age: null,
      isPwd: true,
      seller: false,
      email: null,
      password: null,
      tab: "login"
    };
  },
  methods: {
    onSubmit() {
      this.$refs.LoginForm.validate().then(
        success => {
          if (success) {
            // yay, models are correct
            console.log(success);
            axiosInstance
              .post("/account/signin", {
                username: this.$data.email,
                password: this.$data.password
              })
              .then(response => {
                console.log(response);
                this.$q.notify({
                  color: "green-4",
                  textColor: "white",
                  position: "top",
                  icon: "cloud_done",
                  message: response.data.message
                });
                setTimeout(() => {
                  this.$router.push("/dashboard");
                }, 1000);
              })
              .catch(error => {
                console.log(error.response);

                this.$q.notify({
                  color: "red-4",
                  textColor: "white",
                  icon: "cloud_done",
                  message: error.response.data.message
                });
              });
          }
        },
        err => {
          console.log(err);
          console.log("problems~~~~!");

          // oh no, user has filled in
          // at least an invalid value
          this.$q.notify({
            color: "red-5",
            textColor: "white",
            icon: "warning",
            // message: "Incorrect username and password"
            message: err.message
          });
          // oh no, user has filled in
          // at least an invalid value
          // this.$q.notify({
          //   color: 'red-5',
          //   textColor: 'white',
          //   icon: 'warning',
          //   message: err.message
          // })
        }
      );
    },

    onReset() {
      this.name = null;
      this.age = null;
      this.accept = false;
    }
  }
};
</script>

<style scoped>
.myRe {
  padding: 0px 0px;
}
.myPage {
  background-image: url("../statics/login_background.jpg");
  background-repeat: no-repeat;
  background-size: 100%;
}
.myFlex {
  margin: 10% 5%;
}
</style>
