<template>
  <q-page padding class="flex flex-center bg-grey-9">
    <q-card style="min-width: 800px">
      <q-card-section>
        <div class="text-h6">
          Already a user?
          <q-btn flat text-color="primary" to="/login" push>Log In</q-btn>To
          AuctionSystem! <q-separator />Sign Up
        </div>
      </q-card-section>
      <q-separator />
      <div class="q-pa-md">
        <q-form
          ref="SignUpForm"
          @submit="onSubmit"
          @reset="onReset"
          class="q-gutter-md"
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
            filled
            v-model="passwordConfirm"
            type="password"
            label="Confirm password"
            hint="Enter Login Password"
            :rules="[
              val => (val && val != password) || 'Password does not match'
            ]"
          ></q-input>
          <q-input
            filled
            type="number"
            v-model="age"
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
import { required, email } from "vuelidate/lib/validators";

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
  validations: {
    form: {
      name: {
        required
      },
      email: {
        required,
        email
      },
      password: {
        required
      }
    }
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
      this.name = null;
      this.age = null;
      this.accept = false;
    }
  }
};
</script>
