<script>
export default {
  name: 'Loader',
};
</script>
<style lang="scss" scoped>
  @import '../../../sass/site/variables';

  .spinner {
    width: 50px;
    height: 40px;
    margin: 100px auto;

    font-size: 10px;
    text-align: center;
  }

  .spinner > div {
    display: inline-block;
    width: 6px;
    height: 100%;

    background-color: $primary-color-b;

    -webkit-animation: sk-stretchdelay 1.2s infinite ease-in-out;
    animation: sk-stretchdelay 1.2s infinite ease-in-out;
  }

  .spinner .rect2 {
    -webkit-animation-delay: -1.1s;
    animation-delay: -1.1s;
  }

  .spinner .rect3 {
    -webkit-animation-delay: -1s;
    animation-delay: -1s;
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
    0%,
    40%,
    100% {
      -webkit-transform: scaleY(0.4);
    }

    20% {
      -webkit-transform: scaleY(1);
    }
  }

  @keyframes sk-stretchdelay {
    0%,
    40%,
    100% {
      -webkit-transform: scaleY(0.4);
      transform: scaleY(0.4);
    }

    20% {
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
  }

</style>
<template>
  <div class="spinner">
    <div class="rect1" />
    <div class="rect2" />
    <div class="rect3" />
    <div class="rect4" />
    <div class="rect5" />
  </div>
</template>
