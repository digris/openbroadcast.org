(function() {
var templates = {};
templates["autocomplete.html"] = (function() {
function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += runtime.suppressValue("<div class=\"result\">\n\n\t<div class=\"listing\">\n\t\t");
frame = frame.push();
var t_2 = runtime.contextOrFrameLookup(context, frame, "objects");
for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2.length - t_1);
frame.set("loop.revindex0", t_2.length - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2.length - 1);
frame.set("loop.length", t_2.length);
output += runtime.suppressValue("\n\t\t<div class=\"item hoverable\" data-id=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"id"));
output += runtime.suppressValue("\" data-name=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"name"));
output += runtime.suppressValue("\" data-ct=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"ct"));
output += runtime.suppressValue("\">\n\t\t\t\n\t\t\t<div class=\"row-fluid\">\n\t\t\t\t\n\t\t\t\t<div class=\"span3\">\n\t\t\t\t\t\n\t\t\t\t\t");
if(runtime.suppressLookupValue((t_3),"main_image")) {
output += runtime.suppressValue("\n\t\t\t\t\t<img src=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"main_image"));
output += runtime.suppressValue("\" />\n\t\t\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t\t\t<img src=\"/static/img/base/defaults/listview.");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"ct"));
output += runtime.suppressValue(".xl.png\" width=\"90\" height=\"90\" />\n\t\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span9\">\n\t\t\t\t\t\n\t\t\t\t\t<ul class=\"unstyled\">\n\t\t\t\t\t\t<li><strong>");
output += runtime.suppressValue(env.getFilter("highlight")(runtime.suppressLookupValue((t_3),"name"),runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "meta")),"query")));
output += runtime.suppressValue("</strong>  <small class=\"pull-right\">");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"releasedate"));
output += runtime.suppressValue("</small></li>\n\t\t\t\t\t\t\n\t\t\t\t\t\t");
if(runtime.suppressLookupValue((t_3),"ct") == "release") {
output += runtime.suppressValue("\n\t\t\t\t\t\t<li>");
frame = frame.push();
var t_5 = runtime.suppressLookupValue((t_3),"artist");
for(var t_4=0; t_4 < t_5.length; t_4++) {
var t_6 = t_5[t_4];
frame.set("artist", t_6);
frame.set("loop.index", t_4 + 1);
frame.set("loop.index0", t_4);
frame.set("loop.revindex", t_5.length - t_4);
frame.set("loop.revindex0", t_5.length - t_4 - 1);
frame.set("loop.first", t_4 === 0);
frame.set("loop.last", t_4 === t_5.length - 1);
frame.set("loop.length", t_5.length);
output += runtime.suppressValue(t_6);
if(!runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "loop")),"last")) {
output += runtime.suppressValue(", ");
}
}
frame = frame.pop();
output += runtime.suppressValue("</li>\n\t\t\t\t\t\t<li>Tracks: ");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"media_count"));
output += runtime.suppressValue("</li>\n\t\t\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t\t\t\n\t\t\t\t\t</ul>\n\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\n\t\t</div>\n\t\t");
}
frame = frame.pop();
output += runtime.suppressValue("\n\t</div>\n</div>\n");
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};

})();
templates["importer/nj/importfile.html"] = (function() {
function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += runtime.suppressValue("<div id=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"uuid"));
output += runtime.suppressValue("\" class=\"importfile item ");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status"));
output += runtime.suppressValue("\">\n\n\t<h3>\n\t\t<!--\n\t\t");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"id"));
output += runtime.suppressValue("\n\t\t-->\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "init") {
output += runtime.suppressValue("\n\t\t<i class=\"icon-time\"></i>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "done") {
output += runtime.suppressValue("\n\t\t<i class=\"icon-ok-sign\"></i>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready") {
output += runtime.suppressValue("\n\t\t<i class=\"icon-thumbs-up\"></i>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "working") {
output += runtime.suppressValue("\n\t\t<i class=\"icon-spinner icon-spin\"></i>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += runtime.suppressValue("\n\t\t<i class=\"icon-thumbs-down\"></i>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "duplicate") {
output += runtime.suppressValue("\n\t\t<i class=\"icon-copy\"></i>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "queued") {
output += runtime.suppressValue("\n\t\t<i class=\"icon-spinner icon-spin\"></i>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "importing") {
output += runtime.suppressValue("\n\t\t<i class=\"icon-asterisk icon-spin\"></i>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t\t\n\t\t");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"filename"));
output += runtime.suppressValue(" <small>[");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"mimetype"));
output += runtime.suppressValue("] ");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"id"));
output += runtime.suppressValue("</small>\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "duplicate") {
output += runtime.suppressValue("<span class=\"warning pull-right\">Duplicate</span>");
}
output += runtime.suppressValue("\n\t\t\n\t</h3>\n\t\n\t\n\t\n\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "queued") {
output += runtime.suppressValue("\n\t<div class=\"row-fluid status status-queue\">\n\t\t\n\t\t<div class=\"span1 icon-holder\">&nbsp;</div>\n\n\t\t<div class=\"span8 information\">\n\n\t\t\t<!--<h4>Importing <i class=\"icon icon-padded icon-cogs\"></i></h4>-->\n\t\t\t<p>File placed in the import-queue.<br />Please be patient for a while.</p>\n\t\t\t<p>Depending on server-load and available metadata it can take several minutes per track to complete it's information.</p>\n\t\t\t\n\t\t</div>\n\t\t\n\t\t<div class=\"span3 image\">\n\t\t\t<div class=\"pull-right\">\n\t\t\t\t<i class=\"ajax-loader c3CA3B9\"></i>\n\t\t\t</div>\n\t\t</div>\n\t\t\n\t\t\n\t</div>\n\t");
}
output += runtime.suppressValue("\n\t\n\t\n\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "duplicate") {
output += runtime.suppressValue("\n\t<div class=\"row-fluid result-set status-duplicate\">\n\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")) {
output += runtime.suppressValue("\n\t\t<div class=\"span1\">\n\t\t\t<i class=\"icon icon-padded icon-obp\"></i>\n\t\t</div>\n\t\t\n\t\t<div class=\"span8 information\">\n\t\t\t\n\t\t\t<ul class=\"unstyled\">\n\t\t\t\t<li><strong><a href=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"absolute_url"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"name"));
output += runtime.suppressValue("</a>");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name")) {
output += runtime.suppressValue(" by <a href=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"absolute_url"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name"));
output += runtime.suppressValue("</a>");
}
output += runtime.suppressValue("</strong></li>\n\n\t\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name")) {
output += runtime.suppressValue("\n\t\t\t\t<li><a href=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"absolute_url"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name"));
output += runtime.suppressValue("</a></li>\n\t\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t\t<li>No Release</li>\n\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t\n\t\t\t\t<li class=\"small\">");
output += runtime.suppressValue(env.getFilter("format_timestamp")(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"created")));
output += runtime.suppressValue("</li>\n\n\t\t\t</ul>\n\t\t\t\n\t\t</div>\n\t\t\n\t\t<div class=\"span3 image\">\n\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release") && runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image")) {
output += runtime.suppressValue("\n\t\t\t<img class=\"pull-right\" src=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image"));
output += runtime.suppressValue("\" />\n\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t<img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\" />\n\t\t\t");
}
output += runtime.suppressValue("\n\t\t</div>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t</div>\n\t");
}
output += runtime.suppressValue("\n\t\n\t\n\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "done") {
output += runtime.suppressValue("\n\t<div class=\"row-fluid result-set status-done\">\n\n\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")) {
output += runtime.suppressValue("\n\t\t<div class=\"span1\">\n\t\t\t<i class=\"icon icon-padded icon-obp\"></i>\n\t\t</div>\n\t\t\n\t\t<div class=\"span8 information\">\n\t\t\t\n\t\t\t<ul class=\"unstyled\">\n\t\t\t\t<li><strong><a href=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"absolute_url"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"name"));
output += runtime.suppressValue("</a>");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name")) {
output += runtime.suppressValue(" by <a href=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"absolute_url"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"artist")),"name"));
output += runtime.suppressValue("</a>");
}
output += runtime.suppressValue("</strong></li>\n\n\t\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name")) {
output += runtime.suppressValue("\n\t\t\t\t<li><a href=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"absolute_url"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(env.getFilter("truncate_chars_inner")(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"name"),50));
output += runtime.suppressValue("</a></li>\n\t\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t\t<li>No Release</li>\n\t\t\t\t");
}
output += runtime.suppressValue("\n\n\t\t\t\t<li class=\"small\">");
output += runtime.suppressValue(env.getFilter("format_timestamp")(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"created")));
output += runtime.suppressValue("</li>\n\t\t\t\t\n\t\t\t</ul>\n\t\t\t\n\t\t</div>\n\t\t\n\t\t<div class=\"span3 image\">\n\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release") && runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image")) {
output += runtime.suppressValue("\n\t\t\t<img class=\"pull-right\" src=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"media")),"release")),"main_image"));
output += runtime.suppressValue("\" />\n\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t<img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\" />\n\t\t\t");
}
output += runtime.suppressValue("\n\t\t</div>\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t</div>\n\t");
}
output += runtime.suppressValue("\n\t\n\t\n\n\n\n\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += runtime.suppressValue("\n\t<div class=\"row-fluid result-set hoverable provider-tag\">\n\n\t\t<div class=\"span1\">\n\t\t\t<i class=\"icon icon-padded icon-id3\"></i>\n\t\t</div>\n\n\t\t<div class=\"span4\">\n\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">Title</li>\n\t\t\t\t\t<li class=\"value\" title=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(env.getFilter("truncate_chars_inner")(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_name"),38));
output += runtime.suppressValue("</li>\n\t\t\t\t</ul>\n\t\t\t\t\n\t\t\t<div class=\"clearfix\"></div>\n\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">Release</li>\n\t\t\t\t\t<li class=\"value\" title=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(env.getFilter("truncate_chars_inner")(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_name"),38));
output += runtime.suppressValue("</li>\n\t\t\t\t</ul>\n\n\t\t</div>\n\n\t\t<div class=\"span4\">\n\n\t\t\t<label class=\"checkbox holder-artist_name\">\n\t\t\t\t<input type=\"checkbox\">\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">\n\t\t\t\t\t\tArtist\n\t\t\t\t\t</li>\n\t\t\t\t\t<li class=\"value\" title=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(env.getFilter("truncate_chars_inner")(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"artist_name"),38));
output += runtime.suppressValue("</li>\n\t\t\t\t</ul> </label>\n\t\t\t<div class=\"clearfix\"></div>\n\n\t\t\t<label class=\"checkbox holder-label_name\">\n\t\t\t\t<input type=\"checkbox\">\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">\n\t\t\t\t\t\tLabel\n\t\t\t\t\t</li>\n\t\t\t\t\t<li class=\"value\"></li>\n\t\t\t\t</ul> </label>\n\n\t\t</div>\n\n\t\t<div class=\"span3\">\n\n\t\t\t<label class=\"checkbox holder-media_tracknumber\">\n\t\t\t\t<input type=\"checkbox\">\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">\n\t\t\t\t\t\tTrackNo\n\t\t\t\t\t</li>\n\t\t\t\t\t<li class=\"value\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_tracknumber"));
output += runtime.suppressValue("</li>\n\t\t\t\t</ul> </label>\n\t\t\t<div class=\"clearfix\"></div>\n\n\t\t\t<label class=\"checkbox holder-release_date\">\n\t\t\t\t<input type=\"checkbox\">\n\t\t\t\t<ul class=\"horizontal unstyled\">\n\t\t\t\t\t<li class=\"key\">\n\t\t\t\t\t\tDate\n\t\t\t\t\t</li>\n\t\t\t\t\t<li class=\"value\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"release_date"));
output += runtime.suppressValue("</li>\n\t\t\t\t</ul> </label>\n\n\t\t</div>\n\n\t</div>\n\t");
}
output += runtime.suppressValue("\n\n\n\n\n\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += runtime.suppressValue("\n\t<div class=\"musicbrainz-tag-holder\">\n\t\t\n\t\t\n\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz")),"length") < 1 && runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_tag")),"media_tracknumber")) {
output += runtime.suppressValue("\n\t\t<!--\n\t\t<p>\n\t\t\t<strong>No results available.</strong> \n\t\t\tWould you like to try to <a class=\"rescan\" href=\"#\" data-settings=\"skip_tracknumber, another_setting\">lookup again witouth including the tracknumber</a>?\n\t\t</p>\n\t\t-->\n\t\t");
}
output += runtime.suppressValue("\n\t\t\n\t\t");
frame = frame.push();
var t_2 = runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"results_musicbrainz");
for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("item", t_3);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2.length - t_1);
frame.set("loop.revindex0", t_2.length - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2.length - 1);
frame.set("loop.length", t_2.length);
output += runtime.suppressValue("\n\t\t\n\t\t<div class=\"row-fluid result-set hoverable musicbrainz-tag mb_id-");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"mb_id"));
output += runtime.suppressValue("\">\n\t\n\t\t\t<div class=\"span1\">\n\t\t\t\t<i class=\"icon icon-padded icon-musicbrainz\"></i>\n\t\t\t</div>\n\t\n\t\t\t<div class=\"span8\">\n\t\t\t\t\n\t\t\t\t\t<!-- ids -->\n\t\t\t\t\t<input type=\"hidden\" class=\"media-id\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"media")),"mb_id"));
output += runtime.suppressValue("\">\n\t\t\t\t\t<input type=\"hidden\" class=\"release-id\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"mb_id"));
output += runtime.suppressValue("\">\n\t\t\t\t\t<input type=\"hidden\" class=\"artist-id\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"artist")),"mb_id"));
output += runtime.suppressValue("\">\n\t\t\t\t\t\n\t\t\t\t\t<!-- other data -->\n\t\t\t\t\t<input type=\"hidden\" class=\"releasedate\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"releasedate"));
output += runtime.suppressValue("\">\n\t\t\t\t\t<input type=\"hidden\" class=\"catalognumber\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"label")),"catalognumber"));
output += runtime.suppressValue("\">\n\t\t\t\t\t<input type=\"hidden\" class=\"name\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"media")),"name"));
output += runtime.suppressValue("\">\n\t\t\t\t\t<input type=\"hidden\" class=\"artist\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"artist")),"name"));
output += runtime.suppressValue("\">\n\t\t\t\t\t<input type=\"hidden\" class=\"release\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"name"));
output += runtime.suppressValue("\">\n\t\n\t\t\t\t\t<h5>\n\t\t\t\t\t<a href=\"http://musicbrainz.org/recording/");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"media")),"mb_id"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"media")),"name"));
output += runtime.suppressValue("</a>\n\t\t\t\t\tby\n\t\t\t\t\t<a href=\"http://musicbrainz.org/artist/");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"artist")),"mb_id"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"artist")),"name"));
output += runtime.suppressValue("</a>\n\t\t\t\t\t</h5>\n\t\t\n\t\t\t\t\t<a class=\"external\" href=\"http://musicbrainz.org/release/");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"mb_id"));
output += runtime.suppressValue("\">");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"name"));
output += runtime.suppressValue("</a> \n\t\t\t\t\t<ul class=\"unstyled\">\n\t\t\t\t\t\t<li class=\"small\">");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"country"));
output += runtime.suppressValue(" - ");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"releasedate"));
output += runtime.suppressValue("</li>\n\t\t\t\t\t\t<li class=\"small\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"label")),"name"));
output += runtime.suppressValue(" - ");
output += runtime.suppressValue(runtime.suppressLookupValue((t_3),"catalognumber"));
output += runtime.suppressValue("</li>\n\t\t\t\t\t</ul>\n\t\n\t\t\t</div>\n\t\n\t\t\t<div class=\"span3\">\n\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"relations")),"discogs_image")) {
output += runtime.suppressValue("\n\t\t\t\t<img class=\"pull-right\" src=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((t_3),"relations")),"discogs_image"));
output += runtime.suppressValue("\" />\n\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t\t<img class=\"pull-right\" src=\"/static/img/base/defaults/listview.release.xl.png\" />\n\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t</div>\n\t\t</div>\n\n\t\t\n\t\t");
}
frame = frame.pop();
output += runtime.suppressValue("\n\t\t\n\t\t\n\t</div>\n\t");
}
output += runtime.suppressValue("\n\n\n\n\n\n\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += runtime.suppressValue("\n\t<div class=\"pull-righ result-actions\">\n\n\t\t<form class=\"form-horizontal form-result\">\n\t\t\t<h4>Result</h4>\n\n\t\t\t<!-- name -->\t\t\t\n\t\t\t<div class=\"row-fluid base media ");
if(!runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"name")) {
output += runtime.suppressValue("missing");
}
output += runtime.suppressValue("\">\n\t\t\t\t\n\t\t\t\t<div class=\"span6\">\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Title <span class=\"required\">*</span></label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"release autoupdate\"  data-ct=\"media\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"name"));
output += runtime.suppressValue("\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\n\t\t\t\t\n\t\t\t</div>\n\n\t\t\t<!-- release -->\t\t\t\n\t\t\t<div class=\"row-fluid base release ");
if(!runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"release")) {
output += runtime.suppressValue("missing");
}
output += runtime.suppressValue("\">\n\t\t\t\t\n\t\t\t\t<div class=\"span5\">\n\t\t\t\t\t\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Release <span class=\"required\">*</span></label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"release autocomplete\" data-ct=\"release\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"release"));
output += runtime.suppressValue("\">\n\t\t\t\t\t\t\t<div class=\"ac-result\"></div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id") && !runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_release")) {
output += runtime.suppressValue("\n\t\t\t\t\t\t<a href=\"#\" data-ct=\"release\" data-resource_uri=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_resource_uri"));
output += runtime.suppressValue("\"  class=\"tooltip-inline\">\n\t\t\t\t\t\t\t<i class=\"icon-paper-clip\"></i>\n\t\t\t\t\t\t\tAssigned\n\t\t\t\t\t\t</a>\n\t\t\t\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t\t\t\t<span class=\"dim\"><i class=\"icon-plus\"></i> Create</span>\n\t\t\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id")) {
output += runtime.suppressValue("\n\t\t\t\t\t<input type=\"checkbox\" class=\"force-creation\" ");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_release")) {
output += runtime.suppressValue("checked=\"checked\"");
}
output += runtime.suppressValue("/>\n\t\t\t\t\tForce Creation <a class=\"tooltipable\" data-title=\"Enable this to force the creation of a new entry - even if there is already an item with the same name.\"><i class=\"icon-question-sign\"></i></a>\n\t\t\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t\t\t&nbsp;\n\t\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span3\">\n\t\t\t\t\t<a class=\"btn btn-mini pull-right apply-to-all\" data-ct=\"release\"><i class=\"icon-repeat\"></i> Apply Release to all</a>\n\t\t\t\t</div>\n\n\t\t\t\t\n\t\t\t</div>\n\n\t\t\t<!-- artist -->\t\t\t\n\t\t\t<div class=\"row-fluid base artist ");
if(!runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"artist")) {
output += runtime.suppressValue("missing");
}
output += runtime.suppressValue("\">\n\t\t\t\t\n\t\t\t\t<div class=\"span5\">\n\t\t\t\t\t\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Artist <span class=\"required\">*</span></label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"artist autocomplete\" data-ct=\"artist\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"artist"));
output += runtime.suppressValue("\">\n\t\t\t\t\t\t\t<div class=\"ac-result\"></div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id") && !runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_artist")) {
output += runtime.suppressValue("\n\t\t\t\t\t\t<a href=\"#\" data-ct=\"artist\" data-resource_uri=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_resource_uri"));
output += runtime.suppressValue("\"  class=\"tooltip-inline\">\n\t\t\t\t\t\t\t<i class=\"icon-paper-clip\"></i>\n\t\t\t\t\t\t\tAssigned\n\t\t\t\t\t\t</a>\n\t\t\t\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t\t\t\t<span class=\"dim\"><i class=\"icon-plus\"></i> Create</span>\n\t\t\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span2\">\n\t\t\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id")) {
output += runtime.suppressValue("\n\t\t\t\t\t<input type=\"checkbox\" class=\"force-creation\" ");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"force_artist")) {
output += runtime.suppressValue("checked=\"checked\"");
}
output += runtime.suppressValue("/>\n\t\t\t\t\tForce Creation <a class=\"tooltipable\" data-title=\"Enable this to force the creation of a new entry - even if there is already an item with the same name.\"><i class=\"icon-question-sign\"></i></a>\n\t\t\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t\t\t&nbsp;\n\t\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t\t<div class=\"span3\">\n\t\t\t\t\t<a class=\"btn btn-mini pull-right apply-to-all\" data-ct=\"artist\"><i class=\"icon-repeat\"></i> Apply Artist to all</a>\n\t\t\t\t</div>\n\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t<!--\n\t\t\t<div class=\"row-fluid base\">\n\n\t\t\t\t<div class=\"span6\">\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Title</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"name\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"name"));
output += runtime.suppressValue("\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Release</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"release\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"release"));
output += runtime.suppressValue("\">\n\t\t\t\t\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id")) {
output += runtime.suppressValue("\n\t\t\t\t\t\t\t\t<i class=\"icon-magic\"></i>\n\t\t\t\t\t\t\t\t");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_id"));
output += runtime.suppressValue("\n\t\t\t\t\t\t\t\t");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_release_resource_uri"));
output += runtime.suppressValue("\n\t\t\t\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Release Date</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"releasedate\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"releasedate"));
output += runtime.suppressValue("\">\n\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\n\t\t\t\t<div class=\"span5\">\n\t\t\t\t\t\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputPassword\">Artist</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"artist\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"artist"));
output += runtime.suppressValue("\">\n\t\t\t\t\t\t\t");
if(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id")) {
output += runtime.suppressValue("\n\t\t\t\t\t\t\t\t");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"alibrary_artist_id"));
output += runtime.suppressValue("\n\t\t\t\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Track Number</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" class=\"tracknumber\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"tracknumber"));
output += runtime.suppressValue("\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\n\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Label</label>\n\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t<input type=\"text\" id=\"inputEmail\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"label"));
output += runtime.suppressValue("\">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t\n\t\t\t\t</div>\n\n\t\t\t</div>\n\t\t\t-->\n\n\t\t\t<div class=\"toggle\">\n\t\t\t\t<div class=\"row-fluid\">\n\t\t\t\t\t<div class=\"span12\">\n\t\t\t\t\t\t<a class=\"toggle-advanced pull-right\">More&nbsp;<i class=\"icon-angle-down\"></i></a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\t\t\t<div class=\"advanced-fields\">\n\t\t\t\t\n\t\t\t\t<h4>Musicbrainz IDs</h4>\n\n\t\t\t\t<div class=\"row-fluid musicbrainz\">\n\t\n\t\t\t\t\t<div class=\"span6\">\n\t\n\t\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Track ID</label>\n\t\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t\t<input type=\"text\" class=\"mb-track-id input-minitext\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"mb_track_id"));
output += runtime.suppressValue("\" readonly=\"readonly\">\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\n\t\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t\t<label class=\"control-label\" for=\"inputEmail\">Artist ID</label>\n\t\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t\t<input type=\"text\" class=\"mb-artist-id input-minitext\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"mb_artist_id"));
output += runtime.suppressValue("\" readonly=\"readonly\">\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\n\t\t\t\t\t</div>\n\t\n\t\t\t\t\t<div class=\"span5\">\n\t\t\t\t\t\t\n\t\t\t\t\t\t<div class=\"control-group\">\n\t\t\t\t\t\t\t<label class=\"control-label\" for=\"inputPassword\">Release ID</label>\n\t\t\t\t\t\t\t<div class=\"controls\">\n\t\t\t\t\t\t\t\t<input type=\"text\" class=\"mb-release-id input-minitext\" value=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"import_tag")),"mb_release_id"));
output += runtime.suppressValue("\" readonly=\"readonly\">\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\n\t\t\t\t\t</div>\n\t\n\t\t\t\t</div>\n\t\t\t\n\t\t\t\n\t\t\t</div>\n\n\t\t</form>\n\n\t</div>\n\n\t<div class=\"row-fluid pull-righ result-actions\">\n\n\t\t<div class=\"span8\">\n\t\t\t&nbsp;\n\t\t</div>\n\n\t\t<div class=\"pull-right span4\">\n\t\t\t<a class=\"btn btn-secondary btn-small delete-importfile\">Delete this File</a>\n\t\t\t\n\t\t\t<a class=\"btn btn-secondary btn-small rescan\" data-settings=\"skip_tracknumber\">Scan witouth tracknumber</a>\n\t\t\t\n\t\t\t<a class=\"btn btn-secondary btn-small rescan\">Scan again</a>\n\t\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "ready" || runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "object")),"status") == "warning") {
output += runtime.suppressValue("\n\t\t\t<a class=\"btn btn-primary btn-small start-import\">Start Import</a>\n\t\t\t");
}
output += runtime.suppressValue("\n\t\t</div>\n\t</div>\n\t\n\t\n\t");
}
output += runtime.suppressValue("\n\n</div>");
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};

})();
templates["importer/nj/popover.html"] = (function() {
function root(env, context, frame, runtime) {
var lineno = null;
var colno = null;
var output = "";
try {
output += runtime.suppressValue("<div class=\"po-inline\">\n\t\n\t\n\n\n\t<div class=\"row-fluid\">\n\t\t\n\t\t<div class=\"span2\">\n\t\t\t");
if(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "item")),"main_image")) {
output += runtime.suppressValue("\n\t\t\t<img src=\"");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "item")),"main_image"));
output += runtime.suppressValue("\" />\n\t\t\t");
}
else {
output += runtime.suppressValue("\n\t\t\t<img src=\"/static/img/base/defaults/listview.release.xl.png\" />\n\t\t\t");
}
output += runtime.suppressValue("\n\t\t</div>\n\t\t\n\t\t<div class=\"span10\">\n\t\t\t\t<ul class=\"unstyled\">\n\t\t\t\t\t<li><strong>");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "item")),"name"));
output += runtime.suppressValue("</strong> <small class=\"pull-right\">");
output += runtime.suppressValue(runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "item")),"releasedate"));
output += runtime.suppressValue("</small></li>\n\t\t\t\t\t");
if(runtime.contextOrFrameLookup(context, frame, "artist")) {
output += runtime.suppressValue("\n\t\t\t\t\t<li>");
frame = frame.push();
var t_2 = runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "item")),"artist");
for(var t_1=0; t_1 < t_2.length; t_1++) {
var t_3 = t_2[t_1];
frame.set("artist", t_3);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2.length - t_1);
frame.set("loop.revindex0", t_2.length - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2.length - 1);
frame.set("loop.length", t_2.length);
output += runtime.suppressValue(t_3);
if(!runtime.suppressLookupValue((runtime.contextOrFrameLookup(context, frame, "loop")),"last")) {
output += runtime.suppressValue(", ");
}
}
frame = frame.pop();
output += runtime.suppressValue("</li>\n\t\t\t\t\t");
}
output += runtime.suppressValue("\n\t\t\t\t</ul>\n\t\t</div>\n\t\t\n\t</div>\n\t\n\n\t<div class=\"alert alert-info\">\n\t<p>Track will be added to this item. If this is not desired, please choose \"Force Creation\"</p>\n\t</div>\n\n</div>");
return output;
} catch (e) {
  runtime.handleError(e, lineno, colno);
}
}
return {
root: root
};

})();
nunjucks.env = new nunjucks.Environment([]);
nunjucks.env.registerPrecompiled(templates);
})()
