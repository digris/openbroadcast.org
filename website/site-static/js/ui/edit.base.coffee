class EditBaseUI

  debug: false
  active: false

  constructor: (@container) ->
    if @debug
      console.log 'EditBaseUI', @container
    @autogrow_bindings()
    @autogrow_formset()

  autogrow_bindings: ->

    $('.form-autogrow', $('fieldset')).on 'blur', '.controls input', (e) =>
      @autogrow_formset()

  autogrow_formset: ->

    $('fieldset').each (i, el) ->
      j = 4
      $('.form-autogrow', $(el)).removeClass 'hidden'
      $('.form-autogrow', $(el)).each (i, el) ->
        value = $('.controls input', $(el)).val()
        if value.length > 0
          j++
        j--
        if j < 3
          $(el).addClass 'hidden'
