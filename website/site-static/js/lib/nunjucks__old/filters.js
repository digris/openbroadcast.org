var nunjucks_register_filters = function(nj) {

				nj.addFilter('shorten', function(str, count) {

				    return str.slice(0, count || 5);
				});
				nj.addFilter('truncate_chars_inner', function(str, count) {

					if(str && str.length > count) {
					
						var limit = Math.floor((count - 5) / 2)
						var a = str.substr(0, limit);
						var b = str.substr(str.length - limit, limit);
					
						return a + ' ... ' + b;
					} else {
						return str;
					}

				    
				});
				
				nj.addFilter('highlight', function(str, query) {
				    //return str.slice(0, 4) + query;
				    var re = new RegExp(query,"gi");
				    var highlighted = str.replace(re, '<em class="highlight">' + query + '</em>');
				    return highlighted
				    
				});
				
				
				nj.addFilter('format_timestamp', function(time) {
				
					return '{0}/{1}/{2} {3}:{4}'.format(
						time.substr(0,4),
						time.substr(5,2),
						time.substr(8,2),
						// time
						time.substr(11,2),
						time.substr(14,2)
						);
					
				});
				
				nj.addFilter('format_datetime', function(time, part) {
				
					var ret;
				
					if(part == 'datetime') {

						ret =  '{0}/{1}/{2} {3}:{4}'.format(
							time.substr(0,4),
							time.substr(5,2),
							time.substr(8,2),
							// time
							time.substr(11,2),
							time.substr(14,2)
						);
					}
				
					if(part == 'date') {

						ret =  '{0}/{1}/{2}'.format(
							time.substr(0,4),
							time.substr(5,2),
							time.substr(8,2)
						);
					}
				
					if(part == 'time') {

						ret = '{0}:{1}'.format(
							time.substr(11,2),
							time.substr(14,2)
						);
					}
					
					
						
					return ret;
					
				});
				
				nj.addFilter('ms2time', function(time) {
					
					if(time == 0) {
						return '00:00:000';
					}
					
					time = Math.abs(time);
					
					var millis= time % 1000;
				    time = parseInt(time/1000);
				    var seconds = time % 60;
				    time = parseInt(time/60);
				    var minutes = time % 60;
				    time = parseInt(time/60);
				    var hours = time % 24;
				    var out = "";
				    
				    if(hours && hours > 0) {
				    	out += hours + ':';
				    } else {
				    	// out += '0' + ':';
				    }
				    
				    if(minutes && minutes > 0) {
				    	out += minutes + ':';
				    } else {
				    	out += '00' + ':';
				    }
				    
				    if(seconds && seconds > 0) {
				    	out += seconds + ':';
				    } else {
				    	out += '00' + ':';
				    }
				    
				    if(millis && millis > 0) {
				    	out += millis + '';
				    } else {
				    	out += '000' + '';
				    }
				    
				    /*
				    if(hours && hours > 0) out += hours + "" + ((hours == 1)?":":":") + "";
				    if(minutes && minutes > 0) out += minutes + "" + ((minutes == 1)?":":":") + "";
				    if(seconds && seconds > 0) out += seconds + "" + ((seconds == 1)?":":":") + "";
				    if(millis&& millis> 0) out += millis+ "" + ((millis== 1)?"":"") + "";
				    */
				    return out.trim();
				});


				return nj;
};


String.prototype.format = function() {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};