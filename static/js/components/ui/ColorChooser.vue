<script>

export default {
  name: 'ColorChooser',
  props: {
    colors: {
      type: Object,
      required: true,
    },
    selectedColor: {
      type: Number,
      default: 0,
    },
    width: {
      type: Number,
      default: 16,
    },
    height: {
      type: Number,
      default: 16,
    },
    optionWidth: {
      type: Number,
      default: null,
    },
    optionHeight: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      optionsVisible: false,
    };
  },
  computed: {
    colorOptions() {
      const options = [];
      for (const index in this.colors) {
        options.push({
          index,
          value: this.colors[index],
          style: {
            width: `${this.optionWidth || this.width}px`,
            height: `${this.optionHeight || this.height}px`,
            background: this.colors[index],
            border: `1px solid ${this.colors[index]}`,
          },
        });
      }
      return options;
    },
    style() {
      return {
        width: `${this.width}px`,
        height: `${this.height}px`,
        background: this.colors[this.selectedColor],
      };
    },
  },
  methods: {
    mouseover() {
      this.optionsVisible = true;
    },
    mouseleave() {
      this.optionsVisible = false;
    },
    selectColor(index) {
      this.$emit('select', index);
      this.optionsVisible = false;
    },
  },
};
</script>
<style lang="scss" scoped>
    .color-chooser {
      display: inline-block;
      position: relative;
      cursor: pointer;

      &__options {
        position: absolute;
        z-index: 999;

        &__option {
          margin: 4px 0 0 0;
          cursor: pointer;

          &:hover {
            border-color: #63c !important;
          }
        }
      }
    }
</style>
<template>
  <div
    class="color-chooser"
  >
    <div
      :style="style"
      @mouseover="mouseover"
      @mouseleave="mouseleave"
    >
      <div
        v-if="optionsVisible"
        :style="{top: height + 'px'}"
        class="color-chooser__options"
      >
        <div
          v-for="color in colorOptions"
          :key="`${color.value}-${color.index}`"
          :style="color.style"
          class="color-chooser__options__option"
          @click="selectColor(color.index)"
        />
      </div>
    </div>
  </div>
</template>
