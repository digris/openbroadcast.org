var nunjucks_register_filters = function (nj) {

    nj.addFilter('shorten', function (str, count) {

        if(str == undefined) {
            return '';
        }

        return str.slice(0, count || 5);
    });


    nj.addFilter('truncate_chars_inner', function (str, count) {


        try {

            if (str && str.length > count) {

                var limit = Math.floor((count - 5) / 2)
                var a = str.substr(0, limit);
                var b = str.substr(str.length - limit, limit);

                return a + ' ... ' + b;
            } else {
                return str;
            }
        } catch (e) {
            return '';
        }
    });

    nj.addFilter('highlight', function (str, query) {
        //return str.slice(0, 4) + query;
        var re = new RegExp(query, "gi");
        var highlighted = str.replace(re, '<em class="highlight">' + query + '</em>');
        return highlighted

    });


    nj.addFilter('format_timestamp', function (time) {

        if(time == undefined) {
            return '';
        }


        return '{0}/{1}/{2} {3}:{4}'.format(
            time.substr(0, 4),
            time.substr(5, 2),
            time.substr(8, 2),
            // time
            time.substr(11, 2),
            time.substr(14, 2)
        );

    });

    nj.addFilter('format_datetime', function (time, part) {

        if(time == undefined) {
            return '';
        }

        var ret;

        if (part == 'datetime') {

            ret = '{0}/{1}/{2} {3}:{4}'.format(
                time.substr(0, 4),
                time.substr(5, 2),
                time.substr(8, 2),
                // time
                time.substr(11, 2),
                time.substr(14, 2)
            );
        }

        if (part == 'date') {

            ret = '{0}/{1}/{2}'.format(
                time.substr(0, 4),
                time.substr(5, 2),
                time.substr(8, 2)
            );
        }

        if (part == 'time') {
            ret = '{0}:{1}'.format(
                time.substr(11, 2),
                time.substr(14, 2)
            );
        }

        if (part == 'time_s') {
            ret = '{0}:{1}:{2}'.format(
                time.substr(11, 2),
                time.substr(14, 2),
                time.substr(17, 2)
            );
        }


        return ret;

    });

    nj.addFilter('ms2time', function (time) {

        if(time == undefined) {
            return '';
        }

        if (time == 0) {
            return '00:00:000';
        }

        time = Math.abs(time);

        var millis = time % 1000;
        time = parseInt(time / 1000);
        var seconds = time % 60;
        time = parseInt(time / 60);
        var minutes = time % 60;
        time = parseInt(time / 60);
        var hours = time % 24;
        var out = "";

        if (hours && hours > 0) {
            if (hours < 10) {
                out += '0';
            }
            out += hours + ':';
        } else {
            // out += '0' + ':';
        }

        if (minutes && minutes > 0) {
            if (minutes < 10) {
                out += '0';
            }
            out += minutes + ':';
        } else {
            out += '00' + ':';
        }

        if (seconds && seconds > 0) {
            if (seconds < 10) {
                out += '0';
            }
            out += seconds + '';
        } else {
            out += '00' + '';
        }

        /*
        if (millis && millis > 0) {
            if (millis < 10) {
                out += '0';
            }
            out += millis + '';
        } else {
            out += '000' + '';
        }
        */

        /*
         if(hours && hours > 0) out += hours + "" + ((hours == 1)?":":":") + "";
         if(minutes && minutes > 0) out += minutes + "" + ((minutes == 1)?":":":") + "";
         if(seconds && seconds > 0) out += seconds + "" + ((seconds == 1)?":":":") + "";
         if(millis&& millis> 0) out += millis+ "" + ((millis== 1)?"":"") + "";
         */
        return out.trim();
    });

    nj.addFilter('s2time', function (time) {

        if(time == undefined) {
            return '';
        }

        if (time == 0) {
            return '00:00';
        }

        time = Math.abs(time);


        var seconds = time % 60 * 60;
        time = parseInt(time / 60);
        var minutes = time % 60;
        time = parseInt(time / 60);
        var hours = time % 24;
        var out = "";


        if (hours && hours > 0) {
            out += hours + ':';
        } else {
            // out += '0' + ':';
        }

        if (minutes && minutes > 0) {
            if (minutes < 10) {
                out += '0';
            }
            out += minutes + ':';
        } else {
            out += '00' + ':';
        }

        if (seconds && seconds > 0) {
            if (seconds < 10) {
                out += '0';
            }
            out += seconds;
        } else {
            out += '00';
        }

        return out.trim();
    });

    nj.addFilter('datetime2hhmm', function (datetime) {
        var value = datetime.substr(11, 5);
        return value
    });

    nj.addFilter('datetime2hhmmss', function (datetime) {
        var value = datetime.substr(11, 8);
        return value
    });

    nj.addFilter('linebreaksbr', function (str) {
        var breakTag = '<br>';
        return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
    });

    /*
    nj.addFilter('split', function (str, separator) {

        if(str == undefined) {
            return '';
        }

        if(separator == undefined) {
            separator = ',';
        }

        return ['first', 'second', 'third']
    });
    */

    nj.addFilter('urlize', function (str, target) {

        if(str == undefined) {
            return '';
        }

        return str.autolink()
    });


    return nj;
};


String.prototype.format = function () {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{' + i + '\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};

String.prototype.autolink = function() {
    var k, linkAttributes, option, options, pattern, v;
    options = 1 <= arguments.length ? __slice.call(arguments, 0) : [];

    pattern = /(^|[\s\n]|<br\/?>)((?:https?|ftp):\/\/[\-A-Z0-9+\u0026\u2019@#\/%?=()~_|!:,.;]*[\-A-Z0-9+\u0026@#\/%=~()_|])/gi;
    if (!(options.length > 0)) {
      return this.replace(pattern, "$1<a href='$2'>$2</a>");
    }
    option = options[0];
    linkAttributes = ((function() {
      var _results;
      _results = [];
      for (k in option) {
        v = option[k];
        if (k !== 'callback') {
          _results.push(" " + k + "='" + v + "'");
        }
      }
      return _results;
    })()).join('');
    return this.replace(pattern, function(match, space, url) {
      var link;
      link = (typeof option.callback === "function" ? option.callback(url) : void 0) || ("<a href='" + url + "'" + linkAttributes + ">" + url + "</a>");
      return "" + space + link;
    });
  };

