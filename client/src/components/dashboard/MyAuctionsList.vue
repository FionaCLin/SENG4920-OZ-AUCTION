<template>
  <div>
    <a :name="alink"></a>
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
        <!-- <q-btn v-if="tool" flat dense to="/create">
          <q-icon name="add" />Create Auction
        </q-btn>-->
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
      <!-- table list view -->
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
          <q-td key="seller_name" auto-width :props="props">
            <div>
              <q-item
                v-ripple
                clickable
                @click="userProfile(props.row.seller_id)"
              >
                <q-item-section avatar>
                  <q-avatar>
                    <img :src="user_avatar(props.row.seller_id)" />
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ props.row.seller_name }}</q-item-label>
                  <q-item-label caption>
                    <q-icon
                      v-for="n in user_rating(props.row.seller_id)"
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
      <!-- table grid view -->
      <template v-slot:item="props">
        <div
          class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
        >
          <q-card>
            <q-img
              class="auction-item"
              :src="props.cols.find(col => col.name === 'image').value"
              @click="auctionItem(props.row.id)"
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
                  @click="auctionItem(props.row.id)"
                >
                  <q-item-label v-if="col.name !== 'seller_name'" caption>{{
                    col.value
                  }}</q-item-label>
                  <q-item
                    v-else
                    v-ripple
                    clickable
                    @click="userProfile(props.row.seller_id)"
                  >
                    <q-item-section avatar>
                      <q-avatar>
                        <img :src="user_avatar(props.row.seller_id)" />
                      </q-avatar>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>{{ props.row.seller_name }}</q-item-label>
                      <q-item-label caption>
                        <q-icon
                          v-for="n in user_rating(props.row.seller_id)"
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
    </q-table>
  </div>
</template>
<script>
export default {
  props: ["items", "title", "alink", "tool"],
  data() {
    return {
      grid: false,
      pagination: {},
      filter: "",
      fields: ["created", "price", "location"],
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
          name: "location",
          required: true,
          label: "Location",
          align: "left",
          field: "location",
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
    getUser(id) {
      let auctions = this.$store.state.auction.auctions.find(
        x => x.sellers.seller_id === id
      );
      let user = auctions.sellers;
      user.name = auctions.auction_items[0].seller_name;
      return user;
    },
    user_avatar(id) {
      let user = this.getUser(id);
      return user.avatar;
    },
    user_rating(id) {
      let user = this.getUser(id);
      return user.rating;
    },
    auctionItem: function(id) {
      console.log("from", id);
      console.log("to", this.$route.params.id, this.$route.name);

      if (this.title === "My Auctions" || this.$route.name === "myAuctions") {
        this.$router.push({
          name: "auctiionItem",
          params: {
            id: id
          }
        });
      } else {
        this.$router.push({
          name: "biddingItem",
          params: {
            id: id
          }
        });
      }
    },
    userProfile: function(id) {
      this.$router.push({
        name: "userProfile",
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
