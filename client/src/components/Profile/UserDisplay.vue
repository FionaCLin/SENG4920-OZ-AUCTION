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
  name: "ProfileDisplay",
  props: ["detail", "rating"],
  data() {
    return {
      edit: false,
      user: {
        // "First Name": this.detail.firstName,
        // "Last Name": this.detail.lastName,
        // Email: this.detail.email,
        // Age: this.detail.age,
        // Password: this.detail.password,
        Name: this.detail.name,
        Location: this.detail.location,
        "Payment Method": this.detail.paymentMethod.join(", ")
        // Seller: this.detail.seller
      }
    };
  }
};
</script>
