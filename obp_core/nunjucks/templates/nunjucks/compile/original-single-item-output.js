(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["apps/onair/static/onair/nj/item.html"] = (function() {function root(env, context, frame, runtime, cb) {
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
env.getTemplate("onair/nj/item_playlist.html", false, "apps/onair/static/onair/nj/item.html", function(t_3,t_1) {
if(t_3) { cb(t_3); return; }
t_1.render(context.getVariables(), frame.push(), function(t_4,t_2) {
if(t_4) { cb(t_4); return; }
output += t_2
output += "\n            ";
env.getTemplate("onair/nj/item_author.html", false, "apps/onair/static/onair/nj/item.html", function(t_7,t_5) {
if(t_7) { cb(t_7); return; }
t_5.render(context.getVariables(), frame.push(), function(t_8,t_6) {
if(t_8) { cb(t_8); return; }
output += t_6
output += "\n            ";
env.getTemplate("onair/nj/item_media.html", false, "apps/onair/static/onair/nj/item.html", function(t_11,t_9) {
if(t_11) { cb(t_11); return; }
t_9.render(context.getVariables(), frame.push(), function(t_12,t_10) {
if(t_12) { cb(t_12); return; }
output += t_10
output += "\n            ";
env.getTemplate("onair/nj/item_artist.html", false, "apps/onair/static/onair/nj/item.html", function(t_15,t_13) {
if(t_15) { cb(t_15); return; }
t_13.render(context.getVariables(), frame.push(), function(t_16,t_14) {
if(t_16) { cb(t_16); return; }
output += t_14
output += "\n            ";
env.getTemplate("onair/nj/item_release.html", false, "apps/onair/static/onair/nj/item.html", function(t_19,t_17) {
if(t_19) { cb(t_19); return; }
t_17.render(context.getVariables(), frame.push(), function(t_20,t_18) {
if(t_20) { cb(t_20); return; }
output += t_18
output += "\n            ";
env.getTemplate("onair/nj/item_label.html", false, "apps/onair/static/onair/nj/item.html", function(t_23,t_21) {
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

