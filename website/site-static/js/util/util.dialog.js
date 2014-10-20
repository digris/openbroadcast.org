/*
 * requires jquery.qtip2
 * https://github.com/craga89/qtip2
 */

(function(window, undefined) {

	var util = util || {};

	var UtilDialog = (function() {

		var self = this;

		this.init = (function() {
			console.log('UtilDialog: init');
		});

		this.show = function(object) {

			if (object.url) {
				$('<div />').qtip({
					content : {
						text : '<div class="loading"><span class="throbber large"></span></loading>',
						//ajax : {
						//	url : url,
						//	success : function(data, status) {
						//		this.set('content.text', data);
						//	}
						//},
						title : {
							text : 'aa&nbsp;', // Give the tooltip a title using each elements text
							button : true
						}
					},
					position : {
						my : 'center',
						at : 'center',
						target : $(window)
					},
					show : {
						ready : true, // Show it straight away
						modal : {
							on : true, // Make it modal (darken the rest of the page)...
							blur : false // ... but don't close the tooltip when clicked
						}
					},
					hide : false, // We'll hide it maunally so disable hide events
					style : 'dialog dialog-base', // Add a few styles
					events : {
						// Hide the tooltip when any buttons in the dialogue are clicked
						render : function(event, api) {
							//$('button', api.elements.content).click(api.hide);
						},
						// Destroy the tooltip once it's hidden as we no longer need it!
						hide : function(event, api) {
							api.destroy();
						}
					}
				});
			} else {
				$('<div />').qtip({
					content : {
						text : '<div>' + object.text + '</div>',
						title : {
							text : object.title,
							button : true
						}
					},
					position : {
						my : 'center',
						at : 'center',
						target : $(window)
					},
					show : {
						ready : true,
						modal : {
							on : true,
							blur : true
						}
					},
					hide : false,
					style : 'dialog dialog-base qtip-rounded',
					events : {
						render : function(event, api) {
							//$('button', api.elements.content).click(api.hide);
						},
						hide : function(event, api) {
							api.destroy();
						}
					}
				});
			}

		};

	});

	util.dialog = new UtilDialog;
	util.dialog.init();

})(window);

