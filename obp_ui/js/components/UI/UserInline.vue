<script>

import Visual from './Visual.vue';

export default {
  name: 'UserInline',
  components: {
    visual: Visual,
  },
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      detailsVisible: false,
    };
  },
  methods: {
    mouseover() {
      this.detailsVisible = true;
    },
    mouseleave() {
      this.detailsVisible = false;
    },
  },
};
</script>
<style lang="scss" scoped>
    .user-inline {
      position: relative;
      display: inline-block;

      a {
        color: inherit;
      }
    }

    .user-info {
      position: absolute;
      display: flex;
      width: 200px;
      color: #222;
      background: #fff;
      box-shadow: 2px 2px 2px 2px rgba(#000, 0.1);

      &__visual {
        width: 48px;

        figure {
          height: 48px;
        }
      }

      &__details {
        padding: 4px 6px;
        white-space: nowrap;
      }
    }

</style>
<template>
  <div
    class="user-inline"
  >
    <div
      @mouseover="mouseover"
      @mouseleave="mouseleave"
    >
      <a
        :href="user.detailUrl"
        target="_blank"
        class="user-inline__display-name"
      >{{ user.displayName }}</a>
    </div>
    <div
      v-if="detailsVisible"
      class="user-info"
    >
      <div
        class="user-info__visual"
      >
        <visual :url="user.image" />
      </div>
      <div
        class="user-info__details"
      >
        <div>
          {{ user.displayName }} <span v-if="user.country">{{ user.country }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
