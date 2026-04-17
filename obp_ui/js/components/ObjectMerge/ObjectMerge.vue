<script>
import { EventBus } from 'src/eventBus';
import { objectKeyToAPIUrl } from 'src/utils/urls';
import APIClient from 'src/api/caseTranslatingClient';
import Modal from '../UI/Modal.vue';
import ObjectMergeObject from './ObjectMergeObject.vue';

const API_MERGE_URL = '/api/v2/alibrary/utils/merge-objects/';
const DEBUG = false;

export default {
  name: 'ObjectMerge',
  components: {
    modal: Modal,
    'merge-object': ObjectMergeObject,
  },
  data() {
    return {
      visible: false,
      objectKeys: [],
      objects: [],
      master: null,
      isLoading: false,
    };
  },
  mounted() {
    EventBus.$on('alibrary:mergeObjects', ({ selection }) => {
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
    selectObject(obj) {
      if (DEBUG) console.debug('selectObject', obj);
      this.master = obj;
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
    mergeObjects() {
      if (!this.master) {
        return;
      }

      const url = API_MERGE_URL;

      const slaves = this.objects.filter((o) => (o.uuid !== this.master.uuid)).map((o) => `${o.ct}:${o.uuid}`);
      const payload = {
        master: `${this.master.ct}:${this.master.uuid}`,
        slaves,
      };

      if (DEBUG) console.debug('mergeObjects', url, payload);
      this.isLoading = true;
      APIClient.post(url, payload)
        .then(() => {
          window.location.reload();
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
      Merge items
    </div>
    <div
      slot="content"
      class="object-merge"
    >
      <div class="object-list">
        <merge-object
          v-for="obj in objects"
          :key="obj.uuid"
          :obj="obj"
          :is-selected="(master === obj)"
          @selectObject="selectObject"
        />
      </div>
      <div class="actions">
        <a
          class="button"
          :class="{'button--disabled': (!master)}"
          @click.prevent="mergeObjects"
        >
          Confirm merge
        </a>
      </div>
    </div>
  </modal>
</template>
<style lang="scss" scoped>
  .object-merge {
    color: white;
    .object-list {
      margin: 1rem 0;
    }
    .actions {
      text-align: right;
    }
  }
</style>
