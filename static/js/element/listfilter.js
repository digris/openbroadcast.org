import store from 'store';
import LazyImageLoader from "../utils/lazy-image-loader";

const DEBUG = false;
const STORE_KEY = 'ui-listfilter-expanded';

class ListFilter {

    constructor() {
        this.expanded_filters = [];
        this.load_state();
        this.bindings();
    };

    bindings() {
        // $(document).on('page:change', (e) => {
        //     this.set_counters();
        // });
        $(document).on('click', '[data-listfilter] .header', (e) => {
            let el = $(e.currentTarget).parents('[data-listfilter]');
            let key = el.data('listfilter');
            this.toggle_filter(key);

        });
    };
    toggle_filter(key) {

        let _expanded = this.expanded_filters;

        let index = _expanded.indexOf(key);

        if (index === -1) {
            _expanded.push(key);
        } else {
            _expanded.splice(index, 1);
        }

        this.expanded_filters = _expanded;
        this.save_state();

    };
    load_state() {
        this.expanded_filters = store.get(STORE_KEY, []);
        this.apply_state();
    };
    save_state() {
        store.set(STORE_KEY, this.expanded_filters);
        this.apply_state();
    };
    apply_state() {

        if (DEBUG) console.log('state:', this.expanded_filters);

        $('[data-listfilter]').each((i, item) => {
            let el = $(item);
            if(this.expanded_filters.includes(el.data('listfilter'))) {
                el.addClass('expanded');
            } else {
                el.removeClass('expanded');
            }

        });
    };

}

export default ListFilter;
