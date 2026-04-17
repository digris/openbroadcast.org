<script>
export default {
  name: 'PlayButtonPlaying',
  props: {
    color: {
      type: String,
      default: '#fff',
    },
    isPlaying: {
      type: Boolean,
      default: false,
    },
    isLoading: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      size: 24,
    };
  },
  computed: {
    style() {
      return {
        background: this.color,
      };
    },
  },
};
</script>
<style lang="scss" scoped>

  svg {
    transform: rotate(180deg);
  }

  @keyframes playing {
    0%, 80%, 100% {
      height: 4px;
      // y: 5px;
    }
    20% {
      height: 14px;
    }
    40% {
      height: 9px;
    }
    60% {
      height: 11px;
    }
  }

  .playing {
    svg {
      rect {
        transition: animation 1s;
        animation: playing 1.3s infinite;
        &:nth-child(1n) {
          animation-delay: 100ms;
        }
        &:nth-child(2n) {
          animation-delay: -400ms;
        }
        &:nth-child(3n) {
          animation-delay: -490ms;
        }
        &:nth-child(4n) {
          animation-delay: -600ms;
        }
        &:nth-child(5n) {
          animation-delay: -200ms;
        }
      }
    }
  }

  @keyframes loading {
    0%, 40%, 100% {
      height: 4px;
      y: 10px;
    }
    20% {
      height: 14px;
      y: 5px;
    }
  }

  .loading {
    svg {
      rect {
        transition: animation 1s;
        animation: loading 1.3s infinite ease-in-out;
        &:nth-child(1n) {
          animation-delay: -700ms;
        }
        &:nth-child(2n) {
          animation-delay: -800ms;
        }
        &:nth-child(3n) {
          animation-delay: -900ms;
        }
        &:nth-child(4n) {
          animation-delay: -1000ms;
        }
        &:nth-child(5n) {
          animation-delay: -1100ms;
        }
      }
    }
  }

</style>
<template>
  <div
    class="playing-icon"
    :class="{ playing: isPlaying, loading: isLoading }"
    :style="{ width: `${size}px`, height: `${size}px`}"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
    >
      <rect
        x="5"
        y="5"
        width="2"
        height="2"
      />
      <rect
        x="8"
        y="5"
        width="2"
        height="2"
      />
      <rect
        x="11"
        y="5"
        width="2"
        height="2"
      />
      <rect
        x="14"
        y="5"
        width="2"
        height="2"
      />
      <rect
        x="17"
        y="5"
        width="2"
        height="2"
      />
    </svg>
  </div>
</template>
