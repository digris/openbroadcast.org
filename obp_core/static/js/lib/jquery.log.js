(function(jQuery) {

	/**
	 * log
	 * 
	 * http://www.stoimen.com/blog/2009/07/27/jquery-debug-plugin/
	 *
	 * write debug errors to the console or
	 * alert them if the browser does not support
	 * the console object
	 *
	 * @public
	 * @param {Object}
	 * @return {Void}
	 */
	var log = function( object ) {
		if ( typeof console == 'object' )
			console.log( object );
		else if ( typeof opera == 'object' )
			opera.postError( object );
		else
			alert(object);
	}

	jQuery.fn.log = log;
	jQuery.log = log;

})(jQuery);