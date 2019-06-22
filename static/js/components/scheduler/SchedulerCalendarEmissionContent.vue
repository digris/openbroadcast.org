<script>

    import Visual from '../ui/Visual.vue';
    import Tags from '../../components/ui/Tags.vue';
    import UserInline from '../../components/ui/UserInline.vue';
    import ObjectActions from '../../components/ObjectActions/ObjectActions.vue';

    export default {
        name: 'SchedulerCalendarEmissionContent',
        props: {
            contentObj: Object,
            size: String,
        },
        components: {
            'visual': Visual,
            'tags': Tags,
            'user-inline': UserInline,
            'object-actions': ObjectActions,
        },
        methods: {},
        computed: {}
    }
</script>
<style lang="scss" scoped>
    .content-object {
        display: flex;
        &__visual {
            flex: 0 0 140px;
            position: relative;
            figure {
                background: rgba(255, 255, 255, 0.10);
                height: 140px;
            }
            .object-actions {
                top: 0;
                position: absolute;
                color: #000;
            }
        }
        &__details {
            flex-grow: 1;
            padding: 4px 10px;
            display: flex;
            flex-direction: column;
            &__title {
                font-size: 120%;
                margin-bottom: 4px;
                color: inherit;
            }
            &__body {
                flex-grow: 1;
            }
        }

        &--small {
            .content-object__visual {
                flex: 0 0 90px;
                figure {
                    height: 90px;
                }
            }
        }

    }
</style>

<template>
    <div
        v-if="contentObj"
        :class="{'content-object--small': (size === 'small')}"
        class="content-object">
        <div class="content-object__visual">
            <visual :url="contentObj.image"></visual>
            <object-actions
                :ct="contentObj.ct"
                :uuid="contentObj.uuid"
                :url="contentObj.url"
                :can-play="(true)"
                :can-schedule="(true)">
            </object-actions>
        </div>
        <div class="content-object__details">
            <a
                :href="contentObj.detailUrl"
                target="_blank"
                class="content-object__details__title">
                <span
                    v-if="contentObj.seriesDisplay">{{ contentObj.seriesDisplay }}<br></span>
                <span>{{ contentObj.name }}</span>
            </a>
            <div class="content-object__details__body">
                Editor:
                <user-inline
                    v-if="contentObj.user"
                    :user="contentObj.user"></user-inline>
            </div>
            <div class="content-object__details__tags">
                <tags
                    theme="light"
                    :tags="contentObj.tags"></tags>
            </div>
        </div>
    </div>
</template>
