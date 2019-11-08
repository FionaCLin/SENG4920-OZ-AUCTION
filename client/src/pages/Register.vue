<template>
  <q-page padding class="myPage">
    <div class="row myFlex justify-evenly">
      <q-card
        class="col-xs-12 col-sm-10 col-md-8 col-lg-6"
        style="min-width: 320px;"
      >
        <q-card-section>
          <div class="text-h6">
            Sign Up
          </div>

        </q-card-section>
        <q-separator />
        <div class="q-pa-md" style="margin:10px 20px;">
          <q-form
            ref="SignUpForm"
            class="q-gutter-md"
            @submit="onSubmit"
          >
            <q-input
              v-model="name"
              filled
              label="Your full name"
              lazy-rules
              :rules="[
                val => (val && val.length > 0) || 'Please type your full name'
              ]"
            />
            <q-input
              v-model="email"
              filled
              label="Your email"
              type="email"
              lazy-rules
              :rules="[
                val => (val && val.length > 5 && value.includes('@')) || 'Please enter valid Email'
              ]"
            />
            <q-input
              v-model="password"
              filled
              :type="isPwd ? 'password' : 'text'"
              label="Login password"
              :rules="[
                val => (val && /^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+)$/.test(val)
                        && val.length > 8)
                        || 'Password must have at least one digit and one character and length of more than 8'
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

            <q-input
              v-model="passwordConfirm"
              filled
              type="password"
              label="Confirm password"
              :rules="[
                val => (val && val == password) || 'Password not matching'
              ]"
            ></q-input>

            <div class="text-h9" style="overflow:hidden">
              Already a user?
              <q-btn flat text-color="primary" to="/login" style="padding:0px" push>Log In</q-btn> here.
              <q-btn class="myButton" label="Register" type="submit" color="primary" />
            </div>

          </q-form>
        </div>
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
      passwordConfirm: null,
      register: "register"
    };
  },
  methods: {
    onSubmit() {
      this.$refs.SignUpForm.validate().then(
        success => {
          if (success) {
            // yay, models are correct
            console.log(success);
            axiosInstance
              .post("/account/register", {
                username: this.$data.email,
                password: this.$data.password
              })
              .then(response => {
                console.log(response);
                this.$q.notify({
                  color: "green-4",
                  textColor: "white",
                  icon: "cloud_done",
                  message: response.data.message
                });
                this.$router.push("/login");
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
      this.age = null;
      this.name = null;
      this.isPwd = true;
      this.seller = false;
      this.email = null;
      this.password = null;
      this.passwordConfirm = null;
    }
  }
};
</script>

<style scoped>
  .myPage {
    background-image: url("../statics/register.jpg");
    background-repeat: no-repeat;
    background-size: 100%;
  }
  .myFlex{
    margin-top: 5%;
    margin-bottom: 5%;
  }
  .myButton{
    /* position: relative; */
    float: right;
  }
</style>
