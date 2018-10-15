<script>
    const DEBUG = true;
    export default {
        name: 'Modal',
        props: ['show', 'scope'],
        methods: {
            close: function () {
                this.$emit('close');
            }
        },
        mounted: function () {
            document.addEventListener('keydown', (e) => {
                if (this.show && e.keyCode === 27) {
                    if (DEBUG) console.debug('ESC -> close');
                    this.close();
                }
            });
        }
    }
</script>
<style lang="scss" scoped>
    @import '../../sass/site/variables';

    .modal-mask {
        position: fixed;
        z-index: 99;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(#222, 1);
        display: flex;
        align-items: center;
        justify-content: center;
        .modal-container {
            border: 10px solid #222;
            border-top: none;
            position: fixed;
            z-index: 99;
            min-width: 150px;
            min-height: 150px;
            width: 100vw;
            height: 100vh;
        }
        .modal-topbar {
            background: #000;
            display: flex;
            height: 28px;
            .modal-topbar-title {
                flex-grow: 1;
            }
            .modal-topbar-menu {
                display: flex;
                a {
                    background: $primary-color-b;
                    color: #fff;
                    //line-height: 28px;
                    display: block;
                    padding: 6px 10px 0 10px;
                    text-transform: uppercase;
                }
            }
        }
    }

    // transitions
    .modal-enter-active {
        transition: all .1s;
    }

    .modal-leave-active {
        transition: all .2s;
    }

    .modal-enter, .modal-leave-to {
        transform: translateY(100vh);
        opacity: 0;
    }

</style>
<template>
    <transition name="modal">
        <div class="modal-mask" @click="close" v-show="show">
            <div class="modal-container" v-bind:class="scope" @click.stop>
                <div class="modal-topbar">
                    <div class="modal-topbar-title">
                        <slot name="title"></slot>
                    </div>
                    <div class="modal-topbar-menu">
                        <a @click="close" class="">Close (esc)</a>
                    </div>
                </div>
                <slot name="content"></slot>
            </div>
        </div>
    </transition>
</template>
