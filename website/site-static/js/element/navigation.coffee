class NavigationUI

  debug: true
  hover: false
  active: false
  hover_has_sublevel: false
  active_has_sublevel: false
  timeout: false


  constructor: (@container) ->
    #@update_display()
    #@bindings()
    @active = @container.find '> .selected, > .ancestor'
    @active_has_sublevel = @active.hasClass 'has-sub-level'

    if @debug
      console.debug 'active', @active.length
      console.debug 'active has sublevel', @active_has_sublevel

    @bindings()


  bindings: ->

    # first level
    @container.on 'mouseover', '> li', (e) =>
      target = $(e.currentTarget)
      @hover = target
      target.addClass 'hover'
      @hover_has_sublevel = @hover.hasClass 'has-sub-level'
      clearTimeout @timeout
      @update_display()

    @container.on 'mouseout', '> li', (e) =>
      target = $(e.currentTarget)
      target.removeClass 'hover'
      @timeout = setTimeout ( =>
        @hover = false
        @hover_has_sublevel = false
        @update_display()
      ), 200

    # sub-levels
    @container.on 'mouseover', '> li li', (e) =>
      target = $(e.currentTarget)
      target.addClass 'hover'

    @container.on 'mouseout', '> li li', (e) =>
      target = $(e.currentTarget)
      target.removeClass 'hover'


  update_display: ->

    if debug
      console.debug 'active', @active
      console.debug 'hover', @hover
      console.debug 'active_has_sublevel', @active_has_sublevel
      console.debug 'hover_has_sublevel', @hover_has_sublevel

    if @hover
      $('.sub-level', @container).css('visibility', 'hidden')
      if @hover_has_sublevel
        $('.sub-level', @hover).css('visibility', 'visible')

    else
      $('.sub-level', @container).css('visibility', 'hidden')
      if @active_has_sublevel
        $('.sub-level', @active).css('visibility', 'visible')


class AccountUI

  debug: true

  constructor: (@container) ->
    @bindings()
    @update_display()


  bindings: ->

    @container.on 'mouseover', '> li', (e) =>
      target = $(e.currentTarget)
      target.addClass 'hover'

    @container.on 'mouseout', '> li', (e) =>
      target = $(e.currentTarget)
      target.removeClass 'hover'

  update_display: ->

    $('.sub-level', @container).css('min-width', @container.width())

