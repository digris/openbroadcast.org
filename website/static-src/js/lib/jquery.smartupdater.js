/**
* smartupdater - jQuery Plugin
*  
* Version - 2.0.04
*
* Copyright (c) 2010 Vadim Kiryukhin
* vkiryukhin @ gmail.com
* 
* http://www.eslinstructor.net/demo/smartupdater2/smartupdater_home.html
*
* Dual licensed under the MIT and GPL licenses:
*   http://www.opensource.org/licenses/mit-license.php
*   http://www.gnu.org/licenses/gpl.html
*
* Based on the work done by Terry M. Schmidt and the jQuery ekko plugin.
*
* USAGE:
*
*	$("#myObject").smartupdater({
*			url : "demo.php",
*			minTimeout : 60000
*			}, function (data) {
*				//process data here;
*			}
*		);
*		
*	Public functions:
*		$("#myObject").smartupdaterStop();
*		$("#myObject").smartupdaterRestart();
*		$("#myObject").smartupdaterSetTimeout();
*
*	Public Attributes:
*		var smStatus = $("#myObject")[0].smartupdaterStatus.state; // "ON" | "OFF" | "undefined"
*		var smTimeout = $("#myObject")[0].smartupdaterStatus.timeout; // current timeout
*
**/

(function(jQuery) {
	jQuery.fn.smartupdater = function (options, callback) {

		return this.each(function () {
			var elem = this;

			elem.settings = jQuery.extend({
				url			: '',		// see jQuery.ajax for details
				type		: 'get', 	// see jQuery.ajax for details
				data		: '',   	// see jQuery.ajax for details
				dataType	: 'text', 	// see jQuery.ajax for details
						
				minTimeout	: 60000, // Starting value for the timeout in milliseconds; default 1 minute.
				maxTimeout	: ((1000 * 60) * 60), // Default 1 hour.
				multiplier	: 2,    //if set to 2, interval will double each time the response hasn't changed.
				maxFailedRequests : 10 // smartupdater stops after this number of consecutive ajax failures; 
				
			}, options);
				
			elem.smartupdaterStatus = {};
			elem.smartupdaterStatus.state = '';
			elem.smartupdaterStatus.timeout = 0;

			var es = elem.settings;
				
			es.prevContent = '';
			es.originalMinTimeout = es.minTimeout;
			es.failedRequests = 0;
			es.response = '';
				
			function start() {
				$.ajax({url: es.url,
					type: es.type,
					data: es.data,
					dataType: es.dataType,
					cache: false,
					success: function (data, statusText, xhr) {
						
						if(es.dataType == 'json' && data.smartupdater) {
								es.originalMinTimeout = data.smartupdater;
						}

						if (es.prevContent != xhr.responseText) {
							es.prevContent = xhr.responseText;
							es.minTimeout = es.originalMinTimeout;
							elem.smartupdaterStatus.timeout = es.minTimeout;
							es.periodicalUpdater = setTimeout(start, es.minTimeout);
							callback(data);
						} else if (es.multiplier > 1) {
							es.minTimeout = (es.minTimeout < es.maxTimeout) ? Math.round(es.minTimeout * es.multiplier) : es.maxTimeout;
							elem.smartupdaterStatus.timeout = es.minTimeout;
							es.periodicalUpdater = setTimeout(start, es.minTimeout);
						} else if (es.multiplier <= 1) {
							es.minTimeout = es.originalMinTimeout;
							elem.smartupdaterStatus.timeout = es.minTimeout;
							es.periodicalUpdater = setTimeout(start, es.minTimeout);
						}
						
						es.failedRequests = 0;
						elem.smartupdaterStatus.state = 'ON';
					}, 
							
					error: function() { 
						if ( ++es.failedRequests < es.maxFailedRequests ) {
							es.periodicalUpdater = setTimeout(start, es.minTimeout);
							elem.smartupdaterStatus.timeout = es.minTimeout;
						} else {
							clearTimeout(es.periodicalUpdater);
							elem.smartupdaterStatus.state = 'OFF';
						}
					}
				});
			} 
				
			es.fnStart = start;
			
			
			
			start();
		});
	}; 
	
	jQuery.fn.smartupdaterStop = function () {
		return this.each(function () {
			var elem = this;
			clearTimeout(elem.settings.periodicalUpdater);
            elem.smartupdaterStatus.state = 'OFF';
		});
	}; 
        
    jQuery.fn.smartupdaterRestart = function () {        
		return this.each(function () {
			var elem = this;
			clearTimeout(elem.settings.periodicalUpdater);
            elem.settings.minTimeout = elem.settings.originalMinTimeout;
            elem.settings.fnStart();
		});
	}; 
	
	jQuery.fn.smartupdaterSetTimeout = function (period) {
		return this.each(function () {
			var elem = this;
			clearTimeout(elem.settings.periodicalUpdater);
			this.settings.originalMinTimeout = period;
            this.settings.fnStart();
		});
	}; 
	
})(jQuery);












