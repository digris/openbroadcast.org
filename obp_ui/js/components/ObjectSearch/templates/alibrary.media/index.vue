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
    {{ obj.ct }}*{{ obj.name }}
  </div>
</template>
