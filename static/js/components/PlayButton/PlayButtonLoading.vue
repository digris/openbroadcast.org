<script>
export default {
  name: 'PlayButtonLoading',
  props: {
    scale: {
      type: Number,
      default: 1,
    },
    color: {
      type: String,
      default: '#fff',
    },
    hoverColor: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      hover: false,
    };
  },
  computed: {
    // eslint-disable-next-line no-underscore-dangle
    _scale() {
      return (this.scale) ? this.scale : 1;
    },
    // eslint-disable-next-line no-underscore-dangle
    _color() {
      return (this.color) ? this.color : '#fff';
    },
    // eslint-disable-next-line no-underscore-dangle
    _color_hover() {
      // eslint-disable-next-line no-underscore-dangle
      return (this.color_hover) ? this.color_hover : this._color;
    },
  },
};
</script>
<style lang="scss" scoped>

  .spinner {
    display: flex;
    justify-content: space-between;
    width: 14px;
    height: 14px;
    font-size: 0;
    text-align: center;
  }

  .spinner > div {
    display: inline-block;
    width: 2px;
    height: 100%;
    background-color: #f0f;
    -webkit-animation: sk-stretchdelay 1.2s infinite ease-in-out;
    animation: sk-stretchdelay 1.2s infinite ease-in-out;
  }

  .spinner .rect2 {
    -webkit-animation-delay: -1.1s;
    animation-delay: -1.1s;
  }

  .spinner .rect3 {
    -webkit-animation-delay: -1.0s;
    animation-delay: -1.0s;
  }

  .spinner .rect4 {
    -webkit-animation-delay: -0.9s;
    animation-delay: -0.9s;
  }

  .spinner .rect5 {
    -webkit-animation-delay: -0.8s;
    animation-delay: -0.8s;
  }

  @-webkit-keyframes sk-stretchdelay {
    0%, 40%, 100% {
      -webkit-transform: scaleY(0.4)
    }
    20% {
      -webkit-transform: scaleY(1.0)
    }
  }

  @keyframes sk-stretchdelay {
    0%, 40%, 100% {
      -webkit-transform: scaleY(0.4);
      transform: scaleY(0.4);
    }
    20% {
      -webkit-transform: scaleY(1.0);
      transform: scaleY(1.0);
    }
  }

</style>
<template>
  <div
    class="spinner"
    :style="{ transform: `scale(${_scale})` }"
  >
    <div
      class="rect1"
      :style="{ background: _color }"
    />
    <div
      class="rect2"
      :style="{ background: _color }"
    />
    <div
      class="rect3"
      :style="{ background: _color }"
    />
    <div
      class="rect4"
      :style="{ background: _color }"
    />
    <div
      class="rect5"
      :style="{ background: _color }"
    />
  </div>
</template>
