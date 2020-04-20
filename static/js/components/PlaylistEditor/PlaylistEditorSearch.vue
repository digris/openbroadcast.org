<script>

// import PlayerListItem from './PlayerListItem.vue';
import debounce from 'debounce';

import Checkbox from '../Form/Checkbox.vue';
import APIClient from "../../api/caseTranslatingClient";

import PlaylistEditorSearchResult from './PlaylistEditorSearchResult.vue';

export default {
  name: 'PlaylistEditorSearch',
  components: {
    'search-result': PlaylistEditorSearchResult,
    'checkbox': Checkbox,
  },
  props: {
    items: {
      type: Array,
      required: false,
      default() {
        return [];
      },
    },
  },
  data() {
    return {
      isOpen: false,
      results: [],
      query: '',
      filterType: ['Jingle'],
      isLoading: false,
      arrowCounter: -1,
    };
  },
  watch: {
    filterType(type) {
      this.getResults(this.query);
    },
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  destroyed() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    onChange() {
      this.getResults(this.query)
    },

    getResults: debounce(function (q) {
      const url = '/api/v2/search/global/';
      let params = {
        q: q,
        fuzzy: 0,
        ct: 'alibrary.media',
        filter_type: this.filterType.join(','),
      };
      APIClient.get(url, { params }).then((response) => {
        this.results = response.data.results;
      }).catch(() => {
        this.results = [];
      });
    }, 200),

    selectResult(result) {
      this.arrowCounter = -1;
      this.isOpen = false;
      // this.$emit('result', result);
      this.query = '';
      this.results = [];

      console.debug('selected result', result);

      // this.addMediaToPlaylist(result);

      this.$emit('select', result);

    },
    onArrowDown(evt) {
      if (this.arrowCounter < this.results.length) {
        this.arrowCounter = this.arrowCounter + 1;
      }
    },
    onArrowUp() {
      if (this.arrowCounter > 0) {
        this.arrowCounter = this.arrowCounter - 1;
      }
    },
    onEnter() {
      // no result from autocomplete
      if (this.arrowCounter < 0) {
        this.selectResult(this.search);
      } else {
        this.selectResult(this.results[this.arrowCounter]);
      }
    },
    handleClickOutside(evt) {
      if (!this.$el.contains(evt.target)) {
        this.isOpen = false;
        this.arrowCounter = -1;
      }
    },
  },
};
</script>
<style lang="scss" scoped>
  .playlist-editor-search {
    position: relative;

    background: white;

    .search-input-container {

      display: grid;
      grid-column-gap: 10px;
      grid-template-columns: 50% auto;

      padding: 4px;

    }

    .search-result-container {
      // position: absolute;
      // z-index: 99;
    }

    .search-input {
      width: 100%;
      padding: 10px 4px;
    }

    .search-options {
      display: flex;
      align-items: center;
      justify-content: flex-end;
    }

  }
</style>
<template>
  <div class="playlist-editor-search">
    <div class="search-input-container">
      <input
        v-model="query"
        class="search-input search-input--query"
        type="text"
        maxlength="50"
        placeholder="Search"
        @input="onChange"
        @keydown.down.prevent="onArrowDown"
        @keydown.up.prevent="onArrowUp"
        @keydown.enter.prevent="onEnter"
      >
      <div class="search-options">
        <checkbox
          v-model="filterType"
          value="Jingle"
        >
          Search for jingles only
        </checkbox>
      </div>
    </div>
    <div class="search-result-container">
      <search-result
        v-for="(result, i) in results"
        :key="`search-result-${i}`"
        :media="result"
        :is-active="(i === arrowCounter)"
        @click="selectResult(result)"
      />
    </div>
  </div>
</template>
