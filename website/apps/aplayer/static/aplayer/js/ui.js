/*********************************************************************************
 * APLAYER UI
 * Copyright 2009, Jonas Ohrstrom  - ohrstrom@gmail.com
 * See LICENSE.txt
 *
 * WARNING!!!
 * this code is extremly bad. it is taken from an old (also bad) project and was
 * extended again and again.
 * refactoring is neccessary - but at the moment no time and no budget
 *********************************************************************************/



var aplayer = aplayer || {};
aplayer.ui = aplayer.ui || {};
aplayer.ui.player = aplayer.ui.player || {};

aplayer.ui.use_effects = true;


/*********************************************************************************
 * global initialisation
 *********************************************************************************/
aplayer.ui.init = function() {
	aplayer.ui.bind();
};




/*********************************************************************************
 * Interface bindings (live ones)
 *********************************************************************************/
aplayer.ui.bind = function() {

	// handles '.playable' elements
    // used to play media items
	$('body').on('click', '.playable.popup:not(".disabled")', function(e) {

		e.preventDefault();

        // TODO: make better...
        $('body').addClass('loading-playlist');


        var ct = $(this).data('ct');
		var uri = $(this).data('resource_uri');
		var offset = $(this).data('offset');
		var mode = $(this).data('mode');
		var token = 'xx-yy-zz';
		var source = 'alibrary';

        // ct based switches
        // media set -> ignore uri and build one by ourselves
        if (ct == 'media_set') {

            // get all items currently shown
            var item_ids = [];
            var item_id = $(this).parents('.item').data('item_id');
            var container = $(this).parents('.container');

            $('.item.media', container).each(function(i, el){
                var current_id = $(el).data('item_id');
                if (current_id == item_id) {
                    offset = i;
                }
                item_ids.push(current_id)
            })

            // sorry, kind of ugly..
            uri = '/api/v1/library/simpletrack/?id__in=' + item_ids.join(',');

        }

		aplayer.base.play_in_popup(uri, token, offset, mode, false, source);

	});


	$('body').on('click', '.streamable.popup:not(".disabled")', function(e) {

		e.preventDefault();

		var uri = $(this).data('resource_uri');
		var offset = 0;
		var mode = 'replace';
		var token = 'xx-yy-zz';
		var source = 'abcast';

        aplayer.base.play_in_popup(uri, token, offset, mode, false, source);

    });
	
	// handles cuepoints
	$('a.cuepoint', '.content').live('click', function(e) {
		
		e.preventDefault();
		
		var container = $(this).parents('.cms_plugin');
		
		var action = $('.info a', $('.item', container)).attr('href').split('#');
		var uri = action[0];
		var offset = action[1];
		var mode = action[2];
		var token = 'xx-yy-zz';

		var seek = $(this).attr('href').substring(1);
		
		var force_seek = seek;
		
		aplayer.base.play_in_popup (uri, token, offset, mode, force_seek);		
	});
	
	// cuepoint indicators
	$('a.cuepoint', '.content').live('hover', function(e) {
		
		e.preventDefault();
		
		var container = $(this).parents('.cms_plugin');
		var playhead = $('> .item', container);

		var duration = parseInt($('.item', container).data('duration') / 1000);
		var seek = parseInt($(this).attr('href').substring(1));

		
		var relative_position = parseInt(seek / duration * 100);
		//debug.debug(duration, seek, relative_position);
		
		$('.handler', playhead).css('background-position', relative_position + '% 0');
		

		playhead.addClass("hover");
		
		
	});
	$('a.cuepoint', '.content').live('mouseleave', function(e) {
		
		e.preventDefault();
		
		var container = $(this).parents('.cms_plugin');
		var playhead = $('> .item', container);

		playhead.removeClass("hover");
	});
	
	
	
	
	
	$("a.parent_link").live('click', function(e){
		
  		var href = $(this).attr('href');
  		parent_win.location.href = href;
  		
		return false;
		
	});

	// TODO: move bindings...
	$("#aplayer_playlist div.listing.item").live('click', function(e){
  		var id = $(this).attr('id');
  		id = id.split('_')[2];

  		if($(this).hasClass('active')) {
  			aplayer.controls('pause');
  		} else {
  			aplayer.controls('play', id); 
  		}
	});
	
	
	
	$('.playlist .item.playlist').live('click', function(e){
		
		var uuid = $(this).attr('id');
        try {
            var index = aplayer.vars.uuid_map[uuid];
        } catch (e) {
            var index = 0;
        }

		
		var args = {
			action: 'play',
			index: index
		}
		
		aplayer.base.controls(args)
	});
	

	aplayer.ui.bind_controls($("div.aplayer-controls li > a", '.aplayer'));


    // set status (mode / version)
    $('#aplayer_mode', $('footer')).html(aplayer.vars.stream_mode)
    $('#aplayer_version', $('footer')).html(aplayer.vars.version)


    $('#aplayer_volume', $('footer')).noUiSlider({
        range: [0, 100]
       ,start: 80
       ,step: 1
       ,handles: 1
       ,connect: 'lower'
       ,slide: function(){
          var values = $(this).val();
            aplayer.player.setVolume(values)
       }
    });


    // window resize - adjust playlist screen
    $(window).on('resize', function(){
        var win = $(this);
        var inner_height = win.height() - (238);
        $('#aplayer_playlist').css('height', inner_height);
    });




	aplayer.ui.rebind();

};


