<template>
  <div class="q-gutter-y-md col-auto q-ma-md">
    <q-form
      ref="ProfileForm"
      class="q-gutter-md"
      @submit="onSubmit"
      @reset="onReset"
    >
      <q-input
        v-model="firstName"
        filled
        label="First name *"
        hint="First Name"
        lazy-rules
        :rules="[
          val => (val && val.length > 0) || 'Please type your full name'
        ]"
      />
      <q-input
        v-model="lastName"
        filled
        label="Last name *"
        hint="Last Name"
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
        :rules="[val => (val && val.length > 0) || 'Please enter valid Email']"
      />

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

      <q-field filled label="Payment Method" stack-label>
        <strong>{{ paymentMethod | formatPaymentMethod }}</strong>
      </q-field>
      <div class="q-pa-md">
        <div class="q-px-sm"></div>
        <div class="q-gutter-sm">
          <q-checkbox
            v-for="(k, m) in methods"
            :key="m"
            v-model="paymentMethod"
            :val="k"
            :label="k"
            color="teal"
          />
        </div>
      </div>

      <!-- <q-toggle v-model="seller" filled label="Seller" left-label /> -->

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
    formatPaymentMethod(val) {
      if (val && Array.isArray(val)) return val.join(", ");
      else return "";
    }
  },
  props: ["detail"],
  data() {
    return {
      edit: true,
      firstName: this.detail.firstName,
      lastName: this.detail.lastName,
      email: this.detail.email,
      age: this.detail.age,
      paymentMethod: this.detail.payment_method,
      methods: ["Visa", "Master", "WeChat", "PayPal", "AliPay"]
    };
  },

  methods: {
    onSubmit() {
      this.$refs.ProfileForm.validate().then(
        success => {
          if (success) {
            // yay, models are correct
            this.$emit("editDetail", this.$data);

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
      this.$data.firstName = this.detail.firstName;
      this.$data.lastName = this.detail.lastName;
      this.$data.email = this.detail.email;
      this.$data.age = this.detail.age;
      this.$data.password = this.detail.password;
      this.$data.seller = this.detail.seller;
    }
  }
};
</script>
