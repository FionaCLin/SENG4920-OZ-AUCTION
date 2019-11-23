<template>
  <q-dialog v-model="state" persistent>
    <q-card>
      <q-card-section class="row items-center">
        <q-avatar icon="delete" color="primary" text-color="white" />
        <span class="q-ml-sm">Are you sure to delete this auction?</span>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          v-close-popup
          flat
          label="Confirm"
          color="red"
          @click="$emit('confirm')"
        />
        <q-btn
          v-close-popup
          flat
          label="Cancel"
          color="green"
          @click="$emit('toggle')"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: "Confirmation",
  props: ["state"],
  data() {
    return {
      status: this.state
    };
  }
};
</script>
