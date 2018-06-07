/*
 * BASE JAVASCRIPT
 * Functions defined here, global ones get called in js/init.php through "$(document).ready(function()"
 * However, the init functions can be modifyed in the application / templateing flow.
 */


/* core */
var base = base || {};
base.ui = base.ui || {};

base.ui.use_effects = true;

/* addons */
sm2 = function () {
};


$.cookie.defaults = {};

UiStates = function () {

    var self = this;
    this.css_selector = '.ui-persistent';
    this.cookie_name = 'ui_states_shared';
    this.values = new HashTable();

    // load states from cookie to hash-table
    this.load = function () {


        if ($.cookie(this.cookie_name)) {
            self.values.items = JSON.parse($.cookie(this.cookie_name));
        }

        this.apply_states();
    },
        this.get_states = function (key) {

            $.log('get_states: ' + key);

            if (key !== undefined) {
                return self.values.getItem(key);
            } else {
                return false;
            }

        },
        this.apply_states = function (key) {



            if (key !== undefined) {
                alert('not implemented');
            } else {
                $(this.css_selector).each(function (i, el) {

                    var id = $(el).attr('id');
                    var state = self.values.getItem(id);

                    // check if custom update rules apply for the element
                    if (base.ui.states_custom_update(id, state)) {
                        return;
                    }

                    // else do the default actions..
                    if (state == 'expanded') {
                        $(el).show();
                    }
                    ;
                    if (state == 'hidden') {
                        $(el).hide();
                    }
                    ;

                });
            }
        },

        // set specific state or loop through persistent items
        this.set_states = function (key, value) {

            $.log('set_states: ' + key + ' - ' + value);

            if (key !== undefined && value !== undefined) {
                self.values.setItem(key, value);
            } else {
                $(this.css_selector).each(function (i, el) {
                    self.values.setItem($(el).attr('id'), $(el).data('uistate'));
                });
            }
            $.log(['(set_states) current states', self.values.items]);
        },
        // save states to cookie
        this.save = function () {
            $.cookie(this.cookie_name, JSON.stringify(self.values.items), { expires: 7, path: '/' });
        }
};

BaseUi = function () {

    var self = this;

    this.states = new UiStates();

    this.init = function () {

        $('.ui-persistent').watch('uistate', function () {
            var state = $(this).data('uistate');

            console.debug(state)

            self.states.set_states($(this).attr('id'), state);
            self.states.apply_states();

        });


        this.states.load();
    };

    this.unload = function () {
        this.states.save();
    }
};


base.ui = new BaseUi();


base.ui.states_custom_update = function (id, state) {

    var el = $('#' + id);

    if (id == 'tagcloud_inline') {

        if (state == 'expanded') {
            $('#tagcloud_inline_toggle').addClass('active');
            el.css('display', 'block');
        }
        if (state == 'hidden') {
            $('#tagcloud_inline_toggle').removeClass('active');
            el.css('display', 'none');
        }

        return true;
    }

    if (id == 'playlist_basket') {

        if (state == 'expanded') {
            el.addClass('expanded');
        }
        if (state == 'hidden') {
            el.removeClass('expanded');
        }

        return true;
    }

    if (id == 'jingle_basket') {

        if (state == 'expanded') {
            el.addClass('expanded');
        }
        if (state == 'hidden') {
            el.removeClass('expanded');
        }

        return true;
    }

    if (id == 'default_jingle_set') {
        el.data('resource_uri', state);
        return true;
    }


    if (id.substring(0, 9) == 'filterbox') {

        if (state == 'expanded') {
            el.addClass('boxon');
            el.parent().addClass('boxon');
            $('.boxcontent', el.parent()).show();
        }
        if (state == 'hidden') {
            el.removeClass('boxon');
            el.parent().removeClass('boxon');
            $('.boxcontent', el.parent()).hide();
        }

        return true;
    }


    if (id == 'editor_mode') {

        $('body').removeClass('editor-mode-s');
        $('body').removeClass('editor-mode-m');
        $('body').removeClass('editor-mode-l');
        $('body').addClass('editor-mode-' + state);

        return true;
    }

    return false;

};


function HashTable(obj) {
    this.length = 0;
    this.items = {};
    for (var p in obj) {
        if (obj.hasOwnProperty(p)) {
            this.items[p] = obj[p];
            this.length++;
        }
    }

    this.setItem = function (key, value) {
        var previous = undefined;
        if (this.hasItem(key)) {
            previous = this.items[key];
        }
        else {
            this.length++;
        }
        this.items[key] = value;
        return previous;
    }

    this.getItem = function (key) {
        return this.hasItem(key) ? this.items[key] : undefined;
    }

    this.hasItem = function (key) {
        return this.items.hasOwnProperty(key);
    }

    this.removeItem = function (key) {
        if (this.hasItem(key)) {
            previous = this.items[key];
            this.length--;
            delete this.items[key];
            return previous;
        }
        else {
            return undefined;
        }
    }

    this.keys = function () {
        var keys = [];
        for (var k in this.items) {
            if (this.hasItem(k)) {
                keys.push(k);
            }
        }
        return keys;
    }

    this.values = function () {
        var values = [];
        for (var k in this.items) {
            if (this.hasItem(k)) {
                values.push(this.items[k]);
            }
        }
        return values;
    }

    this.each = function (fn) {
        for (var k in this.items) {
            if (this.hasItem(k)) {
                fn(k, this.items[k]);
            }
        }
    }

    this.clear = function () {
        this.items = {}
        this.length = 0;
    }
};


/* AJAX Indicator */
base.ui.loading = function () {
    $(document).ajaxStart(function () {
        $('body').addClass('ajax_loading');
    }).ajaxStop(function () {
            $('body').removeClass('ajax_loading');
        });
};

/*
 * Periodical UI refresh frequency degrades continuosely
 */
