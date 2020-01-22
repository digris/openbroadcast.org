<script>

const DEBUG = false;

const ICON_MAP = {
  default: 'fa-pencil',
  edit: 'fa-pencil',
  download: 'fa-download',
  message: 'fa-envelope',
  admin: 'fa-lock',
  loginas: 'fa-key',
};

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
  },
  methods: {
    handleAction(action) {
      this.$emit('click', action);
    },
    getIconClass(action) {
      return ICON_MAP[action.key] || ICON_MAP.default;
    },
  },
};
</script>
<style lang="scss" scoped>
    .context-menu {
      position: absolute;
      top: 0;
      right: 0;
      z-index: 999;

      display: flex;
      flex-direction: column;
      min-width: 150px;

      filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.1));

      .menu-item {
        display: flex;
        width: 100%;
        padding: 10px 14px;

        cursor: pointer;

        &:hover {
          color: #fff;

          background: #00bb73;
        }

        &__icon {
          width: 20px;
        }

        &__name {
          flex-grow: 1;

          white-space: nowrap;
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
<template>
  <transition name="fade">
    <div
      v-if="visible"
      class="context-menu"
    >
      <div
        v-for="action in actions"
        :key="action.key"
        class="menu-item"
        @click="handleAction(action)"
      >
        <div class="menu-item__icon">
          <i
            :class="getIconClass(action)"
            class="fa"
          />
        </div>
        <div class="menu-item__name">
          {{ action.title }}
        </div>
      </div>
    </div>
  </transition>
</template>