/*********************************************************************************
 * Non live - Interface bindings
 * (Which may be recalled on newly added elements)
 *********************************************************************************/
aplayer.ui.rebind = function() {

	
	
	// waveform scaleing
	$(document).bind('keydown.modal', function(event) {

		switch(event.which)
		{
			case 32:
				aplayer.base.controls({action: 'pause' });
				break;
			case 39:
				if(aplayer.states.next) {
					aplayer.base.controls({action: 'play', index: aplayer.states.next });
				}
				break;
			case 37:
				if(aplayer.states.prev !== false) {
					aplayer.base.controls({action: 'play', index: aplayer.states.prev });
				}
				break;
		}
		
	});
	
};


/*********************************************************************************
 * Controls (prev, pause, play, next) - applyed to given object
 *********************************************************************************/
aplayer.ui.bind_controls = function(obj) {

	// play buttons / bindings
	obj.live('click', function(e){
  		
  		e.preventDefault();
  		
  		//if(local.aplayer === undefined) {
			aplayer = local.aplayer;
		//}
  		
  		var action = $(this).attr('href').substring(1);

  		if(action == 'pause') {
  			aplayer.base.controls({action: 'pause' });
  		}
  		
  		if(action == 'play' && aplayer.states.state) {
  			aplayer.base.controls({action: 'pause' });
  		}
  		
  		if(action == 'next') {
			if(aplayer.states.next) {
				aplayer.base.controls({action: 'play', index: aplayer.states.next });
			}
  		}
  		
  		if(action == 'prev') {
			if(aplayer.states.prev !== false) { // note: in js 0 == false > true
				aplayer.base.controls({action: 'play', index: aplayer.states.prev });
			}
  		}

	});
	
	
	
	
	// progress bar click / seek
	$('.indicator .wrapper', 'body.popup #progress_bar').live('click', function(e) {
		
		outer_width = $(this).css('width').slice(0, -2);
		base_width = outer_width;

		var pos = util.get_position(e);		
		var x_percent = pos['x'] / (base_width) * 100;
		var uuid = $(this).parents('.item').attr('id');

		// trigger control
		var args = {
			action: 'seek',
			position: x_percent,
			uuid: uuid 
		}
		aplayer.base.controls(args);

	});
	
	// moving the handler
	$('.indicator .wrapper', 'body.popup #progress_bar').live('mousemove', function(e) {
		var pos = util.get_position(e);
		$(this).css('background-position', pos['x'] + 'px' + ' 0px');
	});
	
	

	
	
};


/*********************************************************************************
 * Update
 *********************************************************************************/
