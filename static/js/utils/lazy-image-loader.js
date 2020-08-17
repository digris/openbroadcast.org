import throttle from 'lodash.throttle';

// https://gist.github.com/jjmu15/8646226
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  const html = document.documentElement;
  return (
    rect.top >= 0
        && rect.left >= 0
        && rect.top <= (window.innerHeight || html.clientHeight)
        && rect.left <= (window.innerWidth || html.clientWidth)
  );
}

/** ********************************************************************
 * simple image loader
 ******************************************************************** */
class LazyImageLoader {
  constructor() {
    $(document).on('page:change paginate:complete', () => {
      this.processImages();
    });

    $(document).on('scroll', throttle(() => {
      this.processImages();
    }, 50));

    setTimeout(() => {
      this.processImages();
    }, 100);
  }

  // eslint-disable-next-line class-methods-use-this
  processImages() {
    $('.lazy-image').not('[data-lazy-image-loaded="1"]').each((i, el) => {
      if (!isInViewport(el)) {
        return;
      }

      const item = $(el);
      const src = item.data('src');
      const img = new Image();

      const imageLoaded = () => {
        img.removeEventListener('load', imageLoaded, true);
        item.attr('src', src);
        item.addClass('lazy-image--loaded');
      };

      img.src = src;
      img.addEventListener('load', imageLoaded, true);

      // set loaded attribute to exclude image for next run
      item.attr('data-lazy-image-loaded', '1');
    });
  }
}

export default LazyImageLoader;
