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
        <div
          class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
        >
          <q-card>
            <q-img
              class="auction-item"
              :src="props.cols.find(col => col.name === 'image')[0].value"
              @click="auctionItem(props.row)"
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
                <q-item-section
                  v-ripple
                  side
                  clickable
                  @click="auctionItem(props.row)"
                >
                  <q-item-label v-if="col.name !== 'seller_name'" caption
                    >{{ col.value }}
                  </q-item-label>
                  <q-item
                    v-else
                    v-ripple
                    clickable
                    @click="userProfile(props.row.user)"
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

      <!-- table list view -->
      <template v-else v-slot:body="props">
        <q-tr :props="props">
          <q-td key="image" auto-width :props="props">
            <q-img :src="props.row.image[0]" @click="auctionItem(props.row)" />
          </q-td>
          <q-td key="title" auto-width :props="props">
            <div>
              <q-badge
                color="green-4"
                class="text-bold text-white"
                :label="props.row.title"
                @click="auctionItem(props.row)"
              />
            </div>
            <div class="my-table-details" @click="auctionItem(props.row)">
              {{ props.row.description }}
            </div>
          </q-td>

          <q-td v-for="f in fields" :key="f" auto-width :props="props">
            <p @click="auctionItem(props.row)">{{ props.row[f] }}</p>
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
    </q-table>
  </div>
</template>

<script>
// import { axiosInstance } from "boot/axios";

export default {
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
