<script>

import LayoutBase from '../../templates/LayoutBase.vue';

export default {
  name: 'Exporter',
  components: {
    'layout-base': LayoutBase,
  },
  directives: {},
  data() {
    return {
      calendarWidth: 0,
      termsAccepted: false,
    };
  },
  computed: {
    exports() {
      return this.$store.getters['exporter/exports'];
    }
  },
  mounted() {
    this.$store.dispatch('exporter/loadExports');
  },
  methods: {
    acceptTerms() {
      this.termsAccepted = true;
    }
  }
};
</script>

<style lang="scss" scoped>
    .calendar-navigation {
      margin-bottom: 24px;
    }
</style>

<template>
  <layout-base>
    <div>
      <div class="item--header">
        <div class="header__primary">
          <div class="title title--primary">
            <h2>Terms and Conditions</h2>
          </div>
          <div class="meta">
            <p>By clicking "Accept Terms & Conditions", you agree to our "<a href="/about/terms-and-conditions/">Terms and Conditions</a>"&nbsp;and that you have read our documentation&nbsp;and understand how downloading works.</p>
          </div>
          <div class="actions">
            <a
              class="button action"
              @click="acceptTerms"
            >Accept Terms & Conditions</a>
          </div>
        </div>
      </div>

      <div>
        termsAccepted: {{ termsAccepted }}<br>
        {{ exports }}
      </div>
    </div>
    <template v-slot:sidebar>
      <div>
        (( sidebar ))
      </div>
    </template>
  </layout-base>
</template>
