<template>
  <q-input
    v-model="time"
    filled
    :label="label"
    :rules="
      rule ? [val => validateDate() || 'Deadline must be later than today'] : []
    "
    @input="hello"
  >
    <template v-slot:append>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy transition-show="scale" transition-hide="scale">
          <q-date v-model="time" mask="YYYY-MM-DD" @click="hello" />
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>
<script>
import moment from "moment";

export default {
  name: "TimeInput",
  props: ["date", "label", "rule"],
  data() {
    return {
      time: this.date ? moment(this.date).format("YYYY-MM-DD") : null,
      warning: "hello"
    };
  },
  methods: {
    hello() {
      this.$emit("update-time", this.$data.time);
    },
    validateDate() {
      if (this.label == "Dealine") {
        let input = moment(this.$data.time, "YYYY-MM-DD");
        return input.isAfter(moment());
      }
    }
  }
};
</script>
