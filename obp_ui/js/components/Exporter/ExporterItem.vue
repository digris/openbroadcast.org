<script>
import Date from '../UI/Date.vue';
import Filesize from '../UI/Filesize.vue';

const STATUS_MAP = {
  0: 'init',
  1: 'completed',
  2: 'queued',
  3: 'running',
  4: 'downloaded',
  99: 'error',
};

export default {
  name: 'ExporterItem',
  props: {
    item: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
  components: {
    'date': Date,
    'filesize': Filesize,
  },
  computed: {
    status() {
      return STATUS_MAP[this.item.status];
    },
  },
};
</script>

<template>
  <div
    class="item"
    :class="`is-${status}`"
  >
    <!--
    <div
      class="item__icon"
    >
      {{ item.status }} /
      {{ status }}
    </div>
    -->
    <div
      class="item__name"
    >
      {{ item.name }}
    </div>
    <div
      class="item__timestamp"
    >
      <date
        :value="item.created"
      />
    </div>
    <div
      class="item__size"
    >
      <filesize
        :filesize="item.filesize"
      />
    </div>
    <div
      class="item__actions"
    >
      <a
        v-if="item.filesize"
        :href="item.downloadUrl"
        class="download-link"
        target="_blank"
      >
        Download
      </a>
      <a
        v-else
        class="download-link is-disabled"
      >
        Download
      </a>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.item {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: 1fr auto 100px 100px;
  margin-bottom: 0.5rem;
  padding: 1rem;
  background: white;
  border-bottom: 2px solid #bcbcbc;
  &__size {
    text-align: right;
  }
  &__actions {
    text-align: right;
    .download-link {
      &.is-disabled {
        opacity: 0.5;
        filter: grayscale(100%);
        pointer-events: none;
      }
    }
  }
  transition: border-bottom-color 200ms;
  &.is-completed {
    border-bottom-color: var(--primary-color);
  }
  &.is-downloaded {
    border-bottom-color: var(--secondary-color);
  }
}
</style>
