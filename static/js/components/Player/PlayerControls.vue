<script>

const DEBUG = true;

export default {
  name: 'PlayerControls',
  props: {
    hasNext: {
      type: Boolean,
      default: false,
    },
    hasPrevious: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    play() {
      if (DEBUG) console.debug('play');
        this.$emit('play');
    },
    previous() {
      if (DEBUG) console.debug('previous');
      if(this.hasPrevious) {
        console.debug('has previous - emitting event');
        this.$emit('previous');
      }
    },
    next() {
      if (DEBUG) console.debug('next');
      if(this.hasNext) {
        console.debug('has next - emitting event');
        this.$emit('next');
      }
    },
  }
};
</script>
<template>
  <div class="controls">
    <span
      class="action"
      :class="{ 'action--disabled': (!hasPrevious) }"
      @click.prevent="previous"
    >
      <i class="icn icn-skip-previous" />
    </span>
    <span
      class="action"
      @click.prevent="play"
    >
      <i class="icn icn-pause" />
    </span>
    <span
      class="action"
      @click.prevent="play"
    >
      <i class="icn icn-play-arrow" />
    </span>
    <span
      class="action"
      :class="{ 'action--disabled': (!hasNext) }"
      @click.prevent="next"
    >
      <i class="icn icn-skip-next" />
    </span>
  </div>
</template>
<style lang="scss" scoped>
  .controls {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .action {
    margin: 0 .25rem;

    color: $dark-grey;
    font-size: 36px;

    // background: red;
    border-radius: 50%;

    cursor: pointer;

    transition: color 120ms, background 60ms, transform 60ms;
    &--disabled {
      cursor: not-allowed;
      opacity: 0.5;
    }

    &:hover:not(&--disabled) {
      color: $white;

      background: $secondary-color;
      transform: scale(1.1);
    }

  }
</style>
