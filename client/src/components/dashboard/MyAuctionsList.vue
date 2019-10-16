<template>
  <div class="q-pa-md">
    <h5><a name="myAuctions">My Auctionst</a></h5>
    <q-table
      title="My Auctions"
      :data="data"
      :columns="columns"
      row-key="name"
      lazy
    />
  </div>
</template>
<script>
export default {
  props: ["items"],
  data() {
    return {
      columns: [
        {
          name: "image",
          required: true,
          label: "Images",
          // field: row => row.name,
          // format: val => `${val}`,
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
          name: "desc",
          align: "center",
          label: "Description",
          field: "description",
          sortable: true
        },
        {
          name: "create",
          align: "center",
          label: "Created at",
          field: "created",
          sortable: true
        },
        {
          name: "price",
          label: "Price(Aud)",
          field: "price",
          sortable: true,
          sort: (a, b) => parseInt(a, 10) - parseInt(b, 10)
        }
      ],
      data: this.items
    };
  }
};
</script>
