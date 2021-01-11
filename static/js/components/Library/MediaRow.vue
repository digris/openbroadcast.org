<script>
import { EventBus } from '../../eventBus';
import LazyImage from '../UI/LazyImage.vue';
import ContextMenu from '../UI/VisualWithActions/ContextMenu.vue';
import PlayButton from '../PlayButton/PlayButton.vue';

export default {
  name: 'MediaRow',
  components: {
    'lazy-image': LazyImage,
    'play-button': PlayButton,
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
    displayStyle: {
      type: String,
      required: false,
      default: 'default',
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
    actions: {
      type: Array,
      required: false,
      default() {
        return [];
      },
    },
    tags: {
      type: Array,
      required: false,
      default() {
        return [];
      },
    },
  },
  computed: {
    selected() {
      return this.$store.getters['objectSelection/objectSelection'](this.ct, this.uuid);
    },
    objectActions() {
      const objectActions = [];
      this.actions.forEach((originalAction) => {
        const action = { ...originalAction };
        action.uuid = this.uuid;
        action.ct = this.ct;
        action.url = action.url || this.url;
        objectActions.push(action);
      });

      return objectActions;
    },
    playAction() {
      const index = this.objectActions.findIndex((action) => action.key === 'play');
      if (index < 0) {
        return null;
      }
      return this.objectActions[index];
    },
    hasImage() {
      return this.displayStyle === 'default';
    },
    isMinimal() {
      return this.displayStyle === 'minimal';
    },
  },
  mounted() {
    EventBus.$emit('list-actions:register', this.objectActions);
  },
  methods: {
    toggleSelection() {
      this.$store.dispatch('objectSelection/toggleSelection', { ct: this.ct, uuid: this.uuid });
    },
  },
};
</script>
<template>
  <div
    class="media-row"
    :class="{'is-selected': selected, 'is-minimal': isMinimal}"
  >
    <div
      v-if="hasImage"
      class="media-row__visual"
    >
      <lazy-image
        v-if="hasImage"
        :src="imageUrl"
      />
      <div
        v-if="playAction"
        class="play-button-container"
      >
        <play-button
          :size="32"
          state="stopped"
          :action="playAction"
        />
      </div>
    </div>
    <div
      v-else
      class="media-row__play"
    >
      <play-button
        v-if="playAction"
        :size="20"
        state="stopped"
        hover-color="#6633cc"
        :action="playAction"
      />
    </div>
    <div class="media-row__actions">
      <context-menu
        v-if="actions.length"
        toggle-color="#a5a5a5"
        :obj-ct="ct"
        :obj-uuid="uuid"
        :toggle-size="(24)"
        :menu-position="{top: '48px'}"
        :visible="(false)"
        :actions="objectActions"
      />
    </div>
    <div
      class="media-row__body"
      @click="toggleSelection"
    >
      <slot name="default" />
      <div class="tags">
        <div
          v-for="(tag, index) in tags.slice(0, 5)"
          :key="`tag-${index}`"
          class="tag"
        >
          {{ tag }}
        </div>
      </div>
    </div>
    <div class="media-row__appendix">
      <slot name="appendix" />
    </div>
  </div>
</template>
<style lang="scss" scoped>
.media-row {

  display: flex;

  margin-bottom: 0.5rem;
  background: #fff;

  &.is-selected {
    background: var(--primary-color-light);
  }

  &__visual {
    position: relative;
    display: inline-grid;
    width: 64px;
    height: 64px;

    .play-button-container {

      position: absolute;
      width: 100%;
      height: 100%;
      opacity: 0;
      transition: background 200ms, opacity 200ms;

    }

    &:hover {
      .play-button-container {
        background: rgba(0, 0, 0, 0.5);
        opacity: 1;
      }
    }

  }

  &__play {
    width: 32px;
  }

  &__actions {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;

    width: 64px;

    .is-minimal & {
      width: 48px;
    }

  }

  &__body {


    display: grid;
    flex-grow: 1;
    grid-column-gap: 1rem;
    grid-template-columns: 50% 50%;

    padding: 2px 4px 2px 4px;
    cursor: pointer;

    //.is-minimal & {
    //  background: yellow;
    //}

    .column {
      display: flex;
      flex-direction: column;

      .is-minimal & {
        justify-content: center;
      }
    }

    .extra-artists {
      margin-top: 0;
    }

    .tags {
      display: inline-flex;
      grid-column: span 2;
      margin-top: 4px;

      .is-minimal & {
        display: none;
      }
      .tag {
        display: flex;
        align-items: center;
        justify-content: center;

        margin: 0 4px 0 0;
        padding: 0 4px;
        font-size: 90%;
        text-transform: uppercase;
        background: #f8f8f8;
        opacity: 0.7;
      }
    }

  }

  &__appendix {
    //position: relative;

    display: flex;
    flex-direction: column;

    align-items: flex-end;

    min-width: 140px;

    padding: 4px 4px 4px 4px;

    .is-minimal & {
      justify-content: center;
    }
  }
}
</style>
