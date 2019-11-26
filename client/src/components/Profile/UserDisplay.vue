<template>
  <div class="q-gutter-y-md col-auto q-mb-md">
    <q-field
      v-for="(val, index) in user"
      :key="index"
      filled
      :label="index"
      stack-label
    >
      <template>
        <div
          v-if="index !== 'Rating'"
          class="self-center full-width no-outline text-left"
          tabindex="0"
        >
          {{ val }}
        </div>
      </template>
    </q-field>
  </div>
</template>

<script>
export default {
  name: "UserDisplay",
  props: ["detail", "rating"],
  data() {
    return {
      edit: false
    };
  },
  computed: {
    user: {
      get() {
        if (this.detail) {
          let info = {
            "First Name": this.detail.first_name,
            "Last Name": this.detail.last_name,
            Email: this.detail.email,
            Phone: this.detail.phone_number,
            DOB: this.detail.dob,
            "Payment Method": this.detail.payment_method.join(", "),
            Location: this.detail.location
          };
          return info;
        } else {
          return this.$store.state.user;
        }
      }
    }
  }
};
</script>
