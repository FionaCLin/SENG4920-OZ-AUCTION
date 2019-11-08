<template>
  <div class="q-pa-md mybox">
    <div class="row"></div>
    <div class="row">
      <div class="col-2"></div>
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
                @submit="onSubmit"
                class="q-gutter-md myForm"
              >
                    <q-input
                      filled
                      v-model="search"
                      label="Explore the world with keywords"
                      lazy-rules
                      :rules="[ val => val && val.length > 0 || 'Please type something']"
                    />
                  <div>
                    <q-btn class="myButton" label="Search" type="submit" color="primary"/>
                  </div>
              </q-form>
            </q-tab-panel>

            <q-tab-panel name="two">
              <q-form
                @submit="onSubmit"
                class="q-gutter-md myForm"
              >
                <div>
                  <p class="titles">Time Range</p>
                  <div class="row">
                    <div class="col-6 myItem">
                      <q-input filled v-model="startDate" label="Start Date" mask="date" :rules="['date']">
                        <template v-slot:append>
                          <q-icon name="event" class="cursor-pointer">
                            <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                              <q-date v-model="startDate" @input="() => $refs.qDateProxy.hide()" />
                            </q-popup-proxy>
                          </q-icon>
                        </template>
                      </q-input>
                    </div>
                    <div class="col-6">
                      <q-input filled v-model="endDate" label="End Date" mask="date" :rules="['date']">
                        <template v-slot:append>
                          <q-icon name="event" class="cursor-pointer">
                            <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                              <q-date v-model="endDate" @input="() => $refs.qDateProxy.hide()" />
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
                      <q-input v-model="startPrice" label="From Price" filled type="number" />
                    </div>
                    <div class="col-6">
                      <q-input v-model="endPrice" label="To Price" filled type="number" />
                    </div>
                  </div>
                </div>
                <div>
                  <p class="titles">Category</p>
                  <q-select filled label="Category" v-model="category" :options="optionsCategory" />
                </div>
                <div>
                  <p class="titles">Location</p>
                  <q-select filled label="Location" v-model="location" :options="optionsLocation" />
                </div>
                <div>
                  <q-btn class="myButton" label="Advanced Search" type="submit" color="primary"/>
                </div>
              </q-form>
            </q-tab-panel>

          </q-tab-panels>
        </q-card>
      </div>
      <div class="col-2"></div>
    </div>
  </div>
</template>



<script>
export default {
  data () {
    return {
      search: null,
      tab: 'one',
      startDate: '',
      endDate: '',
      startPric:'',
      endPrice: '',
      category: '',
      location: '',
      optionsCategory: ["Pet Supplies",
                "Movies",
                "Jewellery & Watches",
                "Industrial",
                "Home Entertainment",
                "Home & Garden",
                "Health & Beauty",
                "Sporting Goods",
                "Musical Instruments",
                "Music",
                "Phones & Accessories",
                "Pottery, Glass",
                "Services",
                "Tickets, Travel",
                "Stamps",
                "Gift Cards & Vouchers",
                "Home Appliances",
                "Food & Drinks",
                "Crafts",
                "Dolls, Bears",
                "Electronics",
                "Computers/Tablets & Networking",
                "Coins"],
      optionsLocation: ["Australia",
                        "USA",
                        "UK"

      ]
    }
  },
  methods: {
    onSubmit () {
    }
  }
};
</script>

<style lang="css" scoped>
.mybox { margin: 40px 10px; }
.myForm { margin: 45px 20px 30px 20px; }
.myItem { padding-right: 10px;}
.titles { padding: 0px 5px; }
</style>























