/*
 * JINGLE SCRIPTS
 */

/* core */

JingleUi = function() {

	var self = this;

	this.interval = false;
	this.interval_loops = 0;
	this.interval_duration = 120000;
	// this.interval_duration = false;
	this.api_url = false;
	this.api_url_simple = false; // used for listings as much faster..
	
	this.inline_dom_id = 'inline_jingle_holder';
	this.inline_dom_element;
	
	this.current_data;
	this.current_items = new Array;

	this.init = function() {
		
		console.log('JingleUi: init');
		console.log(self.api_url);
		
		this.inline_dom_element = $('#' + this.inline_dom_id);

		self.iface();
		self.bindings();

		// set interval and run once
		if(self.interval_duration) {
			self.set_interval(self.run_interval, self.interval_duration);
		}
		setTimeout(function(){
			self.run_interval();
		},1000);
		
		
	};

	this.iface = function() {
		// this.floating_inline('lookup_providers', 120)
	};

	this.bindings = function() {


		//self.inline_dom_element.hide(20000)
		var container = $('#inline_jingle_container');

		// states - open / close
		// main box
		$('.ui-persistent > .header', container).live('click', function(e) {
			e.preventDefault();
			var parent = $(this).parents('.ui-persistent');
			if (!parent.hasClass('expanded')) {
				parent.data('uistate', 'expanded');
			} else {
				parent.data('uistate', 'hidden');
			}
		});

		
		// actions
		$('.jingle_holder > .header a', container).live('click', function(e) {
			e.preventDefault();
			
			var id = $(this).parents('.jingle_holder').data('object_id');
			var action = $(this).data('action');
			
			$.log(action, id);
			
			if(action == 'delete' && confirm('Sure?')) {
				// self.delete_jingle(id);
			}
			
			//var name = $('input.name', $(this)).val();
			//self.create_jingle(name);
		});

		// list-inner items
		$('.list.item a', self.inline_dom_element).live('click', function(e) {
			
			e.preventDefault();
			var container = $(this).parents('.list.item');
			var action = $(this).data('action');
			var resource_uri = container.data('resource_uri');

			
			if(action == 'play') {

			};

			
		});

		// selector
		
		$('#jingles_inline_selector').live('change', function(e){
			e.preventDefault();
			
			var resource_uri = $(this).val();

			$('.jingle_holder', self.inline_dom_element).hide();

			$('#default_jingle_set').data('uistate', resource_uri);

		setTimeout(function(){
			self.update_jingles();
		},50);
			//self.update_jingles();

			/*
			$.ajax({
				url: resource_uri + 'set-current/',
				type: 'GET',
				dataType: "json",
				contentType: "application/json",
				processData:  false,
				success: function(data) {
					self.run_interval();
				},
				async: false
			});
			*/
			
		});
		
		

	};

	// interval
	this.set_interval = function(method, duration) {
		self.interval = setInterval(method, duration);
	};
	this.clear_interval = function(method) {
		self.interval = clearInterval(method);
	};

	this.run_interval = function() {
		self.interval_loops += 1;

		// Put functions needed in interval here
		self.update_jingles();

	};
	


	this.update_jingles = function() {
		
		$.getJSON(self.api_url_simple, function(data) {
			self.update_jingle_selector(data);
		});
		
		
		var resource_uri = $('#default_jingle_set').data('resource_uri');
		
		
		if (resource_uri != 'init') {
		
			$.getJSON(resource_uri, function(data) {
				self.update_jingle_display(data);
			});
		};
			
			// maybe not the best way. think about alternatives...
			try {
				setTimeout(function(){
					alibrary.playlist_editor.rebind();
				}, 500);
				
			} catch(e) {
				console.log('error', e);
			}
		
	};
	
	this.update_jingles_callback = function(data) {

		self.update_jingle_display(data);
		self.update_jingle_selector(data);
		this.current_data = data;
	};
	
	this.update_jingle_display = function(data) {

		// console.log(data)
		
		
		console.log('JINGLE DATA', data)

		var status_map = new Array;
		status_map[0] = 'init';
		status_map[1] = 'done';
		status_map[2] = 'ready';
		status_map[3] = 'progress';
		status_map[4] = 'downloaded';
		status_map[99] = 'error';

		//for (var i in data.objects) {

			// var item = data.objects[i];
			var item = data;
			var target_element = $('#jingle_holder_' + item.id);

			item.status_key = status_map[item.status];
			
			console.log('ITEM:', item);
			
			// console.log(item);

			// filter out current jingle
			if (item.is_current || 1 == 1) {

				if (item.id in self.current_items) {
					self.current_items[item.id] = item;
					console.log('item already present');

					if(item.updated != target_element.attr('data-updated')) {
						console.log('update detected');
						
						var html = ich.tpl_jingles_inline({object: item});
						
						html.attr('data-updated', item.updated);
						target_element.replaceWith(html);
					}
					
				} else {

					var html = ich.tpl_jingles_inline({object: item});
					html.attr('data-last_status', item.status);
					self.inline_dom_element.append(html);

					self.current_items[item.id] = item;
				}
			} else {
				// remove item if not the current one
				target_element.remove();
			}
		//}
	};
	
	this.update_jingle_selector = function(data) {
		
		console.log('this.current_data, data', data);

		if(data.objects.length > 0) {
		
			if( ! Object.equals(this.current_data, data)) {
				console.log('data changed');

                // TODO: fix ich templates resp refactor to nj
				//var html = ich.tpl_jingles_inline_selector(data);
				//$('.jingle-selector', self.inline_dom_element.parent()).html(html);
	
			} else {
				console.log('data unchanged');
			}
		
		}
	};


};








Object.equals = function( x, y ) {
  if ( x === y ) return true;
    // if both x and y are null or undefined and exactly the same

  if ( ! ( x instanceof Object ) || ! ( y instanceof Object ) ) return false;
    // if they are not strictly equal, they both need to be Objects

  if ( x.constructor !== y.constructor ) return false;
    // they must have the exact same prototype chain, the closest we can do is
    // test there constructor.

  for ( var p in x ) {
    if ( ! x.hasOwnProperty( p ) ) continue;
      // other properties were tested using x.constructor === y.constructor

    if ( ! y.hasOwnProperty( p ) ) return false;
      // allows to compare x[ p ] and y[ p ] when set to undefined

    if ( x[ p ] === y[ p ] ) continue;
      // if they have the same strict value or identity then they are equal

    if ( typeof( x[ p ] ) !== "object" ) return false;
      // Numbers, Strings, Functions, Booleans must be strictly equal

    if ( ! Object.equals( x[ p ],  y[ p ] ) ) return false;
      // Objects and Arrays must be tested recursively
  }

  for ( p in y ) {
    if ( y.hasOwnProperty( p ) && ! x.hasOwnProperty( p ) ) return false;
      // allows x[ p ] to be set to undefined
  }
  return true;
}