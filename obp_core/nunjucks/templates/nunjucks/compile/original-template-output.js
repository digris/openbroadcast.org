(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["item.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<!-- loaded dynamically to: #onair_container > .items -->\n\n\n<!-- item in this context: \"track\" - active or history -->\n<div\n    class=\"item info ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "extra_classes"), env.opts.autoescape);
output += "\"\n    id=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "dom_id"), env.opts.autoescape);
output += "\"\n    data-time_start=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start", env.opts.autoescape), env.opts.autoescape);
output += "\"\n    data-uuid=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"uuid", env.opts.autoescape), env.opts.autoescape);
output += "\"\n    data-onair=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"onair", env.opts.autoescape), env.opts.autoescape);
output += "\"\n    data-index=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "index"), env.opts.autoescape);
output += "\">\n\n    <!-- base container - media -->\n    <div class=\"container\"\n         ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape) && runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape) && runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"main_image", env.opts.autoescape)) {
output += "\n         style=\"background: url(";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"main_image", env.opts.autoescape), env.opts.autoescape);
output += ");\">\n         ";
;
}
else {
output += "\n         style=\"background: #000;\">\n         ";
;
}
output += "\n\n        <!-- swapable container - artist/label/etc -->\n        <div class=\"details\">\n            ";
env.getTemplate("onair/nj/item_playlist.html", false, "item.html", function(t_3,t_1) {
if(t_3) { cb(t_3); return; }
t_1.render(context.getVariables(), frame.push(), function(t_4,t_2) {
if(t_4) { cb(t_4); return; }
output += t_2
output += "\n            ";
env.getTemplate("onair/nj/item_author.html", false, "item.html", function(t_7,t_5) {
if(t_7) { cb(t_7); return; }
t_5.render(context.getVariables(), frame.push(), function(t_8,t_6) {
if(t_8) { cb(t_8); return; }
output += t_6
output += "\n            ";
env.getTemplate("onair/nj/item_media.html", false, "item.html", function(t_11,t_9) {
if(t_11) { cb(t_11); return; }
t_9.render(context.getVariables(), frame.push(), function(t_12,t_10) {
if(t_12) { cb(t_12); return; }
output += t_10
output += "\n            ";
env.getTemplate("onair/nj/item_artist.html", false, "item.html", function(t_15,t_13) {
if(t_15) { cb(t_15); return; }
t_13.render(context.getVariables(), frame.push(), function(t_16,t_14) {
if(t_16) { cb(t_16); return; }
output += t_14
output += "\n            ";
env.getTemplate("onair/nj/item_release.html", false, "item.html", function(t_19,t_17) {
if(t_19) { cb(t_19); return; }
t_17.render(context.getVariables(), frame.push(), function(t_20,t_18) {
if(t_20) { cb(t_20); return; }
output += t_18
output += "\n            ";
env.getTemplate("onair/nj/item_label.html", false, "item.html", function(t_23,t_21) {
if(t_23) { cb(t_23); return; }
t_21.render(context.getVariables(), frame.push(), function(t_24,t_22) {
if(t_24) { cb(t_24); return; }
output += t_22
output += "\n        </div>\n\n        <!-- action wrapper - play/pause/listen -->\n        <div class=\"wrapper\">\n\n            <div class=\"controls hoverable\">\n\n                <span class=\"play\">\n                    <a href=\"#\" data-login-required data-onair-controls=\"play\">Play</a>\n                </span>\n\n                <span class=\"listen\">\n                    <a data-onair-controls=\"play\" href=\"#\">Listen</a>\n                </span>\n\n                <span class=\"pause\">\n                    <a data-onair-controls=\"pause\" href=\"#\">||</a>\n                </span>\n\n                <span class=\"loading\">\n                    <a href=\"#\">\n                        <i class=\"fa fa-circle-o-notch fa-spin fa-fw\"></i>\n                    </a>\n                </span>\n\n            </div>\n\n\n        </div>\n\n        <div class=\"progress-container hoverable\">\n            <div class=\"progress\">\n              <span class=\"meter\" style=\"width: 0%\"></span>\n            </div>\n        </div>\n\n\n    </div>\n\n</div>\n<!-- item end -->";
cb(null, output);
})})})})})})})})})})})});
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["item_artist.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var t_1;
t_1 = runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"artist", env.opts.autoescape);
frame.set("item", t_1, true);
if(!frame.parent) {
context.setVariable("item", t_1);
context.addExport("item");
}
output += "\n\n";
if(runtime.contextOrFrameLookup(context, frame, "item")) {
output += "\n    <div data-ct=\"artist\" class=\"ct-panel\">\n\n        <div class=\"row header\">\n\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape)) {
output += "\n            <div class=\"small-6 columns\">\n                <img src=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape), env.opts.autoescape);
output += "\">\n            </div>\n            ";
;
}
output += "\n\n            <div class=\"";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape)) {
output += "small-6";
;
}
else {
output += "small-12";
;
}
output += " columns\">\n                <div class=\"text-left\">\n                    <h1>";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name", env.opts.autoescape),24), env.opts.autoescape);
output += "</h1>\n                    <ul class=\"no-bullet\">\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"type", env.opts.autoescape) || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)) {
output += "\n                        <li>\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)) {
output += "\n                                (";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape), env.opts.autoescape);
output += ")\n                            ";
;
}
output += "\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"type", env.opts.autoescape)) {
output += "\n                                ";
output += runtime.suppressValue(env.getFilter("capitalize").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"type", env.opts.autoescape)), env.opts.autoescape);
output += "\n                            ";
;
}
output += "\n                        </li>\n                        ";
;
}
output += "\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_start", env.opts.autoescape) || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_start", env.opts.autoescape)) {
output += "\n                        <li>\n                            ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_start", env.opts.autoescape), env.opts.autoescape);
output += "\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_start", env.opts.autoescape) || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_start", env.opts.autoescape)) {
output += " - ";
;
}
output += "\n                            ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"date_end", env.opts.autoescape), env.opts.autoescape);
output += "\n                        </li>\n                        ";
;
}
output += "\n                    </ul>\n                </div>\n            </div>\n        </div>\n\n        <div class=\"row body\">\n            <div class=\"small-12 columns\">\n                ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"biography", env.opts.autoescape)) {
output += "\n                <p>\n                    ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"biography", env.opts.autoescape),240), env.opts.autoescape);
output += "\n                </p>\n                ";
;
}
output += "\n\n                ";
if(runtime.contextOrFrameLookup(context, frame, "debug")) {
output += "\n                <p>\n                    <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "</a>\n                </p>\n                <p>\n                    <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "</a>\n                </p>\n                ";
;
}
output += "\n\n            </div>\n        </div>\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)) {
output += "\n        <div class=\"row tags text-left\">\n            <div class=\"small-12 columns\">\n                ";
frame = frame.push();
var t_4 = (lineno = 62, colno = 45, runtime.callWrap(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)),"split", env.opts.autoescape), "item[\"d_tags\"][\"split\"]", [","]));
if(t_4) {var t_3 = t_4.length;
for(var t_2=0; t_2 < t_4.length; t_2++) {
var t_5 = t_4[t_2];
frame.set("tag", t_5);
frame.set("loop.index", t_2 + 1);
frame.set("loop.index0", t_2);
frame.set("loop.revindex", t_3 - t_2);
frame.set("loop.revindex0", t_3 - t_2 - 1);
frame.set("loop.first", t_2 === 0);
frame.set("loop.last", t_2 === t_3 - 1);
frame.set("loop.length", t_3);
output += "\n                ";
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.opts.autoescape)) {
output += "<span class=\"tag\">";
output += runtime.suppressValue(t_5, env.opts.autoescape);
output += "</span>";
;
}
output += "\n                ";
;
}
}
frame = frame.pop();
output += "\n            </div>\n        </div>\n        ";
;
}
output += "\n\n    </div>\n";
;
}
cb(null, output);
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
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["item_author.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var t_1;
t_1 = runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"user_co_profile", env.opts.autoescape);
frame.set("item", t_1, true);
if(!frame.parent) {
context.setVariable("item", t_1);
context.addExport("item");
}
output += "\n\n";
if(runtime.contextOrFrameLookup(context, frame, "item")) {
output += "\n    <div data-ct=\"author\" class=\"ct-panel\">\n\n        <div class=\"row header\">\n\n\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"image", env.opts.autoescape)) {
output += "\n            <div class=\"small-6 columns\">\n                <img src=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"image", env.opts.autoescape), env.opts.autoescape);
output += "\">\n            </div>\n            ";
;
}
output += "\n\n\n            <div class=\"";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"image", env.opts.autoescape)) {
output += "small-6";
;
}
else {
output += "small-12";
;
}
output += " columns\">\n                <div class=\"text-left\">\n                    <h1>";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"display_name", env.opts.autoescape),24), env.opts.autoescape);
output += "</h1>\n                    <ul class=\"no-bullet\">\n\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pseudonym", env.opts.autoescape)) {
output += "\n                        <li>\n                            ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pseudonym", env.opts.autoescape), env.opts.autoescape);
output += "\n                        </li>\n                        ";
;
}
output += "\n\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"city", env.opts.autoescape) || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)) {
output += "\n                        <li>\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"city", env.opts.autoescape)) {
output += "\n                                ";
output += runtime.suppressValue(env.getFilter("capitalize").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"city", env.opts.autoescape)), env.opts.autoescape);
output += "\n                            ";
;
}
output += "\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"city", env.opts.autoescape) && runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)) {
output += ", ";
;
}
output += "\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)) {
output += "\n                                ";
output += runtime.suppressValue(env.getFilter("capitalize").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)), env.opts.autoescape);
output += "\n                            ";
;
}
output += "\n                        </li>\n                        ";
;
}
output += "\n\n\n\n                    </ul>\n                </div>\n            </div>\n        </div>\n\n        <div class=\"row body\">\n            <div class=\"small-12 columns\">\n                ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"biography", env.opts.autoescape)) {
output += "\n                <p>\n                    ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"biography", env.opts.autoescape),240), env.opts.autoescape);
output += "\n                </p>\n                ";
;
}
output += "\n            </div>\n        </div>\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)) {
output += "\n        <div class=\"row tags text-left\">\n            <div class=\"small-12 columns\">\n                ";
frame = frame.push();
var t_4 = (lineno = 58, colno = 45, runtime.callWrap(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)),"split", env.opts.autoescape), "item[\"d_tags\"][\"split\"]", [", "]));
if(t_4) {var t_3 = t_4.length;
for(var t_2=0; t_2 < t_4.length; t_2++) {
var t_5 = t_4[t_2];
frame.set("tag", t_5);
frame.set("loop.index", t_2 + 1);
frame.set("loop.index0", t_2);
frame.set("loop.revindex", t_3 - t_2);
frame.set("loop.revindex0", t_3 - t_2 - 1);
frame.set("loop.first", t_2 === 0);
frame.set("loop.last", t_2 === t_3 - 1);
frame.set("loop.length", t_3);
output += "\n                <span class=\"tag\">";
output += runtime.suppressValue(t_5, env.opts.autoescape);
output += "</span>\n                ";
;
}
}
frame = frame.pop();
output += "\n            </div>\n        </div>\n        ";
;
}
output += "\n\n    </div>\n";
;
}
cb(null, output);
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
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["item_label.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var t_1;
t_1 = runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"label", env.opts.autoescape);
frame.set("item", t_1, true);
if(!frame.parent) {
context.setVariable("item", t_1);
context.addExport("item");
}
output += "\n\n";
if(runtime.contextOrFrameLookup(context, frame, "item")) {
output += "\n    <div data-ct=\"label\" class=\"ct-panel\">\n\n        <div class=\"row header\">\n            <div class=\"small-6 columns\">\n                ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape)) {
output += "\n                <img src=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape), env.opts.autoescape);
output += "\">\n                ";
;
}
else {
output += "\n                <span>*</span>\n                ";
;
}
output += "\n            </div>\n            <div class=\"small-6 columns\">\n                <div class=\"text-left\">\n                    <h1>";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name", env.opts.autoescape),24), env.opts.autoescape);
output += "</h1>\n                    <ul class=\"no-bullet\">\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasetype", env.opts.autoescape) || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)) {
output += "\n                        <li>\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)) {
output += "\n                                (";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape), env.opts.autoescape);
output += ")\n                            ";
;
}
output += "\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasetype", env.opts.autoescape)) {
output += "\n                                ";
output += runtime.suppressValue(env.getFilter("capitalize").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasetype", env.opts.autoescape)), env.opts.autoescape);
output += "\n                            ";
;
}
output += "\n                        </li>\n                        ";
;
}
output += "\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasedate_approx", env.opts.autoescape)) {
output += "\n                        <li>\n                            ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasedate_approx", env.opts.autoescape), env.opts.autoescape);
output += "\n                        </li>\n                        ";
;
}
output += "\n                    </ul>\n                </div>\n            </div>\n        </div>\n\n        <div class=\"row body\">\n            <div class=\"small-12 columns\">\n                ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"description", env.opts.autoescape)) {
output += "\n                <p>\n                    ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"description", env.opts.autoescape),240), env.opts.autoescape);
output += "\n                </p>\n                ";
;
}
output += "\n\n\n                ";
if(runtime.contextOrFrameLookup(context, frame, "debug")) {
output += "\n                <p>\n                    <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "</a>\n                </p>\n                <p>\n                    <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "</a>\n                </p>\n                ";
;
}
output += "\n\n            </div>\n        </div>\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)) {
output += "\n        <div class=\"row tags text-left\">\n            <div class=\"small-12 columns\">\n                ";
frame = frame.push();
var t_4 = (lineno = 61, colno = 45, runtime.callWrap(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)),"split", env.opts.autoescape), "item[\"d_tags\"][\"split\"]", [", "]));
if(t_4) {var t_3 = t_4.length;
for(var t_2=0; t_2 < t_4.length; t_2++) {
var t_5 = t_4[t_2];
frame.set("tag", t_5);
frame.set("loop.index", t_2 + 1);
frame.set("loop.index0", t_2);
frame.set("loop.revindex", t_3 - t_2);
frame.set("loop.revindex0", t_3 - t_2 - 1);
frame.set("loop.first", t_2 === 0);
frame.set("loop.last", t_2 === t_3 - 1);
frame.set("loop.length", t_3);
output += "\n                <span class=\"tag\">";
output += runtime.suppressValue(t_5, env.opts.autoescape);
output += "</span>\n                ";
;
}
}
frame = frame.pop();
output += "\n            </div>\n        </div>\n        ";
;
}
output += "\n\n    </div>\n";
;
}
cb(null, output);
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
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["item_media.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var t_1;
t_1 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape);
frame.set("item", t_1, true);
if(!frame.parent) {
context.setVariable("item", t_1);
context.addExport("item");
}
output += "\n\n<div data-ct=\"media\" class=\"ct-panel\">\n\n    <div class=\"row header\">\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"release", env.opts.autoescape) && runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"release", env.opts.autoescape)),"main_image", env.opts.autoescape)) {
output += "\n        <div class=\"small-6 columns\">\n            <img src=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"release", env.opts.autoescape)),"main_image", env.opts.autoescape), env.opts.autoescape);
output += "\">\n        </div>\n        ";
;
}
output += "\n\n        <div class=\"";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"release", env.opts.autoescape) && runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"release", env.opts.autoescape)),"main_image", env.opts.autoescape)) {
output += "small-6";
;
}
else {
output += "small-12";
;
}
output += " columns\">\n            <div class=\"text-left\">\n                <h1>";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name", env.opts.autoescape)) {
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name", env.opts.autoescape),24), env.opts.autoescape);
;
}
output += "</h1>\n                <ul class=\"no-bullet\">\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"mediatype", env.opts.autoescape) || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"version", env.opts.autoescape)) {
output += "\n                    <li>\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"mediatype", env.opts.autoescape)) {
output += "\n                            ";
output += runtime.suppressValue(env.getFilter("capitalize").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"mediatype", env.opts.autoescape)), env.opts.autoescape);
output += "\n                        ";
;
}
output += "\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"version", env.opts.autoescape)) {
output += "\n                            (";
output += runtime.suppressValue(env.getFilter("capitalize").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"version", env.opts.autoescape)), env.opts.autoescape);
output += ")\n                        ";
;
}
output += "\n                    </li>\n                    ";
;
}
output += "\n                    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"duration", env.opts.autoescape)) {
output += "\n                    <li>\n                        ";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"duration", env.opts.autoescape)), env.opts.autoescape);
output += "\n                    </li>\n                    ";
;
}
output += "\n                </ul>\n            </div>\n        </div>\n    </div>\n\n    <div class=\"row body\">\n        <div class=\"small-12 columns\">\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"description", env.opts.autoescape)) {
output += "\n            <p>\n                ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"description", env.opts.autoescape),240), env.opts.autoescape);
output += "\n            </p>\n            ";
;
}
output += "\n        </div>\n    </div>\n\n    ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)) {
output += "\n    <div class=\"row tags text-left\">\n        <div class=\"small-12 columns\">\n            ";
frame = frame.push();
var t_4 = (lineno = 49, colno = 41, runtime.callWrap(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)),"split", env.opts.autoescape), "item[\"d_tags\"][\"split\"]", [","]));
if(t_4) {var t_3 = t_4.length;
for(var t_2=0; t_2 < t_4.length; t_2++) {
var t_5 = t_4[t_2];
frame.set("tag", t_5);
frame.set("loop.index", t_2 + 1);
frame.set("loop.index0", t_2);
frame.set("loop.revindex", t_3 - t_2);
frame.set("loop.revindex0", t_3 - t_2 - 1);
frame.set("loop.first", t_2 === 0);
frame.set("loop.last", t_2 === t_3 - 1);
frame.set("loop.length", t_3);
output += "\n            ";
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.opts.autoescape)) {
output += "<span class=\"tag\">";
output += runtime.suppressValue(t_5, env.opts.autoescape);
output += "</span>";
;
}
output += "\n            ";
;
}
}
frame = frame.pop();
output += "\n        </div>\n    </div>\n    ";
;
}
output += "\n\n</div>";
cb(null, output);
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
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["item_playlist.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var t_1;
t_1 = runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"content_object", env.opts.autoescape);
frame.set("item", t_1, true);
if(!frame.parent) {
context.setVariable("item", t_1);
context.addExport("item");
}
output += "\n\n";
if(runtime.contextOrFrameLookup(context, frame, "item")) {
output += "\n    <div data-ct=\"playlist\" class=\"ct-panel\">\n\n        <div class=\"row header\">\n\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape)) {
output += "\n            <div class=\"small-6 columns\">\n                <img src=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape), env.opts.autoescape);
output += "\">\n            </div>\n            ";
;
}
output += "\n\n            <div class=\"";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape)) {
output += "small-6";
;
}
else {
output += "small-12";
;
}
output += " columns\">\n                <div class=\"text-left\">\n                    <h1>";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name", env.opts.autoescape),24), env.opts.autoescape);
output += "</h1>\n                    <ul class=\"no-bullet\">\n\n                        <li>\n                            ";
output += runtime.suppressValue(env.getFilter("datetime2hhmm").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"time_start", env.opts.autoescape)), env.opts.autoescape);
output += "\n                            -\n                            ";
output += runtime.suppressValue(env.getFilter("datetime2hhmm").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"time_end", env.opts.autoescape)), env.opts.autoescape);
output += "\n                        </li>\n\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"duration", env.opts.autoescape)) {
output += "\n                        <li>\n                            ";
output += runtime.suppressValue(env.getFilter("ms2time").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"duration", env.opts.autoescape)), env.opts.autoescape);
output += "\n                        </li>\n                        ";
;
}
output += "\n                    </ul>\n                </div>\n            </div>\n        </div>\n\n        <div class=\"row body\">\n            <div class=\"small-12 columns\">\n                ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"description", env.opts.autoescape)) {
output += "\n                <p>\n                    ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"description", env.opts.autoescape),240), env.opts.autoescape);
output += "\n                </p>\n                ";
;
}
output += "\n\n\n                ";
if(runtime.contextOrFrameLookup(context, frame, "debug")) {
output += "\n                <p>\n                    <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "</a>\n                </p>\n                <p>\n                    <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"resource_uri", env.opts.autoescape), env.opts.autoescape);
output += "</a>\n                </p>\n                ";
;
}
output += "\n\n            </div>\n        </div>\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)) {
output += "\n        <div class=\"row tags text-left\">\n            <div class=\"small-12 columns\">\n                ";
frame = frame.push();
var t_4 = (lineno = 58, colno = 45, runtime.callWrap(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)),"split", env.opts.autoescape), "item[\"d_tags\"][\"split\"]", [","]));
if(t_4) {var t_3 = t_4.length;
for(var t_2=0; t_2 < t_4.length; t_2++) {
var t_5 = t_4[t_2];
frame.set("tag", t_5);
frame.set("loop.index", t_2 + 1);
frame.set("loop.index0", t_2);
frame.set("loop.revindex", t_3 - t_2);
frame.set("loop.revindex0", t_3 - t_2 - 1);
frame.set("loop.first", t_2 === 0);
frame.set("loop.last", t_2 === t_3 - 1);
frame.set("loop.length", t_3);
output += "\n                ";
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.opts.autoescape)) {
output += "<span class=\"tag\">";
output += runtime.suppressValue(t_5, env.opts.autoescape);
output += "</span>";
;
}
output += "\n                ";
;
}
}
frame = frame.pop();
output += "\n            </div>\n        </div>\n        ";
;
}
output += "\n\n    </div>\n";
;
}
cb(null, output);
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
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["item_release.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var t_1;
t_1 = runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape);
frame.set("item", t_1, true);
if(!frame.parent) {
context.setVariable("item", t_1);
context.addExport("item");
}
output += "\n\n";
if(runtime.contextOrFrameLookup(context, frame, "item")) {
output += "\n    <div data-ct=\"release\" class=\"ct-panel\">\n\n        <div class=\"row header\">\n\n            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape)) {
output += "\n            <div class=\"small-6 columns\">\n                <img src=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape), env.opts.autoescape);
output += "\">\n            </div>\n            ";
;
}
output += "\n\n            <div class=\"";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"main_image", env.opts.autoescape)) {
output += "small-6";
;
}
else {
output += "small-12";
;
}
output += " columns\">\n                <div class=\"text-left\">\n                    <h1>";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name", env.opts.autoescape),32), env.opts.autoescape);
output += "</h1>\n                    <ul class=\"no-bullet\">\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasetype", env.opts.autoescape) || runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)) {
output += "\n                        <li>\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape)) {
output += "\n                                (";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"country", env.opts.autoescape), env.opts.autoescape);
output += ")\n                            ";
;
}
output += "\n                            ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasetype", env.opts.autoescape)) {
output += "\n                                ";
output += runtime.suppressValue(env.getFilter("capitalize").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasetype", env.opts.autoescape)), env.opts.autoescape);
output += "\n                            ";
;
}
output += "\n                        </li>\n                        ";
;
}
output += "\n                        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasedate_approx", env.opts.autoescape)) {
output += "\n                        <li>\n                            ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"releasedate_approx", env.opts.autoescape), env.opts.autoescape);
output += "\n                        </li>\n                        ";
;
}
output += "\n                    </ul>\n                </div>\n            </div>\n\n        </div>\n\n        <div class=\"row body\">\n            <div class=\"small-12 columns\">\n                ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"description", env.opts.autoescape)) {
output += "\n                <p>\n                    ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"description", env.opts.autoescape),240), env.opts.autoescape);
output += "\n                </p>\n                ";
;
}
output += "\n            </div>\n        </div>\n\n        ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)) {
output += "\n        <div class=\"row tags text-left\">\n            <div class=\"small-12 columns\">\n                ";
frame = frame.push();
var t_4 = (lineno = 51, colno = 45, runtime.callWrap(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"d_tags", env.opts.autoescape)),"split", env.opts.autoescape), "item[\"d_tags\"][\"split\"]", [","]));
if(t_4) {var t_3 = t_4.length;
for(var t_2=0; t_2 < t_4.length; t_2++) {
var t_5 = t_4[t_2];
frame.set("tag", t_5);
frame.set("loop.index", t_2 + 1);
frame.set("loop.index0", t_2);
frame.set("loop.revindex", t_3 - t_2);
frame.set("loop.revindex0", t_3 - t_2 - 1);
frame.set("loop.first", t_2 === 0);
frame.set("loop.last", t_2 === t_3 - 1);
frame.set("loop.length", t_3);
output += "\n                ";
if(!runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "loop")),"last", env.opts.autoescape)) {
output += "<span class=\"tag\">";
output += runtime.suppressValue(t_5, env.opts.autoescape);
output += "</span>";
;
}
output += "\n                ";
;
}
}
frame = frame.pop();
output += "\n            </div>\n        </div>\n        ";
;
}
output += "\n\n    </div>\n";
;
}
cb(null, output);
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
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["meta.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<!-- TODO: implement better responsive/mobile handling -->\n\n\n\n<div class=\"show-for-small-only\">\n    <!-- track related -->\n    <p class=\"text-center\">\n        <a target=\"_blank\" data-ct=\"artist\"\n           href=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"artist", env.opts.autoescape)),"absolute_url", env.opts.autoescape), env.opts.autoescape);
output += "\">\n            ";
output += runtime.suppressValue(env.getFilter("shorten").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"artist", env.opts.autoescape)),"name", env.opts.autoescape),30), env.opts.autoescape);
output += "\n        </a>\n        <br>\n        <a target=\"_blank\" data-ct=\"media\"\n           href=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"absolute_url", env.opts.autoescape), env.opts.autoescape);
output += "\">\n            ";
output += runtime.suppressValue(env.getFilter("shorten").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"name", env.opts.autoescape),30), env.opts.autoescape);
output += "\n        </a>\n    </p>\n\n</div>\n\n\n\n<div class=\"show-for-medium-up\">\n    <!-- playlist related -->\n    <dl>\n        <dt>Playlist</dt>\n        <dd>\n            <a target=\"_blank\" data-ct=\"playlist\"\n               href=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"content_object", env.opts.autoescape)),"absolute_url", env.opts.autoescape), env.opts.autoescape);
output += "\"\n               title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"content_object", env.opts.autoescape)),"name", env.opts.autoescape), env.opts.autoescape);
output += "\">\n                ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"content_object", env.opts.autoescape)),"name", env.opts.autoescape),32), env.opts.autoescape);
output += "&nbsp;\n            </a>\n        </dd>\n\n        <dt>by</dt>\n        <dd>\n            <a target=\"_blank\" data-ct=\"author\"\n               href=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"user_co", env.opts.autoescape)),"absolute_url", env.opts.autoescape), env.opts.autoescape);
output += "\">\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"user_co", env.opts.autoescape)),"full_name", env.opts.autoescape)) {
output += "\n                    ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"user_co", env.opts.autoescape)),"full_name", env.opts.autoescape),32), env.opts.autoescape);
output += " (";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"user_co", env.opts.autoescape)),"username", env.opts.autoescape), env.opts.autoescape);
output += ")\n                ";
;
}
else {
output += "\n                    ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"emission", env.opts.autoescape)),"user_co", env.opts.autoescape)),"username", env.opts.autoescape), env.opts.autoescape);
output += "\n                ";
;
}
output += "&nbsp;\n            </a>\n        </dd>\n\n        <dt>Airtime</dt>\n        <dd>\n            <span>";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start", env.opts.autoescape),"time_s"), env.opts.autoescape);
output += "</span>\n            -\n            <span>";
output += runtime.suppressValue(env.getFilter("format_datetime").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_end", env.opts.autoescape),"time_s"), env.opts.autoescape);
output += "</span>\n        </dd>\n    </dl>\n\n    <div class=\"separator\"></div>\n\n    <!-- track related -->\n    <dl>\n        <dt>Song</dt>\n        <dd>\n            <a target=\"_blank\" data-ct=\"media\"\n               href=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"absolute_url", env.opts.autoescape), env.opts.autoescape);
output += "\"\n               title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"name", env.opts.autoescape), env.opts.autoescape);
output += "\">\n                ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"name", env.opts.autoescape),32), env.opts.autoescape);
output += "&nbsp;\n            </a>\n        </dd>\n\n        <dt>by</dt>\n        <dd>\n            <a target=\"_blank\" data-ct=\"artist\"\n               href=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"artist", env.opts.autoescape)),"absolute_url", env.opts.autoescape), env.opts.autoescape);
output += "\"\n               title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"artist", env.opts.autoescape)),"name", env.opts.autoescape), env.opts.autoescape);
output += "\">\n                ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"artist", env.opts.autoescape)),"name", env.opts.autoescape),32), env.opts.autoescape);
output += "&nbsp;\n            </a>\n        </dd>\n\n        <dt>Release</dt>\n        <dd>\n            <a target=\"_blank\" data-ct=\"release\"\n               href=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"absolute_url", env.opts.autoescape), env.opts.autoescape);
output += "\"\n               title=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"name", env.opts.autoescape), env.opts.autoescape);
output += "\">\n                ";
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"name", env.opts.autoescape),22), env.opts.autoescape);
output += "\n\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"country_code", env.opts.autoescape) || runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"releasedate", env.opts.autoescape)) {
output += "(";
;
}
output += "\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"country_code", env.opts.autoescape)) {
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"country_code", env.opts.autoescape), env.opts.autoescape);
;
}
output += "\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"releasedate", env.opts.autoescape)) {
output += runtime.suppressValue(env.getFilter("truncate").call(context, runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"releasedate", env.opts.autoescape),4,false,""), env.opts.autoescape);
;
}
output += "\n                ";
if(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"country_code", env.opts.autoescape) || runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"release", env.opts.autoescape)),"releasedate", env.opts.autoescape)) {
output += ")";
;
}
output += "\n\n                &nbsp;\n            </a>\n        </dd>\n\n        <dt>Label</dt>\n        <dd>\n            <a target=\"_blank\" data-ct=\"label\"\n               href=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "base_url"), env.opts.autoescape);
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"label", env.opts.autoescape)),"absolute_url", env.opts.autoescape), env.opts.autoescape);
output += "\">\n                ";
output += runtime.suppressValue(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"item", env.opts.autoescape)),"label", env.opts.autoescape)),"name", env.opts.autoescape), env.opts.autoescape);
output += "&nbsp;\n            </a>\n        </dd>\n\n    </dl>\n\n\n    <div class=\"separator\"></div>\n</div>\n\n\n\n";
cb(null, output);
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
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["rating.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<h1>---</h1>";
cb(null, output);
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

