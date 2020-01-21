<script src="./search-app.js"></script>

<template>
  <div
    v-click-outside="deactivate_search"
    class="search-app"
    :class="{ active: active }"
  >
    <div
      :class="{ 'has-focus': search_input_has_focus }"
      class="search-input-container"
    >
      <div class="search-input-icon">
        <i class="icon icon-search" />
      </div>
      <div class="controls search-input">
        <input
          type="text"
          placeholder="Search Artists, Releases & more..."
          :value="search_query_string"
          @input="update_query_string"
          @focus="search_input_focus($event)"
          @blur="search_input_blur($event)"
          @keydown.esc="search_input_esc($event)"
          @keydown.up="select_search_result($event, -1)"
          @keydown.down="select_search_result($event, 1)"
          @keydown.left="select_search_result($event, false)"
          @keydown.enter="navigate_to_selection($event)"
        >
      </div>
    </div>
    <div
      class="search-display-container"
      :style="{ left: search_display_box.left + 'px', width: search_display_box.width + 'px' }"
    >
      <div
        :class="{ expanded: active }"
        class="search-options-container"
      >
        <div class="search-settings-container">
          <span v-if="settings.search_fuzzy_match_mode">
            <span
              class="setting"
              @click="update_settings('search_fuzzy_match_mode', false)"
            >
              <i class="icon-check-empty" />
              <span>exact match mode</span>
            </span>
          </span>
          <span v-else>
            <span
              class="setting"
              @click="update_settings('search_fuzzy_match_mode', true)"
            >
              <i class="icon-check-sign" />
              <span>exact match mode</span>
            </span>
          </span>
        </div>
        <div class="search-scope-container">
          <ul class="scopes">
            <!--<li class="scope-label"><span>Scope:</span></li>-->
            <li
              v-for="scope in search_scopes"
              :key="scope.ct"
              :class="{ selected: search_scope === scope.ct }"
              class="scope"
            >
              <a
                href="#"
                @click="set_search_scope(scope.ct)"
              >{{ scope.name }}</a>
            </li>
          </ul>
        </div>
      </div>
      <div
        :class="{ expanded: result_is_visible }"
        class="search-result-container"
      >
        <div
          v-for="item in search_results"
          :key="item.uuid"
          :data-uuid="item.uuid"
          :class="{ 'active': item.selected, 'top-hit': item.top_hit}"
          class="search-result"
        >
          <div class="controls controls-image">
            <div v-if="(item.image)">
              <figure>
                <img :src="item.image">
              </figure>
            </div>
            <div v-else>
              <figure>
                <img
                  width="60"
                  src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
                >
              </figure>
            </div>
          </div>
          <div class="controls controls-meta">
            <span class="title">
              <a @click="navigate_to_item($event, item)">{{ item.name }}<!-- | {{ item.score }} - {{ item.top_hit }}--></a>
              <span v-if="item.artist_display"><br>{{ item.artist_display }}</span>
            </span>
            <br>
            <span
              v-for="(tag, index) in item.tags.slice(0, 4)"
              :key="index"
            >
              {{ tag }}<span v-if="index != item.tags.slice(0, 4).length - 1">,</span>
            </span>
          </div>
          <div class="controls controls-right">
            <span class="ctype">{{ item.scope.name }}</span>
          </div>
        </div>
      </div>
      <div
        v-if="(search_scope !== '_all' && search_results.length > 1)"
        class="search-footer-container"
      >
        <div class="search-actions">
          <a
            href="#"
            class="search-action"
            @click.stop.prevent="navigate_to_selection"
          >Detailed Results</a>
        </div>
      </div>
    </div>
  </div>
</template>
