<template>
  <!-- <q-page class="bg-grey-1">
    <div class="q-pa-md">
      <div class="row">
        <div class="col-10">
          <q-card
            class="col-xs-12 col-sm-11 col-md-10 col-lg-9"
            style="min-width: 300px;"
          >
            <q-item>
              <q-item-section avatar>
                <q-avatar class="self-center" size="100px" font-size="52px">
                  <q-img v-if="images.length" src />
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

                  <q-input filled v-model="date" label="Deadline" mask="date" :rules="['date']">
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
                </q-form>
                <q-select
                  filled
                  label="Category"
                  v-model="categoryId"
                  :options="options"
                />
              </q-item-section>
            </q-item>
            <q-card-actions>
              <q-btn color="primary" label="Submit" type="Submit" />
              <q-btn color="amber" glossy label="Reset" type="reset" />
              <q-btn
                color="deep-orange"
                glossy
                label="Cancel"
                type="cancel"
                @click="goBack"
              />
            </q-card-actions>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>-->

  <div class="q-pa-md">
    <q-stepper ref="stepper" v-model="step" color="primary" animated>
      <q-step :name="1" title="Basic Information" icon="settings" :done="step > 1">
        <q-item class="myItem">
          <q-item-section>
            <q-form
              :ref="edit ? 'EditAuctionForm' : 'CreateAuctionForm'"
              class="q-gutter-md"
              @submit="onSubmit"
            >
              <q-input v-model="title" label="Product title" filled type="text" />
              <q-input v-model="price" label="Starting Price" filled type="number" />
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
                    <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                      <q-date v-model="date" @input="() => $refs.qDateProxy.hide()" />
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
              <q-select filled label="Category" v-model="categoryId" :options="options" />
            </q-form>
          </q-item-section>
        </q-item>
      </q-step>

      <q-step :name="2" title="Images and Description" icon="create_new_folder" :done="step > 2">
        <div>
          <div class="row">
            <div class="col-4">
              <q-uploader label="Batch upload" multiple batch :factory="upload" style="width:100%" />
            </div>
            <div class="col-8" style="padding-left: 20px;">
              <q-editor v-model="description" />
            </div>
          </div>
        </div>
      </q-step>

      <q-step
        :name="3"
        title="Auction Created"
        icon="assignment"
      >Auction is created! Check your new Auctioon here!</q-step>

      <template v-slot:navigation>
        <q-stepper-navigation style="overflow: hidden;">
          <q-btn
            v-if="step < 3"
            style="float:right;"
            color="primary"
            @click="$refs.stepper.next()"
            label="Continue"
          />
          <q-btn
            v-if="step > 1"
            style="float:right;"
            flat
            color="primary"
            label="Back"
            @click="$refs.stepper.previous()"
            class="q-ml-sm"
          />
          <q-btn
            v-if="step === 3"
            style="float:right;"
            flat
            color="primary"
            label="Finish"
            @click="onSubmit()"
            class="q-ml-sm"
          />
        </q-stepper-navigation>
      </template>
    </q-stepper>
  </div>
</template>

<script>
// import { required, minLength } from 'vuelidate/lib/validators'
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
      location: ""
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
      console.log(this.$data)
      console.log("here2");
      console.log(JSON.parse(localStorage.getItem('user')));
      axiosInstance
        .post("/auction", {
          //seller_name: JSON.parse(localStorage.getItem('user')).first_name,
          seller_name: "test",
          seller_id: JSON.parse(localStorage.getItem('user')).user_id,
          category_id: this.$data.categoryId,
          title: this.$data.title,
          description: this.$data.description,
          end_time: this.$data.date.replace(/\//g,'-') + " 00:42:00",
          price: new Number(this.$data.price),
          image: this.$data.image
        })
        .then(response => {
          console.log(response);
        });
      //connect to back-end


      //
      // sellerName: "",
      // sellerId: "",
      if (this.edit) {
        this.$refs.EditAuctionForm.validate().then(//validate underfine
          success => {
            if (success) {
              // yay, models are correct
              // auction call the store to update state
            }
          },
          err => {
            console.log(err);
            // oh no, user has filled in
            // at least an invalid value

            warning.message = err.message;
            this.$q.notify(warning);
          }
        );
        return;
      }
      this.$refs.CreateAuctionForm.validate().then(
        success => {
          if (success) {
            console.log("build");
            console.log(this.data);
          }
        },
        err => {
          console.log("build");
          console.log(this.data);
          console.log(err);

          // oh no, user has filled in
          // at least an invalid value
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
