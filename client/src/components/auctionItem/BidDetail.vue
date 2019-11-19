<template>
  <div>
    <q-table
      :data="biddings_info"
      row-key="name"
      :columns="columns"
      :loading="loading"
      :pagination.sync="pagination"
      virtual-scroll
      lazy
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="user">
            <q-avatar size="68px" font-size="32px">
              <img :src="props.row.user.avatar" />
            </q-avatar>
          </q-td>
          <q-td>
            <span class="text-weight-bold">{{
              props.row.user.first_name + props.row.user.last_name
            }}</span>
            <div caption>{{ props.row.user.location }}</div>
            <div caption>
              <q-icon
                v-for="n in props.row.user.rating"
                :key="n"
                name="star"
              ></q-icon>
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
// import { mapGetters } from "vuex";
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
      loading: true,
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
      biddings_info: []
    };
  },
  created() {
    this.getUsers(this.biddings);
  },
  methods: {
    getUser(bid) {
      return this.$axios
        .get(`/account/manage_profile/${bid.user_id}`)
        .then(res => {
          bid.user = res.data.data;
          return bid;
        });
    },
    getUsers(biddings) {
      let promises = biddings.map(x => this.getUser(x));
      Promise.all(promises).then(results => {
        this.$data.biddings_info = results
          .sort((a, b) => a.proposal_price - b.proposal_price)
          .reverse();
        this.$data.loading = false;
      });
    }
  }
};
</script>
