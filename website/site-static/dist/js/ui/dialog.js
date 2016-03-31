
/*
  a wrapper around qtip for quick dialog handling
 */
var DialogUI;

DialogUI = (function() {
  DialogUI.prototype.debug = false;

  DialogUI.prototype.active = false;

  DialogUI.prototype.container = false;

  function DialogUI(container) {
    this.container = container;
    if (this.debug) {
      console.log('DialogUI', this.container);
    }
  }

  DialogUI.prototype.show = function(opts) {
    var action_container, api, dialog;
    if (opts == null) {
      opts = {};
    }
    if (opts.title == null) {
      opts.title = '-';
    }
    if (opts.body == null) {
      opts.body = '-';
    }
    if (opts.buttons == null) {
      opts.buttons = false;
    }
    dialog = $('<div />').qtip({
      content: {
        text: '...',
        title: {
          text: opts.title,
          button: true
        }
      },
      position: {
        my: 'center',
        at: 'center',
        target: $(window)
      },
      show: {
        ready: true,
        modal: {
          on: true,
          blur: true
        }
      },
      hide: false,
      style: 'dialog dialog-base',
      events: {
        render: function(event, api) {},
        hide: function(event, api) {
          api.destroy();
        }
      }
    });
    api = dialog.qtip('api');
    opts.body = $(opts.body);
    if (opts.buttons) {
      action_container = $('<div class="actions"></div>');
      $(opts.buttons).each(function(i, el) {
        var button, extra_class;
        if (el["class"]) {
          extra_class = el["class"];
        } else {
          extra_class = 'btn-primary';
        }
        button = $("<a class='btn btn-small " + extra_class + "'>" + el.label + "</a>");
        if (el.callback) {
          button.on('click', el.callback);
        }
        if (el.hide) {
          button.on('click', api.hide);
        }
        return action_container.append(button);
      });
      opts.body.append(action_container);
    }
    api.set('content.text', opts.body);
    return api;
  };

  return DialogUI;

})();
