;
var NavigationUI = function() {
    var self = this;
    var container;

    this.init = function(container) {

        self.container = container;
        self.bindings();
    };

    this.bindings = function() {
        //self.container.fadeOut(2000);
        self.container.on('mouseover', '> li > a', function(){
            $(this).parents('li').addClass('hover');
            self.container.addClass('hover');
        }).on('mouseout', 'a', function(){
            $(this).parents('li').removeClass('hover');
            self.container.removeClass('hover');
        })

    };

};