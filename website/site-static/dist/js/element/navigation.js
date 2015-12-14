var AccountUI, NavigationUI;

NavigationUI = (function() {
  NavigationUI.prototype.debug = true;

  NavigationUI.prototype.hover = false;

  NavigationUI.prototype.active = false;

  NavigationUI.prototype.hover_has_sublevel = false;

  NavigationUI.prototype.active_has_sublevel = false;

  NavigationUI.prototype.timeout = false;

  function NavigationUI(container) {
    this.container = container;
    this.active = this.container.find('> .selected, > .ancestor');
    this.active_has_sublevel = this.active.hasClass('has-sub-level');
    if (this.debug) {
      console.debug('active', this.active.length);
      console.debug('active has sublevel', this.active_has_sublevel);
    }
    this.update_display();
    this.bindings();
  }

  NavigationUI.prototype.bindings = function() {
    this.container.on('mouseover', '> li', (function(_this) {
      return function(e) {
        var target;
        target = $(e.currentTarget);
        _this.hover = target;
        target.addClass('hover');
        _this.hover_has_sublevel = _this.hover.hasClass('has-sub-level');
        clearTimeout(_this.timeout);
        return _this.update_display();
      };
    })(this));
    this.container.on('mouseout', '> li', (function(_this) {
      return function(e) {
        var target;
        target = $(e.currentTarget);
        target.removeClass('hover');
        return _this.timeout = setTimeout((function() {
          _this.hover = false;
          _this.hover_has_sublevel = false;
          return _this.update_display();
        }), 200);
      };
    })(this));
    this.container.on('mouseover', '> li li', (function(_this) {
      return function(e) {
        var target;
        target = $(e.currentTarget);
        return target.addClass('hover');
      };
    })(this));
    return this.container.on('mouseout', '> li li', (function(_this) {
      return function(e) {
        var target;
        target = $(e.currentTarget);
        return target.removeClass('hover');
      };
    })(this));
  };

  NavigationUI.prototype.update_display = function() {
    $('.sub-level', this.container).removeClass('hide');
    if (debug) {
      console.debug('active', this.active);
      console.debug('hover', this.hover);
      console.debug('active_has_sublevel', this.active_has_sublevel);
      console.debug('hover_has_sublevel', this.hover_has_sublevel);
    }
    if (this.hover) {
      $('.sub-level', this.container).css('visibility', 'hidden');
      if (this.hover_has_sublevel) {
        $('.sub-level', this.hover).css('visibility', 'visible');
      }
    } else {
      $('.sub-level', this.container).css('visibility', 'hidden');
      if (this.active_has_sublevel) {
        $('.sub-level', this.active).css('visibility', 'visible');
      }
    }
    return $('.sub-level', this.container).each(function(i, el) {
      var parent_offset;
      parent_offset = $(el).parent().position().left;
      console.debug(parent_offset);
      return $(el).css('padding-left', parent_offset + 'px');
    });
  };

  return NavigationUI;

})();

AccountUI = (function() {
  AccountUI.prototype.debug = true;

  function AccountUI(container) {
    this.container = container;
    this.bindings();
    this.update_display();
  }

  AccountUI.prototype.bindings = function() {
    this.container.on('mouseover', '> li', (function(_this) {
      return function(e) {
        var target;
        target = $(e.currentTarget);
        return target.addClass('hover');
      };
    })(this));
    return this.container.on('mouseout', '> li', (function(_this) {
      return function(e) {
        var target;
        target = $(e.currentTarget);
        return target.removeClass('hover');
      };
    })(this));
  };

  AccountUI.prototype.update_display = function() {
    return $('.sub-level', this.container).css('min-width', this.container.width());
  };

  return AccountUI;

})();
