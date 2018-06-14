<script src="./search-app.js"></script>

<style scoped>

    .search-app {
        position: relative;
    }
    .search-result-container {
        display: none;
        position: absolute;
        width: 100%;
    }
    .search-result-container.expanded {
        display: block;
    }

</style>

<template>
    <div class="search-app">

        <div v-bind:class="{ 'has-focus': search_input_has_focus }"
             class="search-input-container">
            <div class="controls search-input">

                <input type="text"
                       placeholder="Search Artists, Releases & more..."
                       :value="search_query_string"
                       @input="update_query_string"
                       @focus="search_input_focus($event)"
                       @blur="search_input_blur($event)"
                       @keydown.esc="search_input_esc($event)"
                       @keydown.up="select_search_result($event, -1)"
                       @keydown.down="select_search_result($event, 1)"
                       @keydown.left="select_search_result($event, false)"
                       @keydown.enter="navigate_to_selected_search_result($event)">



            </div>
            <span>* {{ search_scope }} *</span>
            <span>* {{ search_total_results }} *</span>

        </div>

        <div v-bind:class="{ expanded: result_is_visible }"
             class="search-result-container">

            <div class="search-settings-container">
                <span v-if="settings.search_exact_match_mode">
                    <span @click="update_settings('search_exact_match_mode', false)">[X] exact match mode</span>
                </span>
                <span v-else>
                    <span @click="update_settings('search_exact_match_mode', true)">[&nbsp;] exact match mode</span>
                </span>
            </div>

            <div v-for="item in search_results"
                 :key="item.uuid"
                 v-bind:data-uuid="item.uuid"
                 v-bind:class="{ 'active': item.selected }"
                 class="search-result">

                <div class="controls controls-image">

                    <div v-if="(item.image)">
                        <figure>
                            <img v-bind:src="item.image"/>
                        </figure>
                    </div>
                    <div v-else>
                        <figure>
                            <img width="60"
                                 src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
                        </figure>
                    </div>
                </div>
                <div class="controls controls-meta">

                    <span class="title">
                        <a v-on:click="navigate_to_item($event, item)">{{ item.name }}</a>
                    </span>

                    <br>
                    <span v-for="tag in item.tags">
                        {{ tag }},
                    </span>



                </div>
                <div class="controls controls-right">
                    <span class="ctype">{{ item.ct }}</span>
                </div>

            </div>

            <div class="search-scope-container">
                <ul>
                    <li><a @click="set_search_scope('foo')" href="#">FOO</a></li>
                    <li><a @click="set_search_scope('bar')" href="#">BAR</a></li>
                </ul>
            </div>

        </div>

    </div>
</template>
