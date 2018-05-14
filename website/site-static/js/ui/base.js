
/*
  global ui functionality
 */
var ui;

ui = window.ui || {};

$(function() {
  ui.dialog = new DialogUI;
  return ui.edit_base = new EditBaseUI;
});
