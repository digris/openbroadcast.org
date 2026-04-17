;
var PanelApp = function() {
    var self = this;
    this.container;
    this.expanded = false;
    this.current_panel = false;

    this.init = function() {
        this.bindings();
    };

    this.bindings = function() {
        self.container.on('click', 'a', function(e){
            e.preventDefault();
            var panel = $(this).data('toggle_panel');

            self.display(panel);

        });
    };

    this.display = function(panel) {

        self.current_panel = panel;

        if(!self.expanded) {
            self.expanded = true;
        } else {
            self.expanded = false;
        }

        if(self.expanded) {
            self.container.addClass('expanded');
            $('a[data-toggle_panel=' + self.current_panel + ']').parent().addClass('active');

        } else {
            self.container.removeClass('expanded');
            $('a[data-toggle_panel]').parent().removeClass('active');
        }


    };


};





$(function(){
    var site_panel = new PanelApp();
    site_panel.container = $('#site_panel_container');
    site_panel.init()
});