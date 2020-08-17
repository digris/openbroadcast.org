<script>

const DEBUG = false;

export default {
  name: 'ThumbRating',
  props: {
    objCt: {
      type: String,
      required: true,
    },
    objUuid: {
      type: String,
      required: true,
    },
  },
  data() {
    return {

    };
  },
  computed: {
    key() {
      if (!this.media) {
        return null;
      }
      return `${this.objCt}:${this.objUuid}`;
    },
    votes() {
      if (!this.key) {
        return null;
      }

      return [];


      // const votes = this.$store.getters['rating/votes'][this.key];
      //
      // if (typeof votes === 'undefined') {
      //   this.$store.dispatch('rating/get_votes', this.key);
      // }
      //
      // return votes;
    },
  },
  mounted() {
    // const key = `${this.obj_ct}:${this.media.id}`;
    // this.$store.dispatch('rating/get_votes', {obj_ct: 'alibrary.media', obj_pk: this.media.id});
  },
  methods: {
    vote(value) {
      if (!this.key) {
        return null;
      }
      if (DEBUG) console.debug('vote', value);
      return true;
      // this.$store.dispatch('rating/update_vote', {key: this.key, value: value});
    },
  },
};
</script>
<style lang="scss" scoped>
    .thumb-rating {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 60px;
    }

    .vote {
      position: relative;

      display: flex;
      flex-direction: row;
      align-self: center;

      cursor: pointer;

      svg {
        margin: 0 20px;

        rect,
        polyline {
          transition: fill-opacity 200ms;
        }
      }

      &:hover {
        svg {
          rect,
          polyline {
            fill-opacity: 0.4;
          }
        }
      }

      &--down {
        svg {
          position: relative;
          top: 12px;

          transform: rotateZ(180deg);
        }
      }

      &__value {
        font-size: 105%;
        line-height: 42px;
      }

      &--up & {
        &__value {
          margin-right: 10px;
        }
      }

      &--down & {
        &__value {
          margin-left: 10px;
        }
      }
    }

    .separator {
      width: 2px;
      height: 60px;
      margin: 0 20px;
    }

</style>

<template>
  <div
    class="thumb-rating"
    data-account-login-required
  >
    <div
      class="vote vote--up"
      @click.prevent="vote(1)"
    >
      <span
        data-livefg
        class="vote__value"
      >
        <span v-if="(votes)">{{ votes.up }}</span>
        <span v-else>-</span>
      </span>
      <svg
        id="Layer_1"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        x="0px"
        y="0px"
        width="33px"
        height="33px"
        viewBox="0 0 33 33"
        xml:space="preserve"
      >
        <g>
          <polyline
            fill-opacity="0.1"
            data-livefill-inverse
            stroke="#000000"
            stroke-width="2"
            data-livestroke
            stroke-miterlimit="10"
            points="8,15 14,15 20,1 23,1 23,14,32,14 32,26 29,31 19,31 16,29 8,29"
          />
          <rect
            x="1"
            y="13"
            fill-opacity="0.1"
            data-livefill-inverse
            stroke="#000000"
            stroke-width="2"
            data-livestroke
            stroke-miterlimit="10"
            width="8"
            height="18"
          />
        </g>
      </svg>
    </div>
    <div
      class="vote vote--down"
      @click.prevent="vote(-1)"
    >
      <svg
        id="Layer_1"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        x="0px"
        y="0px"
        width="34px"
        height="33px"
        viewBox="0 0 34 32"
        xml:space="preserve"
      >
        <g>
          <polyline
            fill-opacity="0.1"
            data-livefill-inverse
            stroke="#000000"
            stroke-width="2"
            data-livestroke
            stroke-miterlimit="10"
            points="8,15 14,15 20,1 23,1 23,14,32,14 32,26 29,31 19,31 16,29 8,29"
          />
          <rect
            x="1"
            y="13"
            fill-opacity="0.1"
            data-livefill-inverse
            stroke="#000000"
            stroke-width="2"
            data-livestroke
            stroke-miterlimit="10"
            width="8"
            height="18"
          />
        </g>
      </svg>
      <span
        data-livefg
        class="vote__value"
      >
        <span v-if="(votes)">{{ votes.down }}</span>
        <span v-else>-</span>
      </span>
    </div>
  </div>
</template>
