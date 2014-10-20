


var SessionApp = function() {

	var self = this;
	this.api_url
	this.container
	this.dimensions

	this.shotSize

	this.interval_duration = 10000;
	this.interval = false;

	this.local_data = false;

	

	self.init = function() {
		debug.debug('SessionApp - init');
		debug.debug(self.api_url);

		self.container = $('.holder.session');

		self.bindings();

		self.load();


	};

	self.load = function() {

		var url = self.api_url;

		$.get(url, function(data) {
			debug.debug(data);

			if (self.local_data) {

				if (data.updated != self.local_data.updated) {
					debug.debug('data changed.')
					self.local_data = data;
					self.display(data);
				} else {
					debug.debug('not changed')
				}

			} else {
				self.local_data = data;
				debug.debug('not in cache yet.')
				self.display(data);
			}

			$('#countdown').countdown({
				until : data.time_start,
				format : 'DHMS'
			});

		})
	};

	self.bindings = function() {

		$(window).resize(function() {
			if (this.resizeTO)
				clearTimeout(this.resizeTO);
			this.resizeTO = setTimeout(function() {
				$(this).trigger('resizeEnd');
			}, 500);
		});

		$(window).bind('resizeEnd', function(e) {
			self.dimensions = self.getDimensions(self.container);
			self.display(self.local_data);
		});
	};



	self.display = function(data) {


		var d = {
			object : data,
		}

		html = nj.render('shortcutter/nj/session_detail_grid.html', d);
		self.container.html(html);

		var grid = new Array;
		var shots = new Array;
		var k = 0;
		for (var i in data.slots) {
			var slot = data.slots[i];
			grid[i] = new Array;
			//debug.debug('slot:', i, slot)

			for (var j in slot.shots) {
				var shot = slot.shots[j]
				//debug.debug('shot:', j, shot)
				shots[k] = {
					shot : shot,
					domElement : $('#' + shot.uuid, self.container)
				};
				k++;
			};

		}

		for (var i in shots) {
			
			var shot = new ShotApp;
			shot.local_data = shots[i].shot;
			shot.api_url = shots[i].shot.resource_uri;
			shot.container = shots[i].domElement;
			shot.shotSize = self.shotSize;
			shot.map = self.map;
			shot.init(true);
			
			shots[i] = shot;
			
			// self.displayShot(shot, true);
		}

		debug.debug('shots:', shots);

	};


};
