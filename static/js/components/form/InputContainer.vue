<script>
    export default {
        name: 'InputContainer',
        props: {
            id: {
                type: String,
                required: true,
            },
            required: {
                type: Boolean,
                required: false,
                default: false,
            },
            label: {
                type: String,
                required: false,
                default: null,
            },
            hideLabel: {
                type: String,
                required: false,
                default: null,
            },
            errors: {
                type: Array,
                required: false,
                default: function () {
                    return [];
                },
            },
            help: {
                type: String,
                required: false,
                default: null,
            },
            isCheckbox: {
                type: Boolean,
                required: false,
                default: false,
            },
        },
        computed: {
            hasErrors: function () {
                return (this.errors && this.errors.length);
            }
        },
        methods: {},
    }
</script>
<template>
  <div
    :class="{'has-error': hasErrors, 'is-checkbox': isCheckbox, 'no-label': hideLabel}"
    class="input-container"
  >
    <div
      v-if="(!hideLabel && label)"
      class="label"
      :for="id"
    >
      {{ label }}
      <span
        v-if="required"
        class="label__required"
      >*</span>
    </div>
    <div class="field">
      <slot name="default" />
    </div>
    <div class="appendix">
      <div
        v-if="hasErrors"
        class="errors"
      >
        <p
          v-for="(error, index) in errors"
          :key="(index + error.code)"
        >
          {{ error.message }}
        </p>
      </div>
      <p
        v-if="help"
        class="help"
      >
        {{ help }}
      </p>
    </div>
  </div>
</template>
<style lang="scss" scoped>

    @import '../../../style/abstracts/variables';
    @import '../../../style/components/form';

    .input-container {
        @include input-container-grid;
    }

</style>
