class Topbar {
  constructor() {
    this.container = $('#main_menu');
    this.bindings();
    setTimeout(() => {
      this.show_submenu();
    }, 500);
  }

  bindings() {
    this.container.on('mouseover', '[data-level="0"]', (e) => {
      const el = $(e.currentTarget);
      const id = el.data('id');
      this.show_submenu(id);
    });
    this.container.on('mouseout', '[data-level="0"]', () => {
      this.show_submenu();
    });
  }

  show_submenu(id = null) {
    const active_parent_id = id || $('[data-level="0"].selected', this.container).data('id');
    $('[data-parent-id]', this.container).each((i, el) => {
      const item = $(el);
      const parent_id = item.data('parent-id');
      if (parent_id === active_parent_id) {
        const offset = item.parents('[data-id]').position();
        item.css('padding-left', `${offset.left + 10}px`).addClass('active');
        // item.parent().css('padding-left', `${offset.left + 10}px`).addClass('active');
      } else {
        item.removeClass('active');
        // item.parent().removeClass('active');
      }
    });
  }
}

export default Topbar;
