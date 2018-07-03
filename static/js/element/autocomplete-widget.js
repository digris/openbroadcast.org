import axios from 'axios';
import debounce from 'debounce';
import nunjucks from 'nunjucks';

const api_client = axios.create({
    xsrfHeaderName: 'X-CSRFTOKEN',
    xsrfCookieName: 'csrftoken',
});

const TEMPLATES = {

    'default': `<div class="result" data-id="{{ id }}" data-value="{{ name }}">
                    <div class="image">
                        <figure>
                            <img src="{% if image %}{{ image}}{% else %}data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7{% endif %}" />
                        </figure>
                    </div>
                    <div class="meta">
                        {{ name }}
                    </div>
                    <div class="aux">
                        {{ type }}
                    </div>
                    
                </div>`,

    'alibrary.label': `<div class="result" data-id="{{ id }}" data-value="{{ name }}">
                    <div class="image">
                        <figure>
                            <img src="{% if image %}{{ image}}{% else %}data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7{% endif %}" />
                        </figure>
                    </div>
                    <div class="meta">
                        {{ name }}{% if country %} ({{ country }}){% endif %}
                        <br>
                        {% if year_start %} *{{ year_start }}{% endif %}
                        {% if year_start and year_end %}&mdash;{% endif %}
                        {% if year_end %} ✝{{ year_end }}{% endif %}
                    </div>
                    <div class="aux">
                        {{ type }}
                    </div>
                    
                </div>`,

};

class AutocompleteWidget {

    /******************************************************************
     * single autocomplete-widget,
     * initialized by `AutocompleteWidgets`
     ******************************************************************/

    constructor(container, opts) {
        this.debug = opts.debug || false;

        const results_class = 'autocomplete-widget-results';
        container.append( $('<div/>').addClass(results_class));

        this.container = container;
        this.text_input = container.find('[data-autocomplete-widget-type="text"]');
        this.hidden_input = container.find('[data-autocomplete-widget-type="hidden"]');
        this.result_container = container.find('.' + results_class);
        this.url = this.text_input.data('autocomplete-widget-url');
        this.limit_results = opts.limit_results || 20;
        this.navigation_keys = [13, 27, 38, 40];
        this.results = [];
        this.current_value = this.text_input.val();
        this.current_id = this.hidden_input.val();
        this.selected_index = -1;

        if (this.debug) console.debug(`AutocompleteWidget - url: ${this.url} - value: ${this.current_value} -  id: ${this.current_id} `);

        this.bindings();
    };

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

        // this.text_input.on('focus', (e) => {
        //     const q = $(e.currentTarget).val();
        //     this.autocomplete(q);
        // });

        this.text_input.on('blur', debounce((e) => {

            if(this.text_input.val() !== this.current_value) {
                this.hidden_input.val('');
                this.current_value = this.text_input.val();
            }

            this.set_results([]);
        }, 200));

        this.result_container.on('click', 'div.result', (e) => {
            this.select_item($(e.currentTarget).data());
        });

    };

    handle_keys(e) {
        // handle special keys (up, down, esc, return)

        this.selected_index = $('[data-id].selected', this.results_container).index();

        console.debug('selected index:', this.selected_index, 'num total', $('[data-id]', this.results_container).length, 'key:', e.which)

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
                this.select_item({id: selected.id, value: selected.name});

            } else {
                // remove id (= create new entry) input if text changed
                if(this.text_input.val() !== this.current_value) {
                    this.hidden_input.val('');
                    this.current_value = this.text_input.val();
                }
                this.set_results([]);
            }
        }

        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        return;
    };

    autocomplete(q) {

        if (this.debug) console.debug('AutocompleteWidget: query:', q);

        api_client.get(this.url, {params: {q: q, limit: this.limit_results}})
            .then((response) => {
                if (this.debug) console.table(response.data.results);
                this.set_results(response.data.results);
            }, (error) => {
                console.error(error);
                this.set_results([]);
            })
    };

    set_results(results=[], display=true) {
        this.results = results;
        if(display) {
            this.display_results();
        }
    };

    display_results() {

        let html_results = '';

        if(this.results.length) {
            html_results += '<div class="results-header"><span class="close">close</span></div>';
        }
        html_results += '<div>';
        for (let result of this.results) {
            html_results += this.render_item(result);
        }
        html_results += '</div>';

        this.result_container.html(html_results)
    };

    render_item(item) {
        let tpl = TEMPLATES[item.ctype] || TEMPLATES.default;
        return nunjucks.renderString(tpl, item);
    };

    select_item(item) {

        if (this.debug) console.debug('AutocompleteWidget: select_item', item);

        this.text_input.val(item.value);
        this.hidden_input.val(item.id);
        this.current_value = item.value;
        this.current_id = item.id;

        this.set_results([]);

    };
}


class AutocompleteWidgets {

    /******************************************************************
     * initializes autocomplete-widget on respective items
     ******************************************************************/

    constructor(opts) {

        this.debug = opts.debug || false;
        this.widgets = [];

        if (this.debug) console.group('AutocompleteWidgets');

        $('[data-autocomplete-widget-url]').each((i, item) => {
            const container = $(item).parent();
            this.widgets.push(
                new AutocompleteWidget(container, opts)
            )
        });

        if (this.debug) console.group('num. widgets initialized', this.widgets.length);

        if (this.debug) console.groupEnd();
    };
}

module.exports = AutocompleteWidgets;
