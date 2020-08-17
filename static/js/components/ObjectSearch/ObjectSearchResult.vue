<script>
export default {
  name: 'SearchResult',
  props: {
    data: {
      type: Object,
      required: true,
    },
    ct: {
      type: String,
      default: 'default',
    },
  },
  computed: {
    loader() {
      return () => import(`./templates/${this.ct}/index.vue`);
    },
  },
  data() {
    return {
      component: null,
      foo: 'bar',
    };
  },
  mounted() {
    this.loader()
      .then(() => {
        this.component = () => this.loader()
      })
      .catch(() => {
        this.component = () => import('./templates/default/index.vue')
      })
    // this.component = () => import(`./templates/${this.ct}/index.vue`);
  },
};
</script>
<template>
  <component
    v-if="component"
    :is="component"
    :data="data"/>
</template>
