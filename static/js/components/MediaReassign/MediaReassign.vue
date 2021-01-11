<script>
import { EventBus } from 'src/eventBus';
import { objectKeyToAPIUrl } from 'src/utils/urls';
import APIClient from 'src/api/caseTranslatingClient';
import Modal from '../UI/Modal.vue';
import ObjectSearch from '../ObjectSearch/ObjectSearch.vue';
import MediaReassignTarget from './MediaReassignTarget.vue';

const API_REASSIGN_URL = '/api/v2/alibrary/utils/re-assign-objects/';
const DEBUG = true;

export default {
  name: 'MediaReassign',
  components: {
    modal: Modal,
    'object-search': ObjectSearch,
    'reassign-target': MediaReassignTarget,
  },
  data() {
    return {
      visible: false,
      objectKeys: [],
      objects: [],
      targets: [],
      targetObj: null,
      currentInput: '',
      numTargets: 0,
      master: null,
      isLoading: false,
      createNew: false,
    };
  },
  computed: {
    target() {
      if (this.createNew && this.currentInput) {
        return {
          create: true,
          name: this.currentInput,
        };
      }
      if (this.targetObj) {
        return {
          create: false,
          key: `${this.targetObj.ct}:${this.targetObj.uuid}`,
        };
      }
      return null;
    },
  },
  mounted() {
    EventBus.$on('alibrary:reassignMedia', ({ selection }) => {
      this.objectKeys = selection;
      this.show();
      this.loadObjects();
    });
  },
  methods: {
    show() {
      this.visible = true;
    },
    close() {
      this.visible = false;
    },
    selectTarget(obj) {
      this.targetObj = obj;
    },
    loadObjects() {
      this.master = null;
      this.objects = [];
      this.objectKeys.forEach((key) => {
        const url = objectKeyToAPIUrl(key);
        const params = {
          // fields: ['name'].join(',')
        };
        if (DEBUG) console.debug('loadObjects - url', url);
        APIClient.get(url, { params }).then((response) => {
          this.objects.push(response.data);
        });
      });
    },
    setTargets({ results, total }) {
      this.numTargets = total;
      this.targets = results;
    },
    setInput(q) {
      this.currentInput = q;
    },
    reassignObjects() {
      if (!this.target) {
        return;
      }

      const url = API_REASSIGN_URL;
      const objects = this.objects.map((o) => `${o.ct}:${o.uuid}`);

      const payload = {
        // master: `${this.master.ct}:${this.master.uuid}`,
        target: this.target,
        objects,
      };

      if (DEBUG) console.debug('mergeObjects', url, payload);
      this.isLoading = true;
      APIClient.post(url, payload)
        .then((response) => {
          // this.isLoading = false;
          window.location.href = response.data.location;
        }, (error) => {
          this.isLoading = false;
          console.error('error posting data', error);
        });
    },
  },
};
</script>
<template>
  <modal
    :show="visible"
    :loading="isLoading"
    @close="close"
  >
    <div
      slot="title"
    >
      Re-assign items
    </div>
    <div
      slot="content"
      class="object-merge"
    >
      <div class="input-container">
        <div class="search-input">
          <object-search
            ct="alibrary.release"
            @inputUpdated="setInput"
            @resultsUpdated="setTargets"
          />
        </div>
        <div class="options-input">
          <input
            id="create-target"
            v-model="createNew"
            type="checkbox"
          >
          <label for="create-target">Create new Release</label>
        </div>
      </div>
      <div class="object-list">
        <div v-if="(! createNew)">
          <reassign-target
            v-for="obj in targets"
            :key="obj.uuid"
            :obj="obj"
            :is-selected="(targetObj === obj)"
            @selectObject="selectTarget"
          />
        </div>
      </div>
      <div class="actions">
        <a
          class="button"
          :class="{'button--disabled': (!target)}"
          @click.prevent="reassignObjects"
        >
          Confirm re-assign
        </a>
      </div>
    </div>
  </modal>
</template>
<style lang="scss" scoped>
  .object-merge {
    color: white;
    .object-search {
      margin: 1rem 0;
    }
    .input-container {
      display: flex;
      align-items: center;

      .options-input {
        display: flex;
        align-items: center;
        margin-left: 1rem;
        label {
          margin: 0 0 0 0.5rem;
          color: white;
        }
      }
    }
    .object-list {
      min-height: 400px;
      max-height: 50vh;
      margin: 1rem 0;
      overflow-y: auto;
    }
    .actions {
      text-align: right;
    }
  }
</style>
