/*
 * Some useful util functions
 * (as jQuery plugins)
 */
;
(function (jQuery) {

    var union = function (array1, array2) {
        var hash = {}, union = [];
        $.each($.merge($.merge([], array1), array2), function (index, value) {
            hash[value] = value;
        });
        $.each(hash, function (key, value) {
            union.push(key);
        });
        return union;
    };

    jQuery.fn.union = union;
    jQuery.union = union;

})(jQuery);
;

// url params
(function (jQuery) {

    var insert_uri_param = function(sourceUrl, parameterName, parameterValue, replaceDuplicates) {

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


    jQuery.fn.insert_uri_param = insert_uri_param;
    jQuery.insert_uri_param = insert_uri_param;

})(jQuery);


(function (jQuery) {

    var decodeHTMLEntities = function (str) {
        if (str && typeof str === 'string') {
            var element = document.createElement('div');
            // strip script/html tags
            str = str.replace(/<script[^>]*>([\S\s]*?)<\/script>/gmi, '');
            str = str.replace(/<\/?\w(?:[^"'>]|"[^"]*"|'[^']*')*>/gmi, '');
            element.innerHTML = str;
            str = element.textContent;
            element.textContent = '';
        }

        return str;
    }

    jQuery.fn.decodeHTML = decodeHTMLEntities;
    jQuery.decodeHTML = decodeHTMLEntities;

})(jQuery);



/*
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};
*/

if (typeof String.prototype.endsWith !== 'function') {
    String.prototype.endsWith = function(suffix) {
        return this.indexOf(suffix, this.length - suffix.length) !== -1;
    };
};


function arrRemove(arr, from, to) {
  var rest = arr.slice((to || from) + 1 || arr.length);
  this.length = from < 0 ? arr.length + from : from;
  return arr.push.apply(arr, rest);
};
function isInt(value) {
    return !isNaN(parseInt(value,10)) && (parseFloat(value,10) == parseInt(value,10));
};