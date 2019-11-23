<template>
  <div class="q-gutter-y-md col-auto q-ma-md">
    <q-field
      v-for="index in keys"
      :key="index"
      filled
      :label="index"
      stack-label
    >
      <template>
        <div class="self-center full-width no-outline text-left" tabindex="0">
          {{ user[index] }}
        </div>
      </template>
    </q-field>
    <q-card-actions>
      <q-btn
        label="Update"
        type="Update"
        color="green"
        flat
        @click="$emit('updateEdit', !edit)"
      />
      <q-space />

      <q-btn label="Cancel" type="cancel" color="red" flat to="/dashboard" />
    </q-card-actions>
  </div>
</template>

<script>
import moment from "moment";
export default {
  name: "ProfileDisplay",
  props: ["detail"],
  data() {
    return {
      edit: false,
      keys: [
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Location",
        "DOB",
        "Payment Method"
      ],
      user: {
        "First Name": this.detail.first_name,
        "Last Name": this.detail.last_name,
        Email: this.detail.email,
        Phone: this.detail.phone_number,
        Location: this.detail.location,
        DOB: moment(this.detail.dob, "YYYY-MM-DD h:mm:ss").format("YYYY-MM-DD"),
        "Payment Method": this.detail.payment_method
          ? this.detail.payment_method.join(", ")
          : ""
      }
    };
  }
};
</script>
