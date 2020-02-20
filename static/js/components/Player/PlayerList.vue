<script>

import PlayerListItem from './PlayerListItem.vue';
import PlayerListMedia from './PlayerListMedia.vue';

export default {
  name: 'PlayerList',
  components: {
    'player-item': PlayerListItem,
    'player-media': PlayerListMedia,
  },
  props: {
    items: {
      type: Array,
      required: false,
      default() {
        return [];
      },
    },
  },

};
</script>
<style lang="scss" scoped>

</style>
<template>
  <div>
    <player-item
      v-for="(item, itemIndex) in items"
      :key="`item-${itemIndex}`"
      :item="item"
    >
      <player-media
        v-for="(media, mediaIndex) in item.media"
        :key="`media-${mediaIndex}`"
        :media="media"
      />
    </player-item>
  </div>
</template>
