<script>

import dayjs from 'dayjs';
import advancedFormat from 'dayjs/plugin/advancedFormat';
import { templateFilters } from 'src/utils/template-filters';
import { hexToRGBA } from './utils';
import SchedulerCalendarEmissionContent from './SchedulerCalendarEmissionContent.vue';
import Modal from '../UI/Modal.vue';
import UserInline from '../UI/UserInline.vue';
import EmissionHistoryMatrix from '../EmissionHistory/EmissionHistoryMatrix.vue';

const DEBUG = true;

dayjs.extend(advancedFormat);

export default {
  name: 'SchedulerCalendarEmissionEditor',
  components: {
    modal: Modal,
    'user-inline': UserInline,
    matrix: EmissionHistoryMatrix,
    'content-obj': SchedulerCalendarEmissionContent,
  },
  filters: templateFilters,
  props: {
    uuid: {
      type: String,
      required: false,
      default: null,
    },
  },
  computed: {
    visible() {
      return this.uuid != null;
    },
    emission() {
      if (!this.uuid) {
        return null;
      }
      return this.$store.getters['scheduler/emissionByUuid'](this.uuid);
    },
    contentObj() {
      if (!this.emission) {
        return null;
      }
      return this.emission.co;
    },
    contentObjStyle() {
      if (!this.contentObj) {
        return null;
      }
      const color = this.emission.color;
      return {
        backgroundColor: hexToRGBA(color, 0.2),
        // backgroundColor: `rgba(${color}, .2)`,
      };
    },
    emissionHistory() {
      if (!this.contentObj) {
        return null;
      }
      console.debug('history', this.contentObj.ct, this.contentObj.uuid);
      return this.$store.getters['objectHistory/objectHistoryByKey'](this.contentObj.ct, this.contentObj.uuid);
    },
    formattedTimes() {
      if (!this.emission) {
        return null;
      }
      const start = dayjs(this.emission.timeStart);
      const end = dayjs(this.emission.timeEnd);
      return {
        date: start.format('ddd. D MMMM YYYY'),
        start: start.format('H:mm'),
        end: end.format('H:mm'),
      };
    },
  },
  watch: {
    uuid(oldUuid, newUuid) {
      this.loadEmissionDetails();
      this.loadEmissionHistory();
    },
  },
  methods: {
    close() {
      this.$emit('close');
    },
    loadEmissionDetails() {
      if (this.uuid) {
        const dispatch = this.$store.dispatch('scheduler/loadEmission', this.uuid);
      }
    },
    setColor(color) {
      this.updateEmission({
        color,
      });
    },
    updateEmission(payload) {
      const dispatch = this.$store.dispatch('scheduler/updateEmission', {
        emission: this.emission,
        payload,
      });
    },
    deleteEmission() {
      const dispatch = this.$store.dispatch('scheduler/deleteEmission', this.uuid);
      dispatch.then((response) => {
        this.$emit('close');
      }, (error) => {
        console.warn('error', error.message, error.response);
      });
    },
    // history
    loadEmissionHistory() {
      if (!this.contentObj) {
        return;
      }
      this.$store.dispatch('objectHistory/loadObjectHistory', {
        objCt: this.contentObj.ct,
        objUuid: this.contentObj.uuid,
      });
    },
  },
};
</script>
<style lang="scss" scoped>
    .emission-editor {
      display: flex;
      flex-direction: column;
      height: 100%;
      color: white;

      .content-object {
        margin: 20px 0;
      }

      &__history {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        justify-content: center;
        margin: 20px 0;
      }

      &__actions {
        display: flex;
        flex-direction: column;

        .background-colors {
          display: flex;
          width: 100%;

          .color {
            flex-grow: 1;
            padding: 0;
            cursor: pointer;
          }
        }

        .delete {
          margin-top: 16px;

          &__confirm {
            padding: 6px;
            color: #63c;
            font-size: 120%;
            text-align: center;
            background: #fff;
            border: 2px solid #63c;
            cursor: pointer;

            &:hover {
              color: #fff;
              background: #63c;
              border-radius: 4px;
            }
          }
        }
      }
    }
</style>

<template>
  <modal
    :show="visible"
    @close="close"
  >
    <div
      v-if="emission"
      slot="title"
    >
      <span>{{ emission.timeStart|date('HH:mm') }}-{{ emission.timeEnd|date('HH:mm') }}</span>
      <span> / </span>
      <span>{{ emission.timeStart|date('dd. D MMM. YYYY') }}</span>
      <span
        v-if="(emission && emission.user)"
        class="scheduling-programmer"
      >
        / by:
        <user-inline
          v-if="emission.user"
          :user="emission.user"
        /></span>
    </div>

    <div
      slot="content"
      class="emission-editor"
    >
      <content-obj
        v-if="contentObj"
        :style="contentObjStyle"
        :content-obj="contentObj"
      />
      <div
        class="emission-editor__history"
      >
        <matrix
          v-if="emissionHistory"
          theme="dark"
          :obj-uuid="( (contentObj) ? contentObj.uuid : null )"
          :emission-history="emissionHistory"
        />
      </div>
      <div
        class="emission-editor__actions"
      >
        <div
          v-if="(contentObj && !emission.hasLock)"
          class="delete"
        >
          <div
            class="delete__confirm"
            @click="deleteEmission"
          >
            <span>Remove emission</span>
          </div>
        </div>
      </div>
    </div>
  </modal>
</template>
