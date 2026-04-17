<script>
export default {
  name: 'DefaultResult',
  props: {
    obj: {
      type: Object,
      required: true,
    },
  },
};
</script>
<template>
  <div>
    {{ obj.name }}
  </div>
</template>
