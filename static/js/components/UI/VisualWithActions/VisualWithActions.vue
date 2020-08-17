<script>

import settings from '../../../settings';
import LazyImage from '../LazyImage.vue';
import Lightbox from '../Lightbox.vue';
import Play from './Play.vue';
import ContextMenu from './ContextMenu.vue';

export default {
  name: 'VisualWithActions',
  components: {
    lightbox: Lightbox,
    'lazy-image': LazyImage,
    play: Play,
    'context-menu': ContextMenu,
  },
  props: {
    ct: {
      type: String,
      required: true,
    },
    uuid: {
      type: String,
      required: true,
    },
    url: {
      type: String,
      default: null,
    },
    imageUrl: {
      type: String,
      required: false,
      default: null,
    },
    largeImageUrl: {
      type: String,
      required: false,
      default: null,
    },
    actions: {
      type: Array,
      required: false,
      default() {
        return [];
      },
    },
  },
  data() {
    return {
      placeholderImage: settings.PLACEHOLDER_IMAGE,
      isHover: false,
      lightboxVisible: false,
      secondaryActionsVisible: false,
    };
  },
  computed: {
    canPlay() {
      return this.actions.findIndex((action) => action.key === 'play') > -1;
    },
    playAction() {
      const index = this.actions.findIndex((action) => action.key === 'play');
      if (index < 0) {
        return null;
      }
      return this.actions[index];
      // return this.actions.findIndex((action) => action.key === 'play') > -1;
    },
    // secondaryActions() {
    //   // play is considered to be the primary / first action.
    //   // so return all actions except play.
    //   return this.actions.filter((action) => action.key !== 'play');
    // },
    secondaryActions() {
      // play is considered to be the primary / first action.
      // so return all actions except play.
      return this.actions;
    },
  },
  methods: {
    onMouseOver() {
      this.isHover = true;
    },
    onMouseLeave() {
      this.isHover = false;
      // this.hideSecondaryActions();
      this.$refs.contextMenu.closeMenu();
    },
    toggleSecondaryActions() {
      if (this.secondaryActionsVisible) {
        this.hideSecondaryActions();
      } else {
        this.showSecondaryActions();
      }
    },
    showSecondaryActions() {
      this.secondaryActionsVisible = true;
    },
    hideSecondaryActions() {
      this.secondaryActionsVisible = false;
    },
    showLightbox() {
      this.lightboxVisible = true;
    },
    hideLightbox() {
      this.lightboxVisible = false;
    },
    handleAction() {
      this.hideSecondaryActions();
    },
  },
};
</script>
<template>
  <div
    class="visual-with-actions"
    @mouseover="onMouseOver"
    @mouseleave="onMouseLeave"
  >
    <lazy-image :src="imageUrl" />

    <div
      class="mask"
      :class="{ 'mask--visible': isHover }"
    />

    <div
      v-if="isHover"
      class="panel"
    >
      <div
        class="panel__top"
      />
      <div
        class="panel__middle"
      >
        <div
          class="actions"
        >
          <div
            class="actions__rating"
          >
            <!--R-->
          </div>
          <div
            class="actions__play"
          >
            <play
              v-if="playAction"
              :action="playAction"
            />
          </div>
          <div
            class="actions__secondary"
          >
            <context-menu
              ref="contextMenu"
              toggle-color="white"
              :menu-position="{right: 0, top: '54px'}"
              :visible="secondaryActionsVisible"
              :actions="secondaryActions"
              @click="handleAction"
            />
          </div>
        </div>
      </div>
      <div
        v-if="largeImageUrl"
        class="panel__bottom"
        @click="showLightbox"
      >
        <div
          class="thumbnails"
        >
          <div class="thumbnail">
            <lazy-image :src="imageUrl" />
          </div>
        </div>
      </div>
    </div>

    <lightbox
      v-if="largeImageUrl"
      :visible="lightboxVisible"
      :image-url="largeImageUrl"
      @close="hideLightbox"
    />
  </div>
</template>
<style lang="scss" scoped>
  .visual-with-actions {
    position: relative;

    height: 100%;
    margin: 0;

    .mask {
      position: absolute;
      top: 0;
      left: 0;

      width: 100%;
      height: 100%;

      background: #000;
      opacity: 0;

      transition: opacity 200ms;

      &--visible {
        opacity: 0.65;
      }
    }

    .panel {
      position: absolute;
      top: 0;
      left: 0;

      display: grid;
      grid-template-rows: 30% auto 30%;
      width: 100%;
      height: 100%;

      &__middle {
        display: flex;
        flex-direction: column;
        justify-content: center;
      }

      &__bottom {
        display: flex;
        align-items: flex-end;
      }
    }

    .actions {
      display: grid;
      grid-template-columns: 30% auto 30%;

      &__rating,
      &__play,
      &__secondary {
        display: flex;
        align-items: center;
        justify-content: center;
      }

      &__rating {
        // background: red;
      }

      &__play {
        // background: deepskyblue;
      }

      &__secondary {
        position: relative;
      }
    }

    .thumbnails {
      margin: 0 0 0 6px;

      .thumbnail {
        cursor: pointer;

        img {
          width: 32px;
          height: 32px;
        }
      }
    }
  }

</style>
