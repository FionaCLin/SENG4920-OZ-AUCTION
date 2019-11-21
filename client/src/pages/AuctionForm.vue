<template>
  <div class="q-pa-md">
    <q-stepper ref="stepper" v-model="step" color="primary" animated>
      <q-step
        :name="1"
        title="Basic Information"
        icon="settings"
        :done="step > 1"
      >
        <q-item class="myItem">
          <q-item-section>
            <q-form
              :ref="edit ? 'EditAuctionForm' : 'CreateAuctionForm'"
              class="q-gutter-md"
              @submit="onSubmit"
            >
              <q-input
                v-model="title"
                label="Product title"
                filled
                type="text"
                lazy-rules
                :rules="[
                  val => (val && val.length > 5) || 'Please enter valid title'
                ]"
              />
              <q-input
                v-model="price"
                label="Starting Price"
                prefix="$AD"
                filled
                type="number"
              />
              <q-select
                v-model="location"
                filled
                label="Location"
                use-input
                :options="optionsLocation"
                @filter="filterLocFn"
              />

              <q-select
                v-model="category"
                filled
                label="Category"
                :options="optionsCategory"
                use-input
                @filter="filterCatFn"
              />
              <TimeInputVue
                v-model="endTime"
                :date="endTime"
                :label="`Deadline`"
                @update-time="endTime = $event"
              />

              <div style="overflow: hidden;">
                <q-btn
                  style="float:right;"
                  color="primary"
                  label="Continue"
                  @click="$refs.stepper.next()"
                />
                <q-btn
                  v-if="step > 1"
                  style="float:right;"
                  flat
                  color="primary"
                  label="Back"
                  class="q-ml-sm"
                  @click="$refs.stepper.previous()"
                />
              </div>
            </q-form>
          </q-item-section>
        </q-item>
      </q-step>

      <q-step
        :name="2"
        title="Images and Description"
        icon="create_new_folder"
        :done="step > 2"
      >
        <q-item class="myItem">
          <q-item-section>
            <div class="row">
              <div class="col-4">
                <q-uploader
                  label="Batch upload"
                  multiple
                  batch
                  :factory="upload"
                  style="width:100%"
                />
              </div>
              <div class="col-8" style="padding-left: 20px;">
                <q-editor v-model="description" />
              </div>
            </div>
            <div style="overflow: hidden;">
              <q-btn
                style="float:right;"
                color="primary"
                label="Submit"
                :disabled="!image.length"
                @click="onSubmit()"
              />
              <q-btn
                v-if="step > 1"
                style="float:right;"
                flat
                color="primary"
                label="Back"
                class="q-ml-sm"
                @click="$refs.stepper.previous()"
              />
            </div>
          </q-item-section>
        </q-item>
      </q-step>

      <q-step :name="3" title="Auction Created" icon="assignment">
        Auction is created! Check your new Auction here!
        <div style="overflow: hidden;">
          <q-btn
            style="float:right;"
            color="primary"
            to="/user/myAuction"
            label="See my new Auction"
            @click="viewCreatedAuction()"
          />
        </div>
      </q-step>
    </q-stepper>
  </div>
</template>

<script>
import { uploadImage } from "../helper";
import { dropdownOpts, countries } from "../helper";
import moment from "moment";
import TimeInputVue from "../components/auctionItem/TimeInput.vue";

let warning = {
  color: "red-5",
  textColor: "white",
  icon: "warning",
  message: ""
};

