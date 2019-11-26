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
              />
              <q-input
                v-model="price"
                label="Starting Price"
                filled
                type="number"
              />
              <q-input v-model="location" label="Location" filled type="text" />

              <q-input
                v-model="date"
                filled
                label="Deadline"
                mask="date"
                :rules="['date']"
                style="padding-bottom:0px;"
              >
                <template v-slot:append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      transition-show="scale"
                      transition-hide="scale"
                    >
                      <q-date
                        v-model="date"
                        @input="() => $refs.qDateProxy.hide()"
                      />
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
              <q-select
                v-model="categoryId"
                filled
                label="Category"
                :options="options"
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
            label='See my new Auction'
            @click="viewCreatedAuction()"
          />
        </div>
      </q-step>
    </q-stepper>
  </div>
</template>

<script>
// import { required, minLs } from 'vuelidate/lib/validators'
import { uploadImage } from "../helper";
import { axiosInstance } from "boot/axios";

let warning = {
  color: "red-5",
  textColor: "white",
  icon: "warning",
  message: ""
};

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
      image: [],
      options: ["Handicraft", "Second hand"],
      date: "",
      step: 1,
      location: "",
      createdID: null
    };
  },
  created() {
    console.log("here1");
    console.log(this.data);
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
      this.$data.location = auction.location;
    }
  },
  methods: {
    onSubmit() {
      console.log(JSON.parse(localStorage.getItem("user")));
      axiosInstance
        .post("/auction", {
          //seller_name: JSON.parse(localStorage.getItem('user')).first_name,
          seller_name: "test",
          seller_id: JSON.parse(localStorage.getItem("user")).user_id,
          category: this.$data.categoryId,
          title: this.$data.title,
          description: this.$data.description,
          end_time: this.$data.date.replace(/\//g, "-") + " 00:42:00",
          price: new Number(this.$data.price),
          image: this.$data.image,
          location: this.$data.location
        })
        .then(response => {
          console.log(response);
          this.$data.categoryId = response.data.data.id;
          this.$refs.stepper.next();
        });
      if (this.edit) {
        this.$refs.EditAuctionForm.validate().then(
          //validate underfine
          success => {
            if (success) {
              console.log("validated");
            }
          },
          err => {
            console.log(err);

            warning.message = err.message;
            this.$q.notify(warning);
          }
        );
        return;
      }
      this.$refs.CreateAuctionForm.validate().then(
        success => {
          if (success) {
            // auction call the store to update state
            console.log(this.$data);
          }
        },
        err => {
          console.log("build");
          console.log(this.data);
          console.log(err);

          warning.message = err.message;
          this.$q.notify(warning);
        }
      );
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
    },
    viewCreatedAuction() {
       axiosInstance
        .get("/auction/" + this.$data.categoryId)
        .then(response => {
          console.log(response);
          this.$store.dispatch("auction/getMyAuctions", this.$store.state.user.user_id);
          this.$router.push({
            name: "auctionItem",
            params: {
              id: this.$data.categoryId
            }
          })
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
