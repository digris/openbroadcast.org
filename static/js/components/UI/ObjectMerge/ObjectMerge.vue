<script>

import APIClient from '../../../api/caseTranslatingClient';
import Modal from '../Modal.vue';
import ObjectMergeObject from './ObjectMergeObject.vue';

const DEBUG = true;

const objectKeyToAPIUrl = function(key) {
  // example: alibrary.release:87a71f94-8f2b-4629-801c-b14bdde06838
  const ct = key.split(':')[0];
  const uuid = key.split(':')[1];
  return `/api/v2/${ct.replace('.', '/')}/${uuid}/`;;
};

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
    };
  },
  mounted() {
    window.addEventListener('mergeObjects', (e) => {
      const objectKeys = e.detail;
      if (DEBUG) console.debug('mergeObjects', objectKeys);
      this.objectKeys = objectKeys;
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
      this.objectKeys.forEach((key, i) => {
        const url = objectKeyToAPIUrl(key);
        const params = {
          // fields: ['name'].join(',')
        };
        if (DEBUG) console.debug('loadObjects - url', url);
        APIClient.get(url, {params}).then((response) => {
          this.objects.push(response.data);
        })
      })
    },
    mergeObjects() {
      if(! this.master) {
        return;
      }

      const url = `${this.master.url}merge/`;
      const uuids = this.objects.filter((o) => (o.uuid !== this.master.uuid)).map(({ uuid }) => uuid);
      const payload = {
        slaveUuids: uuids,
      };

      if (DEBUG) console.debug('mergeObjects', url, payload);



    }
  }
};
</script>
<template>
  <modal
    :show="visible"
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
