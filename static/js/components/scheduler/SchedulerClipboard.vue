<script>

import { Drag, Drop } from 'vue-drag-drop';
import SchedulerClipboardItem from './SchedulerClipboardItem.vue';

const DEBUG = true;

export default {
  name: 'SchedulerClipboard',
  components: {
    drag: Drag,
    drop: Drop,
    'clipboard-item': SchedulerClipboardItem,
  },
  props: {
    // emission: Object,
  },
  data() {
    return {
      dropActive: false,
      items: [],
    };
  },
  computed: {
    clipboardItems() {
      return this.$store.getters['scheduler/clipboard'];
    },
  },
  methods: {
    dragenter(transferData, e) {
      if (DEBUG) console.debug('dragenter', transferData, e);
      this.dropActive = true;
    },
    dragleave(transferData, e) {
      if (DEBUG) console.debug('dragleave', transferData, e);
      this.dropActive = false;
    },
    drop(transferData, e) {
      if (DEBUG) console.debug('drop', transferData, e);
      this.dropActive = false;
      this.$store.dispatch('scheduler/addToClipboard', transferData.co);
    },
    clearClipboard() {
      this.$store.dispatch('scheduler/clearClipboard');
    },
    deleteItem(uuid) {
      this.$store.dispatch('scheduler/removeFromClipboard', uuid);
    },
  },
};
</script>
<style lang="scss" scoped>
    .clipboard {
      // background: limegreen;

      /* > div { */

      /* background: orangered; */

      /* } */

      &__dropzone {
        height: 40px;
        background: white;
        pointer-events: none;

        &--is-active {
          // height: 100px;
          background: greenyellow;
        }
      }

      &__actions {
        padding: 8px 0;
        display: flex;

        .action {
          flex-grow: 1;
          justify-content: center;
          cursor: pointer;
          background: white;
          padding: 1px 8px;
          display: inline-flex;
          border: 1px solid #dadada;

          &:hover {
            background: #63c;
            border-color: #63c;
            border-radius: 2px;
            color: white;
          }
        }
      }

      &__items {
        .clipboard-item {
          margin-bottom: 4px;
        }
      }
    }

    .items-leave-active {
      transition: opacity 600ms;
    }

    .items-enter-active {
      transition: opacity 600ms;
    }

    .items-enter,
    .items-leave-to {
      opacity: 0;
    }
</style>

<template>
  <drop
    @dragenter="dragenter"
    @dragleave="dragleave"
    @drop="drop"
  >
    <div class="clipboard">
      <div class="clipboard__actions">
        <span
          class="action"
          @click="clearClipboard"
        >Clear Clipboard</span>
      </div>
      <div class="clipboard__items">
        <transition-group
          name="items"
          tag="div"
          mode="in-out"
        >
          <drag
            v-for="item in clipboardItems"
            :key="item.uuid + item.ct"
            :transfer-data="item"
          >
            <template slot="image">
              <div style="background: yellow; z-index: 1001;">
                (( DRAG ))
              </div>
            </template>
            <clipboard-item
              :item="item"
              @delete="deleteItem"
              @mouseenter="$emit('itemMouseenter', item.uuid)"
              @mouseleave="$emit('itemMouseleave', item.uuid)"
            />
          </drag>
        </transition-group>
      </div>
      <div
        :class="{ 'clipboard__dropzone--is-active': dropActive }"
        class="clipboard__dropzone"
      />
    </div>
    <div style="margin: 10px 0 0 4px;">
      <a href="/program/scheduler/legacy/">Old Scheduler</a>
    </div>
  </drop>
</template>
