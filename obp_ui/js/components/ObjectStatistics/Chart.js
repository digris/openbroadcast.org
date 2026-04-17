import { Bar, mixins } from 'vue-chartjs';

const { reactiveProp } = mixins;

export default {
  extends: Bar,
  mixins: [reactiveProp],
  data: () => ({
    options: {
      responsive: true,
      maintainAspectRatio: false,
      aspectRatio: 0.5,
      stacked: false,
      height: '100px',
      animation: {
        duration: 0,
      },
      scales: {
        xAxes: [{
          // stacked: true,
          gridLines: {
              offsetGridLines: true,
          },
        }],
        yAxes: [{
          // stacked: true,
          ticks: {
            beginAtZero: true,
          },
        }],
      },
      legend: {
        labels: {
          fontColor: 'black',
        },
      },
    },
  }),
  props: {
    chartData: {
      type: Object,
      default: null,
    },
    // options: {
    //   type: Object,
    //   default: null,
    // },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
