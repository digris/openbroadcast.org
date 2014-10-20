/*
 * Copyright 2012, Jonas Ohrstrom  - ohrstrom@gmail.com
 * See LICENSE.txt
 */


var util = util || {};

util.uri_param_insert = function(sourceUrl, parameterName, parameterValue, replaceDuplicates) {

	if((sourceUrl == null) || (sourceUrl.length == 0))
		sourceUrl = document.location.href;
	var urlParts = sourceUrl.split("?");
	var newQueryString = "";
	if(urlParts.length > 1) {
		var parameters = urlParts[1].split("&");
		for(var i = 0; (i < parameters.length); i++) {
			var parameterParts = parameters[i].split("=");
			if(!(replaceDuplicates && parameterParts[0] == parameterName)) {
				if(newQueryString == "")
					newQueryString = "?";
				else
					newQueryString += "&";
				newQueryString += parameterParts[0] + "=" + parameterParts[1];
			}
		}
	}
	if(newQueryString == "")
		newQueryString = "?";
	else
		newQueryString += "&";
	newQueryString += parameterName + "=" + parameterValue;

	return urlParts[0] + newQueryString;
};

util.string_random = function(length) {

	var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz'.split('');

	if(!length) {
		length = Math.floor(Math.random() * chars.length);
	}

	var str = '';
	for(var i = 0; i < length; i++) {
		str += chars[Math.floor(Math.random() * chars.length)];
	}
	return str;
};



util.format_time = function(secs)
{
    var t = new Date(1970,0,1);
    t.setSeconds(secs);
    if(secs < 3600) {
    	var s = t.toTimeString().substr(3,5);
    } else {
    	var s = t.toTimeString().substr(0,8);
    }
    
    
    if(secs > 86399)
        s = Math.floor((t - Date.parse("1/1/70")) / 3600000) + s.substr(2);
    return s;
}

$.fn.serializeObject = function() {
	var o = {};
	var a = this.serializeArray();
	$.each(a, function() {
		if(o[this.name]) {
			if(!o[this.name].push) {
				o[this.name] = [o[this.name]];
			}
			o[this.name].push(this.value || '');
		} else {
			o[this.name] = this.value || '';
		}
	});
	return o;
};


/*
 * AJAX CSRF handling
 */

$(document).ajaxSend(function(event, xhr, settings) {
	function getCookie(name) {
		var cookieValue = null;
		if(document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for(var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if(cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	function sameOrigin(url) {
		// url could be relative or scheme relative or absolute
		var host = document.location.host;
		// host + port
		var protocol = document.location.protocol;
		var sr_origin = '//' + host;
		var origin = protocol + sr_origin;
		// Allow absolute or scheme relative URLs to same origin
		return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
	}

	function safeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	if(!safeMethod(settings.type) && sameOrigin(settings.url)) {
		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	}
});



util.get_position = function(e) {

	//this section is from http://www.quirksmode.org/js/events_properties.html
	var targ;
	if(!e)
		e = window.event;
	if(e.target)
		targ = e.target;
	else if(e.srcElement)
		targ = e.srcElement;
	if(targ.nodeType == 3)// defeat Safari bug
		targ = targ.parentNode;

	// jQuery normalizes the pageX and pageY
	// pageX,Y are the mouse positions relative to the document
	// offset() returns the position of the element relative to the document
	var x = e.pageX - $(targ).offset().left;
	var y = e.pageY - $(targ).offset().top;

	return {
		"x" : x,
		"y" : y
	};
};


util.delay = (function(){
    var timer = 0;
    return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
      };
})();