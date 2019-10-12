<template>
  <div class="q-gutter-y-md col-auto q-ma-md">
    <q-form
      ref="ProfileForm"
      class="q-gutter-md"
      @submit="onSubmit"
      @reset="onReset"
    >
      <q-input
        v-model="fName"
        filled
        label="First name *"
        hint="First Name"
        lazy-rules
        :rules="[
          val => (val && val.length > 0) || 'Please type your full name'
        ]"
      />
      <q-input
        v-model="lName"
        filled
        label="Last name *"
        hint="Last Name"
        lazy-rules
        :value="lName"
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
        :rules="[val => (val && val.length > 0) || 'Please enter valid Email']"
      />

      <!-- <q-input
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
        :rules="[val => (val && val != password) || 'Password does not match']"
      ></q-input> -->

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

      <q-card-actions>
        <q-btn label="Submit" type="Submit" color="green" flat />
        <q-space />

        <q-btn v-if="edit" label="Reset" type="reset" color="warning" flat />
        <q-space v-if="edit" />

        <q-btn
          label="Cancel"
          type="cancel"
          color="red"
          flat
          @click="$emit('updateEdit', !edit)"
        />
      </q-card-actions>
    </q-form>
  </div>
</template>

<script>
export default {
  name: "ProfileEdit",
  filters: {
    formatPwd(val) {
      return val.replace(/./g, "*");
    }
  },
  props: ["detail", "avatarurl"],
  data() {
    return {
      edit: true,
      avatar: this.avatarurl,
      fName: this.detail["First Name"],
      lName: this.detail["Last Name"],
      email: this.detail["E-mail"],
      age: this.detail.Age,
      password: this.detail.password,
      seller: this.detail.Seller
    };
  },

  methods: {
    onSubmit() {
      this.$refs.ProfileForm.validate().then(
        success => {
          if (success) {
            // yay, models are correct
            console.log(success);
            console.log("updateEdit", this.$data);
            this.$emit("updateEdit", false);
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
      this.fName = this.detail["First Name"];
      this.lName = this.detail["Last Name"];
      this.$data.email = this.detail["E-mail"];
      this.$data.age = this.detail.Age;
      this.$data.password = this.detail.Password;
      this.$data.seller = this.detail.Seller;
    }
  }
};
</script>
