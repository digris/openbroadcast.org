<script>

import APIClient from '../../api/caseTranslatingClient';
import TagInputAutocomplete from './TagInputAutocomplete.vue';

export default {
  name: 'TagInputContainer',
  components: {
    'input-autocomplete': TagInputAutocomplete,
  },
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
      default() {
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
  data() {
    return {
      tags: [],
      newTag: '',
      maxTags: 3,
      suggestedTags: [],
      validationErrors: [],
    };
  },
  computed: {
    combinedErrors() {
      return [...this.errors, ...this.validationErrors];
    },
    hasErrors() {
      return (this.combinedErrors && this.combinedErrors.length);
    },
  },
  watch: {
    tags(tags) {
      if (tags.length > this.maxTags) {
        this.validationErrors.push({
          code: 'max-tags',
          message: `A maximum of ${this.maxTags} tags are allowed.`,
        });
      } else {
        this.validationErrors = [];
        this.writeTagsToInput();
      }
    },
  },
  mounted() {
    this.readTagsFromInput();
  },
  methods: {
    removeTag(index) {
      const tags = [...this.tags];
      tags.splice(index, 1);
      this.tags = tags;
    },
    autocomleteInput(input) {
      const url = '/api/v2/tags/tag/';
      const params = {
        q: input,
      };
      APIClient.get(url, { params }).then((response) => {
        this.suggestedTags = response.data.results;
      }).catch(() => {
        this.suggestedTags = [];
      });
    },
    autocompleteResult(result) {
      console.debug('autocompleteResult', result);
      this.tags.unshift(result);
    },
    readTagsFromInput() {
      // console.debug('this.$refs', this.$refs);
      const input = this.$refs.field.querySelector('input');
      this.tags = input.value.split(',');
    },
    writeTagsToInput() {
      const input = this.$refs.field.querySelector('input');
      // input.value = this.tags.join(",");
      input.value = this.tags.map((tag) => `"${tag}"`).join(',');
    },
  },
};
</script>
<template>
  <div
    :class="{'has-error': hasErrors, 'no-label': hideLabel}"
    class="input-container input-container--tag"
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

    <div
      ref="field"
      class="raw-field"
      style="display: none;"
    >
      <slot name="default" />
    </div>

    <div class="field input-container__input">
      <input-autocomplete
        class="input-container__autocomplete"
        :is-async="true"
        :items="suggestedTags"
        @input="autocomleteInput"
        @result="autocompleteResult"
      />
      <div class="input-container__tags">
        <span
          v-for="(tag, index) in tags"
          :key="`tag-${index}`"
          class="tag"
        >
          {{ tag }}
          <span
            class="tag__remove"
            @click="removeTag(index)"
          >x</span>
        </span>
      </div>
    </div>

    <div class="appendix">
      <div
        v-if="hasErrors"
        class="errors"
      >
        <p
          v-for="(error, index) in combinedErrors"
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

      &__input {
        display: flex;
        min-height: 100px;
      }

      &__autocomplete {
        padding-right: 4px;
        width: 220px;
      }

      &__tags {
        flex-grow: 1;
      }
    }

    .tag {
      display: inline-flex;
      height: 22px;
      line-height: 22px;
      background: black;
      margin: 0 4px 4px 0;
      padding: 0 10px;
      text-transform: uppercase;
      color: white;

      &__remove {
        padding: 0 0 0 0.5rem;
        color: white;
        cursor: pointer;
        opacity: 0.5;

        &:hover {
          opacity: 1;
        }
      }
    }

</style>
