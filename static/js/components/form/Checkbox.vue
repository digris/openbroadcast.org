<script>

  export default {
    name: 'Checkbox',
    model: {
      prop: 'model',
      event: 'change'
    },
    props: {
      id: {
        type: String,
        default: undefined
      },
      model: {
        type: [Boolean, Array],
        default: undefined
      },
      checked: {
        type: Boolean,
        default: false
      },
      required: {
        type: Boolean,
        default: false
      },
      disabled: {
        type: Boolean,
        default: false
      },
      value: {
        type: [String, Boolean, Number, Object, Array, Function],
        default: undefined
      },
      name: {
        type: String,
        default: undefined,
      },
      color: {
        type: String,
        default: undefined,
      },
      size: {
        type: Number,
        default: undefined,
      },
      fontSize: {
        type: Number,
        default: undefined,
      },
    },
    data() {
      return {
        uniqueId: '',
        lv: this.model
      }
    },
    computed: {
      checkboxState() {
        if (Array.isArray(this.model)) return this.model.indexOf(this.value) !== -1
        return this.model || Boolean(this.lv)
      },
      classes() {
        return {
          'disabled': this.disabled,
          'active': this.checkboxState
        }
      },
      mainStyle() {
        return this.checkboxState
          ? this.color && `background-color: ${this.color}; border-color: ${this.color};`
          : ''
      },
      sizeStyles() {
        return this.size
          ? `width: ${this.size}px; height: ${this.size}px; `
          : ''
      },
      fontSizeStyles() {
        return this.fontSize
          ? `font-size: ${this.fontSize}px`
          : ''
      }
    },
    watch: {
      checked(v) {
        if (v !== this.checkboxState) this.toggle()
      },
      model(v) {
        this.lv = v
      }
    },
    mounted() {
      this.genId()

      if (this.checked && !this.checkboxState) {
        this.toggle()
      }
    },
    methods: {
      toggle() {
        if(this.disabled) return

        let v = this.model || this.lv

        if (Array.isArray(v)) {
          const i = v.indexOf(this.value)
          if (i === -1) v.push(this.value)
          else v.splice(i, 1)
        }
        else v = !v
        this.lv = v
        this.$emit('change', v, this.value)
      },

      genId() {
        if (this.id === undefined || typeof String) {
          this.uniqueId = `m-checkbox--${Math.random().toString(36).substring(2,10)}`
        }
        else {
          this.uniqueId = this.id
        }
      }
    }
  }
</script>

<template>
  <div
    class="m-chckbox--container"
    :class="[classes]"
  >
    <div
      class="m-chckbox--group"
      :style="mainStyle + sizeStyles"
      @click="toggle"
    >
      <div v-if="checkboxState">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="#fff"
          viewBox="0 0 24 24"
        >
          <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
        </svg>
      </div>
      <div
        class="m-chckbox--ripple"
      >
        <input
          :id="id || uniqueId"
          type="checkbox"
          :name="name"
          :value="value"
          :disabled="disabled"
          :required="required"
          :color="color"
          :checked="checkboxState"
        >
      </div>
    </div>
    <label
      :style="fontSizeStyles"
      class="m-chckbox--label"
      :for="id || uniqueId"
    >
      <slot />
    </label>
  </div>
</template>

<style lang="scss">
  .m-chckbox--container {
    position: relative;

    display: inline-flex;
    align-items: center;

    line-height: 20px;

    cursor: pointer;
  }

  .m-chckbox--label {
    position: relative;

    padding-left: 0.5em;

    cursor: pointer;
  }
  .m-chckbox--group {
    position: relative;

    box-sizing: border-box;
    width: 20px;
    height: 20px;

    border: 2px solid rgba(0,0,0,0.54);
    border-radius: 2px;

    transition: 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    input[type=checkbox] {
      position: absolute;
      left: -999rem;

      -webkit-appearance: none;
      appearance: none;
    }
  }
  .m-chckbox--container.active {
    .m-chckbox--group {
      background-color: var(--primary-color);
      border-color: var(--primary-color);
    }
  }
  .m-chckbox--container.disabled {
    cursor: not-allowed;
    .m-chckbox--group {
      opacity: 0.14;
    }
    .m-chckbox--label {
      cursor: not-allowed;
      opacity: 0.24;
    }
  }
</style>
