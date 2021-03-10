<script>
import Intersect from 'vue-intersect';

export default {
  name: 'MediaAppearances',
  components: {
    intersect: Intersect,
  },
  props: {
    objUuid: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      detailsVisible: false,
      loadingStarted: false,
    };
  },
  computed: {
    appearances() {
      return this.$store.getters['library/mediaAppearancesByUuid'](this.objUuid);
    },
    pub() {
      return this.appearances.public || 0;
    },
    broadcast() {
      return this.appearances.broadcast || 0;
    },
    broadcastUnpublished() {
      return this.appearances.broadcastUnpublished || 0;
    },
    hasAppearances() {
      return (this.pub + this.broadcast + this.broadcastUnpublished > 0);
    },
  },
  methods: {
    onEnter() {
      if (!this.loadingStarted) {
        this.loadAppearances();
        this.loadingStarted = true;
      }
    },
    loadAppearances() {
      this.$store.dispatch('library/loadMediaAppearances', { uuid: this.objUuid });
    },
    showDetails() {
      this.detailsVisible = true;
    },
    hideDetails() {
      this.detailsVisible = false;
    },
  },
};
</script>

<template>
  <intersect
    @enter="onEnter"
  >
    <div
      class="appearances"
    >
      <div
        v-if="hasAppearances"
        class="appearances__summary"
        @mouseover="showDetails"
        @mouseleave="hideDetails"
      >
        <span
          class="label"
        >Appearances:</span>
        <span
          class="value"
        >{{ broadcast }}-{{ broadcastUnpublished }}-{{ pub }}</span>
      </div>
      <div v-else>
        &nbsp;
      </div>
      <div
        v-if="detailsVisible"
        class="appearances__details"
      >
        <div
          class="appearance"
        >
          <span
            class="label"
          >Broadcasts:</span>
          <span
            class="value"
          >{{ broadcast }}</span>
        </div>
        <div
          class="appearance"
        >
          <span
            class="label"
          >Planned Broadcasts:</span>
          <span
            class="value"
          >{{ broadcastUnpublished }}</span>
        </div>
        <div
          class="appearance"
        >
          <span
            class="label"
          >Public Playlists:</span>
          <span
            class="value"
          >{{ pub }}</span>
        </div>
      </div>
    </div>
  </intersect>
</template>

<style lang="scss" scoped>
.appearances {
  position: relative;
  &__summary {
    font-size: 90%;
    .label {
      color: #a3a3a3;
    }
  }
  &__details {
    position: absolute;
    right: 0;
    z-index: 1;
    min-width: 140px;
    padding: 0.5rem;
    background: #ffffff;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
  }
  .appearance {
    display: flex;
    .label {
      flex-grow: 1;
      color: #a3a3a3;
    }
  }
}
</style>
