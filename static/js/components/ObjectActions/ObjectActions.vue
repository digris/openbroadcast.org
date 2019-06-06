<script>

    const DEBUG = false;

    import PlayerControlApp from '../../apps/player/player-control-app';
    import ClickOutside from 'vue-click-outside';
    import ObjectActionsAction from './ObjectActionsAction.vue';
    import ObjectActionsPlay from './ObjectActionsPlay.vue';

    const ACTION_MAP = {
        play: {
            icon: 'fa-play',
            title: 'Play'
        },
        queue: {
            icon: 'fa-pause',
            title: 'Queue'
        },
        download: {
            icon: 'fa-download',
            title: 'Download'
        },
        edit: {
            icon: 'fa-pencil',
            title: 'Edit'
        },
        schedule: {
            icon: 'fa-calendar',
            title: 'Schedule'
        },
    };

    const parseActionKey = function(key) {
        let action = ACTION_MAP[key];
        if(action === undefined) {
            return {
                key: key,
                title: key,
                icon: null,
            }
        }
        action.key = key;
        return action;
    };

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
            objCt: String,
            objUuid: String,
            actions: String
        },
        data() {
            return {
                secondaryActionsVisible: false,
            }
        },
        mounted: function () {
            this.playerControl = new PlayerControlApp();
        },
        computed: {
            parsedActions: function () {
                const keys = this.actions.split(',');
                let actions = [];
                keys.forEach((key) => {
                    actions.push(parseActionKey(key));
                    // actions.push({
                    //     'key': key,
                    //     'name': key,
                    // })
                });

                return actions
            },
            primaryAction: function () {
                if (this.parsedActions.length < 1) {
                    return null;
                }
                return this.parsedActions[0];
            },
            secondaryActions: function () {
                if (this.parsedActions.length < 2) {
                    return null;
                }
                return this.parsedActions.slice(1)
            },
        },
        methods: {
            toggleSecondaryActions: function (e) {
                this.secondaryActionsVisible = !this.secondaryActionsVisible;
            },
            hideSecondaryActions: function (e) {
                this.secondaryActionsVisible = false;
            },
            handleAction: function (key) {


                this.playerControl.send_action({
                    do: 'load',
                    // opts: {
                    //   mode: 'queue',
                    // },
                    items: [{
                        ct: this.objCt,
                        uuid: this.objUuid,
                    }]
                });
            },
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
            left: 15%;
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
            class="actions">
            <div
                class="action action--secondary">
                <div></div>
            </div>
            <div
                class="action action--primary">
                <play
                    @click="toggleSecondaryActions">
                </play>
            </div>
            <div
                class="action action--secondary">
                <div
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
                v-for="action in secondaryActions"
                v-bind:key="action.key">
                <action
                    @click="handleAction(action.key)"
                    :action="action"></action>
            </div>
        </div>
    </div>
</template>
