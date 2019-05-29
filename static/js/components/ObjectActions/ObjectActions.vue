<script>

    const DEBUG = false;

    import PlayerControlApp from '../../apps/player/player-control-app';
    import ClickOutside from 'vue-click-outside';
    import ObjectActionsAction from './ObjectActionsAction.vue';


    export default {
        name: 'ObjectActions',
        components: {
            'action': ObjectActionsAction,
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
                    actions.push({
                        'key': key,
                        'name': key,
                    })
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

        &:hover {
            .primary-actions {
                opacity: 1;
                background: rgba(#000, .5);
            }
        }

        .primary-actions {
            opacity: .4;
            // background: rgba(#000, .5);
            display: flex;
            justify-content: center;
            padding: 8px;
            border-radius: 4px;

            .action {
                font-size: 32px;
                color: #fff;
                cursor: pointer;
                margin: 0 8px;
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
            class="primary-actions">
            <div
                class="action action--primary">
                <div
                    @click="handleAction(primaryAction.key)">
                    <i class="fa fa-play"></i>
                </div>
            </div>
            <div
                class="action action--primary">
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
                        :name="action.name"></action>
                </div>
        </div>
    </div>
</template>
