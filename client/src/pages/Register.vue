<template>
  <q-page padding class="row justify-evenly q-gutter-xs bg-grey-1">
    <q-card
      class="col-xs-12 col-sm-10 col-md-8 col-lg-6"
      style="min-width: 320px;"
    >
      <q-card-section>
        <div class="text-h6">
          Sign Up
        </div>
        <q-separator />
        <div class="text-h9">
          Already a user?
          <q-btn flat text-color="primary" to="/login" push>Log In</q-btn>To
          AuctionSystem!
        </div>
      </q-card-section>
      <q-separator />
      <div class="q-pa-md">
        <q-form
          ref="SignUpForm"
          class="q-gutter-md"
          @submit="onSubmit"
          @reset="onReset"
        >
          <q-input
            v-model="name"
            filled
            label="Your name *"
            hint="Name and surname"
            lazy-rules
            :rules="[
              val => (val && val.length > 0) || 'Please type your full name'
            ]"
          />
          <q-input
            v-model="email"
            filled
            label="Your email *"
            hint="Email"
            lazy-rules
            :rules="[
              val => (val && val.length > 0) || 'Please enter valid Email'
            ]"
          />
          <q-input
            v-model="password"
            filled
            :type="isPwd ? 'password' : 'text'"
            label="Login password"
            hint="Password with toggle"
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
            hint="Enter Login Password"
            :rules="[
              val => (val && val != password) || 'Password does not match'
            ]"
          ></q-input>
          <q-input
            v-model="age"
            filled
            type="number"
            label="Your age *"
            lazy-rules
            :rules="[
              val => (val !== null && val !== '') || 'Please type your age',
              val => (val > 0 && val < 100) || 'Please type a real age'
            ]"
          />

          <q-toggle v-model="seller" label="Seller" />

          <div>
            <q-btn label="Submit" type="submit" color="primary" />
            <q-btn
              label="Reset"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
            />
          </div>
        </q-form>
      </div>
    </q-card>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      name: null,
      age: null,
      isPwd: true,
      seller: false,
      email: null,
      password: null,
      passwordConfirm: null
    };
  },
  methods: {
    onSubmit() {
      this.$refs.SignUpForm.validate().then(
        success => {
          if (success) {
            // yay, models are correct
            console.log(success);
            // this.$q.notify({
            //   color: 'green-4',
            //   textColor: 'white',
            //   icon: 'cloud_done',
            //   message: 'Submitted'
            // })
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
