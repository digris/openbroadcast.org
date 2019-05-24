<script>

  const DEBUG = false;

  export default {
    name: 'ThumbRating',
    props: [
      'objCt',
      'objUuid',
    ],
    data() {
      return {

      }
    },
    mounted: function () {
      // const key = `${this.obj_ct}:${this.media.id}`;
      // this.$store.dispatch('rating/get_votes', {obj_ct: 'alibrary.media', obj_pk: this.media.id});
    },
    computed: {
      user() {
        // return this.$store.getters['account/user'];
      },
      key() {
        if (!this.media) {
          return null;
        }
        return `${this.objCt}:${this.objUuid}`
      },
      votes() {
        if (!this.key) {
          return null;
        }

        // const votes = this.$store.getters['rating/votes'][this.key];
        //
        // if (typeof votes === 'undefined') {
        //   this.$store.dispatch('rating/get_votes', this.key);
        // }
        //
        // return votes;
      },
    },
    methods: {
      vote: function (value) {
        if (!this.key) {
          return null;
        }
        if (DEBUG) console.debug('vote', value);
        // this.$store.dispatch('rating/update_vote', {key: this.key, value: value});
      },
    }
  }
</script>
<style lang="scss" scoped>
    .thumb-rating {
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .vote {
        align-self: center;
        cursor: pointer;
        position: relative;
        display: flex;
        flex-direction: row;

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
                transform: rotateZ(180deg);
                top: 12px;
                position: relative;
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
    <div class="thumb-rating" data-account-login-required>
        <div @click.prevent="vote(1)" class="vote vote--up">
            <span data-livefg class="vote__value">
                <span v-if="(votes)">{{ votes.up }}</span>
                <span v-else>-</span>
            </span>
            <svg version="1.1"
                 id="Layer_1"
                 xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                 x="0px" y="0px"
                 width="33px" height="33px"
                 viewBox="0 0 33 33" xml:space="preserve">
                <g>
                    <polyline
                            fill-opacity="0.1"
                            data-livefill-inverse
                            stroke="#000000"
                            stroke-width="2"
                            data-livestroke
                            stroke-miterlimit="10"
                            points="8,15 14,15 20,1 23,1 23,14,32,14 32,26 29,31 19,31 16,29 8,29"/>
                    <rect
                            x="1" y="13"
                            fill-opacity="0.1"
                            data-livefill-inverse
                            stroke="#000000"
                            stroke-width="2"
                            data-livestroke
                            stroke-miterlimit="10"
                            width="8" height="18"/>
                </g>
            </svg>
        </div>
        <div @click.prevent="vote(-1)" class="vote vote--down">
            <svg version="1.1"
                 id="Layer_1"
                 xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                 x="0px" y="0px"
                 width="34px" height="33px"
                 viewBox="0 0 34 32" xml:space="preserve">
                <g>
                    <polyline
                            fill-opacity="0.1"
                            data-livefill-inverse
                            stroke="#000000"
                            stroke-width="2"
                            data-livestroke
                            stroke-miterlimit="10"
                            points="8,15 14,15 20,1 23,1 23,14,32,14 32,26 29,31 19,31 16,29 8,29"/>
                    <rect
                            x="1" y="13"
                            fill-opacity="0.1"
                            data-livefill-inverse
                            stroke="#000000"
                            stroke-width="2"
                            data-livestroke
                            stroke-miterlimit="10"
                            width="8" height="18"/>
                </g>
            </svg>
            <span data-livefg class="vote__value">
                <span v-if="(votes)">{{ votes.down }}</span>
                <span v-else>-</span>
            </span>
        </div>
    </div>
</template>
