PushyApp = function() {

	var self = this;

	this.socket_url;
	this.socket;
	this.debug = false;
	this.subscriptions = [];

	this.init = function() {
		if(self.debug){
			console.log('PushyApp - init');
		}
		setTimeout(function(){
			self.connect()
		}, 100);
	};
	
	this.connect = function() {

		try {
			
			self.socket = io.connect(self.socket_url);
			self.socket.on('push', function(data) {

				if(self.debug){
					console.log('PushyApp - push:', data);
				}

				if(data.type == 'create') {
					if(self.debug){
						console.log('PushyApp - create:', data.route);
					}
					self.trigger(data);
				};

				if(data.type == 'update') {
					if(self.debug){
						console.log('PushyApp - update:', data.route);
					}
					self.trigger(data);
				};

				if(data.type == 'delete') {
					if(self.debug){
						console.log('PushyApp - delete:', data.route);
					}
					self.trigger(data);
				};

			});

		} catch(err) {
			//alert('Unable to connect to socket-server');
			console.log(err.message);
		}
	};
	
	this.subscribe = function(route, callback) {
		if(self.debug){
			console.log('PushyApp - subscribe:', route);
		}
		this.subscriptions.push({
			route: route,
			callback: callback
		});
	};
	
	this.trigger = function(data) {
		for(i in self.subscriptions) {
			if(self.subscriptions[i].route == data.route) {
				self.subscriptions[i].callback(data);
			}
		};
	};

	this.bindings = function() {

	};
}; 	
