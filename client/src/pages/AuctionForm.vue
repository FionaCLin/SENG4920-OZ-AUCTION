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
                v-model="end_time"
                :date="end_time"
                :label="`Deadline`"
                @update-time="end_time = $event"
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
              <div class="col-5 text-center">
                <div v-if="edit">
                  Update to replace current display auction images.
                  <q-card-actions>
                    <q-btn
                      v-if="!imgedit"
                      label="Update"
                      type="Update"
                      color="green"
                      flat
                      @click="imgedit = true"
                    />

                    <q-btn
                      v-else
                      label="Cancel"
                      type="cancel"
                      color="red"
                      flat
                      @click="imgedit = false"
                    />
                  </q-card-actions>
                </div>
                <div
                  v-if="edit && !imgedit"
                  class="text-center"
                  @click="imgedit = !imgedit"
                >
                  <ImagesDisplay :image="image" />
                </div>
                <div v-else>
                  <q-uploader
                    label="Auction Images Upload"
                    multiple
                    batch
                    :factory="upload"
                    style="width:100%"
                  />
                </div>
                <div v-if="imgsupload">
                  <q-linear-progress dark query size="15px" />
                </div>
              </div>
              <div class="col-7" style="padding-left: 20px;">
                <q-editor v-model="description" />
              </div>
            </div>
            <div style="overflow: hidden;">
              <q-btn
                style="float:right;"
                color="primary"
                label="Submit"
                :disabled="!edit && !image.length"
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
import ImagesDisplay from "../components/auctionItem/ImagesDisplay";

let warning = {
  color: "red-5",
  textColor: "white",
  icon: "warning",
  message: "",
  position: "top"
};
let success = {
  color: "green-4",
  textColor: "white",
  position: "top",
  icon: "cloud_done",
  message: ""
};
export default {
  name: "AuctionCreateForm",
  components: {
    TimeInputVue,
    ImagesDisplay
  },
  props: ["edit"],
  data() {
    return {
      category: "",
      imgedit: false,
      imgsupload: false,
      title: "",
      description: "",
      end_time: moment().format("YYYY-MM-DD h:mm:ss"),
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
      for (let k of Object.keys(auction)) {
        this.$data[k] = auction[k];
      }
      this.$data.category = auction.category;
      this.$data.title = auction.title;
      this.$data.description = auction.description;
      (this.$data.end_time = moment(auction.end_time).format(
        "YYYY-MM-DD h:mm:ss"
      )),
        (this.$data.price = auction.price);
      this.$data.location = auction.location;
      this.auction = auction;
    }
  },
  methods: {
    createAuction() {
      let payload = {
        seller_id: this.$store.state.user.user_id,
        seller_name: this.$store.state.user.first_name,
        title: this.$data["title"],
        description: this.$data["description"],
        price: Number(this.$data["price"]),
        end_time: moment(this.$data["end_time"]).format("YYYY-MM-DD h:mm:ss"),
        location: this.$data["location"],
        category: this.$data["category"],
        image: this.$data["image"]
      };
      this.$store.dispatch("auction/create", payload).then(res => {
        console.log(res, "!!!");
        if (res.status != 200) {
          warning.message = res.data.message;
          this.$q.notify(warning);
          return;
        }
        this.$router.push("/myauctions").catch(() => {});
      });
    },
    onSubmit() {
      if (this.edit) {
        let payload = {};
        for (let k of [
          "title",
          "description",
          "price",
          "end_time",
          "location",
          "category",
          "image"
        ]) {
          if (this.$data[k] != this.auction[k]) {
            payload[k] = this.$data[k];
            if (k == "end_time") {
              payload[k] = moment(payload[k]).format("YYYY-MM-DD h:mm:ss");
            }
          }
        }
        console.log(payload, this.id);
        let id = this.id;

        this.$store
          .dispatch("auction/update", { id, payload })
          .then(res => {
            if (res && res.status != 200) {
              warning.message = res.data.message;
              this.$q.notify(warning);
              return;
            }
            success.message = res.data.message;
            setTimeout(this.$q.notify(success), 1000);
            this.$router
              .push({
                name: "auctionItem",
                params: {
                  id: this.id,
                  item: this.auction
                }
              })
              .catch(() => {});
          })
          .catch(err => console.log(err));
      } else {
        this.createAuction();
      }
    },
    async upload(file) {
      console.log(this.$data.imgsupload, 1);
      this.$data.imgsupload = true;
      console.log(this.$data.imgsupload, 2);
      let ps = [];
      file.forEach(f => {
        let p = new Promise(function(resolve, reject) {
          uploadImage(f, (err, res) => {
            if (err) {
              reject(err.message);
            } else {
              resolve(res.Location);
            }
          });
        });
        ps.push(p);
      });
      Promise.allSettled(ps)
        .then(
          res => {
            console.log("uploading the image");
            this.$data.image = res.map(x => x.value);
            console.log(res, "PPPPP");
          },
          err => {
            warning.message = err.message;
            this.$q.notify(warning);
          }
        )
        .finally(() => {
          this.$data.imgsupload = false;
          console.log(this.$data.imgsupload);
        });
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
            path: "/myauctions"
          })
          .catch(err => console.log(err));
      }
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
