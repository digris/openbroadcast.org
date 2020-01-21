<script>

    import LazyImage from './LazyImage.vue';

    export default {
        name: 'Lightbox',
        components: {
            'lazy-image': LazyImage,
        },
        props: {
            visible: {
                type: Boolean,
                required: false,
                default: false
            },
            imageUrl: {
                type: String,
                required: true,
            },
        },
        methods: {
            close: function () {
                this.$emit('close');
            }
        },
        mounted: function () {
            document.addEventListener('keydown', (e) => {
                if (this.visible && e.keyCode === 27) {
                    this.close();
                }
            });
        }
    }
</script>
<style lang="scss" scoped>

    .lightbox-mask {
        position: fixed;
        z-index: 99;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(#000, .9);
        display: flex;
        align-items: center;
        justify-content: center;

        .content {
            text-align: center;
            width: 50vw;
            height: 50vh;
            max-height: 500px;

            img {
                max-height: 500px;
            }

        }
    }

    // transitions
    .lightbox-enter-active {
        transition: all .1s;
    }

    .lightbox-leave-active {
        transition: all .2s;
    }

    .lightbox-enter, .lightbox-leave-to {
        opacity: 0;
    }

</style>
<template>
    <transition name="lightbox">
        <div class="lightbox-mask" @click="close" v-if="visible">
            <div class="content">
                <lazy-image :src="imageUrl"></lazy-image>
            </div>
        </div>
    </transition>
</template>
