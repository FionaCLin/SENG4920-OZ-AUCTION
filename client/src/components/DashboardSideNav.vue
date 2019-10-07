<template>
  <div class="q-pa-md" style="min-width: 180px">
    <q-list bordered padding class="rounded-borders text-primary">
      <q-item
        clickable
        v-ripple
        :active="link === 'newAuctions'"
        @click="link = 'newAuctions'"
        active-class="my-menu-link"
      >
        <q-item-section avatar>
          <q-icon name="fiber_new" />
        </q-item-section>

        <q-item-section>New Auctions</q-item-section>
      </q-item>

      <q-item
        clickable
        v-ripple
        :active="link === 'auctions'"
        @click="link = 'auctions'"
        active-class="my-menu-link"
      >
        <q-item-section avatar>
          <q-icon name="gavel" />
        </q-item-section>

        <q-item-section>My Auctions</q-item-section>
      </q-item>

      <q-item
        clickable
        v-ripple
        :active="link === 'bids'"
        @click="link = 'bids'"
        active-class="my-menu-link"
      >
        <q-item-section avatar>
          <q-icon name="collections_bookmark" />
        </q-item-section>

        <q-item-section>Bids</q-item-section>
      </q-item>

      <q-separator spaced />

      <q-item
        clickable
        v-ripple
        :active="link === 'trash'"
        @click="link = 'trash'"
        active-class="my-menu-link"
      >
        <q-item-section avatar>
          <q-icon name="delete" />
        </q-item-section>

        <q-item-section>Trash</q-item-section>
      </q-item>

      <q-item
        clickable
        v-ripple
        :active="link === 'help'"
        @click="link = 'help'"
        active-class="my-menu-link"
      >
        <q-item-section avatar>
          <q-icon name="help" />
        </q-item-section>

        <q-item-section>Help</q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
export default {
  name: "SideNav",
  data() {
    return {
      link: "index"
    };
  }
};
</script>
