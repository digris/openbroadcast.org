<script>
    export default {
        name: 'LayoutBase',
    }
</script>

<template>
    <div class="content">
        <div class="content__primary">
            <slot></slot>
        </div>
        <div class="content__sidebar">
            <slot name="sidebar"></slot>
        </div>
    </div>
</template>
