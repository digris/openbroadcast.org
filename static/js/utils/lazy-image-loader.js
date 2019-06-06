import throttle from 'lodash.throttle';

/**********************************************************************
 * simple image loader
 *********************************************************************/
class LazyImageLoader {
    /**
     *
     * @param opts
     */
    constructor(opts) {

        $(document).on('page:change paginate:complete', (e) => {
            this.process_images();
        });

        $(document).on('scroll', throttle((e) => {
            this.process_images();
        }, 50));

        setTimeout(() => {
            this.process_images();
        }, 100)
    };

    /**
     *
     */
    process_images() {

        $('.lazy-image').not('[data-lazy-image-loaded="1"]').each((i, el) => {
            if (!isInViewport(el)) {
                return;
            }

            const item = $(el);
            const src = item.data('src');
            const img = new Image();

            const image_loaded = (a, b, c, d) => {
                img.removeEventListener('load', image_loaded, true);
                item.attr('src', src);
                item.addClass('lazy-image--loaded');
            };

            img.src = src;
            img.addEventListener('load', image_loaded, true);

            // set loaded attribute to exclude image for next run
            item.attr('data-lazy-image-loaded', '1');

        });
    };
}

module.exports = LazyImageLoader;


// https://gist.github.com/jjmu15/8646226
function isInViewport(element) {
    let rect = element.getBoundingClientRect();
    let html = document.documentElement;
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.top <= (window.innerHeight || html.clientHeight) &&
        rect.left <= (window.innerWidth || html.clientWidth)
    );
}
