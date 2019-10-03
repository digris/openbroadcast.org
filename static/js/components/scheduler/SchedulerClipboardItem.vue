<script>

    const DEBUG = true;
    import Visual from '../ui/Visual.vue';
    import EmissionHistory from '../EmissionHistory/EmissionHistory.vue';
    import ObjectActions from '../../components/ObjectActions/ObjectActions.vue';

    export default {
        name: 'SchedulerClipboardItem',
        components: {
            'emission-history': EmissionHistory,
            'visual': Visual,
            'object-actions': ObjectActions,
        },
        props: {
            item: Object,
        },
        // data() {
        //
        // },
        methods: {},
        computed: {
            duration() {
                if(!this.item) {
                    return null;
                }
                return new Date(this.item.duration).toISOString().substr(11, 8);
            }
        }
    }
</script>
<style lang="scss" scoped>
    .clipboard-item {
        background: #fff;
        display: flex;
        cursor: pointer;

        &:hover {
            background: rgba(126, 235, 157, 0.85);
            z-index: 999;
        }

        &__visual {
            width: 64px;
            position: relative;
            img {
                background: deepskyblue;
            }
            figure {
                height: 64px;
            }
            .object-actions {
                top: 0;
                position: absolute;
            }
        }

        &__body {
            flex-grow: 1;
            padding: 0 0 2px 8px;
        }

        &__header {
            display: flex;

            .title {
                color: inherit;
            }

            .emission-history {
                flex-grow: 1;
            }
        }

        &__description {
            opacity: .7;
        }
    }
</style>

<template>
    <div
        class="clipboard-item"
        @mouseenter="$emit('mouseenter')"
        @mouseleave="$emit('mouseleave')">
        <div class="clipboard-item__visual">
            <visual :url="item.image"></visual>
            <object-actions
                :scale="(.6)"
                :ct="item.ct"
                :uuid="item.uuid"
                :url="item.url"
                :can-play="(true)">
            </object-actions>
        </div>
        <div class="clipboard-item__body">
            <div class="clipboard-item__header">
                <a
                    :href="item.detailUrl"
                    target="_blank"
                    class="title">
                    <span v-if="item.seriesDisplay">{{ item.seriesDisplay }}<br></span>
                    {{ item.name }}
                </a>
                <emission-history
                    :obj-ct="item.ct"
                    :obj-uuid="item.uuid">
                </emission-history>
            </div>
            <div class="clipboard-item__description">
                <p>{{ duration }}</p>
            </div>
        </div>
    </div>
</template>
