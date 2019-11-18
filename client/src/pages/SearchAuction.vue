<template>
  <q-page padding class="myPage">
    <div class="q-pa-md mybox">
      <div class="row" style="justify-content: center;">
        <div class="col-8">
          <q-card class="col-xs-12 col-sm-11 col-md-10 col-lg-9">
            <q-tabs v-model="tab" class="text-teal">
              <q-tab label="Search" name="one" />
              <q-tab label="Advanced Search" name="two" />
            </q-tabs>

            <q-separator />

            <q-tab-panels v-model="tab" animated>
              <q-tab-panel name="one">
                <!-- <p>Search with keywords</p> -->

                <q-form
                  ref="normalForm"
                  class="q-gutter-md myForm"
                  @submit="onSubmit"
                >
                  <q-input
                    v-model="normal.search"
                    filled
                    label="Explore the world with keywords"
                    lazy-rules
                    :rules="[
                      val => (val && val.length > 0) || 'Please type something'
                    ]"
                  />
                  <div style="overflow:hidden">
                    <q-btn
                      class="myButton"
                      style="float:right;"
                      label="Search"
                      type="submit"
                      color="primary"
                    />
                  </div>
                </q-form>
              </q-tab-panel>

              <q-tab-panel name="two">
                <q-form
                  ref="advancedForm"
                  class="q-gutter-md myForm"
                  @submit="onSubmit"
                >
                  <div>
                    <p class="titles">Time Range</p>
                    <div class="row">
                      <div class="col-6 myItem">
                        <q-input
                          v-model="advanced.startDate"
                          filled
                          label="Start Date"
                          mask="date"
                          :rules="['date']"
                        >
                          <template v-slot:append>
                            <q-icon name="event" class="cursor-pointer">
                              <q-popup-proxy
                                ref="qDateProxy"
                                transition-show="scale"
                                transition-hide="scale"
                              >
                                <q-date
                                  v-model="advanced.startDate"
                                  @input="() => $refs.qDateProxy.hide()"
                                />
                              </q-popup-proxy>
                            </q-icon>
                          </template>
                        </q-input>
                      </div>
                      <div class="col-6">
                        <q-input
                          v-model="advanced.endDate"
                          filled
                          label="End Date"
                          mask="date"
                          :rules="['date']"
                        >
                          <template v-slot:append>
                            <q-icon name="event" class="cursor-pointer">
                              <q-popup-proxy
                                ref="qDateProxy"
                                transition-show="scale"
                                transition-hide="scale"
                              >
                                <q-date
                                  v-model="advanced.endDate"
                                  @input="() => $refs.qDateProxy.hide()"
                                />
                              </q-popup-proxy>
                            </q-icon>
                          </template>
                        </q-input>
                      </div>
                    </div>
                  </div>
                  <div>
                    <p class="titles">Price Range</p>
                    <div class="row">
                      <div class="col-6 myItem">
                        <q-input
                          v-model="advanced.startPrice"
                          label="From Price"
                          filled
                          type="number"
                        />
                      </div>
                      <div class="col-6">
                        <q-input
                          v-model="advanced.endPrice"
                          label="To Price"
                          filled
                          type="number"
                        />
                      </div>
                    </div>
                  </div>
                  <div>
                    <p class="titles">Category</p>
                    <q-select
                      v-model="advanced.category"
                      filled
                      label="Category"
                      :options="advanced.optionsCategory"
                    />
                  </div>
                  <div>
                    <p class="titles">Location</p>
                    <q-select
                      v-model="advanced.location"
                      filled
                      label="Location"
                      :options="advanced.optionsLocation"
                    />
                  </div>
                  <div style="overflow:hidden">
                    <q-btn
                      class="myButton"
                      style="float:right;"
                      label="Advanced Search"
                      type="submit"
                      color="primary"
                    />
                  </div>
                </q-form>
              </q-tab-panel>
            </q-tab-panels>
          </q-card>
        </div>
      </div>
    </div>
    <q-page>
      <MyAuctionsList :items="searchResult" />
    </q-page>
  </q-page>
</template>

<script>
import MyAuctionsList from "../components/dashboard/MyAuctionsList";
import { axiosInstance } from "boot/axios";
import { dropdownOpts, countries } from "../helper";

export default {
  components: {
    MyAuctionsList
  },
  data() {
    return {
      tab: "one",
      searchResult: [],
      advanced: {
        startDate: null,
        endDate: null,
        startPric: null,
        endPrice: null,
        category: null,
        location: null,
        optionsCategory: dropdownOpts,
        optionsLocation: countries.map(x => x.name)
      },
      normal: {
        search: ""
      }
    };
  },
  methods: {
    onSubmit() {
      // ask filter api
      if (this.$data.tab == "one") {
        this.$refs.normalForm.validate().then(
          success => {
            if (success) {
              // yay, models are correct
              console.log(this.$data.normal);
              axiosInstance
                .get("/auction/search-key/" + this.$data.normal.search)
                .then(
                  response => {
                    console.log(response);
                    console.log(this.$store.state.auction.myAuctions);
                    this.$data.searchResult = response.data;
                  },
                  err => {
                    console.log(err);
                  }
                );
            }
          },
          err => {
            console.log(err);
            console.log("problems!");

            this.$q.notify({
              color: "red-5",
              textColor: "white",
              icon: "warning",
              message: err.message
            });
          }
        );
      } else {
        this.$refs.advancedForm.validate().then(
          success => {
            if (success) {
              // yay, models are correct
              console.log(this.$data.advanced);
            }
          },
          err => {
            console.log(err);
            console.log("problems!");

            this.$q.notify({
              color: "red-5",
              textColor: "white",
              icon: "warning",
              message: err.message
            });
          }
        );
      }
    }
  }
};
</script>

<style lang="css" scoped>
.mybox {
  margin: 5% 10px;
}
.myForm {
  margin: 20px 20px;
}
.myItem {
  padding-right: 10px;
}
.titles {
  padding: 0px 5px;
}
.myPage {
  background-image: url("../statics/search.jpg");
  background-attachment: fixed;
  background-repeat: no-repeat;
  background-size: 100%;
}
</style>
