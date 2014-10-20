PusherApp = function() {

	var self = this;

	this.socket_url;
	this.socket;

	this.subscriptions = [];

	this.init = function() {
		
		$.log('PusherApp: init');
		
		setTimeout(function(){
			self.connect()
		}, 100);
	};
	
	this.connect = function() {
		
		$.log('PusherApp: connect');

		try {
			self.socket = io.connect(self.socket_url);
			self.socket.on('push', function(data) {
				
				// routing data..
				if(data.type == 'update') {
					console.log('update for:', data.route);
					self.trigger(data.route);
				};


			});

		} catch(err) {
			console.log(err.message);
		}
	};
	
	this.subscribe = function(route, callback) {
		this.subscriptions.push({
			route: route,
			callback: callback
		});
	};
	
	this.trigger = function(route) {
		for(i in self.subscriptions) {
			if(self.subscriptions[i].route == route) {
				self.subscriptions[i].callback();
			}
		};
	};

	this.bindings = function() {

	};
}; 	