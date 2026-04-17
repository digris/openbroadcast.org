<script>
export default {
  name: 'Modal',
  props: {
    show: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    scope: {
      type: String,
      required: false,
      default: '',
    },
  },
  mounted() {
    document.addEventListener('keydown', (e) => {
      if (this.show && e.keyCode === 27) {
        this.close();
      }
    });
  },
  methods: {
    close() {
      this.$emit('close');
    },
  },
};
</script>
<style lang="scss" scoped>
  @import '../../../sass/site/variables';

  .modal-mask {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 99;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    height: 100vh;
    background: rgba(#222, 0.2);

    .modal-container {
      position: fixed;
      z-index: 99;
      display: flex;
      flex-direction: column;
      width: 40vw;
      min-width: 800px;
      max-width: 800px;
      min-height: 150px;
      background: #222;
      border: 10px solid #222;
      border-top: none;
      // height: 60%;

      // full-size display in popup
      @media only screen and (max-width: 800px) {
        width: 100vw;
        min-width: unset;
        height: 100%;
      }

      &.is-loading {
        cursor: wait;

        .content-slot {
          opacity: .5;
          filter: grayscale(100%);
          pointer-events: none;
        }

      }

      .content-slot {
        flex: 1;
        overflow: auto;
        transition: opacity 250ms;

      }

      .modal-topbar {
        display: flex;
        height: 28px;
        background: #222;

        .modal-topbar-title {
          flex-grow: 1;
          padding: 6px 0 0 0;
          color: #fff;
        }

        .modal-topbar-menu {
          display: flex;

          a {
            //line-height: 28px;
            display: block;
            padding: 6px 10px 0 10px;
            color: #fff;
            text-transform: uppercase;
            background: $primary-color-b;
            cursor: pointer;
          }
        }
      }
    }
  }

  // transitions
  .modal-enter-active {
    transition: all 0.1s;
  }

  .modal-leave-active {
    transition: all 0.2s;
  }

  .modal-enter,
  .modal-leave-to {
    // transform: translateY(100vh);
    opacity: 0;
  }

</style>
<template>
  <transition name="modal">
    <div
      v-show="show"
      class="modal-mask"
      @click="close"
    >
      <div
        class="modal-container"
        :class="{'is-loading': loading, scope}"
        @click.stop
      >
        <div class="content-header">
          <div class="modal-topbar">
            <div class="modal-topbar-title">
              <slot name="title" />
            </div>
            <div class="modal-topbar-menu">
              <a
                class=""
                @click="close"
              >Close (esc)</a>
            </div>
          </div>
        </div>
        <div
          class="content-slot"
        >
          <slot name="content" />
        </div>
      </div>
    </div>
  </transition>
</template>
