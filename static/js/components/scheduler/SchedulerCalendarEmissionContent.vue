<script>

import Visual from '../ui/Visual.vue';
import Tags from '../ui/Tags.vue';
import UserInline from '../ui/UserInline.vue';
import ObjectActions from '../ObjectActions/ObjectActions.vue';

export default {
  name: 'SchedulerCalendarEmissionContent',
  components: {
    visual: Visual,
    tags: Tags,
    'user-inline': UserInline,
    'object-actions': ObjectActions,
  },
  props: {
    contentObj: {
      type: Object,
      required: true,
    },
    size: {
      type: String,
      default: 'small',
    },
  },
  computed: {},
  methods: {},
};
</script>
<style lang="scss" scoped>
    .content-object {
      display: flex;

      &__visual {
        position: relative;

        flex: 0 0 140px;

        figure {
          height: 140px;

          background: rgba(255, 255, 255, 0.1);
        }

        .object-actions {
          position: absolute;
          top: 0;

          color: #000;
        }
      }

      &__details {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        padding: 4px 10px;

        &__title {
          margin-bottom: 4px;

          color: inherit;
          font-size: 120%;
        }

        &__body {
          flex-grow: 1;
        }
      }

      &--small {
        .content-object__visual {
          flex: 0 0 90px;

          figure {
            height: 90px;
          }
        }
      }
    }
</style>

<template>
  <div
    v-if="contentObj"
    :class="{'content-object--small': (size === 'small')}"
    class="content-object"
  >
    <div class="content-object__visual">
      <visual :url="contentObj.image" />
      <object-actions
        :ct="contentObj.ct"
        :uuid="contentObj.uuid"
        :url="contentObj.url"
        :can-play="(true)"
        :can-schedule="(true)"
      />
    </div>
    <div class="content-object__details">
      <a
        :href="contentObj.detailUrl"
        target="_blank"
        class="content-object__details__title"
      >
        <span
          v-if="contentObj.seriesDisplay"
        >{{ contentObj.seriesDisplay }}<br></span>
        <span>{{ contentObj.name }}</span>
      </a>
      <div class="content-object__details__body">
        Editor:
        <user-inline
          v-if="contentObj.user"
          :user="contentObj.user"
        />
      </div>
      <div class="content-object__details__tags">
        <tags
          theme="light"
          :tags="contentObj.tags"
        />
      </div>
    </div>
  </div>
</template>
