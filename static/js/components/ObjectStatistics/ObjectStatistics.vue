<script>
import APIClient from '../../api/caseTranslatingClient';
import Chart from './Chart';

const API_URL = '/api/v2/statistics/usage-statistics/';

const TITLE_MAP = {
  airplay: 'Airlays',
  stream: 'Plays',
  download: 'Downloads',
};

const COLOR_MAP = {
  default: '#a5a5a5',
  playout: '#6633cc',
  stream: '#00bb73',
  download: '#00a2e2',
};

const annotateDatasets = (datasets) => datasets.map((ds) => {
    const dataset = { ...ds };
    dataset.label = TITLE_MAP[dataset.label] || ds.label;
    dataset.backgroundColor = COLOR_MAP[ds.label] || COLOR_MAP.default;
    return dataset;
  });

export default {
  components: {
    Chart,
  },
  props: {
    objCt: {
      type: String,
      required: true,
    },
    objUuid: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      data: null,
    };
  },
  computed: {
    url() {
      return `${API_URL}${this.objCt}:${this.objUuid}/`;
    },
    parsedData() {
      if (!this.data) {
        return null;
      }
      const { labels, datasets } = this.data;
      return {
        labels,
        datasets: annotateDatasets(datasets),
      };
    },
  },
  mounted() {
    APIClient.get(this.url).then((response) => {
        console.debug(response.data);
        this.data = response.data;
      });
  },
};
</script>

<template>
  <div class="chart">
    <chart :chart-data="parsedData" />
  </div>
</template>
