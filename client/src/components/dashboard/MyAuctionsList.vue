<template>
  <div class="q-pa-md">
    <q-table
      title="My Auctions"
      :data="data"
      :grid="grid"
      :columns="columns"
      row-key="name"
      :pagination.sync="pagination"
      lazy
    >
      <template v-slot:top="props">
        <div class="col-2 q-table__title">My Auctions</div>
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
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="image" auto-width :props="props">
            <q-img :src="props.row.image" @click="auctionItem(props.row.id)" />
          </q-td>
          <q-td key="title" auto-width :props="props">
            <div>
              <q-badge
                color="green-4"
                class="text-bold text-white"
                :label="props.row.title"
                @click="auctionItem(props.row.id)"
              />
            </div>
            <div class="my-table-details" @click="auctionItem(props.row.id)">
              {{ props.row.description }}
            </div>
          </q-td>

          <q-td v-for="f in fields" :key="f" auto-width :props="props">
            <p @click="auctionItem(props.row.id)">{{ props.row[f] }}</p>
          </q-td>
        </q-tr>
      </template>

      <template v-slot:item="props">
        <div
          class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
        >
          <q-card @click="auctionItem(props.row.id)">
            <q-img
              class="auction-item"
              :src="props.cols.find(col => col.name === 'image').value"
            >
              <div class="text-subtitle2 absolute-bottom text-center">
                {{ props.row.title }}
              </div>
            </q-img>
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
                <q-item-section side>
                  <q-item-label caption>{{ col.value }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card>
        </div>
      </template>
    </q-table>
  </div>
</template>
<script>
export default {
  props: ["items"],
  data() {
    return {
      grid: false,
      pagination: {},
      filter: "",
      fields: ["created", "price", "seller_name", "location"],
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
        // {
        //   name: "description",
        //   align: "center",
        //   label: "Description",
        //   field: "description",
        //   sortable: true
        // },
        {
          name: "created",
          align: "center",
          label: "Created at",
          field: "created",
          // format: v => date(v, ""),
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
          name: "seller_name",
          label: "Seller",
          field: "seller_name",
          align: "left",
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
        }
      ],
      data: this.items
    };
  },
  methods: {
    auctionItem: function(id) {
      console.log("from", id);
      this.$router.push({
        name: "auctiionItem",
        params: {
          id: id
        }
      });
    }
  }
};
</script>

<style>
.my-table-details {
  font-size: 0.85em;
  font-style: italic;
  max-width: 200px;
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
