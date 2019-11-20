<template>
  <div>
    <q-table
      :title="title"
      :data="data"
      :grid="grid"
      :columns="columns"
      row-key="name"
      :pagination.sync="pagination"
      lazy
    >
      <!-- table tool bar -->
      <template v-slot:top="props">
        <div v-if="title" class="col-2 q-table__title">{{ title }}</div>
        <q-btn v-if="tool" flat dense to="/create">
          <q-icon name="add" />Create Auction
        </q-btn>
        <q-toggle v-model="grid" :icon="grid ? 'grid_on' : 'list'" />

        <q-space />
        <q-input
          v-model="filter"
          borderless
          dense
          debounce="300"
          placeholder="Search"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>

      <!-- table grid view -->
      <template v-if="grid" v-slot:item="props">
        <cardView
          :props="props"
          @check-item="auctionItem"
          @check-profile="userProfile"
        />
      </template>

      <!-- table list view -->
      <template v-else v-slot:body="props">
        <listView
          :props="props"
          :fields="fields"
          @check-item="auctionItem"
          @check-profile="userProfile"
        />
      </template>
    </q-table>
  </div>
</template>

<script>
import cardView from "./CardView.vue";
import listView from "./ListView.vue";

export default {
  components: {
    cardView,
    listView
  },
  props: ["items", "title", "alink", "tool"],
  data() {
    return {
      grid: false,
      pagination: {},
      user: null,
      filter: "",
      fields: ["created", "end_time", "price", "location", "category"],
      columns: [
        {
          name: "image",
          required: true,
          label: "Images",
          field: "image",
          sortable: false
        },
        {
          name: "title",
          required: true,
          label: "Title",
          align: "left",
          field: "title",
          sortable: true
        },
        {
          name: "created",
          align: "center",
          label: "Created at",
          field: "created",
          sortable: true
        },
        {
          name: "end_time",
          align: "center",
          label: "End at",
          field: "end_time",
          sortable: true
        },
        {
          name: "price",
          label: "Price(Aud)",
          align: "center",
          field: "price",
          sortable: true,
          sort: (a, b) => parseInt(a, 10) - parseInt(b, 10)
        },
        {
          name: "location",
          required: true,
          label: "Location",
          align: "left",
          field: "location",
          sortable: true
        },
        {
          name: "category",
          required: true,
          label: "Category",
          align: "left",
          field: "category",
          sortable: true
        },
        {
          name: "seller_name",
          label: "Seller",
          field: "seller_name",
          align: "left",
          sortable: true,
          sort: (a, b) => parseInt(a, 10) - parseInt(b, 10)
        }
      ],
      data: this.items
    };
  },
  methods: {
    auctionItem: function(auction) {
      if (this.alink === "auctions" || this.$route.name === "myauctions") {
        this.$router
          .push({
            name: "auctionItem",
            params: {
              id: auction.id,
              item: auction
            }
          })
          .catch(err => console.log(err));
      } else {
        this.$router
          .push({
            name: "biddingItem",
            params: {
              id: auction.id,
              item: auction
            }
          })
          .catch(err => console.log(err));
      }
    },
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

<style>
.my-table-details {
  font-size: 0.85em;
  font-style: italic;
  max-width: 500px;
  white-space: normal;
  color: #555;
  margin-top: 4px;
}

.auction-item {
  width: 100%;
  position: relative;
}

.grid-style-transition :hover {
  transform: scale(0.95);
}
</style>
