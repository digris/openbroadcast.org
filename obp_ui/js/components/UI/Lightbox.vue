<script>
import { EventBus } from '../../eventBus';
import Modal from './Modal.vue';
import LazyImage from './LazyImage.vue';

export default {
  name: 'Lightbox',
  components: {
    modal: Modal,
    'lazy-image': LazyImage,
  },
  data() {
    return {
      image: null,
      visible: false,
    };
  },
  mounted() {
    EventBus.$on('lightbox:show-image', (image) => {
      this.show(image);
    });
  },
  methods: {
    close() {
      this.visible = false;
    },
    show(image) {
      this.visible = true;
      this.image = image;
    },
  },
};
</script>
<template>
  <modal
    :show="visible"
    @close="close"
  >
    <div
      v-if="image"
      slot="content"
      class="lightbox"
    >
      <lazy-image :src="image" />
    </div>
  </modal>
</template>
<style lang="scss" scoped>
.lightbox {
  padding: 12px 0px 0px;
}
</style>
