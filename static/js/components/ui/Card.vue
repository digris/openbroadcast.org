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
  };
</script>
<template>
  <div class="card">
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
      <div class="card__visual__bottom" v-if="$slots['visual-bottom']">
        <slot name="visual-bottom" />
      </div>
    </div>
    <div class="card__body">
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
      }

      &__bottom {
        position: absolute;
        right: 0;
        bottom: 0;

        display: flex;
        width: 100%;
      }
    }

    &__body {
      padding: 4px 4px 0 4px;


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
