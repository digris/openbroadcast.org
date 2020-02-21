<script>

  import PlaylistEditorSearch from './PlaylistEditorSearch.vue';
  import APIClient from "../../api/client";

  const DEBUG = true;

  export default {
    name: 'PlaylistEditor',
    components: {
      'playlist-editor-search': PlaylistEditorSearch,
    },
    props: {
      uuid: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        masterWindow: null,
        canAutoplay: null,
        isLoading: false,
        controls: [],
      }
    },
    computed: {

    },
    mounted() {
      if (DEBUG) console.debug('PlaylistEditor - mounted');
    },
    methods: {

      addMediaToPlaylist(media) {
        console.debug('addMediaToPlaylist', media)

        const url = `/api/v2/library/playlist/${this.uuid}/`;
        const itemsToCollect = [{
          content: {
            ct: 'alibrary.media',
            uuid: media.uuid,
            // uuid: '1ce2fcfa-132f-444d-a5ed-6c621500c516',
          },
        }];



        APIClient.put(url, { itemsToCollect })
          .then((response) => {
            console.debug(response);
          }, (error) => {
            console.error('error putting data', error);
            playlist.loading = false;
          });

      },
    },
  };
</script>

<template>
  <div class="playlist-editor">
    <playlist-editor-search
      class="playlist-editor__search"
      @select="addMediaToPlaylist"
    >
      (( search ))
    </playlist-editor-search>
  </div>
</template>

<style lang="scss" scoped>
  .playlist-editor {
    // background: red;
    font-size: 12px;
  }
</style>
