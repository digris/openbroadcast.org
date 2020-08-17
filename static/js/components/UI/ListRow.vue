<script>
import LazyImage from './LazyImage.vue';
import PlayButton from '../PlayButton/PlayButton.vue';
import ContextMenu from './VisualWithActions/ContextMenu.vue';

export default {
  name: 'ListRow',
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
    class="list-row"
    :class="{'list-row--is-selected': selected}"
  >
    <div class="list-row__visual">
      <lazy-image :src="imageUrl" />
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
    <div class="list-row__actions">
      <context-menu
        v-if="actions.length"
        toggle-color="#a5a5a5"
        :toggle-size="(24)"
        :menu-position="{top: '48px'}"
        :visible="(false)"
        :actions="objectActions"
      />
    </div>
    <div
      class="list-row__body"
      @click="toggleSelection"
    >
      <slot name="default" />
    </div>
    <div class="list-row__appendix">
      <slot name="appendix" />
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .list-row {

    display: flex;

    margin-bottom: 0.5rem;

    background: #fff;

    &--is-selected {
      background: var(--primary-color-light);
      /*border: 1px solid red;*/
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

    &__actions {
      position: relative;

      display: flex;

      align-items: center;
      justify-content: center;

      width: 64px;

    }

    &__body {


      display: grid;
      flex-grow: 1;
      grid-column-gap: 1rem;
      grid-template-columns: 50% 50%;

      padding: 4px 4px 4px 4px;

      cursor: pointer;

      .column {
        display: flex;
        flex-direction: column;
      }

      .extra-artists {
        margin-top: 0.5rem;
      }

    }

    &__appendix {
      position: relative;

      display: flex;
      flex-direction: column;

      align-items: flex-end;

      min-width: 140px;

      padding: 4px 4px 4px 4px;
    }
  }
</style>
