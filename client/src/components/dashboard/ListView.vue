<template>
  <q-tr :props="props">
    <q-td key="image" auto-width :props="props">
      <q-img :src="props.row.image[0]" @click="goto(props.row)" />
    </q-td>
    <q-td key="title" auto-width :props="props">
      <div>
        <q-badge
          color="green-4"
          class="text-bold text-white"
          :label="props.row.title"
          @click="goto(props.row)"
        />
      </div>
      <div class="my-table-details" @click="goto(props.row)">
        {{ props.row.description }}
      </div>
    </q-td>

    <q-td v-for="f in fields" :key="f" auto-width :props="props">
      <p @click="goto(props.row)">{{ props.row[f] }}</p>
    </q-td>
    <q-td key="seller_name" auto-width :props="props">
      <div>
        <q-item v-ripple clickable @click="userProfile(props.row.user)">
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
      </div>
    </q-td>
  </q-tr>
</template>
<script>
export default {
  name: "AuctionListView",
  props: ["props", "fields"],
  methods: {
    goto(row) {
      console.log(row);

      this.$emit("check-item", row);
    },
    userProfile(row) {
      this.$emit("check-profile", row);
    }
  }
};
</script>
