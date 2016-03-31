###
  global ui functionality
###

ui = window.ui || {};

$ ->
  ui.dialog = new DialogUI
  ui.edit_base = new EditBaseUI

