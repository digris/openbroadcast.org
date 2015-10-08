NunjucksApp = function() {

	var self = this;

	this.socket_url;
	this.socket;
	this.debug = false;
	this.subscriptions = [];

	this.init = function() {
		if(self.debug){
			console.log('NunjucksApp - init');
		}
	};

}; 	