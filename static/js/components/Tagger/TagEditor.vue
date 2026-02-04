<script>
const DEBUG = true;

const { tagsByCategories } = require('./tagsByCategories');

// Normalize tag for comparisons
function normalizeTag(s) {
  return (s || '').trim().toLowerCase();
}

export default {
  name: 'TagEditor',
  props: {},
  data() {
    return {
      tags: [],
      tagsByCategories,
      t: null, // not used (Tag-it handle)
      isInitialized: false,
      isTagsPanelOpen: false,
    };
  },
  computed: {
    normalizedTags() {
      return this.tags.map(normalizeTag);
    },
  },
  mounted() {
    if (DEBUG) console.debug('TagEditor - mounted');

    this.t = window.jQuery('#id_d_tags');

    // NOTE: initTag is called on first time panel is opened
    // setTimeout(() => {
    //   this.initTagit();
    // }, 2000);
  },
  methods: {

    initTagit() {
      console.debug('init tagit');
      if (this.isInitialized) {
        return;
      }

      // Load initial tags from Tag-it
      try {
        this.tags = this.t.tagit('assignedTags') || [];
      } catch (err) {
        console.warn(err);
        return;
      }

      // Tag-it callbacks (arrow funcs preserve Vue `this`)
      this.t.tagit({
        afterTagAdded: (e, ui) => {
          // Skip tags Tag-it adds during its own initialization
          if (ui?.duringInitialization) return;
          const value = ui.tagLabel;
          if (!this.tags.includes(value)) {
            this.tags.push(value);
          }
        },
        afterTagRemoved: (e, ui) => {
          const value = ui.tagLabel;
          this.tags = this.tags.filter((t) => t !== value);
        },
      });

      this.isInitialize = true;
    },

    isTagSelected(value) {
      return this.normalizedTags.includes(normalizeTag(value));
    },

    syncTagsToTagIt() {
      const tagItTags = this.t.tagit('assignedTags') || [];
      const tagItTagsNorm = tagItTags.map(normalizeTag);

      // Add missing
      this.tags.forEach((t) => {
        if (!tagItTagsNorm.includes(normalizeTag(t))) {
          this.t.tagit('createTag', t);
        }
      });

      // Remove extras
      tagItTags.forEach((t) => {
        if (!this.normalizedTags.includes(normalizeTag(t))) {
          this.t.tagit('removeTagByLabel', t);
        }
      });
    },

    handleTogglePanelVisibility() {
      this.isTagsPanelOpen = !this.isTagsPanelOpen;
      if (this.isTagsPanelOpen) {
        this.initTagit();
      }
    },

    handleAddTag(value) {
      if (!value || this.isTagSelected(value)) return;
      this.tags.push(value);
      this.syncTagsToTagIt();
    },

    handleRemoveTag(value) {
      if (!value) return;

      const normTag = normalizeTag(value);
      const updatedTags = this.tags.filter((t) => normalizeTag(t) !== normTag);

      if (updatedTags.length === this.tags.length) return;

      this.tags = updatedTags;
      this.syncTagsToTagIt();
    },
  },
};
</script>

<template>
  <div class="tag-editor">
    <div class="te-header">
      <button
        type="button"
        class="te-toggle-btn"
        :aria-expanded="isTagsPanelOpen.toString()"
        @click="handleTogglePanelVisibility"
      >
        Tags by Category
        <span
          class="te-toggle-caret"
          aria-hidden="true"
        />
      </button>
    </div>

    <div
      class="te-panel"
      :class="{'is-open': isTagsPanelOpen}"
    >
      <div
        v-for="(cat, i) in tagsByCategories"
        :key="i"
        :class="['te-category', 'clearfix', 'control-group', `te-category--${cat.key}`]"
      >
        <div class="te-category-label control-label">
          {{ cat.title }}
          <span
            v-if="cat.subTitle"
            class="te-category-subtitle"
          >
            {{ cat.subTitle }}
          </span>
        </div>

        <div class="te-tag-list controls field-lookup">
          <button
            v-for="tag in cat.tags"
            :key="tag"
            type="button"
            class="te-tag-btn"
            :class="{ 'is-selected': isTagSelected(tag)}"
            @click="isTagSelected(tag) ? handleRemoveTag(tag) : handleAddTag(tag)"
          >
            {{ tag }}
          </button>
        </div>
      </div>
    </div>
    <!--    <pre v-text="{tags}" />-->
  </div>
</template>

<style lang="scss" scoped>
/* See TagList component + new colors for missing ones */
$cat-colors: (
  genre: red,
  mood: #00bb73,
  descriptive: #008cd7,
  daypart: #f39c12,
  activity: #d42d89,
  instrument: #f5d300,
  type: #a97142,
);

.tag-editor {
  .te-header {
    margin: 8px 0;

    .te-toggle-btn {
      display: inline-flex;
      gap: 6px;
      align-items: center;
      padding: 0;
      color: rgb(102, 51, 204);
      font-weight: 400;
      background: none;
      border: 0;
      cursor: pointer;

      &:hover {
        text-decoration: underline;
      }

      .te-toggle-caret {
        width: 0;
        height: 0;
        margin-left: 2px;
        border-right: 5px solid transparent;
        border-bottom: 6px solid currentColor;
        border-left: 5px solid transparent;
        transition: border-top .2s ease, border-bottom .2s ease;
      }

      &[aria-expanded="false"] .te-toggle-caret {
        border-top: 6px solid currentColor;
        border-bottom: 0;
      }
    }
  }

  .te-panel {
    max-height: 0;
    overflow: hidden;
    visibility: hidden;
    opacity: 0;
    transition: max-height 200ms ease,
      opacity 180ms ease,
      visibility 0s linear 200ms;
    pointer-events: none;

    &.is-open {
      max-height: 1000px;
      visibility: visible;
      opacity: 1;
      transition: max-height 220ms ease,
        opacity 180ms ease,
        visibility 0s;
      pointer-events: auto;
    }
  }

  .te-category {
    margin-top: 12px;

    .te-category-label {
      display: flex;
      flex-direction: column;
      font-weight: 400;

      .te-category-subtitle {
        color: gray;
        font-size: 11px;
      }
    }

    .te-tag-list {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;

      .te-tag-btn {
        display: inline-flex;
        padding: 6px 6px 4px 6px;
        color: #555;
        font-size: 90%;
        text-transform: uppercase;
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-left: 2px solid #5f529a;

        &.is-selected {
          background-color: #d2f6e7;
        }

        &:hover {
          background: #e2f8f0;
        }
      }
    }

    @each $k, $c in $cat-colors {
      &--#{$k} .te-tag-list .te-tag-btn {
        border-left-color: $c;
      }
    }
  }
}
</style>
