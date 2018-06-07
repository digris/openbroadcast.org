var EditBaseUI;

EditBaseUI = (function() {
  EditBaseUI.prototype.debug = false;

  EditBaseUI.prototype.active = false;

  function EditBaseUI(container) {
    this.container = container;
    if (this.debug) {
      console.log('EditBaseUI', this.container);
    }
    this.autogrow_bindings();
    this.autogrow_formset();
  }

  EditBaseUI.prototype.autogrow_bindings = function() {
    return $('.form-autogrow', $('fieldset')).on('blur', '.controls input', (function(_this) {
      return function(e) {
        return _this.autogrow_formset();
      };
    })(this));
  };

  EditBaseUI.prototype.autogrow_formset = function() {
    return $('fieldset').each(function(i, el) {
      var j;
      j = 4;
      $('.form-autogrow', $(el)).removeClass('hidden');
      return $('.form-autogrow', $(el)).each(function(i, el) {
        var value;
        value = $('.controls input', $(el)).val();
        if (value.length > 0) {
          j++;
        }
        j--;
        if (j < 3) {
          return $(el).addClass('hidden');
        }
      });
    });
  };

  return EditBaseUI;

})();
