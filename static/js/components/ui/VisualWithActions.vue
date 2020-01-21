<script>

import settings from '../../settings';
import LazyImage from './LazyImage.vue';
import Lightbox from './Lightbox.vue';
import Play from './VisualWithActions/Play.vue';
import ContextMenu from './VisualWithActions/ContextMenu.vue';

const DEBUG = true;

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
    primaryAction() {
      const index = this.actions.findIndex((action) => action.key === 'play');
      if (index < 0) {
        return null;
      }
      return this.actions[index];
      // return this.actions.findIndex((action) => action.key === 'play') > -1;
    },
    secondaryActions() {
      // play is considered to be the primary / first action.
      // so return all actions except play.
      return this.actions.filter((action) => action.key !== 'play');
    },
  },
  methods: {
    onMouseOver() {
      this.isHover = true;
    },
    onMouseLeave() {
      this.isHover = false;
      this.hideSecondaryActions();
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
    handleAction(action) {
      this.hideSecondaryActions();
      console.debug('handleAction', action);

      // just redirect to url if present
      if (action.url) {
        document.location.href = action.url;
        return;
      }

      // TODO: implement in a modular way...
      if (action.key === 'play') {
        this.playerControls({
          do: 'load',
          items: [{
            ct: this.ct,
            uuid: this.uuid,
          }],
        });
      }
    },
    playerControls(action) {
      const _e = new CustomEvent('player:controls', { detail: action });
      window.dispatchEvent(_e);
    },
  },
};
</script>
<style lang="scss" scoped>
    .visual-with-actions {
      margin: 0;
      position: relative;

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
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-rows: 30% auto 30%;

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

          .toggle {
            cursor: pointer;

            > i {
              color: white;
              font-size: 32px;
              line-height: 32px;
              transition: transform 200ms;
            }

            //&:hover {
            //    > i {
            //        color: red;
            //    }
            //}
            &--active {
              > i {
                transform: rotate(-90deg);
              }
            }
          }

          .context-menu {
            margin-top: 48px;
            margin-right: 4px;
            background: white;
          }
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
              v-if="primaryAction"
              @click="handleAction(primaryAction)"
            />
          </div>
          <div
            class="actions__secondary"
          >
            <div
              v-if="(secondaryActions && secondaryActions.length)"
              class="toggle"
              :class="{ 'toggle--active': secondaryActionsVisible }"
              @click="toggleSecondaryActions"
            >
              <i class="fa fa-ellipsis-h" />
            </div>
            <context-menu
              :visible="secondaryActionsVisible"
              :actions="secondaryActions"
              @click="handleAction"
            />
          </div>
        </div>
      </div>
      <div
        class="panel__bottom"
        @click="showLightbox"
      >
        <div
          v-if="largeImageUrl"
          class="thumbnails"
        >
          <div class="thumbnail">
            <!--<img :src="imageUrl">-->
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