base.ui.refresh = function () {
    // sections to refresh
    $('#refresh').smartupdater({
        url: '/ui/refresh',
        minTimeout: 10000,
        multiplier: 2
    }, function (data) {
        $.taconite(data);
    });
};



/*
 * global interface things
 */
base.ui.iface = function () {


    Boxy.DEFAULTS.title = '&nbsp;';


    if (window.console && console.firebug) {
        console.warn('You should disable firebug, else performance can be very low!');
    }


    $('.tooltipable').tooltip({delay: { show: 50, hide: 10 }});


    $('.hoverable').live('mouseenter', function (e) {
        $(this).addClass('hover');
    });

    $('.hoverable').live('mouseleave', function (e) {
        $(this).removeClass('hover');
    });

    $('.linkable').live('click', function (e) {
        var href = $('a.link-main', this).attr('href');
        window.location.href = href;
    });
    //$('.autocomplete.result').load('http://local.openbroadcast.org:8000/en/content/library/releases/autocomplete/?q=second');


    // translate link to post (eg delete items)
    $('a.transform-post.reload').live('click', function (e) {

        e.preventDefault();
        var href = $(this).attr('href');
        $.post(href, function (d) {
        });

        $(this).parents('.item').hide(300);

    });


    // Cange display depending on applicatinos focus
    jQuery(window).bind("focus",function (event) {

        if (base.ui.use_effects) {
            $('body').animate({opacity: 1}, {queue: true, duration: 200});
        } else {
            $('body').css('opacity', 1);
        }
        $('body').removeClass('blur');


    }).bind("blur", function (event) {

            if (base.ui.use_effects) {
                // $('body').animate({opacity:0.1},{queue:true,duration:200});
            } else {
                // $('body').css('opacity', 0.1);
            }
            $('body').addClass('blur');

        });


    // Prevent disabled / locked clicks
    $('.action a').live('click', function (e) {
        if ($(this).parents('li').hasClass('disabled') || $(this).parents('li').hasClass('locked')) {
            alert('Action not allowed');
            e.stopPropagation();
            return false;
        }
    });

    // add class to external links
    $('body').bind('DOMSubtreeModified', function (e) {
        try {
            if (e.target.innerHTML.length > 0) {
                $("a:not(.skip-external)").filter(function () {
                    return this.hostname && this.hostname !== location.hostname;
                })
                    .addClass('external')
                    // .attr("target","_blank")
                ;
            }
        } catch (e) {

        }
    });


    /*
     * delete selected item
     */
    $('.action.selection_delete a').live('click', function (e) {

        var item_type = $(this).attr('href').substring(1);

        items = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            items.push({item_type: item_type, item_id: item_id, format: 'mp3'});


        });

        // Request url
        var url = base.vars.base_url + 'ajax/items_delete';

        // Request data
        var data = {
            items: items
        };

        base.ui.ajax(url, data);

        return false;
    });


    /*
     * Handlers in dialog window actions and ajax call
     */
    $('.boxy-wrapper .inline.merge a.merge').live('click', function () {

        var master_id = $('input[name=merge_master_id]:checked').val();
        var item_type = $('input[name=item_type]').val();

        item_ids = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            if (item_id != master_id) {
                item_ids.push(item_id);
            }
        });

        // Request url
        var url = base.vars.base_url + 'ajax/items_merge';

        // Request data
        var data = {
            master_id: master_id,
            item_ids: item_ids.join(','),
            item_type: item_type,
            action: 'reload'
        };

        // AJAX Call
        base.ui.ajax(url, data);

        Boxy.get(this).hide();

        return false;
    });


    /*
     * Reassign selected items
     * Basically this is for tracks -> create new release out of selection
     */

    /*
     * Dialog opening and parameter collection
     */
    $('.action.selection_reassign a').live('click', function () {

        if ($(this).hasClass('disabled')) {
            return false;
        }

        var item_type = $(this).attr('href').substring(1);

        item_ids = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            item_ids.push(item_id);
        });

        // Request url
        var url = '/ui/items_reassign?item_type=' + item_type + '&item_ids=' + item_ids.join(',');

        boxy = new Boxy.load(url, { modal: true });
        return boxy;

        return false;
    });

    /*
     * Handlers in dialog window actions and ajax call
     */
    $('.boxy-wrapper .inline.reassign a.reassign').live('click', function () {

        var create_name = $('input[name=release_name]').val();

        item_ids = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            item_ids.push(item_id);
        });

        // Request url
        var url = base.vars.base_url + 'ajax/items_reassign';

        var item_type = base.vars.subset.slice(0, -1);

        // Request data
        var data = {
            create_name: create_name,
            item_ids: item_ids.join(','),
            item_type: item_type
        };

        // AJAX Call
        base.ui.ajax(url, data);

        Boxy.get(this).hide();

        return false;
    });


    /*
     * Play multiple items
     * This function is not really nice... just here as it could be handy
     * (It also is not a requirement. If it does not work it just will be removed)
     */
    $('.action.selection_play a').live('click', function () {

        if ($(this).hasClass('disabled')) {
            return false;
        }

        var item_type = $(this).attr('href').substring(1);

        var uri = base.vars.base_url + 'multiplay/play.json?' + item_type + '_ids=';

        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            uri = uri + item_id + ',';
            if (base.ui.use_effects) {
                $(this).effect("transfer", { to: "#pplayer_inline" }, 300);
            }

        });

        var offset = 0;
        var mode = 'replace';
        var token = 'xx-yy-zz';

        base.ui.play_popup(uri, token, offset, mode);

        return false;
    });



    /*
     * Collect multiple items
     */
    $('.action.selection_collect a').live('click', function () {

        if ($(this).hasClass('disabled')) {
            return false;
        }

        var item_type = $(this).attr('href').substring(1);

        items = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            items.push({item_type: item_type, item_id: item_id, format: 'default'});

            if (base.ui.use_effects) {
                $(this).effect("transfer", { to: ".playlist.basket" }, 300);
            }

        });

        // Request url
        var url = base.vars.base_url + 'ajax/collect';

        // Request data
        var data = {
            items: items
        };

        // AJAX Call
        $.ajax({
            url: url,
            type: "POST",
            data: data,
            dataType: "json",
            success: function (result) {
                if (true == result['status']) {
                    $('#element').load('/ui/sidebar_playlist' + '?r=' + util.string_random(20));
                } else {
                    base.ui.ui_message(result['message']);
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                base.ui.ui_message(errorThrown);
            }
        });


        return false;
    });


    /*
     * Text shortener
     */
    $('.shorten').shorten();


    /*
     * Action handling (class="action")
     * For sitemessages
     */
    $('#sitemessages .message a.action').live('click', function () {

        // extract the action/attr - eg: #seen:231
        var attr = $(this).attr('href').substr(1).split(':');

        var context = 'messages';
        var command = attr[0];
        var id = attr[1];

        base.ui.ajax_action(context, command, id);

        return false;
    });


    /* Preview / ToolTips */
    /*
     $('div.list_body_item ul li a').qtip({
     position: {
     corner: {
     target: 'bottomLeft',
     tooltip: 'topLeft'
     }
     }
     });
     */


    // Clear input "on focus"
    $.fn.on_focus_input = function () {
        return this.focus(function () {
            $(this).addClass('focus');
            $(this).removeClass('blur');
            if (this.value == this.defaultValue) {
                this.value = "";
            }
        }).blur(function () {
                $(this).removeClass('focus');
                $(this).addClass('blur');
                if (!this.value.length) {
                    this.value = this.defaultValue;
                }
            });
    };


    /* Feedback tab */

    $('div.slideout.base').css('display', 'block');

    $('#feedback_submit').click(function () {

        var topic = $('div.slideout.base select[name=topic]').val();
        var subject = $('div.slideout.base input[name=subject]').val();
        var message = $('div.slideout.base textarea[name=message]').val();
        var from = $('div.slideout.base input[name=from]').val();
        var location = $('div.slideout.base input[name=location]').val();
        var request = $('div.slideout.base input[name=request]').val();

        $('div.slideout.base textarea, div.slideout.base select, div.slideout.base input').removeClass('error');

        if (topic && subject && message && from) {

            // Request url
            var url = base.vars.base_url + 'ajax/feedback_send';

            // Request data
            var data = {
                topic: topic,
                subject: subject,
                message: message,
                from: from,
                location: location,
                request: request
            };

            // AJAX Call
            $.ajax({
                url: url,
                type: "POST",
                data: data,
                dataType: "json",
                success: function (result) {
                    if (true == result['status']) {
                        $('.inner.feedback').html(result['message']);
                    } else {
                        base.ui.ui_message(result['message']);
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    base.ui.ui_message(errorThrown);
                }
            });


        } else {
            if (!topic) {
                $('div.slideout.base select[name=topic]').addClass('error');
            }
            if (!subject) {
                $('div.slideout.base input[name=subject]').addClass('error');
            }
            if (!from) {
                $('div.slideout.base input[name=from]').addClass('error');
            }
            if (!message) {
                $('div.slideout.base textarea[name=message]').addClass('error');
            }
        }

        return false;
    });

    // limited lists
    $('dd.limit').on('click', 'a.toggle', function(e){
        e.preventDefault();
        $('.limited', $(this).parents('dd')).toggle();
    });

    // color on hover
    // refactored to css
    // // TODO: where to have this??
    // $('.listview.artists.l').on('mouseover', '.item', function(){
    //     var src = $(this).data('image_color');
    //     if (src != undefined) {
    //         //$(this).css('background-image', 'url(' + src + ')');
    //     }
    // })
    // $('.listview.artists.l').on('mouseout', '.item', function(){
    //     var src = $(this).data('image_bw');
    //     //$(this).css('background-image', 'url(' + src + ')');
    // })

    // preload color images
    $('.listview.artists.l .item').each(function(i){
        var src = $(this).data('image_color');
        if (src != undefined) {
            //$('<img/>')[0].src = src;
        }
    });




    // form reset
    $('form').on('click', 'button:reset', function(e){
        $('body').css('opacity', 0.5);
        e.preventDefault();
        e.stopPropagation();
        document.location.href = document.location.href;
        return false;
    });





};


