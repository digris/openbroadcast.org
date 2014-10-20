/*
 * IMPORTER SCRIPTS
 * probably split in importer.base.js and importer.ui.js later on
 */

/* core */
var importer = importer || {};
importer.base = importer.base || {};
importer.ui = importer.ui || {};

ImporterUi = function() {

	var self = this;

	this.lookup_prefix = 'lookup_id_';
	this.field_prefix = 'id_';
	this.interval = false;
	this.interval_loops = 0;
	this.interval_duration = 50000;
	this.api_url = false;

    this.pushy_paused = false;
	
	this.importfiles = [];

    this.summary;

	// attach fu here
	this.fileupload_id = false;
	this.fileupload_options = false

	this.current_data = new Array;
	this.musicbrainz_data = new Array;

	this.is_ie6 = $.browser == 'msie' && $.browser.version < 7;

	this.init = function() {
		debug.debug('importer: init');
		debug.debug(self.api_url);
		self.iface();

		self.fileupload = $('#' + self.fileupload_id);
		self.fileupload.fileupload('option', self.fileupload_options);

		self.bindings();

		// set interval (now handled by pushy..)
		// self.set_interval(self.run_interval, self.interval_duration);
		pushy.subscribe(self.api_url, function() {

            if(!this.pushy_paused) {
                self.run_interval();
            }
        });
		self.run_interval();


	};

	this.iface = function() {
		this.floating_sidebar('lookup_providers', 120)
	};

	this.bindings = function() {

		self.fileupload.bind('fileuploaddone', function(e, data) {
			// run update
			self.update_import_files();
		});

		// item actions
		var actions = $('#result_holder .importfile.item .result-actions');

		
		$('.start-import-all', $('#import_summary')).live('click', function(e){

			var url = self.api_url + 'import-all/';

            // update view for corresponding items
            $.each(self.importfiles, function(i, item){

                if(item.local_data && item.local_data.status == 'ready') {

                    setTimeout(function(){
                        // override status for fast display update
                        item.local_data.status = 'queued';
                        item.display(item.local_data)
                    },500)

                }
            })

            setTimeout(function(){
                $.ajax({
                    type: "GET",
                    url: url,
                    dataType: "application/json",
                    contentType: 'application/json',
                    processData:  false,
                    success: function(data) {
                        debug.debug(data);
                    }
                });
            }, 0);

		});


		$('.retry-pending', $('#import_summary')).live('click', function(e){

			var url = self.api_url + 'retry-pending/';
            // alert('retry-pending');
            $.ajax({
                type: "POST",
                url: url,
                dataType: "application/json",
                contentType: 'application/json',
                processData:  false,
                success: function(data) {
                    debug.debug(data);
                }
            });




		});
		
		
		/* summary actions */
		var container = $('#import_summary');
		$(container).on('click', 'a.toggle', function(e){

			e.preventDefault();
			var cls = $(this).data('toggle');
			
			if($(this).data('toggle-active') == 0) {
				
				$('i', this).removeClass('icon-angle-down');
				$('i', this).addClass('icon-angle-up');
				
				$('.importfile.' + cls).fadeIn(100);
				$(this).data('toggle-active', 1);
			} else {
				
				$('i', this).removeClass('icon-angle-up');
				$('i', this).addClass('icon-angle-down');
				
				$('.importfile.' + cls).fadeOut(300);
				$(this).data('toggle-active', 0);
			}

			
		});
		
		
		// "add all to playlist"
		var container = $('.sidebar.playlist-container');
		$(container).on('click', 'a.add-all-to-playlist', function(e){
			e.preventDefault();

			// get id's
			// console.log(self.importfiles);
			var ids = [];
			$.each(self.importfiles, function(i, el) {
				if(el.local_data.status == 'done' || el.local_data.status == 'duplicate') {
					ids.push(el.local_data.media.id);
				}
			});

			/**/
			var data = {
				ids: ids.join(','), 
				ct: 'media'
			}

			

			url = '/api/v1/library/playlist/collect/';
			
			/**/
			jQuery.ajax({
				url: url,
				type: 'POST',
				data: data,
				dataType: "json",
				contentType: "application/json",
				//processData:  false,
				success: function(data) {
					alibrary.playlist.update_playlists();
				},
				async: true
			});
			


		});
		
		
		
		
		
	};



	this.import_by_id = function(id) {
		debug.debug('id: ' + id);
		
		var item = self.current_data[id];
		var el = $('#importfile_result_' + id)
		var form_result = $('.form-result', el);

		var import_tag = {
		
			name: $('input.name', form_result).val(), 
			release: $('input.release', form_result).val(), 
			releasedate: $('input.releasedate', form_result).val(), 
			artist: $('input.artist', form_result).val(), 
			tracknumber: $('input.tracknumber', form_result).val(), 
			
			mb_track_id: $('input.mb-track-id', form_result).val(), 
			mb_artist_id: $('input.mb-artist-id', form_result).val(), 
			mb_release_id: $('input.mb-release-id', form_result).val(), 
		}
		
		if(! (import_tag.name && import_tag.artist)) {
			alert('Missing fields!!');
			return;
		}
		
		var data = { 
			status: 6, 
			import_tag: import_tag 
			};
		

		el.removeClass('working');
		el.addClass('queued');
		
		$('.result-set', el).hide(100);
		$('.result-actions', el).hide(200);
		
		/**/
		$.ajax({
			type: "PUT",
			url: item.resource_uri,
			dataType: "application/json",
			contentType: 'application/json',
			processData:  false,
			data: JSON.stringify(data),
			success: function(data) {
				debug.debug(data);
				form_result.hide();
				
			}
		});
		
		
	};


	/*
	 * Methods for import editing
	 */
	this.set_interval = function(method, duration) {
		self.interval = setInterval(method, duration);
	};
	this.clear_interval = function(method) {
		self.interval = clearInterval(method);
	};

	this.run_interval = function() {
		//debug.debug('interval: ' + self.interval_loops);
		self.interval_loops += 1;

		// Put functions needed in interval here
		self.update_import_files();

	};

	this.update_import_files = function() {

		$.getJSON(self.api_url, function(data) {
			self.update_import_files_callback(data);

            $('#loading_message').fadeOut(300);

		});

	};
	this.update_import_files_callback = function(data) {

        console.log('update_import_files_callback', data);

		self.update_list_display(data.files);
		//self.update_summary_display(data);
		try {
			self.update_best_match(data.files);
			self.apply_best_match(data.files);
		} catch(err) {
			// debug.debug(err);
		}

        self.update_summary(data);

	};


	this.update_summary = function(data) {

        // calculate counters
        var counters = {
            num_done: 0,
            num_ready: 0,
            num_working: 0,
            num_pending: 0,
            num_warning: 0,
            num_duplicate: 0,
            num_error: 0
        };

		$.each(self.importfiles, function(i, item) {

			var data = item.local_data;

			if (data.status == 'done') {
				counters.num_done++;
			}
			if (data.status == 'ready') {
				counters.num_ready++;
			}
			if (data.status == 'init') {
				counters.num_pending++;
			}
			if (data.status == 'working') {
				counters.num_working++;
			}
			if (data.status == 'warning') {
				counters.num_warning++;
			}
			if (data.status == 'duplicate') {
				counters.num_duplicate++;
			}
			if (data.status == 'error') {
				counters.num_error++;
			}

		});

        // calculate inserts
        // ignore media - as this is the same as "num_ready"
        var inserts_artist = [];
        var inserts_release = [];
		$.each(self.importfiles, function(i, item) {
			// console.log('update importfile / ImporterApp');
			var data = item.local_data;
			if (data.status == 'ready' || 1 == 1) {
                var it = data.import_tag;
                // possible situations
                // no foreign id's at all: hmm, what to do then?
                // internal id: ignore insert
                // external (mb) id: add to insert
                if(it.alibrary_artist_id == undefined) {
                    if(!it.mb_artist_id == undefined) {
                        if (inserts_artist.indexOf(it.mb_artist_id) < 0) {
                            inserts_artist.push(it.mb_artist_id);
                        }
                    }
                }

                if(it.alibrary_release_id == undefined) {
                    if(!it.mb_release_id == undefined) {
                        if (inserts_release.indexOf(it.mb_release_id) < 0) {
                            inserts_release.push(it.mb_release_id);
                        }
                    }
                }

			}
		});
        var inserts = {
            num_media: counters.num_ready,
            num_artists: inserts_artist.length,
            num_releases: inserts_release.length

        };

        self.summary = {
            counters: counters,
            inserts: inserts
        }

        self.update_summary_display();

	};

	
	this.update_summary_display = function() {

		var container = $('#import_summary');
        var html = nj.render('importer/nj/summary.html', self.summary);
        container.html(html);
	};


	this.apply_best_match = function(data) {

        // TODO: investigate necessity
        return;


        console.log('APPLY BEST MATCH FOR:', data)



		$('.importfile', holder).each(function(i, item) {
			
			//debug.debug(i);
			//debug.debug(item);
			
			var selected = $('.result-set.musicbrainz-tag.selected, .result-set.musicbrainz-tag.choosen', item)
			
			debug.debug('media-id', $('.media-id', selected).val());
			debug.debug('release-id', $('.release-id', selected).val());
			debug.debug('artist-id', $('.artist-id', selected).val());
			
			var result_form = $('.form-result', item);
			// ids
			$('.mb-track-id', result_form).val($('.media-id', selected).val())
			$('.mb-artist-id', result_form).val($('.artist-id', selected).val())
			$('.mb-release-id', result_form).val($('.release-id', selected).val())
			
			// other data
			$('.releasedate', result_form).val($('.releasedate', selected).val())
			$('.catalognumber', result_form).val($('.catalognumber', selected).val())
			$('.release', result_form).val($('.release', selected).val())
			$('.artist', result_form).val($('.artist', selected).val())
			$('.name', result_form).val($('.name', selected).val())
			
			// selected.hide(20000);

			
		});
	
	};

	this.update_best_match = function(data) {

        // TODO: investigate necessity
        return;


        console.log('UPDATE BEST MATCH FOR:', data)

		var active_releases = new Array;

		//debug.debug('update_best_match');

		// populate calculation array
		for (var i in data) {
			var item = data[i];
			var target_result = $('#importfile_result_' + item.id);

			if (item.status > 0) {

				try {
					item.results_musicbrainz = JSON.parse(item.results_musicbrainz);
					
				} catch(err) {
					//debug.debug(err);
				}

				if (item.id in self.current_data) {

					if (item.results_musicbrainz) {

						for (var k in item.results_musicbrainz) {
							var res = item.results_musicbrainz[k]
							//debug.debug(res);

							if (res['mb_id'] in active_releases) {
								active_releases[res['mb_id']] += 1;
							} else {
								active_releases[res['mb_id']] = 1;
							}

						}
					}
				}
			}
		}

		active_releases = sortObject(active_releases);

		// debug.debug(active_releases.reverse());
		
		var hits = active_releases.reverse().slice()
		var top_hit = active_releases[0]['key'];

		//debug.debug(hits);
		//debug.debug(top_hit);

		// set selection state
		
		for (var i in data) {
			var item = data[i];
			var target_result = $('#importfile_result_' + item.id);

			$('.result-set.musicbrainz-tag', target_result).removeClass('selected');
			
			// check if manually choosen
			if(!$('.result-set.musicbrainz-tag', target_result).hasClass('choosen')) {
			
			
				if (item.status > 0) {
					
					//debug.debug(item.results_musicbrainz);
	
					if (item.id in self.current_data) {
	
						if (item.results_musicbrainz) {
	
							//debug.debug('ok');	
							
							for (var k in item.results_musicbrainz) {
								var res = item.results_musicbrainz[k]
								//debug.debug(res['mb_id']);
	
								if (res['mb_id'] == top_hit) {
									// debug.debug('top-match');
									$('.result-set.musicbrainz-tag.mb_id-' + res['mb_id'], target_result).addClass('selected');
								} else {
									//debug.debug('NOOOOOOO-match');
								}
	
							}
						}
					}
	
				}
			
				
			}

			
			
			
			
			
			
		}

	};

	this.update_list_display = function(data, force) {


        var force_update = false;
        if(force != undefined && force == true) {
            force_update = true;
        }

        if(force_update) {
            $('#result_holder').html('');
            self.importfiles = [];
        }


		debug.debug(data);
		$.each(data, function(i, item) {
			debug.debug(item);
			// parse raw data
			try {
				item.results_tag = JSON.parse(item.results_tag);
				item.results_acoustid = JSON.parse(item.results_acoustid);
				item.results_musicbrainz = JSON.parse(item.results_musicbrainz);
				item.import_tag = JSON.parse(item.import_tag);
			} catch(err) {
				item.results_tag = false;
				debug.debug(err);
			}
			
			// check if in dom
			if(! $('#' + item.uuid).size()) {
				debug.debug('element not existent in dom');
				
				// add container
				$('#result_holder').append('<div id="' + item.uuid + '"></div>');
				
				var ifa = new ImportfileApp;
				ifa.local_data = item;
				ifa.container = $('#' + item.uuid);
				ifa.api_url = item.resource_uri;
				ifa.importer = self;
				ifa.init(true);
				
				self.importfiles.push(ifa);
				
			} else {
				debug.debug('element exists in dom');


			};
			
		});



	};


	this.api_lookup = function(item_type, item_id, provider) {

		var data = {
			'item_type' : item_type,
			'item_id' : item_id,
			'provider' : provider
		}

		Dajaxice.alibrary.api_lookup(self.api_lookup_callback, data);
	};

	this.floating_sidebar = function(id, offset) {

		try {

		} catch(err) {
			debug.debug(error);
		}

	};

};

function sortObject(obj) {
	var arr = [];
	for (var prop in obj) {
		if (obj.hasOwnProperty(prop)) {
			arr.push({
				'key' : prop,
				'value' : obj[prop]
			});
		}
	}
	arr.sort(function(a, b) {
		return a.value - b.value;
	});
	return arr;
	// returns array
}