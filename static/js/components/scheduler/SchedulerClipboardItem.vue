<script>

    const DEBUG = true;
    import Visual from '../ui/Visual.vue';
    import EmissionHistory from '../EmissionHistory/EmissionHistory.vue';

    export default {
        name: 'SchedulerClipboardItem',
        components: {
            'emission-history': EmissionHistory,
            'visual': Visual,
        },
        props: {
            item: Object,
        },
        // data() {
        //
        // },
        methods: {},
        computed: {}
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
            img {
                background: deepskyblue;
            }
            figure {
                height: 64px;
            }
        }

        &__body {
            flex-grow: 1;
            padding: 0 0 2px 8px;
        }

        &__header {
            display: flex;
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
        class="clipboard-item">
        <div class="clipboard-item__visual">
            <visual :url="item.image"></visual>
        </div>
        <div class="clipboard-item__body">
            <div class="clipboard-item__header">
                <div>
                    <span v-if="item.seriesDisplay">{{ item.seriesDisplay }}<br></span>
                    {{ item.name }}
                </div>
                <emission-history
                    :obj-ct="item.ct"
                    :obj-uuid="item.uuid">
                </emission-history>
            </div>
            <div class="clipboard-item__description">
                <p>foo the bar</p>
            </div>
        </div>
    </div>
</template>
