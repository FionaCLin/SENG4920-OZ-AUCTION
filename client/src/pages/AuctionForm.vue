<template>
  <q-page class="bg-grey-1">
    <div class="q-pa-md">
      <div class="row">
        <div class="col-2"></div>
        <div class="col-8">
          <h3>Basic Information</h3>
        </div>
        <div class="col-2"></div>
      </div>
      <div class="row">
        <div class="col-2"></div>
        <div class="col-8">
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
                  <q-input v-model="description" label="Description" filled type="text" />
                  <q-input v-model="price" label="Starting Price" filled type="number" />
                  <!-- <q-input
                    v-model="endTime"
                    label="End Time"
                    filled
                    type="date"
                  ></q-input> -->
                  <q-input filled v-model="date" label="Deadline" mask="date" :rules="['date']">
                    <template v-slot:append>
                      <q-icon name="event" class="cursor-pointer">
                        <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                          <q-date v-model="date" @input="() => $refs.qDateProxy.hide()" />
                        </q-popup-proxy>
                      </q-icon>
                    </template>
                  </q-input>
                </q-form>
                <q-select filled label="Category" v-model="categoryId" :options="options" />
              </q-item-section>
            </q-item>
            <q-card-actions>
              <q-btn color="primary" label="Submit" type="Submit" />
              <q-btn color="amber" glossy label="Reset" type="reset" />
              <q-btn color="deep-orange" glossy label="Cancel" type="cancel" @click="goBack"/>
            </q-card-actions>
          </q-card>
        </div>
        <div class="col-2"></div>
      </div>
    </div>
  </q-page>
</template>

<script>
// import { required, minLength } from 'vuelidate/lib/validators'

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
      options: ["Handicraft", "Second hand"],
      date: ""
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
      this.$data.data = "";
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