export default {
  name: "AuctionCreateForm",
  components: {
    TimeInputVue
  },
  props: ["edit"],
  data() {
    return {
      category: "",
      title: "",
      description: "",
      endTime: moment().format("YYYY-MM-DD h:mm:ss"),
      price: 0,
      image: [],
      optionsCategory: dropdownOpts,
      optionsLocation: countries.map(x => x.name),
      date: "",
      step: 1,
      location: "",
      createdID: null
    };
  },
  created() {
    console.log("here1");
    if (this.edit) {
      console.log("edit", this.edit);
      this.id = Number(this.$route.params.id);

      let auction = this.$store.state.auction.myAuctions.find(
        x => x.id === this.id
      );
      console.log(auction);

      this.$data.category = auction.category;
      this.$data.title = auction.title;
      this.$data.description = auction.description;
      this.$data.endTime = auction.end_time;
      this.$data.price = auction.price;
      this.$data.location = auction.location;
    }
  },
  methods: {
    onSubmit() {
      let payload = {
        seller_id: this.$store.state.user.user_id,
        seller_name: this.$store.state.user.first_name,
        title: this.$data["title"],
        description: this.$data["description"],
        price: Number(this.$data["price"]),
        end_time: this.$data["endTime"],
        location: this.$data["location"],
        category: this.$data["category"],
        image: this.$data["image"]
      };
      this.$store.dispatch("auction/create", payload).then(res => {
        console.log(res);
        this.$router.push("/myauctions").catch(() => {});
      });
      // if (this.edit) {
      //   this.$refs.EditAuctionForm.validate().then(
      //     //validate underfine
      //     success => {
      //       if (success) {
      //         console.log("validated");
      //       }
      //     },
      //     err => {
      //       console.log(err);
      //       warning.message = err.message;
      //       this.$q.notify(warning);
      //     }
      //   );
      //   return;
      // }
      // this.$refs.CreateAuctionForm.validate().then(
      //   success => {
      //     if (success) {
      //       // auction call the store to update state
      //       console.log(success);
      //       console.log(this.$data);
      //       let auction = {
      //         seller_name: `${this.$store.state.user.first_name}-${this.$store.state.user.last_name}`,
      //         seller_id: this.$store.state.user.user_id,
      //         category: this.$data.categoryId,
      //         title: this.$data.title,
      //         description: this.$data.description,
      //         end_time: this.$data.date.replace(/\//g, "-") + " 00:42:00",
      //         price: new Number(this.$data.price),
      //         image: this.$data.image,
      //         location: this.$data.location
      //       };
      //       console.log(auction);
      //     }
      //   },
      //   err => {
      //     console.log("build");
      //     console.log(this.data);
      //     console.log(err);
      //     warning.message = err.message;
      //     this.$q.notify(warning);
      //   }
      // );
    },
    upload(file) {
      for (let f of file) {
        uploadImage(f, (err, res) => {
          if (err) {
            warning.message = err.message;
            this.$q.notify(warning);
          }
          console.log("uploading the image");
          this.$data.image.push(res.Location);
          console.log(this.$data.image);
        });
      }
    },
    goBack() {
      if (this.edit) {
        this.$router
          .push({
            name: "auctiionItem",
            params: {
              id: this.id
            }
          })
          .catch(err => console.log(err));
      } else {
        this.$router
          .push({
            path: "/auctions"
          })
          .catch(err => console.log(err));
      }
    },
    viewCreatedAuction() {
      //???
      this.$axios.get("/auction/" + this.$data.categoryId).then(response => {
        console.log(response);
        this.$store.dispatch(
          "auction/getMyAuctions",
          this.$store.state.user.user_id
        );
        this.$router
          .push({
            name: "auctionItem",
            params: {
              id: this.$data.categoryId
            }
          })
          .catch(err => console.log(err));
      });
    },
    filterLocFn(val, update) {
      if (val === "") {
        update(() => {
          this.$data.optionsLocation = countries.map(x => x.name);
        });
        return;
      }

      update(() => {
        const needle = val.toLowerCase();
        this.$data.optionsLocation = countries
          .map(x => x.name)
          .filter(v => v.toLowerCase().indexOf(needle) > -1);
      });
    },
    filterCatFn(val, update) {
      if (val === "") {
        update(() => {
          this.$data.optionsCategory = dropdownOpts;
        });
        return;
      }

      update(() => {
        const needle = val.toLowerCase();
        this.$data.optionsCategory = dropdownOpts.filter(
          v => v.toLowerCase().indexOf(needle) > -1
        );
      });
    }
  }
};
</script>

<style scoped>
.myItem {
  padding-left: 0px;
  padding-right: 0px;
}
</style>
