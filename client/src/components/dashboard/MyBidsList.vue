<template>
  <div class="q-pa-md">
    <q-table
      title="My Bids"
      :data="data"
      :columns="columns"
      row-key="name"
      :pagination.sync="pagination"
      lazy
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="image" auto-width :props="props">
            <q-img :src="props.row.image" />
          </q-td>
          <q-td v-for="f in fields" :key="f" auto-width :props="props">
            {{ props.row[f] }}
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>
<script>
export default {
  props: ["items"],
  data() {
    return {
      pagination: {},
      fields: ["title", "created", "price", "seller_name"],
      columns: [
        {
          name: "image",
          required: true,
          label: "Images",
          field: "image",
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
        // {
        //   name: "description",
        //   align: "center",
        //   label: "Description",
        //   field: "description",
        //   sortable: true
        // },
        {
          name: "created",
          align: "center",
          label: "Created at",
          field: "created",
          // format: v => date(v, ""),
          sortable: true
        },
        {
          name: "price",
          label: "Price(Aud)",
          align: "center",
          field: "price",
          sortable: true,
          sort: (a, b) => parseInt(a, 10) - parseInt(b, 10)
        },
        {
          name: "seller_name",
          label: "Seller",
          field: "seller_name",
          align: "left",
          sortable: true,
          sort: (a, b) => parseInt(a, 10) - parseInt(b, 10)
        }
      ],
      data: this.items
    };
  }
};
</script>
