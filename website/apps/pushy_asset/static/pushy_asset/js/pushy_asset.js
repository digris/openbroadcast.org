PushyAssetApp = function () {

    var self = this;

    this.socket_url;
    this.socket;
    this.debug = true;
    this.subscriptions = [];

    this.init = function () {

        pushy.subscribe('pushy_asset/refresh/', function () {
            self.refresh();
        });
    };

    this.refresh = function () {

        var q = '?reload=' + new Date().getTime();
        $('link[rel="stylesheet"]').each(function () {

            if(this.href.indexOf("wip.css") != -1) {
                this.href = this.href.replace(/\?.*|$/, q);
            } else {
                console.log(this.href)
                console.log('not refreshing, is external one.')
            }


        });

    };

}; 	