aplayer.ui.update = function(aplayer) {
	
	
	
	local.aplayer = aplayer;
	
	this.type = local.type;
	
	// check what has changed since the last poll
	this.state_changed = (aplayer.states.state != aplayer.states_last.state);
	this.media_changed = (aplayer.states.uuid != aplayer.states_last.uuid);


	// TODO: check if this is a good way
	var media = false;
	if (aplayer.vars.source && aplayer.vars.source == 'alibrary') {

		media = aplayer.vars.playlist[aplayer.states.current];
	}

	if (aplayer.vars.source && aplayer.vars.source == 'abcast') {
		//debug.debug('we\'re in abcast mode..');
		var channel = aplayer.vars.playlist[aplayer.states.current];

		if (!channel.media) {
			debug.debug('no channel media available.');
		} else {
			media = channel.media;
		}
	}
	
	if (media) {

		// var media = aplayer.vars.playlist[aplayer.states.current];
		
		//debug.debug('media:', media);
		//debug.debug('media name:', media.name);
	
		// var playlist_container = $('div.listing.extended');
		$('div.item.playlist').not('div.item.playlist.' + media.uuid).removeClass('active playing');
		$('div.item.playlist.' + media.uuid).addClass('active playing');
		
		// modification for alternate layout
		$('div.listview.medias .item').not('div.item.playlist.' + media.uuid).removeClass('active playing');
		$('div.listview.medias .item.' + media.uuid).addClass('active playing');
	
		// playhead
		//var active_playhead = $('div.item.' + media.uuid + ' ' + 'div.indicator');
		
		var container = $('div.aplayer.inline');
		var active_playhead =  $('.playhead .indicator', container_screen);
		
		if(active_playhead.html()) {
			outer_width = active_playhead.css('width');
			try {
				base_width = outer_width.slice(0, -2);
			} catch(err) {
				//debug.debug(media.uuid);
				//debug.debug('no base_width');
				base_width = 700;
			};
			active_playhead.css('background-position', (aplayer.states.position_rel * base_width / 100) + 'px' + ' 0px');
	
		}
		
		// debug.debug(state_changed, 'changed');
		var body = $('body');

        // refactored version, using InlinePlayer
        if(window.aplayer.inline) {
            if(!window.aplayer.inline.player) {
                window.aplayer.inline.player = aplayer;
            }
            window.aplayer.inline.update(aplayer, media);
        };


        // detail player (e.g. on media page)
        if(window.detail_player != undefined) {
            window.detail_player.update(aplayer);
        }



	
		var container_screen = $('#progress_bar');
		if(container_screen) {
			$('div.time-current > span', container_screen).html(util.format_time(aplayer.states.position));
			$('div.time-total > span', container_screen).html(util.format_time(aplayer.states.duration));
			
			// $('.indicator .inner', container_screen).css('width', aplayer.states.position_rel + '%');
			//$('.playhead .indicator', container_screen).css('width', aplayer.states.position_rel + '%');
			
			// playlist inline progress
			$('.indicator .inner', '.item.playlist.playing').css('width', aplayer.states.position_rel + '%');
		}
	
			
		//}
		
		// popup window
		if(this.type == 'popup') {
			
		}
	}

	// debug.debug(aplayer.states, local.type);
    // TODO: make better...
    $('body').removeClass('loading-playlist');



};





/*********************************************************************************
 * Updates the info-screen. (If available gets additional data from API)
 * (renders the tpl_screen.html template)
 *********************************************************************************/
aplayer.ui.screen_display = function(index) {

    // hack - get media in case of abcast (media is mapped to channel data)
    if (aplayer.vars.playlist[index].media) {
        var item = aplayer.vars.playlist[index].media;
        item.source = 'abcast';
    } else {
        var item = aplayer.vars.playlist[index];
        item.source = 'alibrary';
    }

	try {
		item.images = []
		item.images.push(item.release.main_image);
	} catch(err) {};

    // refactored to nj
    /*
	var html = ich.tpl_screen({object: item});
	$( "#aplayer_screen" ).html(html);
    */

    // moving to nj
    var html = nj.render('aplayer/nj/popup_screen.html', {
        object: item
    });
    $( "#aplayer_screen" ).html(html);


};


aplayer.ui.update_emission = function(data) {


    debug.debug('update_emission - data:', data)

    var html = nj.render('aplayer/nj/popup_emission.html', {
        object: data
    });
    $( "#aplayer_emission" ).html(html);
}



/*********************************************************************************
 * Updates the playlist-screen.
 * (renders the tpl_media.html template)
 *********************************************************************************/
aplayer.ui.playlist_display = function(aplayer, target) {

	target.html('');

	var media_listing = new Array();
	
	for (x in aplayer.vars.playlist) {
		var media = aplayer.vars.playlist[x];
		
		var media_name = 'unknown';
		var artist_name = 'unknown';
		
		if(media.name) {
			media_name = media.name;
		}
		if(media.artist) {
			artist_name = media.artist.name;
		}

		media_listing[x] = {
			media: media,
			name: media.name,
		};
		
		media.formated_duration = util.format_time(Number(media.duration / 1000))

		var html = ich.tpl_media({'media': media});
		target.append(html);
		
	};





};










