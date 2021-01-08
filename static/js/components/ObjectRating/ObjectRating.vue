<script>
import settings from '../../settings';

export default {
  name: 'ObjectRating',
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
  // data() {
  //   return {
  //     userVote: -1,
  //   };
  // },
  computed: {
    isReadOnly() {
      return !settings.user.isAuthenticated;
    },
    key() {
      return `${this.objCt}:${this.objUuid}`;
    },
    rating() {
      return this.$store.getters['rating/ratingForKey'](this.key);
    },
    votes() {
      if (this.rating && this.rating.votes) {
        return this.rating.votes;
      }
      return null;
    },
    userVote() {
      if (this.votes && this.votes.user) {
        return this.votes.user;
      }
      return null;
    },
  },
  mounted() {
    this.$store.dispatch('rating/loadRating', { key: this.key });
  },
  methods: {
    vote(vote) {
      if (this.isReadOnly) {
        return false;
      }
      const value = (vote !== this.userVote) ? vote : 0;
      return this.$store.dispatch('rating/updateVote', {
        key: this.key, value,
      });
    },
  },
};
</script>

<template>
  <div
    class="object-rating"
    :class="{'is-readonly': isReadOnly}"
  >
    <div
      class="vote vote--up"
      :class="{'vote--user': userVote === 1}"
      @click.prevent="vote(1)"
    >
      <span
        class="vote__value"
      >
        <span v-if="(votes)">{{ votes.up }}</span>
      </span>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        x="0px"
        y="0px"
        width="24px"
        height="24px"
        viewBox="0 0 24 24"
        xml:space="preserve"
      >
        <g>
          <path
            stroke="#000000"
            stroke-width="1.5"
            fill="#ffffff"
            d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81
            4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55
            11.54L12 21.35z"
          />
        </g>
      </svg>
    </div>
    <div
      class="vote vote--down"
      :class="{'vote--user': userVote === -1}"
      @click.prevent="vote(-1)"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        x="0px"
        y="0px"
        width="24px"
        height="24px"
        viewBox="0 0 24 24"
        xml:space="preserve"
      >
        <g>
          <circle
            stroke="#000000"
            stroke-width="1.5"
            fill="#ffffff"
            cx="12"
            cy="12"
            r="10"
          />
          <line
            stroke="#000000"
            stroke-width="2"
            stroke-miterlimit="10"
            x1="6"
            y1="12"
            x2="18"
            y2="12"
          />
        </g>
      </svg>
      <span
        class="vote__value"
      >
        <span v-if="(votes)">{{ votes.down }}</span>
      </span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.object-rating {
  display: flex;
  align-items: center;
  justify-content: center;

  &.is-readonly {
    pointer-events: none;
  }
}

.vote {
  display: flex;
  flex-direction: row;
  align-items: center;
  align-self: center;

  margin: 0 1rem;

  cursor: pointer;

  svg {
    circle,
    path {
      transition: fill-opacity 200ms;
    }
  }

  &__value {
    min-width: 36px;
    padding: 0 0.5rem;
  }

  &--up & {
    &__value {
      text-align: right;
    }
  }

  &:hover {
    svg {
      circle,
      path {
        transition: fill-opacity 0ms;

        fill: var(--primary-color);
        fill-opacity: 0.6;
      }
    }
  }

  &--user {
    svg {
      circle,
      path {
        fill: var(--secondary-color) !important;
        stroke: var(--secondary-color) !important;
        fill-opacity: 1;
      }
      line {
        stroke: #ffffff;
      }
    }
    &.vote--down {
      svg {
        circle,
        path {
          fill: #e23602 !important;
          stroke: #e23602 !important;
        }
      }
    }
  }
}
</style>
