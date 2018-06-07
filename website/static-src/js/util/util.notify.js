(function( window, undefined ) {

	var util = util || {};
	
	var UtilNotify = (function() {
		
		var self = this;
		
		this.init = (function() {
			
			// console.log('UtilNotify: init');
			
			// button switcher
			if(! this.havePermission && window.webkitNotifications) {
				$('.util.notify.enable').show()
				.live('click', function(){
					self.requestPermission();
				});
			};
			
			
		});
		
		this.requestPermission = function() {
			window.webkitNotifications.requestPermission();
		};
		
		this.havePermission = function() {
			if(window.webkitNotifications.checkPermission() == 0){
				return true;
			} else {
				return false;
			}
			
		};
		
		this.notify = function(noteObject, targetUrl) {
			
			if(self.havePermission) {
				
				var n = window.webkitNotifications.createNotification(
					null,
					'Download ready!',
					'Here is the notification text'
				);
				
				n.onclick = function (x) {
					//window.open("http://stackoverflow.com/a/13328397/1269037");
					
					window.focus();
					this.cancel();
					
					//notification.close();
				}
				n.show();
				
			} else {
				self.requestPermission();
			}
			
		};
		
	});
	
	
	util.notify = new UtilNotify;
	util.notify.init();
	
 
})(window);