<template>
  <q-page class="bg-grey-1">
    <q-card
      class="col-xs-12 col-sm-11 col-md-10 col-lg-9"
      style="min-width: 300px;"
    >
      <q-item>
        <q-item-section avatar>
          <q-avatar class="self-center" size="100px" font-size="52px">
            <q-img v-if="images.length" src="" />
            <q-icon v-else name="image" />
          </q-avatar>
          <q-card-actions>
            <q-btn flat>Upload</q-btn>
            <q-btn flat>Remove</q-btn>
          </q-card-actions>
        </q-item-section>
        <q-item-section>
          <q-form
            :ref="edit ? 'EditAuctionForm' : 'CreateAuctionForm'"
            class="q-gutter-md"
            @submit="onSubmit"
            @reset="onReset"
          >
            <q-input v-model="title" label="Title" filled type="text" />
            <q-input
              v-model="description"
              label="Description"
              filled
              type="text"
            />
            <q-input v-model="price" label="Price" filled type="number" />
            <q-input
              v-model="endTime"
              label="End Time"
              filled
              type="date"
            ></q-input>
            <q-select
              v-model="categoryId"
              :options="options"
              label="Category"
            ></q-select>
          </q-form>
        </q-item-section>
      </q-item>
      <q-card-actions>
        <q-btn label="Submit" type="Submit" color="green" flat />
        <q-space />

        <q-btn label="Reset" type="reset" color="warning" flat />
        <q-space />

        <q-btn label="Cancel" type="cancel" color="red" flat @click="goBack" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script>
export default {
  name: "AuctionCreateForm",
  props: ["edit"],
  data() {
    return {
      categoryId: "",
      title: "",
      description: "",
      endTime: "",
      price: "",
      images: [],
      options: ["Handicraft", "Second hand"]
    };
  },
  created() {
    if (this.edit) {
      console.log("edit", this.edit);
      this.id = Number(this.$route.params.id);

      let auction = this.$store.state.auction.myAuctions.auction_items.find(
        x => x.id === this.id
      );
      console.log(auction);

      this.$data.categoryId = auction.category_id;
      this.$data.title = auction.title;
      this.$data.description = auction.description;
      this.$data.endTime = auction.end_time;
      this.$data.price = auction.price;
      // this.$data.images = auction.images;
    }
  },
  methods: {
    onSubmit() {
      // sellerName: "",
      // sellerId: "",
      if (this.edit) {
        this.$emit("editDetail", this.$data);
        return;
      }
      this.$refs.CreateAuctionForm.validate().then(
        success => {
          if (success) {
            // yay, models are correct
            this.$emit("editDetail", this.$data);
            this.$emit("updateEdit", false);
          }
        },
        err => {
          console.log(err);

          // oh no, user has filled in
          // at least an invalid value
          // this.$q.notify({
          //   color: 'red-5',
          //   textColor: 'white',
          //   icon: 'warning',
          //   message: err.message
          // })
        }
      );
    },

    onReset() {
      this.$data.sellerId = "";
      this.$data.categoryId = "";
      this.$data.title = "";
      this.$data.description = "";
      this.$data.endTime = "";
      this.$data.price = 0;
      this.$data.images = "";
    },
    goBack() {
      if (this.edit) {
        this.$router.push({
          name: "auctiionItem",
          params: {
            id: this.id
          }
        });
      } else {
        this.$router.push({
          path: "/auctions"
        });
      }
    }
  }
};
</script>
