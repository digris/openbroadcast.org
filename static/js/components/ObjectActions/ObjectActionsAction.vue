<script>

const DEBUG = false;

export default {
    name: 'ObjectActionsAction',
    props: {
        name: String,
    }
}
</script>
<style lang="scss" scoped>
    .action {
        cursor: pointer;
        padding: 4px 10px;
        display: flex;

        &:hover {
            background: blue;
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
            P
        </div>
        <div class="action__name">
            {{ name }}
        </div>
    </div>
</template>
