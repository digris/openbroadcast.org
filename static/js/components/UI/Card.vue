<script>

  import settings from '../../settings';
  import VisualWithActions from "./VisualWithActions.vue";

  export default {
    name: 'Card',
    components: {
      'visual-with-actions': VisualWithActions,
    },
    props: {
      ct: {
        type: String,
        required: true,
      },
      uuid: {
        type: String,
        required: true,
      },
      url: {
        type: String,
        default: null,
      },
      imageUrl: {
        type: String,
        required: false,
        default: null,
      },
      actions: {
        type: Array,
        required: false,
        default() {
          return [];
        },
      },
    },
    // data() {
    //   return {
    //     selected: false,
    //   };
    // },
    computed: {
      selected() {
        return this.$store.getters['objectSelection/objectSelection'](this.ct, this.uuid);
      },
    },
    methods: {
      toggleSelection() {
        this.$store.dispatch('objectSelection/toggleSelection', { ct: this.ct, uuid: this.uuid });
      },
    },
  };
</script>
<template>
  <div
    class="card"
    :class="{'card--is-selected': selected}"
  >
    <div class="card__visual">
      <visual-with-actions
        :ct="ct"
        :uuid="uuid"
        :url="url"
        :image-url="imageUrl"
        :actions="actions"
      />
      <div class="card__visual__top">
        <slot name="visual-top" />
      </div>
      <div
        v-if="$slots['visual-bottom']"
        class="card__visual__bottom"
      >
        <slot name="visual-bottom" />
      </div>
    </div>
    <div
      class="card__body"
      @click="toggleSelection"
    >
      <slot name="default" />
    </div>
    <div class="card__footer">
      <slot name="footer" />
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .card {

    background: #fff;

    &--is-selected {
      background: var(--primary-color-light);
      /*border: 1px solid red;*/
    }

    &__visual {
      position: relative;

      display: inline-grid;
      width: 100%;
      height: 0;
      padding-bottom: 100%;

      .visual-with-actions {
        position: absolute;

        width: 100%;

        img {
          width: 100%;
          height: 100%;
        }
      }

      &__top {
        position: absolute;
        top: 0;
        left: 0;

        display: flex;
        width: 100%;

        .flags {

          display: inline-flex;

          flex-grow: 1;

          .flag {
            padding: 2px 4px;

            text-transform: uppercase;

            background: white;
          }

        }

      }

      &__bottom {
        position: absolute;
        right: 0;
        bottom: 0;

        display: flex;
        width: 100%;

        .tags {

          display: flex;
          flex-wrap: wrap;
          justify-content: flex-end;

          width: 100%;


          .tag {

            display: inline-flex;
            align-items: center;

            height: 16px;

            margin: 0 2px 2px 0;
            padding: 0 4px;

            color: white;

            font-size: 11px;
            line-height: 11px;

            text-transform: uppercase;

            background: #5a5a5a;

          }

        }


      }
    }

    &__body {
      padding: 4px 4px 0 4px;

      cursor: pointer;

      &__row {
        display: grid;
        grid-template-columns: auto auto;
        > *:nth-child(even) {
          text-align: right;
        }
      }
    }

    &__footer {
      display: grid;
      grid-template-columns: auto auto;

      padding: 0 4px 2px 4px;

      > *:nth-child(even) {
        text-align: right;
      }

      a {
        filter: grayscale(100%);
      }
    }
  }
</style>
