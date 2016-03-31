var EditBaseUI;

EditBaseUI = (function() {
  EditBaseUI.prototype.debug = false;

  EditBaseUI.prototype.active = false;

  function EditBaseUI(container) {
    this.container = container;
    if (this.debug) {
      console.log('EditBaseUI', this.container);
    }
  }

  return EditBaseUI;

})();
