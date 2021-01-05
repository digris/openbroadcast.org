<script>
export default {
  name: 'SearchResult',
  props: {
    obj: {
      type: Object,
      required: true,
    },
    ct: {
      type: String,
      default: 'default',
    },
  },
  data() {
    return {
      component: null,
      foo: 'bar',
    };
  },
  computed: {
    loader() {
      // const component = `./templates/${this.ct}/index.vue`;
      // return () => import(component);
      return () => import(`./templates/${this.ct}/index.vue`);
    },
  },
  mounted() {
    this.loader()
      .then(() => {
        this.component = () => this.loader();
      })
      .catch(() => {
        this.component = () => import('./templates/default/index.vue');
      });
  },
};
</script>
<template>
  <component
    :is="component"
    v-if="component"
    :obj="obj"
  />
</template>
