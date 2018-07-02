<script src="./search-app.js"></script>

<style scoped>
    .search-app {
        position: relative;
    }
    /*
    .search-display-wrapper {
        position: absolute;
        width: 100%;
    }

    .search-result-container {
        width: 100%;
    }
    .search-result-container.expanded {
        display: block;
    }
    */
</style>

<template>
    <div class="search-app"  v-bind:class="{ active: active }" v-click-outside="deactivate_search">

        <div v-bind:class="{ 'has-focus': search_input_has_focus }"
             class="search-input-container">
            <div class="search-input-icon">
                <i class="icon icon-search"></i>
            </div>
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
                       @keydown.enter="navigate_to_selection($event)">
            </div>
        </div>
        <div class="search-display-wrapper">
            <div v-bind:class="{ expanded: active }" class="search-options-container">
                <div class="search-settings-container">
                    <span v-if="settings.search_fuzzy_match_mode">
                        <span @click="update_settings('search_fuzzy_match_mode', false)" class="setting">
                            <i class="icon-check-empty"></i>
                            <span>exact match mode</span>
                        </span>
                    </span>
                    <span v-else>
                        <span @click="update_settings('search_fuzzy_match_mode', true)" class="setting">
                            <i class="icon-check-sign"></i>
                            <span>exact match mode</span>
                        </span>
                    </span>
                </div>
                <div class="search-scope-container">
                    <ul class="scopes">
                        <!--<li class="scope-label"><span>Scope:</span></li>-->
                        <li v-for="scope in search_scopes" v-bind:class="{ selected: search_scope == scope.ct }" class="scope">
                            <a @click="set_search_scope(scope.ct)" href="#">{{ scope.name }}</a>
                        </li>
                    </ul>
                </div>
            </div>
            <div v-bind:class="{ expanded: result_is_visible }"
                 class="search-result-container">
                <div v-for="item in search_results"
                     :key="item.uuid"
                     v-bind:data-uuid="item.uuid"
                     v-bind:class="{ 'active': item.selected, 'top-hit': item.top_hit}"
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
                            <a v-on:click="navigate_to_item($event, item)">{{ item.name }}<!-- | {{ item.score }} - {{ item.top_hit }}--></a>
                        </span>
                        <br>
                        <span v-for="(tag, index) in item.tags.slice(0, 4)">
                            {{ tag }}<span v-if="index != item.tags.slice(0, 4).length - 1">,</span>
                        </span>
                    </div>
                    <div class="controls controls-right">
                        <span class="ctype">{{ item.scope.name }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
