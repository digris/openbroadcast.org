<script>
import APIClient from 'src/api/caseTranslatingClient';
import debounce from 'debounce';

import ObjectSearchResult from './ObjectSearchResult.vue';

const API_SEARCH_URL = '/api/v2/search/global/';
const INPUT_DEBOUNCE = 300;
const MIN_QUERY_CHARS = 3;

export default {
  name: 'ObjectSearch',
  components: {
    'search-result': ObjectSearchResult,
  },
  data() {
    return {
      searchQuery: '',
      results: [],
      total: 0,
      url: API_SEARCH_URL,
    };
  },
  methods: {
    updateSearchQuery(e) {
      const q = e.target.value;
      this.searchQuery = q;
      if (q.length < MIN_QUERY_CHARS) {
        this.updateResults({ results: [], total: 0 });
        return;
      }
      const query = {
        q,
        fuzzy: 0,
        ct: 'alibrary.media',
      };
      this.search(query);
    },
    // eslint-disable-next-line func-names
    search: debounce(function (query) {
      const params = query;
      APIClient.get(this.url, { params }).then((response) => {
        const { results } = response.data;
        const { total } = response.data;
        this.updateResults({ results, total });
      });
    }, INPUT_DEBOUNCE),
    updateResults({ results, total }) {
      this.results = results;
      this.total = total;
    },
  },
};
</script>
<template>
  <div class="object-search">
    <input
      v-model="searchQuery"
      class="object-search__input"
      @input="updateSearchQuery"
    >
    <div>{{ total }}</div>
    <div>
      <search-result
        v-for="result in results"
        :key="`${result.ct}:${result.uuid}`"
        :ct="result.ct"
        :obj="result"
      >
        {{ result.name }}
      </search-result>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .object-search {
    color: white;

    background: orangered;
  }
</style>
