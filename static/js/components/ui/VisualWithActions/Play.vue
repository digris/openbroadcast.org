<script>

const DEBUG = false;

export default {
  name: 'Play',
};
</script>
<style lang="scss" scoped>
    .play-icon-container {
      cursor: pointer;

      transition: transform 100ms;

      &:hover {
        transform: scale(1.1);

        svg {
          circle {
            stroke: #00bb73;
          }

          polygon {
            fill: #00bb73;
          }
        }
      }
    }
</style>
<template>
  <div
    class="play-icon-container"
    @click="$emit('click')"
  >
    <svg
      version="1.1"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      x="0px"
      y="0px"
      width="56px"
      height="56px"
      viewBox="0 0 56 56"
      xml:space="preserve"
    >
      <g id="playIcon">
        <circle
          fill="#000"
          stroke="#fff"
          d="circle"
          class="st0"
          cx="28"
          cy="28"
          r="27"
        />
        <polygon
          id="triangle"
          fill="#fff"
          class="st1"
          points="21,16.5 41,28 21,39.5 	"
        />
      </g>
    </svg>
  </div>
</template>
