<script>
import { EventBus } from '../../eventBus';
import PlayButtonPlaying from './PlayButtonPlaying.vue';

export default {
  name: 'PlayButton',
  components: {
    // 'loading-icon': PlayButtonLoading,
    'playing-icon': PlayButtonPlaying,
  },
  props: {
    action: {
      type: Object,
      required: true,
    },
    state: {
      type: String,
      default: 'stopped',
    },
    scale: {
      type: Number,
      default: 1,
    },
    size: {
      type: Number,
      default: 24,
    },
    color: {
      type: String,
      default: '#00bb73',
    },
    hoverColor: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      isHover: false,
    };
  },
  computed: {
    iconColor() {
      return (this.isHover && this.hoverColor) ? this.hoverColor : this.color;
    },
    style() {
      return {
        transform: `scale(${this.scale})`,
        cursor: (this.isLoading) ? 'wait' : 'pointer',
        fill: this.iconColor,
      };
    },
    isPlaying() {
      return this.state === 'playing';
    },
    isLoading() {
      return this.state === 'loading';
    },
    isStopped() {
      return !(this.isPlaying || this.isLoading);
    },
  },
  methods: {
    click() {
      // this.$emit((this.isPlaying) ? 'stop' : 'play');
      EventBus.$emit('action', this.action);
    },
  },
};
</script>
<template>
  <div
    class="play-button"
    :style="style"
    @mouseover="isHover=true"
    @mouseleave="isHover=false"
    @click.prevent="click"
  >
    <playing-icon
      v-if="(isPlaying || isLoading)"
      class="icon--playing"
      :style="{ transform: `scale(${size / 24})`}"
      :color="iconColor"
      :is-playing="isPlaying"
      :is-loading="isLoading"
    />
    <!--
        <loading-icon
            class="icon--loading"
            :style="{ transform: `scale(${size / 24})`}"
            :color="iconColor"
            v-if="isLoading"
        ></loading-icon>
        -->
    <div
      v-if="isStopped"
      class="icon--stopped"
      :style="{ width: `${size}px`, height: `${size}px`}"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <path d="M8 5v14l11-7z" />
      </svg>
    </div>
    <div
      class="touch-area"
    />
  </div>
</template>
<style lang="scss" scoped>
  .play-button {
    position: relative;

    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;

    .icon {
      &--stopped {
        position: relative;

        width: inherit;
        height: inherit;
        svg {
          position: absolute;

          width: inherit;
          height: inherit;
        }
      }
    }

    .touch-area {
      position: absolute;

      width: 50px;
      height: 50px;

      background: rgba(0, 0, 0, 0);
      border-radius: 50%;
    }
  }
</style>