/*********************************************************************************
 * Scale the waveform image
 *********************************************************************************/
aplayer.ui.scale_waveform = function(direction) {
	
	var waveform = $('.playhead .waveform');
	var height = parseFloat(waveform.css('height').slice(0, -2));
	
	switch(direction)
	{
		case 'up':
			waveform.css('height', (height + 5) + 'px');
		break;
		
		case 'down':
			waveform.css('height', (height - 5) + 'px');
		break;
	}
};




/*********************************************************************************
 * Control the overlay and other things...
 * Just very basic a.t.m. - just to have it at the correct place 
 *********************************************************************************/
aplayer.ui.hide_overlay = function() {
	$('#overlay_container').hide();
};


aplayer.ui.reset = function() {

    if(window.aplayer.inline) {
        window.aplayer.inline.reset();
    };

    /*
	var container = $('#aplayer_inline');

	container.removeClass('active');
	
	// TODO: modularize
	$('.media_name a').html('PLAYER');
	$('.artist_name a').html('&nbsp;');
	$('.release_name a').html('&nbsp;');
	$('ul.timing', container).fadeOut(500);
	
	
	$('.playlist .item').removeClass('active');
    */
};















/*********************************************************************************
 * Playhead
 *********************************************************************************/
aplayer.ui.playhead = function(base_width) {

	if(base_width === undefined) {
		base_width = 610;
	}

	// moving the handler (red bar) - simple as "pos == %"
	$('.playhead .handler').live('mousemove', function(e) {

		var pos = util.get_position(e);
		
		// debug.debug(pos['x'], 'pos move');
		
		$(this).css('background-position', pos['x'] + 'px' + ' 0px');

	});
	
	

	// playhead in popup (directly attached)
	$('.playhead .handler', 'body.popup').live('click', function(e) {
		
		// TODO: needs check - position not correct on seek
		outer_width = $(this).parents('.playhead').css('width').slice(0, -2);
		base_width = outer_width;
		
		//debug.debug(outer_width, 'outer_width');
		//debug.debug(base_width, 'base_width');

		var pos = util.get_position(e);
		
		//debug.debug(pos['x'], 'pos click');
		
		var x_percent = pos['x'] / (base_width) * 100;
		//debug.debug(x_percent, 'x_percent');

		var uuid = $(this).parents('.item').attr('id');


		// trigger control
		var args = {
			action: 'seek',
			position: x_percent,
			uuid: uuid 
		}
		aplayer.base.controls(args);

	});



	$('.playhead .handler', 'body.base').live('click', function(e) {
		outer_width = $(this).parents('.playhead').css('width').slice(0, -2);
		base_width = outer_width;

		var pos = util.get_position(e);
		var x_percent = pos['x'] / (base_width) * 100;

		// debug.debug(x_rel);

		var uuid = $(this).parents('.item').attr('id');

		// TODO: check if current release is loaded
		
		
		
		try {
			var is_loaded = (uuid in local.aplayer.vars.uuid_map)
		}
		catch(err) {
			var is_loaded = false;
		};

		// check if player exists and loaded
		if( typeof (local.aplayer) != 'undefined' && is_loaded == true) {

			// trigger control
			var args = {
				action: 'seek',
				position: x_percent,
				uuid: uuid 
			}
			local.aplayer.base.controls(args);
			
			
			
		}
		// else create it!
		// TODO: pack in own funtion to not repeat...
		else {

			//debug.debug('player NOT HERE! böööh!');

			var action = $('.info a', $(this).parents('.item')).attr('href').split('#');
			var uri = action[0];
			var offset = action[1];
			var mode = action[2];
			var token = 'xx-yy-zz';
			
			aplayer.base.play_in_popup (uri, token, offset, mode);
			
		}
	});
	

	// wait until all waveforms are loaded
	var loaded = 0;
	var num_images = $("img", '.playhead .waveform').length;
	$('img', '.playhead .waveform').one('load', function() {++loaded;
		if(loaded === num_images) {
			$('div.playhead').removeClass('loading');
		};
	}).each(function() {
		if(this.complete)
			$(this).load();
	});
	
	
	
};


