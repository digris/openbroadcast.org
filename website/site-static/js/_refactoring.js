
// ORIGINAL PLACE:
base.ui.sidebar = function() {	

	// Playlist item, delete action
	$('div.playlist_holder .list_item .action.delete').live('click', function() {

		var param = $(this).attr('href').split(':');
		var playlist_id = param[0].substring(1);
		var media_id = param[1];

		// Remove element from html
		$(this).parent().parent().remove();
		
		// Request url
		var url = base.vars.base_url + 'ajax/playlist_remove_item';
		
		// Request data
		var data = {
			playlist_id : playlist_id,
			media_id : media_id
		};

		// AJAX Call
		$.ajax( {
			url : url,
			type : "POST",
			data : data,
			dataType : "json",
			success : function(result) {
				if (true == result['status']) {
						$('#element').load('/ui/sidebar_playlist' + '?r=' + util.string_random(20));
				} else {
					base.ui.ui_message(result['message']);
				}
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				base.ui.ui_message(errorThrown);
			}
		});

		return false;
	});
	

	
	// Playlist as a whole, delete action
	$('div.playlist_holder .header .action.delete').live('click', function() {

		var playlist_id = $(this).attr('href').substring(1);

		// Remove element from html
		$(this).parent().parent().parent().remove();
		
		// Request url
		var url = base.vars.base_url + 'ajax/playlist_remove';
		
		// Request data
		var data = {
			playlist_id : playlist_id
		};

		// AJAX Call
		$.ajax( {
			url : url,
			type : "POST",
			data : data,
			dataType : "json",
			success : function(result) {
				if (true == result['status']) {
						$('#element').load('/ui/sidebar_playlist' + '?r=' + util.string_random(20));
				} else {
					base.ui.ui_message(result['message']);
				}
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				base.ui.ui_message(errorThrown);
			}
		});

		return false;
	});
	

	
	// Playlist as a whole, edit name
	$('div.playlist_holder .header .action.edit').live('click', function() {

		var edit = $('div.edit', $(this).parent().parent().parent());
		
		if(edit.css("display") == "none") {
			edit.show();
		} else {
			edit.hide();
		}

		return false;
	});
	
	// Action on name change & Enter
	$('div.playlist_holder .panel .edit input').live('keypress', function (e) {

		if(e.keyCode == 13 || e.keyCode == 9) {
			e.preventDefault();
			
			var playlist_id = $(this).attr('id').split("_").pop();;
			var name = $(this).val();
			
			// Request url
			var url = base.vars.base_url + 'ajax/playlist_rename';
			
			// Request data
			var data = {
				playlist_id : playlist_id,
				name : name
			};

			// AJAX Call
			$.ajax( {
				url : url,
				type : "POST",
				data : data,
				dataType : "json",
				success : function(result) {
					if (true == result['status']) {
							$('#element').load('/ui/sidebar_playlist' + '?r=' + util.string_random(20));
					} else {
						base.ui.ui_message(result['message']);
					}
				},
				error : function(XMLHttpRequest, textStatus, errorThrown) {
					base.ui.ui_message(errorThrown);
				}
			});
			
			return false;
		}
		
	});
	
	
	/*
	 * Playlist / Basket create / defaults
	 */
	$('div.playlist .settings .create a').live('click', function() {
		
		var name = $(this).parent().find('input.create').val();
		var url = base.vars.base_url + 'ajax/playlist_create';
		
		var action = 'reload';
		
		var data = {
			'name' : name,
			'subtype' : 'basket',
			'action' : action
		};

		// AJAX Call
		$.ajax( {
			url : url,
			type : "POST",
			data : data,
			dataType : "json",
			success : function(result) {
				if (true == result['status']) {
					$('#element').load('/ui/sidebar_playlist' + '?r=' + util.string_random(20));
				} else {
					base.ui.ui_message(result['message']);
				}
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				base.ui.ui_message(errorThrown);
			}
		});
		
		return false;
	});
	
	$('div.playlist .settings .default select').live('change', function(e) {
		
		var key = $(this).attr('id');
		var value = $(this).parent().find('select.default').val();

		var rel = base.vars.context + '_' + base.vars.section;
		var url = base.vars.base_url + 'ajax/filter_set_value';
		var action = 'reload';
		
		var data = {
			'key' : key,
			'rel' : rel,
			'value' : value,
			'action' : action
		};

		// AJAX Call
		$.ajax( {
			url : url,
			type : "POST",
			data : data,
			dataType : "json",
			success : function(result) {
				if (true == result['status']) {
					$('#element').load('/ui/sidebar_playlist' + '?r=' + util.string_random(20));
				} else {
					base.ui.ui_message(result['message']);
				}
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				base.ui.ui_message(errorThrown);
			}
		});

		return false;
	});
	
	
	/*
	 * 'Convert basket to playlist'
	 * LEGACY FUNCTION, TEMPORARY REDIRECT TO OBP-LEGACY 
	 */
	$('div.playlist_holder .panel .convert a').live('click', function() {

		var header = $('div.header', $(this).closest('.playlist_holder'));
		var name = $('div.name input', header).val();
		
		// Sorry, ugly. But don't blame me... 
		var uri = base.vars.legacy_url + base.vars.username +"/preprod/add/basket/"+ encodeURIComponent(name) +"/";
		uri = uri.replace("%2F", encodeURIComponent("%2F"));
		window.location = uri;

		return false;
	});
	
};


























base.ui.iface = function() {
	// expandables
	$('.expandable .header').live('click', function() {
		
		var parent = $(this).parent()
		var open = parent.hasClass('open');
		var type = parent.attr('class').split(" ");
		type = type[0];
		
		if (open) {
			parent.removeClass('open');
			parent.addClass('close');
			base.ui.save_state(type, 'close', false);
		} else {
			parent.removeClass('close');
			parent.addClass('open');
			base.ui.save_state(type, 'open', false);
		}
		
	});
	
}








