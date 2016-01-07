###
  a wrapper around qtip for quick dialog handling
###


class DialogUI

  debug: true
  active: false
  container: false

  constructor: (@container) ->
    console.log 'DialogUI', @container

  show: (opts = {}) ->

    opts.title ?= '-'
    opts.body ?= '-'
    opts.buttons ?= false

    dialog = $('<div />').qtip
      content:
        #text: opts.body
        text: '...'
        title:
          text: opts.title
          button: true
      position:
        my: 'center'
        at: 'center'
        target: $(window)
      show:
        ready: true
        modal:
          on: true
          blur: true
      hide: false
      style: 'dialog dialog-base'
      events:
        render: (event, api) ->
          return
        hide: (event, api) ->
          api.destroy()
          return

    api = dialog.qtip 'api'

    opts.body = $(opts.body)
    if opts.buttons

      action_container = $('<div class="actions"></div>')

      $(opts.buttons).each (i, el) ->
        if el.class
          extra_class = el.class
        else
          extra_class = 'btn-primary'
        button = $("<a class='btn btn-small #{extra_class}'>#{el.label}</a>")
        if el.callback
          button.on 'click', el.callback
        if el.hide
          button.on 'click', api.hide
        action_container.append button

      opts.body.append(action_container)

    api.set 'content.text', opts.body

    return api
