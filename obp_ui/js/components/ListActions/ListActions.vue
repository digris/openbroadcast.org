<script>
import { EventBus } from '../../eventBus';

// TODO: this should be generalized...
const playerControls = (action) => {
  const e = new CustomEvent('player:controls', { detail: action });
  window.dispatchEvent(e);
};

export default {
  name: 'ListActions',
  props: {
    objCt: {
      type: String,
      required: false,
      default: null,
    },
    objUuid: {
      type: String,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      items: [],
    };
  },
  beforeMount() {
    if (this.objCt && this.objUuid) {
      console.debug('override list action item(s)');
      this.items.push({ ct: this.objCt, uuid: this.objUuid });
      return;
    }
    EventBus.$on('list-actions:register', (actions) => {
      actions.forEach((action) => {
        if (action.key === 'play') {
          this.items.push({ ct: action.ct, uuid: action.uuid });
        }
      });
    });
  },
  methods: {
    playAll() {
      playerControls({
          do: 'load',
          items: this.items,
        });
    },
    queueAll() {
      playerControls({
          do: 'load',
          opts: {
            mode: 'queue',
          },
          items: this.items,
        });
    },
  },
};
</script>
<template>
  <div
    v-if="(items.length)"
    class="list-actions"
  >
    <div
      class="button button--secondary action action--queue"
      @click.prevent="playAll"
    >
      Play All
    </div>
    <div
      class="button button--secondary action action--queue"
      @click.prevent="queueAll"
    >
      Queue All
    </div>
  </div>
</template>
<style lang="scss" scoped>
.list-actions {
  background: transparent;
}
</style>
