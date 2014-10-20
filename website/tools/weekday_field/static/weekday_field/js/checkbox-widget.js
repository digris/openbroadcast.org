
$ = django.jQuery;

$(function() {
  function changeHandler(evt) {
    var $target = $(evt.target);
    var targetValue = evt.target.value;
    var targetChecked = !!$target.attr('checked');
  
    var $others = $('[name=' + $target.attr('name') + ']');
    var $anyAll = $('[value="None"]');
  
    if (targetValue === 'None') {
      $others.attr('checked', true);
      $target.attr('disabled', true);
      return;
    }
  
    // Otherwise, whenever we deselect any, deselect the "All" item.
    if (!targetChecked) {
      $others.filter('[value="None"]').attr('checked', false);
    }
    if (targetValue.match(',')) {
      // This was a multiple box.
      $others.filter(function(i, el) {
        return targetValue.match(el.value);
      }).attr('checked', targetChecked);
    } else {
      // This was a single choice.
      if (!targetChecked) {
        // And it was a deselection.
        $others.filter(function(i, el) {
          return el.value.match(targetValue);
        }).attr('checked', false);
      } else {
        // Only check multiple ones if they all match.
        var value_ = $others.filter(function(i, el) {
          return !el.value.match(',');
        }).filter(':checked');
        var value = [];
      
        $.each(value_, function(i, el){
          value.push(el.value);
        });
        value = value.sort().join();
      
        $others.filter(function(i, el) {
          return value.match(el.value);
        }).attr('checked', true);
      }  
    }
  
    // If we deselected everything, select everything.
    if ($others.filter(':checked').length === 0) {
      $others.attr('checked', true);
    } else {
      // Now check for all to be selected.
      if ($others.filter(':not(:checked)').length === 1) {
        if ($others.filter(':not(:checked)')[0].value === 'None') {
          $others.attr('checked', true);
        }  
      }
    }
  
    $anyAll.attr('disabled', !!$anyAll.attr('checked'));
  }
  
  $('.advanced-weekday-field').click(changeHandler);
  
  // Now disable the All of it is selected.
  $('.advanced-weekday-field[value="None"]:checked').attr('disabled', true);
});