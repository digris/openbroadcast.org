<script>

    const DEBUG = false;

    const ICON_MAP = {
        default: 'fa-pencil',
        edit: 'fa-pencil',
        download: 'fa-download',
        message: 'fa-envelope',
        admin: 'fa-lock',
        loginas: 'fa-key',
    };

    export default {
        name: 'ContextMenu',
        props: {
            visible: {
                type: Boolean,
                required: false,
                default: false
            },
            actions: {
                type: Array,
                required: false,
                default: function () {
                    return [];
                }
            },
        },
        methods: {
            handleAction: function (action) {
                this.$emit('click', action);
            },
            getIconClass: function(action) {
                return ICON_MAP[action.key] || ICON_MAP['default'];
            }
        }
    }
</script>
<style lang="scss" scoped>
    .context-menu {
        position: absolute;
        min-width: 150px;
        top: 0;
        right: 0;

        display: flex;
        flex-direction: column;
        z-index: 999;
        filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.1));

        .menu-item {
            cursor: pointer;
            padding: 10px 14px;
            display: flex;
            width: 100%;
            &:hover {
                background: #00bb73;
                color: #fff;
            }
            &__icon {
                width: 20px;
            }
            &__name {
                flex-grow: 1;
                white-space: nowrap;
            }
        }
    }

    .fade-enter-active, .fade-leave-active {
      transition: opacity 200ms;
    }

    .fade-enter, .fade-leave-to {
      opacity: 0;
    }

</style>
<template>
    <transition name="fade">
        <div
            class="context-menu"
            v-if="visible">
            <div
                class="menu-item"
                v-for="action in actions"
                :key="action.key"
                @click="handleAction(action)">
                <div class="menu-item__icon">
                    <i :class="getIconClass(action)" class="fa"></i>
                </div>
                <div class="menu-item__name">
                    {{ action.title }}
                </div>
            </div>
        </div>
    </transition>
</template>
