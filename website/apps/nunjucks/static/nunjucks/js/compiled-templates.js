

(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["profiles/nj/profile/autocomplete.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"result\">\n\t<div class=\"search\">\n\t\t<h1>Search [Hit \"Enter\"]</h1>\n\t\t<p>\n\t\t\tSearch Network for: \"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query"), env.opts.autoescape);
output += "\"\n\t\t</p>\n        <a class=\"exit btn\">close <i class=\"icon icon-remove-sign\"></i></a>\n\t</div>\n\t<div class=\"listing\">\n\t\t";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n\t\t<div class=\"item linkable hoverable\">\n\t\t\t\n\t\t\t<div class=\"row-fluid\">\n\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"image"), env.opts.autoescape);
output += "\" />\n\t\t\t\t</div>\n\n\t\t\t\t<div class=\"span10\">\n\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"get_absolute_url"), env.opts.autoescape);
output += "\" class=\"link-main\"><h2>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"display_name"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</h2></a>\n                    <span><!--<i class=\"icon icon-user\"></i>-->";
output += runtime.suppressValue(runtime.memberLookup((t_4),"username"), env.opts.autoescape);
output += "</span><br />\n                    <span>";
if(runtime.memberLookup((t_4),"country")) {
output += runtime.suppressValue(runtime.memberLookup((t_4),"country"), env.opts.autoescape);
;
}
output += " ";
if(runtime.memberLookup((t_4),"city")) {
output += runtime.suppressValue(runtime.memberLookup((t_4),"city"), env.opts.autoescape);
;
}
output += "</span><br />\n                    <span>Member since ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((t_4),"created"),"date"), env.opts.autoescape);
output += "</span>\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\n\n\t\t</div>\n\t\t";
;
}
}
frame = frame.pop();
output += "\n\t</div>\n</div>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["shortcutter/nj/session_detail.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div>\n\t\n\t";
frame = frame.push();
var t_3 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"slots");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("slot", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\t<div class=\"holder slot\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.opts.autoescape);
output += "px;\">\n\t\t<div class=\"header\"><h4>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"time"), env.opts.autoescape);
output += "</h4></div>\n\t\t\n\t\t";
frame = frame.push();
var t_7 = runtime.memberLookup((t_4),"shots");
if(t_7) {var t_6 = t_7.length;
for(var t_5=0; t_5 < t_7.length; t_5++) {
var t_8 = t_7[t_5];
frame.set("shot", t_8);
frame.set("loop.index", t_5 + 1);
frame.set("loop.index0", t_5);
frame.set("loop.revindex", t_6 - t_5);
frame.set("loop.revindex0", t_6 - t_5 - 1);
frame.set("loop.first", t_5 === 0);
frame.set("loop.last", t_5 === t_6 - 1);
frame.set("loop.length", t_6);
output += "\n\t\t\t<div class=\"holder shot\">\n\t\t\t\t<div class=\"box\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.opts.autoescape);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.opts.autoescape);
output += "px;\">\n\t\t\t\t";
if(runtime.memberLookup((t_8),"image")) {
output += "\t\t\t\t\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_8),"image"), env.opts.autoescape);
output += "\" width=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 10, env.opts.autoescape);
output += "\"/>\n\t\t\t\t";
;
}
else {
output += "\n\t\t\t\t\t<img src=\"/static/shortcutter/img/shot_placeholder.png\" width=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 10, env.opts.autoescape);
output += "\"/>\n\t\t\t\t";
;
}
output += "\n\t\t\t\t\n\t\t\t\t\t<span class=\"caption caption fade-caption\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 25, env.opts.autoescape);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 25, env.opts.autoescape);
output += "px;\">\n\t\t\t\t\t\t<h3>Caption</h3>\n\t\t\t\t\t\t<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</p>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<dl>\n\t\t\t\t\t\t\t<dt>Created</dt>\n\t\t\t\t\t\t\t<dd>";
output += runtime.suppressValue(runtime.memberLookup((t_8),"created"), env.opts.autoescape);
output += "</dd>\n\t\t\t\t\t\t</dl>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<span class=\"datetime pull-right\"></span>\n\t\t\t\t\t</span>\n\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\n\t\t\t<div class=\"meta shot\">\n\t\t\t<p>";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_8),"user")),"username"), env.opts.autoescape);
output += "\n\t\t\t\t<span class=\"datetime pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((t_8),"created"), env.opts.autoescape);
output += "</span>\n\t\t\t</p>\n\t\t\t</div>\n\t\t\t\n\t\t\t</div>\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last")) {
output += "\n\t\t\t<div style=\"clear: both;\"></div>\n\t\t\t";
;
}
output += "\n\t\t\t\n\t\t\t\n\t\t";
;
}
}
frame = frame.pop();
output += "\n\t\t\n\t\t\n\t</div>\n\t";
;
}
}
frame = frame.pop();
output += "\n\t\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["shortcutter/nj/session_detail_grid.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div>\n\t\n\t";
frame = frame.push();
var t_3 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"slots");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("slot", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\t<div class=\"holder slot\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.opts.autoescape);
output += "px;\">\n\t\t<div class=\"header\"><h4>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"time"), env.opts.autoescape);
output += "</h4></div>\n\t\t\n\t\t";
frame = frame.push();
var t_7 = runtime.memberLookup((t_4),"shots");
if(t_7) {var t_6 = t_7.length;
for(var t_5=0; t_5 < t_7.length; t_5++) {
var t_8 = t_7[t_5];
frame.set("shot", t_8);
frame.set("loop.index", t_5 + 1);
frame.set("loop.index0", t_5);
frame.set("loop.revindex", t_6 - t_5);
frame.set("loop.revindex0", t_6 - t_5 - 1);
frame.set("loop.first", t_5 === 0);
frame.set("loop.last", t_5 === t_6 - 1);
frame.set("loop.length", t_6);
output += "\n\t\t\t<div class=\"holder shot loading\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_8),"uuid"), env.opts.autoescape);
output += "\">\n\n\t\t\t<i class=\"icon-spinner icon-spin\"></i>\n\t\t\t\n\t\t\t</div>\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last")) {
output += "\n\t\t\t<div style=\"clear: both;\"></div>\n\t\t\t";
;
}
output += "\n\t\t\t\n\t\t\t\n\t\t";
;
}
}
frame = frame.pop();
output += "\n\t\t\n\t\t\n\t</div>\n\t";
;
}
}
frame = frame.pop();
output += "\n\t\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["shortcutter/nj/session_detail_shot.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"loader\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.opts.autoescape);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.opts.autoescape);
output += "px;\">\n\n\t<h1 class=\"indicator\"><i class=\"icon-spinner icon-spin\"></i></h1>\n\n</div>\n\n<div class=\"box\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.opts.autoescape);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize"), env.opts.autoescape);
output += "px;\">\n\n\t\n\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"image")) {
output += "\n\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"image"), env.opts.autoescape);
output += "\" width=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 10, env.opts.autoescape);
output += "\"/>\n\t";
;
}
else {
output += "\n\t<img src=\"/static/shortcutter/img/shot_placeholder.png\" width=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 10, env.opts.autoescape);
output += "\"/>\n\t";
;
}
output += "\n\n\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"status") != 100) {
output += "\n\t<span class=\"caption caption fade-caption\" style=\"width: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 25, env.opts.autoescape);
output += "px; height: ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "shotSize") - 25, env.opts.autoescape);
output += "px;\">\n\t\t<h3>";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"user")),"username"), env.opts.autoescape);
output += "</h3>\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"description")) {
output += "\n\t\t<blockquote>\n\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"description"), env.opts.autoescape);
output += "\n\t\t</blockquote>\n\t\t";
;
}
output += "\n\t\t<dl>\n\t\t\t<dt>\n\t\t\t\tShot taken:\n\t\t\t</dt>\n\t\t\t<dd>\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"updated"), env.opts.autoescape);
output += "\n\t\t\t</dd>\n\t\t\t<dt>\n\t\t\t\turi: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"resource_uri"), env.opts.autoescape);
output += "\n\t\t\t</dt>\n\t\t\t<dd>\n\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"pos")),"lat")) {
output += "\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"pos")),"lat"), env.opts.autoescape);
output += "\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "shot")),"pos")),"lng"), env.opts.autoescape);
output += "\n\t\t\t\t";
;
}
output += "\n\t\t\t</dd>\n\t\t</dl>\n\t\t<span class=\"datetime pull-right\"></span>\n\t\t\n\t</span>\n\t";
;
}
output += "\n\t\n\t\n\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["istats/nj/server.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<h4><i class=\"icon-tasks\"></i> Files in Queue</h4>\n\n";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n\n<div class=\"row-fluid \">\n    <div span12>\n        <h6>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"display"), env.opts.autoescape);
output += "</h6>\n    </div>\n</div>\n<div class=\"row-fluid \">\n    <div class=\"span3\">\n        <span class=\"num-files\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"queue"), env.opts.autoescape);
output += "</span> files\n    </div>\n    <div class=\"span9\">\n        time: ~<span class=\"time-wait\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"estimate"), env.opts.autoescape);
output += "</span> Minutes\n    </div>\n</div>\n\n";
;
}
}
frame = frame.pop();
output += "\n\n\n\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/artist/autocomplete.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"result\">\n\t<div class=\"search\">\n\t\t<h1>Search [Hit \"Enter\"]</h1>\n\t\t<p>\n\t\t\tSearch Library for: \"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query"), env.opts.autoescape);
output += "\"\n\t\t</p>\n        <a class=\"exit btn\">close <i class=\"icon icon-remove-sign\"></i></a>\n\t</div>\n    <div class=\"listing\">\n        ";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n            <div class=\"item linkable hoverable\">\n\n                <div class=\"row-fluid\">\n\n                    <div class=\"span2\">\n                        <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\"/>\n                    </div>\n\n                    <div class=\"span10\">\n\n                        <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"get_absolute_url"), env.opts.autoescape);
output += "\" class=\"link-main\"><h2>\n                            ";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"name"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</h2></a>\n\n                        ";
if(runtime.memberLookup((t_4),"namevariations")) {
output += "\n                            <div class=\"related\">\n                                <ul class=\"unstyled horizontal\">\n                                    ";
frame = frame.push();
var t_7 = runtime.memberLookup((t_4),"namevariations");
if(t_7) {var t_6 = t_7.length;
for(var t_5=0; t_5 < t_7.length; t_5++) {
var t_8 = t_7[t_5];
frame.set("name", t_8);
frame.set("loop.index", t_5 + 1);
frame.set("loop.index0", t_5);
frame.set("loop.revindex", t_6 - t_5);
frame.set("loop.revindex0", t_6 - t_5 - 1);
frame.set("loop.first", t_5 === 0);
frame.set("loop.last", t_5 === t_6 - 1);
frame.set("loop.length", t_6);
output += "\n                                    <li>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, t_8,runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += ", </li>\n                                    ";
;
}
}
frame = frame.pop();
output += "\n                                </ul>\n                            </div>\n                        ";
;
}
output += "\n                    </div>\n\n                </div>\n\n            </div>\n        ";
;
}
}
frame = frame.pop();
output += "\n    </div>\n</div>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/label/autocomplete.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"result\">\n\t<div class=\"search\">\n\t\t<h1>Search [Hit \"Enter\"]</h1>\n\t\t<p>\n\t\t\tSearch Library for: \"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query"), env.opts.autoescape);
output += "\"\n\t\t</p>\n        <a class=\"exit btn\">close <i class=\"icon icon-remove-sign\"></i></a>\n\t</div>\n    <div class=\"listing\">\n        ";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n            <div class=\"item linkable hoverable\">\n\n                <div class=\"row-fluid\">\n\n                    <div class=\"span2\">\n                        <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\"/>\n                    </div>\n\n                    <div class=\"span10\">\n\n                        <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"get_absolute_url"), env.opts.autoescape);
output += "\" class=\"link-main\"><h2>\n                            ";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"name"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</h2></a>\n\n                    </div>\n\n                </div>\n\n            </div>\n        ";
;
}
}
frame = frame.pop();
output += "\n    </div>\n</div>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/media/autocomplete.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"result\">\n\t<div class=\"search\">\n\t\t<h1>Search [Hit \"Enter\"]</h1>\n\t\t<p>\n\t\t\tSearch Library for: \"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query"), env.opts.autoescape);
output += "\"\n\t\t</p>\n        <a class=\"exit btn\">close <i class=\"icon icon-remove-sign\"></i></a>\n\t</div>\n\t<div class=\"listing\">\n\t\t";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n\t\t<div class=\"item linkable hoverable\">\n\t\t\t\n\t\t\t<div class=\"row-fluid\">\n\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\" />\n\t\t\t\t</div>\n\n\t\t\t\t<div class=\"span10\">\n\t\t\t\t\t\n\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"get_absolute_url"), env.opts.autoescape);
output += "\" class=\"link-main\"><h2>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"name"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</h2></a>\n\t\t\t\t\t\n\n\n\t\t\t\t\t<div class=\"related\">\n\t\t\t\t\t\t<ul class=\"unstyled\">\n                            ";
if(runtime.memberLookup((t_4),"artist")) {
output += "\n                                <li>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"artist"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</li>\n                            ";
;
}
output += "\n                            ";
if(runtime.memberLookup((t_4),"release")) {
output += "\n                                <li>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"release"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</li>\n                            ";
;
}
output += "\n\t\t\t\t\t\t</ul>\n\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\n\n\t\t</div>\n\t\t";
;
}
}
frame = frame.pop();
output += "\n\t</div>\n</div>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/merge/merge_dialog.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"info\">\n\n    <a class=\"pull-right exit btn\" data-action=\"exit\">close <i class=\"icon icon-remove-sign\"></i></a>\n    <strong>Merge items</strong>\n    <p>(This can not be undone!)</p>\n\n</div>\n\n\n<div class=\"listing\" style=\"max-height: 400px; overflow: auto; width: 700px;\">\n\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "objects")),"length") < 1) {
output += "\n\n        <p>\n            Sorry - but we could not find any objects to merge.\n        </p>\n    ";
;
}
output += "\n\n    ";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("object", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n        <div class=\"item object ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "item_type"), env.opts.autoescape);
output += "\" data-uri=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"uri"), env.opts.autoescape);
output += "\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"id"), env.opts.autoescape);
output += "\">\n\n            <div class=\"row-fluid\">\n\n\n                <div class=\"span2\">\n                    ";
if(runtime.memberLookup((t_4),"main_image")) {
output += "\n                        <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\">\n                    ";
;
}
else {
output += "\n                        <!--<img src=\"/static/img/base/spacer.png\">-->\n                        <img src=\"/static/img/base/defaults/listview.release.xl.png\">\n                    ";
;
}
output += "\n                </div>\n\n                <div class=\"span10\">\n\n                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += "\n                            ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "release") {
output += "\n                            <small class=\"pull-right\"> ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"media")),"length"), env.opts.autoescape);
output += " Tracks</small>\n                            ";
;
}
output += "\n                            ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "artist") {
output += "\n                            <small style=\"font-weight: normal; font-size: 90%; opacity: 0.7; padding-left: 10px;\"> ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"type"), env.opts.autoescape);
output += "</small>\n                            <small class=\"pull-right\"> ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"media_count"), env.opts.autoescape);
output += " Tracks</small>\n                            ";
;
}
output += "\n                            ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "label") {
output += "\n                            <small class=\"pull-right\"> ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"release_count"), env.opts.autoescape);
output += " Releases</small>\n                            ";
;
}
output += "\n                        </strong>\n\n                        <ul class=\"unstyled\">\n                            ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "release") {
output += "\n                                <li>\n                                    <span class=\"value\">\n                                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"releasedate"), env.opts.autoescape);
output += " ";
if(runtime.memberLookup((t_4),"releasedate") && runtime.memberLookup((t_4),"release_country")) {
output += " | ";
;
}
output += " ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"release_country"), env.opts.autoescape);
output += "</strong>\n                                    </span>\n                                </li>\n                                <li>\n                                    <span class=\"title\">\n                                        Artist:\n                                    </span>\n                                    <span class=\"value\">\n                                        ";
frame = frame.push();
var t_7 = runtime.memberLookup((t_4),"artist");
if(t_7) {var t_6 = t_7.length;
for(var t_5=0; t_5 < t_7.length; t_5++) {
var t_8 = t_7[t_5];
frame.set("artist", t_8);
frame.set("loop.index", t_5 + 1);
frame.set("loop.index0", t_5);
frame.set("loop.revindex", t_6 - t_5);
frame.set("loop.revindex0", t_6 - t_5 - 1);
frame.set("loop.first", t_5 === 0);
frame.set("loop.last", t_5 === t_6 - 1);
frame.set("loop.length", t_6);
output += "\n                                            <strong>\n                                                ";
if(runtime.memberLookup((t_8),"artist")) {
output += "\n                                                    ";
output += runtime.suppressValue(runtime.memberLookup((t_8),"artist"), env.opts.autoescape);
output += "\n                                                ";
;
}
else {
output += "\n                                                    ";
output += runtime.suppressValue(t_8, env.opts.autoescape);
output += "\n                                                ";
;
}
output += "\n                                                ";
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last")) {
output += ",";
;
}
output += " </strong>\n                                        ";
;
}
}
frame = frame.pop();
output += "\n                                    </span>\n                                </li>\n\n                                ";
if(runtime.memberLookup((t_4),"label") && runtime.memberLookup((runtime.memberLookup((t_4),"label")),"name")) {
output += "\n                                <li>\n                                    <span class=\"title\">\n                                        Label:\n                                    </span>\n                                    <span class=\"value\">\n                                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"label")),"name"), env.opts.autoescape);
output += "</strong>\n                                    </span>\n                                </li>\n                                ";
;
}
output += "\n\n                                ";
if(runtime.memberLookup((t_4),"catalognumber")) {
output += "\n                                <li>\n                                    <span class=\"title\">\n                                        Catalog #:\n                                    </span>\n                                    <span class=\"value\">\n                                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"catalognumber"), env.opts.autoescape);
output += "</strong>\n                                    </span>\n                                </li>\n                                ";
;
}
output += "\n\n                            ";
;
}
output += "\n\n\n\n                            ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "artist") {
output += "\n\n                                ";
if(runtime.memberLookup((t_4),"country_name")) {
output += "\n                                <li>\n                                    <span class=\"value\">\n                                        ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"country_name"), env.opts.autoescape);
output += "\n                                    </span>\n                                </li>\n                                ";
;
}
output += "\n\n                                ";
if(runtime.memberLookup((t_4),"real_name")) {
output += "\n                                <li>\n                                    <span class=\"title\">\n                                        Real name:\n                                    </span>\n                                    <span class=\"value\">\n                                        ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"real_name"), env.opts.autoescape);
output += "\n                                    </span>\n                                </li>\n                                ";
;
}
output += "\n\n                                <li>\n                                    <span class=\"value\">\n                                        ";
if(runtime.memberLookup((t_4),"date_start")) {
output += "*";
output += runtime.suppressValue(runtime.memberLookup((t_4),"date_start"), env.opts.autoescape);
;
}
output += " ";
if(runtime.memberLookup((t_4),"date_end")) {
output += "✝";
output += runtime.suppressValue(runtime.memberLookup((t_4),"date_end"), env.opts.autoescape);
;
}
output += "\n                                    </span>\n                                </li>\n\n\n                                ";
if(runtime.memberLookup((t_4),"disambiguation")) {
output += "\n                                <li>\n                                    <span class=\"value\">\n                                        ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"disambiguation"), env.opts.autoescape);
output += "\n                                    </span>\n                                </li>\n                                ";
;
}
output += "\n\n                            ";
;
}
output += "\n\n\n                            ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "label") {
output += "\n                                <li>\n                                    <span class=\"value\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"type_display"), env.opts.autoescape);
output += "</span>\n                                </li>\n                                ";
if(runtime.memberLookup((t_4),"labelcode")) {
output += "\n                                <li>\n                                    <span class=\"title\">\n                                        Label code:\n                                    </span>\n                                    <span class=\"value\">\n                                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"labelcode"), env.opts.autoescape);
output += "</strong>\n                                    </span>\n                                </li>\n                                ";
;
}
output += "\n                            ";
;
}
output += "\n\n\n                            ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "media") {
output += "\n                                <li>\n                                    <span class=\"value\">\n                                        ";
if(runtime.memberLookup((t_4),"mediatype")) {
output += "\n                                            ";
output += runtime.suppressValue(env.getFilter("upper").call(context, runtime.memberLookup((t_4),"mediatype")), env.opts.autoescape);
output += " |\n                                        ";
;
}
output += "\n                                        ";
if(runtime.memberLookup((t_4),"artist")) {
output += "\n                                            by: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"artist")),"name"), env.opts.autoescape);
output += "\n                                        ";
;
}
output += "\n                                    </span>\n                                </li>\n\n                                ";
if(runtime.memberLookup((t_4),"release")) {
output += "\n                                <li>\n                                    <span class=\"value\">\n                                        on: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"release")),"name"), env.opts.autoescape);
output += "\n                                    </span>\n                                </li>\n                                ";
;
}
output += "\n\n\n                                <li>\n                                    <span class=\"value\">\n                                        ";
if(runtime.memberLookup((t_4),"base_format")) {
output += "\n                                            ";
output += runtime.suppressValue(env.getFilter("upper").call(context, runtime.memberLookup((t_4),"base_format")), env.opts.autoescape);
output += " |\n                                        ";
;
}
output += "\n                                        ";
if(runtime.memberLookup((t_4),"bitrate")) {
output += "\n                                            ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"bitrate"), env.opts.autoescape);
output += " kbps |\n                                        ";
;
}
output += "\n                                        ";
if(runtime.memberLookup((t_4),"duration")) {
output += "\n                                            ";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((t_4),"duration")), env.opts.autoescape);
output += " |\n                                        ";
;
}
output += "\n                                        ";
if(runtime.memberLookup((t_4),"original_filename")) {
output += "\n                                            Original file: ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"original_filename"), env.opts.autoescape);
output += "\n                                        ";
;
}
output += "\n                                    </span>\n                                </li>\n\n\n                                ";
if(runtime.memberLookup((t_4),"playlist_usage")) {
output += "\n                                <li>\n                                    <span class=\"value warning\">\n                                        Used ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"playlist_usage"), env.opts.autoescape);
output += " time(s) in a playlist!\n                                    </span>\n                                </li>\n                                ";
;
}
output += "\n\n\n                            ";
;
}
output += "\n\n                        </ul>\n\n                </div>\n\n            </div>\n\n\n        </div>\n\n\n\n    ";
;
}
}
frame = frame.pop();
output += "\n</div>\n\n\n<div class=\"action\">\n    <form class=\"form-horizontal\">\n        <a class=\"pull-right confirm btn btn-primary\" data-action=\"confirm\" type=\"button\">Confirm Merge</a>\n    </form>\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/merge/merge_dialog_progress.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"info\">\n\n    <a class=\"pull-right exit btn\" data-action=\"exit\">close <i class=\"icon icon-remove-sign\"></i></a>\n    <strong>Merge items</strong>\n    <p>(This can not be undone!)</p>\n\n</div>\n\n<div class=\"listing\" style=\"height: 200px; width: 700px;\">\n\n    <p style=\"text-align: center; padding-top: 50px; color: white;\">\n        <i class=\"icon icon-spin icon-spinner icon-4x\"></i>\n    </p>\n    <p style=\"text-align: center; padding-top: 5px; color: white;\">\n        Processing merge\n    </p>\n\n</div>\n\n\n<div class=\"action\">\n    &nbsp;\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/playlist/_transform_duration.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"summary item criteria duration ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error")) {
output += "warning";
;
}
else {
output += "success";
;
}
output += "\">\n    <span class=\"title\">\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error")) {
output += "\n            <i class=\"icon-warning-sign\"></i>\n        ";
;
}
else {
output += "\n            <i class=\"icon-check-sign\"></i>\n        ";
;
}
output += "\n        Duration\n    </span>\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error")) {
output += "\n    <div class=\"row-fluid information\">\n        <div class=\"span12\">\n            <p>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error"), env.opts.autoescape);
output += "</p>\n            <dl class=\"dl-horizontal\">\n                <dt>Target</dt>\n                <dd>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"target")), env.opts.autoescape);
output += "</dd>\n\n                <dt>Total</dt>\n                <dd>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"total")), env.opts.autoescape);
output += "</dd>\n\n                <dt class=\"mark\">Difference</dt>\n                <dd class=\"mark\">";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"difference")), env.opts.autoescape);
output += "</dd>\n            </dl>\n        </div>\n    </div>\n    ";
;
}
output += "\n\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/playlist/autocomplete.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"result\">\n\t<div class=\"search\">\n\t\t<h1>Search [Hit \"Enter\"]</h1>\n\t\t<p>\n\t\t\tSearch Library for: \"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query"), env.opts.autoescape);
output += "\"\n\t\t</p>\n        <a class=\"exit btn\">close <i class=\"icon icon-remove-sign\"></i></a>\n\t</div>\n    <div class=\"listing\">\n        ";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n            <div class=\"item linkable hoverable\">\n\n                <div class=\"row-fluid\">\n\n                    <div class=\"span2\">\n                        <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\"/>\n                    </div>\n\n                    <div class=\"span10\">\n\n                        <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"get_absolute_url"), env.opts.autoescape);
output += "\" class=\"link-main\">\n                            <h2>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"name"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
if(runtime.memberLookup((t_4),"type")) {
output += "\n                                <small class=\"\" style=\"font-size: 11px\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"type"), env.opts.autoescape);
output += "</small>";
;
}
output += "</h2>\n                        </a>\n\n\n                        <div class=\"related\">\n                            <ul class=\"unstyled\">\n                                ";
if(runtime.memberLookup((t_4),"series")) {
output += "\n                                    <li>Series:\n                                        ";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"series"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "\n                                        ";
if(runtime.memberLookup((t_4),"series_number")) {
output += "\n                                            #";
output += runtime.suppressValue(runtime.memberLookup((t_4),"series_number"), env.opts.autoescape);
output += "\n                                        ";
;
}
output += "\n                                    </li>\n                                ";
;
}
output += "\n                                ";
if(runtime.memberLookup((t_4),"user")) {
output += "\n                                    <li>User: ";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"user"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</li>\n                                ";
;
}
output += "\n\n                            </ul>\n\n                        </div>\n\n\n                    </div>\n\n                </div>\n\n\n            </div>\n        ";
;
}
}
frame = frame.pop();
output += "\n    </div>\n</div>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/playlist/editor_item.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"list_body_row item hoverable editable ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += " ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_type"), env.opts.autoescape);
output += " ";
if(runtime.contextOrFrameLookup(context, frame, "readonly")) {
output += " readonly";
;
}
output += "\"\n     data-updated=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"updated"), env.opts.autoescape);
output += "\"\n     data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri"), env.opts.autoescape);
output += "\"\n     data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\"\n     data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\"\n     id=\"playlist_item_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\">\n\n    <div class=\"row-fluid base\">\n\n        <div class=\"span1 actions\">\n\n            <ul class=\"unstyled\">\n                <li>\n                    <a href=\"#\" data-action=\"stop\" class=\"visible-while-playing\">\n                        &nbsp;&nbsp;<i class=\" icon-stop icon-large\"></i>\n                    </a>\n                    <a href=\"#\" data-action=\"play\" class=\"hidden-while-playing\">\n                        &nbsp;&nbsp;<i class=\" icon-play icon-large\"></i>\n                    </a>\n                    <a href=\"#\" data-action=\"pause\" class=\"\">\n                        &nbsp;&nbsp;<i class=\" icon-pause icon-large\"></i>\n                    </a>\n                </li>\n            </ul>\n            ";
if(!runtime.contextOrFrameLookup(context, frame, "readonly")) {
output += "\n                <!--\n                <span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"duration")), env.opts.autoescape);
output += "</span>\n                -->\n                <span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, (runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"duration") - runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_in") - runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_out"))), env.opts.autoescape);
output += "</span>\n            ";
;
}
output += "\n        </div>\n\n        <div class=\"span3\">\n            <ul class=\"unstyled\">\n                <li class=\"bold\">\n                    <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"absolute_url"), env.opts.autoescape);
output += "\"\n                       title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"name"), env.opts.autoescape);
output += "\">\n                        ";
output += runtime.suppressValue(env.getFilter("shorten").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"name"),30), env.opts.autoescape);
output += "\n                    </a>\n                </li>\n                <li class=\"small relations\">\n\n                    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"artist")) {
output += "\n                        <span>\n\t\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"artist")),"absolute_url"), env.opts.autoescape);
output += "\"\n                           title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"artist")),"name"), env.opts.autoescape);
output += "\">\n                            ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"artist")),"name"), env.opts.autoescape);
output += "\n                        </a>\n\t\t\t\t\t</span> |\n                    ";
;
}
output += "\n\n                    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"release")) {
output += "\n                        <span>\n\t\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"release")),"absolute_url"), env.opts.autoescape);
output += "\"\n                           title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"release")),"name"), env.opts.autoescape);
output += "\">\n                            ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_object")),"release")),"name"), env.opts.autoescape);
output += "\n                        </a>\n\t\t\t\t\t</span> |\n                    ";
;
}
output += "\n\n\n                </li>\n            </ul>\n        </div>\n        <!---->\n        <div class=\"span1 fade-cue\" style=\"width: 80px;\">\n\n            <div class=\"row-fluid pull-right\">\n\n                <div class=\"span11\" style=\"margin-left: 0\">\n\n                    ";
if(runtime.contextOrFrameLookup(context, frame, "enable_crossfades")) {
output += "\n\n                    ";
if(!runtime.contextOrFrameLookup(context, frame, "readonly")) {
output += "\n                        <input class=\"fade_cross\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_cross"), env.opts.autoescape);
output += "\"/>\n                    ";
;
}
output += "\n\n                    <span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_cross")), env.opts.autoescape);
output += "</span><a class=\"editor preview\"\n                                                                   data-preview=\"fade_cross\"\n                                                                   href=\"#\"><i class=\"icon-volume-up icon-small\"></i></a>\n\n                    ";
;
}
else {
output += "\n                    <span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_cross")), env.opts.autoescape);
output += "</span>\n                    ";
;
}
output += "\n\n                </div>\n\n            </div>\n        </div>\n\n        <div class=\"span3 fade-cue\">\n\n            <div class=\"row-fluid pull-right\">\n\n                <div class=\"span6\" style=\"margin-left: 0\">\n\n                    ";
if(!runtime.contextOrFrameLookup(context, frame, "readonly")) {
output += "\n                        <input class=\"fade_in\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_in"), env.opts.autoescape);
output += "\"/>\n                    ";
;
}
output += "\n\n                    <span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_in")), env.opts.autoescape);
output += "</span> <a class=\"editor preview\" data-preview=\"fade_in\" href=\"#\"><i\n                        class=\"icon-volume-up icon-small\"></i></a>\n\n                </div>\n                <div class=\"span6\" style=\"margin-left: 0\">\n\n                    ";
if(!runtime.contextOrFrameLookup(context, frame, "readonly")) {
output += "\n                        <input class=\"fade_out\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_out"), env.opts.autoescape);
output += "\"/>\n                    ";
;
}
output += "\n\n                    <span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"fade_out")), env.opts.autoescape);
output += "</span> <a class=\"editor preview\"\n                                                                  data-preview=\"fade_out\"\n                                                                  href=\"#\"><i class=\"icon-volume-up icon-small\"></i></a>\n                </div>\n\n            </div>\n\n        </div>\n\n        <div class=\"span3 fade-cue\">\n\n            <div class=\"row-fluid pull-right\">\n\n                <div class=\"span6\" style=\"margin-left: 0\">\n\n                    ";
if(!runtime.contextOrFrameLookup(context, frame, "readonly")) {
output += "\n                        <input class=\"cue_in\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_in"), env.opts.autoescape);
output += "\"/>\n                    ";
;
}
output += "\n                    <span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_in")), env.opts.autoescape);
output += "</span>\n                </div>\n                <div class=\"span6\" style=\"margin-left: 0\">\n\n                    ";
if(!runtime.contextOrFrameLookup(context, frame, "readonly")) {
output += "\n                        <input class=\"cue_out\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_out"), env.opts.autoescape);
output += "\"/>\n                    ";
;
}
output += "\n\n                    <span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"cue_out")), env.opts.autoescape);
output += "</span>\n                </div>\n\n            </div>\n\n        </div>\n\n        <div class=\"span1 actions\">\n\n            <ul class=\"unstyled\">\n                <li>\n\n                    <a href=\"#\" data-action=\"collect\" class=\" pull-right\">\n                        &nbsp;&nbsp;<i class=\"icon-plus icon-large\"></i>\n                    </a>\n\n                    ";
if(!runtime.contextOrFrameLookup(context, frame, "readonly")) {
output += "\n                        <a href=\"#\" data-action=\"delete\" class=\" pull-right\">\n                            <i class=\"icon-trash icon-large\"></i>\n                        </a>\n                    ";
;
}
output += "\n\n\n                </li>\n            </ul>\n\n        </div>\n\n    </div>\n\n\n    <div class=\"row-fluid playhead\">\n        <div class=\"span12\">\n\n            <div class=\"waveform\" id=\"playlist_item_waveform_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\"></div>\n\n        </div>\n\n    </div>\n\n\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/playlist/editor_search.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "\n\n    <div class=\"listing\">\n        ";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n            <div class=\"item hoverable clearfix\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"resource_uri"), env.opts.autoescape);
output += "\">\n\n                <div class=\"\">\n\n                    <div class=\"image\">\n                        <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\"/>\n                    </div>\n\n                    <div class=\"information\">\n\n                        <span class=\"title\">";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"name"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "<small class=\"pull-right\">";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((t_4),"duration")), env.opts.autoescape);
output += "</small></span>\n\n                        <div class=\"related\">\n                            <ul class=\"unstyled horizontal\">\n                                ";
if(runtime.memberLookup((t_4),"artist")) {
output += "\n                                    <li><small>by:</small> ";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"artist"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</li>\n                                ";
;
}
output += "\n                                ";
if(runtime.memberLookup((t_4),"release")) {
output += "\n                                    <li><small>on:</small> ";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"release"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</li>\n                                ";
;
}
output += "\n                            </ul>\n\n                        </div>\n\n                    </div>\n\n                </div>\n\n            </div>\n\n        ";
;
}
}
frame = frame.pop();
output += "\n    </div>\n\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/playlist/editor_transform_summary.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "\n\t\t<div class=\"summary item target-duration ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error")) {
output += "warning";
;
}
else {
output += "success";
;
}
output += "\">\n\t\t\t<span class=\"title\">\n                ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error")) {
output += "\n                    <i class=\"icon-warning-sign\"></i>\n                ";
;
}
else {
output += "\n                    <i class=\"icon-check-sign\"></i>\n                ";
;
}
output += "\n\n                Target Duration\n            </span>\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error")) {
output += "\n\t\t\t<div class=\"row-fluid information\">\n\t\t\t\t<div class=\"span12\">\n\t\t\t\t\t<p>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"error"), env.opts.autoescape);
output += "</p>\n\t\t\t\t\t<dl class=\"dl-horizontal\">\n\t\t\t\t\t\t<dt>Target</dt>\n\t\t\t\t\t\t<dd>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"target")), env.opts.autoescape);
output += "</dd>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<dt>Total</dt>\n\t\t\t\t\t\t<dd>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"total")), env.opts.autoescape);
output += "</dd>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<dt>Difference</dt>\n\t\t\t\t\t\t<dd>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "durations")),"difference")), env.opts.autoescape);
output += "</dd>\n\t\t\t\t\t</dl>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t";
;
}
output += "\n\t\t\t\n\t\t</div>\n\t\n\t\t\n\t\t<div class=\"summary item dayparts\">\n\t\t\t<span class=\"title\"><i class=\"icon-check-sign\"></i> Broadcast Dayparts</span>\n\t\t\t<div class=\"row-fluid information\">\n\t\t\t\t<div class=\"span12\">\n\t\t\t\t\t<p>Please specify the best Broadcast Dayparts</p>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/playlist/listing_inline.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "\n\n\t<div id=\"playlist_holder_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\" data-object_id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\" class=\"playlist_holder \" data-updated=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"updated"), env.opts.autoescape);
output += "\">\n\n\t\t<div class=\"header\">\n\n\t\t\t<div class=\"right\">\n\t\t\t\t<a href=\"#\" title=\"Remove\" data-action=\"delete\" class=\"action delete\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Remove\"></a>\n\t\t\t</div>\n\n\t\t\t<div class=\"right\">\n\t\t\t\t<a href=\"#\" title=\"Edit name\" data-action=\"edit\" class=\"action edit\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Edit name\"></a>\n\t\t\t</div>\n\n\t\t\t<div class=\"right\">\n\t\t\t\t<a href=\"#playlist:393:mp3\" title=\"Download\" data-action=\"download\" class=\"action downloadable queue\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Edit name\"></a>\n\t\t\t</div>\n\n\t\t\t<div class=\"left name\">\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"), env.opts.autoescape);
output += "\n\t\t\t</div>\n\t\t\t<div class=\"clear\"></div>\n\t\t</div>\n\n\t\t<div class=\"panel\">\n\n\t\t\t<div class=\"edit\">\n\t\t\t\t<div class=\"hint\">\n\t\t\t\t\tEnter the new name for the basket\n\t\t\t\t</div>\n\t\t\t\t<div class=\"input\">\n\t\t\t\t\t<input type=\"text\" id=\"playlist_edit_name_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\" name=\"playlist_edit_name\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"), env.opts.autoescape);
output += "\">\n\t\t\t\t</div>\n\t\t\t</div>\n\n\t\t\t<div class=\"convert\">\n\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"edit_url"), env.opts.autoescape);
output += "\">Edit</a>\n\t\t\t\t<!--<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">Detail</a>-->\n\t\t\t</div>\n\t\t\t<div class=\"duration\">\n\t\t\t\t";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"duration")), env.opts.autoescape);
output += "\n\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"target_duration"), env.opts.autoescape);
output += "000\n\t\t\t</div>\n\t\t</div>\n\n\t\t<div class=\"list\">\n\t\t\t\n\n\t\t\t";
frame = frame.push();
var t_3 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"items");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n\t\t\t\n\t\t\t\n\t\t\t<div class=\"sidebar list item source ct-";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"item")),"content_type"), env.opts.autoescape);
output += "\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"resource_uri"), env.opts.autoescape);
output += "\">\n\t\t\t\t<div class=\"right\">\n\t\t\t\t\t<a href=\"#\" title=\"Remove\" data-action=\"delete\" class=\"action delete\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Remove\"></a>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"left\">\n\t\t\t\t\t<a href=\"#\" title=\"Play\" class=\"action play playable popup\"><img src=\"/static/img/base/spacer.png\" width=\"16\" height=\"16\" alt=\"Play\"></a>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"left title\">\n\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((t_4),"item")),"content_object")),"absolute_url"), env.opts.autoescape);
output += "\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((t_4),"item")),"content_object")),"name"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((t_4),"item")),"content_object")),"name"),36), env.opts.autoescape);
output += "</a>\n\t\t\t\t</div>\n\t\t\t\t<div class=\"clear\"></div>\n\t\t\t</div>\n\t\t\t\n\t\t\t";
;
}
}
frame = frame.pop();
output += "\n\t\t\t\n\t\t</div>\n\n\t</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/playlist/select_popup.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<section class=\"title\">\n    <h3>Playlists\n        <small class=\"pull-right\">...</small>\n    </h3>\n</section>\n\n<section class=\"search\">\n    <div class=\"\">\n\n        <input type=\"text\" class=\"search\" title=\"Search\" placeholder=\"Type to search\">\n    </div>\n\n</section>\n\n\n<section class=\"listing nano\" id=\"playlist_list\">\n    <div class=\"content\">\n\n        ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "data")),"objects")),"length") > 0) {
output += "\n\n        <p class=\"notice\">\n        You don't have any playlists yet.<br />\n        Use the \"Create a new list\" function below.\n        </p>\n        ";
;
}
output += "\n\n        ";
frame = frame.push();
var t_3 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "data")),"objects");
runtime.asyncEach(t_3, 1, function(item, t_1, t_2,next) {
frame.set("item", item);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n            ";
env.getTemplate("alibrary/nj/playlist/select_popup_item.html", false, "alibrary/nj/playlist/select_popup.html", function(t_6,t_4) {
if(t_6) { cb(t_6); return; }
t_4.render(context.getVariables(), frame, function(t_7,t_5) {
if(t_7) { cb(t_7); return; }
output += t_5
output += "\n        ";
next(t_1);
})});
}, function(t_9,t_8) {
if(t_9) { cb(t_9); return; }
frame = frame.pop();
output += "\n    </div>\n</section>\n\n<section class=\"form\">\n\n    <div class=\"btn-toolbar\">\n        <div class=\"btn-group\">\n            <input type=\"text\" class=\"name\" title=\"Name\" placeholder=\"Create a new playlist\" required>\n            <a data-action=\"cancel\" class=\"btn btn-mini\">Cancel</a>\n            <a data-action=\"save\" class=\"btn btn-primary btn-mini\">Save</a>\n        </div>\n    </div>\n\n\n</section>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
});
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/playlist/select_popup_item.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"item hoverable playlist ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"uuid"), env.opts.autoescape);
output += "\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += "\" data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"uuid"), env.opts.autoescape);
output += "\" data-name=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name"), env.opts.autoescape);
output += "\"\n     data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"resource_uri"), env.opts.autoescape);
output += "\">\n\n    <div class=\"row-fluid\">\n\n        <div class=\"span1 image\">\n\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image")) {
output += "\n                <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image"), env.opts.autoescape);
output += "\"/>\n            ";
;
}
else {
output += "\n                <img src=\"/static/img/base/defaults/listview.playlist.xl.png\"/>\n            ";
;
}
output += "\n\n        </div>\n\n        <div class=\"span11 information\">\n\n            <ul class=\"unstyled\">\n\n                <li>\n\n                    <strong><a class=\"\" title=\"Click to visit detail page\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name"),30), env.opts.autoescape);
output += "</a></strong>\n\n                    <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"item_count"), env.opts.autoescape);
output += " tracks | ";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"duration")), env.opts.autoescape);
output += "</small>\n                </li>\n                <li>\n                    <!--\n                    <span class=\"number\">";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"updated"),"date"), env.opts.autoescape);
output += "</span>\n                    -->\n                    <span title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags"),30), env.opts.autoescape);
output += "</span>\n\n\n                    <span class=\"collected pull-right\"></span>\n\n\n                    <!--<span>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"type"), env.opts.autoescape);
output += "</span>-->\n                </li>\n            </ul>\n\n        </div>\n\n    </div>\n\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/provider/relation_inline.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<p>\n    <span class=\"relation";
if(runtime.contextOrFrameLookup(context, frame, "match")) {
output += " match";
;
}
if(runtime.contextOrFrameLookup(context, frame, "no_match")) {
output += " diff";
;
}
output += "\"\n         data-service=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"service"), env.opts.autoescape);
output += "\"\n         data-url=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uri"), env.opts.autoescape);
output += "\">\n         <span style=\"white-space: nowrap;\">\n             ";
if(runtime.contextOrFrameLookup(context, frame, "match")) {
output += "\n                <i class=\"icon-link\"></i>\n             ";
;
}
else {
output += "\n                 <i class=\"icon-chevron-sign-up\"></i>\n             ";
;
}
output += "\n\n             <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uri"), env.opts.autoescape);
output += "\" class=\"skip-external\" target=\"_blank\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uri"), env.opts.autoescape);
output += "</a></span>\n    </span>\n</p>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/provider/search_dialog.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"query\">\n\n    <form class=\"form-horizontal\">\n        <input class=\"query\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "query"), env.opts.autoescape);
output += "\">\n        <a class=\"pull-right exit btn\">close <i class=\"icon icon-remove-sign\"></i></a>\n        <a class=\"pull-right search btn btn-primary\" type=\"button\">Search</a>\n\n        ";
if(runtime.contextOrFrameLookup(context, frame, "provider") == "discogs") {
output += "\n            <p class=\"hint\">\n                <i class=\"icon-info-sign\"></i> <strong>Info:</strong> You can search by <em>Discogs IDs</em> as well.\n            </p>\n        ";
;
}
output += "\n\n        ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "release" && runtime.contextOrFrameLookup(context, frame, "provider") == "musicbrainz") {
output += "\n            <p class=\"hint\">\n                <i class=\"icon-info-sign\"></i> <strong>Info:</strong> You can search by <em>BARCODES</em> as well!\n            </p>\n        ";
;
}
output += "\n\n    </form>\n\n</div>\n\n\n<div class=\"results\" style=\"max-height: 400px; overflow: auto; width: 700px;\">\n\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "results")),"length") < 1) {
output += "\n\n        <p>\n            Sorry - but we could not find any results.\n        </p>\n    ";
;
}
output += "\n\n    ";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "results");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("result", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n        <div class=\"item result\" data-uri=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"uri"), env.opts.autoescape);
output += "\">\n\n            ";
if(runtime.contextOrFrameLookup(context, frame, "provider") == "discogs") {
output += "\n                <div class=\"row-fluid\">\n\n                    <div class=\"span2\">\n                        ";
if(runtime.memberLookup((t_4),"thumb")) {
output += "\n                            <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"thumb"), env.opts.autoescape);
output += "\">\n                        ";
;
}
else {
output += "\n                            <img src=\"/static/img/base/defaults/listview.release.xl.png\">\n                        ";
;
}
output += "\n                    </div>\n\n\n                    <div class=\"span10\">\n                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"title"), env.opts.autoescape);
output += "</strong>\n                        <ul class=\"unstyled\">\n\n                            ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "release") {
output += "\n                            <li>\n\n                            <span class=\"value\">\n                                <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"year"), env.opts.autoescape);
output += " | ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"country"), env.opts.autoescape);
output += "</strong>\n                                ";
if(runtime.memberLookup((t_4),"label")) {
output += "\n                                    - on\n                                    <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"label"), env.opts.autoescape);
output += "</strong>\n                                ";
;
}
output += "\n                            </span>\n                            </li>\n\n                            <li>\n                            <span class=\"title\">\n                                Catalog #:\n                            </span>\n                            <span class=\"value\">\n                                <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"catno"), env.opts.autoescape);
output += "</strong>\n                            </span>\n                            </li>\n\n                            <li>\n                            <span class=\"title\">\n                                Format:\n                            </span>\n                            <span class=\"value\">\n                                <strong>\n                                    ";
frame = frame.push();
var t_7 = runtime.memberLookup((t_4),"format");
if(t_7) {var t_6 = t_7.length;
for(var t_5=0; t_5 < t_7.length; t_5++) {
var t_8 = t_7[t_5];
frame.set("k", t_8);
frame.set("loop.index", t_5 + 1);
frame.set("loop.index0", t_5);
frame.set("loop.revindex", t_6 - t_5);
frame.set("loop.revindex0", t_6 - t_5 - 1);
frame.set("loop.first", t_5 === 0);
frame.set("loop.last", t_5 === t_6 - 1);
frame.set("loop.length", t_6);
output += "\n                                        ";
output += runtime.suppressValue(t_8, env.opts.autoescape);
output += " |\n                                    ";
;
}
}
frame = frame.pop();
output += "\n                                </strong>\n                            </span>\n                            ";
;
}
output += "\n\n                            </li>\n\n                        </ul>\n                    </div>\n\n\n                </div>\n            ";
;
}
output += "\n\n            ";
if(runtime.contextOrFrameLookup(context, frame, "provider") == "musicbrainz") {
output += "\n                <div class=\"row-fluid\">\n\n                    <div class=\"span2\">\n                        ";
if(runtime.memberLookup((t_4),"thumb")) {
output += "\n                            <img src=\"/static/img/base/defaults/listview.release.xl.png\" data-carchive_url=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"thumb"), env.opts.autoescape);
output += "\">\n                        ";
;
}
output += "\n                    </div>\n\n\n\n\n                    <div class=\"span10\">\n\n\n\n                        ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "release") {
output += "\n                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"title"), env.opts.autoescape);
output += "</strong>\n                        <ul class=\"unstyled\">\n\n                            ";
if(runtime.memberLookup((t_4),"artist-credit")) {
output += "\n                                ";
frame = frame.push();
var t_11 = runtime.memberLookup((t_4),"artist-credit");
if(t_11) {var t_10 = t_11.length;
for(var t_9=0; t_9 < t_11.length; t_9++) {
var t_12 = t_11[t_9];
frame.set("a", t_12);
frame.set("loop.index", t_9 + 1);
frame.set("loop.index0", t_9);
frame.set("loop.revindex", t_10 - t_9);
frame.set("loop.revindex0", t_10 - t_9 - 1);
frame.set("loop.first", t_9 === 0);
frame.set("loop.last", t_9 === t_10 - 1);
frame.set("loop.length", t_10);
output += "\n                                    <li>\n                                        <span class=\"value\">\n                                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_12),"artist")),"name"), env.opts.autoescape);
output += "</strong>\n                                        </span>\n                                    </li>\n                                ";
;
}
}
frame = frame.pop();
output += "\n                            ";
;
}
output += "\n\n\n                            <li>\n                                <span class=\"value\">\n                                    <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"date"), env.opts.autoescape);
output += " ";
if(runtime.memberLookup((t_4),"date") && runtime.memberLookup((t_4),"country")) {
output += "|";
;
}
output += " ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"country"), env.opts.autoescape);
output += "</strong>\n                                </span>\n                            </li>\n\n                            ";
if(runtime.memberLookup((t_4),"label-info")) {
output += "\n                                ";
frame = frame.push();
var t_15 = runtime.memberLookup((t_4),"label-info");
if(t_15) {var t_14 = t_15.length;
for(var t_13=0; t_13 < t_15.length; t_13++) {
var t_16 = t_15[t_13];
frame.set("l", t_16);
frame.set("loop.index", t_13 + 1);
frame.set("loop.index0", t_13);
frame.set("loop.revindex", t_14 - t_13);
frame.set("loop.revindex0", t_14 - t_13 - 1);
frame.set("loop.first", t_13 === 0);
frame.set("loop.last", t_13 === t_14 - 1);
frame.set("loop.length", t_14);
output += "\n                                    <li style=\"float: left; margin-right: 30px;\">\n\n                                        <span class=\"title\">\n                                            Catalog #:\n                                        </span>\n                                        <span class=\"value\">\n                                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_16),"catalog-number"), env.opts.autoescape);
output += "</strong>\n                                        </span>\n                                    </li>\n                                ";
;
}
}
frame = frame.pop();
output += "\n                            ";
;
}
output += "\n\n\n                            ";
if(runtime.memberLookup((t_4),"barcode")) {
output += "\n                                <li>\n                                <span class=\"title\">\n                                    Barcode:\n                                </span>\n                                <span class=\"value\">\n                                    <strong>\n                                        ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"barcode"), env.opts.autoescape);
output += "\n                                    </strong>\n                                </span>\n                                </li>\n                            ";
;
}
output += "\n\n\n                        </ul>\n                        ";
;
}
output += "\n\n\n\n                        ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "artist") {
output += "\n                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += " | ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"country"), env.opts.autoescape);
output += "</strong>\n                        <ul class=\"unstyled\">\n\n\n                            <li>\n                            <span class=\"title\">\n                                Type:\n                            </span>\n                            <span class=\"value\">\n                                <strong>\n                                    ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"type"), env.opts.autoescape);
output += "\n\n                                </strong>\n                            </span>\n                            </li>\n\n                        </ul>\n                        ";
;
}
output += "\n\n\n\n                        ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "label") {
output += "\n                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += " | ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"country"), env.opts.autoescape);
output += "</strong>\n                        <ul class=\"unstyled\">\n\n                            ";
if(runtime.memberLookup((runtime.memberLookup((t_4),"life-span")),"begin")) {
output += "\n                            <li>\n                            <span class=\"title\">\n                                Dates:\n                            </span>\n                            <span class=\"value\">\n                                ";
if(runtime.memberLookup((runtime.memberLookup((t_4),"life-span")),"begin")) {
output += "\n                                <strong>\n                                    * ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"life-span")),"begin"), env.opts.autoescape);
output += "\n                                </strong>\n                                ";
;
}
output += "\n                                ";
if(runtime.memberLookup((runtime.memberLookup((t_4),"life-span")),"end")) {
output += "\n                                <strong>\n                                    ✝ ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"life-span")),"end"), env.opts.autoescape);
output += "\n                                </strong>\n                                ";
;
}
output += "\n                            </span>\n                            </li>\n                            ";
;
}
output += "\n\n                        </ul>\n                        ";
;
}
output += "\n\n\n\n                        ";
if(runtime.contextOrFrameLookup(context, frame, "item_type") == "media") {
output += "\n                        <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"title"), env.opts.autoescape);
output += "</strong> | <span>";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((t_4),"length")), env.opts.autoescape);
output += "</span>\n                        <ul class=\"unstyled\">\n\n                            ";
if(runtime.memberLookup((t_4),"artist-credit")) {
output += "\n                            <li>\n                            <span class=\"title\">\n                                Artist:\n                            </span>\n                            <span class=\"value\">\n\n                                <strong>\n                                    ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((t_4),"artist-credit")),0)),"artist")),"name"), env.opts.autoescape);
output += "\n                                </strong>\n\n                            </span>\n                            </li>\n                            ";
;
}
output += "\n\n                        </ul>\n                        ";
;
}
output += "\n\n\n\n\n                    </div>\n\n\n                </div>\n            ";
;
}
output += "\n\n\n        </div>\n\n\n\n    ";
;
}
}
frame = frame.pop();
output += "\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/reassign/reassign_dialog.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"query\">\n\n    <form class=\"form-horizontal\">\n        <input class=\"query\" type=\"text\" value=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "query"), env.opts.autoescape);
output += "\">\n        <a class=\"pull-right exit btn\" data-action=\"exit\">close <i class=\"icon icon-remove-sign\"></i></a>\n\n        <!--\n        <p class=\"hint\">\n            <i class=\"icon-warning-sign\"></i> <strong>Warning:</strong> This can not be undone!\n        </p>\n        -->\n    </form>\n</div>\n\n\n<div class=\"results\" style=\"max-height: 400px; overflow: auto; width: 700px;\">\n\n    <div id=\"search_result\">\n        <!-- loaded dynamically, template: reassign_dialog_search_result.html -->\n    </div>\n\n</div>\n\n\n<div class=\"action\">\n    <form class=\"form-horizontal\">\n        <!--\n        <span class=\"info\" style=\"top: 6px; position: relative;\">\n            4 Tracks will be moved to a <em>NEWLY CREATED</em> release with the name \"Peter & der Wolf\".\n        </span>\n        -->\n        <a class=\"pull-right confirm btn btn-primary\" data-action=\"confirm\" type=\"button\">Confirm reassignment</a>\n    </form>\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/reassign/reassign_dialog_continue.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"query\">\n\n    <form class=\"form-horizontal\">\n        <span>&nbsp;</span>\n        <a class=\"pull-right exit btn\" data-action=\"exit\">close <i class=\"icon icon-remove-sign\"></i></a>\n    </form>\n</div>\n\n\n<div class=\"results\" style=\"max-height: 400px; overflow: auto; width: 700px;\">\n    <p class=\"message\">Items successfully reassigned.</p>\n</div>\n\n\n<div class=\"action\">\n    <form class=\"form-horizontal\">\n        <a href=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "next"), env.opts.autoescape);
output += "\" class=\"pull-right confirm btn btn-primary\" type=\"button\">Continue to assigned Release</a>\n        <a class=\"pull-right confirm btn btn-primary\" data-action=\"stay\" type=\"button\">Stay on this page</a>\n    </form>\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/reassign/reassign_dialog_progress.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"info\">\n\n    <a class=\"pull-right exit btn\" data-action=\"exit\">close <i class=\"icon icon-remove-sign\"></i></a>\n    <strong>Reassign items</strong>\n    <p>(This can not be undone!)</p>\n\n</div>\n\n<div class=\"listing\" style=\"height: 200px; width: 700px;\">\n\n    <p style=\"text-align: center; padding-top: 50px; color: white;\">\n        <i class=\"icon icon-spin icon-spinner icon-4x\"></i>\n    </p>\n    <p style=\"text-align: center; padding-top: 5px; color: white;\">\n        Processing assignment\n    </p>\n\n</div>\n\n\n<div class=\"action\">\n    &nbsp;\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/reassign/reassign_dialog_search_result.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("object", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n    <div class=\"item result hoverable\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"id"), env.opts.autoescape);
output += "\" data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"uuid"), env.opts.autoescape);
output += "\">\n\n\n        <div class=\"row-fluid\">\n\n            <div class=\"span2\">\n                ";
if(runtime.memberLookup((t_4),"main_image")) {
output += "\n                    <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\">\n                ";
;
}
else {
output += "\n                    <img src=\"/static/img/base/defaults/listview.release.xl.png\">\n                ";
;
}
output += "\n\n            </div>\n\n            <div class=\"span10\">\n\n                <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += "</strong>\n\n                <ul class=\"unstyled\">\n\n                    <li>\n                        <span class=\"value\">\n                            ";
frame = frame.push();
var t_7 = runtime.memberLookup((t_4),"artist");
if(t_7) {var t_6 = t_7.length;
for(var t_5=0; t_5 < t_7.length; t_5++) {
var t_8 = t_7[t_5];
frame.set("a", t_8);
frame.set("loop.index", t_5 + 1);
frame.set("loop.index0", t_5);
frame.set("loop.revindex", t_6 - t_5);
frame.set("loop.revindex0", t_6 - t_5 - 1);
frame.set("loop.first", t_5 === 0);
frame.set("loop.last", t_5 === t_6 - 1);
frame.set("loop.length", t_6);
output += "\n                                <strong>";
output += runtime.suppressValue(t_8, env.opts.autoescape);
output += "</strong>\n                            ";
;
}
}
frame = frame.pop();
output += "\n                        </span>\n                    </li>\n\n                    <li>\n                        <span class=\"value\">\n                            <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"media_count"), env.opts.autoescape);
output += "</strong>\n                        </span>\n                        <span class=\"title\">Tracks</span>\n                    </li>\n\n                    <li>\n                        <span class=\"value\">\n                            <strong>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"releasedate"), env.opts.autoescape);
output += "</strong>\n                        </span>\n                    </li>\n                </ul>\n            </div>\n        </div>\n    </div>\n";
;
}
}
frame = frame.pop();
output += "\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["alibrary/nj/release/autocomplete.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"result\">\n\t<div class=\"search\">\n\t\t<h1>Search [Hit \"Enter\"]</h1>\n\t\t<p>\n\t\t\tSearch Library for: \"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query"), env.opts.autoescape);
output += "\"\n\t\t</p>\n        <a class=\"exit btn\">close <i class=\"icon icon-remove-sign\"></i></a>\n\t</div>\n\t<div class=\"listing\">\n\t\t";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n\t\t<div class=\"item linkable hoverable\">\n\t\t\t\n\t\t\t<div class=\"row-fluid\">\n\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\" />\n\t\t\t\t</div>\n\n\t\t\t\t<div class=\"span10\">\n\t\t\t\t\t\n\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"get_absolute_url"), env.opts.autoescape);
output += "\" class=\"link-main\"><h2>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"name"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</h2></a>\n\t\t\t\t\t\n\n\n\t\t\t\t\t<div class=\"related\">\n\t\t\t\t\t\t";
if(env.getFilter("length").call(context, runtime.memberLookup((t_4),"media")) > 0) {
output += " <span>Tracks:</span>\n\t\t\t\t\t\t<ul class=\"horizontal\">\n\t\t\t\t\t\t\t";
frame = frame.push();
var t_7 = runtime.memberLookup((t_4),"media");
if(t_7) {var t_6 = t_7.length;
for(var t_5=0; t_5 < t_7.length; t_5++) {
var t_8 = t_7[t_5];
frame.set("media", t_8);
frame.set("loop.index", t_5 + 1);
frame.set("loop.index0", t_5);
frame.set("loop.revindex", t_6 - t_5);
frame.set("loop.revindex0", t_6 - t_5 - 1);
frame.set("loop.first", t_5 === 0);
frame.set("loop.last", t_5 === t_6 - 1);
frame.set("loop.length", t_6);
output += "\n\t\t\t\t\t\t\t<li>\n\t\t\t\t\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((t_8),"get_absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_8),"name"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += " | ";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_8),"artist"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</a>\n\t\t\t\t\t\t\t\t";
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last")) {
output += ",";
;
}
output += "\n\t\t\t\t\t\t\t</li>\n\t\t\t\t\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last")) {
output += "\n\t\t\t\t\t\t\t\t<div class=\"clear\"></div>\n\t\t\t\t\t\t\t";
;
}
output += "\n\t\t\t\t\t\t\t";
;
}
}
frame = frame.pop();
output += "\n\t\t\t\t\t\t</ul>\n\t\t\t\t\t\t";
;
}
output += "\n\t\t\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\n\n\t\t</div>\n\t\t";
;
}
}
frame = frame.pop();
output += "\n\t</div>\n</div>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["aplayer/nj/detail_player.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"list_body_row item hoverable media ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += " ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item")),"content_type"), env.opts.autoescape);
output += "\"\n     data-updated=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"updated"), env.opts.autoescape);
output += "\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri"), env.opts.autoescape);
output += "\" data-ct=\"media\" data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\"\n     data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\" id=\"playlist_item_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\">\n\n\n    <div class=\"row-fluid playhead\">\n        <div class=\"span12\">\n\n            <div class=\"overlay primary\">\n                <ul class=\"unstyled action\">\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "perms")),"play")) {
output += "\n                    <li class=\"square\">\n                        <a href=\"#\"\n                           class=\"playable popup\"\n                           data-ct=\"media\"\n                           data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri"), env.opts.autoescape);
output += "\"\n                           data-offset=\"0\"\n                           data-mode=\"replace\"\n                           title=\"Play\">\n                            <i class=\"icon icon-play\"></i>\n                        </a>\n                    </li>\n                    ";
;
}
output += "\n\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "perms")),"play")) {
output += "\n                    <li class=\"square\">\n                        <a href=\"#\"\n                           class=\"playable popup\"\n                           data-ct=\"media\"\n                           data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri"), env.opts.autoescape);
output += "\"\n                           data-offset=\"0\"\n                           data-mode=\"queue\"\n                           title=\"Queue\">\n                            <i class=\"icon icon-reorder\"></i></a>\n\n                    </li>\n                    ";
;
}
output += "\n\n                </ul>\n            </div>\n\n            <div class=\"overlay secondary\">\n                <ul class=\"unstyled action\">\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "perms")),"add")) {
output += "\n\n                    <li>\n                        <a href=\"#\"\n                           class=\"\"\n                           data-action=\"collect\"\n                           title=\"Add to playlist\">\n                            <i class=\"icon icon-plus\"></i>\n                        </a>\n                    </li>\n                    ";
;
}
output += "\n\n                </ul>\n            </div>\n\n\n            <div class=\"waveform\" id=\"detail_player_waveform_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\"></div>\n\n        </div>\n\n    </div>\n\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["aplayer/nj/inline_player_item.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"item playlist media object ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += " hoverable\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\"\n     id=\"playlist_item_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\"\n     data-item_id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\"\n     data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\"\n     data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\">\n\n    <div class=\"wrapper\">\n\n        <div class=\"row-fluid\">\n            <div class=\"span10 information\">\n                <span class=\"title\">\n                    <a class=\"\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"), env.opts.autoescape);
output += "</a>\n                </span>\n                <span><a class=\"\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"name"), env.opts.autoescape);
output += "</a> |\n                <a class=\"\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"name"), env.opts.autoescape);
output += "</a></span>\n            </div>\n            <div class=\"span2 duration\">\n                <span>\n                ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"formated_duration"), env.opts.autoescape);
output += "\n                    <a class=\"\" data-action=\"collect\" href=\"#\"><i class=\"icon-plus icon-large\"></i></a>\n                </span>\n\n\n            </div>\n        </div>\n\n    </div>\n\n\n    <div class=\"indicator\" style=\"width: 100% !important\">\n        <div class=\"wrapper\">\n            <div class=\"inner\">&nbsp;</div>\n        </div>\n    </div>\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["aplayer/nj/popup_emission.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<section class=\"title\">\n\t<h3>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"), env.opts.autoescape);
output += " <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"type_display"), env.opts.autoescape);
output += "</small></h3>\n\t<ul class=\"unstyled\">\n\t\t<li>\n\t\t\t<i class=\"icon-time\"></i> ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start"),"time"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_end"),"time"), env.opts.autoescape);
output += " | ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start"),"date"), env.opts.autoescape);
output += "\n\t\t</li>\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user")) {
output += "\n\t\t<li>\n\t\t\t<i class=\"icon-user\"></i>\n            <a class=\"parent_link\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user")),"username"), env.opts.autoescape);
output += "</a>\n            <small>scheduler</small>\n\t\t</li>\n\t\t";
;
}
output += "\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user_co")) {
output += "\n\t\t<li>\n\t\t\t<i class=\"icon-user\"></i>\n            <a class=\"parent_link\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user_co")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user_co")),"username"), env.opts.autoescape);
output += "</a>\n            <small>creator</small>\n\t\t</li>\n\t\t";
;
}
output += "\n\t</ul>\n</section>\n\n<section class=\"description\">\n\n\n    <!--\n\t<p>";
output += runtime.suppressValue(env.getFilter("linebreaksbr").call(context, env.getFilter("shorten").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description_html"),200)), env.opts.autoescape);
output += "</p>\n    -->\n    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description")) {
output += "\n\t<div class=\"description markdown-remove\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description_html"), env.opts.autoescape);
output += "</div>\n    ";
;
}
output += "\n\t<!--\n\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"absolute_url"), env.opts.autoescape);
output += "\" class=\"pull-left\">> Read more</a>\n\t-->\n\n\t<ul class=\"unstyled object-links\">\n\t\t<li>\n\t\t\t<a class=\"parent_link\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">&gt; Emission details</a>\n\t\t</li>\n        <!--\n\t\t<li>\n\t\t\t<a  class=\"parent_link\"href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"absolute_url"), env.opts.autoescape);
output += "\">&gt; Content details</a>\n\t\t</li>\n\t\t-->\n\t</ul>\n\n</section>\n\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["aplayer/nj/popup_information_abcast.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<ul class=\"unstyled\">\n    <li>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"), env.opts.autoescape);
output += "</li>\n    <li>";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"name"), env.opts.autoescape);
output += "</li>\n    <li>";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"name"), env.opts.autoescape);
output += "</li>\n</ul>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["aplayer/nj/popup_screen.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"row-fluid aplayer-information ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"source"), env.opts.autoescape);
output += "\">\n    <div class=\"span8 information\">\n        <div class=\"padded-x padded-y\">\n\n\n            <h1><a class=\"parent_link\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"),30), env.opts.autoescape);
output += "</a></h1>\n\n            <span><a class=\"parent_link\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"absolute_url"), env.opts.autoescape);
output += "\">\n                ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"name"),30), env.opts.autoescape);
output += "</a></span>\n\n            <br>\n\n            <span>\n                <a class=\"parent_link\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"absolute_url"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"name"),30), env.opts.autoescape);
output += "</a>\n\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"releasedate")) {
output += "\n                    <small> ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"releasedate"), env.opts.autoescape);
output += "</small>\n                ";
;
}
output += "\n\n            </span>\n\n\n        </div>\n    </div>\n\n    <div class=\"span4 image\">\n        <div class=\"padded-x padded-y\">\n\n            ";
frame = frame.push();
var t_3 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"images");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("image", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n                <img class=\" pull-right\" id=\"\" src=\"";
output += runtime.suppressValue(t_4, env.opts.autoescape);
output += "\">\n            ";
;
}
}
frame = frame.pop();
output += "\n\n        </div>\n    </div>\n\n</div>\n\n<div class=\"row-fluid aplayer-progress\" id=\"progress_bar\">\n\n\n    <!-- main wrapper -->\n    <div class=\"indicator playhead hoverable\">\n\n        <!-- background layer (for hover/active/etc ? ) -->\n        <div class=\"background\">\n\n            <!-- holder for indicator (animated transparent png-24 bg.image) -->\n            <div class=\"indicator\">\n\n                <!-- holder for handler (animated transparent png-24 bg.image) -->\n                <div class=\"handler\">\n\n                    <!-- actual waveform (transparent inner) -->\n                    <div class=\"waveform\">\n\n                        <img data-href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"waveform_image"), env.opts.autoescape);
output += "\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"waveform_image"), env.opts.autoescape);
output += "\"\n                             style=\"width: 100%; height: 100%\"/></img>\n\n                    </div>\n\n                </div>\n\n            </div>\n\n        </div>\n\n        <div class=\"clear\"></div>\n    </div>\n\n    <div class=\"row-fluid aplayer-controls\">\n\n        <p>\n                <span class=\"prev\">\n                    <a href=\"#prev\" title=\"Previous\"> <i class=\"icon-step-backward\"></i> </a>\n                </span>\n\n                <span class=\"\">\n                    <a href=\"#pause\" title=\"Stop\"> <i class=\"icon-pause\"></i> </a>\n                </span>\n\n                <!--\n                <span class=\"hidden-while-paused\">\n                    <a href=\"#pause\" title=\"Stop\"> <i class=\"icon-pause\"></i> </a>\n                </span>\n\n                <span class=\"hidden-while-playing hidden-while-buffering\">\n                    <a href=\"#play\" title=\"Play\"> <i class=\"icon-play\"></i> </a>\n                </span>\n                -->\n\n                <span class=\"next\">\n                    <a href=\"#next\" title=\"Next\"> <i class=\"icon-step-forward\"></i> </a>\n                </span>\n        </p>\n\n        <!--\n        <div class=\"span6\">\n            <ul class=\"horizontal unstyled\">\n\n                <li class=\"prev\">\n                    <a href=\"#prev\" title=\"Previous\"> <i class=\"icon-step-backward\"></i> </a>\n                </li>\n\n                <li class=\"hidden-while-paused\">\n                    <a href=\"#pause\" title=\"Stop\"> <i class=\"icon-pause\"></i> </a>\n                </li>\n                <li class=\"hidden-while-playing hidden-while-buffering\">\n                    <a href=\"#play\" title=\"Play\"> <i class=\"icon-play\"></i> </a>\n                </li>\n\n                <li class=\"next\">\n                    <a href=\"#next\" title=\"Next\"> <i class=\"icon-step-forward\"></i> </a>\n                </li>\n\n            </ul>\n        </div>\n        -->\n\n\n    </div>\n\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["importer/nj/__orig__importfile.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\" class=\"importfile item ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status"), env.opts.autoescape);
output += "\">\n\n<h3>\n    <!--\n\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\n\t\t-->\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "init") {
output += "\n        <i class=\"icon-time icon-spin\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "done") {
output += "\n        <i class=\"icon-ok-sign\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready") {
output += "\n        <i class=\"icon-thumbs-up\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "working") {
output += "\n        <i class=\"icon-spinner icon-spin\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n        <i class=\"icon-thumbs-down\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "duplicate") {
output += "\n        <i class=\"icon-copy\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "queued") {
output += "\n        <i class=\"icon-spinner icon-spin\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "importing") {
output += "\n        <i class=\"icon-asterisk icon-spin\"></i>\n    ";
;
}
output += "\n\n\n    ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"filename"), env.opts.autoescape);
output += "\n    <small><!--[";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"mimetype"), env.opts.autoescape);
output += "]--> (debug: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ")</small>\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "duplicate") {
output += "<span class=\"warning pull-right\">Duplicate</span>";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"error")) {
output += "<span class=\"warning pull-right\">Error: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"error"), env.opts.autoescape);
output += "</span>";
;
}
output += "\n\n</h3>\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "working") {
output += "\n    <div class=\"row-fluid status status-working provider-tag\">\n\n        <div class=\"span1\">\n            <i class=\"icon icon-padded icon-id3\"></i>\n        </div>\n\n        <div class=\"span4\">\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n            <div class=\"clearfix\"></div>\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n        </div>\n\n        <div class=\"span4\">\n\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n            <div class=\"clearfix\"></div>\n\n        </div>\n\n        <div class=\"span3\">\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_tracknumber"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media_tracknumber")),"media_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n            <div class=\"clearfix\"></div>\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_date"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_date"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n\n        </div>\n\n\n    </div>\n    <div class=\"row-fluid status\">\n        <div class=\"progress\">\n            <div class=\"bar bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\" style=\"width: 0%;\"></div>\n        </div>\n\n\n        <script>\n\n            var progress";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += " = setInterval(function () {\n                var $bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += " = $('.bar.bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "');\n                if ($bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width() > 770) {\n                    clearInterval(progress";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ");\n                    //$('.progress').removeClass('active');\n                } else {\n                    $bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width($bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width() + 10);\n                }\n            }, 80);\n\n        </script>\n\n    </div>\n";
;
}
output += "\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "queued") {
output += "\n    <div class=\"row-fluid status status-queue\">\n\n        <div class=\"span1 icon-holder\">&nbsp;</div>\n\n        <div class=\"span8 information\">\n\n            <!--<h4>Importing <i class=\"icon icon-padded icon-cogs\"></i></h4>-->\n            <p>File placed in the import-queue.<br/>Please be patient for a while.</p>\n\n            <!--\n            <p>Depending on server-load and available metadata it can take several minutes per track to complete it's\n                information.</p>\n            -->\n        </div>\n\n        <div class=\"span3 image\">\n            <div class=\"pull-right\">\n                <!--\n                <i class=\"ajax-loader c3CA3B9\"></i>\n                -->\n            </div>\n        </div>\n\n\n    </div>\n    <div class=\"row-fluid status\">\n        <div class=\"progress\">\n            <div class=\"bar\" style=\"width: 0%;\"></div>\n        </div>\n\n\n        <script>\n\n            var progress";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += " = setInterval(function () {\n                var $bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += " = $('.bar.bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "');\n                if ($bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width() > 770) {\n                    clearInterval(progress";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ");\n                    //$('.progress').removeClass('active');\n                } else {\n                    $bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width($bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width() + 10);\n                }\n            }, 80);\n\n        </script>\n\n    </div>\n";
;
}
output += "\n\n\n\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "duplicate") {
output += "\n    <div class=\"row-fluid result-set status-duplicate\">\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")) {
output += "\n            <div class=\"span1\">\n                <i class=\"icon icon-padded icon-obp\"></i>\n            </div>\n\n            <div class=\"span8 information\">\n\n                <ul class=\"unstyled\">\n                    <li><strong><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"name"), env.opts.autoescape);
output += "</a>\n                        ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name")) {
output += " by\n                            <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name"), env.opts.autoescape);
output += "</a>";
;
}
output += "\n                    </strong></li>\n\n                    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name")) {
output += "\n                        <li><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name"), env.opts.autoescape);
output += "</a></li>\n                    ";
;
}
else {
output += "\n                        <li>No Release</li>\n                    ";
;
}
output += "\n\n                    <li class=\"small\">";
output += runtime.suppressValue(env.getFilter("format_timestamp").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"created")), env.opts.autoescape);
output += "</li>\n\n                </ul>\n\n            </div>\n\n            <div class=\"span3 image\">\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release") && runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image")) {
output += "\n                    <img class=\"pull-right\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image"), env.opts.autoescape);
output += "\"/>\n                ";
;
}
else {
output += "\n                    <img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\"/>\n                ";
;
}
output += "\n            </div>\n        ";
;
}
output += "\n\n    </div>\n";
;
}
output += "\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "done") {
output += "\n    <div class=\"row-fluid result-set status-done\">\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")) {
output += "\n            <div class=\"span1\">\n                <i class=\"icon icon-padded icon-obp\"></i>\n            </div>\n\n            <div class=\"span8 information\">\n\n                <ul class=\"unstyled\">\n                    <li><strong><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"name"), env.opts.autoescape);
output += "</a>\n                        ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name")) {
output += " by\n                            <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name"), env.opts.autoescape);
output += "</a>";
;
}
output += "\n                    </strong></li>\n\n                    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name")) {
output += "\n                        <li><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"absolute_url"), env.opts.autoescape);
output += "\">\n                            ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name"),50), env.opts.autoescape);
output += "</a></li>\n                    ";
;
}
else {
output += "\n                        <li>No Release</li>\n                    ";
;
}
output += "\n\n                    <li class=\"small\">";
output += runtime.suppressValue(env.getFilter("format_timestamp").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"created")), env.opts.autoescape);
output += "</li>\n\n                </ul>\n\n            </div>\n\n            <div class=\"span3 image\">\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release") && runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image")) {
output += "\n                    <img class=\"pull-right\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image"), env.opts.autoescape);
output += "\"/>\n                ";
;
}
else {
output += "\n                    <img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\"/>\n                ";
;
}
output += "\n            </div>\n        ";
;
}
output += "\n\n    </div>\n";
;
}
output += "\n\n\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n\n\n\n    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz")),"length") > 0) {
output += "\n        <div class=\"hint\">\n            <p>File Metadata</p>\n        </div>\n    ";
;
}
output += "\n\n    <div class=\"row-fluid result-set hoverable provider-tag\">\n\n        <div class=\"span1\">\n            <i class=\"icon icon-padded icon-id3\"></i>\n        </div>\n\n        <div class=\"span4\">\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"key\">Title</li>\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n            <div class=\"clearfix\"></div>\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"key\">Release</li>\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n        </div>\n\n        <div class=\"span4\">\n\n            <label class=\"checkbox holder-artist_name\">\n                <input type=\"checkbox\">\n                <ul class=\"horizontal unstyled\">\n                    <li class=\"key\">\n                        Artist\n                    </li>\n                    <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"), env.opts.autoescape);
output += "\">\n                        ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"),38), env.opts.autoescape);
output += "</li>\n                </ul>\n            </label>\n\n            <div class=\"clearfix\"></div>\n\n            <label class=\"checkbox holder-label_name\">\n                <input type=\"checkbox\">\n                <ul class=\"horizontal unstyled\">\n                    <li class=\"key\">\n                        Label\n                    </li>\n                    <li class=\"value\"></li>\n                </ul>\n            </label>\n\n        </div>\n\n        <div class=\"span3\">\n\n            <label class=\"checkbox holder-media_tracknumber\">\n                <input type=\"checkbox\">\n                <ul class=\"horizontal unstyled\">\n                    <li class=\"key\">\n                        TrackNo\n                    </li>\n                    <li class=\"value\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_tracknumber"), env.opts.autoescape);
output += "</li>\n                </ul>\n            </label>\n\n            <div class=\"clearfix\"></div>\n\n            <label class=\"checkbox holder-release_date\">\n                <input type=\"checkbox\">\n                <ul class=\"horizontal unstyled\">\n                    <li class=\"key\">\n                        Date\n                    </li>\n                    <li class=\"value\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_date"), env.opts.autoescape);
output += "</li>\n                </ul>\n            </label>\n\n        </div>\n\n    </div>\n";
;
}
output += "\n\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n\n    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz")),"length") > 0) {
output += "\n        <div class=\"hint\">\n            <p>Possible Releases found on musicbrainz.org. </p>\n        </div>\n    ";
;
}
output += "\n\n    <div class=\"musicbrainz-tag-holder\">\n\n\n\n        ";
frame = frame.push();
var t_3 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n            <div class=\"row-fluid result-set hoverable musicbrainz-tag mb_id-";
output += runtime.suppressValue(runtime.memberLookup((t_4),"mb_id"), env.opts.autoescape);
output += "\">\n\n                <div class=\"span1\">\n                    <i class=\"icon icon-padded icon-musicbrainz\"></i>\n                </div>\n\n                <div class=\"span8\">\n\n                    <!-- ids -->\n                    <input type=\"hidden\" class=\"media-id\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"media")),"mb_id"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"release-id\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"mb_id"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"artist-id\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"artist")),"mb_id"), env.opts.autoescape);
output += "\">\n\n                    <!-- other data -->\n                    <input type=\"hidden\" class=\"releasedate\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"releasedate"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"catalognumber\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"label")),"catalognumber"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"name\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"media")),"name"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"artist\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"artist")),"name"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"release\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += "\">\n\n                    <h5>\n                        <a href=\"http://musicbrainz.org/recording/";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"media")),"mb_id"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"media")),"name"), env.opts.autoescape);
output += "</a>\n                        by\n                        <a href=\"http://musicbrainz.org/artist/";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"artist")),"mb_id"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"artist")),"name"), env.opts.autoescape);
output += "</a>\n                    </h5>\n\n                    <a class=\"external\" href=\"http://musicbrainz.org/release/";
output += runtime.suppressValue(runtime.memberLookup((t_4),"mb_id"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += "</a>\n                    <ul class=\"unstyled\">\n                        <li class=\"small\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"country"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"releasedate"), env.opts.autoescape);
output += " | ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"status"), env.opts.autoescape);
output += "</li>\n                        <li class=\"small\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"label")),"name"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"catalognumber"), env.opts.autoescape);
output += "</li>\n                    </ul>\n\n                </div>\n\n                <div class=\"span3\">\n                    ";
if(runtime.memberLookup((runtime.memberLookup((t_4),"relations")),"discogs_image")) {
output += "\n                        <img class=\"pull-right\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"relations")),"discogs_image"), env.opts.autoescape);
output += "\"/>\n                    ";
;
}
else {
output += "\n                        <img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\"/>\n                    ";
;
}
output += "\n                </div>\n            </div>\n\n\n        ";
;
}
}
frame = frame.pop();
output += "\n\n\n    </div>\n";
;
}
output += "\n\n\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n    <div class=\"pull-righ result-actions\">\n\n    <form class=\"form-horizontal form-result\">\n    <h4>Result</h4>\n\n    <!-- name -->\n    <div class=\"row-fluid base media ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"name")) {
output += "missing";
;
}
output += "\">\n\n        <div class=\"span6\">\n\n            <div class=\"control-group\">\n                <label class=\"control-label\" for=\"inputEmail\">Title <span class=\"required\">*</span></label>\n\n                <div class=\"controls\">\n                    <input type=\"text\" class=\"release autoupdate\" data-ct=\"media\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"name"), env.opts.autoescape);
output += "\">\n                </div>\n            </div>\n\n        </div>\n\n\n    </div>\n\n    <!-- release -->\n    <div class=\"row-fluid base release ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"release")) {
output += "missing";
;
}
output += "\">\n\n        <div class=\"span5\">\n\n            <div class=\"control-group\">\n                <label class=\"control-label\" for=\"inputEmail\">Release <span class=\"required\">*</span></label>\n\n                <div class=\"controls\">\n                    <input type=\"text\"\n                           class=\"release autocomplete\"\n                           data-ct=\"release\"\n                           value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"release"), env.opts.autoescape);
output += "\">\n\n                    <div class=\"ac-result\"></div>\n                </div>\n            </div>\n\n        </div>\n\n        <div class=\"span3\">\n            ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id") && !runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_release")) {
output += "\n                <a href=\"#\"\n                   data-ct=\"release\"\n                   data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_resource_uri"), env.opts.autoescape);
output += "\"\n                   class=\"tooltip-inline\">\n                    <i class=\"icon-paper-clip\"></i>\n                    Assigned\n                </a>\n            ";
;
}
else {
output += "\n                <span class=\"dim\"><i class=\"icon-plus\"></i> Create</span>\n            ";
;
}
output += "\n        </div>\n\n        <div class=\"span2\">\n            ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id")) {
output += "\n                <input type=\"checkbox\"\n                       class=\"force-creation\"\n                       ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_release")) {
output += "checked=\"checked\"";
;
}
output += "/>\n                Force Creation<a class=\"tooltipable\"\n                                 data-title=\"Enable this to force the creation of a new entry - even if there is already an item with the same name.\"><i\n                    class=\"icon-question-sign\"></i></a>\n            ";
;
}
else {
output += "\n                &nbsp;\n            ";
;
}
output += "\n        </div>\n\n        <div class=\"span2\">\n            <a class=\"btn btn-mini pull-right apply-to-all\" data-ct=\"release\"><i class=\"icon-repeat\"></i> Apply Release\n                to all</a>\n        </div>\n\n\n    </div>\n\n    <!-- artist -->\n    <div class=\"row-fluid base artist ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"artist")) {
output += "missing";
;
}
output += "\">\n\n        <div class=\"span5\">\n\n            <div class=\"control-group\">\n                <label class=\"control-label\" for=\"inputEmail\">Artist <span class=\"required\">*</span></label>\n\n                <div class=\"controls\">\n                    <input type=\"text\"\n                           class=\"artist autocomplete\"\n                           data-ct=\"artist\"\n                           value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"artist"), env.opts.autoescape);
output += "\">\n\n                    <div class=\"ac-result\"></div>\n                </div>\n            </div>\n\n        </div>\n\n        <div class=\"span3\">\n            ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id") && !runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_artist")) {
output += "\n                <a href=\"#\"\n                   data-ct=\"artist\"\n                   data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_resource_uri"), env.opts.autoescape);
output += "\"\n                   class=\"tooltip-inline\">\n                    <i class=\"icon-paper-clip\"></i>\n                    Assigned\n                </a>\n            ";
;
}
else {
output += "\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_matches")) {
output += "\n                    <a href=\"#\" class=\"matches\"><i class=\"icon-warning-sign\"></i> ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_matches"), env.opts.autoescape);
output += " matches</a>\n                ";
;
}
output += "\n                <span class=\"dim\"><i class=\"icon-plus\"></i> Create</span>\n            ";
;
}
output += "\n        </div>\n\n        <div class=\"span2\">\n            ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id")) {
output += "\n                <input type=\"checkbox\"\n                       class=\"force-creation\"\n                       ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_artist")) {
output += "checked=\"checked\"";
;
}
output += "/>\n                Force Creation<a class=\"tooltipable\"\n                                 data-title=\"Enable this to force the creation of a new entry - even if there is already an item with the same name.\"><i\n                    class=\"icon-question-sign\"></i></a>\n            ";
;
}
else {
output += "\n                &nbsp;\n            ";
;
}
output += "\n        </div>\n\n        <div class=\"span2\">\n            <a class=\"btn btn-mini pull-right apply-to-all\" data-ct=\"artist\"><i class=\"icon-repeat\"></i> Apply Artist to\n                all</a>\n        </div>\n\n\n    </div>\n\n\n    <!--\n\t\t\t<div class=\"row-fluid base\">\n\n\t\t\t\t<div class=\"span6\">\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Title</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"name\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"name"), env.opts.autoescape);
output += "\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Release</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"release\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"release"), env.opts.autoescape);
output += "\">\n\t\t\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id")) {
output += "\n\t\t\t\t\t\t\t\t<i class=\"icon-magic\"></i>\n\t\t\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id"), env.opts.autoescape);
output += "\n\t\t\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_resource_uri"), env.opts.autoescape);
output += "\n\t\t\t\t\t\t\t";
;
}
output += "\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Release Date</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"releasedate\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"releasedate"), env.opts.autoescape);
output += "\">\n\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\n\t\t\t\t<div class=\"span5\">\n\t\t\t\t\t\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputPassword\">Artist</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"artist\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"artist"), env.opts.autoescape);
output += "\">\n\t\t\t\t\t\t\t";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id")) {
output += "\n\t\t\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id"), env.opts.autoescape);
output += "\n\t\t\t\t\t\t\t";
;
}
output += "\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Track Number</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"tracknumber\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"tracknumber"), env.opts.autoescape);
output += "\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Label</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" id=\"inputEmail\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"label"), env.opts.autoescape);
output += "\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\n\t\t\t</div>\n\t\t\t-->\n\n\n\n    <!--\n    <div class=\"toggle\">\n        <div class=\"row-fluid\">\n            <div class=\"span12\">\n                <a class=\"toggle-advanced pull-right\">More&nbsp;<i class=\"icon-angle-down\"></i></a>\n            </div>\n        </div>\n\n    </div>\n\n    <div class=\"advanced-fields\">\n\n        <h4>Musicbrainz IDs</h4>\n\n        <div class=\"row-fluid musicbrainz\">\n\n            <div class=\"span6\">\n\n                <div class=\"control-group\">\n                    <label class=\"control-label\" for=\"inputEmail\">Track ID</label>\n\n                    <div class=\"controls\">\n                        <input type=\"text\"\n                               class=\"mb-track-id input-minitext\"\n                               value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"mb_track_id"), env.opts.autoescape);
output += "\"\n                               readonly=\"readonly\">\n                    </div>\n                </div>\n\n                <div class=\"control-group\">\n                    <label class=\"control-label\" for=\"inputEmail\">Artist ID</label>\n\n                    <div class=\"controls\">\n                        <input type=\"text\"\n                               class=\"mb-artist-id input-minitext\"\n                               value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"mb_artist_id"), env.opts.autoescape);
output += "\"\n                               readonly=\"readonly\">\n                    </div>\n                </div>\n\n            </div>\n\n            <div class=\"span5\">\n\n                <div class=\"control-group\">\n                    <label class=\"control-label\" for=\"inputPassword\">Release ID</label>\n\n                    <div class=\"controls\">\n                        <input type=\"text\"\n                               class=\"mb-release-id input-minitext\"\n                               value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"mb_release_id"), env.opts.autoescape);
output += "\"\n                               readonly=\"readonly\">\n                    </div>\n                </div>\n\n            </div>\n\n        </div>\n\n\n    </div>\n    -->\n\n    </form>\n\n    </div>\n\n    <div class=\"row-fluid pull-righ result-actions\">\n\n        <div class=\"span2\">\n            &nbsp;\n        </div>\n\n        <div class=\"pull-right span10\">\n            <a class=\"btn btn-secondary btn-small delete-importfile\">Delete this File</a>\n            <!--\n            <a class=\"btn btn-secondary btn-small rescan\" data-settings=\"skip_tracknumber\">Scan witouth tracknumber</a>\n            -->\n            <a class=\"btn btn-secondary btn-small rescan\">Scan again</a>\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n                <a class=\"btn btn-primary btn-small start-import\">Start Import</a>\n            ";
;
}
output += "\n        </div>\n    </div>\n\n\n";
;
}
output += "\n\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["importer/nj/autocomplete.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"result\">\n\n\t<div class=\"listing\">\n\t\t";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\t\t<div class=\"item hoverable\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"id"), env.opts.autoescape);
output += "\" data-name=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += "\" data-ct=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"ct"), env.opts.autoescape);
output += "\">\n\t\t\t\n\t\t\t<div class=\"row-fluid\">\n\t\t\t\t\n\t\t\t\t<div class=\"span3\">\n\t\t\t\t\t\n\t\t\t\t\t";
if(runtime.memberLookup((t_4),"main_image")) {
output += "\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\" />\n\t\t\t\t\t";
;
}
else {
output += "\n\t\t\t\t\t<img src=\"/static/img/base/defaults/listview.";
output += runtime.suppressValue(runtime.memberLookup((t_4),"ct"), env.opts.autoescape);
output += ".xl.png\" width=\"90\" height=\"90\" />\n\t\t\t\t\t";
;
}
output += "\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span9\">\n\t\t\t\t\t\n\t\t\t\t\t<ul class=\"unstyled\">\n\t\t\t\t\t\t<li><strong>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, runtime.memberLookup((t_4),"name"),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</strong>  <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"releasedate"), env.opts.autoescape);
output += "</small></li>\n\t\t\t\t\t\t\n\t\t\t\t\t\t";
if(runtime.memberLookup((t_4),"ct") == "release") {
output += "\n\t\t\t\t\t\t<li>";
frame = frame.push();
var t_7 = runtime.memberLookup((t_4),"artist");
if(t_7) {var t_6 = t_7.length;
for(var t_5=0; t_5 < t_7.length; t_5++) {
var t_8 = t_7[t_5];
frame.set("artist", t_8);
frame.set("loop.index", t_5 + 1);
frame.set("loop.index0", t_5);
frame.set("loop.revindex", t_6 - t_5);
frame.set("loop.revindex0", t_6 - t_5 - 1);
frame.set("loop.first", t_5 === 0);
frame.set("loop.last", t_5 === t_6 - 1);
frame.set("loop.length", t_6);
output += runtime.suppressValue(t_8, env.opts.autoescape);
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last")) {
output += ", ";
;
}
;
}
}
frame = frame.pop();
output += "</li>\n\t\t\t\t\t\t<li>Tracks: ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"media_count"), env.opts.autoescape);
output += "</li>\n\t\t\t\t\t\t";
;
}
output += "\n\t\t\t\t\t\t\n\t\t\t\t\t</ul>\n\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\n\t\t</div>\n\t\t";
;
}
}
frame = frame.pop();
output += "\n\t</div>\n</div>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["importer/nj/importfile.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\" class=\"importfile item ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status"), env.opts.autoescape);
output += "\" xmlns=\"http://www.w3.org/1999/html\">\n\n<h3>\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "init") {
output += "\n        <i class=\"icon-time icon-spin\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "done") {
output += "\n        <i class=\"icon-ok-sign\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready") {
output += "\n        <i class=\"icon-thumbs-up\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "working") {
output += "\n        <i class=\"icon-spinner icon-spin\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n        <i class=\"icon-thumbs-down\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "duplicate") {
output += "\n        <i class=\"icon-copy\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "queued") {
output += "\n        <i class=\"icon-spinner icon-spin\"></i>\n    ";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "importing") {
output += "\n        <i class=\"icon-asterisk icon-spin\"></i>\n    ";
;
}
output += "\n\n\n    ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"filename"), env.opts.autoescape);
output += "\n    <small><!--[";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"mimetype"), env.opts.autoescape);
output += "]--> (debug: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ")</small>\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "duplicate") {
output += "<span class=\"warning pull-right\">Duplicate</span>";
;
}
output += "\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"error")) {
output += "<span class=\"warning pull-right\">Error: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"error"), env.opts.autoescape);
output += "</span>";
;
}
output += "\n\n</h3>\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "working") {
output += "\n    <div class=\"row-fluid status status-working provider-tag\">\n\n        <div class=\"span1\">\n            <!--<i class=\"icon icon-large icon-large icon-ok\"></i>-->\n        </div>\n\n        <div class=\"span4\">\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n            <div class=\"clearfix\"></div>\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n        </div>\n\n        <div class=\"span4\">\n\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n            <div class=\"clearfix\"></div>\n\n        </div>\n\n        <div class=\"span3\">\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_tracknumber"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media_tracknumber")),"media_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n            <div class=\"clearfix\"></div>\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_date"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_date"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n\n        </div>\n\n\n    </div>\n    <div class=\"row-fluid status\">\n        <div class=\"progress\">\n            <div class=\"bar bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "\" style=\"width: 0%;\"></div>\n        </div>\n\n\n        <script>\n\n            var progress";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += " = setInterval(function () {\n                var $bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += " = $('.bar.bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "');\n                if ($bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width() > 770) {\n                    clearInterval(progress";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ");\n                    //$('.progress').removeClass('active');\n                } else {\n                    $bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width($bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width() + 10);\n                }\n            }, 80);\n\n        </script>\n\n    </div>\n";
;
}
output += "\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "queued") {
output += "\n    <div class=\"row-fluid status status-queue\">\n\n        <div class=\"span1 icon-holder\">&nbsp;</div>\n\n        <div class=\"span8 information\">\n            \n            <p>File placed in the import-queue.<br/>Please be patient for a while.</p>\n\n            <!--\n            <p>Depending on server-load and available metadata it can take several minutes per track to complete it's\n                information.</p>\n            -->\n        </div>\n\n        <div class=\"span3 image\">\n            <div class=\"pull-right\">\n                <!--\n                <i class=\"ajax-loader c3CA3B9\"></i>\n                -->\n            </div>\n        </div>\n\n\n    </div>\n    <div class=\"row-fluid status\">\n        <div class=\"progress\">\n            <div class=\"bar\" style=\"width: 0%;\"></div>\n        </div>\n\n\n        <script>\n\n            var progress";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += " = setInterval(function () {\n                var $bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += " = $('.bar.bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "');\n                if ($bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width() > 770) {\n                    clearInterval(progress";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ");\n                    //$('.progress').removeClass('active');\n                } else {\n                    $bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width($bar";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += ".width() + 10);\n                }\n            }, 80);\n\n        </script>\n\n    </div>\n";
;
}
output += "\n\n\n\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "duplicate") {
output += "\n    <div class=\"row-fluid result-set status-duplicate\">\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")) {
output += "\n            <div class=\"span1\">\n                <i class=\"icon icon-large icon-obp\"></i>\n            </div>\n\n            <div class=\"span8 information\">\n\n                <ul class=\"unstyled\">\n                    <li><strong><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"name"), env.opts.autoescape);
output += "</a>\n                        ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name")) {
output += " by\n                            <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name"), env.opts.autoescape);
output += "</a>";
;
}
output += "\n                    </strong></li>\n\n                    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name")) {
output += "\n                        <li><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name"), env.opts.autoescape);
output += "</a></li>\n                    ";
;
}
else {
output += "\n                        <li>No Release</li>\n                    ";
;
}
output += "\n\n                    <li class=\"small\">";
output += runtime.suppressValue(env.getFilter("format_timestamp").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"created")), env.opts.autoescape);
output += "</li>\n\n                </ul>\n\n            </div>\n\n            <div class=\"span3 image\">\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release") && runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image")) {
output += "\n                    <img class=\"pull-right\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image"), env.opts.autoescape);
output += "\"/>\n                ";
;
}
else {
output += "\n                    <img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\"/>\n                ";
;
}
output += "\n            </div>\n        ";
;
}
output += "\n\n    </div>\n";
;
}
output += "\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "done") {
output += "\n    <div class=\"row-fluid result-set status-done\">\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")) {
output += "\n            <div class=\"span1\">\n                <i class=\"icon icon-large icon-obp\"></i>\n            </div>\n\n            <div class=\"span8 information\">\n\n                <ul class=\"unstyled\">\n                    <li><strong><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"name"), env.opts.autoescape);
output += "</a>\n                        ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name")) {
output += " by\n                            <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name"), env.opts.autoescape);
output += "</a>";
;
}
output += "\n                    </strong></li>\n\n                    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name")) {
output += "\n                        <li><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"absolute_url"), env.opts.autoescape);
output += "\">\n                            ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name"),50), env.opts.autoescape);
output += "</a></li>\n                    ";
;
}
else {
output += "\n                        <li>No Release</li>\n                    ";
;
}
output += "\n\n                    <li class=\"small\">";
output += runtime.suppressValue(env.getFilter("format_timestamp").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"created")), env.opts.autoescape);
output += "</li>\n\n                </ul>\n\n            </div>\n\n            <div class=\"span3 image\">\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release") && runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image")) {
output += "\n                    <img class=\"pull-right\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image"), env.opts.autoescape);
output += "\"/>\n                ";
;
}
else {
output += "\n                    <img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\"/>\n                ";
;
}
output += "\n            </div>\n        ";
;
}
output += "\n\n    </div>\n";
;
}
output += "\n\n\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n\n    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz")),"length") > 0) {
output += "\n        <div class=\"hint\">\n            <p>\n                <em>File Metadata</em> <a class=\"toggle-hint\" href=\"#\"><i class=\"icon-question-sign\"></i></a><br>\n                Information extracted from your uploaded file.<br>\n                Choose this entry if you want to continue with the bare file metadata.\n            </p>\n            <div class=\"expandable\">\n                <p>(( More to read here soon. ))</p>\n            </div>\n        </div>\n    ";
;
}
output += "\n\n    <div class=\"row-fluid result-set hoverable provider-tag\">\n\n        <div class=\"span1\">\n            <i class=\"icon icon-large icon-ok\"></i>\n        </div>\n\n        <div class=\"span4\">\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"key\">Title</li>\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n            <div class=\"clearfix\"></div>\n\n            <ul class=\"horizontal unstyled\">\n                <li class=\"key\">Release</li>\n                <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"),38), env.opts.autoescape);
output += "</li>\n            </ul>\n\n        </div>\n\n        <div class=\"span4\">\n\n            <label class=\"checkbox holder-artist_name\">\n                <input type=\"checkbox\">\n                <ul class=\"horizontal unstyled\">\n                    <li class=\"key\">\n                        Artist\n                    </li>\n                    <li class=\"value\" title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"), env.opts.autoescape);
output += "\">\n                        ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"),38), env.opts.autoescape);
output += "</li>\n                </ul>\n            </label>\n\n            <div class=\"clearfix\"></div>\n\n            <label class=\"checkbox holder-label_name\">\n                <input type=\"checkbox\">\n                <ul class=\"horizontal unstyled\">\n                    <li class=\"key\">\n                        Label\n                    </li>\n                    <li class=\"value\"></li>\n                </ul>\n            </label>\n\n        </div>\n\n        <div class=\"span3\">\n\n            <label class=\"checkbox holder-media_tracknumber\">\n                <input type=\"checkbox\">\n                <ul class=\"horizontal unstyled\">\n                    <li class=\"key\">\n                        TrackNo\n                    </li>\n                    <li class=\"value\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_tracknumber"), env.opts.autoescape);
output += "</li>\n                </ul>\n            </label>\n\n            <div class=\"clearfix\"></div>\n\n            <label class=\"checkbox holder-release_date\">\n                <input type=\"checkbox\">\n                <ul class=\"horizontal unstyled\">\n                    <li class=\"key\">\n                        Date\n                    </li>\n                    <li class=\"value\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_date"), env.opts.autoescape);
output += "</li>\n                </ul>\n            </label>\n\n        </div>\n\n    </div>\n";
;
}
output += "\n\n\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n\n    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz")),"length") > 0) {
output += "\n        <div class=\"hint\">\n            <p>\n                <em>Possible Releases</em> <a class=\"toggle-hint\" href=\"#\"><i class=\"icon-question-sign\"></i></a><br>\n                Information found in our linked databases.<br>\n                Select the most appropriate result to automatically complete the metadata.\n            </p>\n            <div class=\"expandable\">\n                <p>(( More to read here soon. ))</p>\n            </div>\n        </div>\n    ";
;
}
output += "\n\n    <div class=\"musicbrainz-tag-holder\">\n\n\n\n        ";
frame = frame.push();
var t_3 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\n            <div class=\"row-fluid result-set hoverable musicbrainz-tag mb_id-";
output += runtime.suppressValue(runtime.memberLookup((t_4),"mb_id"), env.opts.autoescape);
output += "\">\n\n                <div class=\"span1\">\n                    <i class=\"icon icon-large icon-ok\"></i>\n                </div>\n\n                <div class=\"span8\">\n\n                    <!-- ids -->\n                    <input type=\"hidden\" class=\"media-id\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"media")),"mb_id"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"release-id\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"mb_id"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"artist-id\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"artist")),"mb_id"), env.opts.autoescape);
output += "\">\n\n                    <!-- other data -->\n                    <input type=\"hidden\" class=\"releasedate\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"releasedate"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"catalognumber\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"label")),"catalognumber"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"name\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"media")),"name"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"artist\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"artist")),"name"), env.opts.autoescape);
output += "\">\n                    <input type=\"hidden\" class=\"release\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += "\">\n\n                    <h5>\n                        <a href=\"http://musicbrainz.org/recording/";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"media")),"mb_id"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"media")),"name"), env.opts.autoescape);
output += "</a>\n                        by\n                        <a href=\"http://musicbrainz.org/artist/";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"artist")),"mb_id"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"artist")),"name"), env.opts.autoescape);
output += "</a>\n                    </h5>\n\n                    <a class=\"external\" href=\"http://musicbrainz.org/release/";
output += runtime.suppressValue(runtime.memberLookup((t_4),"mb_id"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += "</a>\n                    <ul class=\"unstyled\">\n                        <li class=\"small\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"country"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"releasedate"), env.opts.autoescape);
output += " | ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"status"), env.opts.autoescape);
output += "</li>\n                        <li class=\"small\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"label")),"name"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(runtime.memberLookup((t_4),"catalognumber"), env.opts.autoescape);
output += "</li>\n                    </ul>\n\n                </div>\n\n                <div class=\"span3\">\n                    ";
if(runtime.memberLookup((runtime.memberLookup((t_4),"relations")),"discogs_image")) {
output += "\n                        <img class=\"pull-right\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((t_4),"relations")),"discogs_image"), env.opts.autoescape);
output += "\"/>\n                    ";
;
}
else {
output += "\n                        <img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\"/>\n                    ";
;
}
output += "\n                </div>\n            </div>\n\n        ";
;
}
}
frame = frame.pop();
output += "\n\n    </div>\n";
;
}
output += "\n\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n    <div class=\"pull-righ result-actions\">\n\n    <form class=\"form-horizontal form-result\">\n\n        <div class=\"hint\">\n            <p>\n                <em>Selected Information</em> <a class=\"toggle-hint\" href=\"#\"><i class=\"icon-question-sign\"></i></a>\n            </p>\n            <div class=\"expandable\">\n                <p>(( More to read here soon. ))</p>\n            </div>\n        </div>\n\n    <!-- name -->\n    <div class=\"row-fluid base media ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"name")) {
output += "missing";
;
}
output += "\">\n\n        <div class=\"span6\">\n\n            <div class=\"control-group\">\n                <label class=\"control-label\" for=\"inputEmail\">Title <span class=\"required\">*</span></label>\n\n                <div class=\"controls\">\n                    <input type=\"text\" class=\"release autoupdate\" data-ct=\"media\" value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"name"), env.opts.autoescape);
output += "\">\n                </div>\n            </div>\n\n        </div>\n\n    </div>\n\n    <!-- release -->\n    <div class=\"row-fluid base release ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"release")) {
output += "missing";
;
}
output += "\">\n\n        <div class=\"span5\">\n\n            <div class=\"control-group\">\n                <label class=\"control-label\" for=\"inputEmail\">Release <span class=\"required\">*</span></label>\n\n                <div class=\"controls\">\n                    <input type=\"text\"\n                           class=\"release autocomplete\"\n                           data-ct=\"release\"\n                           value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"release"), env.opts.autoescape);
output += "\">\n\n                    <div class=\"ac-result\"></div>\n                </div>\n            </div>\n\n        </div>\n\n        <div class=\"span3\">\n            ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id") && !runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_release")) {
output += "\n                <a href=\"#\"\n                   data-ct=\"release\"\n                   data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_resource_uri"), env.opts.autoescape);
output += "\"\n                   class=\"tooltip-inline\">\n                    <i class=\"icon-paper-clip\"></i>\n                    Assigned\n                </a>\n            ";
;
}
else {
output += "\n                <span class=\"dim\"><i class=\"icon-plus\"></i> Create</span>\n            ";
;
}
output += "\n        </div>\n\n        <div class=\"span2\">\n            ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id")) {
output += "\n                <input type=\"checkbox\"\n                       class=\"force-creation\"\n                       ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_release")) {
output += "checked=\"checked\"";
;
}
output += "/>\n                Force Creation<a class=\"tooltipable\"\n                                 data-title=\"Enable this to force the creation of a new entry - even if there is already an item with the same name.\"><i\n                    class=\"icon-question-sign\"></i></a>\n            ";
;
}
else {
output += "\n                &nbsp;\n            ";
;
}
output += "\n        </div>\n\n        <div class=\"span2\">\n            <a class=\"btn btn-mini pull-right apply-to-all\" data-ct=\"release\"><i class=\"icon-repeat\"></i> Apply Release\n                to all</a>\n        </div>\n\n\n    </div>\n\n    <!-- artist -->\n    <div class=\"row-fluid base artist ";
if(!runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"artist")) {
output += "missing";
;
}
output += "\">\n\n        <div class=\"span5\">\n\n            <div class=\"control-group\">\n                <label class=\"control-label\" for=\"inputEmail\">Artist <span class=\"required\">*</span></label>\n\n                <div class=\"controls\">\n                    <input type=\"text\"\n                           class=\"artist autocomplete\"\n                           data-ct=\"artist\"\n                           value=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"artist"), env.opts.autoescape);
output += "\">\n\n                    <div class=\"ac-result\"></div>\n                </div>\n            </div>\n\n        </div>\n\n        <div class=\"span3\">\n            ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id") && !runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_artist")) {
output += "\n                <a href=\"#\"\n                   data-ct=\"artist\"\n                   data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_resource_uri"), env.opts.autoescape);
output += "\"\n                   class=\"tooltip-inline\">\n                    <i class=\"icon-paper-clip\"></i>\n                    Assigned\n                </a>\n            ";
;
}
else {
output += "\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_matches")) {
output += "\n                    <a href=\"#\" class=\"matches\"><i class=\"icon-warning-sign\"></i> ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_matches"), env.opts.autoescape);
output += " matches</a>\n                ";
;
}
output += "\n                <span class=\"dim\"><i class=\"icon-plus\"></i> Create</span>\n            ";
;
}
output += "\n        </div>\n\n        <div class=\"span2\">\n            ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id")) {
output += "\n                <input type=\"checkbox\"\n                       class=\"force-creation\"\n                       ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_artist")) {
output += "checked=\"checked\"";
;
}
output += "/>\n                Force Creation<a class=\"tooltipable\"\n                                 data-title=\"Enable this to force the creation of a new entry - even if there is already an item with the same name.\"><i\n                    class=\"icon-question-sign\"></i></a>\n            ";
;
}
else {
output += "\n                &nbsp;\n            ";
;
}
output += "\n        </div>\n\n        <div class=\"span2\">\n            <a class=\"btn btn-mini pull-right apply-to-all\" data-ct=\"artist\"><i class=\"icon-repeat\"></i> Apply Artist to all</a>\n        </div>\n\n\n    </div>\n\n    </form>\n\n    </div>\n\n    <div class=\"row-fluid pull-righ result-actions\">\n\n        <div class=\"span2\">\n            &nbsp;\n        </div>\n\n        <div class=\"pull-right span10\">\n            <a class=\"btn btn-secondary btn-small delete-importfile\">Delete this File</a>\n            <!--\n            <a class=\"btn btn-secondary btn-small rescan\" data-settings=\"skip_tracknumber\">Scan witouth tracknumber</a>\n            -->\n            <a class=\"btn btn-secondary btn-small rescan\">Scan again</a>\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += "\n                <a class=\"btn btn-primary btn-small start-import\">Continue Import</a>\n            ";
;
}
output += "\n        </div>\n    </div>\n\n\n";
;
}
output += "\n\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["importer/nj/popover.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"po-inline\">\n\n    <div class=\"row-fluid\">\n\n        <div class=\"span2\">\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image")) {
output += "\n                <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image"), env.opts.autoescape);
output += "\"/>\n            ";
;
}
else {
output += "\n                <img src=\"/static/img/base/defaults/listview.release.xl.png\"/>\n            ";
;
}
output += "\n        </div>\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"ct") == "release") {
output += "\n            <div class=\"span10\">\n                <ul class=\"unstyled\">\n                    <li><strong>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name"), env.opts.autoescape);
output += "</strong>\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"catalognumber")) {
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"catalognumber"), env.opts.autoescape);
;
}
output += "\n                        <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasedate"), env.opts.autoescape);
output += "</small>\n                    </li>\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"artist")) {
output += "\n                        <li>";
frame = frame.push();
var t_3 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"artist");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("artist", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += runtime.suppressValue(t_4, env.opts.autoescape);
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last")) {
output += ",\n                        ";
;
}
;
}
}
frame = frame.pop();
output += "</li>\n                    ";
;
}
output += "\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"label")) {
output += "\n                        <li>";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"label")),"name"), env.opts.autoescape);
output += "</li>\n                    ";
;
}
output += "\n                </ul>\n            </div>\n        ";
;
}
output += "\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"ct") == "artist") {
output += "\n            <div class=\"span10\">\n                <ul class=\"unstyled\">\n                    <li><strong>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name"), env.opts.autoescape);
output += "</strong>\n                        <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"type"), env.opts.autoescape);
output += "</small>\n                    </li>\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_start")) {
output += "*";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_start"), env.opts.autoescape);
;
}
output += "\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_end")) {
output += "✝";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_end"), env.opts.autoescape);
;
}
output += "\n                </ul>\n            </div>\n        ";
;
}
output += "\n\n    </div>\n\n\n    <div class=\"alert alert-info\">\n        <p>Track will be added to this ";
output += runtime.suppressValue(env.getFilter("title").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"ct")), env.opts.autoescape);
output += ". If this is not desired, enable \"Force\n            Creation\"</p>\n    </div>\n\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["importer/nj/summary.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div id=\"import_summary\" class=\"import summary listing\">\n\n    <div class=\"page-header\">\n        <h4>Summary\n            <small>Current Import</small>\n        </h4>\n    </div>\n\n    <div class=\"summary item ready hoverable\">\n        <strong><i class=\"icon-check-empty\"></i> Ready to import</strong>\n\n        <div class=\"row-fluid \">\n            <div class=\"span12\">\n                <span class=\"num-files\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "counters")),"num_ready"), env.opts.autoescape);
output += "</span> files\n            </div>\n        </div>\n\n\n        <!--\n        <div class=\"row-fluid\">\n            <div class=\"span12 counters\">\n                <p>Importing all files will ad +/_ the following to the library:</p>\n                <dl>\n                    <dt>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "inserts")),"num_media"), env.opts.autoescape);
output += "</dt>\n                    <dd>Track(s)</dd>\n\n                    <dt>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "inserts")),"num_artists"), env.opts.autoescape);
output += "</dt>\n                    <dd>Artist(s)</dd>\n\n                    <dt>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "inserts")),"num_releases"), env.opts.autoescape);
output += "</dt>\n                    <dd>Release(s)</dd>\n                </dl>\n            </div>\n        </div>\n        -->\n\n\n        <div class=\"row-fluid \">\n            <div class=\"span12\">\n                <button class=\" pull-right btn btn-mini btn-primary start-import-all\"\n                        type=\"button\">Import all\n                </button>\n            </div>\n        </div>\n\n\n\n\n    </div>\n\n    <div class=\"summary item done hoverable\">\n        <strong><i class=\"icon-check\"></i> Import completed <a class=\"toggle\"\n                                                               data-toggle=\"done\"\n                                                               href=\"#\"><i class=\"icon-angle-up pull-right icon-2x\"></i></a></strong>\n\n        <div class=\"row-fluid \">\n            <div class=\"span3\">\n                <span class=\"num-files\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "counters")),"num_done"), env.opts.autoescape);
output += "</span> files\n            </div>\n            <div class=\"span9\">\n            </div>\n        </div>\n    </div>\n\n    <div class=\"summary item duplicate hoverable\">\n        <strong><i class=\"icon-copy\"></i> Duplicates <a class=\"toggle\"\n                                                        data-toggle=\"duplicate\"\n                                                        href=\"#\"><i class=\"icon-angle-up pull-right icon-2x\"></i></a></strong>\n\n        <div class=\"row-fluid \">\n            <div class=\"span3\">\n                <span class=\"num-files\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "counters")),"num_duplicate"), env.opts.autoescape);
output += "</span> files\n            </div>\n            <div class=\"span9\">\n\n            </div>\n        </div>\n    </div>\n\n    <div class=\"summary item pending hoverable\">\n        <strong><i class=\"icon-time\"></i> Processing</strong>\n\n        <div class=\"row-fluid \">\n            <div class=\"span3\">\n                <span class=\"num-files\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "counters")),"num_working"), env.opts.autoescape);
output += "</span> files\n            </div>\n            <div class=\"span9\">\n\n            </div>\n        </div>\n\n        <div class=\"row-fluid \">\n            <div class=\"span12\">\n                <button class=\" pull-right btn btn-mini btn-secondary retry-pending\"\n                        type=\"button\">Retry all\n                </button>\n            </div>\n        </div>\n\n    </div>\n\n    <div class=\"summary item warning hoverable\">\n        <strong><i class=\"icon-question-sign\"></i> Information needed</strong>\n\n        <div class=\"row-fluid \">\n            <div class=\"span3\">\n                <span class=\"num-files\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "counters")),"num_warning"), env.opts.autoescape);
output += "</span> files\n            </div>\n            <div class=\"span9\">\n\n            </div>\n        </div>\n    </div>\n\n    <div class=\"summary item error hoverable\">\n        <strong><i class=\"icon-warning-sign\"></i> Errors</strong>\n\n        <div class=\"row-fluid \">\n            <div class=\"span3\">\n                <span class=\"num-files\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "counters")),"num_error"), env.opts.autoescape);
output += "</span> files\n            </div>\n            <div class=\"span9\">\n\n            </div>\n        </div>\n    </div>\n\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["exporter/nj/export.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<tr class=\"item export ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status_display"), env.opts.autoescape);
output += "\" data-last_status=\"0\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\">\n    <td>\n\n        <i class=\"icon-refresh icon-spin visible-while-init\"></i>\n        <i class=\"icon-download-alt visible-while-done\"></i>\n        <i class=\"icon-ok-sign visible-while-downloaded\"></i>\n        <i class=\"icon-refresh icon-spin visible-while-ready\"></i>\n        <i class=\"icon-tasks visible-while-progress\"></i>\n        <i class=\"icon-warning-sign icon-pulse visible-while-error\"\n           ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status_msg")) {
output += "\n               title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status_msg"), env.opts.autoescape);
output += "\"\n           ";
;
}
output += "\n           ></i>\n\n    </td>\n\n\n    <td>\n        ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"filename"), env.opts.autoescape);
output += " <small>debug: ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "</small>\n\n    </td>\n    <td>";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"created"),"datetime"), env.opts.autoescape);
output += "</td>\n    <td>\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"downloaded")) {
output += "\n            ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"downloaded"),"datetime"), env.opts.autoescape);
output += "\n        ";
;
}
output += "\n    </td>\n\n    <td>\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"filesize")) {
output += "\n            <div class=\"pull-right\">\n                ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"formatted_filesize"), env.opts.autoescape);
output += "\n            </div>\n        ";
;
}
output += "\n    </td>\n    <td>\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == 1 || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") == 4) {
output += "\n        <a href=\"#\" data-action=\"download\"><i class=\"icon-download-alt\"></i> Download</a>\n        ";
;
}
output += "\n    </td>\n    <td>\n\n\n        <div class=\"btn-group pull-right\">\n            <button class=\"btn btn-mini btn-prrimary\" data-toggle=\"dropdown\">\n                Actions\n            </button>\n            <button class=\"btn btn-mini btn-prrimary dropdown-toggle\" data-toggle=\"dropdown\">\n                <span class=\"caret\"></span>\n            </button>\n            <ul class=\"dropdown-menu\">\n                <!--\n                <li>\n                    <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"get_absolute_url"), env.opts.autoescape);
output += "\"><i class=\"icon-edit\"></i> Details</a>\n                </li>\n                -->\n                ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"status") != 2) {
output += "\n                <li>\n                    <a href=\"#\" data-action=\"delete\">Delete</a>\n                </li>\n                ";
;
}
else {
output += "\n                    <li>...</li>\n                ";
;
}
output += "\n                <!--\n                <li class=\"divider\"></li>\n                <li>\n                    <a href=\"#\">Separated link</a>\n                </li>\n                -->\n            </ul>\n        </div>\n\n    </td>\n\n</tr>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["abcast/nj/autocomplete.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"result\">\n\n\t<div class=\"listing\">\n\t\t";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n\t\t<div class=\"item hoverable\" data-id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"id"), env.opts.autoescape);
output += "\" data-name=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name"), env.opts.autoescape);
output += "\" data-ct=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"ct"), env.opts.autoescape);
output += "\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"resource_uri"), env.opts.autoescape);
output += "\">\n\t\t\t\n\t\t\t<div class=\"row-fluid\">\n\t\t\t\t\n\t\t\t\t<div class=\"span3\">\n\t\t\t\t\t\n\t\t\t\t\t";
if(runtime.memberLookup((t_4),"main_image")) {
output += "\n\t\t\t\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"main_image"), env.opts.autoescape);
output += "\" />\n\t\t\t\t\t";
;
}
else {
output += "\n\t\t\t\t\t<img src=\"/static/img/base/defaults/listview.";
output += runtime.suppressValue(runtime.memberLookup((t_4),"ct"), env.opts.autoescape);
output += ".xl.png\" width=\"90\" height=\"90\" />\n\t\t\t\t\t";
;
}
output += "\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span9\">\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t<!---->\n\t\t\t\t\t<ul class=\"unstyled\">\n\t\t\t\t\t\t\n\t\t\t\t\t\t<li><strong>";
output += runtime.suppressValue(env.getFilter("highlight").call(context, env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((t_4),"name"),30),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query")), env.opts.autoescape);
output += "</strong>  <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((t_4),"releasedate"), env.opts.autoescape);
output += "</small></li>\n\t\t\t\t\t\t<li>\n\t\t\t\t\t\t\t<span>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"user"), env.opts.autoescape);
output += "</span>\n\t\t\t\t\t\t\t|\n\t\t\t\t\t\t\t<span>";
output += runtime.suppressValue(runtime.memberLookup((t_4),"target_duration") / 60, env.opts.autoescape);
output += " min</span>\n\t\t\t\t\t\t</li>\n\t\t\t\t\t\t<li><span>";
output += runtime.suppressValue(env.getFilter("shorten").call(context, runtime.memberLookup((t_4),"tags"),30), env.opts.autoescape);
output += "</span></li>\n\t\t\t\t\t\t<!--\n\t\t\t\t\t\t";
if(runtime.memberLookup((t_4),"ct") == "playlist") {
output += "\n\t\t\t\t\t\t";
frame = frame.push();
var t_7 = runtime.memberLookup((t_4),"media");
if(t_7) {var t_6 = t_7.length;
for(var t_5=0; t_5 < t_7.length; t_5++) {
var t_8 = t_7[t_5];
frame.set("item", t_8);
frame.set("loop.index", t_5 + 1);
frame.set("loop.index0", t_5);
frame.set("loop.revindex", t_6 - t_5);
frame.set("loop.revindex0", t_6 - t_5 - 1);
frame.set("loop.first", t_5 === 0);
frame.set("loop.last", t_5 === t_6 - 1);
frame.set("loop.length", t_6);
output += "\n\t\t\t\t\t\t<li>\n\t\t\t\t\t\t";
output += runtime.suppressValue(runtime.memberLookup((t_8),"name"), env.opts.autoescape);
output += "\n\t\t\t\t\t\t</li>\n\t\t\t\t\t\t";
;
}
}
frame = frame.pop();
output += "\n\t\t\t\t\t\t";
;
}
output += "\n\t\t\t\t\t\t-->\n\t\t\t\t\t</ul>\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\n\t\t</div>\n\t\t";
;
}
}
frame = frame.pop();
output += "\n\t</div>\n</div>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["abcast/nj/col_day.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["abcast/nj/emission.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div \n\tclass=\"hoverable chip fix ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"source"), env.opts.autoescape);
output += " emission theme-";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color"), env.opts.autoescape);
output += "\"\n\tdata-resource-uri=";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri"), env.opts.autoescape);
output += "\n\tid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\" \n\tdata-tip=\"<div class='tooltip-emission'><strong><i class='icon-tasks'></i> ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"type"), env.opts.autoescape);
output += "</strong><br>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"start"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"end"), env.opts.autoescape);
output += "<br>scheduled by: ";
output += runtime.suppressValue(env.getFilter("escape").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user")),"username")), env.opts.autoescape);
output += "<div class='description markdown-remove'>";
output += runtime.suppressValue(env.getFilter("escape").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description_html")), env.opts.autoescape);
output += "</div>";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"main_image")) {
output += "<img src='";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"main_image"), env.opts.autoescape);
output += "' style='width: 200px;'>";
;
}
output += "</div>\"\n\tstyle=\"top:";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "top"), env.opts.autoescape);
output += "px;left:-1px;width:100%;\n\">\n\n\n\t<dl class=\"cbrd\" style=\"height:";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "height") - 1, env.opts.autoescape);
output += "px;\">\n\t\t<dt style=\"\">\n\t\t\t\n\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"absolute_url"), env.opts.autoescape);
output += "\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"resource_uri"), env.opts.autoescape);
output += "\">\n\t\t\t";
output += runtime.suppressValue(env.getFilter("escape").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name")), env.opts.autoescape);
output += "\n\t\t\t</a>\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"playing")) {
output += "\n\t\t\t<i class=\"icon-bullhorn pull-right\"></i>\n                asd\n\t\t\t";
;
}
output += "\n\t\t\t\n\t\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"locked")) {
output += "\n\t\t\t<i class=\"icon-lock pull-right\"></i>\n\t\t\t";
;
}
output += "\n            ";
if(runtime.contextOrFrameLookup(context, frame, "height") > 20) {
output += "\n            <div class=\"time\">\n                <span>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"start"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"end"), env.opts.autoescape);
output += "</span>\n            </div>\n            ";
;
}
output += "\n\n\t\t</dt>\n\n\t</dl>\n\t\n</div>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["abcast/nj/emission_popup.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<section class=\"title\">\n\t<h3>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"), env.opts.autoescape);
output += " <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"type_display"), env.opts.autoescape);
output += "</small></h3>\n\t<ul class=\"unstyled\">\n\t\t<li>\n\t\t\t<i class=\"icon-time\"></i> ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start"),"time"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_end"),"time"), env.opts.autoescape);
output += " | ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start"),"date"), env.opts.autoescape);
output += "\n\t\t</li>\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user")) {
output += "\n\t\t<li>\n\t\t\t<i class=\"icon-user\"></i>\n            <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user")),"username"), env.opts.autoescape);
output += "</a>\n            <small>scheduler</small>\n\t\t</li>\n\t\t";
;
}
output += "\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user_co")) {
output += "\n\t\t<li>\n\t\t\t<i class=\"icon-user\"></i>\n            <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user_co")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user_co")),"username"), env.opts.autoescape);
output += "</a>\n            <small>creator</small>\n\t\t</li>\n\t\t";
;
}
output += "\n\t</ul>\n</section>\n\n<section class=\"description\">\n\n\n    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"main_image")) {
output += "\n    <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"main_image"), env.opts.autoescape);
output += "\" style=\"width: 50%;\">\n    ";
;
}
output += "\n\n    <!--\n\t<p>";
output += runtime.suppressValue(env.getFilter("linebreaksbr").call(context, env.getFilter("shorten").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description_html"),200)), env.opts.autoescape);
output += "</p>\n    -->\n    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description")) {
output += "\n\t<div class=\"description markdown-remove\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description_html"), env.opts.autoescape);
output += "</div>\n    ";
;
}
output += "\n\t<!--\n\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"absolute_url"), env.opts.autoescape);
output += "\" class=\"pull-left\">> Read more</a>\n\t-->\n\n\t<ul class=\"unstyled object-links\">\n\t\t<li>\n\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">&gt; Emission details</a>\n\t\t</li>\n\t\t<li>\n\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"absolute_url"), env.opts.autoescape);
output += "\">&gt; Content details</a>\n\t\t</li>\n\t</ul>\n\n</section>\n\n\n";
if(!runtime.contextOrFrameLookup(context, frame, "readonly")) {
output += "\n<section class=\"form\">\n\n\t<fieldset>\n\t\t<label class=\"checkbox\">\n\t\t\t<input type=\"checkbox\" class=\"edit-lock\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"locked") == 1) {
output += "checked=\"checked\"";
;
}
output += ">\n\t\t\tLock editing </label>\n\t</fieldset>\n\t\n\t<fieldset class=\"color\">\n\t\t<div class=\"controls\">\n\t\t\t\n\t\t\t<label class=\"radio  theme-0\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"0\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color") == 0) {
output += "checked=\"checked\"";
;
}
output += ">\n\t\t\t</label>\n\t\t\t\n\t\t\t<label class=\"radio theme-1\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"1\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color") == 1) {
output += "checked=\"checked\"";
;
}
output += ">\n\t\t\t</label>\n\t\t\t\n\t\t\t<label class=\"radio theme-2\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"2\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color") == 2) {
output += "checked=\"checked\"";
;
}
output += ">\n\t\t\t</label>\n\t\t\t\n\t\t\t<label class=\"radio theme-3\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"3\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color") == 3) {
output += "checked=\"checked\"";
;
}
output += ">\n\t\t\t</label>\n\t\t\t\n\t\t\t<label class=\"radio theme-4\">\n\t\t\t\t<input type=\"radio\" class=\"color\" name=\"color\" value=\"4\" ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"color") == 4) {
output += "checked=\"checked\"";
;
}
output += ">\n\t\t\t</label>\n\n\t\t</div>\n\t</fieldset>\n\t\n\n\t<div class=\"btn-toolbar\">\n\t\t<div class=\"btn-group pull-right\">\n\t\t\t<a data-action=\"cancel\" class=\"btn btn-mini pull-right\">Cancel</a>\n\t\t\t";
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"locked")) {
output += "\n\t\t\t<a data-action=\"delete\" class=\"btn btn-mini pull-right\">Delete</a>\n\t\t\t";
;
}
output += "\n\t\t\t<a data-action=\"save\" class=\"btn btn-primary btn-mini pull-right\">Save</a>\n\t\t</div>\n\t</div>\n\n</section>\n";
;
}
output += "\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["abcast/nj/on_air_emission.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<!--\n<ul class=\"unstyled\">\n\t<li><strong class=\"name\"><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"),30), env.opts.autoescape);
output += "</a></strong><small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"type_display"), env.opts.autoescape);
output += "</small></li>\n\t<li><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user")),"full_name"), env.opts.autoescape);
output += "</a></li>\n\t<li>";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start"),"time"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_end"),"time"), env.opts.autoescape);
output += "</li>\n</ul>\n-->\n\n<section class=\"title\">\n    <!--\n\t<h3>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"), env.opts.autoescape);
output += " <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"type_display"), env.opts.autoescape);
output += "</small></h3>\n\t-->\n\t<h3>\n        <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"), env.opts.autoescape);
output += "</a>\n        <small class=\"pull-right\">\n            <a href=\"#\" class=\"btn streamable popup\" data-resource_uri=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "api_url"), env.opts.autoescape);
output += "\"><i class=\"icon-play\"></i>&nbsp;&nbsp;Tune In</a>\n        </small>\n    </h3>\n\t<ul class=\"unstyled\">\n\t\t<li>\n\t\t\t<i class=\"icon-time\"></i> ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start"),"time"), env.opts.autoescape);
output += " - ";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_end"),"time"), env.opts.autoescape);
output += "\n\t\t</li>\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user_co")) {
output += "\n\t\t<li>\n\t\t\t<i class=\"icon-user\"></i>\n            <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user_co")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"user_co")),"username"), env.opts.autoescape);
output += "</a>\n\n            <a style=\"font-size: 16px;\" href=\"#\" onclick=\"$('section.description').toggle(200);\" class=\"pull-right\"><i class=\"icon-caret-down icon-large\"></i></a>\n\n\t\t</li>\n\t\t";
;
}
output += "\n\t</ul>\n</section>\n\n<section class=\"description\">\n\n\n    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"main_image")) {
output += "\n    <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"main_image"), env.opts.autoescape);
output += "\" style=\"width: 50%;\">\n    ";
;
}
output += "\n\n    <!--\n\t<p>";
output += runtime.suppressValue(env.getFilter("linebreaksbr").call(context, env.getFilter("shorten").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description_html"),200)), env.opts.autoescape);
output += "</p>\n    -->\n    ";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description")) {
output += "\n\t<div class=\"description markdown-remove\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"description_html"), env.opts.autoescape);
output += "</div>\n    ";
;
}
output += "\n\t<!--\n\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"absolute_url"), env.opts.autoescape);
output += "\" class=\"pull-left\">> Read more</a>\n\t-->\n\n\t<ul class=\"unstyled object-links\">\n\t\t<li>\n\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">&gt; Emission details</a>\n\t\t</li>\n\t\t<li>\n\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"content_object")),"absolute_url"), env.opts.autoescape);
output += "\">&gt; Content details</a>\n\t\t</li>\n\t</ul>\n\n</section>\n\n\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["abcast/nj/on_air_item.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"on-air item\" data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\">\n\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release") && runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"main_image")) {
output += "\n\n        <div class=\"image\">\n            <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">\n                <img class=\"release\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"main_image"), env.opts.autoescape);
output += "\">\n                <img class=\"artist\" src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"main_image"), env.opts.autoescape);
output += "\">\n            </a>\n        </div>\n\n    ";
;
}
output += "\n\n\n    <div class=\"information\">\n\n        <div class=\"rating-inline pull-right\">\n\n            <ul class=\"horizontal unstyled arating\">\n\n                ";
if(runtime.contextOrFrameLookup(context, frame, "authenticated")) {
output += "\n                    <li>\n                        <a data-vote=\"";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"votes")),"user") == -1) {
output += "0";
;
}
else {
output += "-1";
;
}
output += "\"\n                           class=\"vote-1";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"votes")),"user") == -1) {
output += " active";
;
}
output += "\"\n                           href=\"/en/vote/alibrary.media/";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "/0/\">\n                            <i class=\"icon-thumbs-down\"></i>\n                            <span class=\"count\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"votes")),"down"), env.opts.autoescape);
output += "</span>\n                        </a>\n                    </li>\n\n                    <li>\n                        <a data-vote=\"";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"votes")),"user") == 1) {
output += "0";
;
}
else {
output += "1";
;
}
output += "\"\n                           class=\"vote1";
if(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"votes")),"user") == 1) {
output += " active";
;
}
output += "\"\n                           href=\"/en/vote/alibrary.media/";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id"), env.opts.autoescape);
output += "/0/\">\n                            <i class=\"icon-thumbs-up\"></i>\n                            <span class=\"count\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"votes")),"up"), env.opts.autoescape);
output += "</span>\n                        </a>\n                    </li>\n                ";
;
}
else {
output += "\n                    <li>\n                            <i class=\"icon-thumbs-down\"></i>\n                            <span class=\"count\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"votes")),"down"), env.opts.autoescape);
output += "</span>\n\n                    </li>\n\n                    <li>\n\n                            <i class=\"icon-thumbs-up\"></i>\n                            <span class=\"count\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"votes")),"up"), env.opts.autoescape);
output += "</span>\n                    </li>\n                ";
;
}
output += "\n\n\n            </ul>\n\n\n        </div>\n\n        <ul class=\"unstyled\">\n            <li>\n                <h4 class=\"name\"><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"),24), env.opts.autoescape);
output += "</a></h4>\n            </li>\n            <li>\n                <a data-target=\"artist\" href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"absolute_url"), env.opts.autoescape);
output += "\">\n                    ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"name"),32), env.opts.autoescape);
output += "</a>\n            </li>\n            <li>\n                <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"name"),32), env.opts.autoescape);
output += "</a>\n            </li>\n\n            <li>\n                <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"label")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"label")),"name"),32), env.opts.autoescape);
output += "</a>\n            </li>\n        </ul>\n    </div>\n\n</div>\n\n\n<!--\n<div class=\"row-fluid\" style=\"display: none;\">\n\n\t<div class=\"span3\">\n\t\t\n\t\t";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")) {
output += "\n\t\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"main_image"), env.opts.autoescape);
output += "\" width=\"54\">\n\t\t";
;
}
else {
output += "\n\t\t&nbsp;\n\t\t";
;
}
output += "\n\t\t\n\t</div>\n\n\t<div class=\"span9\">\n\n\t\t<ul class=\"unstyled\">\n\t\t\t<li>\n\t\t\t\t<span class=\"playing\">\n\t\t\t\t<i class=\"icon-headphones\"></i>\n\t\t\t\t</span>\n\t\t\t\t<strong class=\"name\"><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"),32), env.opts.autoescape);
output += "</a></strong>\n\t\t\t</li>\n\t\t\t<li>\n\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"artist")),"name"),32), env.opts.autoescape);
output += "</a>\n\t\t\t</li>\n\t\t\t<li>\n\t\t\t\t<a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"absolute_url"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"release")),"name"),32), env.opts.autoescape);
output += "</a>\n\t\t\t</li>\n\t\t</ul>\n\n\t</div>\n\n</div>\n-->\n\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["abcast/nj/selected_object.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<h4>Selected for scheduling</h4>\n<p>Drag and drop to a free slot</p>\n\n<div class=\"object-search\">\n    <input class=\"autocomplete\" data-ct=\"playlist\" type=\"text\" placeholder=\"Search broadcasts\">\n\n    <div class=\"ac-result\"></div>\n</div>\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id")) {
output += "\n    <div class=\"_container object-to-schedule\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"), env.opts.autoescape);
output += "\">\n        <div class=\"row-fluid\">\n            <div class=\"span3\">\n                ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"main_image")) {
output += "\n                    <img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"main_image"), env.opts.autoescape);
output += "\"/>\n                ";
;
}
else {
output += "\n                    <img src=\"/static/img/base/defaults/listview.playlist.xl.png\"\n                         width=\"90\"\n                         height=\"90\"/>\n                ";
;
}
output += "\n            </div>\n\n            <div class=\"span9\">\n                <ul class=\"unstyled\">\n                    <li>\n                        <strong><a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"absolute_url"), env.opts.autoescape);
output += "\">\n                            ";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name"),30), env.opts.autoescape);
output += "</a></strong>\n                        <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"target_duration") / 60, env.opts.autoescape);
output += " min</small>\n                    </li>\n                    <p class=\"tags\">";
output += runtime.suppressValue(env.getFilter("shorten").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"d_tags"),60), env.opts.autoescape);
output += "</p>\n                </ul>\n            </div>\n        </div>\n    </div>\n";
;
}
output += "\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["abcast/nj/top_week.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<table class=\"wk-weektop wk-full-mode\" cellpadding=\"0\" cellspacing=\"0\">\n\t<tbody>\n\t\t<tr class=\"wk-daynames\">\n\t\t\t<td class=\"wk-tzlabel\" style=\"width:60px\" rowspan=\"3\"></td><th title=\"Sun 5/19\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22195 wk-daylink\">Sun 5/19</span>\n\t\t\t</div></th><th title=\"Mon 5/20\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22196 wk-daylink\">Mon 5/20</span>\n\t\t\t</div></th><th title=\"Tue 5/21\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22197 wk-daylink\">Tue 5/21</span>\n\t\t\t</div></th><th title=\"Wed 5/22\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22198 wk-daylink\">Wed 5/22</span>\n\t\t\t</div></th><th title=\"Thu 5/23\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname\">\n\t\t\t\t<span class=\"ca-cdp22199 wk-daylink\">Thu 5/235</span>\n\t\t\t</div></th><th title=\"Fri 5/24\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname wk-today\">\n\t\t\t\t<span class=\"ca-cdp22200 wk-daylink\">Fri 5/24</span>\n\t\t\t</div></th><th title=\"Sat 5/25\" scope=\"col\">\n\t\t\t<div class=\"wk-dayname wk-tomorrow\">\n\t\t\t\t<span class=\"ca-cdp22201 wk-daylink\">Sat 5/25</span>\n\t\t\t</div></th><th class=\"wk-dummyth\" rowspan=\"3\" style=\"width: 17px;\">&nbsp;</th>\n\t\t</tr>\n\t</tbody>\n</table>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();



