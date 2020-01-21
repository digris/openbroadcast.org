import axios from 'axios';
import debounce from 'debounce';
import nunjucks from 'nunjucks';
import APIClient from '../api/caseTranslatingClient';

const DEBUG = false;

const api_client = axios.create({
  xsrfHeaderName: 'X-CSRFTOKEN',
  xsrfCookieName: 'csrftoken',
});

// const IMAGE_PLACEHOLDER = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
const IMAGE_PLACEHOLDER = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAVCAYAAACpF6WWAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyhpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTM4IDc5LjE1OTgyNCwgMjAxNi8wOS8xNC0wMTowOTowMSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKE1hY2ludG9zaCkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6QTZGODUyNzlCNTE2MTFFODlCMTFFRDFEMDAyOTFBRDQiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6QTZGODUyN0FCNTE2MTFFODlCMTFFRDFEMDAyOTFBRDQiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDpBNkY4NTI3N0I1MTYxMUU4OUIxMUVEMUQwMDI5MUFENCIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDpBNkY4NTI3OEI1MTYxMUU4OUIxMUVEMUQwMDI5MUFENCIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PpzFGLUAAABHSURBVHjaYvz//z8DtQETAw3ACDeUBZvghw8fCOkDxS4jiCEgIDAMw/T/sIv9/9Qw9P+g9f5/Wobp/wGPfcbR8nRoGAoQYACJbA8guOHyXAAAAABJRU5ErkJggg==';
const TEMPLATES = {

  default: `<div class="result" data-id="{{ id }}" data-value="{{ name }}">
                    <div class="image">
                        <figure>
                            <img src="{% if image %}{{ image}}{% else %}${IMAGE_PLACEHOLDER}{% endif %}" />
                        </figure>
                    </div>
                    <div class="meta">
                        <div class="name">{{ name }}</div>
                    </div>
                    <div class="aux">
                        {{ type }}
                    </div>
                </div>`,

  'alibrary.label': `<div class="result" data-id="{{ id }}" data-value="{{ name }}">
                    <div class="image">
                        <figure>
                            <img src="{% if image %}{{ image}}{% else %}${IMAGE_PLACEHOLDER}{% endif %}" />
                        </figure>
                    </div>
                    <div class="meta">
                        <div class="name">{{ name }}{% if country_code %} <small>{{ country_code }}</small>{% endif %}</div>
                        {% if year_start %} *{{ year_start }}{% endif %}
                        {% if year_start and year_end %}&mdash;{% endif %}
                        {% if year_end %} ✝{{ year_end }}{% endif %}
                    </div>
                    <div class="aux">
                        {% if type %}{{ type }}{% endif %}
                        {% if type and labelcode %}<br>{% endif %}
                        {% if labelcode %}LC:{{ labelcode }}{% endif %}
                    </div>
                </div>`,

  'alibrary.artist': `<div class="result" data-id="{{ id }}" data-value="{{ name }}">
                    <div class="image">
                        <figure>
                            <img src="{% if image %}{{ image}}{% else %}${IMAGE_PLACEHOLDER}{% endif %}" />
                        </figure>
                    </div>
                    <div class="meta">
                        <div class="name">{{ name }}{% if country_code %} <small>{{ country_code }}</small>{% endif %}</div>
                        {% if year_start %} *{{ year_start }}{% endif %}
                        {% if year_start and year_end %}&mdash;{% endif %}
                        {% if year_end %} ✝{{ year_end }}{% endif %}
                    </div>
                    <div class="aux">
                        {% if type %}{{ type }}{% endif %}
                    </div>
                </div>`,

  'alibrary.release': `<div class="result" data-id="{{ id }}" data-value="{{ name }}">
                    <div class="image">
                        <figure>
                            <img src="{% if image %}{{ image}}{% else %}${IMAGE_PLACEHOLDER}{% endif %}" />
                        </figure>
                    </div>
                    <div class="meta">
                        <div class="name">{{ name }}{% if country_code %} <small>{{ country_code }}</small>{% endif %}</div>
                        {% if artist_display %}by: {{ artist_display }}<br>{% endif %}
                        {% if label_display %}on: {{ label_display }}<br>{% endif %}
                    </div>
                    <div class="aux">
                        {% if type %}{{ type }}{% endif %}
                        {% if type and catalognumber %}<br>{% endif %}
                        {% if catalognumber %}{{ catalognumber }}{% endif %}
                    </div>
                </div>`,

};

class AutocompleteWidget {
  /** ****************************************************************
     * single autocomplete-widget,
     * initialized by `AutocompleteWidgets`
     ***************************************************************** */

