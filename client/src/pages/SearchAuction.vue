<template>
  <q-page padding class="myPage">
    <div class="q-mb-md">
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
                        <TimeInputVue
                          v-model="advanced.startDate"
                          :date="advanced.startDate"
                          :label="`Start Date`"
                          @update-time="advanced.startDate = $event"
                        />
                      </div>
                      <div class="col-6">
                        <TimeInputVue
                          v-model="advanced.endDate"
                          :date="advanced.endDate"
                          :label="`End Date`"
                          @update-time="advanced.endDate = $event"
                        />
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
                      :options="optionsCategory"
                      use-input
                      @filter="filterCatFn"
                    />
                  </div>
                  <div>
                    <p class="titles">Location</p>
                    <q-select
                      v-model="advanced.location"
                      filled
                      label="Location"
                      use-input
                      :options="optionsLocation"
                      @filter="filterLocFn"
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
    <div v-if="searchResult && searchResult.length > 0">
      <MyAuctionsList :items="searchResult" />
    </div>
    <div v-else-if="loading" class="flex flex-center">
      <q-linear-progress
        dark
        rounded
        style="height: 20px"
        query
        color="cyan"
        class="q-mt-sm"
      />
    </div>
  </q-page>
</template>

<script>
import MyAuctionsList from "../components/dashboard/MyAuctionsList";
import { dropdownOpts, countries } from "../helper";
import TimeInputVue from "../components/auctionItem/TimeInput.vue";

export default {
  components: {
    MyAuctionsList,
    TimeInputVue
  },
  data() {
    return {
      tab: "one",
      searchResult: [],
      loading: false,
      advanced: {
        startDate: null,
        endDate: null,
        startPrice: null,
        endPrice: null,
        category: null,
        location: null
      },
      optionsCategory: dropdownOpts,
      optionsLocation: countries.map(x => x.name),
      normal: {
        search: ""
      }
    };
  },
  methods: {
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
    },
    normalSearch() {
      return this.$axios
        .get("/auction/search-key/" + this.$data.normal.search)
        .then(async res => {
          this.$data.loading = true;

          return res.data;
        })
        .catch(err => {
          console.log(err);
        });
    },
    advancedSearch(query) {
      return this.$axios
        .get(`/auction/search/filter${query}`)
        .then(async res => {
          this.$data.loading = true;

          return res.data;
        })
        .catch(err => {
          console.log(err);
        });
    },
    onSubmit() {
      if (this.$data.tab == "one") {
        this.$refs.normalForm.validate().then(
          async success => {
            if (success) {
              // yay, models are correct
              this.$data.searchResult = [];
              let res = await this.normalSearch();
              console.log(res, "$$$$$$");
              setTimeout(() => {
                this.$data.searchResult = res;
                this.$data.loading = false;
              }, 2000);
            }
          },
          err => {
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
          async success => {
            if (success) {
              let query = [];

              for (let k of [
                "startDate",
                "endDate",
                "startPrice",
                "endPrice",
                "category",
                "location"
              ]) {
                if (this.advanced[k] !== null && this.advanced[k] !== "") {
                  query.push(`${k}=${this.advanced[k]}`);
                }
              }
              console.log(this.$data.advanced, "Target~~~~~~!");
              if (query.length) {
                query = query.join("&");
                query = `?${query}`;
              }

              this.$data.searchResult = [];
              console.log(query);
              let res = await this.advancedSearch(query);
              console.log(res, "$$$$$$", query);
              setTimeout(() => {
                this.$data.searchResult = res;
                this.$data.loading = false;
              }, 2000);
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
