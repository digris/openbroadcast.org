/*
 * EDIT JAVASCRIPT
 * probably split in edit.base.js and edit.ui.js later on
 */

/* core */
var edit = edit || {};
edit.base = edit.base || {};
edit.ui = edit.ui || {};

EditUi = function () {

    var self = this;

    this.lookup_prefix = 'lookup_id_';
    this.field_prefix = 'id_';

    this.is_ie6 = $.browser == 'msie' && $.browser.version < 7;

    this.lookup_data = null;
    this.lookup_offset = 0;

    this.current_data = {
        item_type: null,
        item_id: null,
        provider: null,
        query: null,
        uri: null
    };

    this.dialog_window = false;


    this.init = function () {
        self.bindings();
        self.iface();
    };

    this.iface = function () {
        this.floating_sidebar('lookup_providers', 120)
        self.autogrow();
    };


    this.autogrow = function(){
        // hide formsets until limit

        $('fieldset').each(function(i, el){
        var j = 4; // the limit
            $('.form-autogrow', $(el)).removeClass('hidden');
            $('.form-autogrow', $(el)).each(function(i, el){

                // get the input
                var value = $('.controls input', $(el)).val();
                if(value.length > 0) {
                    j++;
                }
                j--;

                if(j < 3){
                   $(el).addClass('hidden')
                };
            });
        });


    };

    this.bindings = function () {
        // lookup providers
        var container = $('.lookup.provider.listing');

        // handle autogrow
        $('.form-autogrow', $('fieldset')).on('blur', '.controls input', function(e){
            self.autogrow();
        });

        // handle links
        $(container).on('click', '.item a.external', function (e) {
            e.stopPropagation();
        });

        // handle actions
        $(container).on('click', '.item a.action', function (e) {

            e.stopPropagation();
            e.preventDefault();

            var item = $(this).parents('.item');

            var item_type = item.data('item_type');
            var item_id = item.data('item_id');
            var provider = item.data('provider');

            self.provider_search(item_type, item_id, provider);

        });


        $(container).on('click', '.item', function (e) {

            e.preventDefault();
            var item = $(this);

            var item_type = item.data('item_type');
            var item_id = item.data('item_id');
            var provider = item.data('provider');

            // check if provider set
            if (item.hasClass('available')) {

                // try to get api_url
                var api_url = false;
                $('fieldset.relations input[name^="relation"]').each(function(i, el){
                    if ($(this).val().toLowerCase().indexOf(provider) >= 0) {
                        api_url = $(this).val();
                    }
                });

                self.api_lookup(item_type, item_id, provider, api_url);
            } else {
                debug.debug('provider url not set');
            }
            // else show research dialog

        });


        // handle compare clicks
        $("[id^=" + self.lookup_prefix + "]").live('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            var el = $(this);
            self.apply_value(el);
            return false;
        });
        // allow clicks on parent element as well
        $("div.field-lookup-holder").live('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            // 'simulate' click in child element
            $('span', $(this)).click()
            return false;

        });




        $('.bulk_apply').live('click', function (e) {

            e.preventDefault();

            var id = $(this).attr('id');
            var key = id.substring(11); // strip off "bulk_apply_"

            console.log('bulk apply:', id, key)

            if (key == 'license') {
                var src_id = $("#id_bulkedit-bulk_license").val();
                var start = 'id_media'
                var end = 'license'
                var dst_id = $('[id^="' + start + '"][id$="' + end + '"]')
                if (!src_id) {
                    alert('Nothing selected.');
                    return;
                }
                dst_id.val(src_id);
            }



            if (key == 'artist_name') {

                console.log('bulk apply artist name');

                var src_id = $("#id_bulkedit-bulk_artist_name_1").val()
                var src_name = $("#id_bulkedit-bulk_artist_name_0").val()

                console.log('src_id', src_id, 'src_name', src_name);

                var dst_id = $('[id^="' + 'id_media' + '"][id$="' + 'artist_1' + '"]')
                var dst_name = $('[id^="' + 'id_media' + '"][id$="' + 'artist_0' + '"]')

                if (!src_name) {
                    alert('Nothing selected.');
                    return;
                }

                dst_id.val(src_id);
                dst_name.val(src_name);
            }

        });


        $('#search_dialog_container .item').live('mouseover', function () {
            $(this).addClass('hover');
        });

        $('#search_dialog_container .item').live('mouseout', function () {
            $(this).removeClass('hover');
        });

        $('#search_dialog_container .item').live('click', function () {

            var uri = $(this).data('uri');
            self.current_data = $.extend(self.current_data, {
                uri: uri
            });

            Dajaxice.alibrary.provider_update(function (data) {

                if (data) {
                    try {
                        var api = self.dialog_window.qtip('api');
                        api.destroy();
                    } catch (e) {
                    }
                    ;

                    // TODO: maybe make a bit nicer...
                    // set button classes
                    $(".item[data-provider='" + self.current_data.provider + "']", container).addClass('available');
                    $(".item[data-provider='" + self.current_data.provider + "']", container).removeClass('unavailable');


                    // replace link in form
                    if($('.external.' + self.current_data.provider).length) {

                        var field = $('.controls input', $('.external.' + self.current_data.provider)
                            .parents('.relation-row'))
                            .val(self.current_data.uri);

                    } else {
                        var _container = $('fieldset.relations .relation-row:not(".hidden")').last();
                        $('.controls input', _container).val(self.current_data.uri);
                        self.autogrow();
                    }

                    // TODO: refactor
                    // try to get api_url
                    var api_url = false;
                    $('fieldset.relations input[name^="relation"]').each(function(i, el){
                        if ($(this).val().toLowerCase().indexOf(self.current_data.provider) >= 0) {
                            api_url = $(this).val();
                        }
                    });

                    self.api_lookup(
                        self.current_data.item_type,
                        self.current_data.item_id,
                        self.current_data.provider,
                        api_url
                    )

                }

            }, self.current_data);

        });

        // search form
        $('#search_dialog_container .query .search').live('click', function () {
            var query = $('#search_dialog_container .query .query').val();
            self.provider_search_update_dialog(query);
        });
        $('#search_dialog_container .query .query').live('keypress', function (e) {

            if (e.keyCode == 13) {
                e.preventDefault();
                e.stopPropagation();
                var query = $(this).val();
                self.provider_search_update_dialog(query);
            }
        });
        $('#search_dialog_container .query .exit').live('click', function () {
            try {
                var api = self.dialog_window.qtip('api');
                api.destroy();
            } catch (e) {
            }
        });



        // reset
        $('button.reset').live('click', function (e) {
            e.preventDefault();
            location.reload();
        });

        // shift offset (single, by click)
        $('#offset_selector a').live('click', function (e) {
            e.preventDefault();
            var offset = $(this).data('offset');
            if (offset == 'add') {
                self.lookup_offset++;
            } else if (offset == 'subtract') {
                self.lookup_offset--;
            }
            self.media_lookup(self.lookup_data);
        });


        // shift offset (via dropdown)
        $('#offset_selector .shift-offset select').live('change', function () {
            var offset = $(this).val();
            self.lookup_offset = parseInt(offset);
            self.media_lookup(self.lookup_data);
        });


        $('fieldset.relations').on('click', '.relation', function (e) {

            e.preventDefault();

            var el = $(this);

            if(el.hasClass('match')){
                return;
            }

            var url = el.data('url');

            if(el.parents('.lookup-container').length) {
                // if item is in generic container
                // find last 'unused' input & assign value
                var container = $('fieldset.relations .relation-row:not(".hidden")').last();
                $('.controls input', container).val(url);
                el.remove();

                // reqrow...
                self.autogrow();

            } else {
                // attached to a specific service
                var container = el.parents('.relation-url');
                $('.controls input', container).val(url);
                el.removeClass('diff');
                el.addClass('match');
            }

        });






    };


    /***************************************************************************************
     * Search & selection
     ***************************************************************************************/

    this.provider_search = function (item_type, item_id, provider) {
        debug.debug(item_type, item_id, provider);
        self.current_data = $.extend(self.current_data, {
            'item_type': item_type,
            'item_id': item_id,
            'provider': provider
        });

        // ask api what query string to use
        // exmple return: Human After All Daft Punk
        Dajaxice.alibrary.provider_search_query(function (data) {
            console.log('data:', data);
            if (data && data.query) {
                self.provider_search_dialog(data.query);
            }
        }, self.current_data);

    };

    // create dialog container
    this.provider_search_dialog = function (query) {


        try {
            var api = self.dialog_window.qtip('api');
            api.destroy();
        } catch (e) {
        }
        ;


        self.dialog_window = $('<div />').qtip({
            content: {
                text: function (api) {
                    return '<div id="search_dialog_container"><div class="loading-placeholder"><i class="icon-spinner icon-spin icon-large"></i> loading</div></div>'
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
                    blur: false
                }
            },
            hide: false,
            style: 'qtip-dark qtip-dialogue qtip-shadow qtip-rounded popup-actions popup-provider-search',
            events: {
                render: function (event, api) {
                    $('a.btn', api.elements.content).click(api.hide);
                }
            }
        });


        self.provider_search_update_dialog(query);

    };


    this.provider_search_update_dialog = function (query) {


        self.current_data = $.extend(self.current_data, {
            query: query
        });

        Dajaxice.alibrary.provider_search(function (data) {

            data.item_type = self.current_data.item_type;
            data.provider = self.current_data.provider;

            console.log('data:', data);

            var html = nj.render('alibrary/nj/provider/search_dialog.html', data);
            setTimeout(function () {
                $('#search_dialog_container').html(html);
            }, 100)

        }, self.current_data);

    };


    /***************************************************************************************
     * API comparison
     ***************************************************************************************/

    this.api_lookup = function (item_type, item_id, provider, api_url) {


        // which keys should not be marked red/green?
        var exclude_mark = [
            'description',
            'biography',
            'date_start',
            'date_end',
            'main_image',
            'namevariations',
            'releasedate_approx',
            'release_country',
            'country',
            'type',
            'd_tags'
        ];

        var data = {
            'item_type': item_type,
            'item_id': item_id,
            'provider': provider,
            'api_url': api_url
        };

        debug.debug('query data:', data);

        // add status class
        $('body').addClass('api_lookup-progress');

        // reset elements
        $("[id^=" + self.lookup_prefix + "]").parent().removeClass('lookup-match');
        $("[id^=" + self.lookup_prefix + "]").parent().fadeOut(100);


        Dajaxice.alibrary.api_lookup(function (data) {


            var lookup_prefix = 'lookup_id_';

            $('body').removeClass('api_lookup-progress');

            debug.debug('returned data:', data);

            self.lookup_data = data;

            for (var key_ in data) {
                console.log('* ' + key_)
            };


            // check for errors
            if(data.error) {
                alert(data.error);
                return;
            }


            // generic data
            for (var key in data) {


                var obj = data[key];
                console.log('key: ' + key + ': ', obj);

                // check if custom method is required for this key



                switch(key) {
                    case 'main_image':
                        self.image_lookup(key);
                        break;
                    case 'relations':
                        console.log('!!!', key);

                        // for some strange reason this does not work
                        // self.relation_lookup(key);


                        var val = self.lookup_data[key];
                        $('fieldset.relations .lookup-container').html('');
                        $(val).each(function(i, item){
                            debug.debug(item);
                            console.log(item);

                            // try to find relation in form - not extremly nice :(
                            var container = $('.controls input', $('.external.' + item.service).parents('.relation-row'))

                            if(container.length) {

                                console.log('got container');
                                var inner = container.parents('.relation-url')

                                var match = false;
                                var no_match = false;

                                if(container.val() == item.uri) {
                                    match=true;
                                } else {
                                    no_match = true
                                }

                                var data = {
                                    object: item,
                                    match: match,
                                    no_match: no_match
                                }
                                var html = nj.render('alibrary/nj/provider/relation_inline.html', data);

                                if($('.relation', inner).length) {
                                    $('.relation', inner).replaceWith(html);
                                } else {
                                    inner.append(html);
                                }

                            } else {
                                console.log('no container');
                                var match = false;

                                $('.controls input', $('.relation-row')).each(function(i, el){
                                   if($(el).val() == item.uri) {
                                       match = true;
                                   }
                                });

                                var data = {
                                    object: item,
                                    match: match
                                }



                                html = nj.render('alibrary/nj/provider/relation_inline.html', data);

                                if(match) {
                                    $('fieldset.relations .lookup-container').prepend(html);
                                } else {
                                    $('fieldset.relations .lookup-container').append(html);
                                }

                            }

                        });

                        break;

                    default:
                        $('#' + self.lookup_prefix + key).html(obj);
                        $('#' + self.lookup_prefix + key).parent().fadeIn(200);
                }




                // if ($.inArray(key, exclude_mark)) {
                if (exclude_mark.indexOf(key) == -1) {
                    $('#' + self.lookup_prefix + key).parent().addClass('lookup-' + self.lookup_compare(key, data));
                }
            }

            // media (a.k.a. track)-based data
            // look at the tracklist to eventually detect an offset
            var tbd = [];
            if(data.tracklist){
                $.each(data.tracklist, function (i, el) {
                    console.log('el', el);
                    if (el.duration == '' && el.position == '') {
                        tbd.push(i);
                    }
                });
            }


            // remove eventual non-track data
            /*
            var ros = 0;
            $.each(tbd, function (i, el) {
                // data.tracklist.remove(el - ros);
                try {
                    data.tracklist = arrRemove(data.tracklist, (el-ros));
                    ros++;
                } catch(err) {
                    console.log('error:', err)
                }
            });
            */


            // display dta
            if (data.tracklist) {
                self.offset_selector();
                self.media_lookup(data);
            }

            if (data.media) {
                self.media_lookup_mb(data);
            }


            // clean up interface
            $('div.field-lookup-holder').each(function(i, el){
                var el = $(el);
                if(! $('span', el).html().length) {
                    el.hide()
                }
            });



        }, data);
    };


    this.image_lookup = function (key) {
        var val = self.lookup_data[key];

        var image_container = $('#' + self.lookup_prefix + key);
        var html = '<img src="' + val + '" style="height: 125px;">'

        image_container.html(html);
        image_container.parent().fadeIn(200);


    };


    this.relation_lookup = function (key) {
        var val = self.lookup_data[key];


        debug.debug('relation_lookup:', val);

        $('fieldset.relations .lookup-container').html('');

        $(val).each(function(i, item){
            debug.debug(item);

            // try to find relation in form - not extremly nice :(
            var container = $('.controls input', $('.external.' + item.service).parents('.relation-row'))

            if(container.length) {
                // if so, add form-extra
                //container.css('background-color', '#f0f')
                //var inner = $('.relation-url', container)
                var inner = container.parents('.relation-url')
                //inner.css('background-color', '#ff0')

                var match = false;
                var no_match = false;

                if(container.val() == item.url) {
                    match=true;
                } else {
                    no_match = true
                }

                var data = {
                    object: item,
                    match: match,
                    no_match: no_match
                }
                var html = nj.render('alibrary/nj/provider/relation_inline.html', data);


                if($('.relation', inner).length) {
                    $('.relation', inner).replaceWith(html);
                } else {
                    inner.append(html);
                }





            } else {
                // if not - add to generic panel

                // check if link is already set
                var match = false;


                $('.relation-url', $('.relations.external')).fadeOut(5000)

                $('.controls input', $('.relation-row')).each(function(i, el){
                   if($(el).val() == item.url) {
                       match = true;
                   }
                });


                var data = {
                    object: item,
                    match: match
                }
                html = nj.render('alibrary/nj/provider/relation_inline.html', data);

                //if(match) {
                //    $('fieldset.relations .lookup-container').prepend(html);
                //} else {
                //    $('fieldset.relations .lookup-container').append(html);
                //}
            }



        })


    };


    this.offset_selector = function () {

        // generate the dropdown list
        var select = $('#offset_selector .shift-offset select');
        var html = '';
        $.each(self.lookup_data.tracklist, function (i, el) {
            html += '<option';
            html += ' value="' + i + '" ';
            if (i == self.lookup_offset) {
                html += ' selected="selected" ';
            }
            html += '>';
            if (el.position) {
                html += el.position + ' - ' + el.title;
            } else {
                html += '# ' + el.title;
            }
            html += '</option>';
        });
        select.html(html);
    };


    /*
     * Mapping track-based data
     * Discogs version
     */
    this.media_lookup = function (data) {
        var container = $('#release_media_form');
        debug.debug('data:', data);


        // reset the lookup results
        $('.field-lookup .field-lookup-holder', container).hide();
        $('.field-lookup span', container).html('');
        // reset markers
        $('.field-lookup .field-lookup-holder', container).removeClass('lookup-match');
        $('.field-lookup .field-lookup-holder', container).removeClass('lookup-diff');


        var tracklist = data.tracklist;

        // offset tracks - in case of 'non-track-meta'
        var offset = self.lookup_offset;

        console.log('OFFSET: ', offset);


        $('.releasemedia-row', container).each(function (i, el) {

            // check if we have a tracknumber
            var tracknumber = null
            try {
                var tracknumber = parseInt($('select[name$="tracknumber"] option:selected', el).val());
            } catch (e) {
                debug.debug(e);
            }

            // ok got one, try to map. tracknumber is 1-based, index of tracklist 0-based
            if (tracknumber && tracknumber != 0) {
                var meta = false;
                var index = (tracknumber - 1) + offset;

                try {
                    var meta = tracklist[index];
                } catch (e) {
                    debug.debug(e);
                }

                debug.debug('tracknumber:', tracknumber, 'meta:', meta);

                // apply meta lookup information
                if (meta) {


                    // media name
                    var value = meta.title;
                    var holder_name = $('.field-lookup-holder span[id$="name"]', el);
                    holder_name.html(value);
                    holder_name.parent().fadeIn(100);
                    // mark
                    var target_name = $('#' + self.field_prefix + holder_name.attr('id').replace(self.lookup_prefix, ''));
                    if (value.toLowerCase() == target_name.val().toLowerCase()) {
                        holder_name.parent().addClass('lookup-match');
                    } else {
                        holder_name.parent().addClass('lookup-diff');
                    }


                    // media artist name
                    value = '';
                    if (meta.artists && meta.artists.length > 0) {
                        value = meta.artists[0].name;
                    } else if (data.artists && data.artists.length > 0) {
                        value = data.artists[0].name;
                    }
                    var holder_artist = $('.field-lookup-holder span[id$="artist_0"]', el);
                    holder_artist.html(value);
                    holder_artist.parent().fadeIn(100);
                    // mark
                    var target_artist = $('#' + self.field_prefix + holder_artist.attr('id').replace(self.lookup_prefix, ''));
                    if (value == target_artist.val()) {
                        holder_artist.parent().addClass('lookup-match');
                    } else {
                        holder_artist.parent().addClass('lookup-diff');
                    }
                }


            }


            console.log('tracknumber:', tracknumber);


        });


        // update the dropdown
        setTimeout(function () {
            self.offset_selector();
        }, 10);


    };

    /*
     * Mapping track-based data
     * Musicbrainz version
     */
    this.media_lookup_mb = function (data) {


        var container = $('#release_media_form');
        debug.debug('data:', data);


        // reset the lookup results
        $('.field-lookup .field-lookup-holder', container).hide();
        $('.field-lookup span', container).html('');
        // reset markers
        $('.field-lookup .field-lookup-holder', container).removeClass('lookup-match');
        $('.field-lookup .field-lookup-holder', container).removeClass('lookup-diff');


        var tracklist = data.media[0].tracks;

        console.log(tracklist);


        // offset tracks - in case of 'non-track-meta'
        var offset = self.lookup_offset;

        $('.releasemedia-row', container).each(function (i, el) {

            // check if we have a tracknumber
            var tracknumber = null
            try {
                var tracknumber = parseInt($('select[name$="tracknumber"] option:selected', el).val());
            } catch (e) {
                debug.debug(e);
            }

            // ok got one, try to map. tracknumber is 1-based, index of tracklist 0-based
            if (tracknumber && tracknumber != 0) {
                var meta = false;

                $.each(tracklist, function(i, el){

                   if(el.number && el.number == tracknumber) {
                       meta = el;
                   }

                });

                debug.debug('tracknumber:', tracknumber, 'meta:', meta);

                // apply meta lookup information
                if (meta) {


                    // media name
                    var value = meta.title;
                    var holder_name = $('.field-lookup-holder span[id$="name"]', el);
                    holder_name.html(value);
                    holder_name.parent().fadeIn(100);
                    // mark
                    var target_name = $('#' + self.field_prefix + holder_name.attr('id').replace(self.lookup_prefix, ''));
                    if (value.toLowerCase() == target_name.val().toLowerCase()) {
                        holder_name.parent().addClass('lookup-match');
                    } else {
                        holder_name.parent().addClass('lookup-diff');
                    }


                    // media artist name
                    value = '';
                    if (meta.artists && meta.artists.length > 0) {
                        value = meta.artists[0].name;
                    } else if (data.artists && data.artists.length > 0) {
                        value = data.artists[0].name;
                    }
                    var holder_artist = $('.field-lookup-holder span[id$="artist_0"]', el);
                    holder_artist.html(value);
                    holder_artist.parent().fadeIn(100);
                    // mark
                    var target_artist = $('#' + self.field_prefix + holder_artist.attr('id').replace(self.lookup_prefix, ''));
                    if (value == target_artist.val()) {
                        holder_artist.parent().addClass('lookup-match');
                    } else {
                        holder_artist.parent().addClass('lookup-diff');
                    }
                }


            }


            console.log('tracknumber:', tracknumber);


        });

    };


    this.lookup_compare = function (key, data) {

        // which keys should be checked case-insensitive=
        var keys_ci = [
            'releasetype',
            'main_image'
        ];

        // compare original value & lookup suggestion
        var orig = $('#' + self.field_prefix + key).val();
        var lookup_value = data[key];

        // console.log('orig:', orig, 'lookup_value:', lookup_value)

        //if (orig != undefined && !$.inArray(key, keys_ci)) {
        if (orig != undefined && keys_ci.indexOf(key) != -1) {
            orig = orig.toLowerCase();
            lookup_value = lookup_value.toLowerCase();
        }
        ;


        if (orig == lookup_value) {
            return 'match';
        } else {
            return 'diff';
        }

    };


    this.apply_value = function (el) {

        var key = el.attr('id').replace(self.lookup_prefix, '');
        var val = el.html();
        var target = $('#' + self.field_prefix + key);

        var skip_apply = false;


        console.log('apply value:', val, ' key: ', key, 'prefix:', self.lookup_prefix);

        // hack for autocomlete fields (there is a hidden value)
        if (key.endsWith('_0')) {
            var t = key.slice(0, key.length - 1) + '1';
            var hidden_target = $('#' + self.field_prefix + t);
            hidden_target.val('');
        }

        // special handling for image field (value should be put to hidden input)
        if (key == 'main_image') {
            var val_b = $('#' + self.lookup_prefix + 'remote_image').html();
            var target_b = $('#' + self.field_prefix + 'remote_image');

            // reflect change in info-panel
            //$('.iteminfo .image a').attr('href','#');
            //$('.iteminfo .image img').attr('src',val_b);

            // create img element if not present
            // extremely ugly, i know.
            if(!$('#div_id_main_image img.placeholder').length) {
                $('#div_id_main_image').css('position', 'relative');
                $('#div_id_main_image').append('<img class="placeholder" style="height: 102px; position: absolute; left:132px; top: 25px;"></img>');
            }

            $('#div_id_main_image img').attr('src',val_b);

            target_b.val(val_b);
        }

        // handle tags
        if (key == 'd_tags') {
            var tags = val.split(',');

            $(tags).each(function (i, el) {
                //$("#id_d_tags").tagit("createTag", $.trim(el));
                $("#id_d_tags").tagit("createTag", $('<input />').html($.trim(el)).text());
            });
        }

        // handle country mapping (kind of hakish...)
        if (key == 'release_country') {

            console.log('release_country:', val, val.length)

            if(val.length < 4) {
                var target = $('#' + self.field_prefix + 'release_country option:contains("' + val + ')")');
            } else {
                var target = $('#' + self.field_prefix + 'release_country option:contains(' + val + ')');
            }
            target.prop("selected", "selected");
            skip_apply = true;
        }
        if (key == 'country') {
            if(val.length < 4) {
                var target = $('#' + self.field_prefix + 'country option:contains("' + val + ')")');
            } else {
                var target = $('#' + self.field_prefix + 'country option:contains(' + val + ')');
            }
            target.prop("selected", "selected");
            skip_apply = true;
        }

        // artist type mapping
        if (key == 'type' && $('form.form-artist').length) {

            var target = $('#' + self.field_prefix + 'type option:contains(' + val + ')');
            target.prop("selected", "selected");
            skip_apply = true;
        }

        // release type mapping
        if (key == 'releasetype' && $('form.form-release').length) {
            var target = $('#' + self.field_prefix + 'releasetype option:contains(' + val + ')');
            target.prop("selected", "selected");
            skip_apply = true;
        }

        // handle pagedown-preview
        if (key == 'description') {

            try {
                setTimeout(function(){
                    pd_editor.refreshPreview()
                }, 200)
            } catch (e) {
            }
        }
        // handle pagedown-preview
        if (key == 'biography') {

            try {
                setTimeout(function(){
                    pd_editor.refreshPreview()
                }, 200)
            } catch (e) {
            }
        }

        // apply feedback
        el.parent().removeClass('lookup-diff');
        el.parent().addClass('lookup-match');

        if(!skip_apply){
            target.val($.decodeHTML(val));
        }

        // hack for autocomlete fields - trigger search dialog
        if (key.endsWith('_0')) {
            target.djselectable('search', $.decodeHTML(val));
        }
    };


    /***************************************************************************************
     * Utils & helpers
     ***************************************************************************************/

    this.floating_sidebar = function (id, offset) {

        try {
            if (!self.is_ie6) {
                var top = $('#' + id).offset().top - parseFloat($('#' + id).css('margin-top').replace(/auto/, 0));
                $(window).scroll(function (e) {
                    var y = $(this).scrollTop();
                    if (y >= top - offset) {
                        $('#' + id).addClass('fixed');
                    } else {
                        $('#' + id).removeClass('fixed');
                    }
                });
            }
        }
        catch (err) {

        }

    };

};


edit.ui = new EditUi();