  constructor(container) {
    const results_class = 'autocomplete-widget-results';
    container.append($('<div/>').addClass(results_class));

    this.container = container;
    this.text_input = container.find('[data-autocomplete-widget-type="text"]');
    this.hidden_input = container.find('[data-autocomplete-widget-type="hidden"]');
    this.result_container = container.find(`.${results_class}`);
    this.url = this.text_input.data('autocomplete-widget-url');
    this.limit_results = 20;
    this.navigation_keys = [13, 27, 38, 40];
    this.results = [];
    this.current_value = this.text_input.val();
    this.current_id = this.hidden_input.val();
    this.selected_index = -1;

    if (DEBUG) console.debug(`AutocompleteWidget - url: ${this.url} - value: ${this.current_value} -  id: ${this.current_id} `);

    this.bindings();
  }

  bindings() {
    this.text_input.on('keydown', (e) => {
      if (this.navigation_keys.includes(e.which)) {
        return this.handle_keys(e);
      }
    });

    this.text_input.on('keyup', debounce((e) => {
      const q = $(e.currentTarget).val();
      if (!this.navigation_keys.includes(e.which)) {
        this.autocomplete(q);
      }
    }, 100));

    this.text_input.on('blur', debounce((e) => {
      if (this.text_input.val() !== this.current_value) {
        this.hidden_input.val('');
        this.current_value = this.text_input.val();
      }
      this.set_results([]);
    }, 200));

    this.container.on('click', '[data-action="close"]', (e) => {
      this.selected_index = -1;
      this.set_results([]);
    });

    this.result_container.on('click', 'div.result', (e) => {
      this.select_item($(e.currentTarget).data());
    });

    // event handler is vanilla javascript
    // needed as 'legacy' components use an old version of jquery, outside of webpack.
    this.container[0].addEventListener('autocomplete:changed', (e) => {
      if (DEBUG) console.info('autocomplete:changed', e.detail);
      this.autocomplete(e.detail.value);
    }, false);
  }

  handle_keys(e) {
    // handle special keys (up, down, esc, return)

    this.selected_index = $('[data-id].selected', this.results_container).index();

    if (DEBUG) console.debug('selected index:', this.selected_index, 'num total', $('[data-id]', this.results_container).length, 'key:', e.which);

    // down
    if (e.which === 40) {
      if ($('[data-id]', this.results_container).length - 1 > this.selected_index) {
        this.selected_index++;
      }
    }

    // up
    if (e.which === 38) {
      if (this.selected_index >= 0) {
        this.selected_index--;
      }
    }

    $('[data-id]', this.results_container).each((i, item) => {
      const el = $(item);
      if (i === this.selected_index) {
        el.addClass('selected');
      } else {
        el.removeClass('selected');
      }
    });

    // esc
    if (e.which === 27) {
      this.set_results([]);
    }

    // return
    if (e.which === 13) {
      if (this.selected_index > -1) {
        const selected = this.results[this.selected_index];
        this.select_item({ id: selected.id, value: selected.name });
      } else {
        // remove id (= create new entry) input if text changed
        if (this.text_input.val() !== this.current_value) {
          this.hidden_input.val('');
          this.current_value = this.text_input.val();
        }
        this.set_results([]);
      }
    }

    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
  }

  autocomplete(q) {
    if (DEBUG) console.debug('AutocompleteWidget: query:', q);

    api_client.get(this.url, { params: { q, limit: this.limit_results } })
      .then((response) => {
        if (DEBUG) console.table(response.data.results);
        this.set_results(response.data.results);
      }, (error) => {
        console.error(error);
        this.set_results([]);
      });
  }

  set_results(results = [], display = true) {
    this.results = results;
    if (display) {
      this.display_results();
    }
  }

  display_results() {
    let html_results = '';

    if (this.results.length) {
      html_results += '<div class="results-header"><span class="close" data-action="close">close</span></div>';
    }
    html_results += '<div class="results-list">';
    for (const result of this.results) {
      html_results += this.render_item(result);
    }
    html_results += '</div>';

    this.result_container.html(html_results);
  }

  render_item(item) {
    const tpl = TEMPLATES[item.ct] || TEMPLATES.default;

    console.log('tpl:', tpl);
    console.log('item:', item);

    return nunjucks.renderString(tpl, item);
  }

  select_item(item) {
    if (DEBUG) console.debug('AutocompleteWidget: select_item', item);

    this.text_input.val(item.value);
    this.hidden_input.val(item.id);
    this.current_value = item.value;
    this.current_id = item.id;

    this.set_results([]);
  }
}


class AutocompleteWidgets {
  /** ****************************************************************
     * initializes autocomplete-widget on respective items
     ***************************************************************** */

  constructor() {
    this.widgets = [];

    if (DEBUG) console.group('AutocompleteWidgets');

    $('[data-autocomplete-widget-url]').each((i, item) => {
      const container = $(item).parent();
      this.widgets.push(
        new AutocompleteWidget(container),
      );
    });

    if (DEBUG) console.group('num. widgets initialized', this.widgets.length);

    if (DEBUG) console.groupEnd();
  }
}


export default AutocompleteWidgets;
