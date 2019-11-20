<template>
  <div class="q-pa-md">
    <q-carousel v-model="slide" animated infinite autoplay swipeable thumbnails>
      <q-carousel-slide
        v-for="(src, i) in image"
        :key="i"
        :name="i"
        :img-src="src"
      />
    </q-carousel>
  </div>
</template>
<script>
export default {
  name: "ImagesDisplay",
  props: ["image"],
  data() {
    return {
      slide: 1
    };
  }
};
</script>
