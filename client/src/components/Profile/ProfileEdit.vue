<template>
  <div class="q-gutter-y-md col-auto q-ma-md">
    <q-form
      ref="ProfileForm"
      class="q-gutter-md"
      @submit.once="onSubmit"
      @reset="onReset"
    >
      <q-input
        v-model="first_name"
        filled
        label="First name *"
        lazy-rules
        :rules="[
          val => (val && val.length > 0) || 'Please type your full name'
        ]"
      />
      <q-input
        v-model="last_name"
        filled
        label="Last name *"
        lazy-rules
        :rules="[
          val => (val && val.length > 0) || 'Please type your full name'
        ]"
      />
      <q-input
        v-model="email"
        filled
        label="Your email *"
        lazy-rules
        :rules="[val => (val && val.length > 0) || 'Please enter valid Email']"
      />
      <q-input
        v-model="phone_number"
        filled
        label="Your phone *"
        lazy-rules
        :rules="[val => (val && val.length > 0) || 'Please enter valid Phone']"
      />
      <q-select
        v-model="location"
        filled
        label="Location"
        use-input
        :options="optionsLocation"
        @filter="filterLocFn"
      />
      <TimeInput
        v-model="dob"
        :date="dob"
        :label="`Your DOB *`"
        @update-time="dob = $event"
      />

      <q-field filled label="Payment Method" stack-label>
        <strong>{{ payment_method | formatPaymentMethod }}</strong>
      </q-field>
      <div class="q-pa-md">
        <div class="q-px-sm"></div>
        <div class="q-gutter-sm">
          <q-checkbox
            v-for="(k, m) in methods"
            :key="m"
            v-model="payment_method"
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
import moment from "moment";
import { countries, warning } from "../../helper";
import TimeInput from "../../components/auctionItem/TimeInput";

export default {
  name: "ProfileEdit",
  components: { TimeInput },
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
      first_name: this.detail.first_name,
      last_name: this.detail.last_name,
      email: this.detail.email,
      dob: this.detail.dob
        ? moment(this.detail.dob, "YYYY-MM-DD h:mm:ss")
        : null,
      location: this.detail.location,
      phone_number: this.detail.phone_number,
      payment_method: this.detail.payment_method,
      methods: ["Visa", "Master", "WeChat", "PayPal", "AliPay"],
      optionsLocation: countries.map(x => x.name)
    };
  },
  methods: {
    onSubmit() {
      this.$refs.ProfileForm.validate().then(
        success => {
          if (success) {
            // yay, models are correct
            let data = {};
            for (let k of Object.keys(this.detail)) {
              if (k == "dob" && this.$data[k]) {
                let oldVal = moment(this.detail[k], "YYYY-MM-DD h:mm:ss");
                let newVal = moment(this.$data[k], "YYYY-MM-DD h:mm:ss");
                if (!oldVal.isSame(newVal)) {
                  data[k] = newVal;
                }
              } else if (
                k !== "dob" &&
                this.$data[k] &&
                this.detail[k] !== this.$data[k]
              ) {
                data[k] = this.$data[k];
              }
            }
            this.$store
              .dispatch("user/updateProfile", data)
              .then(res => {
                console.log(res);
                this.$emit("updateEdit", false);
                this.$emit("editDetail", data);
              })
              .catch(err => {
                warning.message = err.data.message;
                this.$q.notify(warning);
              });
          }
        },
        err => {
          warning.message = err.data.message;
          this.$q.notify(warning);
        }
      );
    },
    filterLocFn(val, update) {
      if (val === "") {
        update(() => {
          this.$data.optionsLocation = countries.map(x => x.name);
        });
        return;
      }

      update(() => {
        const needle = val.toLowerCase();
        this.$data.optionsLocation = countries
          .map(x => x.name)
          .filter(v => v.toLowerCase().indexOf(needle) > -1);
      });
    },
    onReset() {
      this.$data.first_name = this.detail.first_name;
      this.$data.last_name = this.detail.last_name;
      this.$data.email = this.detail.email;
      this.$data.location = this.detail.location;
      this.$data.phone_number = this.detail.phone_number;
      this.$data.dob = moment(this.detail.dob, "YYYY-MM-DD h:mm:ss").format(
        "YYYY-MM-DD"
      );
      this.$data.payment_method = this.detail.payment_method;
    }
  }
};
</script>
