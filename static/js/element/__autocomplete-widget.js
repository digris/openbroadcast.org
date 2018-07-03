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

    constructor(opts) {
        this.debug = opts.debug || false;
        this.bindings();
        this.navigation_keys = [
            13, 27, 38, 40
        ];
    };

    bindings() {

        if (this.debug) console.debug('AutocompleteWidget - bindings');

        const input_selector = '[data-autocomplete-widget-type="text"]';

        $(document).on('keydown', input_selector, (e) => {
            if(this.navigation_keys.includes(e.which)) {
                return this.handle_keys(e);
            }
        });

        $(document).on('keyup', input_selector, (e) => {

            const el = $(e.currentTarget);
            const q = el.val();
            const url = el.data('autocomplete-widget-url');

            if(! this.navigation_keys.includes(e.which)) {
                this.autocomplete(url, q, el);
            }

        });

        $(document).on('click', '.autocomplete-widget-results div', (e) => {
            this.select_item($(e.currentTarget));
        });

    };

    autocomplete(url, q, el) {

        if (this.debug) console.debug('AutocompleteWidget: query', q);

        const container = el.parent();

        let result_container = container.find('.autocomplete-widget-results');
        if(result_container.length < 1) {
            result_container = $('<div/>').addClass('autocomplete-widget-results');
            container.append(result_container)
        }

        api_client.get(url, {params: {q: q}})
            .then((response) => {
                if (this.debug) console.table(response.data.results);
                result_container.html('');
                for (let item of response.data.results) {
                    result_container.append(this.render_item(item));
                }
            }, (error) => {
                result_container.html('');
            })
    };

    handle_keys(e) {
        // handle special keys (up, down, esc, return)

        const el = $(e.currentTarget);
        const container = el.parent();
        const results_container = container.find('.autocomplete-widget-results');
        let selected_index = $('[data-id].selected', results_container).index();

        // down
        if(e.which === 40) {
            if($('[data-id]', results_container).length -1 > selected_index) {
                selected_index++;
            }
        }

        // up
        if(e.which === 38) {
            if(selected_index >= 0) {
                selected_index--;
            }
        }

        $('[data-id]', results_container).each((i, item) => {
            if(i === selected_index) {
                $(item).addClass('selected');
            } else {
                $(item).removeClass('selected');
            }
        });

        // esc
        if(e.which === 27) {
            results_container.html('')
        }

        // return
        if(e.which === 13) {
            if(selected_index > -1) {
                $('[data-id].selected', results_container).click();
                results_container.html('')
            } else {
                container.find('[data-autocomplete-widget-type="hidden"]').val('');
                results_container.html('');
            }
        }

        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        return;
    };

    render_item(item) {
        let tpl = TEMPLATES[item.ctype] || TEMPLATES.default;
        return nunjucks.renderString(tpl, item);
    };

    select_item(el) {

         if (this.debug) console.debug('AutocompleteWidget: select_item', el);

         const data = el.data();
         const container = el.parents('.controls');
         const results_container = container.find('.autocomplete-widget-results');

         container.find('[data-autocomplete-widget-type="text"]').val(data.value);
         container.find('[data-autocomplete-widget-type="hidden"]').val(data.id);

         results_container.html('')

    };
}

module.exports = AutocompleteWidget;
