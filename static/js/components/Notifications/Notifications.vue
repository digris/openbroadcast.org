<script>

const DEBUG = true;

export default {
  name: 'Notifications',
  computed: {
    notifications() {
      return this.$store.getters['notifications/notifications'];
    },
  },
  methods: {
    click(notification) {
      console.debug('notification', notification);
      this.$store.dispatch('notifications/removeNotification', { uuid: notification.uuid });
    },
  },
};
</script>
<style lang="scss" scoped>
  .notifications {

    // padding: 1rem;

    position: fixed;
    top: 32px;
    right: 1rem;
    // top: calc(32px + 1rem);
    z-index: 99;

    // background: var(--secondary-color);

    .notification {

      width: 320px;

      margin-top: 1rem;

      padding: 1rem;
      color: white;
      background: var(--primary-color);
      // background: #333;

      cursor: pointer;
      transition: all 1s;

      ::v-deep a {
        padding: 2px 4px;
        color: inherit;
        text-decoration: underline;

        &:hover {
          background: rgba(#fff, 0.2);
        }
      }

      &__title {
        margin-bottom: 0.5rem;
        font-size: 150%;
      }
    }
  }

  .notification-list-enter-active, .notification-list-leave-active {
    transition: all 1s;
  }
  .notification-list-enter, .notification-list-leave-to {
    opacity: 0;
  }
  .notification-leave-active {
    position: absolute;
  }

</style>
<template>
  <div
    class="notifications"
  >
    <transition-group
      name="notification-list"
      tag="div"
    >
      <div
        v-for="notification in notifications"
        :key="`notification-${notification.uuid}`"
        class="notification"
        @click="click(notification)"
      >
        <div
          v-if="notification.title"
          class="notification__title"
        >
          {{ notification.title }}
        </div>
        <!-- eslint-disable vue/no-v-html -->
        <div
          v-if="notification.body"
          class="notification__body"
          v-html="notification.body"
        />
      </div>
    </transition-group>
  </div>
</template>
