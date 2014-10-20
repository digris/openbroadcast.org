/*
 * JINGLE SCRIPTS
 */

/* core */

OnAirApp = function() {

	var self = this;
	
	this.timeout = false;
	this.timeout_duration = 60000;
	
	this.api_url = false;
	
	this.dom_id = 'on_air_app';
	this.dom_element;
	
	this.current_data = false;
	this.current_emission = false;
	this.current_item = false;

	this.init = function() {
		
		debug.debug('OnAirApp: init');
		debug.debug(self.api_url);
		
		this.dom_element = $('#' + this.dom_id);

		self.iface();
		self.bindings();

		self.load();

		pushy.subscribe('19741cf3-cf71-11e2-ae7c-b8f6b11a3aed', function(data) {
			debug.debug('pushy callback');
			self.load(data)
		});
		
		
	};

	this.iface = function() {
		// this.floating_inline('lookup_providers', 120)
	};

	this.bindings = function() {
		
	
	};

	// timeout
	this.set_timeout = function(callback, duration) {
		self.timeout = setTimeout(callback, duration);
	};

	this.load = function(data) {
	
		console.log(data);
	
		$.get(self.api_url, function(data){
			
			self.current_data = data;

			var start_next = data.start_next;

			if(start_next && start_next < 60 * 1000) {
				debug.debug('setting timeout to: ' +  (Math.floor(start_next) + 1) * 1000);
				self.set_timeout(self.load, (Math.floor(start_next) + 1) * 1000);
			} else {
				debug.debug('setting timeout to default: ' +  self.timeout_duration + ' - start_next is: ' + start_next);
				self.set_timeout(self.load, self.timeout_duration);
			}

			if(data.playing && data.playing.emission) {
				$.get(data.playing.emission, function(data, start_next){
					self.current_emission = data;
					self.display_emission(data);
				});
			} else {
				self.current_emission = false;
				$('.emission', self.dom_element).html('');
			}
			
			if(data.playing && data.playing.item) {
				$.get(data.playing.item, function(data, start_next){
					setTimeout(function() {
						self.current_item = data;
						self.display_item(data);
					}, 200);
				});
			} else {
				self.current_item = false;
				$('.item', self.dom_element).html('');
			}

			
			// init countdown
			$('.countdown', self.dom_element).html('<span></span>');
			var cnt_holder = $('.countdown > span', self.dom_element); 
			cnt_holder.countdown({
				until: start_next,
				format: 'HMS',
				compact: true,
				significant: 4
			});

			
			
		});
	
		self.interval_loops++;
		// self.dom_element.append('<p>' + self.interval_loops + '</p>');
	};
	
	this.display_item = function(data, start_next) {
		debug.debug('OnAirApp: display_item');
		debug.debug(data);
		
		var container = $('.items', self.dom_element);
		var d = {
			object : data
		}
		$('div', container).addClass('past');
		$('div', container).removeClass('playing');
		var html = nj.render('abcast/nj/on_air_item.html', d);
		container.prepend($(html).addClass('playing').fadeIn(500));
		
	};
	
	this.display_emission = function(data, start_next) {
		debug.debug('OnAirApp: display_emission');
		debug.debug(data);
		
		// check if item changed
		var changed = false;
		if (self.last_emission && ! data.uuid == self.last_emission.uuid) {
			changed = true;
		}
		self.last_emission = data;
		
		var container = $('.emission', self.dom_element);
		var d = {
			object : data
		}
		var html = nj.render('abcast/nj/on_air_emission.html', d);
		if(changed) {
			$('.items', self.dom_element).html('');
		}
		container.html(html);

	};



};




