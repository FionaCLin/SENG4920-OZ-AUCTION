<template>
  <div
    class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
  >
    <q-card>
      <!-- item image -->
      <q-img
        class="auction-item"
        :src="props.row.image[0]"
        @click="goto(props.row)"
      >
        <div class="text-subtitle2 absolute-bottom text-center">
          {{ props.row.title }}
        </div>
      </q-img>

      <!-- item detail -->
      <q-list dense>
        <q-item
          v-for="col in props.cols.filter(
            col => col.name !== 'image' && col.name !== 'title'
          )"
          :key="col.name"
        >
          <q-item-section>
            <q-item-label>{{ col.label }}</q-item-label>
          </q-item-section>
          <q-item-section v-ripple side clickable @click="goto(props.row)">
            <q-item-label v-if="col.name !== 'seller_name'" caption>{{
              col.value
            }}</q-item-label>
            <q-item
              v-else
              v-ripple
              clickable
              @click="goProfile(props.row.user)"
            >
              <q-item-section avatar>
                <q-avatar>
                  <img :src="props.row.user.avatar" />
                </q-avatar>
              </q-item-section>
              <q-item-section>
                <q-item-label>{{ props.row.seller_name }}</q-item-label>
                <q-item-label caption>
                  <q-icon
                    v-for="n in props.row.user.rating"
                    :key="n"
                    name="star"
                  ></q-icon>
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-item-section>
        </q-item>
      </q-list>
    </q-card>
  </div>
</template>
<script>
export default {
  name: "AuctionListGridView",
  props: ["props"],
  methods: {
    goto(row) {
      console.log(row);

      this.$emit("check-item", row);
    },
    goProfile(row) {
      this.$emit("check-profile", row);
    }
  }
};
</script>
