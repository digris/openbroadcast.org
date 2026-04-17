;
$(document).ready(function() {

	$('ul.arating a').live('click', function(e) {
		e.preventDefault();
		var el = $(this);
		var base_url = el.attr('href').slice(0, -2);
		var url = base_url + el.attr('data-vote') + '/';

		$.getJSON(url, function(data) {
			var items = [];

			$.each(data.choices, function(key, val) {
				var choice = val

				//var cel = $('ul.arating a.vote' + choice.key);
				var cel = $('ul.arating a.vote' + choice.key, el.parent().parent().parent()); // sorry...


				$('span.count', cel).html(choice.count);
				if(choice.active) {
					cel.addClass('active')
					cel.attr('data-vote', 0);
				} else {
					cel.removeClass('active');
					cel.attr('data-vote', choice.key );
				}
			});

		});

	});

}); 