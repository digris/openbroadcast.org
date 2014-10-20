(function() {
var templates = {};
templates["abcast/nj/autocomplete.html"] = (function() {
function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"result\">\n\n\t<div class=\"listing\">\n\t\t";
frame = frame.push();
var t_2 = runtime.contextOrFrameLookup(context, frame, "objects");
if(t_2 !== undefined) {for(var t_1=0; t_1 < t_2.length; t_1++) {
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
output += runtime.suppressValue(env.getFilter("highlight")(env.getFilter("truncate_chars_inner")(runtime.memberLookup((t_3),"name", env.autoesc),30),runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "meta")),"query", env.autoesc)), env.autoesc);
output += "</strong>  <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((t_3),"releasedate", env.autoesc), env.autoesc);
output += "</small></li>\n\t\t\t\t\t\t<li>\n\t\t\t\t\t\t\t<span>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"user", env.autoesc), env.autoesc);
output += "</span>\n\t\t\t\t\t\t\t|\n\t\t\t\t\t\t\t<span>";
output += runtime.suppressValue(runtime.memberLookup((t_3),"target_duration", env.autoesc) / 60, env.autoesc);
output += " min</span>\n\t\t\t\t\t\t</li>\n\t\t\t\t\t\t<li><span>";
output += runtime.suppressValue(env.getFilter("shorten")(runtime.memberLookup((t_3),"tags", env.autoesc),30), env.autoesc);
output += "</span></li>\n\t\t\t\t\t\t<!--\n\t\t\t\t\t\t";
if(runtime.memberLookup((t_3),"ct", env.autoesc) == "playlist") {
output += "\n\t\t\t\t\t\t";
frame = frame.push();
var t_5 = runtime.memberLookup((t_3),"media", env.autoesc);
if(t_5 !== undefined) {for(var t_4=0; t_4 < t_5.length; t_4++) {
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

})();
templates["abcast/nj/col_day.html"] = (function() {
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

})();
templates["abcast/nj/emission.html"] = (function() {
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

})();
templates["abcast/nj/emission_popup.html"] = (function() {
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
output += runtime.suppressValue(env.getFilter("format_datetime")(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start", env.autoesc),"time"), env.autoesc);
output += " - ";
output += runtime.suppressValue(env.getFilter("format_datetime")(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_end", env.autoesc),"time"), env.autoesc);
output += " | ";
output += runtime.suppressValue(env.getFilter("format_datetime")(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"time_start", env.autoesc),"date"), env.autoesc);
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

})();
templates["abcast/nj/selected_object.html"] = (function() {
function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "\n<h4>Selected for scheduling</h4>\n<p>Drag and drop to a free slot</p>\n\n<div class=\"object-search\">\n\t<input class=\"autocomplete\" data-ct=\"playlist\" type=\"text\" placeholder=\"Search broadcasts\">\n\t<div class=\"ac-result\"></div>\n</div>\n\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"id", env.autoesc)) {
output += "\n<div class=\"_container object-to-schedule\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"uuid", env.autoesc), env.autoesc);
output += "\">\n\t<h4>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"name", env.autoesc), env.autoesc);
output += " <small class=\"pull-right\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"target_duration", env.autoesc) / 60, env.autoesc);
output += " min</small></h4>\n\t<p class=\"tags\">";
output += runtime.suppressValue(env.getFilter("shorten")(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"d_tags", env.autoesc),60), env.autoesc);
output += "</p>\n\t\n\t\n\t<!--\n\t<ul class=\"unstyled item-list\">\n\t";
frame = frame.push();
var t_2 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "object")),"items", env.autoesc);
if(t_2 !== undefined) {for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
output += "\n\t<li>";
output += runtime.suppressValue(env.getFilter("truncate_chars_inner")(runtime.memberLookup((runtime.memberLookup((runtime.memberLookup((t_3),"item", env.autoesc)),"content_object", env.autoesc)),"name", env.autoesc),30), env.autoesc);
output += "</li>\n\t";
}
}frame = frame.pop();
output += "\n\t</ul>\n\t-->\n</div>\n";
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

})();
templates["abcast/nj/top_week.html"] = (function() {
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

})();
if(typeof define === "function" && define.amd) {
    define(["nunjucks"], function(nunjucks) {
        nunjucks.env = new nunjucks.Environment([], null);
        nunjucks.env.registerPrecompiled(templates);
        return nunjucks;
    });
}
else if(typeof nunjucks === "object") {
    nunjucks.env = new nunjucks.Environment([], null);
    nunjucks.env.registerPrecompiled(templates);
}
else {
    console.error("ERROR: You must load nunjucks before the precompiled templates");
}
})();
