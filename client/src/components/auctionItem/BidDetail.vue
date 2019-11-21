<template>
  <div>
    <q-table
      :data="biddings_info"
      row-key="name"
      :columns="columns"
      :pagination.sync="pagination"
      virtual-scroll
      lazy
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="user">
            <div @click="userProfile(props.row.buyer)">
              <q-avatar size="68px" font-size="32px">
                <img :src="props.row.buyer.avatar" />
              </q-avatar>
            </div>
          </q-td>
          <q-td>
            <div @click="userProfile(props.row.buyer)">
              <span class="text-weight-bold">{{
                props.row.buyer.first_name + props.row.buyer.last_name
              }}</span>
              <div caption>{{ props.row.buyer.location }}</div>
              <div caption>
                <q-icon
                  v-for="n in props.row.buyer.rating"
                  :key="n"
                  name="star"
                ></q-icon>
              </div>
            </div>
          </q-td>
          <q-td>
            <div class="text-h6">
              {{ props.row.proposal_price | currency }}
            </div>
            <div class="text-subtitle1">{{ props.row.created }}</div>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>
<script>
export default {
  name: "BidItem",
  filters: {
    currency: function(value) {
      return "$" + Number.parseFloat(value).toFixed(2);
    }
  },
  props: ["biddings"],
  data() {
    return {
      pagination: {},
      columns: [
        {
          name: "price",
          required: true,
          label: "",
          field: "proposal_price",
          sortable: true
        },
        {
          name: "user",
          required: true,
          label: "",
          field: "user",
          sortable: false
        }
      ],
      biddings_info: this.biddings
    };
  },
  created() {
    console.log(this.biddings);
  },
  methods: {
    userProfile: function(user) {
      this.$router
        .push({
          name: "userProfile",
          params: {
            id: user.user_id,
            user: user
          }
        })
        .catch(err => console.log(err));
    }
  }
};
</script>
