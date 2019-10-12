<template>
  <div class="q-gutter-y-md col-auto q-ma-md">
    <q-field
      v-for="(val, index) in user"
      :key="index"
      filled
      :label="index"
      stack-label
    >
      <template v-if="index !== 'Avatar'">
        <div
          v-if="index == 'Seller'"
          class="self-center full-width no-outline text-left"
          tabindex="0"
        >
          <q-toggle v-model="user.Seller" />
        </div>
        <div
          v-else-if="index === 'Password'"
          class="self-center full-width no-outline text-left"
          tabindex="0"
        >
          {{ val | formatPwd }}
        </div>
        <div
          v-else
          class="self-center full-width no-outline text-left"
          tabindex="0"
        >
          {{ val }}
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

      <q-btn label="Cancel" type="cancel" color="red" flat />
    </q-card-actions>
  </div>
</template>

<script>
export default {
  name: "ProfileDisplay",
  filters: {
    formatPwd(val) {
      return val.replace(/./g, "*");
    }
  },
  props: ["detail", "avatarurl"],
  data() {
    return {
      edit: false,
      user: this.detail,
      avatar: this.avatarurl
    };
  }
};
</script>
