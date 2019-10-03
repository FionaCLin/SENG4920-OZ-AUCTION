<template>
  <q-page padding class="flex flex-center bg-grey-9">
    <q-card style="min-width: 800px">
      <q-card-section>
        <div class="text-h6">Login</div>
      </q-card-section>
      <q-separator />
      <q-card-section class="q-pa-md">
        <q-form
          ref="LoginForm"
          class="q-gutter-md"
          @submit="onSubmit"
          @reset="onReset"
        >
          <q-input
            v-model="email"
            filled
            type="email"
            label="Your email *"
            hint="Email"
            lazy-rules
            :rules="[
              val => (val && val.length > 10) || 'Please enter valid Email'
            ]"
          ></q-input>
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
      </q-card-section>
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
      password: null
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
      this.$refs.LoginForm.validate().then(
        success => {
          if (success) {
            // yay, models are correct
            this.$q.notify({
              color: "green-4",
              textColor: "white",
              icon: "cloud_done",
              message: "Submitted"
            });
          }
        },
        err => {
          // oh no, user has filled in
          // at least an invalid value
          this.$q.notify({
            color: "red-5",
            textColor: "white",
            icon: "warning",
            message: err.message
          });
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
