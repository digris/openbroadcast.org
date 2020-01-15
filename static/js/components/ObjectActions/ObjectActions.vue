<script>

    const DEBUG = true;

    // import PlayerControlApp from '../../apps/player/player-control-app';
    import ClickOutside from 'vue-click-outside';
    import ObjectActionsAction from './ObjectActionsAction.vue';
    import ObjectActionsPlay from './ObjectActionsPlay.vue';

    export default {
        name: 'ObjectActions',
        components: {
            'action': ObjectActionsAction,
            'play': ObjectActionsPlay,
        },
        directives: {
            ClickOutside,
        },
        props: {
            scale: {
                type: Number,
                default: 1,
            },
            ct: {
                type: String,
                required: true,
            },
            uuid: {
                type: String,
                required: true,
            },
            url: {
                type: String,
                required: true,
            },
            editUrl: {
                type: String,
            },
            canPlay: {
                type: Boolean,
                default: false,
            },
            canQueue: {
                type: Boolean,
                default: false,
            },
            canDownload: {
                type: Boolean,
                default: false,
            },
            canEdit: {
                type: Boolean,
                default: false,
            },
            canSchedule: {
                type: Boolean,
                default: false,
            },
        },
        data() {
            return {
                secondaryActionsVisible: false,
            }
        },
        mounted: function () {
            // this.playerControl = new PlayerControlApp();
        },
        computed: {
            actions: function () {
                const actions = [];

                if (this.canQueue) {
                    actions.push({
                        key: 'queue',
                        icon: 'fa-pause',
                        title: 'Queue',
                    })
                }

                if (this.canDownload) {
                    actions.push({
                        key: 'download',
                        icon: 'fa-download',
                        title: 'Download',
                    })
                }

                if (this.canEdit) {
                    actions.push({
                        key: 'edit',
                        icon: 'fa-pencil',
                        title: 'Edit',
                    })
                }

                if (this.canSchedule) {
                    actions.push({
                        key: 'clipboard',
                        icon: 'fa-calendar',
                        title: 'Add to scheduler',
                    })
                }

                return actions;
            },
        },
        methods: {
            toggleSecondaryActions: function (e) {
                this.secondaryActionsVisible = !this.secondaryActionsVisible;
            },
            hideSecondaryActions: function (e, el) {
                console.debug(el, e, 'click outside...');
                // if(this.secondaryActionsVisible) {
                //     this.secondaryActionsVisible = false;
                // }
            },
            handleAction: function (key) {

                console.debug('handleAction', key);
                this.secondaryActionsVisible = false;

                // TODO: handle actions...
                if (key === 'play') {
                    this.playerControls({
                        do: 'load',
                        // opts: {
                        //   mode: 'queue',
                        // },
                        items: [{
                            ct: this.ct,
                            uuid: this.uuid,
                        }]
                    });
                }
                if (key === 'queue') {
                    this.playerControls({
                        do: 'load',
                        opts: {
                            mode: 'queue',
                        },
                        items: [{
                            ct: this.ct,
                            uuid: this.uuid,
                        }]
                    });
                }
                if (key === 'edit') {
                    document.location.href = this.editUrl;
                }

                if (key === 'clipboard') {
                    const co = {
                        name: '...loading...',
                        ct: this.ct,
                        uuid: this.uuid,
                        url: this.url,
                    };
                    this.$store.dispatch('scheduler/addToClipboard', co);
                }
            },
            playerControls: function(action) {
                const _e = new CustomEvent('player:controls', {detail: action});
                if (DEBUG) console.debug('playerControls emit action', _e);
                window.dispatchEvent(_e);
            }
        },
    }
</script>
<style lang="scss" scoped>
    .object-actions {
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        opacity: 0;

        &:hover {
            background: rgba(#000, .5);
            opacity: 1;
        }

        .actions {
            // background: rgba(#000, .5);
            display: flex;
            justify-content: center;

            .action {
                font-size: 32px;
                color: #fff;
                cursor: pointer;
                margin: 0 8px;

                &--primary {
                    width: 48%;

                    .circle-button {
                        width: 60px;
                        height: 60px;
                        background: black;
                        border-radius: 30px;
                        display: block;
                    }
                }

                &--secondary {
                    width: 24%;
                }
            }

        }

        .secondary-actions {
            display: flex;
            flex-direction: column;
            position: absolute;
            top: 55%;
            right: 4px;
            z-index: 999;
            filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.1));

            &__triangle {
                opacity: 0;
                background: white;
                margin: 0 auto;
                width: 20px;
                height: 10px;
                clip-path: polygon(50% 0%, 100% 100%, 0 100%);
            }

            &__list {
                background: white;
            }

        }

    }
</style>

<template>
    <div
        class="object-actions">
        <div
            :style="{transform: `scale(${scale})`}"
            class="actions">
            <div
                class="action action--secondary">
                <div></div>
            </div>
            <div
                class="action action--primary">
                <play
                    v-if="canPlay"
                    @click="handleAction('play')">
                </play>
            </div>
            <div
                class="action action--secondary">
                <div
                    v-if="(actions && actions.length)"
                    @click="toggleSecondaryActions">
                    <i class="fa fa-ellipsis-h"></i>
                </div>
            </div>
        </div>
        <div
            class="secondary-actions"
            v-if="secondaryActionsVisible"
            v-click-outside="hideSecondaryActions">
            <div class="secondary-actions__triangle"></div>
            <div
                class="secondary-actions__list"
                v-for="action in actions"
                v-bind:key="action.key">
                <action
                    @click="handleAction(action.key)"
                    :action="action"></action>
            </div>
        </div>
    </div>
</template>
