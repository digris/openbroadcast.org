// nunjucks main object
(function () {

    var templates = {};

    
    templates["shortcutter/nj/session_detail.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div>\n\t\n\t";
frame = frame.push();
var t_2 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"slots", env.autoesc);
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("slot", t_3);
frame.set("loop.last", t_1 === t_2.length - 1);
output += "\n\t<div class=\"holder slot\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.autoesc);
output += "px;\">\n\t\t<div class=\"header\"><h4>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"time", env.autoesc), env.autoesc);
output += "</h4></div>\n\t\t\n\t\t";
frame = frame.push();
var t_5 = runtime.memberLookup((t_3),"shots", env.autoesc);
if(t_5) {for(var t_4=0; t_4 < t_5.length; t_4++) {
var t_6 = t_5[t_4];
frame.set("shot", t_6);
frame.set("loop.last", t_4 === t_5.length - 1);
output += "\n\t\t\t<div class=\"holder shot\">\n\t\t\t\t<div class=\"box\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.autoesc);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.autoesc);
output += "px;\">\n\t\t\t\t";
if(runtime.memberLookup((t_6),"image", env.autoesc)) {
output += "\t\t\t\t\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_6),"image", env.autoesc), env.autoesc);
output += "\" width=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 10, env.autoesc);
output += "\"/>\n\t\t\t\t";
}
else {
output += "\n\t\t\t\t\t<img src=\"/static/shortcutter/img/shot_placeholder.png\" width=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 10, env.autoesc);
output += "\"/>\n\t\t\t\t";
}
output += "\n\t\t\t\t\n\t\t\t\t\t<span class=\"caption caption fade-caption\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 25, env.autoesc);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 25, env.autoesc);
output += "px;\">\n\t\t\t\t\t\t<h3>Caption</h3>\n\t\t\t\t\t\t<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</p>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<dl>\n\t\t\t\t\t\t\t<dt>Created</dt>\n\t\t\t\t\t\t\t<dd>";
output += runtime.suppressValue(runtime.memberLookup((t_6),"created", env.autoesc), env.autoesc);
output += "</dd>\n\t\t\t\t\t\t</dl>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<span class=\"datetime pull-right\"></span>\n\t\t\t\t\t</span>\n\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\n\t\t\t<div class=\"meta shot\">\n\t\t\t<p>";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_6),"user", env.autoesc)),"username", env.autoesc), env.autoesc);
output += "\n\t\t\t\t<span class=\"datetime pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((t_6),"created", env.autoesc), env.autoesc);
output += "</span>\n\t\t\t</p>\n\t\t\t</div>\n\t\t\t\n\t\t\t</div>\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.autoesc)) {
output += "\n\t\t\t<div style=\"clear: both;\"></div>\n\t\t\t";
}
output += "\n\t\t\t\n\t\t\t\n\t\t";
}
}frame = frame.pop();
output += "\n\t\t\n\t\t\n\t</div>\n\t";
}
}frame = frame.pop();
output += "\n\t\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["shortcutter/nj/session_detail_grid.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div>\n\t\n\t";
frame = frame.push();
var t_2 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"slots", env.autoesc);
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("slot", t_3);
frame.set("loop.last", t_1 === t_2.length - 1);
output += "\n\t<div class=\"holder slot\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.autoesc);
output += "px;\">\n\t\t<div class=\"header\"><h4>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"time", env.autoesc), env.autoesc);
output += "</h4></div>\n\t\t\n\t\t";
frame = frame.push();
var t_5 = runtime.memberLookup((t_3),"shots", env.autoesc);
if(t_5) {for(var t_4=0; t_4 < t_5.length; t_4++) {
var t_6 = t_5[t_4];
frame.set("shot", t_6);
frame.set("loop.last", t_4 === t_5.length - 1);
output += "\n\t\t\t<div class=\"holder shot loading\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_6),"uuid", env.autoesc), env.autoesc);
output += "\">\n\n\t\t\t<i class=\"icon-spinner icon-spin\"></i>\n\t\t\t\n\t\t\t</div>\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.autoesc)) {
output += "\n\t\t\t<div style=\"clear: both;\"></div>\n\t\t\t";
}
output += "\n\t\t\t\n\t\t\t\n\t\t";
}
}frame = frame.pop();
output += "\n\t\t\n\t\t\n\t</div>\n\t";
}
}frame = frame.pop();
output += "\n\t\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["shortcutter/nj/session_detail_shot.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"loader\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.autoesc);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.autoesc);
output += "px;\">\n\n\t<h1 class=\"indicator\"><i class=\"icon-spinner icon-spin\"></i></h1>\n\n</div>\n\n<div class=\"box\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.autoesc);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.autoesc);
output += "px;\">\n\n\t\n\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"image", env.autoesc)) {
output += "\n\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"image", env.autoesc), env.autoesc);
output += "\" width=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 10, env.autoesc);
output += "\"/>\n\t";
}
else {
output += "\n\t<img src=\"/static/shortcutter/img/shot_placeholder.png\" width=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 10, env.autoesc);
output += "\"/>\n\t";
}
output += "\n\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"status", env.autoesc) != 100) {
output += "\n\t<span class=\"caption caption fade-caption\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 25, env.autoesc);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 25, env.autoesc);
output += "px;\">\n\t\t<h3>";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"user", env.autoesc)),"username", env.autoesc), env.autoesc);
output += "</h3>\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"description", env.autoesc)) {
output += "\n\t\t<blockquote>\n\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"description", env.autoesc), env.autoesc);
output += "\n\t\t</blockquote>\n\t\t";
}
output += "\n\t\t<dl>\n\t\t\t<dt>\n\t\t\t\tShot taken:\n\t\t\t</dt>\n\t\t\t<dd>\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"updated", env.autoesc), env.autoesc);
output += "\n\t\t\t</dd>\n\t\t\t<dt>\n\t\t\t\turi: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"resource_uri", env.autoesc), env.autoesc);
output += "\n\t\t\t</dt>\n\t\t\t<dd>\n\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"pos", env.autoesc)),"lat", env.autoesc)) {
output += "\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"pos", env.autoesc)),"lat", env.autoesc), env.autoesc);
output += "\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"pos", env.autoesc)),"lng", env.autoesc), env.autoesc);
output += "\n\t\t\t\t";
}
output += "\n\t\t\t</dd>\n\t\t</dl>\n\t\t<span class=\"datetime pull-right\"></span>\n\t\t\n\t</span>\n\t";
}
output += "\n\t\n\t\n\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["istats/nj/server.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<h2><i class=\"icon-tasks\"></i> Files in Queue</h2>\n\n";
frame = frame.push();
var t_2 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
output += "\n\n\n<div class=\"row-fluid \">\n    <div span12>\n        <h6>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"display", env.autoesc), env.autoesc);
output += "</h6>\n    </div>\n</div>\n<div class=\"row-fluid \">\n    <div class=\"span3\">\n        <span class=\"num-files\">";
output += runtime.suppressValue(runtime.memberLookup((t_3),"queue", env.autoesc), env.autoesc);
output += "</span> files\n    </div>\n    <div class=\"span9\">\n        time: ~<span class=\"time-wait\">";
output += runtime.suppressValue(runtime.memberLookup((t_3),"estimate", env.autoesc), env.autoesc);
output += "</span> Minutes\n    </div>\n</div>\n\n";
}
}frame = frame.pop();
output += "\n\n\n\n";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["alibrary/nj/merge/merge_dialog.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "\n\n\n<div class=\"info\">\n\n<strong>Kjhaksdhaksdh</strong>\n<p>asldkjhakjshdksjhdkjh</p>\n\n</div>\n\n\n<div class=\"listing\" style=\"max-height: 400px; overflow: auto; width: 700px;\">\n\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "objects")),"length", env.autoesc) < 1) {
output += "\n\n        <p>\n            Sorry - but we could not find any objects to merge.\n        </p>\n    ";
}
output += "\n\n    ";
frame = frame.push();
var t_2 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("object", t_3);
output += "\n\n        <div class=\"item object \" data-uri=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"uri", env.autoesc), env.autoesc);
output += "\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"id", env.autoesc), env.autoesc);
output += "\">\n\n            <div class=\"row-fluid\">\n\n                <div class=\"span2\">\n                    ";
if(runtime.memberLookup((t_3),"main_image", env.autoesc)) {
output += "\n                        <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"main_image", env.autoesc), env.autoesc);
output += "\">\n                    ";
}
else {
output += "\n                        <img src=\"/static/img/base/spacer.png\">\n                    ";
}
output += "\n                </div>\n\n                <div class=\"span10\">\n                    <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"name", env.autoesc), env.autoesc);
output += "<small class=\"pull-right\"> ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"media", env.autoesc)),"length", env.autoesc), env.autoesc);
output += " Tracks</small></strong>\n                    <ul class=\"unstyled\">\n\n                        <li>\n\n                            <span class=\"value\">\n                                <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"releasedate", env.autoesc), env.autoesc);
output += " | ";
output += runtime.suppressValue(runtime.memberLookup((t_3),"release_country", env.autoesc), env.autoesc);
output += "</strong>\n\n                            </span>\n                        </li>\n\n                        <li>\n                            <span class=\"title\">\n                                Artist:\n                            </span>\n                            <span class=\"value\">\n                                ";
frame = frame.push();
var t_5 = runtime.memberLookup((t_3),"artist", env.autoesc);
if(t_5) {for(var t_4=0; t_4 < t_5.length; t_4++) {
var t_6 = t_5[t_4];
frame.set("artist", t_6);
output += "\n                                    <strong>";
output += runtime.suppressValue(t_6, env.autoesc);
output += "</strong>\n                                ";
}
}frame = frame.pop();
output += "\n                            </span>\n                        </li>\n\n\n                        <li>\n                            <span class=\"title\">\n                                Catalog #:\n                            </span>\n                            <span class=\"value\">\n                                <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"catalognumber", env.autoesc), env.autoesc);
output += "</strong>\n                            </span>\n                        </li>\n\n\n\n                    </ul>\n                </div>\n\n            </div>\n\n\n        </div>\n\n\n\n    ";
}
}frame = frame.pop();
output += "\n</div>\n\n\n<div class=\"action\">\n\n    <form class=\"form-horizontal\">\n\n\n\n        <a class=\"pull-right confirm btn btn-primary\" data-action=\"confirm\" type=\"button\">Confirm</a>\n        <a class=\"pull-right confirm btn\" data-action=\"cancel\" type=\"button\">Cancel</a>\n\n    </form>\n\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["alibrary/nj/playlist/editor_item.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"list_body_row item hoverable editable ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += " ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_type", env.autoesc), env.autoesc);
output += "\" data-updated=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"updated", env.autoesc), env.autoesc);
output += "\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri", env.autoesc), env.autoesc);
output += "\" data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += "\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\" id=\"playlist_item_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\">\n\n\t<div class=\"row-fluid base\">\n\t\t\n\t\t<div class=\"span1 actions\">\n\n\t\t\t<ul class=\"unstyled\">\n\t\t\t\t<li>\n\t\t\t\t\t<a href=\"#\" data-action=\"stop\" class=\"visible-while-playing\">\n\t\t\t\t\t\t<i class=\" icon-stop icon-large\"></i>\n\t\t\t\t\t</a>\n\t\t\t\t\t<a href=\"#\" data-action=\"play\" class=\"hidden-while-playing\">\n\t\t\t\t\t\t<i class=\" icon-play icon-large\"></i>\n\t\t\t\t\t</a>\n\t\t\t\t\t<a href=\"#\" data-action=\"pause\" class=\"\">\n\t\t\t\t\t\t<i class=\" icon-pause icon-large\"></i>\n\t\t\t\t\t</a>\n\t\t\t\t</li>\n\t\t\t</ul>\n\t\t\t\n\t\t\t<span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"duration", env.autoesc)), env.autoesc);
output += "</span>\n\t\t</div>\n\t\t\n\t\t<div class=\"span3\">\n\t\t\t<ul class=\"unstyled\">\n\t\t\t\t<li class=\"bold\">\n\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t";
output += runtime.suppressValue(env.getFilter("shorten").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"name", env.autoesc),30), env.autoesc);
output += "\n\t\t\t\t\t</a>\n\t\t\t\t</li>\n\t\t\t\t<li class=\"small relations\">\n\t\t\t\t\t\n\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"artist", env.autoesc)) {
output += "\n\t\t\t\t\t<span>\n\t\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"artist", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"artist", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"artist", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\n\t\t\t\t\t\t</a>\n\t\t\t\t\t</span> |\n\t\t\t\t\t";
}
output += "\n\t\t\t\t\t\n\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"release", env.autoesc)) {
output += "\n\t\t\t\t\t<span>\n\t\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"release", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"release", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"release", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\n\t\t\t\t\t\t</a>\n\t\t\t\t\t</span> |\n\t\t\t\t\t";
}
output += "\n\t\t\t\t\t\n\t\t\t\t\t\n\n\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t</li>\n\t\t\t</ul>\n\t\t</div>\n\t\t\n\t\t<div class=\"span1 fade-cue\" style=\"width: 80px;\">\n\t\t\t<!--\n\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_object", env.autoesc)),"duration", env.autoesc), env.autoesc);
output += "\n\t\t\t-->\n\t\t\t<div class=\"row-fluid pull-right\">\n\n\t\t\t\t<div class=\"span11\" style=\"margin-left: 0\">\n\t\t\t\t\t<input class=\"fade_cross\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_cross", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t\t\t<span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_cross", env.autoesc)), env.autoesc);
output += "</span><a class=\"editor preview\" data-preview=\"fade_cross\" href=\"#\"><i class=\"icon-volume-up icon-small\"></i></a>\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\t\t</div>\n\t\t\n\t\t<div class=\"span3 fade-cue\">\n\t\t\t\n\t\t\t<div class=\"row-fluid pull-right\">\n\t\t\t\t\n\t\t\t\t<div class=\"span6\" style=\"margin-left: 0\">\n\t\t\t\t\t<input class=\"fade_in\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_in", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t\t\t<span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_in", env.autoesc)), env.autoesc);
output += "</span> <a class=\"editor preview\" data-preview=\"fade_in\" href=\"#\"><i class=\"icon-volume-up icon-small\"></i></a>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"span6\" style=\"margin-left: 0\">\n\t\t\t\t\t<input class=\"fade_out\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_out", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t\t\t<span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_out", env.autoesc)), env.autoesc);
output += "</span> <a class=\"editor preview\" data-preview=\"fade_out\" href=\"#\"><i class=\"icon-volume-up icon-small\"></i></a>\n\t\t\t\t</div>\n\t\t\t\t<!--\n\t\t\t\t<div class=\"span1\">\n\t\t\t\t\t<input class=\"fade_cross\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_cross", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t\t\t<span>00:00:000</span>\n\t\t\t\t</div>\n\t\t\t\t-->\n\t\t\t</div>\n\t\t\t\n\t\t</div>\n\t\t\n\t\t<div class=\"span3 fade-cue\">\n\t\t\t\n\t\t\t<div class=\"row-fluid pull-right\">\n\t\t\t\t\n\t\t\t\t<div class=\"span6\" style=\"margin-left: 0\">\n\t\t\t\t\t<input class=\"cue_in\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_in", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t\t\t<span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_in", env.autoesc)), env.autoesc);
output += "</span>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"span6\" style=\"margin-left: 0\">\n\t\t\t\t\t<input class=\"cue_out\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_out", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t\t\t<span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_out", env.autoesc)), env.autoesc);
output += "</span>\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\t\t</div>\n\t\t\n\t\t<div class=\"span1 actions\">\n\t\t\t\n\t\t\t<ul class=\"unstyled\">\n\t\t\t\t<li>\n\t\t\t\t\t<a href=\"#\" data-action=\"collect\" class=\" pull-right\">\n\t\t\t\t\t\t<i class=\"icon-plus icon-large\"></i>\n\t\t\t\t\t</a>\n\t\t\t\t\t<a href=\"#\" data-action=\"delete\" class=\" pull-right\">\n\t\t\t\t\t\t<i class=\"icon-trash icon-large\"></i>\n\t\t\t\t\t</a>\n\t\t\t\t</li>\n\t\t\t</ul>\n\t\t\t\n\t\t</div>\n\t\t\n\t</div>\n\t\n\t\n\t<div class=\"row-fluid playhead\">\n\t\t<div class=\"span12\">\n\t\t\t\t\t\t\n\t\t\t<div class=\"waveform\" id=\"playlist_item_waveform_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\"></div>\n\t\t\t\n\t\t</div>\n\t\t\n\t</div>\n\n\t\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["alibrary/nj/playlist/editor_transform_summary.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "\n\t\t<div class=\"summary item target-duration ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error", env.autoesc)) {
output += "warning";
}
else {
output += "success";
}
output += "\">\n\t\t\t<h4><i class=\"icon-check\"></i> Target Duration</h4>\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error", env.autoesc)) {
output += "\n\t\t\t<div class=\"row-fluid information\">\n\t\t\t\t<div class=\"span12\">\n\t\t\t\t\t<p>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error", env.autoesc), env.autoesc);
output += "</p>\n\t\t\t\t\t<dl class=\"dl-horizontal\">\n\t\t\t\t\t\t<dt>Target</dt>\n\t\t\t\t\t\t<dd>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"target", env.autoesc)), env.autoesc);
output += "</dd>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<dt>Total</dt>\n\t\t\t\t\t\t<dd>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"total", env.autoesc)), env.autoesc);
output += "</dd>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<dt>Difference</dt>\n\t\t\t\t\t\t<dd>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"difference", env.autoesc)), env.autoesc);
output += "</dd>\n\t\t\t\t\t</dl>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t";
}
output += "\n\t\t\t\n\t\t</div>\n\t\n\t\t\n\t\t<div class=\"summary item dayparts\">\n\t\t\t<h4><i class=\"icon-check\"></i>Broadcast Dayparts</h4>\n\t\t\t<div class=\"row-fluid information\">\n\t\t\t\t<div class=\"span12\">\n\t\t\t\t\t<p>Please specify the best Broadcast Dayparts</p>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["alibrary/nj/playlist/listing_inline.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "\n\n\t<div id=\"playlist_holder_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\" data-object_id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\" class=\"playlist_holder \" data-updated=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"updated", env.autoesc), env.autoesc);
output += "\">\n\n\t\t<div class=\"header\">\n\n\t\t\t<div class=\"right\">\n\t\t\t\t<a href=\"#\" title=\"Remove\" data-action=\"delete\" class=\"action delete\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Remove\"></a>\n\t\t\t</div>\n\n\t\t\t<div class=\"right\">\n\t\t\t\t<a href=\"#\" title=\"Edit name\" data-action=\"edit\" class=\"action edit\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Edit name\"></a>\n\t\t\t</div>\n\n\t\t\t<div class=\"right\">\n\t\t\t\t<a href=\"#playlist:393:mp3\" title=\"Download\" data-action=\"download\" class=\"action downloadable queue\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Edit name\"></a>\n\t\t\t</div>\n\n\t\t\t<div class=\"left name\">\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name", env.autoesc), env.autoesc);
output += "\n\t\t\t</div>\n\t\t\t<div class=\"clear\"></div>\n\t\t</div>\n\n\t\t<div class=\"panel\">\n\n\t\t\t<div class=\"edit\">\n\t\t\t\t<div class=\"hint\">\n\t\t\t\t\tEnter the new name for the basket\n\t\t\t\t</div>\n\t\t\t\t<div class=\"input\">\n\t\t\t\t\t<input type=\"text\" id=\"playlist_edit_name_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\" name=\"playlist_edit_name\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t</div>\n\t\t\t</div>\n\n\t\t\t<div class=\"convert\">\n\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"edit_url", env.autoesc), env.autoesc);
output += "\">Edit</a>\n\t\t\t\t<!--<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url", env.autoesc), env.autoesc);
output += "\">Detail</a>-->\n\t\t\t</div>\n\t\t\t<div class=\"duration\">\n\t\t\t\t";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"duration", env.autoesc)), env.autoesc);
output += "\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"target_duration", env.autoesc), env.autoesc);
output += "000\n\t\t\t</div>\n\t\t</div>\n\n\t\t<div class=\"list\">\n\t\t\t\n\n\t\t\t";
frame = frame.push();
var t_2 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"items", env.autoesc);
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
output += "\n\n\t\t\t\n\t\t\t\n\t\t\t<div class=\"sidebar list item source ct-";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"item", env.autoesc)),"content_type", env.autoesc), env.autoesc);
output += "\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"resource_uri", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t<div class=\"right\">\n\t\t\t\t\t<a href=\"#\" title=\"Remove\" data-action=\"delete\" class=\"action delete\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Remove\"></a>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"left\">\n\t\t\t\t\t<a href=\"#\" title=\"Play\" class=\"action play playable popup\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Play\"></a>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"left title\">\n\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((t_3),"item", env.autoesc)),"content_object", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((t_3),"item", env.autoesc)),"content_object", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((t_3),"item", env.autoesc)),"content_object", env.autoesc)),"name", env.autoesc),36), env.autoesc);
output += "</a>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"clear\"></div>\n\t\t\t</div>\n\t\t\t\n\t\t\t";
}
}frame = frame.pop();
output += "\n\t\t\t\n\t\t</div>\n\n\t</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["alibrary/nj/playlist/select_popup.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<section class=\"title\">\n    <h3>Playlists\n        <small class=\"pull-right\">...</small>\n    </h3>\n</section>\n\n<section class=\"search\">\n    <div class=\"\">\n\n        <input type=\"text\" class=\"search\" title=\"Search\" placeholder=\"Type to search\">\n    </div>\n\n</section>\n\n\n<section class=\"listing nano\" id=\"playlist_list\">\n    <div class=\"content\">\n\n        ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "data")),"objects", env.autoesc)),"length", env.autoesc) > 0) {
output += "\n\n        <p class=\"notice\">\n        You don't have any playlists yet.<br />\n        Use the \"Create a new list\" function below.\n        </p>\n        ";
}
output += "\n\n        ";
frame = frame.push();
var t_2 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "data")),"objects", env.autoesc);
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
output += "\n            ";
var includeTemplate = env.getTemplate("alibrary/nj/playlist/select_popup_item.html");
output += includeTemplate.render(context.getVariables(), frame.push());
output += "\n        ";
}
}frame = frame.pop();
output += "\n    </div>\n</section>\n\n<section class=\"form\">\n\n    <div class=\"btn-toolbar\">\n        <div class=\"btn-group\">\n            <input type=\"text\" class=\"name\" title=\"Name\" placeholder=\"Create a new list\" required>\n            <a data-action=\"cancel\" class=\"btn btn-mini\">Cancel</a>\n            <a data-action=\"save\" class=\"btn btn-primary btn-mini\">Save</a>\n        </div>\n    </div>\n\n\n</section>\n";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["alibrary/nj/playlist/select_popup_item.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"item hoverable playlist ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"uuid", env.autoesc), env.autoesc);
output += "\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id", env.autoesc), env.autoesc);
output += "\" data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"uuid", env.autoesc), env.autoesc);
output += "\" data-name=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name", env.autoesc), env.autoesc);
output += "\"\n     data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"resource_uri", env.autoesc), env.autoesc);
output += "\">\n\n    <div class=\"row-fluid\">\n\n        <div class=\"span2 image\">\n\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.autoesc)) {
output += "\n                <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.autoesc), env.autoesc);
output += "\"/>\n            ";
}
else {
output += "\n                <img src=\"/static/img/base/defaults/listview.playlist.xl.png\"/>\n            ";
}
output += "\n\n        </div>\n\n        <div class=\"span10 information\">\n\n            <ul class=\"unstyled\">\n\n                <li>\n\n                    <strong><a class=\"\" title=\"Click to visit detail page\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name", env.autoesc),30), env.autoesc);
output += "</a></strong>\n\n                    <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"item_count", env.autoesc), env.autoesc);
output += " tracks | ";
output += runtime.suppressValue(env.getFilter("s2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"duration", env.autoesc)), env.autoesc);
output += "</small>\n                </li>\n                <li>\n                    <!--\n                    <span class=\"number\">";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"updated", env.autoesc),"date"), env.autoesc);
output += "</span>\n                    -->\n                    <span title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.autoesc),30), env.autoesc);
output += "</span>\n\n\n                    <span class=\"collected pull-right\"></span>\n\n\n                    <!--<span>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"type", env.autoesc), env.autoesc);
output += "</span>-->\n                </li>\n            </ul>\n\n        </div>\n\n    </div>\n\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["alibrary/nj/provider/relation_inline.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<p>\n    <span class=\"relation";
if(runtime.contextOrFrameLookup(context, frame, "match")) {
output += " match";
}
if(runtime.contextOrFrameLookup(context, frame, "no_match")) {
output += " diff";
}
output += "\"\n         data-service=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"service", env.autoesc), env.autoesc);
output += "\"\n         data-url=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"url", env.autoesc), env.autoesc);
output += "\">\n         <span>\n             ";
if(runtime.contextOrFrameLookup(context, frame, "match")) {
output += "\n                <i class=\"icon-link\"></i>\n             ";
}
else {
output += "\n                 <i class=\"icon-chevron-sign-up\"></i>\n             ";
}
output += "\n\n             <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"url", env.autoesc), env.autoesc);
output += "\" class=\"skip-external\" target=\"_blank\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"url", env.autoesc), env.autoesc);
output += "</a></span>\n    </span>\n</p>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["alibrary/nj/provider/search_dialog.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"query\">\n\n    <form class=\"form-horizontal\">\n\n        <input class=\"query\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "query"), env.autoesc);
output += "\">\n\n        <a class=\"pull-right search btn btn-primary\" type=\"button\">Search</a>\n\n    </form>\n\n</div>\n\n\n<div class=\"results\" style=\"max-height: 400px; overflow: auto; width: 700px;\">\n\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "results")),"length", env.autoesc) < 1) {
output += "\n\n        <p>\n            Sorry - but we could not find any results.\n        </p>\n    ";
}
output += "\n\n    ";
frame = frame.push();
var t_2 = runtime.contextOrFrameLookup(context, frame, "results");
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("result", t_3);
output += "\n\n        <div class=\"item result\" data-uri=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"uri", env.autoesc), env.autoesc);
output += "\">\n\n            <div class=\"row-fluid\">\n\n                <div class=\"span2\">\n                    ";
if(runtime.memberLookup((t_3),"thumb", env.autoesc)) {
output += "\n                    <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"thumb", env.autoesc), env.autoesc);
output += "\">\n                    ";
}
output += "\n                </div>\n\n                <div class=\"span10\">\n                    <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"title", env.autoesc), env.autoesc);
output += "</strong>\n                    <ul class=\"unstyled\">\n\n                        <li>\n\n                            <span class=\"value\">\n                                <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"year", env.autoesc), env.autoesc);
output += " | ";
output += runtime.suppressValue(runtime.memberLookup((t_3),"country", env.autoesc), env.autoesc);
output += "</strong>\n                            </span>\n                        </li>\n\n                        <li>\n                            <span class=\"title\">\n                                Catalog #:\n                            </span>\n                            <span class=\"value\">\n                                <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"catno", env.autoesc), env.autoesc);
output += "</strong>\n                            </span>\n                        </li>\n\n                        <li>\n                            <span class=\"title\">\n                                Format:\n                            </span>\n                            <span class=\"value\">\n                                <strong>\n                                    ";
frame = frame.push();
var t_5 = runtime.memberLookup((t_3),"format", env.autoesc);
if(t_5) {for(var t_4=0; t_4 < t_5.length; t_4++) {
var t_6 = t_5[t_4];
frame.set("k", t_6);
output += "\n                                        ";
output += runtime.suppressValue(t_6, env.autoesc);
output += " |\n                                    ";
}
}frame = frame.pop();
output += "\n                                </strong>\n                            </span>\n                        </li>\n\n                    </ul>\n                </div>\n\n            </div>\n\n\n        </div>\n\n\n\n    ";
}
}frame = frame.pop();
output += "\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["alibrary/nj/release/autocomplete.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"result\">\n\t<div class=\"search\">\n\t\t<h1>Search [Hit \"Enter\"]</h1>\n\t\t<p>\n\t\t\tSearch Library for: \"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query", env.autoesc), env.autoesc);
output += "\"\n\t\t\t\n\t\t</p>\n\t</div>\n\t<div class=\"listing\">\n\t\t";
frame = frame.push();
var t_2 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
frame.set("loop.last", t_1 === t_2.length - 1);
output += "\n\n\t\t<div class=\"item linkable hoverable\">\n\t\t\t\n\t\t\t<div class=\"row-fluid\">\n\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"main_image", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t\t</div>\n\n\t\t\t\t<div class=\"span10\">\n\t\t\t\t\t\n\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"get_absolute_url", env.autoesc), env.autoesc);
output += "\" class=\"link-main\"><h2>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_3),"name", env.autoesc),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query", env.autoesc)), env.autoesc);
output += "</h2></a>\n\t\t\t\t\t\n\n\n\t\t\t\t\t<div class=\"related\">\n\t\t\t\t\t\t";
if(env.getFilter("length").call(context, runtime.memberLookup((t_3),"media", env.autoesc)) > 0) {
output += " <span>Tracks:</span>\n\t\t\t\t\t\t<ul class=\"horizontal\">\n\t\t\t\t\t\t\t";
frame = frame.push();
var t_5 = runtime.memberLookup((t_3),"media", env.autoesc);
if(t_5) {for(var t_4=0; t_4 < t_5.length; t_4++) {
var t_6 = t_5[t_4];
frame.set("media", t_6);
frame.set("loop.last", t_4 === t_5.length - 1);
output += "\n\t\t\t\t\t\t\t<li>\n\t\t\t\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((t_6),"get_absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_6),"name", env.autoesc),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query", env.autoesc)), env.autoesc);
output += " | ";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_6),"artist", env.autoesc),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query", env.autoesc)), env.autoesc);
output += "</a>\n\t\t\t\t\t\t\t\t";
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.autoesc)) {
output += ",";
}
output += "\n\t\t\t\t\t\t\t</li>\n\t\t\t\t\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.autoesc)) {
output += "\n\t\t\t\t\t\t\t\t<div class=\"clear\"></div>\n\t\t\t\t\t\t\t";
}
output += "\n\t\t\t\t\t\t\t";
}
}frame = frame.pop();
output += "\n\t\t\t\t\t\t</ul>\n\t\t\t\t\t\t";
}
output += "\n\t\t\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\n\n\t\t</div>\n\t\t";
}
}frame = frame.pop();
output += "\n\t</div>\n</div>\n";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["aplayer/nj/detail_player.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"list_body_row item hoverable media ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += " ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.autoesc)),"content_type", env.autoesc), env.autoesc);
output += "\"\n     data-updated=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"updated", env.autoesc), env.autoesc);
output += "\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri", env.autoesc), env.autoesc);
output += "\" data-ct=\"media\" data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += "\"\n     data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\" id=\"playlist_item_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\">\n\n\n    <div class=\"row-fluid playhead\">\n        <div class=\"span12\">\n\n            <div class=\"overlay primary\">\n                <ul class=\"unstyled action\">\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "perms")),"play", env.autoesc)) {
output += "\n                    <li class=\"square\">\n                        <a href=\"#\"\n                           class=\"playable popup\"\n                           data-ct=\"media\"\n                           data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri", env.autoesc), env.autoesc);
output += "\"\n                           data-offset=\"0\"\n                           data-mode=\"replace\"\n                           title=\"Play\">\n                            <i class=\"icon icon-play\"></i>\n                        </a>\n                    </li>\n                    ";
}
output += "\n\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "perms")),"play", env.autoesc)) {
output += "\n                    <li class=\"square\">\n                        <a href=\"#\"\n                           class=\"playable popup\"\n                           data-ct=\"media\"\n                           data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri", env.autoesc), env.autoesc);
output += "\"\n                           data-offset=\"0\"\n                           data-mode=\"queue\"\n                           title=\"Queue\">\n                            <i class=\"icon icon-reorder\"></i></a>\n\n                    </li>\n                    ";
}
output += "\n\n                </ul>\n            </div>\n\n            <div class=\"overlay secondary\">\n                <ul class=\"unstyled action\">\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "perms")),"add", env.autoesc)) {
output += "\n\n                    <li>\n                        <a href=\"#\"\n                           class=\"\"\n                           data-action=\"collect\"\n                           title=\"Add to playlist\">\n                            <i class=\"icon icon-plus\"></i>\n                        </a>\n                    </li>\n                    ";
}
output += "\n\n                </ul>\n            </div>\n\n\n            <div class=\"waveform\" id=\"detail_player_waveform_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\"></div>\n\n        </div>\n\n    </div>\n\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["aplayer/nj/inline_player_item.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"item playlist media object ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += " hoverable\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += "\"\n     id=\"playlist_item_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\"\n     data-item_id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\"\n     data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\"\n     data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += "\">\n\n    <div class=\"wrapper\">\n\n        <div class=\"row-fluid\">\n            <div class=\"span10 information\">\n                <span class=\"title\">\n                    <a class=\"\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name", env.autoesc), env.autoesc);
output += "</a>\n                </span>\n                <span><a class=\"\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "</a> |\n                <a class=\"\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "</a></span>\n            </div>\n            <div class=\"span2 duration\">\n                <span>\n                ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"formated_duration", env.autoesc), env.autoesc);
output += "\n                <a class=\"\" data-action=\"collect\" href=\"#\"><i class=\"icon-plus icon-large\"></i></a>\n                </span>\n\n\n            </div>\n        </div>\n\n    </div>\n\n\n    <div class=\"indicator\" style=\"width: 100% !important\">\n        <div class=\"wrapper\">\n            <div class=\"inner\">&nbsp;</div>\n        </div>\n    </div>\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["importer/nj/autocomplete.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"result\">\n\n\t<div class=\"listing\">\n\t\t";
frame = frame.push();
var t_2 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
frame.set("loop.last", t_1 === t_2.length - 1);
output += "\n\t\t<div class=\"item hoverable\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"id", env.autoesc), env.autoesc);
output += "\" data-name=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"name", env.autoesc), env.autoesc);
output += "\" data-ct=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"ct", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\n\t\t\t<div class=\"row-fluid\">\n\t\t\t\t\n\t\t\t\t<div class=\"span3\">\n\t\t\t\t\t\n\t\t\t\t\t";
if(runtime.memberLookup((t_3),"main_image", env.autoesc)) {
output += "\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"main_image", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t\t\t";
}
else {
output += "\n\t\t\t\t\t<img src=\"/static/img/base/defaults/listview.";
output += runtime.suppressValue(runtime.memberLookup((t_3),"ct", env.autoesc), env.autoesc);
output += ".xl.png\" width=\"90\" height=\"90\" />\n\t\t\t\t\t";
}
output += "\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span9\">\n\t\t\t\t\t\n\t\t\t\t\t<ul class=\"unstyled\">\n\t\t\t\t\t\t<li><strong>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_3),"name", env.autoesc),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query", env.autoesc)), env.autoesc);
output += "</strong>  <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((t_3),"releasedate", env.autoesc), env.autoesc);
output += "</small></li>\n\t\t\t\t\t\t\n\t\t\t\t\t\t";
if(runtime.memberLookup((t_3),"ct", env.autoesc) == "release") {
output += "\n\t\t\t\t\t\t<li>";
frame = frame.push();
var t_5 = runtime.memberLookup((t_3),"artist", env.autoesc);
if(t_5) {for(var t_4=0; t_4 < t_5.length; t_4++) {
var t_6 = t_5[t_4];
frame.set("artist", t_6);
frame.set("loop.last", t_4 === t_5.length - 1);
output += runtime.suppressValue(t_6, env.autoesc);
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.autoesc)) {
output += ", ";
}
}
}frame = frame.pop();
output += "</li>\n\t\t\t\t\t\t<li>Tracks: ";
output += runtime.suppressValue(runtime.memberLookup((t_3),"media_count", env.autoesc), env.autoesc);
output += "</li>\n\t\t\t\t\t\t";
}
output += "\n\t\t\t\t\t\t\n\t\t\t\t\t</ul>\n\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\n\t\t</div>\n\t\t";
}
}frame = frame.pop();
output += "\n\t</div>\n</div>\n";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["importer/nj/importfile.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += "\" class=\"importfile item ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc), env.autoesc);
output += "\">\n\n\t<h3>\n\t\t<!--\n\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "\n\t\t-->\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "init") {
output += "\n\t\t<i class=\"icon-time\"></i>\n\t\t";
}
output += "\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "done") {
output += "\n\t\t<i class=\"icon-ok-sign\"></i>\n\t\t";
}
output += "\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "ready") {
output += "\n\t\t<i class=\"icon-thumbs-up\"></i>\n\t\t";
}
output += "\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "working") {
output += "\n\t\t<i class=\"icon-spinner icon-spin\"></i>\n\t\t";
}
output += "\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "warning") {
output += "\n\t\t<i class=\"icon-thumbs-down\"></i>\n\t\t";
}
output += "\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "duplicate") {
output += "\n\t\t<i class=\"icon-copy\"></i>\n\t\t";
}
output += "\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "queued") {
output += "\n\t\t<i class=\"icon-spinner icon-spin\"></i>\n\t\t";
}
output += "\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "importing") {
output += "\n\t\t<i class=\"icon-asterisk icon-spin\"></i>\n\t\t";
}
output += "\n\t\t\n\t\t\n\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"filename", env.autoesc), env.autoesc);
output += " <small>[";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"mimetype", env.autoesc), env.autoesc);
output += "] ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc), env.autoesc);
output += "</small>\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "duplicate") {
output += "<span class=\"warning pull-right\">Duplicate</span>";
}
output += "\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"error", env.autoesc)) {
output += "<span class=\"warning pull-right\">Error: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"error", env.autoesc), env.autoesc);
output += "</span>";
}
output += "\n\t\t\n\t</h3>\n\t\n\t\n\t\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "queued") {
output += "\n\t<div class=\"row-fluid status status-queue\">\n\t\t\n\t\t<div class=\"span1 icon-holder\">&nbsp;</div>\n\n\t\t<div class=\"span8 information\">\n\n\t\t\t<!--<h4>Importing <i class=\"icon icon-padded icon-cogs\"></i></h4>-->\n\t\t\t<p>File placed in the import-queue.<br />Please be patient for a while.</p>\n\t\t\t<p>Depending on server-load and available metadata it can take several minutes per track to complete it's information.</p>\n\t\t\t\n\t\t</div>\n\t\t\n\t\t<div class=\"span3 image\">\n\t\t\t<div class=\"pull-right\">\n\t\t\t\t<i class=\"ajax-loader c3CA3B9\"></i>\n\t\t\t</div>\n\t\t</div>\n\t\t\n\t\t\n\t</div>\n\t";
}
output += "\n\n\n\n\n\t\n\t\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "duplicate") {
output += "\n\t<div class=\"row-fluid result-set status-duplicate\">\n\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)) {
output += "\n\t\t<div class=\"span1\">\n\t\t\t<i class=\"icon icon-padded icon-obp\"></i>\n\t\t</div>\n\t\t\n\t\t<div class=\"span8 information\">\n\t\t\t\n\t\t\t<ul class=\"unstyled\">\n\t\t\t\t<li><strong><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "</a>";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"artist", env.autoesc)),"name", env.autoesc)) {
output += " by <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"artist", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"artist", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "</a>";
}
output += "</strong></li>\n\n\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"name", env.autoesc)) {
output += "\n\t\t\t\t<li><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "</a></li>\n\t\t\t\t";
}
else {
output += "\n\t\t\t\t<li>No Release</li>\n\t\t\t\t";
}
output += "\n\t\t\t\t\n\t\t\t\t<li class=\"small\">";
output += runtime.suppressValue(env.getFilter("format_timestamp").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"created", env.autoesc)), env.autoesc);
output += "</li>\n\n\t\t\t</ul>\n\t\t\t\n\t\t</div>\n\t\t\n\t\t<div class=\"span3 image\">\n\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc) && runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"main_image", env.autoesc)) {
output += "\n\t\t\t<img class=\"pull-right\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"main_image", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t";
}
else {
output += "\n\t\t\t<img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\" />\n\t\t\t";
}
output += "\n\t\t</div>\n\t\t";
}
output += "\n\t\t\n\t</div>\n\t";
}
output += "\n\t\n\t\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "done") {
output += "\n\t<div class=\"row-fluid result-set status-done\">\n\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)) {
output += "\n\t\t<div class=\"span1\">\n\t\t\t<i class=\"icon icon-padded icon-obp\"></i>\n\t\t</div>\n\t\t\n\t\t<div class=\"span8 information\">\n\t\t\t\n\t\t\t<ul class=\"unstyled\">\n\t\t\t\t<li><strong><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "</a>";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"artist", env.autoesc)),"name", env.autoesc)) {
output += " by <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"artist", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"artist", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "</a>";
}
output += "</strong></li>\n\n\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"name", env.autoesc)) {
output += "\n\t\t\t\t<li><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"name", env.autoesc),50), env.autoesc);
output += "</a></li>\n\t\t\t\t";
}
else {
output += "\n\t\t\t\t<li>No Release</li>\n\t\t\t\t";
}
output += "\n\n\t\t\t\t<li class=\"small\">";
output += runtime.suppressValue(env.getFilter("format_timestamp").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"created", env.autoesc)), env.autoesc);
output += "</li>\n\t\t\t\t\n\t\t\t</ul>\n\t\t\t\n\t\t</div>\n\t\t\n\t\t<div class=\"span3 image\">\n\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc) && runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"main_image", env.autoesc)) {
output += "\n\t\t\t<img class=\"pull-right\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media", env.autoesc)),"release", env.autoesc)),"main_image", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t";
}
else {
output += "\n\t\t\t<img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\" />\n\t\t\t";
}
output += "\n\t\t</div>\n\t\t";
}
output += "\n\t\t\n\t</div>\n\t";
}
output += "\n\t\n\t\n\n\n\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "warning") {
output += "\n\t<div class=\"row-fluid result-set hoverable provider-tag\">\n\n\t\t<div class=\"span1\">\n\t\t\t<i class=\"icon icon-padded icon-id3\"></i>\n\t\t</div>\n\n\t\t<div class=\"span4\">\n\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">Title</li>\n\t\t\t\t\t<li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag", env.autoesc)),"media_name", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag", env.autoesc)),"media_name", env.autoesc),38), env.autoesc);
output += "</li>\n\t\t\t\t</ul>\n\t\t\t\t\n\t\t\t<div class=\"clearfix\"></div>\n\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">Release</li>\n\t\t\t\t\t<li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag", env.autoesc)),"release_name", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag", env.autoesc)),"release_name", env.autoesc),38), env.autoesc);
output += "</li>\n\t\t\t\t</ul>\n\n\t\t</div>\n\n\t\t<div class=\"span4\">\n\n\t\t\t<label class=\"checkbox holder-artist_name\">\n\t\t\t\t<input type=\"checkbox\">\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">\n\t\t\t\t\t\tArtist\n\t\t\t\t\t</li>\n\t\t\t\t\t<li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag", env.autoesc)),"artist_name", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag", env.autoesc)),"artist_name", env.autoesc),38), env.autoesc);
output += "</li>\n\t\t\t\t</ul> </label>\n\t\t\t<div class=\"clearfix\"></div>\n\n\t\t\t<label class=\"checkbox holder-label_name\">\n\t\t\t\t<input type=\"checkbox\">\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">\n\t\t\t\t\t\tLabel\n\t\t\t\t\t</li>\n\t\t\t\t\t<li class=\"value\"></li>\n\t\t\t\t</ul> </label>\n\n\t\t</div>\n\n\t\t<div class=\"span3\">\n\n\t\t\t<label class=\"checkbox holder-media_tracknumber\">\n\t\t\t\t<input type=\"checkbox\">\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">\n\t\t\t\t\t\tTrackNo\n\t\t\t\t\t</li>\n\t\t\t\t\t<li class=\"value\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag", env.autoesc)),"media_tracknumber", env.autoesc), env.autoesc);
output += "</li>\n\t\t\t\t</ul> </label>\n\t\t\t<div class=\"clearfix\"></div>\n\n\t\t\t<label class=\"checkbox holder-release_date\">\n\t\t\t\t<input type=\"checkbox\">\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">\n\t\t\t\t\t\tDate\n\t\t\t\t\t</li>\n\t\t\t\t\t<li class=\"value\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag", env.autoesc)),"release_date", env.autoesc), env.autoesc);
output += "</li>\n\t\t\t\t</ul> </label>\n\n\t\t</div>\n\n\t</div>\n\t";
}
output += "\n\n\n\n\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "warning") {
output += "\n\t<div class=\"musicbrainz-tag-holder\">\n\t\t\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz", env.autoesc)),"length", env.autoesc) < 1 && runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag", env.autoesc)),"media_tracknumber", env.autoesc)) {
output += "\n\t\t<!--\n\t\t<p>\n\t\t\t<strong>No results available.</strong> \n\t\t\tWould you like to try to <a class=\"rescan\" href=\"#\" data-settings=\"skip_tracknumber, another_setting\">lookup again witouth including the tracknumber</a>?\n\t\t</p>\n\t\t-->\n\t\t";
}
output += "\n\t\t\n\t\t";
frame = frame.push();
var t_2 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz", env.autoesc);
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
output += "\n\t\t\n\t\t<div class=\"row-fluid result-set hoverable musicbrainz-tag mb_id-";
output += runtime.suppressValue(runtime.memberLookup((t_3),"mb_id", env.autoesc), env.autoesc);
output += "\">\n\t\n\t\t\t<div class=\"span1\">\n\t\t\t\t<i class=\"icon icon-padded icon-musicbrainz\"></i>\n\t\t\t</div>\n\t\n\t\t\t<div class=\"span8\">\n\t\t\t\t\n\t\t\t\t\t<!-- ids -->\n\t\t\t\t\t<input type=\"hidden\" class=\"media-id\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"media", env.autoesc)),"mb_id", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t<input type=\"hidden\" class=\"release-id\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"mb_id", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t<input type=\"hidden\" class=\"artist-id\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"artist", env.autoesc)),"mb_id", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\n\t\t\t\t\t<!-- other data -->\n\t\t\t\t\t<input type=\"hidden\" class=\"releasedate\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"releasedate", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t<input type=\"hidden\" class=\"catalognumber\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"label", env.autoesc)),"catalognumber", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t<input type=\"hidden\" class=\"name\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"media", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t<input type=\"hidden\" class=\"artist\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"artist", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t<input type=\"hidden\" class=\"release\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"name", env.autoesc), env.autoesc);
output += "\">\n\t\n\t\t\t\t\t<h5>\n\t\t\t\t\t<a href=\"http://musicbrainz.org/recording/";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"media", env.autoesc)),"mb_id", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"media", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "</a>\n\t\t\t\t\tby\n\t\t\t\t\t<a href=\"http://musicbrainz.org/artist/";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"artist", env.autoesc)),"mb_id", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"artist", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "</a>\n\t\t\t\t\t</h5>\n\t\t\n\t\t\t\t\t<a class=\"external\" href=\"http://musicbrainz.org/release/";
output += runtime.suppressValue(runtime.memberLookup((t_3),"mb_id", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((t_3),"name", env.autoesc), env.autoesc);
output += "</a> \n\t\t\t\t\t<ul class=\"unstyled\">\n\t\t\t\t\t\t<li class=\"small\">";
output += runtime.suppressValue(runtime.memberLookup((t_3),"country", env.autoesc), env.autoesc);
output += " - ";
output += runtime.suppressValue(runtime.memberLookup((t_3),"releasedate", env.autoesc), env.autoesc);
output += "</li>\n\t\t\t\t\t\t<li class=\"small\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"label", env.autoesc)),"name", env.autoesc), env.autoesc);
output += " - ";
output += runtime.suppressValue(runtime.memberLookup((t_3),"catalognumber", env.autoesc), env.autoesc);
output += "</li>\n\t\t\t\t\t</ul>\n\t\n\t\t\t</div>\n\t\n\t\t\t<div class=\"span3\">\n\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((t_3),"relations", env.autoesc)),"discogs_image", env.autoesc)) {
output += "\n\t\t\t\t<img class=\"pull-right\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_3),"relations", env.autoesc)),"discogs_image", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t";
}
else {
output += "\n\t\t\t\t<img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\" />\n\t\t\t";
}
output += "\n\t\t\t</div>\n\t\t</div>\n\n\t\t\n\t\t";
}
}frame = frame.pop();
output += "\n\t\t\n\t\t\n\t</div>\n\t";
}
output += "\n\n\n\n\n\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "warning") {
output += "\n\t<div class=\"pull-righ result-actions\">\n\n\t\t<form class=\"form-horizontal form-result\">\n\t\t\t<h4>Result</h4>\n\n\t\t\t<!-- name -->\t\t\t\n\t\t\t<div class=\"row-fluid base media ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"name", env.autoesc)) {
output += "missing";
}
output += "\">\n\t\t\t\t\n\t\t\t\t<div class=\"span6\">\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Title <span class=\"required\">*</span></label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"release autoupdate\"  data-ct=\"media\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\n\t\t\t\t\n\t\t\t</div>\n\n\t\t\t<!-- release -->\t\t\t\n\t\t\t<div class=\"row-fluid base release ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"release", env.autoesc)) {
output += "missing";
}
output += "\">\n\t\t\t\t\n\t\t\t\t<div class=\"span5\">\n\t\t\t\t\t\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Release <span class=\"required\">*</span></label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"release autocomplete\" data-ct=\"release\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"release", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t\t<div class=\"ac-result\"></div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_release_id", env.autoesc) && !runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"force_release", env.autoesc)) {
output += "\n\t\t\t\t\t\t<a href=\"#\" data-ct=\"release\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_release_resource_uri", env.autoesc), env.autoesc);
output += "\"  class=\"tooltip-inline\">\n\t\t\t\t\t\t\t<i class=\"icon-paper-clip\"></i>\n\t\t\t\t\t\t\tAssigned\n\t\t\t\t\t\t</a>\n\t\t\t\t\t\t";
}
else {
output += "\n\t\t\t\t\t\t<span class=\"dim\"><i class=\"icon-plus\"></i> Create</span>\n\t\t\t\t\t\t";
}
output += "\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_release_id", env.autoesc)) {
output += "\n\t\t\t\t\t<input type=\"checkbox\" class=\"force-creation\" ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"force_release", env.autoesc)) {
output += "checked=\"checked\"";
}
output += "/>\n\t\t\t\t\tForce Creation <a class=\"tooltipable\" data-title=\"Enable this to force the creation of a new entry - even if there is already an item with the same name.\"><i class=\"icon-question-sign\"></i></a>\n\t\t\t\t\t";
}
else {
output += "\n\t\t\t\t\t&nbsp;\n\t\t\t\t\t";
}
output += "\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span3\">\n\t\t\t\t\t<a class=\"btn btn-mini pull-right apply-to-all\" data-ct=\"release\"><i class=\"icon-repeat\"></i> Apply Release to all</a>\n\t\t\t\t</div>\n\n\t\t\t\t\n\t\t\t</div>\n\n\t\t\t<!-- artist -->\t\t\t\n\t\t\t<div class=\"row-fluid base artist ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"artist", env.autoesc)) {
output += "missing";
}
output += "\">\n\t\t\t\t\n\t\t\t\t<div class=\"span5\">\n\t\t\t\t\t\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Artist <span class=\"required\">*</span></label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"artist autocomplete\" data-ct=\"artist\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"artist", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t\t<div class=\"ac-result\"></div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_artist_id", env.autoesc) && !runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"force_artist", env.autoesc)) {
output += "\n\t\t\t\t\t\t<a href=\"#\" data-ct=\"artist\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_artist_resource_uri", env.autoesc), env.autoesc);
output += "\"  class=\"tooltip-inline\">\n\t\t\t\t\t\t\t<i class=\"icon-paper-clip\"></i>\n\t\t\t\t\t\t\tAssigned\n\t\t\t\t\t\t</a>\n\t\t\t\t\t\t";
}
else {
output += "\n\t\t\t\t\t\t<span class=\"dim\"><i class=\"icon-plus\"></i> Create</span>\n\t\t\t\t\t\t";
}
output += "\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_artist_id", env.autoesc)) {
output += "\n\t\t\t\t\t<input type=\"checkbox\" class=\"force-creation\" ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"force_artist", env.autoesc)) {
output += "checked=\"checked\"";
}
output += "/>\n\t\t\t\t\tForce Creation <a class=\"tooltipable\" data-title=\"Enable this to force the creation of a new entry - even if there is already an item with the same name.\"><i class=\"icon-question-sign\"></i></a>\n\t\t\t\t\t";
}
else {
output += "\n\t\t\t\t\t&nbsp;\n\t\t\t\t\t";
}
output += "\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span3\">\n\t\t\t\t\t<a class=\"btn btn-mini pull-right apply-to-all\" data-ct=\"artist\"><i class=\"icon-repeat\"></i> Apply Artist to all</a>\n\t\t\t\t</div>\n\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t<!--\n\t\t\t<div class=\"row-fluid base\">\n\n\t\t\t\t<div class=\"span6\">\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Title</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"name\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"name", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Release</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"release\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"release", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_release_id", env.autoesc)) {
output += "\n\t\t\t\t\t\t\t\t<i class=\"icon-magic\"></i>\n\t\t\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_release_id", env.autoesc), env.autoesc);
output += "\n\t\t\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_release_resource_uri", env.autoesc), env.autoesc);
output += "\n\t\t\t\t\t\t\t";
}
output += "\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Release Date</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"releasedate\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"releasedate", env.autoesc), env.autoesc);
output += "\">\n\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\n\t\t\t\t<div class=\"span5\">\n\t\t\t\t\t\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputPassword\">Artist</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"artist\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"artist", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_artist_id", env.autoesc)) {
output += "\n\t\t\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"alibrary_artist_id", env.autoesc), env.autoesc);
output += "\n\t\t\t\t\t\t\t";
}
output += "\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Track Number</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"tracknumber\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"tracknumber", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Label</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" id=\"inputEmail\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"label", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\n\t\t\t</div>\n\t\t\t-->\n\n\t\t\t<div class=\"toggle\">\n\t\t\t\t<div class=\"row-fluid\">\n\t\t\t\t\t<div class=\"span12\">\n\t\t\t\t\t\t<a class=\"toggle-advanced pull-right\">More&nbsp;<i class=\"icon-angle-down\"></i></a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\t\t\t<div class=\"advanced-fields\">\n\t\t\t\t\n\t\t\t\t<h4>Musicbrainz IDs</h4>\n\n\t\t\t\t<div class=\"row-fluid musicbrainz\">\n\t\n\t\t\t\t\t<div class=\"span6\">\n\t\n\t\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Track ID</label>\n\t\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t\t<input type=\"text\" class=\"mb-track-id input-minitext\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"mb_track_id", env.autoesc), env.autoesc);
output += "\" readonly=\"readonly\">\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\n\t\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Artist ID</label>\n\t\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t\t<input type=\"text\" class=\"mb-artist-id input-minitext\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"mb_artist_id", env.autoesc), env.autoesc);
output += "\" readonly=\"readonly\">\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\n\t\t\t\t\t</div>\n\t\n\t\t\t\t\t<div class=\"span5\">\n\t\t\t\t\t\t\n\t\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t\t<label class=\"control-label\" for=\"inputPassword\">Release ID</label>\n\t\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t\t<input type=\"text\" class=\"mb-release-id input-minitext\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag", env.autoesc)),"mb_release_id", env.autoesc), env.autoesc);
output += "\" readonly=\"readonly\">\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\n\t\t\t\t\t</div>\n\t\n\t\t\t\t</div>\n\t\t\t\n\t\t\t\n\t\t\t</div>\n\n\t\t</form>\n\n\t</div>\n\n\t<div class=\"row-fluid pull-righ result-actions\">\n\n\t\t<div class=\"span8\">\n\t\t\t&nbsp;\n\t\t</div>\n\n\t\t<div class=\"pull-right span4\">\n\t\t\t<a class=\"btn btn-secondary btn-small delete-importfile\">Delete this File</a>\n\t\t\t<!--\n\t\t\t<a class=\"btn btn-secondary btn-small rescan\" data-settings=\"skip_tracknumber\">Scan witouth tracknumber</a>\n\t\t\t-->\n\t\t\t<a class=\"btn btn-secondary btn-small rescan\">Scan again</a>\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status", env.autoesc) == "warning") {
output += "\n\t\t\t<a class=\"btn btn-primary btn-small start-import\">Start Import</a>\n\t\t\t";
}
output += "\n\t\t</div>\n\t</div>\n\t\n\t\n\t";
}
output += "\n\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["importer/nj/popover.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"po-inline\">\n\t\n\t\n\n\n\t<div class=\"row-fluid\">\n\t\t\n\t\t<div class=\"span2\">\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.autoesc)) {
output += "\n\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t";
}
else {
output += "\n\t\t\t<img src=\"/static/img/base/defaults/listview.release.xl.png\" />\n\t\t\t";
}
output += "\n\t\t</div>\n\t\t\n\t\t<div class=\"span10\">\n\t\t\t\t<ul class=\"unstyled\">\n\t\t\t\t\t<li><strong>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name", env.autoesc), env.autoesc);
output += "</strong> <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasedate", env.autoesc), env.autoesc);
output += "</small></li>\n\t\t\t\t\t";
if(runtime.contextOrFrameLookup(context, frame, "artist")) {
output += "\n\t\t\t\t\t<li>";
frame = frame.push();
var t_2 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"artist", env.autoesc);
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("artist", t_3);
frame.set("loop.last", t_1 === t_2.length - 1);
output += runtime.suppressValue(t_3, env.autoesc);
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.autoesc)) {
output += ", ";
}
}
}frame = frame.pop();
output += "</li>\n\t\t\t\t\t";
}
output += "\n\t\t\t\t</ul>\n\t\t</div>\n\t\t\n\t</div>\n\t\n\n\t<div class=\"alert alert-info\">\n\t<p>Track will be added to this item. If this is not desired, please choose \"Force Creation\"</p>\n\t</div>\n\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["exporter/nj/export.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<tr class=\"item export ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status_display", env.autoesc), env.autoesc);
output += "\" data-last_status=\"0\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += "\">\n    <td>\n\n        <i class=\"icon-refresh icon-spin visible-while-init\"></i>\n        <i class=\"icon-download-alt visible-while-done\"></i>\n        <i class=\"icon-ok-sign visible-while-downloaded\"></i>\n        <i class=\"icon-refresh icon-spin visible-while-ready\"></i>\n        <i class=\"icon-tasks visible-while-progress\"></i>\n        <i class=\"icon-warning-sign icon-pulse visible-while-error\"></i>\n\n    </td>\n\n\n    <td>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"filename", env.autoesc), env.autoesc);
output += "</td>\n    <td>";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"created", env.autoesc),"datetime"), env.autoesc);
output += "</td>\n    <td>\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"downloaded", env.autoesc)) {
output += "\n            ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"downloaded", env.autoesc),"datetime"), env.autoesc);
output += "\n        ";
}
output += "\n    </td>\n\n    <td>\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"filesize", env.autoesc)) {
output += "\n            <div class=\"pull-right\">\n                ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"formatted_filesize", env.autoesc), env.autoesc);
output += "\n            </div>\n        ";
}
output += "\n    </td>\n    <td>\n        <a href=\"#\" data-action=\"download\"><i class=\"icon-download-alt\"></i> Download</a>\n\n    </td>\n    <td>\n\n\n        <div class=\"btn-group pull-right\">\n            <button class=\"btn btn-mini btn-prrimary\" data-toggle=\"dropdown\">\n                Actions\n            </button>\n            <button class=\"btn btn-mini  btn-prrimary dropdown-toggle\" data-toggle=\"dropdown\">\n                <span class=\"caret\"></span>\n            </button>\n            <ul class=\"dropdown-menu\">\n                <!--\n                <li>\n                    <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"get_absolute_url", env.autoesc), env.autoesc);
output += "\"><i class=\"icon-edit\"></i> Details</a>\n                </li>\n                -->\n                <li>\n                    <a href=\"#\" data-action=\"delete\"><i class=\"icon-trash\"></i>\n                        Delete</a>\n                </li>\n                <!--\n                <li class=\"divider\"></li>\n                <li>\n                    <a href=\"#\">Separated link</a>\n                </li>\n                -->\n            </ul>\n        </div>\n\n    </td>\n\n</tr>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["abcast/nj/autocomplete.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"result\">\n\n\t<div class=\"listing\">\n\t\t";
frame = frame.push();
var t_2 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
output += "\n\t\t<div class=\"item hoverable\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"id", env.autoesc), env.autoesc);
output += "\" data-name=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"name", env.autoesc), env.autoesc);
output += "\" data-ct=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"ct", env.autoesc), env.autoesc);
output += "\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"resource_uri", env.autoesc), env.autoesc);
output += "\">\n\t\t\t\n\t\t\t<div class=\"row-fluid\">\n\t\t\t\t\n\t\t\t\t<div class=\"span3\">\n\t\t\t\t\t\n\t\t\t\t\t";
if(runtime.memberLookup((t_3),"main_image", env.autoesc)) {
output += "\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_3),"main_image", env.autoesc), env.autoesc);
output += "\" />\n\t\t\t\t\t";
}
else {
output += "\n\t\t\t\t\t<img src=\"/static/img/base/defaults/listview.";
output += runtime.suppressValue(runtime.memberLookup((t_3),"ct", env.autoesc), env.autoesc);
output += ".xl.png\" width=\"90\" height=\"90\" />\n\t\t\t\t\t";
}
output += "\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span9\">\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t<!---->\n\t\t\t\t\t<ul class=\"unstyled\">\n\t\t\t\t\t\t\n\t\t\t\t\t\t<li><strong>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((t_3),"name", env.autoesc),30),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query", env.autoesc)), env.autoesc);
output += "</strong>  <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((t_3),"releasedate", env.autoesc), env.autoesc);
output += "</small></li>\n\t\t\t\t\t\t<li>\n\t\t\t\t\t\t\t<span>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"user", env.autoesc), env.autoesc);
output += "</span>\n\t\t\t\t\t\t\t|\n\t\t\t\t\t\t\t<span>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"target_duration", env.autoesc) / 60, env.autoesc);
output += " min</span>\n\t\t\t\t\t\t</li>\n\t\t\t\t\t\t<li><span>";
output += runtime.suppressValue(env.getFilter("shorten").call(context, runtime.memberLookup((t_3),"tags", env.autoesc),30), env.autoesc);
output += "</span></li>\n\t\t\t\t\t\t<!--\n\t\t\t\t\t\t";
if(runtime.memberLookup((t_3),"ct", env.autoesc) == "playlist") {
output += "\n\t\t\t\t\t\t";
frame = frame.push();
var t_5 = runtime.memberLookup((t_3),"media", env.autoesc);
if(t_5) {for(var t_4=0; t_4 < t_5.length; t_4++) {
var t_6 = t_5[t_4];
frame.set("item", t_6);
output += "\n\t\t\t\t\t\t<li>\n\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((t_6),"name", env.autoesc), env.autoesc);
output += "\n\t\t\t\t\t\t</li>\n\t\t\t\t\t\t";
}
}frame = frame.pop();
output += "\n\t\t\t\t\t\t";
}
output += "\n\t\t\t\t\t\t-->\n\t\t\t\t\t</ul>\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\n\t\t</div>\n\t\t";
}
}frame = frame.pop();
output += "\n\t</div>\n</div>\n";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["abcast/nj/col_day.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["abcast/nj/emission.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div \n\tclass=\"chip fix ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"source", env.autoesc), env.autoesc);
output += " emission theme-";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color", env.autoesc), env.autoesc);
output += "\" \n\tdata-resource-uri=";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri", env.autoesc), env.autoesc);
output += "\n\tid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += "\" \n\tdata-tip=\"<strong><i class='icon-tasks'></i> ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"type", env.autoesc), env.autoesc);
output += "</strong><br>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"start", env.autoesc), env.autoesc);
output += " - ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"end", env.autoesc), env.autoesc);
output += "<br>by: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user", env.autoesc)),"username", env.autoesc), env.autoesc);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object", env.autoesc)),"description_html", env.autoesc), env.autoesc);
output += "\" \n\tstyle=\"top:";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "top"), env.autoesc);
output += "px;left:-1px;width:100%;\n\">\n\t\n\t<dl class=\"cbrd\" style=\"height:";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "height") - 4, env.autoesc);
output += "px;\">\n\t\t<dt style=\"\">\n\t\t\t\n\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri", env.autoesc), env.autoesc);
output += "\">\n\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name", env.autoesc), env.autoesc);
output += "\n\t\t\t</a>\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"playing", env.autoesc)) {
output += "\n\t\t\t<i class=\"icon-bullhorn pull-right\"></i>\n\t\t\t";
}
output += "\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"locked", env.autoesc)) {
output += "\n\t\t\t<i class=\"icon-lock pull-right\"></i>\n\t\t\t";
}
output += "\n\t\t</dt>\n\n\t</dl>\n\t\n</div>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["abcast/nj/emission_popup.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<section class=\"title\">\n\t<h3>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name", env.autoesc), env.autoesc);
output += " <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"type_display", env.autoesc), env.autoesc);
output += "</small></h3>\n\t<ul class=\"unstyled\">\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user", env.autoesc)) {
output += "\n\t\t<li>\n\t\t\t<i class=\"icon-user\"></i> ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user", env.autoesc)),"username", env.autoesc), env.autoesc);
output += "\n\t\t</li>\n\t\t";
}
output += "\n\t\t<li>\n\t\t\t<i class=\"icon-time\"></i> ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start", env.autoesc),"time"), env.autoesc);
output += " - ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_end", env.autoesc),"time"), env.autoesc);
output += " | ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start", env.autoesc),"date"), env.autoesc);
output += "\n\t\t</li>\n\t</ul>\n</section>\n\n<section class=\"description\">\n\n\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object", env.autoesc)),"description", env.autoesc), env.autoesc);
output += "\n\n\t<!--\n\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\" class=\"pull-left\">> Read more</a>\n\t-->\n\n\t<ul class=\"unstyled\">\n\t\t<li>\n\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url", env.autoesc), env.autoesc);
output += "\">&gt; Emission details</a>\n\t\t</li>\n\t\t<li>\n\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">&gt; Content details</a>\n\t\t</li>\n\t</ul>\n\n</section>\n\n<section class=\"form\">\n\n\t<fieldset>\n\t\t<label class=\"checkbox\">\n\t\t\t<input type=\"checkbox\" class=\"edit-lock\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"locked", env.autoesc) == 1) {
output += "checked=\"checked\"";
}
output += ">\n\t\t\tLock editing </label>\n\t</fieldset>\n\t\n\t\n\n\t\n\t<fieldset class=\"color\">\n\t\t<div class=\"controls\">\n\t\t\t\n\t\t\t<label class=\"radio  theme-0\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"0\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color", env.autoesc) == 0) {
output += "checked=\"checked\"";
}
output += ">\n\t\t\t</label>\n\t\t\t\n\t\t\t<label class=\"radio theme-1\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"1\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color", env.autoesc) == 1) {
output += "checked=\"checked\"";
}
output += ">\n\t\t\t</label>\n\t\t\t\n\t\t\t<label class=\"radio theme-2\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"2\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color", env.autoesc) == 2) {
output += "checked=\"checked\"";
}
output += ">\n\t\t\t</label>\n\t\t\t\n\t\t\t<label class=\"radio theme-3\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"3\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color", env.autoesc) == 3) {
output += "checked=\"checked\"";
}
output += ">\n\t\t\t</label>\n\t\t\t\n\t\t\t<label class=\"radio theme-4\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"4\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color", env.autoesc) == 4) {
output += "checked=\"checked\"";
}
output += ">\n\t\t\t</label>\n\n\t\t</div>\n\t</fieldset>\n\t\n\n\t<div class=\"btn-toolbar\">\n\t\t<div class=\"btn-group pull-right\">\n\n\t\t\t<a data-action=\"cancel\" class=\"btn btn-mini pull-right\">Cancel</a>\n\n\t\t\t";
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"locked", env.autoesc)) {
output += "\n\t\t\t<a data-action=\"delete\" class=\"btn btn-mini pull-right\">Delete</a>\n\t\t\t";
}
output += "\n\t\t\t<a data-action=\"save\" class=\"btn btn-primary btn-mini pull-right\">Save</a>\n\t\t</div>\n\t</div>\n\n</section>\n";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["abcast/nj/on_air_emission.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<ul class=\"unstyled\">\n\t<li><strong class=\"name\"><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name", env.autoesc),30), env.autoesc);
output += "</a></strong><small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"type_display", env.autoesc), env.autoesc);
output += "</small></li>\n\t<li><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user", env.autoesc)),"full_name", env.autoesc), env.autoesc);
output += "</a></li>\n\t<li>";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start", env.autoesc),"time"), env.autoesc);
output += " - ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_end", env.autoesc),"time"), env.autoesc);
output += "</li>\n</ul>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["abcast/nj/on_air_item.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"row-fluid\" style=\"display: none;\">\n\t<div class=\"span3\">\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release", env.autoesc)) {
output += "\n\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release", env.autoesc)),"main_image", env.autoesc), env.autoesc);
output += "\" width=\"54\">\n\t\t";
}
else {
output += "\n\t\t&nbsp;\n\t\t";
}
output += "\n\t\t\n\t</div>\n\t<div class=\"span9\">\n\n\t\t<ul class=\"unstyled\">\n\t\t\t<li>\n\t\t\t\t<span class=\"playing\">\n\t\t\t\t<i class=\"icon-headphones\"></i>\n\t\t\t\t</span>\n\t\t\t\t<strong class=\"name\"><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name", env.autoesc),30), env.autoesc);
output += "</a></strong>\n\t\t\t</li>\n\t\t\t<li>\n\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist", env.autoesc)),"name", env.autoesc),20), env.autoesc);
output += "</a>\t\n\t\t\t</li>\n\t\t\t<li>\n\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release", env.autoesc)),"absolute_url", env.autoesc), env.autoesc);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release", env.autoesc)),"name", env.autoesc),20), env.autoesc);
output += "</a>\n\t\t\t</li>\n\t\t</ul>\n\n\t</div>\n\n</div>\n\n";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["abcast/nj/selected_object.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<h4>Selected for scheduling</h4>\n<p>Drag and drop to a free slot</p>\n\n<div class=\"object-search\">\n    <input class=\"autocomplete\" data-ct=\"playlist\" type=\"text\" placeholder=\"Search broadcasts\">\n\n    <div class=\"ac-result\"></div>\n</div>\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc)) {
output += "\n    <div class=\"_container object-to-schedule\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += "\">\n        <span class=\"name\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name", env.autoesc), env.autoesc);
output += " <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"target_duration", env.autoesc) / 60, env.autoesc);
output += " min\n        </small></span>\n\n        <p class=\"tags\">";
output += runtime.suppressValue(env.getFilter("shorten").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"d_tags", env.autoesc),60), env.autoesc);
output += "</p>\n\n        <p>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"description", env.autoesc), env.autoesc);
output += "</p>\n\n\n        ";
frame = frame.push();
var t_2 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"broadcast_status_messages", env.autoesc);
if(t_2) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("message", t_3);
output += "\n        ";
output += runtime.suppressValue(t_3, env.autoesc);
output += "\n        ";
}
}frame = frame.pop();
output += "\n\n\n        <h1>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"duration", env.autoesc) / 60 / 1000, env.autoesc);
output += "</h1>\n\n    </div>\n";
}
output += "\n";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    
    templates["abcast/nj/top_week.html"] = (function () {
    function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<table class=\"wk-weektop wk-full-mode\" cellpadding=\"0\" cellspacing=\"0\">\n\t<tbody>\n\t\t<tr class=\"wk-daynames\">\n\t\t\t<td class=\"wk-tzlabel\" style=\"width:60px\" rowspan=\"3\"></td><th title=\"Sun 5/19\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22195 wk-daylink\">Sun 5/19</span>\n\t\t\t</div></th><th title=\"Mon 5/20\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22196 wk-daylink\">Mon 5/20</span>\n\t\t\t</div></th><th title=\"Tue 5/21\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22197 wk-daylink\">Tue 5/21</span>\n\t\t\t</div></th><th title=\"Wed 5/22\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22198 wk-daylink\">Wed 5/22</span>\n\t\t\t</div></th><th title=\"Thu 5/23\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22199 wk-daylink\">Thu 5/235</span>\n\t\t\t</div></th><th title=\"Fri 5/24\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname wk-today\">\n\t\t\t\t<span class=\"ca-cdp22200 wk-daylink\">Fri 5/24</span>\n\t\t\t</div></th><th title=\"Sat 5/25\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname wk-tomorrow\">\n\t\t\t\t<span class=\"ca-cdp22201 wk-daylink\">Sat 5/25</span>\n\t\t\t</div></th><th class=\"wk-dummyth\" rowspan=\"3\" style=\"width: 17px;\">&nbsp;</th>\n\t\t</tr>\n\t</tbody>\n</table>";
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};


    })();  // template container ();
    

    // register templates
    if (typeof nunjucks === "object") {
        nunjucks.env = new nunjucks.Environment([], null);
        nunjucks.env.registerPrecompiled(templates);
    }
    else {
        console.error("ERROR: You must load nunjucks before the precompiled templates");
    }

})();
