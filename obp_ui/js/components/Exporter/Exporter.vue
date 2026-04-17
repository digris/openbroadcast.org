<script>

import LayoutBase from '../../templates/LayoutBase.vue';
import ExporterItem from './ExporterItem.vue';

const UPDATE_INTERVAL = 5000;

export default {
  name: 'Exporter',
  components: {
    'layout-base': LayoutBase,
    'exporter-item': ExporterItem,
  },
  directives: {},
  data() {
    return {
      calendarWidth: 0,
      termsAccepted: false,
    };
  },
  computed: {
    isLocked() {
      return this.$store.getters['exporter/isLocked'];
    },
    exports() {
      return this.$store.getters['exporter/exports'];
    },
  },
  mounted() {
    this.$store.dispatch('exporter/loadExports');
    setInterval(() => {
      if (this.isLocked) {
        console.warn('locked');
        return;
      }
      this.$store.dispatch('exporter/loadExports');
    }, UPDATE_INTERVAL);
  },
  methods: {
    acceptTerms() {
      this.termsAccepted = true;
    },
    archiveExports(limitStatus) {
      const status = limitStatus || null;
      this.$store.dispatch('exporter/archiveExports', status);
    },
  },
};
</script>

<template>
  <layout-base>
    <div>
      <div class="item--header">
        <div class="header__primary">
          <div class="title title--primary">
            <h2>Download</h2>
          </div>
          <div class="meta">
            <p>By clicking "Accept Terms & Conditions", you agree to our "<a href="/about/terms-and-conditions/">Terms
              and Conditions</a>"&nbsp;and that you have read our documentation&nbsp;and understand how downloading
              works.</p>
          </div>
          <div class="actions">
            <a
              class="button action"
              @click="acceptTerms"
            >Accept Terms & Conditions</a>
          </div>
        </div>
      </div>

      <div
        class="export-list"
        :class="{'is-locked': (!termsAccepted)}"
      >
        <exporter-item
          v-for="item in exports"
          :item="item"
          :key="item.uuid"
        />
      </div>
    </div>
    <template v-slot:sidebar>
      <div class="menu-context">
        <div class="action-group">
          <ul>
            <li class="action is-enabled">
              <a
                @click.prevent="archiveExports()"
              >Archive All</a>
            </li>
            <li class="action is-enabled">
              <a
                @click.prevent="archiveExports(4)"
              >Archive Downloaded</a>
            </li>
          </ul>
        </div>
      </div>
    </template>
  </layout-base>
</template>

<style lang="scss" scoped>
.export-list {
  margin: 2rem 0;
  &.is-locked {
    cursor: not-allowed;
    opacity: 0.5;
    filter: grayscale(100%);
    .item {
      pointer-events: none;
    }
  }
}
.actions {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
</style>
