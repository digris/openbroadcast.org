<script>


import Visual from './Visual.vue';
import Tags from './Tags.vue';

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
      display: inline-block;
      position: relative;

      a {
        color: inherit;
      }
    }

    .user-info {
      background: #fff;
      color: #222;
      position: absolute;
      width: 200px;
      display: flex;
      box-shadow: 2px 2px 2px 2px rgba(#000, 0.1);

      &__visual {
        width: 48px;

        figure {
          height: 48px;
        }
      }

      &__details {
        white-space: nowrap;
        padding: 4px 6px;
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
