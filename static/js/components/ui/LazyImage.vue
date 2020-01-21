<script>

    import settings from '../../settings';
    import throttle from 'lodash.throttle';

    export default {
        name: 'LazyImage',
        props: {
            src: {
                type: String,
                required: true,
            },
            width: {
                type: Number,
                required: false,
                default: null,
            },
            height: {
                type: Number,
                required: false,
                default: null,
            },
        },
        data() {
            return {
                placeholderImage: settings.PLACEHOLDER_IMAGE,
                isLoading: false,
                isLoaded: false,
                isVisible: false,
            }
        },
        computed: {
            canPlay: function () {
                return false;
            },
            imageSource: function() {
                if(this.isLoaded) {
                    return this.src;
                }
                return this.placeholderImage;
            },
            imageWidth: function() {
                return this.width;
            },
            imageHeight: function() {
                return this.height;
            }
        },
        mounted: function () {
            window.addEventListener('scroll', this.processImage);
            this.processImage();
        },
        methods: {

            throttledProcessImage: throttle(function() {
                this.processImage();
            }, 50),

            processImage: function() {
                if(this.isLoading || this.isLoaded) {
                    return;
                }

                if(!isInViewport(this.$el)) {
                    return;
                }

                this.isLoadig = true;
                const img = new Image();
                img.src = this.src;
                img.addEventListener('load', () => {
                    this.isLoading = false;
                    this.isLoaded = true;
                }, true);

            },
        },
    }

    function isInViewport(element) {
        let rect = element.getBoundingClientRect();
        let html = document.documentElement;
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.top <= (window.innerHeight || html.clientHeight) &&
            rect.left <= (window.innerWidth || html.clientWidth)
        );
    }

</script>
<style lang="scss" scoped>
    img {
        max-width: 100%;
        max-height: 100%;
        transition: opacity 200ms;
        &.placeholder {
            image-rendering: pixelated;
            opacity: 0.5;
        }
    }
</style>
<template>
  <img
    :class="{placeholder: !isLoaded}"
    :src="imageSource"
  >
</template>
