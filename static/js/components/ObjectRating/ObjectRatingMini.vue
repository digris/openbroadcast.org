<script>
export default {
  name: 'ObjectRatingMini',
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
  computed: {
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
};
</script>

<template>
  <div
    v-if="userVote"
    class="object-rating-mini"
  >
    <svg
      v-if="(userVote === 1)"
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
          fill="#00BB73"
          d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81
          4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55
          11.54L12 21.35z"
        />
      </g>
    </svg>
    <svg
      v-if="(userVote === -1)"
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
          stroke="#e23602"
          stroke-width="1.5"
          fill="#e23602"
          cx="12"
          cy="12"
          r="10"
        />
        <line
          stroke="#ffffff"
          stroke-width="2"
          stroke-miterlimit="10"
          x1="6"
          y1="12"
          x2="18"
          y2="12"
        />
      </g>
    </svg>
  </div>
</template>
<style lang="scss" scoped>
.object-rating-mini {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  background: white;

  svg {
    height: 14px;
  }
}
</style>
