<script>

import debounce from 'debounce';

import { EventBus } from '../../../eventBus';

export default {
  name: 'ContextMenu',
  props: {
    visible: {
      type: Boolean,
      required: false,
      default: false,
    },
    actions: {
      type: Array,
      required: false,
      default() {
        return [];
      },
    },
    toggleColor: {
      type: String,
      default: 'inherit',
    },
    toggleSize: {
      type: Number,
      default: 32,
    },
    menuPosition: {
      type: Object,
      default() {
        return {
          left: 0,
          top: 0,
        };
      },
    },
  },
  data() {
    return {
      menuVisible: false,
    };
  },
  computed: {
    toggleStyle() {
      return {
        color: this.toggleColor,
        fontSize: `${this.toggleSize}px`,
        lineHeight: `${this.toggleSize}px`,
      };
    },
    menuStyle() {
      return this.menuPosition;
    },
  },
  methods: {
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
    closeMenu() {
      this.menuVisible = false;
    },
    debounceCloseMenu: debounce(function closeMenu() {
      this.closeMenu();
    }, 100),
    handleAction(action) {
      // this.$emit('click', action);
      EventBus.$emit('action', action);
    },
  },
};
</script>
<template>
  <div class="context-menu">
    <div
      class="context-menu__toggle"
      :style="toggleStyle"
      :class="{ 'is-active': menuVisible }"
      @click="toggleMenu"
    >
      <i class="fa fa-ellipsis-h" />
    </div>
    <transition name="fade">
      <div
        v-if="menuVisible"
        :style="menuStyle"
        class="context-menu__menu"
        @mouseleave="debounceCloseMenu"
      >
        <a
          v-for="action in actions"
          :key="action.key"
          :href="(action.url || '#')"
          class="menu-item"
          @click.prevent="handleAction(action)"
        >
          {{ action.title }}
        </a>
      </div>
    </transition>
  </div>
</template>
<style lang="scss" scoped>
  .context-menu {

    &__toggle {
      cursor: pointer;

      > i {
        color: inherit;
        font-size: inherit;
        line-height: inherit;

        transition: transform 200ms;
      }

      &.is-active {
        > i {
          transform: rotate(-90deg);
        }
      }

    }

    &__menu {

      position: absolute;
      z-index: 999;

      display: flex;
      flex-direction: column;
      min-width: 150px;

      background: white;

      filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.1));


      .menu-item {
        display: flex;
        width: 100%;
        padding: 10px 14px;

        color: #333333;

        white-space: nowrap;

        text-decoration: none;

        cursor: pointer;

        &:hover {
          color: #fff;

          background: #00bb73;
        }

      }
    }
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 200ms;
  }

  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }

</style>
