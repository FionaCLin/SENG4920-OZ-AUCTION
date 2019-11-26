<template>
  <q-input v-model="time" filled :label="label" @input="hello">
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
  props: ["date", "label"],
  data() {
    return {
      time: this.date ? moment(this.date).format("YYYY-MM-DD") : null
    };
  },
  methods: {
    hello() {
      console.log(this.$data.time);
      this.$emit("update-time", this.$data.time);
    }
  }
};
</script>
