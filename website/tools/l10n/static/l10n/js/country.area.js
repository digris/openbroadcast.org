django.jQuery(function() {
    var $ = django.jQuery;
    var country_selector = "#id_" + L10N.country_field;
    var area_selector = "#id_" + L10N.area_field;
    var $country = $(country_selector).change(function() {
        var $states = $(area_selector).empty();
        $.get(L10N.ajaxUrls.country_areas, { "country_id": $(this).val() }, 
              function(data) {
                  areas = JSON.parse(data);
                  if(!L10N.area_field_required) {
                      $states.append('<option value="" selected="selected">---------</option>');
                  }
                  for(var i = 0 ; i < areas.length ; i++) {
                      var area = areas[i];
                      $states.append("<option value='"+area.id+"'>"+area.name+"</option>");
                  }
              });
    });
    if($country.val())
        $country.change();
});