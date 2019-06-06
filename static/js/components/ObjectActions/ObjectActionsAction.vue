<script>

const DEBUG = false;

export default {
    name: 'ObjectActionsAction',
    props: {
        action: Object,
    }
}
</script>
<style lang="scss" scoped>
    .action {
        cursor: pointer;
        padding: 8px 12px;
        display: flex;
        min-width: 120px;

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
</style>

<template>
    <div
        @click="$emit('click')"
        class="action">
        <div class="action__icon">
            <i v-bind:class="action.icon" class="fa"></i>
        </div>
        <div class="action__name">
            {{ action.title }}
        </div>
    </div>
</template>