/*
 * General AJAX Action/command call
 */
base.ui.ajax_action = function (context, command, id) {

    // Request url
    var url = base.vars.base_url + 'ajax/' + context + '/' + command + '/' + id;

    // Request data
    var data = {
        command: command,
        id: id
    };

    var result = false

    // AJAX Call
    $.ajax({
        url: url,
        async: false,
        type: "POST",
        data: data,
        dataType: "json",
        success: function (result) {
            if (true == result['status']) {
                if (false != result['message']) {
                    base.ui.ui_message(result['message'], 10000);
                }


                // some post actions
                switch (result['post_action']) {
                    case 'message_remove':
                        $('#sitemessages #message_' + id).fadeOut();
                }


            } else {
                if (false != result['message']) {
                    base.ui.ui_message(result['message']);
                }
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            base.ui.ui_message(errorThrown);
        }
    });

};


base.ui.skeleton = function () {
    // info panel
    $('a.action.beta_notes').live('click', function (event) {

        var uri = $(this).attr('href').substr(1);

        if ($('#slider_top').hasClass('open')) {
            $('#slider_top').removeClass('open');
            $('#slider_top').fadeOut();
            $('#slider_top').html('');
        } else {
            $('#slider_top').addClass('open');
            $('#slider_top').fadeIn();
            $('#slider_top').load('/static/element/' + uri);
        }

        return false;
    });
};

/* top navigation aka toolbar
TODO: remove when new navigation is implemented
base.ui.toolbar = function () {


    $('a', 'ul.navigation-main').live('click', function (e) {
        e.preventDefault();
        var section = $(this).parent().attr('id').substring(9);
        $('ul.navigation-sub').hide();
        $('ul#nav_sub-' + section).show();

        return false;
    });

    $('.navigation-sub > li.descendant').parent().css('display', 'block');
    $('.navigation-sub > li.selected').parent().css('display', 'block');
    $('.navigation-sub > li.ancestor').parent().css('display', 'block');

    $("#toolbar #username").on_focus_input();
    $("#toolbar #password").on_focus_input();

    $(".nav_sub a.chat_irc").live('click', function (e) {
        e.preventDefault();
        uri = base.vars.irc_chat_url + '&nick=' + base.vars.username;

        var chat_win = window.open('', 'chat', 'width=650, height=720');

        if (chat_win) {
            // load the player page if necessary
            if (typeof (chat_win.loaded) == 'undefined') {
                chat_win.location.href = uri;
            }

        } else {
            alert('sorry - chat could not be loaded');
        }

        chat_win.focus();
        return false;

    });

};
*/
AutocompleteApp = function () {

    var self = this;
    this.api_url;
    this.container;
    this.ct;
    this.template = 'alibrary/nj/release/autocomplete.html';
    this.q_min = 3;

    this.search = function (q) {

        if (q.length >= this.q_min) {
            $.get(this.api_url + '?q=' + q, function (data) {
                self.display(data);
            });
        } else {
            self.container.fadeOut(100)
            .queue(function(nxt) {
                $(this).html('');
                nxt();
            });
        }
    };

    this.display = function (data) {
        html = nj.render(self.template, data);
        self.container.html(html).fadeIn(50);
    };

    this.close = function () {
        self.container.html('');
    };

};

base.ui.searchbar = function () {

    var self = this;

    var container = $('#searchbar');
    var ct = container.data('ct');



    this.autocomplete = new AutocompleteApp();
    this.autocomplete.ct = ct;
    this.autocomplete.template = 'alibrary/nj/' + ct + '/autocomplete.html';

    // hackish, map for non-library items
    if (ct == 'profile') {
        this.autocomplete.template = 'profiles/nj/' + ct + '/autocomplete.html';
    }

    // hackish api mapping :(
    if(ct == 'media') {
        ct = 'track';
    }

    // hackish - endpoint switch :(
    var entity = 'library/'
    if(ct == 'profile') {
        entity = '';
    }


    this.autocomplete.api_url = '/api/v1/' + entity + ct + '/autocomplete/';
    this.autocomplete.container = $('#autocomplete_holder');


    // search & Submit on 'ENTER'
    // refactored version with delay
    $(container).on('keyup', '#searchbar_input', function (e) {

        var el = $(this);
        var q = $(this).val();
        // catch enter
        if (e.keyCode == 13 || e.keyCode == 9) {
            var uri = util.uri_param_insert(window.location.href, 'q', q, true);
            window.location = util.uri_param_insert(uri, 'page', 1, true);
            return false;
        }
        // catch esc
        if (e.keyCode == 27) {
            $('#searchbar_input').val('')
            self.autocomplete.close();
            return false;
        }

        // autocomplete
        util.delay(function(){
            self.autocomplete.search(q);
        }, 500 );
    });
    $('#autocomplete_holder').on('click', 'a.exit', function (e) {
        $('#searchbar_input').val('')
        self.autocomplete.close();
    });







    $('a.tbtag.search').live('click', function (e) {
        if ($(e.target).is("input")) {
            e.preventDefault();
            return false;
        }
    });
    $('input.autosize').each(function () {
        $(this).attr("size", $(this).val().length);
    });
    $('input.autosize').autoGrowInput({
        comfortZone: 5,
        minWidth: 5,
        maxWidth: 170
    });


    // Remove hint on focus

    $("#searchbar_input").on_focus_input();


};

/* tagcloud (inline) */
base.ui.tagcloud = function () {

    $('a#tagcloud_inline_toggle').live('click', function (e) {

        e.preventDefault();

        var display = $('#tagcloud_inline').css('display');

        if (display == 'none') {
            $('#tagcloud_inline').data('uistate', 'expanded');
        }
        if (display == 'block') {
            $('#tagcloud_inline').data('uistate', 'hidden');
        }

    });

    $('.tag-level a', '#tagcloud_inline').live('click', function (e) {
        e.preventDefault();
        var level = $(this).data('taglevel');

        for (i = 1; i <= level; i++) {
            console.log('show:', i);
            $('a.level' + (i), '#tagcloud_inline').removeClass('tag-hidden');
        }

        for (i = 6; i > level; i--) {
            console.log('hide:', i);
            $('a.level' + (i), '#tagcloud_inline').addClass('tag-hidden');
        }

    });

    // aply "highlight" class for selected tag(s)
    $('#tagcloud_inline .cloud-container a.on').each(function(i, el){
        var tag_id = $(el).data('id');
        $('.listview .tags li[data-id="' + tag_id + '"]').addClass('active');
    });

};

/* sidebar */
base.ui.sidebar = function () {


    $('div.box div.boxtitle').live('click', function (e) {

        e.preventDefault();

        if (!$(this).hasClass('boxon')) {
            $(this).data('uistate', 'expanded');
        } else {
            $(this).data('uistate', 'hidden');
        }

    });


    /*
     * Releasedate custom range
     */
    $('.box select.range').live('change', function (e) {

        var key = $(this).attr('id');
        var value = $(this).val();

        var rel = base.vars.context + '_' + base.vars.section + '_' + base.vars.subset;
        var url = base.vars.base_url + 'ajax/filter_set_value';

        var active = $(this).parent().parent().find('a.filterbox_item').hasClass('on');
        var action = false;
        if (active) {
            action = 'reload';
        }

        var data = {
            'key': key,
            'rel': rel,
            'value': value,
            'action': action
        };

        // AJAX Call
        $.ajax({
            url: url,
            type: "POST",
            data: data,
            dataType: "json",
            success: function (result) {
                if (true == result['status']) {
                    if (result['message']) {
                        base.ui.ui_message(result['message'], 10000);
                    }
                    if (result['action'] == 'reload') {
                        window.location.reload();
                    }
                } else {
                    base.ui.ui_message(result['message']);
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                base.ui.ui_message(errorThrown);
            }
        });

        return false;

    });


    /*
     * Country artist
     */
    $('.box select.country').live('change', function (e) {

        var key = $(this).attr('id');
        var value = $(this).val();

        var uri = util.uri_param_insert(window.location.href, key, value, true);
        uri = util.uri_param_insert(uri, 'page', 1, true);

        window.location = uri;

        return false;

    });


    /*
     * Change sorting - key/direction
     */
    $('.box select.sorting').live('change', function (e) {

        e.preventDefault();
        var id = $(this).attr('id');
        var value = $(this).val();

        var key = false;

        switch (id) {
            case 'sort_key':
                key = 'order_by';
                break;
            case 'sort_direction':
                key = 'direction';
                break;
        }

        var uri = util.uri_param_insert(window.location.href, key, value, true);

        //alert(uri);
        window.location = uri;

        return false;
    });


    /*
     * Sidebar actions / bindings for the download-screen
     */

    $('.action.download_delete a').live('click', function () {

        if ($(this).hasClass('disabled')) {
            return false;
        }

        var range = false;

        if ($(this).parents('li').hasClass('delete_all')) {
            range = 'delete_all';
        }
        if ($(this).parents('li').hasClass('delete_completed')) {
            range = 'delete_completed';
        }

        // Request url
        var url = base.vars.base_url + 'ajax/downloads_delete';

        // Request data
        var data = {
            range: range,
            action: 'reload'
        };

        // AJAX Call
        $.ajax({
            url: url,
            type: "POST",
            data: data,
            dataType: "json",
            success: function (result) {
                if (true == result['status']) {
                    if (result['message']) {
                        base.ui.ui_message(result['message'], 10000);
                    }
                    if ('reload' == result['action']) {
                        window.location.reload();
                    }
                } else {
                    base.ui.ui_message(result['message']);
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                base.ui.ui_message(errorThrown);
            }
        });


        return false;
    });


    /*
     * Count box children and display next to box title
     * TODO: Consider moving styles to sass later
     */
    $('.sidebar .box').each(function (i, el) {

        var list = $(this).find('.boxcontent');


        var count_available = $('> div', list).size();
        var count_active = $('> div.minus', list).size();

        if (count_active > 0) {
            $(this).find('.boxtitle span').append('<span style="float: right"><span class="opt" style="text-align: right; color: #00BB00;">' + count_active + '</span><span class="opt" style="color: #999999;">/' + count_available + '</span>&nbsp;&nbsp;</span>');
            $(this).addClass('has_active');
        } else {
            $(this).find('.boxtitle span').append('<span style="float: right"><span class="opt" style="text-align: right; color: #999999;">' + count_active + '/' + count_available + '</span>&nbsp;&nbsp;</span>');
            $(this).removeClass('has_active');
        }
    });


};

base.ui.itemview = function () {

    // zoomable images
    var zoomable_defaults = {
        transition: "none",
        width: "520px",
        height: "520px"
    };
    $("a.zoomable").colorbox(zoomable_defaults);

    $("a.zoomable").hover(
        function () {
            $(this).addClass("hover");
        },
        function () {
            $(this).removeClass("hover");
        }
    );


    // rate
    var rate_defaults = {
        showHalf: true,
        path: '/media/css/img/raty/',
        score: 'rate_score'
    };

    $('.rate').raty(rate_defaults);


};

/* generic listview setup */
base.ui.listview = function () {

    /*
     * Listview - Style selector
     */

    /* moved to query variable
     $('div.listhead a.action.list_style').live('click', function() {

     var key = 'list_style';

     var value = false;
     if($(this).hasClass('s')) {
     value = 's';
     }
     if($(this).hasClass('m')) {
     value = 'm';
     }
     if($(this).hasClass('l')) {
     value = 'l';
     }

     var rel = base.vars.context + '_' + base.vars.section + '_' + base.vars.subset;
     var url = base.vars.base_url + 'ajax/filter_set_value';

     var	action = 'reload';

     var data = {
     'key' : key,
     'rel' : rel,
     'value' : value,
     'action' : action
     };

     // AJAX Call
     base.ui.ajax(url, data);

     return false;
     });
     */


    /*
     * Listview - row functions
     */

    // detail-click on image element
    $('div.item.clickable').on('click', '.spacer', function (e) {

        e.preventDefault();
        e.stopPropagation();

        var url = $(this).parents('.item').data('absolute_url');
        window.location.href = url;

    });



    // hover / -out
    $('div.listview.container div.list_body_row').hover(function (event) {
        $(this).addClass("hover");
    }, function (event) {
        $(this).removeClass("hover");
    });

    // select
    $('div.listview.container div.list_body_row.selectable').live('click', function (event) {

        if ($(event.target).is("a") || $(event.target).is("img") || $(event.target).is("i")) {
            // alert('no div');
        }
        else {
            $(this).toggleClass('selection');
            base.ui.listview.selection_update();
        }

    });

    // modify selection
    $('div.listview.footer #control_selection a.action').live('click', function (event) {
        var options = $(this).attr('href').substr(1).split(':');
        var context = options[0]; // not needed here
        var action = options[1];

        switch (action) {
            case 'invert':
                $('div.listview.container div.list_body_row.selectable.selection').addClass('selection_old');
                $('div.listview.container div.list_body_row.selectable').addClass('selection');
                $('div.listview.container div.list_body_row.selectable.selection_old').removeClass('selection').removeClass('selection_old');
                break;
            case 'all':
                $('div.listview.container div.list_body_row.selectable').addClass('selection');
                break;
            case 'clear':
                $('div.listview.container div.list_body_row.selectable').removeClass('selection');
                break;
        }

        base.ui.listview.selection_update();
        return false;
    });


    /*
     * Info display for 'large' view
     * refcatored to css3
     */
    /*
     $('div.listview.container.l div.list_body_row').hover(function(event) {

     var container = $(this);
     var spacer = $(this).find('div.spacer');
     spacer.animate({height:'52px'},{queue:true,duration:100});

     }, function(event) {

     var container = $(this);
     var spacer = $(this).find('div.spacer');
     spacer.animate({height:'150px'},{queue:true,duration:50});
     });
     */


    /*
     * Items per page (list footer)
     */
    /*
     $('div.ipp a').live('click', function(event) {

     var ipp = $(this).attr('href').substring(1);

     base.ui.save_state('ipp', ipp, 'reset_page');


     return false;
     });
     */


    // Highlighter
    if (base.vars.list_highlight) {
        var hls = base.vars.list_highlight.split(' ');
        for (i in hls) {
            $('.listview.container .list_body').highlight(hls[i]);
        }
    }


};
/*
 * Takes care about enabling / disabling resp. actions
 */
base.ui.listview.selection_update = function () {


    // reworked version
    // Create array out of selected elements
    var current_selection = [];
    $('div.list_body_row.selectable.selection').each(function () {
        var item_id = $(this).attr('id').split("_").pop();
        current_selection.push(item_id);
    });

    // Trigger ui update for elements that relay on selection count
    // disable all elements
    $('.action .selection-required').addClass('disabled');
    $('.action .selection-required.selection-multiple small').html('');
    $('.action .selection-required.selection-any small').html('');
    var count = current_selection.length;
    switch (count) {
        case 0:
            // nothing selected
            $('.action .selection-required').addClass('disabled');
            break;
        case 1:
            // only _one_ single item selected
            $('.action .selection-required.selection-single').removeClass('disabled');
            $('.action .selection-required.selection-any').removeClass('disabled');
            $('.action .selection-required.selection-any small').html(count);
            break;
        default:
            // multiple items selected
            $('.action .selection-required.selection-multiple').removeClass('disabled');
            $('.action .selection-required.selection-any').removeClass('disabled');
            $('.action .selection-required.selection-multiple small').html(count);
            $('.action .selection-required.selection-any small').html(count);
            break;
    }




    // Create array out of selected elements
    base.ui.listview.selection_current = [];
    $('div.listview.container div.list_body_row.selectable.selection').each(function () {
        var item_id = $(this).attr('id').split("_").pop();
        base.ui.listview.selection_current.push(item_id);
    });


    // Trigger ui update for elements that relay on selection count
    var selected_count = base.ui.listview.selection_current.length;
    // disable all elements
    $('.action.selection_required').addClass('disabled');
    $('.action.selection_required.selection_multiple span.opt').html('');
    $('.action.selection_required.selection_any span.opt').html('');
    switch (selected_count) {
        case 0:
            // nothing selected
            $('.action.selection_required').addClass('disabled');
            break;
        case 1:
            // only _one_ single item selected
            $('.action.selection_required.selection_single').removeClass('disabled');
            $('.action.selection_required.selection_any').removeClass('disabled');
            break;
        default:
            // multiple items selected
            $('.action.selection_required.selection_multiple').removeClass('disabled');
            $('.action.selection_required.selection_any').removeClass('disabled');
            $('.action.selection_required.selection_multiple span.opt').html('(' + selected_count + ')');
            $('.action.selection_required.selection_any span.opt').html('(' + selected_count + ')');
            break;
    }
};

base.ui.listview.selection_current = new Array;


/* generic tracklist setup */
base.ui.tracklist = function () {
    /*
     $('div.tracklist div.media').draggable( {
     // axis: 'y'
     });
     */
};

/* generic listview setup */
sm2.test = function (param) {

    $.playable(base.vars.js_path + 'lib/sm2/swf/', {
        debugMode: true
    });

    $('div.sm2').playable();

};

/* generic listview setup */
sm2.rtmp = function (param) {

    soundManager.url = '/media/js/lib/sm2/swf/';
    soundManager.useMovieStar = true;
    soundManager.flashVersion = 9;

    soundManager.debugMode = true;
    soundManager.debugFlash = true;

    soundManager.useConsole = true;
    soundManager.useHTML5Audio = true;

    soundManager.onready(function () {

        soundManager.createSound({
            id: 'rtmp_live',
            serverURL: 'rtmp://yoddha.anorg.net/recast/',
            url: 'mp3:obp.stream',
            autoPlay: true
        });

        /*
         * soundManager.createSound( { id : 'rtmp_live', serverURL :
         * 'rtmpt://stream01.test.digris.ch/streamAccess', url : 'mp3:demo.mp3',
         * autoPlay : true });
         */
    });

};


$.jGrowl.defaults.position = 'bottom-center';
base.ui.ui_message = function (message, life) {

    if (typeof(life) == 'undefined') {
        life = 2000;
    }

    $.jGrowl(message, {
        life: life
    });

    return true;
};


/*
 * Load & save UI states
 */
base.ui.load_state = function () {
    base.ui.state = $.cookie('ui_state');
    return true;
};

base.ui.save_state = function (key, val, action) {

    if (action === undefined) {
        action = "reload";
    }

    var url = base.vars.base_url + 'ui/state_save';
    var data = {
        key: key,
        val: val,
        action: action
    };

    $.ajax({
        url: url,
        type: "POST",
        data: data,
        dataType: "json",
        success: function (result) {
            if (true == result['status']) {
                if ('reload' == result['action']) {
                    window.location.reload();
                }
                if ('reset_page' == result['action']) {
                    var uri = util.uri_param_insert(window.location.href, 'page', 1, true);
                    window.location = uri;
                }
            } else {
                base.ui.ui_message(result['message']);
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });


};

/*
 * Popup-player handling
 */

base.ui.play = new Object;

base.ui.play_popup = function (uri, token, offset, mode) {

    if (mode === undefined) {
        mode = "replace";
    }
    if (offset === undefined) {
        offset = 0;
    }

    base.ui.play.uri = uri;
    base.ui.play.token = token;
    base.ui.play.offset = offset;
    base.ui.play.mode = mode;

    pplayer = base.ui.grab_player(true, true);

};

/*
 * This function is called in case the player was open before.
 * Tries to re-attach it to the main window
 */
base.ui.pplayer_do_grab = function () {
    pplayer = base.ui.grab_player(true, false);
};


/*
 * Player ready function, gets called either by the 'grap_player function' (if
 * existing player) or hrough the document ready function from the popup window
 */
base.ui.pplayer_ready = function (pplayer) {

    pplayer.load(base.ui.play.uri, base.ui.play.token, base.ui.play.offset, base.ui.play.mode);

    pplayer = pplayer;

    // save player state, so wen recall its object on subsequent requests
    // base.ui.save_state('pplayer_open', 1, false); // moved to server-side script
};

base.ui.pplayer_status = function (obj) {
    // $.log(obj.position);
    // $('#v15_experimental').html(obj.position);
};

// Function gets called by pplayer.ui.update() from the popup
base.ui.pplayer_update = function (item) {

    if (!item) {
        item = new Object;
        item.name = '';
        item.release = '';
        item.artist = '';
        item.id = 0;
        item.release_id = 0;
    }

    var name = (item.name != undefined) ? item.name : '';
    var release = (item.release != undefined) ? item.release : '';
    var artist = (item.artist != undefined) ? item.artist : '';


    // Update media-display
    $('#pplayer_inline_scroll .name').html('<a href="' + item.release_url + '">' + name + '</a>');
    $('#pplayer_inline_scroll .release').html('<a href="' + item.release_url + '">' + release + '</a>');
    $('#pplayer_inline_scroll .artist').html('<a href="' + item.artist_url + '">' + artist + '</a>');


    console.info('playing track', item.id)
    console.info('playing release', item.release_id)

    // try to set indicator for playing track
    $('.listview.container.medias .list_body_row').removeClass('playing');
    $('.listview.container.medias #list_item_' + item.id).addClass('playing');
    $('.listview.container.releases .list_body_row').removeClass('playing');
    $('.listview.container.releases #list_item_' + item.release_id).addClass('playing');

};
// Progress update
base.ui.pplayer_progress_update = function (sound) {
    // Just a dummy to test - maybe usefull somewhere in The Future™
    // $('.listview.container.medias .list_body_row.playing .c6').html(sound.position);
};


base.ui.grab_player = function (force, focus) {

    if (force === undefined) {
        force = false;
    }
    if (focus === undefined) {
        focus = false;
    }

    var pplayer_win = window.open('', 'pplayer', 'width=362, height=570');

    if (pplayer_win) {

        pplayer_win.opener = window;
        pplayer = pplayer_win.pplayer;

        // load the player page if necessary
        if (typeof (pplayer_win.loaded) == 'undefined') {
            pplayer_win.location.href = '/player';
        } else {
            if (pplayer && force) {
                // player is allready ready, so call pplayer_ready directly
                base.ui.pplayer_ready(pplayer);
            }
        }

    } else {

        // Show dialog
        var message = '<p><br />&nbsp;Unable to open the Player-window. Please set your browser to allow popups from this site.<br /><br /></p>';
        boxy = new Boxy(message);
    }

    if (focus) {
        pplayer_win.focus();
    }

    // little hackish - update the pplayer_inline
    try {
        var index = pplayer.sound_current.split("_").pop();

        // var item = pplayer.playlist[index];
        var item = pplayer.current_item;

        base.ui.pplayer_update(item);
    }
    catch (err) {

    }
    ;


    return pplayer;
};


/*
 * Dialog handling
 * Dialog is handled through two steps. base.ui.dialog_show() opens the dialog and loads the given
 * url into it. Then attach needed functionality to the content as needed. e.g. close can be used
 * generally in dialog content.
 */
base.ui.dialog = function (url, title) {

    // Generic 'close'
    $('.boxy-wrapper .close').live('click', function () {
        Boxy.get(this).hide();
        return false;
    });


    // Wrappers to load dialog content
    // Non-modal -> clear background
    $('a.dialog.info').live('click', function () {
        base.ui.dialog_show(false, $(this).attr('href'));
        return false;
    });
    // Modal -> darkened, inactive background
    $('a.dialog.modal').live('click', function () {
        base.ui.dialog_show(true, $(this).attr('href'));
        return false;
    });


};

base.ui.dialog_show = function (modal, url, title) {

    if (modal === undefined) {
        modal = false;
    }
    if (title === undefined) {
        title = '&nbsp;';
    }

    boxy = new Boxy.load(url, { modal: modal, closeText: 'X'});
    return boxy;

};

base.ui.dialog_static = function (dialog) {

    message = '<div class="message ' + dialog.type + '">' + dialog.message + '</div>';
    boxy = new Boxy(message, {title: dialog.title});
    return boxy;

};


/*
 * Download functions / Archiver
 */
/*
 base.ui.archiver = new Object;

 base.ui.archiver.enqueue = function() {
 $.log('base.archiver.prepare');
 }
 */

/*
 * AJAX wrapper
 * Generic UI ajax wrapper
 */
base.ui.ajax = function (url, data) {

    // Add to tracking queue
    if (base.vars.ga_track_events) {
        _gaq.push(['_trackEvent', 'AJAX', 'call', url]);
    }

    // AJAX Call
    $.ajax({
        url: url,
        type: "POST",
        data: data,
        dataType: "json",
        success: function (result) {

            if (true == result['status']) {
                // Display jGrowl message
                if (result['message']) {
                    base.ui.ui_message(result['message'], 10000);
                }
                // Display Dialog
                if (result['dialog']) {
                    base.ui.dialog_static(result['dialog']);
                }
                // Reload the current page
                if (result['action'] == 'reload') {
                    window.location.reload();
                }
                // Redirect to the given location
                if (result['redirect']) {
                    window.location = result['redirect'];
                }
                // Reset pageing counter to 1
                if ('reset_page' == result['action']) {
                    var uri = util.uri_param_insert(window.location.href, 'page', 1, true);
                    window.location = uri;
                }

            } else {
                if (result['message']) {
                    base.ui.ui_message(result['message']);
                }
                if (result['dialog']) {
                    base.ui.dialog_static(result['dialog']);
                }
            }

            // Provide a way to execute js
            if (result['eval']) {
                eval(result['eval']);
            }

        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            base.ui.ui_message(errorThrown);
        }
    });

};


$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};


/*


 // bind save() to window.onunload
 $(window).unload(function(){ base.ui.state.save('myLayout') });

 // DEFAULT LAYOUT SETTINGS
 var myDefaultSettings = {
 initClosed: true,
 west__size: 150,
 east__size: 150
 }

 var myLayout; // create global var for the layout-instance object

 $(document).ready( function() {
 // load & used 'saved-state' to override defaults
 myLayout = $("body").layout(
 $.extend( myDefaultSettings, base.ui.state.load('myLayout') )
 );
 });


 */
base.ui.state___ = {

    options: {
        layoutName: 'myLayout' // default name (optional)

        //	*** IMPORTANT *** specify your keys in same format as your layout options...
        /*	Sub-Key-Format State Options
         ,	keys:		'north.size,south.size,east.size,west.size,' +
         'north.isClosed,south.isClosed,east.isClosed,west.isClosed,' +
         'north.isHidden,south.isHidden,east.isHidden,west.isHidden'
         */
        //	Flat-Format State Options
        , keys: 'north__size,south__size,east__size,west__size,' +
            'north__isClosed,south__isClosed,east__isClosed,west__isClosed,' +
            'north__isHidden,south__isHidden,east__isHidden,west__isHidden'
        // Cookie Options
        , domain: '', path: '', expires: ''	// 'days' to keep cookie - leave blank for 'session cookie'
        , secure: false
    }, data: {}, clear: function (layoutName) {
        this.save(layoutName, 'dummyKey', { expires: -1 });
    }, save: function (layoutName, keys, opts) {
        var
            o = jQuery.extend({}, this.options, opts || {})
            , layout = window[ layoutName || o.layoutName ]
            ;
        if (!keys) keys = o.keys;
        if (typeof keys == 'string') keys = keys.split(',');
        if (!layout || !layout.state || !keys.length) return false;

        var
            isNum = typeof o.expires == 'number'
            , date = new Date()
            , params = ''
            , clear = false
            ;
        if (isNum || o.expires.toUTCString) {
            if (isNum) {
                if (o.expires <= 0) {
                    date.setYear(1970);
                    clear = true;
                }
                else
                    date.setTime(date.getTime() + (o.expires * 24 * 60 * 60 * 1000));
            }
            else
                date = o.expires;
            // use expires attribute, max-age is not supported by IE
            params += ';expires=' + date.toUTCString();
        }
        if (o.path)        params += ';path=' + o.path;
        if (o.domain)    params += ';domain=' + o.domain;
        if (o.secure)    params += ';secure';

        if (clear) {
            this.data = {}; // clear the data struct too
            document.cookie = (layoutName || o.layoutName) + '=' + params;
        }
        else {
            this.data = readState(layout, keys); // read current panes-state
            document.cookie = (layoutName || o.layoutName) + '=' + encodeURIComponent(JSON.stringify(this.data)) + params;
            //alert( 'JSON.stringify(this.data) = '+ (layoutName || o.layoutName) +'='+ JSON.stringify( this.data ) );
        }
        return this.data;

        // SUB-ROUTINE
        function readState(layout, keys) {
            var
                state = layout.state	// alias to the 'layout state'
                , data = {}
                , panes = 'north,south,east,west,center' // validation
                , alt = { isClosed: 'initClosed', isHidden: 'initHidden' }
                , delim = (keys[0].indexOf('__') > 0 ? '__' : '.')
                , pair, pane, key, val
                ;
            for (var i = 0; i < keys.length; i++) {
                pair = keys[i].split(delim);
                pane = pair[0];
                key = pair[1];
                if (panes.indexOf(pane) < 0) continue; // bad pane!
                if (key == 'isClosed') // if 'temporarily open' (sliding), then isClosed=false, so...
                    val = state[ pane ][ key ] || state[ pane ][ 'isSliding' ];
                else
                    val = state[ pane ][ key ];
                if (val != undefined) {
                    if (delim == '.') { // sub-key format
                        if (!data[ pane ]) data[ pane ] = {};
                        data[ pane ][ alt[key] ? alt[key] : key ] = val;
                    }
                    else // delim = '__' - flat-format
                        data[ pane + delim + (alt[key] ? alt[key] : key) ] = val;
                }
            }
            return data;
        }
    }, load: function (layoutName) {
        if (!layoutName) layoutName = this.options.layoutName;
        if (!layoutName) return {};
        var
            data = {}
            , c = document.cookie
            , cs, pair, i // loop vars
            ;
        if (c && c != '') {
            cs = c.split(';');
            for (i = 0; i < cs.length; i++) {
                c = jQuery.trim(cs[i]);
                pair = c.split('='); // name=value pair
                if (pair[0] == layoutName) { // this is the layout cookie
                    data = JSON.parse(decodeURIComponent(pair[1]));
                    break; // DONE
                }
            }
        }
        return (this.data = data);
    }

};
