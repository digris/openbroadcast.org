import store from 'store';

const STORE_KEY = 'ui-tagcloud-expanded';

class Tagcloud {
  constructor() {
    this.expanded = store.get(STORE_KEY, false);
    this.container = $('#tagcloud');
    this.tagcloud_toggle = $('.tagcloud-toggle');
    this.bindings();

    if (this.expanded) {
      this.show(false);
    }
  }

  bindings() {
    this.tagcloud_toggle.on('click', () => {
      e.preventDefault();
      this.toggle(true);
    });
  }

  toggle(animate = false) {
    this.expanded = !this.expanded;
    if (this.expanded) {
      this.show(animate);
    } else {
      this.hide(animate);
    }
  }

  // eslint-disable-next-line no-unused-vars
  show(animate = false) {
    store.set(STORE_KEY, true);
    this.container.addClass('tagcloud--expanded');
    this.tagcloud_toggle.addClass('tagcloud-toggle--expanded');
  }

  // eslint-disable-next-line no-unused-vars
  hide(animate = false) {
    store.set(STORE_KEY, false);
    this.container.removeClass('tagcloud--expanded');
    this.tagcloud_toggle.removeClass('tagcloud-toggle--expanded');
  }
}

export default Tagcloud;
