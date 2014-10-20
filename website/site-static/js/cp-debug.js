jQuery.fn.extend({everyTime: function (interval, label, fn, times, belay) {
    return this.each(function () {
        jQuery.timer.add(this, interval, label, fn, times, belay);
    });
}, oneTime: function (interval, label, fn) {
    return this.each(function () {
        jQuery.timer.add(this, interval, label, fn, 1);
    });
}, stopTime: function (label, fn) {
    return this.each(function () {
        jQuery.timer.remove(this, label, fn);
    });
}});
jQuery.event.special
jQuery.extend({timer: {global: [], guid: 1, dataKey: "jQuery.timer", regex: /^([0-9]+(?:\.[0-9]*)?)\s*(.*s)?$/, powers: {'ms': 1, 'cs': 10, 'ds': 100, 's': 1000, 'das': 10000, 'hs': 100000, 'ks': 1000000}, timeParse: function (value) {
    if (value == undefined || value == null)
        return null;
    var result = this.regex.exec(jQuery.trim(value.toString()));
    if (result[2]) {
        var num = parseFloat(result[1]);
        var mult = this.powers[result[2]] || 1;
        return num * mult;
    } else {
        return value;
    }
}, add: function (element, interval, label, fn, times, belay) {
    var counter = 0;
    if (jQuery.isFunction(label)) {
        if (!times)
            times = fn;
        fn = label;
        label = interval;
    }
    interval = jQuery.timer.timeParse(interval);
    if (typeof interval != 'number' || isNaN(interval) || interval <= 0)
        return;
    if (times && times.constructor != Number) {
        belay = !!times;
        times = 0;
    }
    times = times || 0;
    belay = belay || false;
    var timers = jQuery.data(element, this.dataKey) || jQuery.data(element, this.dataKey, {});
    if (!timers[label])
        timers[label] = {};
    fn.timerID = fn.timerID || this.guid++;
    var handler = function () {
        if (belay && this.inProgress)
            return;
        this.inProgress = true;
        if ((++counter > times && times !== 0) || fn.call(element, counter) === false)
            jQuery.timer.remove(element, label, fn);
        this.inProgress = false;
    };
    handler.timerID = fn.timerID;
    if (!timers[label][fn.timerID])
        timers[label][fn.timerID] = window.setInterval(handler, interval);
    this.global.push(element);
}, remove: function (element, label, fn) {
    var timers = jQuery.data(element, this.dataKey), ret;
    if (timers) {
        if (!label) {
            for (label in timers)
                this.remove(element, label, fn);
        } else if (timers[label]) {
            if (fn) {
                if (fn.timerID) {
                    window.clearInterval(timers[label][fn.timerID]);
                    delete timers[label][fn.timerID];
                }
            } else {
                for (var fn in timers[label]) {
                    window.clearInterval(timers[label][fn]);
                    delete timers[label][fn];
                }
            }
            for (ret in timers[label])break;
            if (!ret) {
                ret = null;
                delete timers[label];
            }
        }
        for (ret in timers)break;
        if (!ret)
            jQuery.removeData(element, this.dataKey);
    }
}}});
jQuery(window).bind("unload", function () {
    jQuery.each(jQuery.timer.global, function (index, item) {
        jQuery.timer.remove(item);
    });
});
jQuery.cookie = function (name, value, options) {
    if (typeof value != 'undefined') {
        options = options || {};
        if (value === null) {
            value = '';
            options = $.extend({}, options);
            options.expires = -1;
        }
        var expires = '';
        if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
            var date;
            if (typeof options.expires == 'number') {
                date = new Date();
                date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
            } else {
                date = options.expires;
            }
            expires = '; expires=' + date.toUTCString();
        }
        var path = options.path ? '; path=' + (options.path) : '';
        var domain = options.domain ? '; domain=' + (options.domain) : '';
        var secure = options.secure ? '; secure' : '';
        document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
    } else {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
};
(function ($) {
    $.jGrowl = function (m, o) {
        if ($('#jGrowl').size() == 0)
            $('<div id="jGrowl"></div>').addClass($.jGrowl.defaults.position).appendTo('body');
        $('#jGrowl').jGrowl(m, o);
    };
    $.fn.jGrowl = function (m, o) {
        if ($.isFunction(this.each)) {
            var args = arguments;
            return this.each(function () {
                var self = this;
                if ($(this).data('jGrowl.instance') == undefined) {
                    $(this).data('jGrowl.instance', $.extend(new $.fn.jGrowl(), {notifications: [], element: null, interval: null}));
                    $(this).data('jGrowl.instance').startup(this);
                }
                if ($.isFunction($(this).data('jGrowl.instance')[m])) {
                    $(this).data('jGrowl.instance')[m].apply($(this).data('jGrowl.instance'), $.makeArray(args).slice(1));
                } else {
                    $(this).data('jGrowl.instance').create(m, o);
                }
            });
        }
        ;
    };
    $.extend($.fn.jGrowl.prototype, {defaults: {pool: 0, header: '', group: '', sticky: false, position: 'bottom-right', glue: 'after', theme: 'default', corners: '10px', check: 250, life: 3000, speed: 'normal', easing: 'swing', closer: true, closeTemplate: '&times;', closerTemplate: '<div>[ close all ]</div>', log: function (e, m, o) {
    }, beforeOpen: function (e, m, o) {
    }, open: function (e, m, o) {
    }, beforeClose: function (e, m, o) {
    }, close: function (e, m, o) {
    }, animateOpen: {opacity: 'show'}, animateClose: {opacity: 'hide'}}, notifications: [], element: null, interval: null, create: function (message, o) {
        var o = $.extend({}, this.defaults, o);
        this.notifications.push({message: message, options: o});
        o.log.apply(this.element, [this.element, message, o]);
    }, render: function (notification) {
        var self = this;
        var message = notification.message;
        var o = notification.options;
        var notification = $('<div class="jGrowl-notification ui-state-highlight ui-corner-all' +
            ((o.group != undefined && o.group != '') ? ' ' + o.group : '') + '">' + '<div class="close">' + o.closeTemplate + '</div>' + '<div class="header">' + o.header + '</div>' + '<div class="message">' + message + '</div></div>').data("jGrowl", o).addClass(o.theme).children('div.close').bind("click.jGrowl",function () {
                $(this).parent().trigger('jGrowl.close');
            }).parent();
        $(notification).bind("mouseover.jGrowl",function () {
            $('div.jGrowl-notification', self.element).data("jGrowl.pause", true);
        }).bind("mouseout.jGrowl",function () {
            $('div.jGrowl-notification', self.element).data("jGrowl.pause", false);
        }).bind('jGrowl.beforeOpen',function () {
            if (o.beforeOpen.apply(notification, [notification, message, o, self.element]) != false) {
                $(this).trigger('jGrowl.open');
            }
        }).bind('jGrowl.open',function () {
            if (o.open.apply(notification, [notification, message, o, self.element]) != false) {
                if (o.glue == 'after') {
                    $('div.jGrowl-notification:last', self.element).after(notification);
                } else {
                    $('div.jGrowl-notification:first', self.element).before(notification);
                }
                $(this).animate(o.animateOpen, o.speed, o.easing, function () {
                    if ($.browser.msie && (parseInt($(this).css('opacity'), 10) === 1 || parseInt($(this).css('opacity'), 10) === 0))
                        this.style.removeAttribute('filter');
                    $(this).data("jGrowl").created = new Date();
                });
            }
        }).bind('jGrowl.beforeClose',function () {
                if (o.beforeClose.apply(notification, [notification, message, o, self.element]) != false)
                    $(this).trigger('jGrowl.close');
            }).bind('jGrowl.close',function () {
                $(this).data('jGrowl.pause', true);
                $(this).animate(o.animateClose, o.speed, o.easing, function () {
                    $(this).remove();
                    var close = o.close.apply(notification, [notification, message, o, self.element]);
                    if ($.isFunction(close))
                        close.apply(notification, [notification, message, o, self.element]);
                });
            }).trigger('jGrowl.beforeOpen');
        if ($.fn.corner != undefined)$(notification).corner(o.corners);
        if ($('div.jGrowl-notification:parent', self.element).size() > 1 && $('div.jGrowl-closer', self.element).size() == 0 && this.defaults.closer != false) {
            $(this.defaults.closerTemplate).addClass('jGrowl-closer ui-state-highlight ui-corner-all').addClass(this.defaults.theme).appendTo(self.element).animate(this.defaults.animateOpen, this.defaults.speed, this.defaults.easing).bind("click.jGrowl", function () {
                $(this).siblings().children('div.close').trigger("click.jGrowl");
                if ($.isFunction(self.defaults.closer)) {
                    self.defaults.closer.apply($(this).parent()[0], [$(this).parent()[0]]);
                }
            });
        }
        ;
    }, update: function () {
        $(this.element).find('div.jGrowl-notification:parent').each(function () {
            if ($(this).data("jGrowl") != undefined && $(this).data("jGrowl").created != undefined && ($(this).data("jGrowl").created.getTime() + $(this).data("jGrowl").life) < (new Date()).getTime() && $(this).data("jGrowl").sticky != true && ($(this).data("jGrowl.pause") == undefined || $(this).data("jGrowl.pause") != true)) {
                $(this).trigger('jGrowl.beforeClose');
            }
        });
        if (this.notifications.length > 0 && (this.defaults.pool == 0 || $(this.element).find('div.jGrowl-notification:parent').size() < this.defaults.pool))
            this.render(this.notifications.shift());
        if ($(this.element).find('div.jGrowl-notification:parent').size() < 2) {
            $(this.element).find('div.jGrowl-closer').animate(this.defaults.animateClose, this.defaults.speed, this.defaults.easing, function () {
                $(this).remove();
            });
        }
    }, startup: function (e) {
        this.element = $(e).addClass('jGrowl').append('<div class="jGrowl-notification"></div>');
        this.interval = setInterval(function () {
            $(e).data('jGrowl.instance').update();
        }, this.defaults.check);
        if ($.browser.msie && parseInt($.browser.version) < 7 && !window["XMLHttpRequest"]) {
            $(this.element).addClass('ie6');
        }
    }, shutdown: function () {
        $(this.element).removeClass('jGrowl').find('div.jGrowl-notification').remove();
        clearInterval(this.interval);
    }, close: function () {
        $(this.element).find('div.jGrowl-notification').each(function () {
            $(this).trigger('jGrowl.beforeClose');
        });
    }});
    $.jGrowl.defaults = $.fn.jGrowl.prototype.defaults;
})(jQuery);
(function ($) {
    var ajaxQueue = $({});
    $.ajaxQueue = function (ajaxOpts) {
        var jqXHR, dfd = $.Deferred(), promise = dfd.promise();

        function doRequest(next) {
            jqXHR = $.ajax(ajaxOpts);
            jqXHR.done(dfd.resolve).fail(dfd.reject).then(next, next);
        }

        ajaxQueue.queue(doRequest);
        promise.abort = function (statusText) {
            if (jqXHR) {
                return jqXHR.abort(statusText);
            }
            var queue = ajaxQueue.queue(), index = $.inArray(doRequest, queue);
            if (index > -1) {
                queue.splice(index, 1);
            }
            dfd.rejectWith(ajaxOpts.context || ajaxOpts, [promise, statusText, ""]);
            return promise;
        };
        return promise;
    };
})(jQuery);
window.debug = (function () {
    var window = this, aps = Array.prototype.slice, con = window.console, that = {}, callback_func, callback_force, log_level = 9, log_methods = ['error', 'warn', 'info', 'debug', 'log'], pass_methods = 'assert clear count dir dirxml exception group groupCollapsed groupEnd profile profileEnd table time timeEnd trace'.split(' '), idx = pass_methods.length, logs = [];
    while (--idx >= 0) {
        (function (method) {
            that[method] = function () {
                log_level !== 0 && con && con[method] && con[method].apply(con, arguments);
            }
        })(pass_methods[idx]);
    }
    idx = log_methods.length;
    while (--idx >= 0) {
        (function (idx, level) {
            that[level] = function () {
                var args = aps.call(arguments), log_arr = [level].concat(args);
                logs.push(log_arr);
                exec_callback(log_arr);
                if (!con || !is_level(idx)) {
                    return;
                }
                con.firebug ? con[level].apply(window, args) : con[level] ? con[level](args) : con.log(args);
            };
        })(idx, log_methods[idx]);
    }
    function exec_callback(args) {
        if (callback_func && (callback_force || !con || !con.log)) {
            callback_func.apply(window, args);
        }
    };
    that.setLevel = function (level) {
        log_level = typeof level === 'number' ? level : 9;
    };
    function is_level(level) {
        return log_level > 0 ? log_level > level : log_methods.length + log_level <= level;
    };
    that.setCallback = function () {
        var args = aps.call(arguments), max = logs.length, i = max;
        callback_func = args.shift() || null;
        callback_force = typeof args[0] === 'boolean' ? args.shift() : false;
        i -= typeof args[0] === 'number' ? args.shift() : max;
        while (i < max) {
            exec_callback(logs[i++]);
        }
    };
    return that;
})();
(function () {
    var modules = {};
    (function () {
        function extend(cls, name, props) {
            var prototype = Object.create(cls.prototype);
            var fnTest = /xyz/.test(function () {
                xyz;
            }) ? /\bparent\b/ : /.*/;
            props = props || {};
            for (var k in props) {
                var src = props[k];
                var parent = prototype[k];
                if (typeof parent == "function" && typeof src == "function" && fnTest.test(src)) {
                    prototype[k] = (function (src, parent) {
                        return function () {
                            var tmp = this.parent;
                            this.parent = parent;
                            var res = src.apply(this, arguments);
                            this.parent = tmp;
                            return res;
                        };
                    })(src, parent);
                }
                else {
                    prototype[k] = src;
                }
            }
            prototype.typename = name;
            var new_cls = function () {
                if (prototype.init) {
                    prototype.init.apply(this, arguments);
                }
            };
            new_cls.prototype = prototype;
            new_cls.prototype.constructor = new_cls;
            new_cls.extend = function (name, props) {
                if (typeof name == "object") {
                    props = name;
                    name = "anonymous";
                }
                return extend(new_cls, name, props);
            };
            return new_cls;
        }

        modules['object'] = extend(Object, "Object", {});
    })();
    (function () {
        var ArrayProto = Array.prototype;
        var ObjProto = Object.prototype;
        var escapeMap = {'&': '&amp;', '"': '&quot;', "'": '&#39;', "<": '&lt;', ">": '&gt;'};
        var lookupEscape = function (ch) {
            return escapeMap[ch];
        };
        var exports = modules['lib'] = {};
        exports.withPrettyErrors = function (path, withInternals, func) {
            try {
                return func();
            } catch (e) {
                if (!e.Update) {
                    e = new exports.TemplateError(e);
                }
                e.Update(path);
                if (!withInternals) {
                    var old = e;
                    e = new Error(old.message);
                    e.name = old.name;
                }
                throw e;
            }
        }
        exports.TemplateError = function (message, lineno, colno) {
            var err = this;
            if (message instanceof Error) {
                err = message;
                message = message.name + ": " + message.message;
            } else {
                if (Error.captureStackTrace) {
                    Error.captureStackTrace(err);
                }
            }
            err.name = "Template render error";
            err.message = message;
            err.lineno = lineno;
            err.colno = colno;
            err.firstUpdate = true;
            err.Update = function (path) {
                var message = "(" + (path || "unknown path") + ")";
                if (this.firstUpdate) {
                    if (this.lineno && this.colno) {
                        message += ' [Line ' + this.lineno + ', Column ' + this.colno + ']';
                    }
                    else if (this.lineno) {
                        message += ' [Line ' + this.lineno + ']';
                    }
                }
                message += '\n ';
                if (this.firstUpdate) {
                    message += ' ';
                }
                this.message = message + (this.message || '');
                this.firstUpdate = false;
                return this;
            };
            return err;
        };
        exports.TemplateError.prototype = Error.prototype;
        exports.escape = function (val) {
            return val.replace(/[&"'<>]/g, lookupEscape);
        };
        exports.isFunction = function (obj) {
            return ObjProto.toString.call(obj) == '[object Function]';
        };
        exports.isArray = Array.isArray || function (obj) {
            return ObjProto.toString.call(obj) == '[object Array]';
        };
        exports.isString = function (obj) {
            return ObjProto.toString.call(obj) == '[object String]';
        };
        exports.isObject = function (obj) {
            return obj === Object(obj);
        };
        exports.groupBy = function (obj, val) {
            var result = {};
            var iterator = exports.isFunction(val) ? val : function (obj) {
                return obj[val];
            };
            for (var i = 0; i < obj.length; i++) {
                var value = obj[i];
                var key = iterator(value, i);
                (result[key] || (result[key] = [])).push(value);
            }
            return result;
        };
        exports.toArray = function (obj) {
            return Array.prototype.slice.call(obj);
        };
        exports.without = function (array) {
            var result = [];
            if (!array) {
                return result;
            }
            var index = -1, length = array.length, contains = exports.toArray(arguments).slice(1);
            while (++index < length) {
                if (contains.indexOf(array[index]) === -1) {
                    result.push(array[index]);
                }
            }
            return result;
        };
        exports.extend = function (obj, obj2) {
            for (var k in obj2) {
                obj[k] = obj2[k];
            }
            return obj;
        };
        exports.repeat = function (char_, n) {
            var str = '';
            for (var i = 0; i < n; i++) {
                str += char_;
            }
            return str;
        };
        exports.each = function (obj, func, context) {
            if (obj == null) {
                return;
            }
            if (ArrayProto.each && obj.each == ArrayProto.each) {
                obj.forEach(func, context);
            }
            else if (obj.length === +obj.length) {
                for (var i = 0, l = obj.length; i < l; i++) {
                    func.call(context, obj[i], i, obj);
                }
            }
        };
        exports.map = function (obj, func) {
            var results = [];
            if (obj == null) {
                return results;
            }
            if (ArrayProto.map && obj.map === ArrayProto.map) {
                return obj.map(func);
            }
            for (var i = 0; i < obj.length; i++) {
                results[results.length] = func(obj[i], i);
            }
            if (obj.length === +obj.length) {
                results.length = obj.length;
            }
            return results;
        };
    })();
    (function () {
        var util = modules["util"];
        var lib = modules["lib"];
        var Object = modules["object"];

        function traverseAndCheck(obj, type, results) {
            if (obj instanceof type) {
                results.push(obj);
            }
            if (obj instanceof Node) {
                obj.findAll(type, results);
            }
        }

        var Node = Object.extend("Node", {init: function (lineno, colno) {
            this.lineno = lineno;
            this.colno = colno;
            var fields = this.fields;
            for (var i = 0, l = fields.length; i < l; i++) {
                var field = fields[i];
                var val = arguments[i + 2];
                if (val === undefined) {
                    val = null;
                }
                this[field] = val;
            }
        }, findAll: function (type, results) {
            results = results || [];
            if (this instanceof NodeList) {
                var children = this.children;
                for (var i = 0, l = children.length; i < l; i++) {
                    traverseAndCheck(children[i], type, results);
                }
            }
            else {
                var fields = this.fields;
                for (var i = 0, l = fields.length; i < l; i++) {
                    traverseAndCheck(this[fields[i]], type, results);
                }
            }
            return results;
        }, iterFields: function (func) {
            lib.each(this.fields, function (field) {
                func(this[field], field);
            }, this);
        }});
        var Value = Node.extend("Value", {fields: ['value']});
        var NodeList = Node.extend("NodeList", {fields: ['children'], init: function (lineno, colno, nodes) {
            this.parent(lineno, colno, nodes || []);
        }, addChild: function (node) {
            this.children.push(node);
        }});
        var Root = NodeList.extend("Root");
        var Literal = Value.extend("Literal");
        var Symbol = Value.extend("Symbol");
        var Group = NodeList.extend("Group");
        var Array = NodeList.extend("Array");
        var Pair = Node.extend("Pair", {fields: ['key', 'value']});
        var Dict = NodeList.extend("Dict");
        var LookupVal = Node.extend("LookupVal", {fields: ['target', 'val']});
        var If = Node.extend("If", {fields: ['cond', 'body', 'else_']});
        var InlineIf = Node.extend("InlineIf", {fields: ['cond', 'body', 'else_']});
        var For = Node.extend("For", {fields: ['arr', 'name', 'body']});
        var Macro = Node.extend("Macro", {fields: ['name', 'args', 'body']});
        var Import = Node.extend("Import", {fields: ['template', 'target']});
        var FromImport = Node.extend("FromImport", {fields: ['template', 'names'], init: function (lineno, colno, template, names) {
            this.parent(lineno, colno, template, names || new NodeList());
        }});
        var FunCall = Node.extend("FunCall", {fields: ['name', 'args']});
        var Filter = FunCall.extend("Filter");
        var KeywordArgs = Dict.extend("KeywordArgs");
        var Block = Node.extend("Block", {fields: ['name', 'body']});
        var TemplateRef = Node.extend("TemplateRef", {fields: ['template']});
        var Extends = TemplateRef.extend("Extends");
        var Include = TemplateRef.extend("Include");
        var Set = Node.extend("Set", {fields: ['targets', 'value']});
        var Output = NodeList.extend("Output");
        var TemplateData = Literal.extend("TemplateData");
        var UnaryOp = Node.extend("UnaryOp", {fields: ['target']});
        var BinOp = Node.extend("BinOp", {fields: ['left', 'right']});
        var Or = BinOp.extend("Or");
        var And = BinOp.extend("And");
        var Not = UnaryOp.extend("Not");
        var Add = BinOp.extend("Add");
        var Sub = BinOp.extend("Sub");
        var Mul = BinOp.extend("Mul");
        var Div = BinOp.extend("Div");
        var FloorDiv = BinOp.extend("FloorDiv");
        var Mod = BinOp.extend("Mod");
        var Pow = BinOp.extend("Pow");
        var Neg = UnaryOp.extend("Neg");
        var Pos = UnaryOp.extend("Pos");
        var Compare = Node.extend("Compare", {fields: ['expr', 'ops']});
        var CompareOperand = Node.extend("CompareOperand", {fields: ['expr', 'type']});
        var CustomTag = Node.extend("CustomTag", {init: function (lineno, colno, name) {
            this.lineno = lineno;
            this.colno = colno;
            this.name = name;
        }});
        var CallExtension = Node.extend("CallExtension", {fields: ['extName', 'prop', 'args', 'contentArgs'], init: function (ext, prop, args, contentArgs) {
            this.extName = ext._name;
            this.prop = prop;
            this.args = args;
            this.contentArgs = contentArgs;
        }});

        function printNodes(node, indent) {
            indent = indent || 0;
            function print(str, indent, inline) {
                var lines = str.split("\n");
                for (var i = 0; i < lines.length; i++) {
                    if (lines[i]) {
                        if ((inline && i > 0) || !inline) {
                            for (var j = 0; j < indent; j++) {
                                util.print(" ");
                            }
                        }
                    }
                    if (i === lines.length - 1) {
                        util.print(lines[i]);
                    }
                    else {
                        util.puts(lines[i]);
                    }
                }
            }

            print(node.typename + ": ", indent);
            if (node instanceof NodeList) {
                print('\n');
                lib.each(node.children, function (n) {
                    printNodes(n, indent + 2);
                });
            }
            else {
                var nodes = null;
                var props = null;
                node.iterFields(function (val, field) {
                    if (val instanceof Node) {
                        nodes = nodes || {};
                        nodes[field] = val;
                    }
                    else {
                        props = props || {};
                        props[field] = val;
                    }
                });
                if (props) {
                    print(util.inspect(props, true, null) + '\n', null, true);
                }
                else {
                    print('\n');
                }
                if (nodes) {
                    for (var k in nodes) {
                        printNodes(nodes[k], indent + 2);
                    }
                }
            }
        }

        modules['nodes'] = {Node: Node, Root: Root, NodeList: NodeList, Value: Value, Literal: Literal, Symbol: Symbol, Group: Group, Array: Array, Pair: Pair, Dict: Dict, Output: Output, TemplateData: TemplateData, If: If, InlineIf: InlineIf, For: For, Macro: Macro, Import: Import, FromImport: FromImport, FunCall: FunCall, Filter: Filter, KeywordArgs: KeywordArgs, Block: Block, Extends: Extends, Include: Include, Set: Set, LookupVal: LookupVal, BinOp: BinOp, Or: Or, And: And, Not: Not, Add: Add, Sub: Sub, Mul: Mul, Div: Div, FloorDiv: FloorDiv, Mod: Mod, Pow: Pow, Neg: Neg, Pos: Pos, Compare: Compare, CompareOperand: CompareOperand, CallExtension: CallExtension, printNodes: printNodes};
    })();
    (function () {
        var lib = modules["lib"];
        var Object = modules["object"];
        var Frame = Object.extend({init: function (parent) {
            this.variables = {};
            this.parent = parent;
        }, set: function (name, val) {
            var parts = name.split('.');
            var obj = this.variables;
            for (var i = 0; i < parts.length - 1; i++) {
                var id = parts[i];
                if (!obj[id]) {
                    obj[id] = {};
                }
                obj = obj[id];
            }
            obj[parts[parts.length - 1]] = val;
        }, get: function (name) {
            var val = this.variables[name];
            if (val !== undefined && val !== null) {
                return val;
            }
            return null;
        }, lookup: function (name) {
            var p = this.parent;
            var val = this.variables[name];
            if (val !== undefined && val !== null) {
                return val;
            }
            return p && p.lookup(name);
        }, push: function () {
            return new Frame(this);
        }, pop: function () {
            return this.parent;
        }});

        function makeMacro(argNames, kwargNames, func) {
            return function () {
                var argCount = numArgs(arguments);
                var args;
                var kwargs = getKeywordArgs(arguments);
                if (argCount > argNames.length) {
                    args = Array.prototype.slice.call(arguments, 0, argNames.length);
                    var vals = Array.prototype.slice.call(arguments, args.length, argCount);
                    for (var i = 0; i < vals.length; i++) {
                        if (i < kwargNames.length) {
                            kwargs[kwargNames[i]] = vals[i];
                        }
                    }
                    args.push(kwargs);
                }
                else if (argCount < argNames.length) {
                    args = Array.prototype.slice.call(arguments, 0, argCount);
                    for (var i = argCount; i < argNames.length; i++) {
                        var arg = argNames[i];
                        args.push(kwargs[arg]);
                        delete kwargs[arg];
                    }
                    args.push(kwargs);
                }
                else {
                    args = arguments;
                }
                return func.apply(this, args);
            };
        }

        function makeKeywordArgs(obj) {
            obj.__keywords = true;
            return obj;
        }

        function getKeywordArgs(args) {
            var len = args.length;
            if (len) {
                var lastArg = args[len - 1];
                if (lastArg && lastArg.hasOwnProperty('__keywords')) {
                    return lastArg;
                }
            }
            return{};
        }

        function numArgs(args) {
            var len = args.length;
            if (len === 0) {
                return 0;
            }
            var lastArg = args[len - 1];
            if (lastArg && lastArg.hasOwnProperty('__keywords')) {
                return len - 1;
            }
            else {
                return len;
            }
        }

        function SafeString(val) {
            if (typeof val != 'string') {
                return val;
            }
            this.toString = function () {
                return val;
            };
            this.length = val.length;
            var methods = ['charAt', 'charCodeAt', 'concat', 'contains', 'endsWith', 'fromCharCode', 'indexOf', 'lastIndexOf', 'length', 'localeCompare', 'match', 'quote', 'replace', 'search', 'slice', 'split', 'startsWith', 'substr', 'substring', 'toLocaleLowerCase', 'toLocaleUpperCase', 'toLowerCase', 'toUpperCase', 'trim', 'trimLeft', 'trimRight'];
            for (var i = 0; i < methods.length; i++) {
                this[methods[i]] = proxyStr(val[methods[i]]);
            }
        }

        function copySafeness(dest, target) {
            if (dest instanceof SafeString) {
                return new SafeString(target);
            }
            return target.toString();
        }

        function proxyStr(func) {
            return function () {
                var ret = func.apply(this, arguments);
                if (typeof ret == 'string') {
                    return new SafeString(ret);
                }
                return ret;
            };
        }

        function suppressValue(val, autoescape) {
            val = (val !== undefined && val !== null) ? val : "";
            if (autoescape && typeof val === "string") {
                val = lib.escape(val);
            }
            return val;
        }

        function memberLookup(obj, val) {
            obj = obj || {};
            if (typeof obj[val] === 'function') {
                return function () {
                    return obj[val].apply(obj, arguments);
                };
            }
            return obj[val];
        }

        function callWrap(obj, name, args) {
            if (!obj) {
                throw new Error('Unable to call `' + name + '`, which is undefined or falsey');
            }
            else if (typeof obj !== 'function') {
                throw new Error('Unable to call `' + name + '`, which is not a function');
            }
            return obj.apply(this, args);
        }

        function contextOrFrameLookup(context, frame, name) {
            var val = context.lookup(name);
            return(val !== undefined && val !== null) ? val : frame.lookup(name);
        }

        function handleError(error, lineno, colno) {
            if (error.lineno) {
                throw error;
            }
            else {
                throw new lib.TemplateError(error, lineno, colno);
            }
        }

        modules['runtime'] = {Frame: Frame, makeMacro: makeMacro, makeKeywordArgs: makeKeywordArgs, numArgs: numArgs, suppressValue: suppressValue, memberLookup: memberLookup, contextOrFrameLookup: contextOrFrameLookup, callWrap: callWrap, handleError: handleError, isArray: lib.isArray, SafeString: SafeString, copySafeness: copySafeness};
    })();
    (function () {
        var whitespaceChars = " \n\t\r";
        var delimChars = "()[]{}%*-+/#,:|.<>=!";
        var intChars = "0123456789";
        var BLOCK_START = "{%";
        var BLOCK_END = "%}";
        var VARIABLE_START = "{{";
        var VARIABLE_END = "}}";
        var COMMENT_START = "{#";
        var COMMENT_END = "#}";
        var TOKEN_STRING = "string";
        var TOKEN_WHITESPACE = "whitespace";
        var TOKEN_DATA = "data";
        var TOKEN_BLOCK_START = "block-start";
        var TOKEN_BLOCK_END = "block-end";
        var TOKEN_VARIABLE_START = "variable-start";
        var TOKEN_VARIABLE_END = "variable-end";
        var TOKEN_COMMENT = "comment";
        var TOKEN_LEFT_PAREN = "left-paren";
        var TOKEN_RIGHT_PAREN = "right-paren";
        var TOKEN_LEFT_BRACKET = "left-bracket";
        var TOKEN_RIGHT_BRACKET = "right-bracket";
        var TOKEN_LEFT_CURLY = "left-curly";
        var TOKEN_RIGHT_CURLY = "right-curly";
        var TOKEN_OPERATOR = "operator";
        var TOKEN_COMMA = "comma";
        var TOKEN_COLON = "colon";
        var TOKEN_PIPE = "pipe";
        var TOKEN_INT = "int";
        var TOKEN_FLOAT = "float";
        var TOKEN_BOOLEAN = "boolean";
        var TOKEN_SYMBOL = "symbol";
        var TOKEN_SPECIAL = "special";

        function token(type, value, lineno, colno) {
            return{type: type, value: value, lineno: lineno, colno: colno};
        }

        function Tokenizer(str) {
            this.str = str;
            this.index = 0;
            this.len = str.length;
            this.lineno = 0;
            this.colno = 0;
            this.in_code = false;
        }

        Tokenizer.prototype.nextToken = function () {
            var lineno = this.lineno;
            var colno = this.colno;
            if (this.in_code) {
                var cur = this.current();
                var tok;
                if (this.is_finished()) {
                    return null;
                }
                else if (cur == "\"" || cur == "'") {
                    return token(TOKEN_STRING, this.parseString(cur), lineno, colno);
                }
                else if ((tok = this._extract(whitespaceChars))) {
                    return token(TOKEN_WHITESPACE, tok, lineno, colno);
                }
                else if ((tok = this._extractString(BLOCK_END)) || (tok = this._extractString('-' + BLOCK_END))) {
                    this.in_code = false;
                    return token(TOKEN_BLOCK_END, tok, lineno, colno);
                }
                else if ((tok = this._extractString(VARIABLE_END))) {
                    this.in_code = false;
                    return token(TOKEN_VARIABLE_END, tok, lineno, colno);
                }
                else if (delimChars.indexOf(cur) != -1) {
                    this.forward();
                    var complexOps = ['==', '!=', '<=', '>=', '//', '**'];
                    var curComplex = cur + this.current();
                    var type;
                    if (complexOps.indexOf(curComplex) != -1) {
                        this.forward();
                        cur = curComplex;
                    }
                    switch (cur) {
                        case"(":
                            type = TOKEN_LEFT_PAREN;
                            break;
                        case")":
                            type = TOKEN_RIGHT_PAREN;
                            break;
                        case"[":
                            type = TOKEN_LEFT_BRACKET;
                            break;
                        case"]":
                            type = TOKEN_RIGHT_BRACKET;
                            break;
                        case"{":
                            type = TOKEN_LEFT_CURLY;
                            break;
                        case"}":
                            type = TOKEN_RIGHT_CURLY;
                            break;
                        case",":
                            type = TOKEN_COMMA;
                            break;
                        case":":
                            type = TOKEN_COLON;
                            break;
                        case"|":
                            type = TOKEN_PIPE;
                            break;
                        default:
                            type = TOKEN_OPERATOR;
                    }
                    return token(type, cur, lineno, colno);
                }
                else {
                    tok = this._extractUntil(whitespaceChars + delimChars);
                    if (tok.match(/^[-+]?[0-9]+$/)) {
                        if (this.current() == '.') {
                            this.forward();
                            var dec = this._extract(intChars);
                            return token(TOKEN_FLOAT, tok + '.' + dec, lineno, colno);
                        }
                        else {
                            return token(TOKEN_INT, tok, lineno, colno);
                        }
                    }
                    else if (tok.match(/^(true|false)$/)) {
                        return token(TOKEN_BOOLEAN, tok, lineno, colno);
                    }
                    else if (tok) {
                        return token(TOKEN_SYMBOL, tok, lineno, colno);
                    }
                    else {
                        throw new Error("Unexpected value while parsing: " + tok);
                    }
                }
            }
            else {
                var beginChars = (BLOCK_START[0] +
                    VARIABLE_START[0] +
                    COMMENT_START[0] +
                    COMMENT_END[0]);
                var tok;
                if (this.is_finished()) {
                    return null;
                }
                else if ((tok = this._extractString(BLOCK_START + '-')) || (tok = this._extractString(BLOCK_START))) {
                    this.in_code = true;
                    return token(TOKEN_BLOCK_START, tok, lineno, colno);
                }
                else if ((tok = this._extractString(VARIABLE_START))) {
                    this.in_code = true;
                    return token(TOKEN_VARIABLE_START, tok, lineno, colno);
                }
                else {
                    tok = '';
                    var data;
                    var in_comment = false;
                    if (this._matches(COMMENT_START)) {
                        in_comment = true;
                        tok = this._extractString(COMMENT_START);
                    }
                    while ((data = this._extractUntil(beginChars)) !== null) {
                        tok += data;
                        if ((this._matches(BLOCK_START) || this._matches(VARIABLE_START) || this._matches(COMMENT_START)) && !in_comment) {
                            break;
                        }
                        else if (this._matches(COMMENT_END)) {
                            if (!in_comment) {
                                throw new Error("unexpected end of comment");
                            }
                            tok += this._extractString(COMMENT_END);
                            break;
                        }
                        else {
                            tok += this.current();
                            this.forward();
                        }
                    }
                    if (data === null && in_comment) {
                        throw new Error("expected end of comment, got end of file");
                    }
                    return token(in_comment ? TOKEN_COMMENT : TOKEN_DATA, tok, lineno, colno);
                }
            }
            throw new Error("Could not parse text");
        };
        Tokenizer.prototype.parseString = function (delimiter) {
            this.forward();
            var lineno = this.lineno;
            var colno = this.colno;
            var str = "";
            while (this.current() != delimiter) {
                var cur = this.current();
                if (cur == "\\") {
                    this.forward();
                    switch (this.current()) {
                        case"n":
                            str += "\n";
                            break;
                        case"t":
                            str += "\t";
                            break;
                        case"r":
                            str += "\r";
                            break;
                        default:
                            str += this.current();
                    }
                    this.forward();
                }
                else {
                    str += cur;
                    this.forward();
                }
            }
            this.forward();
            return str;
        };
        Tokenizer.prototype._matches = function (str) {
            if (this.index + str.length > this.length) {
                return null;
            }
            var m = this.str.slice(this.index, this.index + str.length);
            return m == str;
        };
        Tokenizer.prototype._extractString = function (str) {
            if (this._matches(str)) {
                this.index += str.length;
                return str;
            }
            return null;
        };
        Tokenizer.prototype._extractUntil = function (charString) {
            return this._extractMatching(true, charString || "");
        };
        Tokenizer.prototype._extract = function (charString) {
            return this._extractMatching(false, charString);
        };
        Tokenizer.prototype._extractMatching = function (breakOnMatch, charString) {
            if (this.is_finished()) {
                return null;
            }
            var first = charString.indexOf(this.current());
            if ((breakOnMatch && first == -1) || (!breakOnMatch && first != -1)) {
                var t = this.current();
                this.forward();
                var idx = charString.indexOf(this.current());
                while (((breakOnMatch && idx == -1) || (!breakOnMatch && idx != -1)) && !this.is_finished()) {
                    t += this.current();
                    this.forward();
                    idx = charString.indexOf(this.current());
                }
                return t;
            }
            return"";
        };
        Tokenizer.prototype.is_finished = function () {
            return this.index >= this.len;
        };
        Tokenizer.prototype.forwardN = function (n) {
            for (var i = 0; i < n; i++) {
                this.forward();
            }
        };
        Tokenizer.prototype.forward = function () {
            this.index++;
            if (this.previous() == "\n") {
                this.lineno++;
                this.colno = 0;
            }
            else {
                this.colno++;
            }
        };
        Tokenizer.prototype.backN = function (n) {
            for (var i = 0; i < n; i++) {
                self.back();
            }
        };
        Tokenizer.prototype.back = function () {
            this.index--;
            if (this.current() == "\n") {
                this.lineno--;
                var idx = this.src.lastIndexOf("\n", this.index - 1);
                if (idx == -1) {
                    this.colno = this.index;
                }
                else {
                    this.colno = this.index - idx;
                }
            }
            else {
                this.colno--;
            }
        };
        Tokenizer.prototype.current = function () {
            if (!this.is_finished()) {
                return this.str[this.index];
            }
            return"";
        };
        Tokenizer.prototype.previous = function () {
            return this.str[this.index - 1];
        };
        modules['lexer'] = {lex: function (src) {
            return new Tokenizer(src);
        }, setTags: function (tags) {
            BLOCK_START = tags.blockStart || BLOCK_START;
            BLOCK_END = tags.blockEnd || BLOCK_END;
            VARIABLE_START = tags.variableStart || VARIABLE_START;
            VARIABLE_END = tags.variableEnd || VARIABLE_END;
            COMMENT_START = tags.commentStart || COMMENT_START;
            COMMENT_END = tags.commentEnd || COMMENT_END;
        }, TOKEN_STRING: TOKEN_STRING, TOKEN_WHITESPACE: TOKEN_WHITESPACE, TOKEN_DATA: TOKEN_DATA, TOKEN_BLOCK_START: TOKEN_BLOCK_START, TOKEN_BLOCK_END: TOKEN_BLOCK_END, TOKEN_VARIABLE_START: TOKEN_VARIABLE_START, TOKEN_VARIABLE_END: TOKEN_VARIABLE_END, TOKEN_COMMENT: TOKEN_COMMENT, TOKEN_LEFT_PAREN: TOKEN_LEFT_PAREN, TOKEN_RIGHT_PAREN: TOKEN_RIGHT_PAREN, TOKEN_LEFT_BRACKET: TOKEN_LEFT_BRACKET, TOKEN_RIGHT_BRACKET: TOKEN_RIGHT_BRACKET, TOKEN_LEFT_CURLY: TOKEN_LEFT_CURLY, TOKEN_RIGHT_CURLY: TOKEN_RIGHT_CURLY, TOKEN_OPERATOR: TOKEN_OPERATOR, TOKEN_COMMA: TOKEN_COMMA, TOKEN_COLON: TOKEN_COLON, TOKEN_PIPE: TOKEN_PIPE, TOKEN_INT: TOKEN_INT, TOKEN_FLOAT: TOKEN_FLOAT, TOKEN_BOOLEAN: TOKEN_BOOLEAN, TOKEN_SYMBOL: TOKEN_SYMBOL, TOKEN_SPECIAL: TOKEN_SPECIAL};
    })();
    (function () {
        var lexer = modules["lexer"];
        var nodes = modules["nodes"];
        var Object = modules["object"];
        var lib = modules["lib"];
        var Parser = Object.extend({init: function (tokens) {
            this.tokens = tokens;
            this.peeked = null;
            this.breakOnBlocks = null;
            this.dropLeadingWhitespace = false;
            this.extensions = [];
        }, nextToken: function (withWhitespace) {
            var tok;
            if (this.peeked) {
                if (!withWhitespace && this.peeked.type == lexer.TOKEN_WHITESPACE) {
                    this.peeked = null;
                }
                else {
                    tok = this.peeked;
                    this.peeked = null;
                    return tok;
                }
            }
            tok = this.tokens.nextToken();
            if (!withWhitespace) {
                while (tok && tok.type == lexer.TOKEN_WHITESPACE) {
                    tok = this.tokens.nextToken();
                }
            }
            return tok;
        }, peekToken: function () {
            this.peeked = this.peeked || this.nextToken();
            return this.peeked;
        }, pushToken: function (tok) {
            if (this.peeked) {
                throw new Error("pushToken: can only push one token on between reads");
            }
            this.peeked = tok;
        }, fail: function (msg, lineno, colno) {
            if ((lineno === undefined || colno === undefined) && this.peekToken()) {
                var tok = this.peekToken();
                lineno = tok.lineno;
                colno = tok.colno;
            }
            if (lineno !== undefined)lineno += 1;
            if (colno !== undefined)colno += 1;
            throw new lib.TemplateError(msg, lineno, colno);
        }, skip: function (type) {
            var tok = this.nextToken();
            if (!tok || tok.type != type) {
                this.pushToken(tok);
                return false;
            }
            return true;
        }, expect: function (type) {
            var tok = this.nextToken();
            if (!tok.type == type) {
                this.fail('expected ' + type + ', got ' + tok.type, tok.lineno, tok.colno);
            }
            return tok;
        }, skipValue: function (type, val) {
            var tok = this.nextToken();
            if (!tok || tok.type != type || tok.value != val) {
                this.pushToken(tok);
                return false;
            }
            return true;
        }, skipWhitespace: function () {
            return this.skip(lexer.TOKEN_WHITESPACE);
        }, skipSymbol: function (val) {
            return this.skipValue(lexer.TOKEN_SYMBOL, val);
        }, advanceAfterBlockEnd: function (name) {
            if (!name) {
                var tok = this.peekToken();
                if (!tok) {
                    this.fail('unexpected end of file');
                }
                if (tok.type != lexer.TOKEN_SYMBOL) {
                    this.fail("advanceAfterBlockEnd: expected symbol token or " + "explicit name to be passed");
                }
                name = this.nextToken().value;
            }
            var tok = this.nextToken();
            if (tok.type == lexer.TOKEN_BLOCK_END) {
                if (tok.value.charAt(0) === '-') {
                    this.dropLeadingWhitespace = true;
                }
            }
            else {
                this.fail("expected block end in " + name + " statement");
            }
        }, advanceAfterVariableEnd: function () {
            if (!this.skip(lexer.TOKEN_VARIABLE_END)) {
                this.fail("expected variable end");
            }
        }, parseFor: function () {
            var forTok = this.peekToken();
            if (!this.skipSymbol('for')) {
                this.fail("parseFor: expected for", forTok.lineno, forTok.colno);
            }
            var node = new nodes.For(forTok.lineno, forTok.colno);
            node.name = this.parsePrimary();
            if (!(node.name instanceof nodes.Symbol)) {
                this.fail('parseFor: variable name expected for loop');
            }
            var type = this.peekToken().type;
            if (type == lexer.TOKEN_COMMA) {
                var key = node.name;
                node.name = new nodes.Array(key.lineno, key.colno);
                node.name.addChild(key);
                while (this.skip(lexer.TOKEN_COMMA)) {
                    var prim = this.parsePrimary();
                    node.name.addChild(prim);
                }
            }
            if (!this.skipSymbol('in')) {
                this.fail('parseFor: expected "in" keyword for loop', forTok.lineno, forTok.colno);
            }
            node.arr = this.parseExpression();
            this.advanceAfterBlockEnd(forTok.value);
            node.body = this.parseUntilBlocks('endfor');
            this.advanceAfterBlockEnd();
            return node;
        }, parseMacro: function () {
            var macroTok = this.peekToken();
            if (!this.skipSymbol('macro')) {
                this.fail("expected macro");
            }
            var name = this.parsePrimary(true);
            var args = this.parseSignature();
            var node = new nodes.Macro(macroTok.lineno, macroTok.colno, name, args);
            this.advanceAfterBlockEnd(macroTok.value);
            node.body = this.parseUntilBlocks('endmacro');
            this.advanceAfterBlockEnd();
            return node;
        }, parseImport: function () {
            var importTok = this.peekToken();
            if (!this.skipSymbol('import')) {
                this.fail("parseImport: expected import", importTok.lineno, importTok.colno);
            }
            var template = this.parsePrimary();
            if (!this.skipSymbol('as')) {
                this.fail('parseImport: expected "as" keyword', importTok.lineno, importTok.colno);
            }
            var target = this.parsePrimary();
            var node = new nodes.Import(importTok.lineno, importTok.colno, template, target);
            this.advanceAfterBlockEnd(importTok.value);
            return node;
        }, parseFrom: function () {
            var fromTok = this.peekToken();
            if (!this.skipSymbol('from')) {
                this.fail("parseFrom: expected from");
            }
            var template = this.parsePrimary();
            var node = new nodes.FromImport(fromTok.lineno, fromTok.colno, template, new nodes.NodeList());
            if (!this.skipSymbol('import')) {
                this.fail("parseFrom: expected import", fromTok.lineno, fromTok.colno);
            }
            var names = node.names;
            while (1) {
                var nextTok = this.peekToken();
                if (nextTok.type == lexer.TOKEN_BLOCK_END) {
                    if (!names.children.length) {
                        this.fail('parseFrom: Expected at least one import name', fromTok.lineno, fromTok.colno);
                    }
                    if (nextTok.value.charAt(0) == '-') {
                        this.dropLeadingWhitespace = true;
                    }
                    this.nextToken();
                    break;
                }
                if (names.children.length > 0 && !this.skip(lexer.TOKEN_COMMA)) {
                    this.fail('parseFrom: expected comma', fromTok.lineno, fromTok.colno);
                }
                var name = this.parsePrimary();
                if (name.value.charAt(0) == '_') {
                    this.fail('parseFrom: names starting with an underscore ' + 'cannot be imported', name.lineno, name.colno);
                }
                if (this.skipSymbol('as')) {
                    var alias = this.parsePrimary();
                    names.addChild(new nodes.Pair(name.lineno, name.colno, name, alias));
                }
                else {
                    names.addChild(name);
                }
            }
            return node;
        }, parseBlock: function () {
            var tag = this.peekToken();
            if (!this.skipSymbol('block')) {
                this.fail('parseBlock: expected block', tag.lineno, tag.colno);
            }
            var node = new nodes.Block(tag.lineno, tag.colno);
            node.name = this.parsePrimary();
            if (!(node.name instanceof nodes.Symbol)) {
                this.fail('parseBlock: variable name expected', tag.lineno, tag.colno);
            }
            this.advanceAfterBlockEnd(tag.value);
            node.body = this.parseUntilBlocks('endblock');
            if (!this.peekToken()) {
                this.fail('parseBlock: expected endblock, got end of file');
            }
            this.advanceAfterBlockEnd();
            return node;
        }, parseTemplateRef: function (tagName, nodeType) {
            var tag = this.peekToken();
            if (!this.skipSymbol(tagName)) {
                this.fail('parseTemplateRef: expected ' + tagName);
            }
            var node = new nodeType(tag.lineno, tag.colno);
            node.template = this.parsePrimary();
            this.advanceAfterBlockEnd(tag.value);
            return node;
        }, parseExtends: function () {
            return this.parseTemplateRef('extends', nodes.Extends);
        }, parseInclude: function () {
            return this.parseTemplateRef('include', nodes.Include);
        }, parseIf: function () {
            var tag = this.peekToken();
            if (!this.skipSymbol('if') && !this.skipSymbol('elif')) {
                this.fail("parseIf: expected if or elif", tag.lineno, tag.colno);
            }
            var node = new nodes.If(tag.lineno, tag.colno);
            node.cond = this.parseExpression();
            this.advanceAfterBlockEnd(tag.value);
            node.body = this.parseUntilBlocks('elif', 'else', 'endif');
            var tok = this.peekToken();
            switch (tok && tok.value) {
                case"elif":
                    node.else_ = this.parseIf();
                    break;
                case"else":
                    this.advanceAfterBlockEnd();
                    node.else_ = this.parseUntilBlocks("endif");
                    this.advanceAfterBlockEnd();
                    break;
                case"endif":
                    node.else_ = null;
                    this.advanceAfterBlockEnd();
                    break;
                default:
                    this.fail('parseIf: expected endif, else, or endif, ' + 'got end of file');
            }
            return node;
        }, parseSet: function () {
            var tag = this.peekToken();
            if (!this.skipSymbol('set')) {
                this.fail('parseSet: expected set', tag.lineno, tag.colno);
            }
            var node = new nodes.Set(tag.lineno, tag.colno, []);
            var target;
            while ((target = this.parsePrimary())) {
                node.targets.push(target);
                if (!this.skip(lexer.TOKEN_COMMA)) {
                    break;
                }
            }
            if (!this.skipValue(lexer.TOKEN_OPERATOR, '=')) {
                this.fail('parseSet: expected = in set tag', tag.lineno, tag.colno);
            }
            node.value = this.parseExpression();
            this.advanceAfterBlockEnd(tag.value);
            return node;
        }, parseStatement: function () {
            var tok = this.peekToken();
            var node;
            if (tok.type != lexer.TOKEN_SYMBOL) {
                this.fail('tag name expected', tok.lineno, tok.colno);
            }
            if (this.breakOnBlocks && this.breakOnBlocks.indexOf(tok.value) != -1) {
                return null;
            }
            switch (tok.value) {
                case'raw':
                    return this.parseRaw();
                case'if':
                    return this.parseIf();
                case'for':
                    return this.parseFor();
                case'block':
                    return this.parseBlock();
                case'extends':
                    return this.parseExtends();
                case'include':
                    return this.parseInclude();
                case'set':
                    return this.parseSet();
                case'macro':
                    return this.parseMacro();
                case'import':
                    return this.parseImport();
                case'from':
                    return this.parseFrom();
                default:
                    if (this.extensions.length) {
                        for (var i = 0; i < this.extensions.length; i++) {
                            var ext = this.extensions[i];
                            if ((ext.tags || []).indexOf(tok.value) > -1) {
                                return ext.parse(this, nodes, lexer);
                            }
                        }
                    }
                    this.fail('unknown block tag: ' + tok.value, tok.lineno, tok.colno);
            }
            return node;
        }, parseRaw: function () {
            this.advanceAfterBlockEnd();
            var str = '';
            var begun = this.peekToken();
            while (1) {
                var tok = this.nextToken(true);
                if (!tok) {
                    this.fail("expected endraw, got end of file");
                }
                if (tok.type == lexer.TOKEN_BLOCK_START) {
                    var ws = null;
                    var name = this.nextToken(true);
                    if (name.type == lexer.TOKEN_WHITESPACE) {
                        ws = name;
                        name = this.nextToken();
                    }
                    if (name.type == lexer.TOKEN_SYMBOL && name.value == 'endraw') {
                        this.advanceAfterBlockEnd(name.value);
                        break;
                    }
                    else {
                        str += tok.value;
                        if (ws) {
                            str += ws.value;
                        }
                        str += name.value;
                    }
                }
                else {
                    str += tok.value;
                }
            }
            var output = new nodes.Output(begun.lineno, begun.colno, [new nodes.TemplateData(begun.lineno, begun.colno, str)]);
            return output;
        }, parsePostfix: function (node) {
            var tok = this.peekToken();
            while (tok) {
                if (tok.type == lexer.TOKEN_LEFT_PAREN) {
                    node = new nodes.FunCall(tok.lineno, tok.colno, node, this.parseSignature());
                }
                else if (tok.type == lexer.TOKEN_LEFT_BRACKET) {
                    var lookup = this.parseAggregate();
                    if (lookup.children.length > 1) {
                        this.fail('invalid index');
                    }
                    node = new nodes.LookupVal(tok.lineno, tok.colno, node, lookup.children[0]);
                }
                else if (tok.type == lexer.TOKEN_OPERATOR && tok.value == '.') {
                    this.nextToken();
                    var val = this.nextToken();
                    if (val.type != lexer.TOKEN_SYMBOL) {
                        this.fail('expected name as lookup value, got ' + val.value, val.lineno, val.colno);
                    }
                    var lookup = new nodes.Literal(val.lineno, val.colno, val.value);
                    node = new nodes.LookupVal(tok.lineno, tok.colno, node, lookup);
                }
                else {
                    break;
                }
                tok = this.peekToken();
            }
            return node;
        }, parseExpression: function () {
            var node = this.parseInlineIf();
            return node;
        }, parseInlineIf: function () {
            var node = this.parseOr();
            if (this.skipSymbol('if')) {
                var cond_node = this.parseOr();
                var body_node = node;
                node = new nodes.InlineIf(node.lineno, node.colno);
                node.body = body_node;
                node.cond = cond_node;
                if (this.skipSymbol('else')) {
                    node.else_ = this.parseOr();
                } else {
                    node.else_ = null;
                }
            }
            return node;
        }, parseOr: function () {
            var node = this.parseAnd();
            while (this.skipSymbol('or')) {
                var node2 = this.parseAnd();
                node = new nodes.Or(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseAnd: function () {
            var node = this.parseNot();
            while (this.skipSymbol('and')) {
                var node2 = this.parseNot();
                node = new nodes.And(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseNot: function () {
            var tok = this.peekToken();
            if (this.skipSymbol('not')) {
                return new nodes.Not(tok.lineno, tok.colno, this.parseNot());
            }
            return this.parseCompare();
        }, parseCompare: function () {
            var compareOps = ['==', '!=', '<', '>', '<=', '>='];
            var expr = this.parseAdd();
            var ops = [];
            while (1) {
                var tok = this.nextToken();
                if (!tok) {
                    break;
                }
                else if (compareOps.indexOf(tok.value) != -1) {
                    ops.push(new nodes.CompareOperand(tok.lineno, tok.colno, this.parseAdd(), tok.value));
                }
                else if (tok.type == lexer.TOKEN_SYMBOL && tok.value == 'in') {
                    ops.push(new nodes.CompareOperand(tok.lineno, tok.colno, this.parseAdd(), 'in'));
                }
                else if (tok.type == lexer.TOKEN_SYMBOL && tok.value == 'not' && this.skipSymbol('in')) {
                    ops.push(new nodes.CompareOperand(tok.lineno, tok.colno, this.parseAdd(), 'notin'));
                }
                else {
                    this.pushToken(tok);
                    break;
                }
            }
            if (ops.length) {
                return new nodes.Compare(ops[0].lineno, ops[0].colno, expr, ops);
            }
            else {
                return expr;
            }
        }, parseAdd: function () {
            var node = this.parseSub();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '+')) {
                var node2 = this.parseSub();
                node = new nodes.Add(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseSub: function () {
            var node = this.parseMul();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '-')) {
                var node2 = this.parseMul();
                node = new nodes.Sub(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseMul: function () {
            var node = this.parseDiv();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '*')) {
                var node2 = this.parseDiv();
                node = new nodes.Mul(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseDiv: function () {
            var node = this.parseFloorDiv();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '/')) {
                var node2 = this.parseFloorDiv();
                node = new nodes.Div(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseFloorDiv: function () {
            var node = this.parseMod();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '//')) {
                var node2 = this.parseMod();
                node = new nodes.FloorDiv(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseMod: function () {
            var node = this.parsePow();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '%')) {
                var node2 = this.parsePow();
                node = new nodes.Mod(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parsePow: function () {
            var node = this.parseUnary();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '**')) {
                var node2 = this.parseUnary();
                node = new nodes.Pow(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseUnary: function (noFilters) {
            var tok = this.peekToken();
            var node;
            if (this.skipValue(lexer.TOKEN_OPERATOR, '-')) {
                node = new nodes.Neg(tok.lineno, tok.colno, this.parseUnary(true));
            }
            else if (this.skipValue(lexer.TOKEN_OPERATOR, '+')) {
                node = new nodes.Pos(tok.lineno, tok.colno, this.parseUnary(true));
            }
            else {
                node = this.parsePrimary();
            }
            if (!noFilters) {
                node = this.parseFilter(node);
            }
            return node;
        }, parsePrimary: function (noPostfix) {
            var tok = this.nextToken();
            var val = null;
            var node = null;
            if (!tok) {
                this.fail('expected expression, got end of file');
            }
            else if (tok.type == lexer.TOKEN_STRING) {
                val = tok.value;
            }
            else if (tok.type == lexer.TOKEN_INT) {
                val = parseInt(tok.value, 10);
            }
            else if (tok.type == lexer.TOKEN_FLOAT) {
                val = parseFloat(tok.value);
            }
            else if (tok.type == lexer.TOKEN_BOOLEAN) {
                if (tok.value == "true") {
                    val = true;
                }
                else if (tok.value == "false") {
                    val = false;
                }
                else {
                    this.fail("invalid boolean: " + tok.val, tok.lineno, tok.colno);
                }
            }
            if (val !== null) {
                node = new nodes.Literal(tok.lineno, tok.colno, val);
            }
            else if (tok.type == lexer.TOKEN_SYMBOL) {
                node = new nodes.Symbol(tok.lineno, tok.colno, tok.value);
                if (!noPostfix) {
                    node = this.parsePostfix(node);
                }
            }
            else {
                this.pushToken(tok);
                node = this.parseAggregate();
            }
            if (node) {
                return node;
            }
            else {
                this.fail('unexpected token: ' + tok.value, tok.lineno, tok.colno);
            }
        }, parseFilter: function (node) {
            while (this.skip(lexer.TOKEN_PIPE)) {
                var tok = this.expect(lexer.TOKEN_SYMBOL);
                var name = tok.value;
                while (this.skipValue(lexer.TOKEN_OPERATOR, '.')) {
                    name += '.' + this.expect(lexer.TOKEN_SYMBOL).value;
                }
                node = new nodes.Filter(tok.lineno, tok.colno, new nodes.Symbol(tok.lineno, tok.colno, name), new nodes.NodeList(tok.lineno, tok.colno, [node]));
                if (this.peekToken().type == lexer.TOKEN_LEFT_PAREN) {
                    var call = this.parsePostfix(node);
                    node.args.children = node.args.children.concat(call.args.children);
                }
            }
            return node;
        }, parseAggregate: function () {
            var tok = this.nextToken();
            var node;
            switch (tok.type) {
                case lexer.TOKEN_LEFT_PAREN:
                    node = new nodes.Group(tok.lineno, tok.colno);
                    break;
                case lexer.TOKEN_LEFT_BRACKET:
                    node = new nodes.Array(tok.lineno, tok.colno);
                    break;
                case lexer.TOKEN_LEFT_CURLY:
                    node = new nodes.Dict(tok.lineno, tok.colno);
                    break;
                default:
                    return null;
            }
            while (1) {
                var type = this.peekToken().type;
                if (type == lexer.TOKEN_RIGHT_PAREN || type == lexer.TOKEN_RIGHT_BRACKET || type == lexer.TOKEN_RIGHT_CURLY) {
                    this.nextToken();
                    break;
                }
                if (node.children.length > 0) {
                    if (!this.skip(lexer.TOKEN_COMMA)) {
                        this.fail("parseAggregate: expected comma after expression", tok.lineno, tok.colno);
                    }
                }
                if (node instanceof nodes.Dict) {
                    var key = this.parsePrimary();
                    if (!this.skip(lexer.TOKEN_COLON)) {
                        this.fail("parseAggregate: expected colon after dict key", tok.lineno, tok.colno);
                    }
                    var value = this.parseExpression();
                    node.addChild(new nodes.Pair(key.lineno, key.colno, key, value));
                }
                else {
                    var expr = this.parseExpression();
                    node.addChild(expr);
                }
            }
            return node;
        }, parseSignature: function (tolerant, noParens) {
            var tok = this.peekToken();
            if (!noParens && tok.type != lexer.TOKEN_LEFT_PAREN) {
                if (tolerant) {
                    return null;
                }
                else {
                    this.fail('expected arguments', tok.lineno, tok.colno);
                }
            }
            if (tok.type == lexer.TOKEN_LEFT_PAREN) {
                tok = this.nextToken();
            }
            var args = new nodes.NodeList(tok.lineno, tok.colno);
            var kwargs = new nodes.KeywordArgs(tok.lineno, tok.colno);
            var kwnames = [];
            var checkComma = false;
            while (1) {
                tok = this.peekToken();
                if (!noParens && tok.type == lexer.TOKEN_RIGHT_PAREN) {
                    this.nextToken();
                    break;
                }
                else if (noParens && tok.type == lexer.TOKEN_BLOCK_END) {
                    break;
                }
                if (checkComma && !this.skip(lexer.TOKEN_COMMA)) {
                    this.fail("parseSignature: expected comma after expression", tok.lineno, tok.colno);
                }
                else {
                    var arg = this.parsePrimary();
                    if (this.skipValue(lexer.TOKEN_OPERATOR, '=')) {
                        kwargs.addChild(new nodes.Pair(arg.lineno, arg.colno, arg, this.parseExpression()));
                    }
                    else {
                        args.addChild(arg);
                    }
                }
                checkComma = true;
            }
            if (kwargs.children.length) {
                args.addChild(kwargs);
            }
            return args;
        }, parseUntilBlocks: function () {
            var prev = this.breakOnBlocks;
            this.breakOnBlocks = lib.toArray(arguments);
            var ret = this.parse();
            this.breakOnBlocks = prev;
            return ret;
        }, parseNodes: function () {
            var tok;
            var buf = [];
            while ((tok = this.nextToken())) {
                if (tok.type == lexer.TOKEN_DATA) {
                    var data = tok.value;
                    var nextToken = this.peekToken();
                    var nextVal = nextToken && nextToken.value;
                    if (this.dropLeadingWhitespace) {
                        data = data.replace(/^\s*/, '');
                        this.dropLeadingWhitespace = false;
                    }
                    if (nextToken && nextToken.type == lexer.TOKEN_BLOCK_START && nextVal.charAt(nextVal.length - 1) == '-') {
                        data = data.replace(/\s*$/, '');
                    }
                    buf.push(new nodes.Output(tok.lineno, tok.colno, [new nodes.TemplateData(tok.lineno, tok.colno, data)]));
                }
                else if (tok.type == lexer.TOKEN_BLOCK_START) {
                    var n = this.parseStatement();
                    if (!n) {
                        break;
                    }
                    buf.push(n);
                }
                else if (tok.type == lexer.TOKEN_VARIABLE_START) {
                    var e = this.parseExpression();
                    this.advanceAfterVariableEnd();
                    buf.push(new nodes.Output(tok.lineno, tok.colno, [e]));
                }
                else if (tok.type != lexer.TOKEN_COMMENT) {
                    this.fail("Unexpected token at top-level: " +
                        tok.type, tok.lineno, tok.colno);
                }
            }
            return buf;
        }, parse: function () {
            return new nodes.NodeList(0, 0, this.parseNodes());
        }, parseAsRoot: function () {
            return new nodes.Root(0, 0, this.parseNodes());
        }});
        modules['parser'] = {parse: function (src, extensions) {
            var p = new Parser(lexer.lex(src));
            if (extensions !== undefined) {
                p.extensions = extensions;
            }
            return p.parseAsRoot();
        }};
    })();
    (function () {
        var lib = modules["lib"];
        var parser = modules["parser"];
        var nodes = modules["nodes"];
        var Object = modules["object"];
        var Frame = modules["runtime"].Frame;
        var compareOps = {'==': '==', '!=': '!=', '<': '<', '>': '>', '<=': '<=', '>=': '>='};

        function binOpEmitter(str) {
            return function (node, frame) {
                this.compile(node.left, frame);
                this.emit(str);
                this.compile(node.right, frame);
            };
        }

        function quotedArray(arr) {
            return'[' +
                lib.map(arr, function (x) {
                    return'"' + x + '"';
                }) + ']';
        }

        var Compiler = Object.extend({init: function (extensions) {
            this.codebuf = [];
            this.lastId = 0;
            this.buffer = null;
            this.bufferStack = [];
            this.isChild = false;
            this.extensions = extensions || [];
        }, fail: function (msg, lineno, colno) {
            if (lineno !== undefined)lineno += 1;
            if (colno !== undefined)colno += 1;
            throw new lib.TemplateError(msg, lineno, colno);
        }, pushBufferId: function (id) {
            this.bufferStack.push(this.buffer);
            this.buffer = id;
            this.emit('var ' + this.buffer + ' = "";');
        }, popBufferId: function () {
            this.buffer = this.bufferStack.pop();
        }, emit: function (code) {
            this.codebuf.push(code);
        }, emitLine: function (code) {
            this.emit(code + "\n");
        }, emitLines: function () {
            lib.each(lib.toArray(arguments), function (line) {
                this.emitLine(line);
            }, this);
        }, emitFuncBegin: function (name) {
            this.buffer = 'output';
            this.emitLine('function ' + name + '(env, context, frame, runtime) {');
            this.emitLine('var lineno = null;');
            this.emitLine('var colno = null;');
            this.emitLine('var ' + this.buffer + ' = "";');
            this.emitLine('try {');
        }, emitFuncEnd: function (noReturn) {
            if (!noReturn) {
                this.emitLine('return ' + this.buffer + ';');
            }
            this.emitLine('} catch (e) {');
            this.emitLine('  runtime.handleError(e, lineno, colno);');
            this.emitLine('}');
            this.emitLine('}');
            this.buffer = null;
        }, tmpid: function () {
            this.lastId++;
            return't_' + this.lastId;
        }, _bufferAppend: function (func) {
            this.emit(this.buffer + ' += runtime.suppressValue(');
            func.call(this);
            this.emit(', env.autoesc);\n');
        }, _compileChildren: function (node, frame) {
            var children = node.children;
            for (var i = 0, l = children.length; i < l; i++) {
                this.compile(children[i], frame);
            }
        }, _compileAggregate: function (node, frame, startChar, endChar) {
            this.emit(startChar);
            for (var i = 0; i < node.children.length; i++) {
                if (i > 0) {
                    this.emit(',');
                }
                this.compile(node.children[i], frame);
            }
            this.emit(endChar);
        }, _compileExpression: function (node, frame) {
            this.assertType(node, nodes.Literal, nodes.Symbol, nodes.Group, nodes.Array, nodes.Dict, nodes.FunCall, nodes.Filter, nodes.LookupVal, nodes.Compare, nodes.InlineIf, nodes.And, nodes.Or, nodes.Not, nodes.Add, nodes.Sub, nodes.Mul, nodes.Div, nodes.FloorDiv, nodes.Mod, nodes.Pow, nodes.Neg, nodes.Pos, nodes.Compare);
            this.compile(node, frame);
        }, assertType: function (node) {
            var types = lib.toArray(arguments).slice(1);
            var success = false;
            for (var i = 0; i < types.length; i++) {
                if (node instanceof types[i]) {
                    success = true;
                }
            }
            if (!success) {
                this.fail("assertType: invalid type: " + node.typename, node.lineno, node.colno);
            }
        }, compileCallExtension: function (node, frame) {
            var name = node.extName;
            var args = node.args;
            var contentArgs = node.contentArgs;
            var transformedArgs = [];
            this.emit(this.buffer + ' += runtime.suppressValue(');
            this.emit('env.getExtension("' + node.extName + '")["' + node.prop + '"](');
            this.emit('context');
            if (args || contentArgs) {
                this.emit(',');
            }
            if (args) {
                if (!(args instanceof nodes.NodeList)) {
                    this.fail('compileCallExtension: arguments must be a NodeList, ' + 'use `parser.parseSignature`');
                }
                lib.each(args.children, function (arg, i) {
                    this._compileExpression(arg, frame);
                    if (i != args.children.length || contentArgs) {
                        this.emit(',');
                    }
                }, this);
            }
            if (contentArgs) {
                lib.each(contentArgs, function (arg, i) {
                    if (i > 0) {
                        this.emit(',');
                    }
                    if (arg) {
                        var id = this.tmpid();
                        this.emit('function() {');
                        this.pushBufferId(id);
                        this.compile(arg, frame);
                        this.popBufferId();
                        this.emitLine('return ' + id + ';\n' + '}');
                    }
                    else {
                        this.emit('null');
                    }
                }, this);
            }
            this.emit(')');
            this.emit(', env.autoesc);\n');
        }, compileNodeList: function (node, frame) {
            this._compileChildren(node, frame);
        }, compileLiteral: function (node, frame) {
            if (typeof node.value == "string") {
                var val = node.value.replace(/\\/g, '\\\\');
                val = val.replace(/"/g, '\\"');
                val = val.replace(/\n/g, "\\n");
                val = val.replace(/\r/g, "\\r");
                val = val.replace(/\t/g, "\\t");
                this.emit('"' + val + '"');
            }
            else {
                this.emit(node.value.toString());
            }
        }, compileSymbol: function (node, frame) {
            var name = node.value;
            var v;
            if ((v = frame.lookup(name))) {
                this.emit(v);
            }
            else {
                this.emit('runtime.contextOrFrameLookup(' + 'context, frame, "' + name + '")');
            }
        }, compileGroup: function (node, frame) {
            this._compileAggregate(node, frame, '(', ')');
        }, compileArray: function (node, frame) {
            this._compileAggregate(node, frame, '[', ']');
        }, compileDict: function (node, frame) {
            this._compileAggregate(node, frame, '{', '}');
        }, compilePair: function (node, frame) {
            var key = node.key;
            var val = node.value;
            if (key instanceof nodes.Symbol) {
                key = new nodes.Literal(key.lineno, key.colno, key.value);
            }
            else if (!(key instanceof nodes.Literal && typeof key.value == "string")) {
                this.fail("compilePair: Dict keys must be strings or names", key.lineno, key.colno);
            }
            this.compile(key, frame);
            this.emit(': ');
            this._compileExpression(val, frame);
        }, compileInlineIf: function (node, frame) {
            this.emit('(');
            this.compile(node.cond, frame);
            this.emit('?');
            this.compile(node.body, frame);
            this.emit(':');
            if (node.else_ !== null)
                this.compile(node.else_, frame); else
                this.emit('""');
            this.emit(')');
        }, compileOr: binOpEmitter(' || '), compileAnd: binOpEmitter(' && '), compileAdd: binOpEmitter(' + '), compileSub: binOpEmitter(' - '), compileMul: binOpEmitter(' * '), compileDiv: binOpEmitter(' / '), compileMod: binOpEmitter(' % '), compileNot: function (node, frame) {
            this.emit('!');
            this.compile(node.target, frame);
        }, compileFloorDiv: function (node, frame) {
            this.emit('Math.floor(');
            this.compile(node.left, frame);
            this.emit(' / ');
            this.compile(node.right, frame);
            this.emit(')');
        }, compilePow: function (node, frame) {
            this.emit('Math.pow(');
            this.compile(node.left, frame);
            this.emit(', ');
            this.compile(node.right, frame);
            this.emit(')');
        }, compileNeg: function (node, frame) {
            this.emit('-');
            this.compile(node.target, frame);
        }, compilePos: function (node, frame) {
            this.emit('+');
            this.compile(node.target, frame);
        }, compileCompare: function (node, frame) {
            this.compile(node.expr, frame);
            for (var i = 0; i < node.ops.length; i++) {
                var n = node.ops[i];
                this.emit(' ' + compareOps[n.type] + ' ');
                this.compile(n.expr, frame);
            }
        }, compileLookupVal: function (node, frame) {
            this.emit('runtime.memberLookup((');
            this._compileExpression(node.target, frame);
            this.emit('),');
            this._compileExpression(node.val, frame);
            this.emit(', env.autoesc)');
        }, _getNodeName: function (node) {
            switch (node.typename) {
                case'Symbol':
                    return node.value;
                case'FunCall':
                    return'the return value of (' + this._getNodeName(node.name) + ')';
                case'LookupVal':
                    return this._getNodeName(node.target) + '["' +
                        this._getNodeName(node.val) + '"]';
                case'Literal':
                    return node.value.toString().substr(0, 10);
                default:
                    return'--expression--';
            }
        }, compileFunCall: function (node, frame) {
            this.emit('(lineno = ' + node.lineno + ', colno = ' + node.colno + ', ');
            this.emit('runtime.callWrap(');
            this._compileExpression(node.name, frame);
            this.emit(', "' + this._getNodeName(node.name).replace(/"/g, '\\"') + '", ');
            this._compileAggregate(node.args, frame, '[', '])');
            this.emit(')');
        }, compileFilter: function (node, frame) {
            var name = node.name;
            this.assertType(name, nodes.Symbol);
            this.emit('env.getFilter("' + name.value + '")');
            this._compileAggregate(node.args, frame, '(', ')');
        }, compileKeywordArgs: function (node, frame) {
            var names = [];
            lib.each(node.children, function (pair) {
                names.push(pair.key.value);
            });
            this.emit('runtime.makeKeywordArgs(');
            this.compileDict(node, frame);
            this.emit(')');
        }, compileSet: function (node, frame) {
            var ids = [];
            lib.each(node.targets, function (target) {
                var name = target.value;
                var id = frame.get(name);
                if (id === null) {
                    id = this.tmpid();
                    frame.set(name, id);
                    this.emitLine('var ' + id + ';');
                }
                ids.push(id);
            }, this);
            this.emit(ids.join(' = ') + ' = ');
            this._compileExpression(node.value, frame);
            this.emitLine(';');
            lib.each(node.targets, function (target, i) {
                var id = ids[i];
                var name = target.value;
                this.emitLine('frame.set("' + name + '", ' + id + ');');
                this.emitLine('if(!frame.parent) {');
                this.emitLine('context.setVariable("' + name + '", ' + id + ');');
                if (name.charAt(0) != '_') {
                    this.emitLine('context.addExport("' + name + '");');
                }
                this.emitLine('}');
            }, this);
        }, compileIf: function (node, frame) {
            this.emit('if(');
            this._compileExpression(node.cond, frame);
            this.emitLine(') {');
            this.compile(node.body, frame);
            if (node.else_) {
                this.emitLine('}\nelse {');
                this.compile(node.else_, frame);
            }
            this.emitLine('}');
        }, compileFor: function (node, frame) {
            var i = this.tmpid();
            var arr = this.tmpid();
            frame = frame.push();
            this.emitLine('frame = frame.push();');
            this.emit('var ' + arr + ' = ');
            this._compileExpression(node.arr, frame);
            this.emitLine(';');
            var loopUses = {};
            node.iterFields(function (field) {
                var lookups = field.findAll(nodes.LookupVal);
                lib.each(lookups, function (lookup) {
                    if (lookup.target instanceof nodes.Symbol && lookup.target.value == 'loop' && lookup.val instanceof nodes.Literal) {
                        loopUses[lookup.val.value] = true;
                    }
                });
            });
            this.emit('if(' + arr + ' !== undefined) {');
            if (node.name instanceof nodes.Array) {
                this.emitLine('var ' + i + ';');
                this.emitLine('if (runtime.isArray(' + arr + ')) {');
                this.emitLine('for (' + i + '=0; ' + i + ' < ' + arr + '.length; '
                    + i + '++) {');
                for (var u = 0; u < node.name.children.length; u++) {
                    var tid = this.tmpid();
                    this.emitLine('var ' + tid + ' = ' + arr + '[' + i + '][' + u + ']');
                    this.emitLine('frame.set("' + node.name.children[u].value
                        + '", ' + arr + '[' + i + '][' + u + ']' + ');');
                    frame.set(node.name.children[u].value, tid);
                }
                if ('index'in loopUses) {
                    this.emitLine('frame.set("loop.index", ' + i + ' + 1);');
                }
                if ('index0'in loopUses) {
                    this.emitLine('frame.set("loop.index0", ' + i + ');');
                }
                if ('first'in loopUses) {
                    this.emitLine('frame.set("loop.first", ' + i + ' === 0);');
                }
                this.compile(node.body, frame);
                this.emitLine('}');
                this.emitLine('} else {');
                this.emitLine(i + ' = -1;');
                var key = node.name.children[0];
                var val = node.name.children[1];
                var k = this.tmpid();
                var v = this.tmpid();
                frame.set(key.value, k);
                frame.set(val.value, v);
                this.emitLine('for(var ' + k + ' in ' + arr + ') {');
                this.emitLine(i + '++;');
                this.emitLine('var ' + v + ' = ' + arr + '[' + k + '];');
                this.emitLine('frame.set("' + key.value + '", ' + k + ');');
                this.emitLine('frame.set("' + val.value + '", ' + v + ');');
                if ('index'in loopUses) {
                    this.emitLine('frame.set("loop.index", ' + i + ' + 1);');
                }
                if ('index0'in loopUses) {
                    this.emitLine('frame.set("loop.index0", ' + i + ');');
                }
                if ('first'in loopUses) {
                    this.emitLine('frame.set("loop.first", ' + i + ' === 0);');
                }
                this.compile(node.body, frame);
                this.emitLine('}');
                this.emitLine('}');
            }
            else {
                var v = this.tmpid();
                frame.set(node.name.value, v);
                this.emitLine('for(var ' + i + '=0; ' + i + ' < ' + arr + '.length; ' +
                    i + '++) {');
                this.emitLine('var ' + v + ' = ' + arr + '[' + i + '];');
                this.emitLine('frame.set("' + node.name.value + '", ' + v + ');');
                if ('index'in loopUses) {
                    this.emitLine('frame.set("loop.index", ' + i + ' + 1);');
                }
                if ('index0'in loopUses) {
                    this.emitLine('frame.set("loop.index0", ' + i + ');');
                }
                if ('revindex'in loopUses) {
                    this.emitLine('frame.set("loop.revindex", ' + arr + '.length - ' + i + ');');
                }
                if ('revindex0'in loopUses) {
                    this.emitLine('frame.set("loop.revindex0", ' + arr + '.length - ' + i + ' - 1);');
                }
                if ('first'in loopUses) {
                    this.emitLine('frame.set("loop.first", ' + i + ' === 0);');
                }
                if ('last'in loopUses) {
                    this.emitLine('frame.set("loop.last", ' + i + ' === ' + arr + '.length - 1);');
                }
                if ('length'in loopUses) {
                    this.emitLine('frame.set("loop.length", ' + arr + '.length);');
                }
                this.compile(node.body, frame);
                this.emitLine('}');
            }
            this.emit('}');
            this.emitLine('frame = frame.pop();');
        }, _emitMacroBegin: function (node, frame) {
            var args = [];
            var kwargs = null;
            var funcId = 'macro_' + this.tmpid();
            lib.each(node.args.children, function (arg, i) {
                if (i === node.args.children.length - 1 && arg instanceof nodes.Dict) {
                    kwargs = arg;
                }
                else {
                    this.assertType(arg, nodes.Symbol);
                    args.push(arg);
                }
            }, this);
            var realNames = lib.map(args, function (n) {
                return'l_' + n.value;
            });
            realNames.push('kwargs');
            var argNames = lib.map(args, function (n) {
                return'"' + n.value + '"';
            });
            var kwargNames = lib.map((kwargs && kwargs.children) || [], function (n) {
                return'"' + n.key.value + '"';
            });
            this.emitLines('var ' + funcId + ' = runtime.makeMacro(', '[' + argNames.join(', ') + '], ', '[' + kwargNames.join(', ') + '], ', 'function (' + realNames.join(', ') + ') {', 'frame = frame.push();', 'kwargs = kwargs || {};');
            lib.each(args, function (arg) {
                this.emitLine('frame.set("' + arg.value + '", ' + 'l_' + arg.value + ');');
                frame.set(arg.value, 'l_' + arg.value);
            }, this);
            if (kwargs) {
                lib.each(kwargs.children, function (pair) {
                    var name = pair.key.value;
                    this.emit('frame.set("' + name + '", ' + 'kwargs.hasOwnProperty("' + name + '") ? ' + 'kwargs["' + name + '"] : ');
                    this._compileExpression(pair.value, frame);
                    this.emitLine(');');
                }, this);
            }
            return funcId;
        }, _emitMacroEnd: function () {
            this.emitLine('frame = frame.pop();');
            this.emitLine('return new runtime.SafeString(' + this.buffer + ');');
            this.emitLine('});');
        }, compileMacro: function (node, frame) {
            frame = frame.push();
            var funcId = this._emitMacroBegin(node, frame);
            var prevBuffer = this.buffer;
            this.buffer = 'output';
            this.emitLine('var ' + this.buffer + '= "";');
            this.compile(node.body, frame);
            this._emitMacroEnd();
            this.buffer = prevBuffer;
            var name = node.name.value;
            frame = frame.pop();
            frame.set(name, funcId);
            if (frame.parent) {
                this.emitLine('frame.set("' + name + '", ' + funcId + ');');
            }
            else {
                if (node.name.value.charAt(0) != '_') {
                    this.emitLine('context.addExport("' + name + '");');
                }
                this.emitLine('context.setVariable("' + name + '", ' + funcId + ');');
            }
        }, compileImport: function (node, frame) {
            var id = this.tmpid();
            var target = node.target.value;
            this.emit('var ' + id + ' = env.getTemplate(');
            this._compileExpression(node.template, frame);
            this.emitLine(').getExported();');
            frame.set(target, id);
            if (frame.parent) {
                this.emitLine('frame.set("' + target + '", ' + id + ');');
            }
            else {
                this.emitLine('context.setVariable("' + target + '", ' + id + ');');
            }
        }, compileFromImport: function (node, frame) {
            this.emit('var imported = env.getTemplate(');
            this.compile(node.template, frame);
            this.emitLine(').getExported();');
            lib.each(node.names.children, function (nameNode) {
                var name;
                var alias;
                var id = this.tmpid();
                if (nameNode instanceof nodes.Pair) {
                    name = nameNode.key.value;
                    alias = nameNode.value.value;
                }
                else {
                    name = nameNode.value;
                    alias = name;
                }
                this.emitLine('if(imported.hasOwnProperty("' + name + '")) {');
                this.emitLine('var ' + id + ' = imported.' + name + ';');
                this.emitLine('} else {');
                this.emitLine('throw new Error("cannot import \'' + name + '\'")');
                this.emitLine('}');
                frame.set(alias, id);
                if (frame.parent) {
                    this.emitLine('frame.set("' + alias + '", ' + id + ');');
                }
                else {
                    this.emitLine('context.setVariable("' + alias + '", ' + id + ');');
                }
            }, this);
        }, compileBlock: function (node, frame) {
            if (!this.isChild) {
                this.emitLine(this.buffer + ' += context.getBlock("' +
                    node.name.value + '")(env, context, frame, runtime);');
            }
        }, compileExtends: function (node, frame) {
            if (this.isChild) {
                this.fail('compileExtends: cannot extend multiple times', node.template.lineno, node.template.colno);
            }
            this.emit('var parentTemplate = env.getTemplate(');
            this._compileExpression(node.template, frame);
            this.emitLine(', true);');
            var k = this.tmpid();
            this.emitLine('for(var ' + k + ' in parentTemplate.blocks) {');
            this.emitLine('context.addBlock(' + k + ', parentTemplate.blocks[' + k + ']);');
            this.emitLine('}');
            this.isChild = true;
        }, compileInclude: function (node, frame) {
            this.emit('var includeTemplate = env.getTemplate(');
            this._compileExpression(node.template, frame);
            this.emitLine(');');
            this.emitLine(this.buffer + ' += includeTemplate.render(' + 'context.getVariables(), frame.push());');
        }, compileTemplateData: function (node, frame) {
            this.compileLiteral(node, frame);
        }, compileOutput: function (node, frame) {
            var children = node.children;
            for (var i = 0, l = children.length; i < l; i++) {
                if (children[i]instanceof nodes.TemplateData) {
                    if (children[i].value) {
                        this.emit(this.buffer + ' += ');
                        this.compileLiteral(children[i], frame);
                        this.emitLine(';');
                    }
                }
                else {
                    this.emit(this.buffer + ' += runtime.suppressValue(');
                    this.compile(children[i], frame);
                    this.emit(', env.autoesc);\n');
                }
            }
        }, compileRoot: function (node, frame) {
            if (frame) {
                this.fail("compileRoot: root node can't have frame");
            }
            frame = new Frame();
            this.emitFuncBegin('root');
            this._compileChildren(node, frame);
            if (this.isChild) {
                this.emitLine('return ' + 'parentTemplate.rootRenderFunc(env, context, frame, runtime);');
            }
            this.emitFuncEnd(this.isChild);
            this.isChild = false;
            var blocks = node.findAll(nodes.Block);
            for (var i = 0; i < blocks.length; i++) {
                var block = blocks[i];
                var name = block.name.value;
                this.emitFuncBegin('b_' + name);
                this.emitLine('var l_super = context.getSuper(env, ' + '"' + name + '", ' + 'b_' + name + ', ' + 'frame, ' + 'runtime);');
                var tmpFrame = new Frame();
                tmpFrame.set('super', 'l_super');
                this.compile(block.body, tmpFrame);
                this.emitFuncEnd();
            }
            this.emitLine('return {');
            for (var i = 0; i < blocks.length; i++) {
                var block = blocks[i];
                var name = 'b_' + block.name.value;
                this.emitLine(name + ': ' + name + ',');
            }
            this.emitLine('root: root\n};');
        }, compile: function (node, frame) {
            var _compile = this["compile" + node.typename];
            if (_compile) {
                _compile.call(this, node, frame);
            }
            else {
                this.fail("compile: Cannot compile node: " + node.typename, node.lineno, node.colno);
            }
        }, getCode: function () {
            return this.codebuf.join('');
        }});
        modules['compiler'] = {compile: function (src, extensions, name) {
            var c = new Compiler(extensions);
            if (extensions && extensions.length) {
                for (var i = 0; i < extensions.length; i++) {
                    if ('preprocess'in extensions[i]) {
                        src = extensions[i].preprocess(src, name);
                    }
                }
            }
            c.compile(parser.parse(src, extensions));
            return c.getCode();
        }, Compiler: Compiler};
    })();
    (function () {
        var lib = modules["lib"];
        var r = modules["runtime"];
        var filters = {abs: function (n) {
            return Math.abs(n);
        }, batch: function (arr, linecount, fill_with) {
            var res = [];
            var tmp = [];
            for (var i = 0; i < arr.length; i++) {
                if (i % linecount === 0 && tmp.length) {
                    res.push(tmp);
                    tmp = [];
                }
                tmp.push(arr[i]);
            }
            if (tmp.length) {
                if (fill_with) {
                    for (var i = tmp.length; i < linecount; i++) {
                        tmp.push(fill_with);
                    }
                }
                res.push(tmp);
            }
            return res;
        }, capitalize: function (str) {
            var ret = str.toLowerCase();
            return r.copySafeness(str, ret[0].toUpperCase() + ret.slice(1));
        }, center: function (str, width) {
            width = width || 80;
            if (str.length >= width) {
                return str;
            }
            var spaces = width - str.length;
            var pre = lib.repeat(" ", spaces / 2 - spaces % 2);
            var post = lib.repeat(" ", spaces / 2);
            return r.copySafeness(str, pre + str + post);
        }, 'default': function (val, def) {
            return val ? val : def;
        }, dictsort: function (val, case_sensitive, by) {
            if (!lib.isObject(val)) {
                throw new lib.TemplateError("dictsort filter: val must be an object");
            }
            var array = [];
            for (var k in val) {
                array.push([k, val[k]]);
            }
            var si;
            if (by === undefined || by === "key") {
                si = 0;
            } else if (by === "value") {
                si = 1;
            } else {
                throw new lib.TemplateError("dictsort filter: You can only sort by either key or value");
            }
            array.sort(function (t1, t2) {
                var a = t1[si];
                var b = t2[si];
                if (!case_sensitive) {
                    if (lib.isString(a)) {
                        a = a.toUpperCase();
                    }
                    if (lib.isString(b)) {
                        b = b.toUpperCase();
                    }
                }
                return a > b ? 1 : (a == b ? 0 : -1);
            });
            return array;
        }, escape: function (str) {
            if (typeof str == 'string' || str instanceof r.SafeString) {
                return lib.escape(str);
            }
            return str;
        }, safe: function (str) {
            return new r.SafeString(str);
        }, first: function (arr) {
            return arr[0];
        }, groupby: function (arr, attr) {
            return lib.groupBy(arr, attr);
        }, indent: function (str, width, indentfirst) {
            width = width || 4;
            var res = '';
            var lines = str.split('\n');
            var sp = lib.repeat(' ', width);
            for (var i = 0; i < lines.length; i++) {
                if (i == 0 && !indentfirst) {
                    res += lines[i] + '\n';
                }
                else {
                    res += sp + lines[i] + '\n';
                }
            }
            return r.copySafeness(str, res);
        }, join: function (arr, del, attr) {
            del = del || '';
            if (attr) {
                arr = lib.map(arr, function (v) {
                    return v[attr];
                });
            }
            return arr.join(del);
        }, last: function (arr) {
            return arr[arr.length - 1];
        }, length: function (arr) {
            return arr.length;
        }, list: function (val) {
            if (lib.isString(val)) {
                return val.split('');
            }
            else if (lib.isObject(val)) {
                var keys = [];
                if (Object.keys) {
                    keys = Object.keys(val);
                }
                else {
                    for (var k in val) {
                        keys.push(k);
                    }
                }
                return lib.map(keys, function (k) {
                    return{key: k, value: val[k]};
                });
            }
            else {
                throw new lib.TemplateError("list filter: type not iterable");
            }
        }, lower: function (str) {
            return str.toLowerCase();
        }, random: function (arr) {
            var i = Math.floor(Math.random() * arr.length);
            if (i == arr.length) {
                i--;
            }
            return arr[i];
        }, replace: function (str, old, new_, maxCount) {
            var res = str;
            var last = res;
            var count = 1;
            res = res.replace(old, new_);
            while (last != res) {
                if (count >= maxCount) {
                    break;
                }
                last = res;
                res = res.replace(old, new_);
                count++;
            }
            return r.copySafeness(str, res);
        }, reverse: function (val) {
            var arr;
            if (lib.isString(val)) {
                arr = filters.list(val);
            }
            else {
                arr = lib.map(val, function (v) {
                    return v;
                });
            }
            arr.reverse();
            if (lib.isString(val)) {
                return r.copySafeness(val, arr.join(''));
            }
            return arr;
        }, round: function (val, precision, method) {
            precision = precision || 0;
            var factor = Math.pow(10, precision);
            var rounder;
            if (method == 'ceil') {
                rounder = Math.ceil;
            }
            else if (method == 'floor') {
                rounder = Math.floor;
            }
            else {
                rounder = Math.round;
            }
            return rounder(val * factor) / factor;
        }, slice: function (arr, slices, fillWith) {
            var sliceLength = Math.floor(arr.length / slices);
            var extra = arr.length % slices;
            var offset = 0;
            var res = [];
            for (var i = 0; i < slices; i++) {
                var start = offset + i * sliceLength;
                if (i < extra) {
                    offset++;
                }
                var end = offset + (i + 1) * sliceLength;
                var slice = arr.slice(start, end);
                if (fillWith && i >= extra) {
                    slice.push(fillWith);
                }
                res.push(slice);
            }
            return res;
        }, sort: function (arr, reverse, caseSens, attr) {
            arr = lib.map(arr, function (v) {
                return v;
            });
            arr.sort(function (a, b) {
                var x, y;
                if (attr) {
                    x = a[attr];
                    y = b[attr];
                }
                else {
                    x = a;
                    y = b;
                }
                if (!caseSens && lib.isString(x) && lib.isString(y)) {
                    x = x.toLowerCase();
                    y = y.toLowerCase();
                }
                if (x < y) {
                    return reverse ? 1 : -1;
                }
                else if (x > y) {
                    return reverse ? -1 : 1;
                }
                else {
                    return 0;
                }
            });
            return arr;
        }, string: function (obj) {
            return r.copySafeness(obj, obj);
        }, title: function (str) {
            var words = str.split(' ');
            for (var i = 0; i < words.length; i++) {
                words[i] = filters.capitalize(words[i]);
            }
            return r.copySafeness(str, words.join(' '));
        }, trim: function (str) {
            return r.copySafeness(str, str.replace(/^\s*|\s*$/g, ''));
        }, truncate: function (input, length, killwords, end) {
            var orig = input;
            length = length || 255;
            if (input.length <= length)
                return input;
            if (killwords) {
                input = input.substring(0, length);
            } else {
                var idx = input.lastIndexOf(' ', length);
                if (idx === -1) {
                    idx = length;
                }
                input = input.substring(0, idx);
            }
            input += (end !== undefined && end !== null) ? end : '...';
            return r.copySafeness(orig, input);
        }, upper: function (str) {
            return str.toUpperCase();
        }, wordcount: function (str) {
            return str.match(/\w+/g).length;
        }, 'float': function (val, def) {
            var res = parseFloat(val);
            return isNaN(res) ? def : res;
        }, 'int': function (val, def) {
            var res = parseInt(val, 10);
            return isNaN(res) ? def : res;
        }};
        filters.d = filters['default'];
        filters.e = filters.escape;
        modules['filters'] = filters;
    })();
    (function () {
        function cycler(items) {
            var index = -1;
            var current = null;
            return{reset: function () {
                index = -1;
                current = null;
            }, next: function () {
                index++;
                if (index >= items.length) {
                    index = 0;
                }
                current = items[index];
                return current;
            }};
        }

        function joiner(sep) {
            sep = sep || ',';
            var first = true;
            return function () {
                var val = first ? '' : sep;
                first = false;
                return val;
            };
        }

        var globals = {range: function (start, stop, step) {
            if (!stop) {
                stop = start;
                start = 0;
                step = 1;
            }
            else if (!step) {
                step = 1;
            }
            var arr = [];
            for (var i = start; i < stop; i += step) {
                arr.push(i);
            }
            return arr;
        }, cycler: function () {
            return cycler(Array.prototype.slice.call(arguments));
        }, joiner: function (sep) {
            return joiner(sep);
        }}
        modules['globals'] = globals;
    })();
    (function () {
        var Object = modules["object"];
        var HttpLoader = Object.extend({init: function (baseURL, neverUpdate) {
            console.log("[nunjucks] Warning: only use HttpLoader in " + "development. Otherwise precompile your templates.");
            this.baseURL = baseURL || '';
            this.neverUpdate = neverUpdate;
        }, getSource: function (name) {
            var src = this.fetch(this.baseURL + '/' + name);
            var _this = this;
            if (!src) {
                return null;
            }
            return{src: src, path: name, upToDate: function () {
                return _this.neverUpdate;
            }};
        }, fetch: function (url) {
            var ajax = new XMLHttpRequest();
            var src = null;
            ajax.onreadystatechange = function () {
                if (ajax.readyState == 4 && ajax.status == 200) {
                    src = ajax.responseText;
                }
            };
            url += (url.indexOf('?') === -1 ? '?' : '&') + 's=' + Date.now();
            ajax.open('GET', url, false);
            ajax.send();
            return src;
        }});
        modules['web-loaders'] = {HttpLoader: HttpLoader};
    })();
    (function () {
        if (typeof window === 'undefined') {
            modules['loaders'] = modules["node-loaders"];
        }
        else {
            modules['loaders'] = modules["web-loaders"];
        }
    })();
    (function () {
        var lib = modules["lib"];
        var Object = modules["object"];
        var lexer = modules["lexer"];
        var compiler = modules["compiler"];
        var builtin_filters = modules["filters"];
        var builtin_loaders = modules["loaders"];
        var runtime = modules["runtime"];
        var globals = modules["globals"];
        var Frame = runtime.Frame;
        var Environment = Object.extend({init: function (loaders, opts) {
            opts = opts || {};
            this.dev = !!opts.dev;
            this.autoesc = !!opts.autoescape;
            if (!loaders) {
                if (builtin_loaders.FileSystemLoader) {
                    this.loaders = [new builtin_loaders.FileSystemLoader()];
                }
                else {
                    this.loaders = [new builtin_loaders.HttpLoader('/views')];
                }
            }
            else {
                this.loaders = lib.isArray(loaders) ? loaders : [loaders];
            }
            if (opts.tags) {
                lexer.setTags(opts.tags);
            }
            this.filters = builtin_filters;
            this.cache = {};
            this.extensions = {};
            this.extensionsList = [];
        }, addExtension: function (name, extension) {
            extension._name = name;
            this.extensions[name] = extension;
            this.extensionsList.push(extension);
        }, getExtension: function (name) {
            return this.extensions[name];
        }, addFilter: function (name, func) {
            this.filters[name] = func;
        }, getFilter: function (name) {
            if (!this.filters[name]) {
                throw new Error('filter not found: ' + name);
            }
            return this.filters[name];
        }, getTemplate: function (name, eagerCompile) {
            if (name && name.raw) {
                name = name.raw;
            }
            var info = null;
            var tmpl = this.cache[name];
            var upToDate;
            if (typeof name !== 'string') {
                throw new Error('template names must be a string: ' + name);
            }
            if (!tmpl || !tmpl.isUpToDate()) {
                for (var i = 0; i < this.loaders.length; i++) {
                    if ((info = this.loaders[i].getSource(name))) {
                        break;
                    }
                }
                if (!info) {
                    throw new Error('template not found: ' + name);
                }
                this.cache[name] = new Template(info.src, this, info.path, info.upToDate, eagerCompile);
            }
            return this.cache[name];
        }, registerPrecompiled: function (templates) {
            for (var name in templates) {
                this.cache[name] = new Template({type: 'code', obj: templates[name]}, this, name, function () {
                    return true;
                }, true);
            }
        }, express: function (app) {
            var env = this;
            if (app.render) {
                app.render = function (name, ctx, k) {
                    var context = {};
                    if (lib.isFunction(ctx)) {
                        k = ctx;
                        ctx = {};
                    }
                    context = lib.extend(context, this.locals);
                    if (ctx._locals) {
                        context = lib.extend(context, ctx._locals);
                    }
                    context = lib.extend(context, ctx);
                    var res = env.render(name, context);
                    k(null, res);
                };
            }
            else {
                var http = modules["http"];
                var res = http.ServerResponse.prototype;
                res._render = function (name, ctx, k) {
                    var app = this.app;
                    var context = {};
                    if (this._locals) {
                        context = lib.extend(context, this._locals);
                    }
                    if (ctx) {
                        context = lib.extend(context, ctx);
                        if (ctx.locals) {
                            context = lib.extend(context, ctx.locals);
                        }
                    }
                    context = lib.extend(context, app._locals);
                    var str = env.render(name, context);
                    if (k) {
                        k(null, str);
                    }
                    else {
                        this.send(str);
                    }
                };
            }
        }, render: function (name, ctx) {
            return this.getTemplate(name).render(ctx);
        }});
        var Context = Object.extend({init: function (ctx, blocks) {
            this.ctx = ctx;
            this.blocks = {};
            this.exported = [];
            for (var name in blocks) {
                this.addBlock(name, blocks[name]);
            }
        }, lookup: function (name) {
            if (name in globals && !(name in this.ctx)) {
                return globals[name];
            }
            else {
                return this.ctx[name];
            }
        }, setVariable: function (name, val) {
            this.ctx[name] = val;
        }, getVariables: function () {
            return this.ctx;
        }, addBlock: function (name, block) {
            this.blocks[name] = this.blocks[name] || [];
            this.blocks[name].push(block);
        }, getBlock: function (name) {
            if (!this.blocks[name]) {
                throw new Error('unknown block "' + name + '"');
            }
            return this.blocks[name][0];
        }, getSuper: function (env, name, block, frame, runtime) {
            var idx = (this.blocks[name] || []).indexOf(block);
            var blk = this.blocks[name][idx + 1];
            var context = this;
            return function () {
                if (idx == -1 || !blk) {
                    throw new Error('no super block available for "' + name + '"');
                }
                return blk(env, context, frame, runtime);
            };
        }, addExport: function (name) {
            this.exported.push(name);
        }, getExported: function () {
            var exported = {};
            for (var i = 0; i < this.exported.length; i++) {
                var name = this.exported[i];
                exported[name] = this.ctx[name];
            }
            return exported;
        }});
        var Template = Object.extend({init: function (src, env, path, upToDate, eagerCompile) {
            this.env = env || new Environment();
            if (lib.isObject(src)) {
                switch (src.type) {
                    case'code':
                        this.tmplProps = src.obj;
                        break;
                    case'string':
                        this.tmplStr = src.obj;
                        break;
                }
            }
            else if (lib.isString(src)) {
                this.tmplStr = src;
            }
            else {
                throw new Error("src must be a string or an object describing " + "the source");
            }
            this.path = path;
            this.upToDate = upToDate || function () {
                return false;
            };
            if (eagerCompile) {
                var _this = this;
                lib.withPrettyErrors(this.path, this.env.dev, function () {
                    _this._compile();
                });
            }
            else {
                this.compiled = false;
            }
        }, render: function (ctx, frame) {
            var self = this;
            var render = function () {
                if (!self.compiled) {
                    self._compile();
                }
                var context = new Context(ctx || {}, self.blocks);
                return self.rootRenderFunc(self.env, context, frame || new Frame(), runtime);
            };
            return lib.withPrettyErrors(this.path, this.env.dev, render);
        }, isUpToDate: function () {
            return this.upToDate();
        }, getExported: function () {
            if (!this.compiled) {
                this._compile();
            }
            var context = new Context({}, this.blocks);
            this.rootRenderFunc(this.env, context, new Frame(), runtime);
            return context.getExported();
        }, _compile: function () {
            var props;
            if (this.tmplProps) {
                props = this.tmplProps;
            }
            else {
                var source = compiler.compile(this.tmplStr, this.env.extensionsList, this.path);
                var func = new Function(source);
                props = func();
            }
            this.blocks = this._getBlocks(props);
            this.rootRenderFunc = props.root;
            this.compiled = true;
        }, _getBlocks: function (props) {
            var blocks = {};
            for (var k in props) {
                if (k.slice(0, 2) == 'b_') {
                    blocks[k.slice(2)] = props[k];
                }
            }
            return blocks;
        }});
        modules['environment'] = {Environment: Environment, Template: Template};
    })();
    var nunjucks;
    var env = modules["environment"];
    var compiler = modules["compiler"];
    var parser = modules["parser"];
    var lexer = modules["lexer"];
    var runtime = modules["runtime"];
    var loaders = modules["loaders"];
    nunjucks = {};
    nunjucks.Environment = env.Environment;
    nunjucks.Template = env.Template;
    if (loaders) {
        if (loaders.FileSystemLoader) {
            nunjucks.FileSystemLoader = loaders.FileSystemLoader;
        }
        else {
            nunjucks.HttpLoader = loaders.HttpLoader;
        }
    }
    nunjucks.compiler = compiler;
    nunjucks.parser = parser;
    nunjucks.lexer = lexer;
    nunjucks.runtime = runtime;
    nunjucks.require = function (name) {
        return modules[name];
    };
    if (typeof define === 'function' && define.amd) {
        define(function () {
            return nunjucks;
        });
    }
    else {
        window.nunjucks = nunjucks;
    }
})();
(function () {
    var modules = {};
    (function () {
        function extend(cls, name, props) {
            var prototype = Object.create(cls.prototype);
            var fnTest = /xyz/.test(function () {
                xyz;
            }) ? /\bparent\b/ : /.*/;
            props = props || {};
            for (var k in props) {
                var src = props[k];
                var parent = prototype[k];
                if (typeof parent == "function" && typeof src == "function" && fnTest.test(src)) {
                    prototype[k] = (function (src, parent) {
                        return function () {
                            var tmp = this.parent;
                            this.parent = parent;
                            var res = src.apply(this, arguments);
                            this.parent = tmp;
                            return res;
                        };
                    })(src, parent);
                }
                else {
                    prototype[k] = src;
                }
            }
            prototype.typename = name;
            var new_cls = function () {
                if (prototype.init) {
                    prototype.init.apply(this, arguments);
                }
            };
            new_cls.prototype = prototype;
            new_cls.prototype.constructor = new_cls;
            new_cls.extend = function (name, props) {
                if (typeof name == "object") {
                    props = name;
                    name = "anonymous";
                }
                return extend(new_cls, name, props);
            };
            return new_cls;
        }

        modules['object'] = extend(Object, "Object", {});
    })();
    (function () {
        var ArrayProto = Array.prototype;
        var ObjProto = Object.prototype;
        var escapeMap = {'&': '&amp;', '"': '&quot;', "'": '&#39;', "<": '&lt;', ">": '&gt;'};
        var lookupEscape = function (ch) {
            return escapeMap[ch];
        };
        var exports = modules['lib'] = {};
        exports.withPrettyErrors = function (path, withInternals, func) {
            try {
                return func();
            } catch (e) {
                if (!e.Update) {
                    e = new exports.TemplateError(e);
                }
                e.Update(path);
                if (!withInternals) {
                    var old = e;
                    e = new Error(old.message);
                    e.name = old.name;
                }
                throw e;
            }
        }
        exports.TemplateError = function (message, lineno, colno) {
            var err = this;
            if (message instanceof Error) {
                err = message;
                message = message.name + ": " + message.message;
            } else {
                if (Error.captureStackTrace) {
                    Error.captureStackTrace(err);
                }
            }
            err.name = "Template render error";
            err.message = message;
            err.lineno = lineno;
            err.colno = colno;
            err.firstUpdate = true;
            err.Update = function (path) {
                var message = "(" + (path || "unknown path") + ")";
                if (this.firstUpdate) {
                    if (this.lineno && this.colno) {
                        message += ' [Line ' + this.lineno + ', Column ' + this.colno + ']';
                    }
                    else if (this.lineno) {
                        message += ' [Line ' + this.lineno + ']';
                    }
                }
                message += '\n ';
                if (this.firstUpdate) {
                    message += ' ';
                }
                this.message = message + (this.message || '');
                this.firstUpdate = false;
                return this;
            };
            return err;
        };
        exports.TemplateError.prototype = Error.prototype;
        exports.escape = function (val) {
            return val.replace(/[&"'<>]/g, lookupEscape);
        };
        exports.isFunction = function (obj) {
            return ObjProto.toString.call(obj) == '[object Function]';
        };
        exports.isArray = Array.isArray || function (obj) {
            return ObjProto.toString.call(obj) == '[object Array]';
        };
        exports.isString = function (obj) {
            return ObjProto.toString.call(obj) == '[object String]';
        };
        exports.isObject = function (obj) {
            return obj === Object(obj);
        };
        exports.groupBy = function (obj, val) {
            var result = {};
            var iterator = exports.isFunction(val) ? val : function (obj) {
                return obj[val];
            };
            for (var i = 0; i < obj.length; i++) {
                var value = obj[i];
                var key = iterator(value, i);
                (result[key] || (result[key] = [])).push(value);
            }
            return result;
        };
        exports.toArray = function (obj) {
            return Array.prototype.slice.call(obj);
        };
        exports.without = function (array) {
            var result = [];
            if (!array) {
                return result;
            }
            var index = -1, length = array.length, contains = exports.toArray(arguments).slice(1);
            while (++index < length) {
                if (contains.indexOf(array[index]) === -1) {
                    result.push(array[index]);
                }
            }
            return result;
        };
        exports.extend = function (obj, obj2) {
            for (var k in obj2) {
                obj[k] = obj2[k];
            }
            return obj;
        };
        exports.repeat = function (char_, n) {
            var str = '';
            for (var i = 0; i < n; i++) {
                str += char_;
            }
            return str;
        };
        exports.each = function (obj, func, context) {
            if (obj == null) {
                return;
            }
            if (ArrayProto.each && obj.each == ArrayProto.each) {
                obj.forEach(func, context);
            }
            else if (obj.length === +obj.length) {
                for (var i = 0, l = obj.length; i < l; i++) {
                    func.call(context, obj[i], i, obj);
                }
            }
        };
        exports.map = function (obj, func) {
            var results = [];
            if (obj == null) {
                return results;
            }
            if (ArrayProto.map && obj.map === ArrayProto.map) {
                return obj.map(func);
            }
            for (var i = 0; i < obj.length; i++) {
                results[results.length] = func(obj[i], i);
            }
            if (obj.length === +obj.length) {
                results.length = obj.length;
            }
            return results;
        };
    })();
    (function () {
        var util = modules["util"];
        var lib = modules["lib"];
        var Object = modules["object"];

        function traverseAndCheck(obj, type, results) {
            if (obj instanceof type) {
                results.push(obj);
            }
            if (obj instanceof Node) {
                obj.findAll(type, results);
            }
        }

        var Node = Object.extend("Node", {init: function (lineno, colno) {
            this.lineno = lineno;
            this.colno = colno;
            var fields = this.fields;
            for (var i = 0, l = fields.length; i < l; i++) {
                var field = fields[i];
                var val = arguments[i + 2];
                if (val === undefined) {
                    val = null;
                }
                this[field] = val;
            }
        }, findAll: function (type, results) {
            results = results || [];
            if (this instanceof NodeList) {
                var children = this.children;
                for (var i = 0, l = children.length; i < l; i++) {
                    traverseAndCheck(children[i], type, results);
                }
            }
            else {
                var fields = this.fields;
                for (var i = 0, l = fields.length; i < l; i++) {
                    traverseAndCheck(this[fields[i]], type, results);
                }
            }
            return results;
        }, iterFields: function (func) {
            lib.each(this.fields, function (field) {
                func(this[field], field);
            }, this);
        }});
        var Value = Node.extend("Value", {fields: ['value']});
        var NodeList = Node.extend("NodeList", {fields: ['children'], init: function (lineno, colno, nodes) {
            this.parent(lineno, colno, nodes || []);
        }, addChild: function (node) {
            this.children.push(node);
        }});
        var Root = NodeList.extend("Root");
        var Literal = Value.extend("Literal");
        var Symbol = Value.extend("Symbol");
        var Group = NodeList.extend("Group");
        var Array = NodeList.extend("Array");
        var Pair = Node.extend("Pair", {fields: ['key', 'value']});
        var Dict = NodeList.extend("Dict");
        var LookupVal = Node.extend("LookupVal", {fields: ['target', 'val']});
        var If = Node.extend("If", {fields: ['cond', 'body', 'else_']});
        var InlineIf = Node.extend("InlineIf", {fields: ['cond', 'body', 'else_']});
        var For = Node.extend("For", {fields: ['arr', 'name', 'body']});
        var Macro = Node.extend("Macro", {fields: ['name', 'args', 'body']});
        var Import = Node.extend("Import", {fields: ['template', 'target']});
        var FromImport = Node.extend("FromImport", {fields: ['template', 'names'], init: function (lineno, colno, template, names) {
            this.parent(lineno, colno, template, names || new NodeList());
        }});
        var FunCall = Node.extend("FunCall", {fields: ['name', 'args']});
        var Filter = FunCall.extend("Filter");
        var KeywordArgs = Dict.extend("KeywordArgs");
        var Block = Node.extend("Block", {fields: ['name', 'body']});
        var TemplateRef = Node.extend("TemplateRef", {fields: ['template']});
        var Extends = TemplateRef.extend("Extends");
        var Include = TemplateRef.extend("Include");
        var Set = Node.extend("Set", {fields: ['targets', 'value']});
        var Output = NodeList.extend("Output");
        var TemplateData = Literal.extend("TemplateData");
        var UnaryOp = Node.extend("UnaryOp", {fields: ['target']});
        var BinOp = Node.extend("BinOp", {fields: ['left', 'right']});
        var Or = BinOp.extend("Or");
        var And = BinOp.extend("And");
        var Not = UnaryOp.extend("Not");
        var Add = BinOp.extend("Add");
        var Sub = BinOp.extend("Sub");
        var Mul = BinOp.extend("Mul");
        var Div = BinOp.extend("Div");
        var FloorDiv = BinOp.extend("FloorDiv");
        var Mod = BinOp.extend("Mod");
        var Pow = BinOp.extend("Pow");
        var Neg = UnaryOp.extend("Neg");
        var Pos = UnaryOp.extend("Pos");
        var Compare = Node.extend("Compare", {fields: ['expr', 'ops']});
        var CompareOperand = Node.extend("CompareOperand", {fields: ['expr', 'type']});
        var CustomTag = Node.extend("CustomTag", {init: function (lineno, colno, name) {
            this.lineno = lineno;
            this.colno = colno;
            this.name = name;
        }});
        var CallExtension = Node.extend("CallExtension", {fields: ['extName', 'prop', 'args', 'contentArgs'], init: function (ext, prop, args, contentArgs) {
            this.extName = ext._name;
            this.prop = prop;
            this.args = args;
            this.contentArgs = contentArgs;
        }});

        function printNodes(node, indent) {
            indent = indent || 0;
            function print(str, indent, inline) {
                var lines = str.split("\n");
                for (var i = 0; i < lines.length; i++) {
                    if (lines[i]) {
                        if ((inline && i > 0) || !inline) {
                            for (var j = 0; j < indent; j++) {
                                util.print(" ");
                            }
                        }
                    }
                    if (i === lines.length - 1) {
                        util.print(lines[i]);
                    }
                    else {
                        util.puts(lines[i]);
                    }
                }
            }

            print(node.typename + ": ", indent);
            if (node instanceof NodeList) {
                print('\n');
                lib.each(node.children, function (n) {
                    printNodes(n, indent + 2);
                });
            }
            else {
                var nodes = null;
                var props = null;
                node.iterFields(function (val, field) {
                    if (val instanceof Node) {
                        nodes = nodes || {};
                        nodes[field] = val;
                    }
                    else {
                        props = props || {};
                        props[field] = val;
                    }
                });
                if (props) {
                    print(util.inspect(props, true, null) + '\n', null, true);
                }
                else {
                    print('\n');
                }
                if (nodes) {
                    for (var k in nodes) {
                        printNodes(nodes[k], indent + 2);
                    }
                }
            }
        }

        modules['nodes'] = {Node: Node, Root: Root, NodeList: NodeList, Value: Value, Literal: Literal, Symbol: Symbol, Group: Group, Array: Array, Pair: Pair, Dict: Dict, Output: Output, TemplateData: TemplateData, If: If, InlineIf: InlineIf, For: For, Macro: Macro, Import: Import, FromImport: FromImport, FunCall: FunCall, Filter: Filter, KeywordArgs: KeywordArgs, Block: Block, Extends: Extends, Include: Include, Set: Set, LookupVal: LookupVal, BinOp: BinOp, Or: Or, And: And, Not: Not, Add: Add, Sub: Sub, Mul: Mul, Div: Div, FloorDiv: FloorDiv, Mod: Mod, Pow: Pow, Neg: Neg, Pos: Pos, Compare: Compare, CompareOperand: CompareOperand, CallExtension: CallExtension, printNodes: printNodes};
    })();
    (function () {
        var lib = modules["lib"];
        var Object = modules["object"];
        var Frame = Object.extend({init: function (parent) {
            this.variables = {};
            this.parent = parent;
        }, set: function (name, val) {
            var parts = name.split('.');
            var obj = this.variables;
            for (var i = 0; i < parts.length - 1; i++) {
                var id = parts[i];
                if (!obj[id]) {
                    obj[id] = {};
                }
                obj = obj[id];
            }
            obj[parts[parts.length - 1]] = val;
        }, get: function (name) {
            var val = this.variables[name];
            if (val !== undefined && val !== null) {
                return val;
            }
            return null;
        }, lookup: function (name) {
            var p = this.parent;
            var val = this.variables[name];
            if (val !== undefined && val !== null) {
                return val;
            }
            return p && p.lookup(name);
        }, push: function () {
            return new Frame(this);
        }, pop: function () {
            return this.parent;
        }});

        function makeMacro(argNames, kwargNames, func) {
            return function () {
                var argCount = numArgs(arguments);
                var args;
                var kwargs = getKeywordArgs(arguments);
                if (argCount > argNames.length) {
                    args = Array.prototype.slice.call(arguments, 0, argNames.length);
                    var vals = Array.prototype.slice.call(arguments, args.length, argCount);
                    for (var i = 0; i < vals.length; i++) {
                        if (i < kwargNames.length) {
                            kwargs[kwargNames[i]] = vals[i];
                        }
                    }
                    args.push(kwargs);
                }
                else if (argCount < argNames.length) {
                    args = Array.prototype.slice.call(arguments, 0, argCount);
                    for (var i = argCount; i < argNames.length; i++) {
                        var arg = argNames[i];
                        args.push(kwargs[arg]);
                        delete kwargs[arg];
                    }
                    args.push(kwargs);
                }
                else {
                    args = arguments;
                }
                return func.apply(this, args);
            };
        }

        function makeKeywordArgs(obj) {
            obj.__keywords = true;
            return obj;
        }

        function getKeywordArgs(args) {
            var len = args.length;
            if (len) {
                var lastArg = args[len - 1];
                if (lastArg && lastArg.hasOwnProperty('__keywords')) {
                    return lastArg;
                }
            }
            return{};
        }

        function numArgs(args) {
            var len = args.length;
            if (len === 0) {
                return 0;
            }
            var lastArg = args[len - 1];
            if (lastArg && lastArg.hasOwnProperty('__keywords')) {
                return len - 1;
            }
            else {
                return len;
            }
        }

        function SafeString(val) {
            if (typeof val != 'string') {
                return val;
            }
            this.toString = function () {
                return val;
            };
            this.length = val.length;
            var methods = ['charAt', 'charCodeAt', 'concat', 'contains', 'endsWith', 'fromCharCode', 'indexOf', 'lastIndexOf', 'length', 'localeCompare', 'match', 'quote', 'replace', 'search', 'slice', 'split', 'startsWith', 'substr', 'substring', 'toLocaleLowerCase', 'toLocaleUpperCase', 'toLowerCase', 'toUpperCase', 'trim', 'trimLeft', 'trimRight'];
            for (var i = 0; i < methods.length; i++) {
                this[methods[i]] = proxyStr(val[methods[i]]);
            }
        }

        function copySafeness(dest, target) {
            if (dest instanceof SafeString) {
                return new SafeString(target);
            }
            return target.toString();
        }

        function proxyStr(func) {
            return function () {
                var ret = func.apply(this, arguments);
                if (typeof ret == 'string') {
                    return new SafeString(ret);
                }
                return ret;
            };
        }

        function suppressValue(val, autoescape) {
            val = (val !== undefined && val !== null) ? val : "";
            if (autoescape && typeof val === "string") {
                val = lib.escape(val);
            }
            return val;
        }

        function memberLookup(obj, val) {
            obj = obj || {};
            if (typeof obj[val] === 'function') {
                return function () {
                    return obj[val].apply(obj, arguments);
                };
            }
            return obj[val];
        }

        function callWrap(obj, name, args) {
            if (!obj) {
                throw new Error('Unable to call `' + name + '`, which is undefined or falsey');
            }
            else if (typeof obj !== 'function') {
                throw new Error('Unable to call `' + name + '`, which is not a function');
            }
            return obj.apply(this, args);
        }

        function contextOrFrameLookup(context, frame, name) {
            var val = context.lookup(name);
            return(val !== undefined && val !== null) ? val : frame.lookup(name);
        }

        function handleError(error, lineno, colno) {
            if (error.lineno) {
                throw error;
            }
            else {
                throw new lib.TemplateError(error, lineno, colno);
            }
        }

        modules['runtime'] = {Frame: Frame, makeMacro: makeMacro, makeKeywordArgs: makeKeywordArgs, numArgs: numArgs, suppressValue: suppressValue, memberLookup: memberLookup, contextOrFrameLookup: contextOrFrameLookup, callWrap: callWrap, handleError: handleError, isArray: lib.isArray, SafeString: SafeString, copySafeness: copySafeness};
    })();
    (function () {
        var whitespaceChars = " \n\t\r";
        var delimChars = "()[]{}%*-+/#,:|.<>=!";
        var intChars = "0123456789";
        var BLOCK_START = "{%";
        var BLOCK_END = "%}";
        var VARIABLE_START = "{{";
        var VARIABLE_END = "}}";
        var COMMENT_START = "{#";
        var COMMENT_END = "#}";
        var TOKEN_STRING = "string";
        var TOKEN_WHITESPACE = "whitespace";
        var TOKEN_DATA = "data";
        var TOKEN_BLOCK_START = "block-start";
        var TOKEN_BLOCK_END = "block-end";
        var TOKEN_VARIABLE_START = "variable-start";
        var TOKEN_VARIABLE_END = "variable-end";
        var TOKEN_COMMENT = "comment";
        var TOKEN_LEFT_PAREN = "left-paren";
        var TOKEN_RIGHT_PAREN = "right-paren";
        var TOKEN_LEFT_BRACKET = "left-bracket";
        var TOKEN_RIGHT_BRACKET = "right-bracket";
        var TOKEN_LEFT_CURLY = "left-curly";
        var TOKEN_RIGHT_CURLY = "right-curly";
        var TOKEN_OPERATOR = "operator";
        var TOKEN_COMMA = "comma";
        var TOKEN_COLON = "colon";
        var TOKEN_PIPE = "pipe";
        var TOKEN_INT = "int";
        var TOKEN_FLOAT = "float";
        var TOKEN_BOOLEAN = "boolean";
        var TOKEN_SYMBOL = "symbol";
        var TOKEN_SPECIAL = "special";

        function token(type, value, lineno, colno) {
            return{type: type, value: value, lineno: lineno, colno: colno};
        }

        function Tokenizer(str) {
            this.str = str;
            this.index = 0;
            this.len = str.length;
            this.lineno = 0;
            this.colno = 0;
            this.in_code = false;
        }

        Tokenizer.prototype.nextToken = function () {
            var lineno = this.lineno;
            var colno = this.colno;
            if (this.in_code) {
                var cur = this.current();
                var tok;
                if (this.is_finished()) {
                    return null;
                }
                else if (cur == "\"" || cur == "'") {
                    return token(TOKEN_STRING, this.parseString(cur), lineno, colno);
                }
                else if ((tok = this._extract(whitespaceChars))) {
                    return token(TOKEN_WHITESPACE, tok, lineno, colno);
                }
                else if ((tok = this._extractString(BLOCK_END)) || (tok = this._extractString('-' + BLOCK_END))) {
                    this.in_code = false;
                    return token(TOKEN_BLOCK_END, tok, lineno, colno);
                }
                else if ((tok = this._extractString(VARIABLE_END))) {
                    this.in_code = false;
                    return token(TOKEN_VARIABLE_END, tok, lineno, colno);
                }
                else if (delimChars.indexOf(cur) != -1) {
                    this.forward();
                    var complexOps = ['==', '!=', '<=', '>=', '//', '**'];
                    var curComplex = cur + this.current();
                    var type;
                    if (complexOps.indexOf(curComplex) != -1) {
                        this.forward();
                        cur = curComplex;
                    }
                    switch (cur) {
                        case"(":
                            type = TOKEN_LEFT_PAREN;
                            break;
                        case")":
                            type = TOKEN_RIGHT_PAREN;
                            break;
                        case"[":
                            type = TOKEN_LEFT_BRACKET;
                            break;
                        case"]":
                            type = TOKEN_RIGHT_BRACKET;
                            break;
                        case"{":
                            type = TOKEN_LEFT_CURLY;
                            break;
                        case"}":
                            type = TOKEN_RIGHT_CURLY;
                            break;
                        case",":
                            type = TOKEN_COMMA;
                            break;
                        case":":
                            type = TOKEN_COLON;
                            break;
                        case"|":
                            type = TOKEN_PIPE;
                            break;
                        default:
                            type = TOKEN_OPERATOR;
                    }
                    return token(type, cur, lineno, colno);
                }
                else {
                    tok = this._extractUntil(whitespaceChars + delimChars);
                    if (tok.match(/^[-+]?[0-9]+$/)) {
                        if (this.current() == '.') {
                            this.forward();
                            var dec = this._extract(intChars);
                            return token(TOKEN_FLOAT, tok + '.' + dec, lineno, colno);
                        }
                        else {
                            return token(TOKEN_INT, tok, lineno, colno);
                        }
                    }
                    else if (tok.match(/^(true|false)$/)) {
                        return token(TOKEN_BOOLEAN, tok, lineno, colno);
                    }
                    else if (tok) {
                        return token(TOKEN_SYMBOL, tok, lineno, colno);
                    }
                    else {
                        throw new Error("Unexpected value while parsing: " + tok);
                    }
                }
            }
            else {
                var beginChars = (BLOCK_START[0] +
                    VARIABLE_START[0] +
                    COMMENT_START[0] +
                    COMMENT_END[0]);
                var tok;
                if (this.is_finished()) {
                    return null;
                }
                else if ((tok = this._extractString(BLOCK_START + '-')) || (tok = this._extractString(BLOCK_START))) {
                    this.in_code = true;
                    return token(TOKEN_BLOCK_START, tok, lineno, colno);
                }
                else if ((tok = this._extractString(VARIABLE_START))) {
                    this.in_code = true;
                    return token(TOKEN_VARIABLE_START, tok, lineno, colno);
                }
                else {
                    tok = '';
                    var data;
                    var in_comment = false;
                    if (this._matches(COMMENT_START)) {
                        in_comment = true;
                        tok = this._extractString(COMMENT_START);
                    }
                    while ((data = this._extractUntil(beginChars)) !== null) {
                        tok += data;
                        if ((this._matches(BLOCK_START) || this._matches(VARIABLE_START) || this._matches(COMMENT_START)) && !in_comment) {
                            break;
                        }
                        else if (this._matches(COMMENT_END)) {
                            if (!in_comment) {
                                throw new Error("unexpected end of comment");
                            }
                            tok += this._extractString(COMMENT_END);
                            break;
                        }
                        else {
                            tok += this.current();
                            this.forward();
                        }
                    }
                    if (data === null && in_comment) {
                        throw new Error("expected end of comment, got end of file");
                    }
                    return token(in_comment ? TOKEN_COMMENT : TOKEN_DATA, tok, lineno, colno);
                }
            }
            throw new Error("Could not parse text");
        };
        Tokenizer.prototype.parseString = function (delimiter) {
            this.forward();
            var lineno = this.lineno;
            var colno = this.colno;
            var str = "";
            while (this.current() != delimiter) {
                var cur = this.current();
                if (cur == "\\") {
                    this.forward();
                    switch (this.current()) {
                        case"n":
                            str += "\n";
                            break;
                        case"t":
                            str += "\t";
                            break;
                        case"r":
                            str += "\r";
                            break;
                        default:
                            str += this.current();
                    }
                    this.forward();
                }
                else {
                    str += cur;
                    this.forward();
                }
            }
            this.forward();
            return str;
        };
        Tokenizer.prototype._matches = function (str) {
            if (this.index + str.length > this.length) {
                return null;
            }
            var m = this.str.slice(this.index, this.index + str.length);
            return m == str;
        };
        Tokenizer.prototype._extractString = function (str) {
            if (this._matches(str)) {
                this.index += str.length;
                return str;
            }
            return null;
        };
        Tokenizer.prototype._extractUntil = function (charString) {
            return this._extractMatching(true, charString || "");
        };
        Tokenizer.prototype._extract = function (charString) {
            return this._extractMatching(false, charString);
        };
        Tokenizer.prototype._extractMatching = function (breakOnMatch, charString) {
            if (this.is_finished()) {
                return null;
            }
            var first = charString.indexOf(this.current());
            if ((breakOnMatch && first == -1) || (!breakOnMatch && first != -1)) {
                var t = this.current();
                this.forward();
                var idx = charString.indexOf(this.current());
                while (((breakOnMatch && idx == -1) || (!breakOnMatch && idx != -1)) && !this.is_finished()) {
                    t += this.current();
                    this.forward();
                    idx = charString.indexOf(this.current());
                }
                return t;
            }
            return"";
        };
        Tokenizer.prototype.is_finished = function () {
            return this.index >= this.len;
        };
        Tokenizer.prototype.forwardN = function (n) {
            for (var i = 0; i < n; i++) {
                this.forward();
            }
        };
        Tokenizer.prototype.forward = function () {
            this.index++;
            if (this.previous() == "\n") {
                this.lineno++;
                this.colno = 0;
            }
            else {
                this.colno++;
            }
        };
        Tokenizer.prototype.backN = function (n) {
            for (var i = 0; i < n; i++) {
                self.back();
            }
        };
        Tokenizer.prototype.back = function () {
            this.index--;
            if (this.current() == "\n") {
                this.lineno--;
                var idx = this.src.lastIndexOf("\n", this.index - 1);
                if (idx == -1) {
                    this.colno = this.index;
                }
                else {
                    this.colno = this.index - idx;
                }
            }
            else {
                this.colno--;
            }
        };
        Tokenizer.prototype.current = function () {
            if (!this.is_finished()) {
                return this.str[this.index];
            }
            return"";
        };
        Tokenizer.prototype.previous = function () {
            return this.str[this.index - 1];
        };
        modules['lexer'] = {lex: function (src) {
            return new Tokenizer(src);
        }, setTags: function (tags) {
            BLOCK_START = tags.blockStart || BLOCK_START;
            BLOCK_END = tags.blockEnd || BLOCK_END;
            VARIABLE_START = tags.variableStart || VARIABLE_START;
            VARIABLE_END = tags.variableEnd || VARIABLE_END;
            COMMENT_START = tags.commentStart || COMMENT_START;
            COMMENT_END = tags.commentEnd || COMMENT_END;
        }, TOKEN_STRING: TOKEN_STRING, TOKEN_WHITESPACE: TOKEN_WHITESPACE, TOKEN_DATA: TOKEN_DATA, TOKEN_BLOCK_START: TOKEN_BLOCK_START, TOKEN_BLOCK_END: TOKEN_BLOCK_END, TOKEN_VARIABLE_START: TOKEN_VARIABLE_START, TOKEN_VARIABLE_END: TOKEN_VARIABLE_END, TOKEN_COMMENT: TOKEN_COMMENT, TOKEN_LEFT_PAREN: TOKEN_LEFT_PAREN, TOKEN_RIGHT_PAREN: TOKEN_RIGHT_PAREN, TOKEN_LEFT_BRACKET: TOKEN_LEFT_BRACKET, TOKEN_RIGHT_BRACKET: TOKEN_RIGHT_BRACKET, TOKEN_LEFT_CURLY: TOKEN_LEFT_CURLY, TOKEN_RIGHT_CURLY: TOKEN_RIGHT_CURLY, TOKEN_OPERATOR: TOKEN_OPERATOR, TOKEN_COMMA: TOKEN_COMMA, TOKEN_COLON: TOKEN_COLON, TOKEN_PIPE: TOKEN_PIPE, TOKEN_INT: TOKEN_INT, TOKEN_FLOAT: TOKEN_FLOAT, TOKEN_BOOLEAN: TOKEN_BOOLEAN, TOKEN_SYMBOL: TOKEN_SYMBOL, TOKEN_SPECIAL: TOKEN_SPECIAL};
    })();
    (function () {
        var lexer = modules["lexer"];
        var nodes = modules["nodes"];
        var Object = modules["object"];
        var lib = modules["lib"];
        var Parser = Object.extend({init: function (tokens) {
            this.tokens = tokens;
            this.peeked = null;
            this.breakOnBlocks = null;
            this.dropLeadingWhitespace = false;
            this.extensions = [];
        }, nextToken: function (withWhitespace) {
            var tok;
            if (this.peeked) {
                if (!withWhitespace && this.peeked.type == lexer.TOKEN_WHITESPACE) {
                    this.peeked = null;
                }
                else {
                    tok = this.peeked;
                    this.peeked = null;
                    return tok;
                }
            }
            tok = this.tokens.nextToken();
            if (!withWhitespace) {
                while (tok && tok.type == lexer.TOKEN_WHITESPACE) {
                    tok = this.tokens.nextToken();
                }
            }
            return tok;
        }, peekToken: function () {
            this.peeked = this.peeked || this.nextToken();
            return this.peeked;
        }, pushToken: function (tok) {
            if (this.peeked) {
                throw new Error("pushToken: can only push one token on between reads");
            }
            this.peeked = tok;
        }, fail: function (msg, lineno, colno) {
            if ((lineno === undefined || colno === undefined) && this.peekToken()) {
                var tok = this.peekToken();
                lineno = tok.lineno;
                colno = tok.colno;
            }
            if (lineno !== undefined)lineno += 1;
            if (colno !== undefined)colno += 1;
            throw new lib.TemplateError(msg, lineno, colno);
        }, skip: function (type) {
            var tok = this.nextToken();
            if (!tok || tok.type != type) {
                this.pushToken(tok);
                return false;
            }
            return true;
        }, expect: function (type) {
            var tok = this.nextToken();
            if (!tok.type == type) {
                this.fail('expected ' + type + ', got ' + tok.type, tok.lineno, tok.colno);
            }
            return tok;
        }, skipValue: function (type, val) {
            var tok = this.nextToken();
            if (!tok || tok.type != type || tok.value != val) {
                this.pushToken(tok);
                return false;
            }
            return true;
        }, skipWhitespace: function () {
            return this.skip(lexer.TOKEN_WHITESPACE);
        }, skipSymbol: function (val) {
            return this.skipValue(lexer.TOKEN_SYMBOL, val);
        }, advanceAfterBlockEnd: function (name) {
            if (!name) {
                var tok = this.peekToken();
                if (!tok) {
                    this.fail('unexpected end of file');
                }
                if (tok.type != lexer.TOKEN_SYMBOL) {
                    this.fail("advanceAfterBlockEnd: expected symbol token or " + "explicit name to be passed");
                }
                name = this.nextToken().value;
            }
            var tok = this.nextToken();
            if (tok.type == lexer.TOKEN_BLOCK_END) {
                if (tok.value.charAt(0) === '-') {
                    this.dropLeadingWhitespace = true;
                }
            }
            else {
                this.fail("expected block end in " + name + " statement");
            }
        }, advanceAfterVariableEnd: function () {
            if (!this.skip(lexer.TOKEN_VARIABLE_END)) {
                this.fail("expected variable end");
            }
        }, parseFor: function () {
            var forTok = this.peekToken();
            if (!this.skipSymbol('for')) {
                this.fail("parseFor: expected for", forTok.lineno, forTok.colno);
            }
            var node = new nodes.For(forTok.lineno, forTok.colno);
            node.name = this.parsePrimary();
            if (!(node.name instanceof nodes.Symbol)) {
                this.fail('parseFor: variable name expected for loop');
            }
            var type = this.peekToken().type;
            if (type == lexer.TOKEN_COMMA) {
                var key = node.name;
                node.name = new nodes.Array(key.lineno, key.colno);
                node.name.addChild(key);
                while (this.skip(lexer.TOKEN_COMMA)) {
                    var prim = this.parsePrimary();
                    node.name.addChild(prim);
                }
            }
            if (!this.skipSymbol('in')) {
                this.fail('parseFor: expected "in" keyword for loop', forTok.lineno, forTok.colno);
            }
            node.arr = this.parseExpression();
            this.advanceAfterBlockEnd(forTok.value);
            node.body = this.parseUntilBlocks('endfor');
            this.advanceAfterBlockEnd();
            return node;
        }, parseMacro: function () {
            var macroTok = this.peekToken();
            if (!this.skipSymbol('macro')) {
                this.fail("expected macro");
            }
            var name = this.parsePrimary(true);
            var args = this.parseSignature();
            var node = new nodes.Macro(macroTok.lineno, macroTok.colno, name, args);
            this.advanceAfterBlockEnd(macroTok.value);
            node.body = this.parseUntilBlocks('endmacro');
            this.advanceAfterBlockEnd();
            return node;
        }, parseImport: function () {
            var importTok = this.peekToken();
            if (!this.skipSymbol('import')) {
                this.fail("parseImport: expected import", importTok.lineno, importTok.colno);
            }
            var template = this.parsePrimary();
            if (!this.skipSymbol('as')) {
                this.fail('parseImport: expected "as" keyword', importTok.lineno, importTok.colno);
            }
            var target = this.parsePrimary();
            var node = new nodes.Import(importTok.lineno, importTok.colno, template, target);
            this.advanceAfterBlockEnd(importTok.value);
            return node;
        }, parseFrom: function () {
            var fromTok = this.peekToken();
            if (!this.skipSymbol('from')) {
                this.fail("parseFrom: expected from");
            }
            var template = this.parsePrimary();
            var node = new nodes.FromImport(fromTok.lineno, fromTok.colno, template, new nodes.NodeList());
            if (!this.skipSymbol('import')) {
                this.fail("parseFrom: expected import", fromTok.lineno, fromTok.colno);
            }
            var names = node.names;
            while (1) {
                var nextTok = this.peekToken();
                if (nextTok.type == lexer.TOKEN_BLOCK_END) {
                    if (!names.children.length) {
                        this.fail('parseFrom: Expected at least one import name', fromTok.lineno, fromTok.colno);
                    }
                    if (nextTok.value.charAt(0) == '-') {
                        this.dropLeadingWhitespace = true;
                    }
                    this.nextToken();
                    break;
                }
                if (names.children.length > 0 && !this.skip(lexer.TOKEN_COMMA)) {
                    this.fail('parseFrom: expected comma', fromTok.lineno, fromTok.colno);
                }
                var name = this.parsePrimary();
                if (name.value.charAt(0) == '_') {
                    this.fail('parseFrom: names starting with an underscore ' + 'cannot be imported', name.lineno, name.colno);
                }
                if (this.skipSymbol('as')) {
                    var alias = this.parsePrimary();
                    names.addChild(new nodes.Pair(name.lineno, name.colno, name, alias));
                }
                else {
                    names.addChild(name);
                }
            }
            return node;
        }, parseBlock: function () {
            var tag = this.peekToken();
            if (!this.skipSymbol('block')) {
                this.fail('parseBlock: expected block', tag.lineno, tag.colno);
            }
            var node = new nodes.Block(tag.lineno, tag.colno);
            node.name = this.parsePrimary();
            if (!(node.name instanceof nodes.Symbol)) {
                this.fail('parseBlock: variable name expected', tag.lineno, tag.colno);
            }
            this.advanceAfterBlockEnd(tag.value);
            node.body = this.parseUntilBlocks('endblock');
            if (!this.peekToken()) {
                this.fail('parseBlock: expected endblock, got end of file');
            }
            this.advanceAfterBlockEnd();
            return node;
        }, parseTemplateRef: function (tagName, nodeType) {
            var tag = this.peekToken();
            if (!this.skipSymbol(tagName)) {
                this.fail('parseTemplateRef: expected ' + tagName);
            }
            var node = new nodeType(tag.lineno, tag.colno);
            node.template = this.parsePrimary();
            this.advanceAfterBlockEnd(tag.value);
            return node;
        }, parseExtends: function () {
            return this.parseTemplateRef('extends', nodes.Extends);
        }, parseInclude: function () {
            return this.parseTemplateRef('include', nodes.Include);
        }, parseIf: function () {
            var tag = this.peekToken();
            if (!this.skipSymbol('if') && !this.skipSymbol('elif')) {
                this.fail("parseIf: expected if or elif", tag.lineno, tag.colno);
            }
            var node = new nodes.If(tag.lineno, tag.colno);
            node.cond = this.parseExpression();
            this.advanceAfterBlockEnd(tag.value);
            node.body = this.parseUntilBlocks('elif', 'else', 'endif');
            var tok = this.peekToken();
            switch (tok && tok.value) {
                case"elif":
                    node.else_ = this.parseIf();
                    break;
                case"else":
                    this.advanceAfterBlockEnd();
                    node.else_ = this.parseUntilBlocks("endif");
                    this.advanceAfterBlockEnd();
                    break;
                case"endif":
                    node.else_ = null;
                    this.advanceAfterBlockEnd();
                    break;
                default:
                    this.fail('parseIf: expected endif, else, or endif, ' + 'got end of file');
            }
            return node;
        }, parseSet: function () {
            var tag = this.peekToken();
            if (!this.skipSymbol('set')) {
                this.fail('parseSet: expected set', tag.lineno, tag.colno);
            }
            var node = new nodes.Set(tag.lineno, tag.colno, []);
            var target;
            while ((target = this.parsePrimary())) {
                node.targets.push(target);
                if (!this.skip(lexer.TOKEN_COMMA)) {
                    break;
                }
            }
            if (!this.skipValue(lexer.TOKEN_OPERATOR, '=')) {
                this.fail('parseSet: expected = in set tag', tag.lineno, tag.colno);
            }
            node.value = this.parseExpression();
            this.advanceAfterBlockEnd(tag.value);
            return node;
        }, parseStatement: function () {
            var tok = this.peekToken();
            var node;
            if (tok.type != lexer.TOKEN_SYMBOL) {
                this.fail('tag name expected', tok.lineno, tok.colno);
            }
            if (this.breakOnBlocks && this.breakOnBlocks.indexOf(tok.value) != -1) {
                return null;
            }
            switch (tok.value) {
                case'raw':
                    return this.parseRaw();
                case'if':
                    return this.parseIf();
                case'for':
                    return this.parseFor();
                case'block':
                    return this.parseBlock();
                case'extends':
                    return this.parseExtends();
                case'include':
                    return this.parseInclude();
                case'set':
                    return this.parseSet();
                case'macro':
                    return this.parseMacro();
                case'import':
                    return this.parseImport();
                case'from':
                    return this.parseFrom();
                default:
                    if (this.extensions.length) {
                        for (var i = 0; i < this.extensions.length; i++) {
                            var ext = this.extensions[i];
                            if ((ext.tags || []).indexOf(tok.value) > -1) {
                                return ext.parse(this, nodes, lexer);
                            }
                        }
                    }
                    this.fail('unknown block tag: ' + tok.value, tok.lineno, tok.colno);
            }
            return node;
        }, parseRaw: function () {
            this.advanceAfterBlockEnd();
            var str = '';
            var begun = this.peekToken();
            while (1) {
                var tok = this.nextToken(true);
                if (!tok) {
                    this.fail("expected endraw, got end of file");
                }
                if (tok.type == lexer.TOKEN_BLOCK_START) {
                    var ws = null;
                    var name = this.nextToken(true);
                    if (name.type == lexer.TOKEN_WHITESPACE) {
                        ws = name;
                        name = this.nextToken();
                    }
                    if (name.type == lexer.TOKEN_SYMBOL && name.value == 'endraw') {
                        this.advanceAfterBlockEnd(name.value);
                        break;
                    }
                    else {
                        str += tok.value;
                        if (ws) {
                            str += ws.value;
                        }
                        str += name.value;
                    }
                }
                else {
                    str += tok.value;
                }
            }
            var output = new nodes.Output(begun.lineno, begun.colno, [new nodes.TemplateData(begun.lineno, begun.colno, str)]);
            return output;
        }, parsePostfix: function (node) {
            var tok = this.peekToken();
            while (tok) {
                if (tok.type == lexer.TOKEN_LEFT_PAREN) {
                    node = new nodes.FunCall(tok.lineno, tok.colno, node, this.parseSignature());
                }
                else if (tok.type == lexer.TOKEN_LEFT_BRACKET) {
                    var lookup = this.parseAggregate();
                    if (lookup.children.length > 1) {
                        this.fail('invalid index');
                    }
                    node = new nodes.LookupVal(tok.lineno, tok.colno, node, lookup.children[0]);
                }
                else if (tok.type == lexer.TOKEN_OPERATOR && tok.value == '.') {
                    this.nextToken();
                    var val = this.nextToken();
                    if (val.type != lexer.TOKEN_SYMBOL) {
                        this.fail('expected name as lookup value, got ' + val.value, val.lineno, val.colno);
                    }
                    var lookup = new nodes.Literal(val.lineno, val.colno, val.value);
                    node = new nodes.LookupVal(tok.lineno, tok.colno, node, lookup);
                }
                else {
                    break;
                }
                tok = this.peekToken();
            }
            return node;
        }, parseExpression: function () {
            var node = this.parseInlineIf();
            return node;
        }, parseInlineIf: function () {
            var node = this.parseOr();
            if (this.skipSymbol('if')) {
                var cond_node = this.parseOr();
                var body_node = node;
                node = new nodes.InlineIf(node.lineno, node.colno);
                node.body = body_node;
                node.cond = cond_node;
                if (this.skipSymbol('else')) {
                    node.else_ = this.parseOr();
                } else {
                    node.else_ = null;
                }
            }
            return node;
        }, parseOr: function () {
            var node = this.parseAnd();
            while (this.skipSymbol('or')) {
                var node2 = this.parseAnd();
                node = new nodes.Or(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseAnd: function () {
            var node = this.parseNot();
            while (this.skipSymbol('and')) {
                var node2 = this.parseNot();
                node = new nodes.And(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseNot: function () {
            var tok = this.peekToken();
            if (this.skipSymbol('not')) {
                return new nodes.Not(tok.lineno, tok.colno, this.parseNot());
            }
            return this.parseCompare();
        }, parseCompare: function () {
            var compareOps = ['==', '!=', '<', '>', '<=', '>='];
            var expr = this.parseAdd();
            var ops = [];
            while (1) {
                var tok = this.nextToken();
                if (!tok) {
                    break;
                }
                else if (compareOps.indexOf(tok.value) != -1) {
                    ops.push(new nodes.CompareOperand(tok.lineno, tok.colno, this.parseAdd(), tok.value));
                }
                else if (tok.type == lexer.TOKEN_SYMBOL && tok.value == 'in') {
                    ops.push(new nodes.CompareOperand(tok.lineno, tok.colno, this.parseAdd(), 'in'));
                }
                else if (tok.type == lexer.TOKEN_SYMBOL && tok.value == 'not' && this.skipSymbol('in')) {
                    ops.push(new nodes.CompareOperand(tok.lineno, tok.colno, this.parseAdd(), 'notin'));
                }
                else {
                    this.pushToken(tok);
                    break;
                }
            }
            if (ops.length) {
                return new nodes.Compare(ops[0].lineno, ops[0].colno, expr, ops);
            }
            else {
                return expr;
            }
        }, parseAdd: function () {
            var node = this.parseSub();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '+')) {
                var node2 = this.parseSub();
                node = new nodes.Add(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseSub: function () {
            var node = this.parseMul();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '-')) {
                var node2 = this.parseMul();
                node = new nodes.Sub(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseMul: function () {
            var node = this.parseDiv();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '*')) {
                var node2 = this.parseDiv();
                node = new nodes.Mul(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseDiv: function () {
            var node = this.parseFloorDiv();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '/')) {
                var node2 = this.parseFloorDiv();
                node = new nodes.Div(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseFloorDiv: function () {
            var node = this.parseMod();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '//')) {
                var node2 = this.parseMod();
                node = new nodes.FloorDiv(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseMod: function () {
            var node = this.parsePow();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '%')) {
                var node2 = this.parsePow();
                node = new nodes.Mod(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parsePow: function () {
            var node = this.parseUnary();
            while (this.skipValue(lexer.TOKEN_OPERATOR, '**')) {
                var node2 = this.parseUnary();
                node = new nodes.Pow(node.lineno, node.colno, node, node2);
            }
            return node;
        }, parseUnary: function (noFilters) {
            var tok = this.peekToken();
            var node;
            if (this.skipValue(lexer.TOKEN_OPERATOR, '-')) {
                node = new nodes.Neg(tok.lineno, tok.colno, this.parseUnary(true));
            }
            else if (this.skipValue(lexer.TOKEN_OPERATOR, '+')) {
                node = new nodes.Pos(tok.lineno, tok.colno, this.parseUnary(true));
            }
            else {
                node = this.parsePrimary();
            }
            if (!noFilters) {
                node = this.parseFilter(node);
            }
            return node;
        }, parsePrimary: function (noPostfix) {
            var tok = this.nextToken();
            var val = null;
            var node = null;
            if (!tok) {
                this.fail('expected expression, got end of file');
            }
            else if (tok.type == lexer.TOKEN_STRING) {
                val = tok.value;
            }
            else if (tok.type == lexer.TOKEN_INT) {
                val = parseInt(tok.value, 10);
            }
            else if (tok.type == lexer.TOKEN_FLOAT) {
                val = parseFloat(tok.value);
            }
            else if (tok.type == lexer.TOKEN_BOOLEAN) {
                if (tok.value == "true") {
                    val = true;
                }
                else if (tok.value == "false") {
                    val = false;
                }
                else {
                    this.fail("invalid boolean: " + tok.val, tok.lineno, tok.colno);
                }
            }
            if (val !== null) {
                node = new nodes.Literal(tok.lineno, tok.colno, val);
            }
            else if (tok.type == lexer.TOKEN_SYMBOL) {
                node = new nodes.Symbol(tok.lineno, tok.colno, tok.value);
                if (!noPostfix) {
                    node = this.parsePostfix(node);
                }
            }
            else {
                this.pushToken(tok);
                node = this.parseAggregate();
            }
            if (node) {
                return node;
            }
            else {
                this.fail('unexpected token: ' + tok.value, tok.lineno, tok.colno);
            }
        }, parseFilter: function (node) {
            while (this.skip(lexer.TOKEN_PIPE)) {
                var tok = this.expect(lexer.TOKEN_SYMBOL);
                var name = tok.value;
                while (this.skipValue(lexer.TOKEN_OPERATOR, '.')) {
                    name += '.' + this.expect(lexer.TOKEN_SYMBOL).value;
                }
                node = new nodes.Filter(tok.lineno, tok.colno, new nodes.Symbol(tok.lineno, tok.colno, name), new nodes.NodeList(tok.lineno, tok.colno, [node]));
                if (this.peekToken().type == lexer.TOKEN_LEFT_PAREN) {
                    var call = this.parsePostfix(node);
                    node.args.children = node.args.children.concat(call.args.children);
                }
            }
            return node;
        }, parseAggregate: function () {
            var tok = this.nextToken();
            var node;
            switch (tok.type) {
                case lexer.TOKEN_LEFT_PAREN:
                    node = new nodes.Group(tok.lineno, tok.colno);
                    break;
                case lexer.TOKEN_LEFT_BRACKET:
                    node = new nodes.Array(tok.lineno, tok.colno);
                    break;
                case lexer.TOKEN_LEFT_CURLY:
                    node = new nodes.Dict(tok.lineno, tok.colno);
                    break;
                default:
                    return null;
            }
            while (1) {
                var type = this.peekToken().type;
                if (type == lexer.TOKEN_RIGHT_PAREN || type == lexer.TOKEN_RIGHT_BRACKET || type == lexer.TOKEN_RIGHT_CURLY) {
                    this.nextToken();
                    break;
                }
                if (node.children.length > 0) {
                    if (!this.skip(lexer.TOKEN_COMMA)) {
                        this.fail("parseAggregate: expected comma after expression", tok.lineno, tok.colno);
                    }
                }
                if (node instanceof nodes.Dict) {
                    var key = this.parsePrimary();
                    if (!this.skip(lexer.TOKEN_COLON)) {
                        this.fail("parseAggregate: expected colon after dict key", tok.lineno, tok.colno);
                    }
                    var value = this.parseExpression();
                    node.addChild(new nodes.Pair(key.lineno, key.colno, key, value));
                }
                else {
                    var expr = this.parseExpression();
                    node.addChild(expr);
                }
            }
            return node;
        }, parseSignature: function (tolerant, noParens) {
            var tok = this.peekToken();
            if (!noParens && tok.type != lexer.TOKEN_LEFT_PAREN) {
                if (tolerant) {
                    return null;
                }
                else {
                    this.fail('expected arguments', tok.lineno, tok.colno);
                }
            }
            if (tok.type == lexer.TOKEN_LEFT_PAREN) {
                tok = this.nextToken();
            }
            var args = new nodes.NodeList(tok.lineno, tok.colno);
            var kwargs = new nodes.KeywordArgs(tok.lineno, tok.colno);
            var kwnames = [];
            var checkComma = false;
            while (1) {
                tok = this.peekToken();
                if (!noParens && tok.type == lexer.TOKEN_RIGHT_PAREN) {
                    this.nextToken();
                    break;
                }
                else if (noParens && tok.type == lexer.TOKEN_BLOCK_END) {
                    break;
                }
                if (checkComma && !this.skip(lexer.TOKEN_COMMA)) {
                    this.fail("parseSignature: expected comma after expression", tok.lineno, tok.colno);
                }
                else {
                    var arg = this.parsePrimary();
                    if (this.skipValue(lexer.TOKEN_OPERATOR, '=')) {
                        kwargs.addChild(new nodes.Pair(arg.lineno, arg.colno, arg, this.parseExpression()));
                    }
                    else {
                        args.addChild(arg);
                    }
                }
                checkComma = true;
            }
            if (kwargs.children.length) {
                args.addChild(kwargs);
            }
            return args;
        }, parseUntilBlocks: function () {
            var prev = this.breakOnBlocks;
            this.breakOnBlocks = lib.toArray(arguments);
            var ret = this.parse();
            this.breakOnBlocks = prev;
            return ret;
        }, parseNodes: function () {
            var tok;
            var buf = [];
            while ((tok = this.nextToken())) {
                if (tok.type == lexer.TOKEN_DATA) {
                    var data = tok.value;
                    var nextToken = this.peekToken();
                    var nextVal = nextToken && nextToken.value;
                    if (this.dropLeadingWhitespace) {
                        data = data.replace(/^\s*/, '');
                        this.dropLeadingWhitespace = false;
                    }
                    if (nextToken && nextToken.type == lexer.TOKEN_BLOCK_START && nextVal.charAt(nextVal.length - 1) == '-') {
                        data = data.replace(/\s*$/, '');
                    }
                    buf.push(new nodes.Output(tok.lineno, tok.colno, [new nodes.TemplateData(tok.lineno, tok.colno, data)]));
                }
                else if (tok.type == lexer.TOKEN_BLOCK_START) {
                    var n = this.parseStatement();
                    if (!n) {
                        break;
                    }
                    buf.push(n);
                }
                else if (tok.type == lexer.TOKEN_VARIABLE_START) {
                    var e = this.parseExpression();
                    this.advanceAfterVariableEnd();
                    buf.push(new nodes.Output(tok.lineno, tok.colno, [e]));
                }
                else if (tok.type != lexer.TOKEN_COMMENT) {
                    this.fail("Unexpected token at top-level: " +
                        tok.type, tok.lineno, tok.colno);
                }
            }
            return buf;
        }, parse: function () {
            return new nodes.NodeList(0, 0, this.parseNodes());
        }, parseAsRoot: function () {
            return new nodes.Root(0, 0, this.parseNodes());
        }});
        modules['parser'] = {parse: function (src, extensions) {
            var p = new Parser(lexer.lex(src));
            if (extensions !== undefined) {
                p.extensions = extensions;
            }
            return p.parseAsRoot();
        }};
    })();
    (function () {
        var lib = modules["lib"];
        var parser = modules["parser"];
        var nodes = modules["nodes"];
        var Object = modules["object"];
        var Frame = modules["runtime"].Frame;
        var compareOps = {'==': '==', '!=': '!=', '<': '<', '>': '>', '<=': '<=', '>=': '>='};

        function binOpEmitter(str) {
            return function (node, frame) {
                this.compile(node.left, frame);
                this.emit(str);
                this.compile(node.right, frame);
            };
        }

        function quotedArray(arr) {
            return'[' +
                lib.map(arr, function (x) {
                    return'"' + x + '"';
                }) + ']';
        }

        var Compiler = Object.extend({init: function (extensions) {
            this.codebuf = [];
            this.lastId = 0;
            this.buffer = null;
            this.bufferStack = [];
            this.isChild = false;
            this.extensions = extensions || [];
        }, fail: function (msg, lineno, colno) {
            if (lineno !== undefined)lineno += 1;
            if (colno !== undefined)colno += 1;
            throw new lib.TemplateError(msg, lineno, colno);
        }, pushBufferId: function (id) {
            this.bufferStack.push(this.buffer);
            this.buffer = id;
            this.emit('var ' + this.buffer + ' = "";');
        }, popBufferId: function () {
            this.buffer = this.bufferStack.pop();
        }, emit: function (code) {
            this.codebuf.push(code);
        }, emitLine: function (code) {
            this.emit(code + "\n");
        }, emitLines: function () {
            lib.each(lib.toArray(arguments), function (line) {
                this.emitLine(line);
            }, this);
        }, emitFuncBegin: function (name) {
            this.buffer = 'output';
            this.emitLine('function ' + name + '(env, context, frame, runtime) {');
            this.emitLine('var lineno = null;');
            this.emitLine('var colno = null;');
            this.emitLine('var ' + this.buffer + ' = "";');
            this.emitLine('try {');
        }, emitFuncEnd: function (noReturn) {
            if (!noReturn) {
                this.emitLine('return ' + this.buffer + ';');
            }
            this.emitLine('} catch (e) {');
            this.emitLine('  runtime.handleError(e, lineno, colno);');
            this.emitLine('}');
            this.emitLine('}');
            this.buffer = null;
        }, tmpid: function () {
            this.lastId++;
            return't_' + this.lastId;
        }, _bufferAppend: function (func) {
            this.emit(this.buffer + ' += runtime.suppressValue(');
            func.call(this);
            this.emit(', env.autoesc);\n');
        }, _compileChildren: function (node, frame) {
            var children = node.children;
            for (var i = 0, l = children.length; i < l; i++) {
                this.compile(children[i], frame);
            }
        }, _compileAggregate: function (node, frame, startChar, endChar) {
            this.emit(startChar);
            for (var i = 0; i < node.children.length; i++) {
                if (i > 0) {
                    this.emit(',');
                }
                this.compile(node.children[i], frame);
            }
            this.emit(endChar);
        }, _compileExpression: function (node, frame) {
            this.assertType(node, nodes.Literal, nodes.Symbol, nodes.Group, nodes.Array, nodes.Dict, nodes.FunCall, nodes.Filter, nodes.LookupVal, nodes.Compare, nodes.InlineIf, nodes.And, nodes.Or, nodes.Not, nodes.Add, nodes.Sub, nodes.Mul, nodes.Div, nodes.FloorDiv, nodes.Mod, nodes.Pow, nodes.Neg, nodes.Pos, nodes.Compare);
            this.compile(node, frame);
        }, assertType: function (node) {
            var types = lib.toArray(arguments).slice(1);
            var success = false;
            for (var i = 0; i < types.length; i++) {
                if (node instanceof types[i]) {
                    success = true;
                }
            }
            if (!success) {
                this.fail("assertType: invalid type: " + node.typename, node.lineno, node.colno);
            }
        }, compileCallExtension: function (node, frame) {
            var name = node.extName;
            var args = node.args;
            var contentArgs = node.contentArgs;
            var transformedArgs = [];
            this.emit(this.buffer + ' += runtime.suppressValue(');
            this.emit('env.getExtension("' + node.extName + '")["' + node.prop + '"](');
            this.emit('context');
            if (args || contentArgs) {
                this.emit(',');
            }
            if (args) {
                if (!(args instanceof nodes.NodeList)) {
                    this.fail('compileCallExtension: arguments must be a NodeList, ' + 'use `parser.parseSignature`');
                }
                lib.each(args.children, function (arg, i) {
                    this._compileExpression(arg, frame);
                    if (i != args.children.length || contentArgs) {
                        this.emit(',');
                    }
                }, this);
            }
            if (contentArgs) {
                lib.each(contentArgs, function (arg, i) {
                    if (i > 0) {
                        this.emit(',');
                    }
                    if (arg) {
                        var id = this.tmpid();
                        this.emit('function() {');
                        this.pushBufferId(id);
                        this.compile(arg, frame);
                        this.popBufferId();
                        this.emitLine('return ' + id + ';\n' + '}');
                    }
                    else {
                        this.emit('null');
                    }
                }, this);
            }
            this.emit(')');
            this.emit(', env.autoesc);\n');
        }, compileNodeList: function (node, frame) {
            this._compileChildren(node, frame);
        }, compileLiteral: function (node, frame) {
            if (typeof node.value == "string") {
                var val = node.value.replace(/\\/g, '\\\\');
                val = val.replace(/"/g, '\\"');
                val = val.replace(/\n/g, "\\n");
                val = val.replace(/\r/g, "\\r");
                val = val.replace(/\t/g, "\\t");
                this.emit('"' + val + '"');
            }
            else {
                this.emit(node.value.toString());
            }
        }, compileSymbol: function (node, frame) {
            var name = node.value;
            var v;
            if ((v = frame.lookup(name))) {
                this.emit(v);
            }
            else {
                this.emit('runtime.contextOrFrameLookup(' + 'context, frame, "' + name + '")');
            }
        }, compileGroup: function (node, frame) {
            this._compileAggregate(node, frame, '(', ')');
        }, compileArray: function (node, frame) {
            this._compileAggregate(node, frame, '[', ']');
        }, compileDict: function (node, frame) {
            this._compileAggregate(node, frame, '{', '}');
        }, compilePair: function (node, frame) {
            var key = node.key;
            var val = node.value;
            if (key instanceof nodes.Symbol) {
                key = new nodes.Literal(key.lineno, key.colno, key.value);
            }
            else if (!(key instanceof nodes.Literal && typeof key.value == "string")) {
                this.fail("compilePair: Dict keys must be strings or names", key.lineno, key.colno);
            }
            this.compile(key, frame);
            this.emit(': ');
            this._compileExpression(val, frame);
        }, compileInlineIf: function (node, frame) {
            this.emit('(');
            this.compile(node.cond, frame);
            this.emit('?');
            this.compile(node.body, frame);
            this.emit(':');
            if (node.else_ !== null)
                this.compile(node.else_, frame); else
                this.emit('""');
            this.emit(')');
        }, compileOr: binOpEmitter(' || '), compileAnd: binOpEmitter(' && '), compileAdd: binOpEmitter(' + '), compileSub: binOpEmitter(' - '), compileMul: binOpEmitter(' * '), compileDiv: binOpEmitter(' / '), compileMod: binOpEmitter(' % '), compileNot: function (node, frame) {
            this.emit('!');
            this.compile(node.target, frame);
        }, compileFloorDiv: function (node, frame) {
            this.emit('Math.floor(');
            this.compile(node.left, frame);
            this.emit(' / ');
            this.compile(node.right, frame);
            this.emit(')');
        }, compilePow: function (node, frame) {
            this.emit('Math.pow(');
            this.compile(node.left, frame);
            this.emit(', ');
            this.compile(node.right, frame);
            this.emit(')');
        }, compileNeg: function (node, frame) {
            this.emit('-');
            this.compile(node.target, frame);
        }, compilePos: function (node, frame) {
            this.emit('+');
            this.compile(node.target, frame);
        }, compileCompare: function (node, frame) {
            this.compile(node.expr, frame);
            for (var i = 0; i < node.ops.length; i++) {
                var n = node.ops[i];
                this.emit(' ' + compareOps[n.type] + ' ');
                this.compile(n.expr, frame);
            }
        }, compileLookupVal: function (node, frame) {
            this.emit('runtime.memberLookup((');
            this._compileExpression(node.target, frame);
            this.emit('),');
            this._compileExpression(node.val, frame);
            this.emit(', env.autoesc)');
        }, _getNodeName: function (node) {
            switch (node.typename) {
                case'Symbol':
                    return node.value;
                case'FunCall':
                    return'the return value of (' + this._getNodeName(node.name) + ')';
                case'LookupVal':
                    return this._getNodeName(node.target) + '["' +
                        this._getNodeName(node.val) + '"]';
                case'Literal':
                    return node.value.toString().substr(0, 10);
                default:
                    return'--expression--';
            }
        }, compileFunCall: function (node, frame) {
            this.emit('(lineno = ' + node.lineno + ', colno = ' + node.colno + ', ');
            this.emit('runtime.callWrap(');
            this._compileExpression(node.name, frame);
            this.emit(', "' + this._getNodeName(node.name).replace(/"/g, '\\"') + '", ');
            this._compileAggregate(node.args, frame, '[', '])');
            this.emit(')');
        }, compileFilter: function (node, frame) {
            var name = node.name;
            this.assertType(name, nodes.Symbol);
            this.emit('env.getFilter("' + name.value + '")');
            this._compileAggregate(node.args, frame, '(', ')');
        }, compileKeywordArgs: function (node, frame) {
            var names = [];
            lib.each(node.children, function (pair) {
                names.push(pair.key.value);
            });
            this.emit('runtime.makeKeywordArgs(');
            this.compileDict(node, frame);
            this.emit(')');
        }, compileSet: function (node, frame) {
            var ids = [];
            lib.each(node.targets, function (target) {
                var name = target.value;
                var id = frame.get(name);
                if (id === null) {
                    id = this.tmpid();
                    frame.set(name, id);
                    this.emitLine('var ' + id + ';');
                }
                ids.push(id);
            }, this);
            this.emit(ids.join(' = ') + ' = ');
            this._compileExpression(node.value, frame);
            this.emitLine(';');
            lib.each(node.targets, function (target, i) {
                var id = ids[i];
                var name = target.value;
                this.emitLine('frame.set("' + name + '", ' + id + ');');
                this.emitLine('if(!frame.parent) {');
                this.emitLine('context.setVariable("' + name + '", ' + id + ');');
                if (name.charAt(0) != '_') {
                    this.emitLine('context.addExport("' + name + '");');
                }
                this.emitLine('}');
            }, this);
        }, compileIf: function (node, frame) {
            this.emit('if(');
            this._compileExpression(node.cond, frame);
            this.emitLine(') {');
            this.compile(node.body, frame);
            if (node.else_) {
                this.emitLine('}\nelse {');
                this.compile(node.else_, frame);
            }
            this.emitLine('}');
        }, compileFor: function (node, frame) {
            var i = this.tmpid();
            var arr = this.tmpid();
            frame = frame.push();
            this.emitLine('frame = frame.push();');
            this.emit('var ' + arr + ' = ');
            this._compileExpression(node.arr, frame);
            this.emitLine(';');
            var loopUses = {};
            node.iterFields(function (field) {
                var lookups = field.findAll(nodes.LookupVal);
                lib.each(lookups, function (lookup) {
                    if (lookup.target instanceof nodes.Symbol && lookup.target.value == 'loop' && lookup.val instanceof nodes.Literal) {
                        loopUses[lookup.val.value] = true;
                    }
                });
            });
            this.emit('if(' + arr + ' !== undefined) {');
            if (node.name instanceof nodes.Array) {
                this.emitLine('var ' + i + ';');
                this.emitLine('if (runtime.isArray(' + arr + ')) {');
                this.emitLine('for (' + i + '=0; ' + i + ' < ' + arr + '.length; '
                    + i + '++) {');
                for (var u = 0; u < node.name.children.length; u++) {
                    var tid = this.tmpid();
                    this.emitLine('var ' + tid + ' = ' + arr + '[' + i + '][' + u + ']');
                    this.emitLine('frame.set("' + node.name.children[u].value
                        + '", ' + arr + '[' + i + '][' + u + ']' + ');');
                    frame.set(node.name.children[u].value, tid);
                }
                if ('index'in loopUses) {
                    this.emitLine('frame.set("loop.index", ' + i + ' + 1);');
                }
                if ('index0'in loopUses) {
                    this.emitLine('frame.set("loop.index0", ' + i + ');');
                }
                if ('first'in loopUses) {
                    this.emitLine('frame.set("loop.first", ' + i + ' === 0);');
                }
                this.compile(node.body, frame);
                this.emitLine('}');
                this.emitLine('} else {');
                this.emitLine(i + ' = -1;');
                var key = node.name.children[0];
                var val = node.name.children[1];
                var k = this.tmpid();
                var v = this.tmpid();
                frame.set(key.value, k);
                frame.set(val.value, v);
                this.emitLine('for(var ' + k + ' in ' + arr + ') {');
                this.emitLine(i + '++;');
                this.emitLine('var ' + v + ' = ' + arr + '[' + k + '];');
                this.emitLine('frame.set("' + key.value + '", ' + k + ');');
                this.emitLine('frame.set("' + val.value + '", ' + v + ');');
                if ('index'in loopUses) {
                    this.emitLine('frame.set("loop.index", ' + i + ' + 1);');
                }
                if ('index0'in loopUses) {
                    this.emitLine('frame.set("loop.index0", ' + i + ');');
                }
                if ('first'in loopUses) {
                    this.emitLine('frame.set("loop.first", ' + i + ' === 0);');
                }
                this.compile(node.body, frame);
                this.emitLine('}');
                this.emitLine('}');
            }
            else {
                var v = this.tmpid();
                frame.set(node.name.value, v);
                this.emitLine('for(var ' + i + '=0; ' + i + ' < ' + arr + '.length; ' +
                    i + '++) {');
                this.emitLine('var ' + v + ' = ' + arr + '[' + i + '];');
                this.emitLine('frame.set("' + node.name.value + '", ' + v + ');');
                if ('index'in loopUses) {
                    this.emitLine('frame.set("loop.index", ' + i + ' + 1);');
                }
                if ('index0'in loopUses) {
                    this.emitLine('frame.set("loop.index0", ' + i + ');');
                }
                if ('revindex'in loopUses) {
                    this.emitLine('frame.set("loop.revindex", ' + arr + '.length - ' + i + ');');
                }
                if ('revindex0'in loopUses) {
                    this.emitLine('frame.set("loop.revindex0", ' + arr + '.length - ' + i + ' - 1);');
                }
                if ('first'in loopUses) {
                    this.emitLine('frame.set("loop.first", ' + i + ' === 0);');
                }
                if ('last'in loopUses) {
                    this.emitLine('frame.set("loop.last", ' + i + ' === ' + arr + '.length - 1);');
                }
                if ('length'in loopUses) {
                    this.emitLine('frame.set("loop.length", ' + arr + '.length);');
                }
                this.compile(node.body, frame);
                this.emitLine('}');
            }
            this.emit('}');
            this.emitLine('frame = frame.pop();');
        }, _emitMacroBegin: function (node, frame) {
            var args = [];
            var kwargs = null;
            var funcId = 'macro_' + this.tmpid();
            lib.each(node.args.children, function (arg, i) {
                if (i === node.args.children.length - 1 && arg instanceof nodes.Dict) {
                    kwargs = arg;
                }
                else {
                    this.assertType(arg, nodes.Symbol);
                    args.push(arg);
                }
            }, this);
            var realNames = lib.map(args, function (n) {
                return'l_' + n.value;
            });
            realNames.push('kwargs');
            var argNames = lib.map(args, function (n) {
                return'"' + n.value + '"';
            });
            var kwargNames = lib.map((kwargs && kwargs.children) || [], function (n) {
                return'"' + n.key.value + '"';
            });
            this.emitLines('var ' + funcId + ' = runtime.makeMacro(', '[' + argNames.join(', ') + '], ', '[' + kwargNames.join(', ') + '], ', 'function (' + realNames.join(', ') + ') {', 'frame = frame.push();', 'kwargs = kwargs || {};');
            lib.each(args, function (arg) {
                this.emitLine('frame.set("' + arg.value + '", ' + 'l_' + arg.value + ');');
                frame.set(arg.value, 'l_' + arg.value);
            }, this);
            if (kwargs) {
                lib.each(kwargs.children, function (pair) {
                    var name = pair.key.value;
                    this.emit('frame.set("' + name + '", ' + 'kwargs.hasOwnProperty("' + name + '") ? ' + 'kwargs["' + name + '"] : ');
                    this._compileExpression(pair.value, frame);
                    this.emitLine(');');
                }, this);
            }
            return funcId;
        }, _emitMacroEnd: function () {
            this.emitLine('frame = frame.pop();');
            this.emitLine('return new runtime.SafeString(' + this.buffer + ');');
            this.emitLine('});');
        }, compileMacro: function (node, frame) {
            frame = frame.push();
            var funcId = this._emitMacroBegin(node, frame);
            var prevBuffer = this.buffer;
            this.buffer = 'output';
            this.emitLine('var ' + this.buffer + '= "";');
            this.compile(node.body, frame);
            this._emitMacroEnd();
            this.buffer = prevBuffer;
            var name = node.name.value;
            frame = frame.pop();
            frame.set(name, funcId);
            if (frame.parent) {
                this.emitLine('frame.set("' + name + '", ' + funcId + ');');
            }
            else {
                if (node.name.value.charAt(0) != '_') {
                    this.emitLine('context.addExport("' + name + '");');
                }
                this.emitLine('context.setVariable("' + name + '", ' + funcId + ');');
            }
        }, compileImport: function (node, frame) {
            var id = this.tmpid();
            var target = node.target.value;
            this.emit('var ' + id + ' = env.getTemplate(');
            this._compileExpression(node.template, frame);
            this.emitLine(').getExported();');
            frame.set(target, id);
            if (frame.parent) {
                this.emitLine('frame.set("' + target + '", ' + id + ');');
            }
            else {
                this.emitLine('context.setVariable("' + target + '", ' + id + ');');
            }
        }, compileFromImport: function (node, frame) {
            this.emit('var imported = env.getTemplate(');
            this.compile(node.template, frame);
            this.emitLine(').getExported();');
            lib.each(node.names.children, function (nameNode) {
                var name;
                var alias;
                var id = this.tmpid();
                if (nameNode instanceof nodes.Pair) {
                    name = nameNode.key.value;
                    alias = nameNode.value.value;
                }
                else {
                    name = nameNode.value;
                    alias = name;
                }
                this.emitLine('if(imported.hasOwnProperty("' + name + '")) {');
                this.emitLine('var ' + id + ' = imported.' + name + ';');
                this.emitLine('} else {');
                this.emitLine('throw new Error("cannot import \'' + name + '\'")');
                this.emitLine('}');
                frame.set(alias, id);
                if (frame.parent) {
                    this.emitLine('frame.set("' + alias + '", ' + id + ');');
                }
                else {
                    this.emitLine('context.setVariable("' + alias + '", ' + id + ');');
                }
            }, this);
        }, compileBlock: function (node, frame) {
            if (!this.isChild) {
                this.emitLine(this.buffer + ' += context.getBlock("' +
                    node.name.value + '")(env, context, frame, runtime);');
            }
        }, compileExtends: function (node, frame) {
            if (this.isChild) {
                this.fail('compileExtends: cannot extend multiple times', node.template.lineno, node.template.colno);
            }
            this.emit('var parentTemplate = env.getTemplate(');
            this._compileExpression(node.template, frame);
            this.emitLine(', true);');
            var k = this.tmpid();
            this.emitLine('for(var ' + k + ' in parentTemplate.blocks) {');
            this.emitLine('context.addBlock(' + k + ', parentTemplate.blocks[' + k + ']);');
            this.emitLine('}');
            this.isChild = true;
        }, compileInclude: function (node, frame) {
            this.emit('var includeTemplate = env.getTemplate(');
            this._compileExpression(node.template, frame);
            this.emitLine(');');
            this.emitLine(this.buffer + ' += includeTemplate.render(' + 'context.getVariables(), frame.push());');
        }, compileTemplateData: function (node, frame) {
            this.compileLiteral(node, frame);
        }, compileOutput: function (node, frame) {
            var children = node.children;
            for (var i = 0, l = children.length; i < l; i++) {
                if (children[i]instanceof nodes.TemplateData) {
                    if (children[i].value) {
                        this.emit(this.buffer + ' += ');
                        this.compileLiteral(children[i], frame);
                        this.emitLine(';');
                    }
                }
                else {
                    this.emit(this.buffer + ' += runtime.suppressValue(');
                    this.compile(children[i], frame);
                    this.emit(', env.autoesc);\n');
                }
            }
        }, compileRoot: function (node, frame) {
            if (frame) {
                this.fail("compileRoot: root node can't have frame");
            }
            frame = new Frame();
            this.emitFuncBegin('root');
            this._compileChildren(node, frame);
            if (this.isChild) {
                this.emitLine('return ' + 'parentTemplate.rootRenderFunc(env, context, frame, runtime);');
            }
            this.emitFuncEnd(this.isChild);
            this.isChild = false;
            var blocks = node.findAll(nodes.Block);
            for (var i = 0; i < blocks.length; i++) {
                var block = blocks[i];
                var name = block.name.value;
                this.emitFuncBegin('b_' + name);
                this.emitLine('var l_super = context.getSuper(env, ' + '"' + name + '", ' + 'b_' + name + ', ' + 'frame, ' + 'runtime);');
                var tmpFrame = new Frame();
                tmpFrame.set('super', 'l_super');
                this.compile(block.body, tmpFrame);
                this.emitFuncEnd();
            }
            this.emitLine('return {');
            for (var i = 0; i < blocks.length; i++) {
                var block = blocks[i];
                var name = 'b_' + block.name.value;
                this.emitLine(name + ': ' + name + ',');
            }
            this.emitLine('root: root\n};');
        }, compile: function (node, frame) {
            var _compile = this["compile" + node.typename];
            if (_compile) {
                _compile.call(this, node, frame);
            }
            else {
                this.fail("compile: Cannot compile node: " + node.typename, node.lineno, node.colno);
            }
        }, getCode: function () {
            return this.codebuf.join('');
        }});
        modules['compiler'] = {compile: function (src, extensions, name) {
            var c = new Compiler(extensions);
            if (extensions && extensions.length) {
                for (var i = 0; i < extensions.length; i++) {
                    if ('preprocess'in extensions[i]) {
                        src = extensions[i].preprocess(src, name);
                    }
                }
            }
            c.compile(parser.parse(src, extensions));
            return c.getCode();
        }, Compiler: Compiler};
    })();
    (function () {
        var lib = modules["lib"];
        var r = modules["runtime"];
        var filters = {abs: function (n) {
            return Math.abs(n);
        }, batch: function (arr, linecount, fill_with) {
            var res = [];
            var tmp = [];
            for (var i = 0; i < arr.length; i++) {
                if (i % linecount === 0 && tmp.length) {
                    res.push(tmp);
                    tmp = [];
                }
                tmp.push(arr[i]);
            }
            if (tmp.length) {
                if (fill_with) {
                    for (var i = tmp.length; i < linecount; i++) {
                        tmp.push(fill_with);
                    }
                }
                res.push(tmp);
            }
            return res;
        }, capitalize: function (str) {
            var ret = str.toLowerCase();
            return r.copySafeness(str, ret[0].toUpperCase() + ret.slice(1));
        }, center: function (str, width) {
            width = width || 80;
            if (str.length >= width) {
                return str;
            }
            var spaces = width - str.length;
            var pre = lib.repeat(" ", spaces / 2 - spaces % 2);
            var post = lib.repeat(" ", spaces / 2);
            return r.copySafeness(str, pre + str + post);
        }, 'default': function (val, def) {
            return val ? val : def;
        }, dictsort: function (val, case_sensitive, by) {
            if (!lib.isObject(val)) {
                throw new lib.TemplateError("dictsort filter: val must be an object");
            }
            var array = [];
            for (var k in val) {
                array.push([k, val[k]]);
            }
            var si;
            if (by === undefined || by === "key") {
                si = 0;
            } else if (by === "value") {
                si = 1;
            } else {
                throw new lib.TemplateError("dictsort filter: You can only sort by either key or value");
            }
            array.sort(function (t1, t2) {
                var a = t1[si];
                var b = t2[si];
                if (!case_sensitive) {
                    if (lib.isString(a)) {
                        a = a.toUpperCase();
                    }
                    if (lib.isString(b)) {
                        b = b.toUpperCase();
                    }
                }
                return a > b ? 1 : (a == b ? 0 : -1);
            });
            return array;
        }, escape: function (str) {
            if (typeof str == 'string' || str instanceof r.SafeString) {
                return lib.escape(str);
            }
            return str;
        }, safe: function (str) {
            return new r.SafeString(str);
        }, first: function (arr) {
            return arr[0];
        }, groupby: function (arr, attr) {
            return lib.groupBy(arr, attr);
        }, indent: function (str, width, indentfirst) {
            width = width || 4;
            var res = '';
            var lines = str.split('\n');
            var sp = lib.repeat(' ', width);
            for (var i = 0; i < lines.length; i++) {
                if (i == 0 && !indentfirst) {
                    res += lines[i] + '\n';
                }
                else {
                    res += sp + lines[i] + '\n';
                }
            }
            return r.copySafeness(str, res);
        }, join: function (arr, del, attr) {
            del = del || '';
            if (attr) {
                arr = lib.map(arr, function (v) {
                    return v[attr];
                });
            }
            return arr.join(del);
        }, last: function (arr) {
            return arr[arr.length - 1];
        }, length: function (arr) {
            return arr.length;
        }, list: function (val) {
            if (lib.isString(val)) {
                return val.split('');
            }
            else if (lib.isObject(val)) {
                var keys = [];
                if (Object.keys) {
                    keys = Object.keys(val);
                }
                else {
                    for (var k in val) {
                        keys.push(k);
                    }
                }
                return lib.map(keys, function (k) {
                    return{key: k, value: val[k]};
                });
            }
            else {
                throw new lib.TemplateError("list filter: type not iterable");
            }
        }, lower: function (str) {
            return str.toLowerCase();
        }, random: function (arr) {
            var i = Math.floor(Math.random() * arr.length);
            if (i == arr.length) {
                i--;
            }
            return arr[i];
        }, replace: function (str, old, new_, maxCount) {
            var res = str;
            var last = res;
            var count = 1;
            res = res.replace(old, new_);
            while (last != res) {
                if (count >= maxCount) {
                    break;
                }
                last = res;
                res = res.replace(old, new_);
                count++;
            }
            return r.copySafeness(str, res);
        }, reverse: function (val) {
            var arr;
            if (lib.isString(val)) {
                arr = filters.list(val);
            }
            else {
                arr = lib.map(val, function (v) {
                    return v;
                });
            }
            arr.reverse();
            if (lib.isString(val)) {
                return r.copySafeness(val, arr.join(''));
            }
            return arr;
        }, round: function (val, precision, method) {
            precision = precision || 0;
            var factor = Math.pow(10, precision);
            var rounder;
            if (method == 'ceil') {
                rounder = Math.ceil;
            }
            else if (method == 'floor') {
                rounder = Math.floor;
            }
            else {
                rounder = Math.round;
            }
            return rounder(val * factor) / factor;
        }, slice: function (arr, slices, fillWith) {
            var sliceLength = Math.floor(arr.length / slices);
            var extra = arr.length % slices;
            var offset = 0;
            var res = [];
            for (var i = 0; i < slices; i++) {
                var start = offset + i * sliceLength;
                if (i < extra) {
                    offset++;
                }
                var end = offset + (i + 1) * sliceLength;
                var slice = arr.slice(start, end);
                if (fillWith && i >= extra) {
                    slice.push(fillWith);
                }
                res.push(slice);
            }
            return res;
        }, sort: function (arr, reverse, caseSens, attr) {
            arr = lib.map(arr, function (v) {
                return v;
            });
            arr.sort(function (a, b) {
                var x, y;
                if (attr) {
                    x = a[attr];
                    y = b[attr];
                }
                else {
                    x = a;
                    y = b;
                }
                if (!caseSens && lib.isString(x) && lib.isString(y)) {
                    x = x.toLowerCase();
                    y = y.toLowerCase();
                }
                if (x < y) {
                    return reverse ? 1 : -1;
                }
                else if (x > y) {
                    return reverse ? -1 : 1;
                }
                else {
                    return 0;
                }
            });
            return arr;
        }, string: function (obj) {
            return r.copySafeness(obj, obj);
        }, title: function (str) {
            var words = str.split(' ');
            for (var i = 0; i < words.length; i++) {
                words[i] = filters.capitalize(words[i]);
            }
            return r.copySafeness(str, words.join(' '));
        }, trim: function (str) {
            return r.copySafeness(str, str.replace(/^\s*|\s*$/g, ''));
        }, truncate: function (input, length, killwords, end) {
            var orig = input;
            length = length || 255;
            if (input.length <= length)
                return input;
            if (killwords) {
                input = input.substring(0, length);
            } else {
                var idx = input.lastIndexOf(' ', length);
                if (idx === -1) {
                    idx = length;
                }
                input = input.substring(0, idx);
            }
            input += (end !== undefined && end !== null) ? end : '...';
            return r.copySafeness(orig, input);
        }, upper: function (str) {
            return str.toUpperCase();
        }, wordcount: function (str) {
            return str.match(/\w+/g).length;
        }, 'float': function (val, def) {
            var res = parseFloat(val);
            return isNaN(res) ? def : res;
        }, 'int': function (val, def) {
            var res = parseInt(val, 10);
            return isNaN(res) ? def : res;
        }};
        filters.d = filters['default'];
        filters.e = filters.escape;
        modules['filters'] = filters;
    })();
    (function () {
        function cycler(items) {
            var index = -1;
            var current = null;
            return{reset: function () {
                index = -1;
                current = null;
            }, next: function () {
                index++;
                if (index >= items.length) {
                    index = 0;
                }
                current = items[index];
                return current;
            }};
        }

        function joiner(sep) {
            sep = sep || ',';
            var first = true;
            return function () {
                var val = first ? '' : sep;
                first = false;
                return val;
            };
        }

        var globals = {range: function (start, stop, step) {
            if (!stop) {
                stop = start;
                start = 0;
                step = 1;
            }
            else if (!step) {
                step = 1;
            }
            var arr = [];
            for (var i = start; i < stop; i += step) {
                arr.push(i);
            }
            return arr;
        }, cycler: function () {
            return cycler(Array.prototype.slice.call(arguments));
        }, joiner: function (sep) {
            return joiner(sep);
        }}
        modules['globals'] = globals;
    })();
    (function () {
        var Object = modules["object"];
        var HttpLoader = Object.extend({init: function (baseURL, neverUpdate) {
            console.log("[nunjucks] Warning: only use HttpLoader in " + "development. Otherwise precompile your templates.");
            this.baseURL = baseURL || '';
            this.neverUpdate = neverUpdate;
        }, getSource: function (name) {
            var src = this.fetch(this.baseURL + '/' + name);
            var _this = this;
            if (!src) {
                return null;
            }
            return{src: src, path: name, upToDate: function () {
                return _this.neverUpdate;
            }};
        }, fetch: function (url) {
            var ajax = new XMLHttpRequest();
            var src = null;
            ajax.onreadystatechange = function () {
                if (ajax.readyState == 4 && ajax.status == 200) {
                    src = ajax.responseText;
                }
            };
            url += (url.indexOf('?') === -1 ? '?' : '&') + 's=' + Date.now();
            ajax.open('GET', url, false);
            ajax.send();
            return src;
        }});
        modules['web-loaders'] = {HttpLoader: HttpLoader};
    })();
    (function () {
        if (typeof window === 'undefined') {
            modules['loaders'] = modules["node-loaders"];
        }
        else {
            modules['loaders'] = modules["web-loaders"];
        }
    })();
    (function () {
        var lib = modules["lib"];
        var Object = modules["object"];
        var lexer = modules["lexer"];
        var compiler = modules["compiler"];
        var builtin_filters = modules["filters"];
        var builtin_loaders = modules["loaders"];
        var runtime = modules["runtime"];
        var globals = modules["globals"];
        var Frame = runtime.Frame;
        var Environment = Object.extend({init: function (loaders, opts) {
            opts = opts || {};
            this.dev = !!opts.dev;
            this.autoesc = !!opts.autoescape;
            if (!loaders) {
                if (builtin_loaders.FileSystemLoader) {
                    this.loaders = [new builtin_loaders.FileSystemLoader()];
                }
                else {
                    this.loaders = [new builtin_loaders.HttpLoader('/views')];
                }
            }
            else {
                this.loaders = lib.isArray(loaders) ? loaders : [loaders];
            }
            if (opts.tags) {
                lexer.setTags(opts.tags);
            }
            this.filters = builtin_filters;
            this.cache = {};
            this.extensions = {};
            this.extensionsList = [];
        }, addExtension: function (name, extension) {
            extension._name = name;
            this.extensions[name] = extension;
            this.extensionsList.push(extension);
        }, getExtension: function (name) {
            return this.extensions[name];
        }, addFilter: function (name, func) {
            this.filters[name] = func;
        }, getFilter: function (name) {
            if (!this.filters[name]) {
                throw new Error('filter not found: ' + name);
            }
            return this.filters[name];
        }, getTemplate: function (name, eagerCompile) {
            if (name && name.raw) {
                name = name.raw;
            }
            var info = null;
            var tmpl = this.cache[name];
            var upToDate;
            if (typeof name !== 'string') {
                throw new Error('template names must be a string: ' + name);
            }
            if (!tmpl || !tmpl.isUpToDate()) {
                for (var i = 0; i < this.loaders.length; i++) {
                    if ((info = this.loaders[i].getSource(name))) {
                        break;
                    }
                }
                if (!info) {
                    throw new Error('template not found: ' + name);
                }
                this.cache[name] = new Template(info.src, this, info.path, info.upToDate, eagerCompile);
            }
            return this.cache[name];
        }, registerPrecompiled: function (templates) {
            for (var name in templates) {
                this.cache[name] = new Template({type: 'code', obj: templates[name]}, this, name, function () {
                    return true;
                }, true);
            }
        }, express: function (app) {
            var env = this;
            if (app.render) {
                app.render = function (name, ctx, k) {
                    var context = {};
                    if (lib.isFunction(ctx)) {
                        k = ctx;
                        ctx = {};
                    }
                    context = lib.extend(context, this.locals);
                    if (ctx._locals) {
                        context = lib.extend(context, ctx._locals);
                    }
                    context = lib.extend(context, ctx);
                    var res = env.render(name, context);
                    k(null, res);
                };
            }
            else {
                var http = modules["http"];
                var res = http.ServerResponse.prototype;
                res._render = function (name, ctx, k) {
                    var app = this.app;
                    var context = {};
                    if (this._locals) {
                        context = lib.extend(context, this._locals);
                    }
                    if (ctx) {
                        context = lib.extend(context, ctx);
                        if (ctx.locals) {
                            context = lib.extend(context, ctx.locals);
                        }
                    }
                    context = lib.extend(context, app._locals);
                    var str = env.render(name, context);
                    if (k) {
                        k(null, str);
                    }
                    else {
                        this.send(str);
                    }
                };
            }
        }, render: function (name, ctx) {
            return this.getTemplate(name).render(ctx);
        }});
        var Context = Object.extend({init: function (ctx, blocks) {
            this.ctx = ctx;
            this.blocks = {};
            this.exported = [];
            for (var name in blocks) {
                this.addBlock(name, blocks[name]);
            }
        }, lookup: function (name) {
            if (name in globals && !(name in this.ctx)) {
                return globals[name];
            }
            else {
                return this.ctx[name];
            }
        }, setVariable: function (name, val) {
            this.ctx[name] = val;
        }, getVariables: function () {
            return this.ctx;
        }, addBlock: function (name, block) {
            this.blocks[name] = this.blocks[name] || [];
            this.blocks[name].push(block);
        }, getBlock: function (name) {
            if (!this.blocks[name]) {
                throw new Error('unknown block "' + name + '"');
            }
            return this.blocks[name][0];
        }, getSuper: function (env, name, block, frame, runtime) {
            var idx = (this.blocks[name] || []).indexOf(block);
            var blk = this.blocks[name][idx + 1];
            var context = this;
            return function () {
                if (idx == -1 || !blk) {
                    throw new Error('no super block available for "' + name + '"');
                }
                return blk(env, context, frame, runtime);
            };
        }, addExport: function (name) {
            this.exported.push(name);
        }, getExported: function () {
            var exported = {};
            for (var i = 0; i < this.exported.length; i++) {
                var name = this.exported[i];
                exported[name] = this.ctx[name];
            }
            return exported;
        }});
        var Template = Object.extend({init: function (src, env, path, upToDate, eagerCompile) {
            this.env = env || new Environment();
            if (lib.isObject(src)) {
                switch (src.type) {
                    case'code':
                        this.tmplProps = src.obj;
                        break;
                    case'string':
                        this.tmplStr = src.obj;
                        break;
                }
            }
            else if (lib.isString(src)) {
                this.tmplStr = src;
            }
            else {
                throw new Error("src must be a string or an object describing " + "the source");
            }
            this.path = path;
            this.upToDate = upToDate || function () {
                return false;
            };
            if (eagerCompile) {
                var _this = this;
                lib.withPrettyErrors(this.path, this.env.dev, function () {
                    _this._compile();
                });
            }
            else {
                this.compiled = false;
            }
        }, render: function (ctx, frame) {
            var self = this;
            var render = function () {
                if (!self.compiled) {
                    self._compile();
                }
                var context = new Context(ctx || {}, self.blocks);
                return self.rootRenderFunc(self.env, context, frame || new Frame(), runtime);
            };
            return lib.withPrettyErrors(this.path, this.env.dev, render);
        }, isUpToDate: function () {
            return this.upToDate();
        }, getExported: function () {
            if (!this.compiled) {
                this._compile();
            }
            var context = new Context({}, this.blocks);
            this.rootRenderFunc(this.env, context, new Frame(), runtime);
            return context.getExported();
        }, _compile: function () {
            var props;
            if (this.tmplProps) {
                props = this.tmplProps;
            }
            else {
                var source = compiler.compile(this.tmplStr, this.env.extensionsList, this.path);
                var func = new Function(source);
                props = func();
            }
            this.blocks = this._getBlocks(props);
            this.rootRenderFunc = props.root;
            this.compiled = true;
        }, _getBlocks: function (props) {
            var blocks = {};
            for (var k in props) {
                if (k.slice(0, 2) == 'b_') {
                    blocks[k.slice(2)] = props[k];
                }
            }
            return blocks;
        }});
        modules['environment'] = {Environment: Environment, Template: Template};
    })();
    var nunjucks;
    var env = modules["environment"];
    var compiler = modules["compiler"];
    var parser = modules["parser"];
    var lexer = modules["lexer"];
    var runtime = modules["runtime"];
    var loaders = modules["loaders"];
    nunjucks = {};
    nunjucks.Environment = env.Environment;
    nunjucks.Template = env.Template;
    if (loaders) {
        if (loaders.FileSystemLoader) {
            nunjucks.FileSystemLoader = loaders.FileSystemLoader;
        }
        else {
            nunjucks.HttpLoader = loaders.HttpLoader;
        }
    }
    nunjucks.compiler = compiler;
    nunjucks.parser = parser;
    nunjucks.lexer = lexer;
    nunjucks.runtime = runtime;
    nunjucks.require = function (name) {
        return modules[name];
    };
    if (typeof define === 'function' && define.amd) {
        define(function () {
            return nunjucks;
        });
    }
    else {
        window.nunjucks = nunjucks;
    }
})();
var nunjucks_register_filters = function (nj) {
    nj.addFilter('shorten', function (str, count) {
        if (str == undefined) {
            return'';
        }
        return str.slice(0, count || 5);
    });
    nj.addFilter('truncate_chars_inner', function (str, count) {
        try {
            if (str && str.length > count) {
                var limit = Math.floor((count - 5) / 2)
                var a = str.substr(0, limit);
                var b = str.substr(str.length - limit, limit);
                return a + ' ... ' + b;
            } else {
                return str;
            }
        } catch (e) {
            return'';
        }
    });
    nj.addFilter('highlight', function (str, query) {
        var re = new RegExp(query, "gi");
        var highlighted = str.replace(re, '<em class="highlight">' + query + '</em>');
        return highlighted
    });
    nj.addFilter('format_timestamp', function (time) {
        if (time == undefined) {
            return'';
        }
        return'{0}/{1}/{2} {3}:{4}'.format(time.substr(0, 4), time.substr(5, 2), time.substr(8, 2), time.substr(11, 2), time.substr(14, 2));
    });
    nj.addFilter('format_datetime', function (time, part) {
        if (time == undefined) {
            return'';
        }
        var ret;
        if (part == 'datetime') {
            ret = '{0}/{1}/{2} {3}:{4}'.format(time.substr(0, 4), time.substr(5, 2), time.substr(8, 2), time.substr(11, 2), time.substr(14, 2));
        }
        if (part == 'date') {
            ret = '{0}/{1}/{2}'.format(time.substr(0, 4), time.substr(5, 2), time.substr(8, 2));
        }
        if (part == 'time') {
            ret = '{0}:{1}'.format(time.substr(11, 2), time.substr(14, 2));
        }
        return ret;
    });
    nj.addFilter('ms2time', function (time) {
        if (time == undefined) {
            return'';
        }
        if (time == 0) {
            return'00:00:000';
        }
        time = Math.abs(time);
        var millis = time % 1000;
        time = parseInt(time / 1000);
        var seconds = time % 60;
        time = parseInt(time / 60);
        var minutes = time % 60;
        time = parseInt(time / 60);
        var hours = time % 24;
        var out = "";
        if (hours && hours > 0) {
            if (hours < 10) {
                out += '0';
            }
            out += hours + ':';
        } else {
        }
        if (minutes && minutes > 0) {
            if (minutes < 10) {
                out += '0';
            }
            out += minutes + ':';
        } else {
            out += '00' + ':';
        }
        if (seconds && seconds > 0) {
            if (seconds < 10) {
                out += '0';
            }
            out += seconds + ':';
        } else {
            out += '00' + ':';
        }
        if (millis && millis > 0) {
            if (millis < 10) {
                out += '0';
            }
            out += millis + '';
        } else {
            out += '000' + '';
        }
        return out.trim();
    });
    nj.addFilter('s2time', function (time) {
        if (time == undefined) {
            return'';
        }
        if (time == 0) {
            return'00:00';
        }
        time = Math.abs(time);
        var seconds = time % 60 * 60;
        time = parseInt(time / 60);
        var minutes = time % 60;
        time = parseInt(time / 60);
        var hours = time % 24;
        var out = "";
        if (hours && hours > 0) {
            out += hours + ':';
        } else {
        }
        if (minutes && minutes > 0) {
            if (minutes < 10) {
                out += '0';
            }
            out += minutes + ':';
        } else {
            out += '00' + ':';
        }
        if (seconds && seconds > 0) {
            if (seconds < 10) {
                out += '0';
            }
            out += seconds;
        } else {
            out += '00';
        }
        return out.trim();
    });
    nj.addFilter('linebreaksbr', function (str) {
        var breakTag = '<br>';
        return(str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
    });
    return nj;
};
String.prototype.format = function () {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{' + i + '\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};
jQuery.fn.daterangepicker = function (settings) {
    var rangeInput = jQuery(this);
    var options = jQuery.extend({presetRanges: [
        {text: 'Today', dateStart: 'today', dateEnd: 'today'},
        {text: 'Last 7 days', dateStart: 'today-7days', dateEnd: 'today'},
        {text: 'Month to date', dateStart: function () {
            return Date.parse('today').moveToFirstDayOfMonth();
        }, dateEnd: 'today'},
        {text: 'Year to date', dateStart: function () {
            var x = Date.parse('today');
            x.setMonth(0);
            x.setDate(1);
            return x;
        }, dateEnd: 'today'},
        {text: 'The previous Month', dateStart: function () {
            return Date.parse('1 month ago').moveToFirstDayOfMonth();
        }, dateEnd: function () {
            return Date.parse('1 month ago').moveToLastDayOfMonth();
        }}
    ], presets: {specificDate: 'Specific Date', allDatesBefore: 'All Dates Before', allDatesAfter: 'All Dates After', dateRange: 'Date Range'}, rangeStartTitle: 'Start date', rangeEndTitle: 'End date', nextLinkText: 'Next', prevLinkText: 'Prev', doneButtonText: 'Done', earliestDate: Date.parse('-15years'), latestDate: Date.parse('+15years'), rangeSplitter: '-', dateFormat: 'm/d/yy', closeOnSelect: true, arrows: false, posX: rangeInput.offset().left, posY: rangeInput.offset().top + rangeInput.outerHeight(), appendTo: 'body', onClose: function () {
    }, onOpen: function () {
    }, onChange: function () {
    }, datepickerOptions: null}, settings);
    var datepickerOptions = {onSelect: function () {
        if (rp.find('.ui-daterangepicker-specificDate').is('.ui-state-active')) {
            rp.find('.range-end').datepicker('setDate', rp.find('.range-start').datepicker('getDate'));
        }
        var rangeA = fDate(rp.find('.range-start').datepicker('getDate'));
        var rangeB = fDate(rp.find('.range-end').datepicker('getDate'));
        if (rangeInput.length == 2) {
            rangeInput.eq(0).val(rangeA);
            rangeInput.eq(1).val(rangeB);
        }
        else {
            rangeInput.val((rangeA != rangeB) ? rangeA + ' ' + options.rangeSplitter + ' ' + rangeB : rangeA);
        }
        if (options.closeOnSelect) {
            if (!rp.find('li.ui-state-active').is('.ui-daterangepicker-dateRange') && !rp.is(':animated')) {
                hideRP();
            }
        }
        options.onChange();
    }, defaultDate: +0};
    rangeInput.change(options.onChange);
    options.datepickerOptions = (settings) ? jQuery.extend(datepickerOptions, settings.datepickerOptions) : datepickerOptions;
    var inputDateA, inputDateB = Date.parse('today');
    var inputDateAtemp, inputDateBtemp;
    if (rangeInput.size() == 2) {
        inputDateAtemp = Date.parse(rangeInput.eq(0).val());
        inputDateBtemp = Date.parse(rangeInput.eq(1).val());
        if (inputDateAtemp == null) {
            inputDateAtemp = inputDateBtemp;
        }
        if (inputDateBtemp == null) {
            inputDateBtemp = inputDateAtemp;
        }
    }
    else {
        inputDateAtemp = Date.parse(rangeInput.val().split(options.rangeSplitter)[0]);
        inputDateBtemp = Date.parse(rangeInput.val().split(options.rangeSplitter)[1]);
        if (inputDateBtemp == null) {
            inputDateBtemp = inputDateAtemp;
        }
    }
    if (inputDateAtemp != null) {
        inputDateA = inputDateAtemp;
    }
    if (inputDateBtemp != null) {
        inputDateB = inputDateBtemp;
    }
    var rp = jQuery('<div class="ui-daterangepicker ui-widget ui-helper-clearfix ui-widget-content ui-corner-all"></div>');
    var rpPresets = (function () {
        var ul = jQuery('<ul class="ui-widget-content"></ul>').appendTo(rp);
        jQuery.each(options.presetRanges, function () {
            jQuery('<li class="ui-daterangepicker-' + this.text.replace(/ /g, '') + ' ui-corner-all"><a href="#">' + this.text + '</a></li>').data('dateStart', this.dateStart).data('dateEnd', this.dateEnd).appendTo(ul);
        });
        var x = 0;
        jQuery.each(options.presets, function (key, value) {
            jQuery('<li class="ui-daterangepicker-' + key + ' preset_' + x + ' ui-helper-clearfix ui-corner-all"><span class="ui-icon ui-icon-triangle-1-e"></span><a href="#">' + value + '</a></li>').appendTo(ul);
            x++;
        });
        ul.find('li').hover(function () {
            jQuery(this).addClass('ui-state-hover');
        },function () {
            jQuery(this).removeClass('ui-state-hover');
        }).click(function () {
            rp.find('.ui-state-active').removeClass('ui-state-active');
            jQuery(this).addClass('ui-state-active').clickActions(rp, rpPickers, doneBtn);
            return false;
        });
        return ul;
    })();

    function fDate(date) {
        if (!date.getDate()) {
            return'';
        }
        var day = date.getDate();
        var month = date.getMonth();
        var year = date.getFullYear();
        month++;
        var dateFormat = options.dateFormat;
        return jQuery.datepicker.formatDate(dateFormat, date);
    }

    jQuery.fn.restoreDateFromData = function () {
        if (jQuery(this).data('saveDate')) {
            jQuery(this).datepicker('setDate', jQuery(this).data('saveDate')).removeData('saveDate');
        }
        return this;
    }
    jQuery.fn.saveDateToData = function () {
        if (!jQuery(this).data('saveDate')) {
            jQuery(this).data('saveDate', jQuery(this).datepicker('getDate'));
        }
        return this;
    }
    function showRP() {
        if (rp.data('state') == 'closed') {
            rp.data('state', 'open');
            rp.fadeIn(300);
            options.onOpen();
        }
    }

    function hideRP() {
        if (rp.data('state') == 'open') {
            rp.data('state', 'closed');
            rp.fadeOut(300);
            options.onClose();
        }
    }

    function toggleRP() {
        if (rp.data('state') == 'open') {
            hideRP();
        }
        else {
            showRP();
        }
    }

    rp.data('state', 'closed');
    jQuery.fn.clickActions = function (rp, rpPickers, doneBtn) {
        if (jQuery(this).is('.ui-daterangepicker-specificDate')) {
            doneBtn.hide();
            rpPickers.show();
            rp.find('.title-start').text(options.presets.specificDate);
            rp.find('.range-start').restoreDateFromData().show(400);
            rp.find('.range-end').restoreDateFromData().hide(400);
            setTimeout(function () {
                doneBtn.fadeIn();
            }, 400);
        }
        else if (jQuery(this).is('.ui-daterangepicker-allDatesBefore')) {
            doneBtn.hide();
            rpPickers.show();
            rp.find('.title-end').text(options.presets.allDatesBefore);
            rp.find('.range-start').saveDateToData().datepicker('setDate', options.earliestDate).hide(400);
            rp.find('.range-end').restoreDateFromData().show(400);
            setTimeout(function () {
                doneBtn.fadeIn();
            }, 400);
        }
        else if (jQuery(this).is('.ui-daterangepicker-allDatesAfter')) {
            doneBtn.hide();
            rpPickers.show();
            rp.find('.title-start').text(options.presets.allDatesAfter);
            rp.find('.range-start').restoreDateFromData().show(400);
            rp.find('.range-end').saveDateToData().datepicker('setDate', options.latestDate).hide(400);
            setTimeout(function () {
                doneBtn.fadeIn();
            }, 400);
        }
        else if (jQuery(this).is('.ui-daterangepicker-dateRange')) {
            doneBtn.hide();
            rpPickers.show();
            rp.find('.title-start').text(options.rangeStartTitle);
            rp.find('.title-end').text(options.rangeEndTitle);
            rp.find('.range-start').restoreDateFromData().show(400);
            rp.find('.range-end').restoreDateFromData().show(400);
            setTimeout(function () {
                doneBtn.fadeIn();
            }, 400);
        }
        else {
            doneBtn.hide();
            rp.find('.range-start, .range-end').hide(400, function () {
                rpPickers.hide();
            });
            var dateStart = (typeof jQuery(this).data('dateStart') == 'string') ? Date.parse(jQuery(this).data('dateStart')) : jQuery(this).data('dateStart')();
            var dateEnd = (typeof jQuery(this).data('dateEnd') == 'string') ? Date.parse(jQuery(this).data('dateEnd')) : jQuery(this).data('dateEnd')();
            rp.find('.range-start').datepicker('setDate', dateStart).find('.ui-datepicker-current-day').trigger('click');
            rp.find('.range-end').datepicker('setDate', dateEnd).find('.ui-datepicker-current-day').trigger('click');
        }
        return false;
    }
    var rpPickers = jQuery('<div class="ranges ui-widget-header ui-corner-all ui-helper-clearfix"><div class="range-start"><span class="title-start">Start Date</span></div><div class="range-end"><span class="title-end">End Date</span></div></div>').appendTo(rp);
    rpPickers.find('.range-start, .range-end').datepicker(options.datepickerOptions);
    rpPickers.find('.range-start').datepicker('setDate', inputDateA);
    rpPickers.find('.range-end').datepicker('setDate', inputDateB);
    var doneBtn = jQuery('<button class="btnDone ui-state-default ui-corner-all">' + options.doneButtonText + '</button>').click(function () {
        rp.find('.ui-datepicker-current-day').trigger('click');
        hideRP();
    }).hover(function () {
        jQuery(this).addClass('ui-state-hover');
    },function () {
        jQuery(this).removeClass('ui-state-hover');
    }).appendTo(rpPickers);
    jQuery(this).click(function () {
        toggleRP();
        return false;
    });
    rpPickers.css('display', 'none').find('.range-start, .range-end, .btnDone').css('display', 'none');
    jQuery(options.appendTo).append(rp);
    rp.wrap('<div class="ui-daterangepickercontain"></div>');
    if (options.posX) {
        rp.parent().css('left', options.posX);
    }
    if (options.posY) {
        rp.parent().css('top', options.posY);
    }
    if (options.arrows && rangeInput.size() == 1) {
        var prevLink = jQuery('<a href="#" class="ui-daterangepicker-prev ui-corner-all" title="' + options.prevLinkText + '"><span class="ui-icon ui-icon-circle-triangle-w">' + options.prevLinkText + '</span></a>');
        var nextLink = jQuery('<a href="#" class="ui-daterangepicker-next ui-corner-all" title="' + options.nextLinkText + '"><span class="ui-icon ui-icon-circle-triangle-e">' + options.nextLinkText + '</span></a>');
        jQuery(this).addClass('ui-rangepicker-input ui-widget-content').wrap('<div class="ui-daterangepicker-arrows ui-widget ui-widget-header ui-helper-clearfix ui-corner-all"></div>').before(prevLink).before(nextLink).parent().find('a').click(function () {
            var dateA = rpPickers.find('.range-start').datepicker('getDate');
            var dateB = rpPickers.find('.range-end').datepicker('getDate');
            var diff = Math.abs(new TimeSpan(dateA - dateB).getTotalMilliseconds()) + 86400000;
            if (jQuery(this).is('.ui-daterangepicker-prev')) {
                diff = -diff;
            }
            rpPickers.find('.range-start, .range-end ').each(function () {
                var thisDate = jQuery(this).datepicker("getDate");
                if (thisDate == null) {
                    return false;
                }
                jQuery(this).datepicker("setDate", thisDate.add({milliseconds: diff})).find('.ui-datepicker-current-day').trigger('click');
            });
            return false;
        }).hover(function () {
                jQuery(this).addClass('ui-state-hover');
            }, function () {
                jQuery(this).removeClass('ui-state-hover');
            });
    }
    jQuery(document).click(function () {
        if (rp.is(':visible')) {
            hideRP();
        }
    });
    rp.click(function () {
        return false;
    }).hide();
    return this;
}
Date.CultureInfo = {name: "en-US", englishName: "English (United States)", nativeName: "English (United States)", dayNames: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], abbreviatedDayNames: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], shortestDayNames: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"], firstLetterDayNames: ["S", "M", "T", "W", "T", "F", "S"], monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], abbreviatedMonthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], amDesignator: "AM", pmDesignator: "PM", firstDayOfWeek: 0, twoDigitYearMax: 2029, dateElementOrder: "mdy", formatPatterns: {shortDate: "M/d/yyyy", longDate: "dddd, MMMM dd, yyyy", shortTime: "h:mm tt", longTime: "h:mm:ss tt", fullDateTime: "dddd, MMMM dd, yyyy h:mm:ss tt", sortableDateTime: "yyyy-MM-ddTHH:mm:ss", universalSortableDateTime: "yyyy-MM-dd HH:mm:ssZ", rfc1123: "ddd, dd MMM yyyy HH:mm:ss GMT", monthDay: "MMMM dd", yearMonth: "MMMM, yyyy"}, regexPatterns: {jan: /^jan(uary)?/i, feb: /^feb(ruary)?/i, mar: /^mar(ch)?/i, apr: /^apr(il)?/i, may: /^may/i, jun: /^jun(e)?/i, jul: /^jul(y)?/i, aug: /^aug(ust)?/i, sep: /^sep(t(ember)?)?/i, oct: /^oct(ober)?/i, nov: /^nov(ember)?/i, dec: /^dec(ember)?/i, sun: /^su(n(day)?)?/i, mon: /^mo(n(day)?)?/i, tue: /^tu(e(s(day)?)?)?/i, wed: /^we(d(nesday)?)?/i, thu: /^th(u(r(s(day)?)?)?)?/i, fri: /^fr(i(day)?)?/i, sat: /^sa(t(urday)?)?/i, future: /^next/i, past: /^last|past|prev(ious)?/i, add: /^(\+|after|from)/i, subtract: /^(\-|before|ago)/i, yesterday: /^yesterday/i, today: /^t(oday)?/i, tomorrow: /^tomorrow/i, now: /^n(ow)?/i, millisecond: /^ms|milli(second)?s?/i, second: /^sec(ond)?s?/i, minute: /^min(ute)?s?/i, hour: /^h(ou)?rs?/i, week: /^w(ee)?k/i, month: /^m(o(nth)?s?)?/i, day: /^d(ays?)?/i, year: /^y((ea)?rs?)?/i, shortMeridian: /^(a|p)/i, longMeridian: /^(a\.?m?\.?|p\.?m?\.?)/i, timezone: /^((e(s|d)t|c(s|d)t|m(s|d)t|p(s|d)t)|((gmt)?\s*(\+|\-)\s*\d\d\d\d?)|gmt)/i, ordinalSuffix: /^\s*(st|nd|rd|th)/i, timeContext: /^\s*(\:|a|p)/i}, abbreviatedTimeZoneStandard: {GMT: "-000", EST: "-0400", CST: "-0500", MST: "-0600", PST: "-0700"}, abbreviatedTimeZoneDST: {GMT: "-000", EDT: "-0500", CDT: "-0600", MDT: "-0700", PDT: "-0800"}};
Date.getMonthNumberFromName = function (name) {
    var n = Date.CultureInfo.monthNames, m = Date.CultureInfo.abbreviatedMonthNames, s = name.toLowerCase();
    for (var i = 0; i < n.length; i++) {
        if (n[i].toLowerCase() == s || m[i].toLowerCase() == s) {
            return i;
        }
    }
    return-1;
};
Date.getDayNumberFromName = function (name) {
    var n = Date.CultureInfo.dayNames, m = Date.CultureInfo.abbreviatedDayNames, o = Date.CultureInfo.shortestDayNames, s = name.toLowerCase();
    for (var i = 0; i < n.length; i++) {
        if (n[i].toLowerCase() == s || m[i].toLowerCase() == s) {
            return i;
        }
    }
    return-1;
};
Date.isLeapYear = function (year) {
    return(((year % 4 === 0) && (year % 100 !== 0)) || (year % 400 === 0));
};
Date.getDaysInMonth = function (year, month) {
    return[31, (Date.isLeapYear(year) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month];
};
Date.getTimezoneOffset = function (s, dst) {
    return(dst || false) ? Date.CultureInfo.abbreviatedTimeZoneDST[s.toUpperCase()] : Date.CultureInfo.abbreviatedTimeZoneStandard[s.toUpperCase()];
};
Date.getTimezoneAbbreviation = function (offset, dst) {
    var n = (dst || false) ? Date.CultureInfo.abbreviatedTimeZoneDST : Date.CultureInfo.abbreviatedTimeZoneStandard, p;
    for (p in n) {
        if (n[p] === offset) {
            return p;
        }
    }
    return null;
};
Date.prototype.clone = function () {
    return new Date(this.getTime());
};
Date.prototype.compareTo = function (date) {
    if (isNaN(this)) {
        throw new Error(this);
    }
    if (date instanceof Date && !isNaN(date)) {
        return(this > date) ? 1 : (this < date) ? -1 : 0;
    } else {
        throw new TypeError(date);
    }
};
Date.prototype.equals = function (date) {
    return(this.compareTo(date) === 0);
};
Date.prototype.between = function (start, end) {
    var t = this.getTime();
    return t >= start.getTime() && t <= end.getTime();
};
Date.prototype.addMilliseconds = function (value) {
    this.setMilliseconds(this.getMilliseconds() + value);
    return this;
};
Date.prototype.addSeconds = function (value) {
    return this.addMilliseconds(value * 1000);
};
Date.prototype.addMinutes = function (value) {
    return this.addMilliseconds(value * 60000);
};
Date.prototype.addHours = function (value) {
    return this.addMilliseconds(value * 3600000);
};
Date.prototype.addDays = function (value) {
    return this.addMilliseconds(value * 86400000);
};
Date.prototype.addWeeks = function (value) {
    return this.addMilliseconds(value * 604800000);
};
Date.prototype.addMonths = function (value) {
    var n = this.getDate();
    this.setDate(1);
    this.setMonth(this.getMonth() + value);
    this.setDate(Math.min(n, this.getDaysInMonth()));
    return this;
};
Date.prototype.addYears = function (value) {
    return this.addMonths(value * 12);
};
Date.prototype.add = function (config) {
    if (typeof config == "number") {
        this._orient = config;
        return this;
    }
    var x = config;
    if (x.millisecond || x.milliseconds) {
        this.addMilliseconds(x.millisecond || x.milliseconds);
    }
    if (x.second || x.seconds) {
        this.addSeconds(x.second || x.seconds);
    }
    if (x.minute || x.minutes) {
        this.addMinutes(x.minute || x.minutes);
    }
    if (x.hour || x.hours) {
        this.addHours(x.hour || x.hours);
    }
    if (x.month || x.months) {
        this.addMonths(x.month || x.months);
    }
    if (x.year || x.years) {
        this.addYears(x.year || x.years);
    }
    if (x.day || x.days) {
        this.addDays(x.day || x.days);
    }
    return this;
};
Date._validate = function (value, min, max, name) {
    if (typeof value != "number") {
        throw new TypeError(value + " is not a Number.");
    } else if (value < min || value > max) {
        throw new RangeError(value + " is not a valid value for " + name + ".");
    }
    return true;
};
Date.validateMillisecond = function (n) {
    return Date._validate(n, 0, 999, "milliseconds");
};
Date.validateSecond = function (n) {
    return Date._validate(n, 0, 59, "seconds");
};
Date.validateMinute = function (n) {
    return Date._validate(n, 0, 59, "minutes");
};
Date.validateHour = function (n) {
    return Date._validate(n, 0, 23, "hours");
};
Date.validateDay = function (n, year, month) {
    return Date._validate(n, 1, Date.getDaysInMonth(year, month), "days");
};
Date.validateMonth = function (n) {
    return Date._validate(n, 0, 11, "months");
};
Date.validateYear = function (n) {
    return Date._validate(n, 1, 9999, "seconds");
};
Date.prototype.set = function (config) {
    var x = config;
    if (!x.millisecond && x.millisecond !== 0) {
        x.millisecond = -1;
    }
    if (!x.second && x.second !== 0) {
        x.second = -1;
    }
    if (!x.minute && x.minute !== 0) {
        x.minute = -1;
    }
    if (!x.hour && x.hour !== 0) {
        x.hour = -1;
    }
    if (!x.day && x.day !== 0) {
        x.day = -1;
    }
    if (!x.month && x.month !== 0) {
        x.month = -1;
    }
    if (!x.year && x.year !== 0) {
        x.year = -1;
    }
    if (x.millisecond != -1 && Date.validateMillisecond(x.millisecond)) {
        this.addMilliseconds(x.millisecond - this.getMilliseconds());
    }
    if (x.second != -1 && Date.validateSecond(x.second)) {
        this.addSeconds(x.second - this.getSeconds());
    }
    if (x.minute != -1 && Date.validateMinute(x.minute)) {
        this.addMinutes(x.minute - this.getMinutes());
    }
    if (x.hour != -1 && Date.validateHour(x.hour)) {
        this.addHours(x.hour - this.getHours());
    }
    if (x.month !== -1 && Date.validateMonth(x.month)) {
        this.addMonths(x.month - this.getMonth());
    }
    if (x.year != -1 && Date.validateYear(x.year)) {
        this.addYears(x.year - this.getFullYear());
    }
    if (x.day != -1 && Date.validateDay(x.day, this.getFullYear(), this.getMonth())) {
        this.addDays(x.day - this.getDate());
    }
    if (x.timezone) {
        this.setTimezone(x.timezone);
    }
    if (x.timezoneOffset) {
        this.setTimezoneOffset(x.timezoneOffset);
    }
    return this;
};
Date.prototype.clearTime = function () {
    this.setHours(0);
    this.setMinutes(0);
    this.setSeconds(0);
    this.setMilliseconds(0);
    return this;
};
Date.prototype.isLeapYear = function () {
    var y = this.getFullYear();
    return(((y % 4 === 0) && (y % 100 !== 0)) || (y % 400 === 0));
};
Date.prototype.isWeekday = function () {
    return!(this.is().sat() || this.is().sun());
};
Date.prototype.getDaysInMonth = function () {
    return Date.getDaysInMonth(this.getFullYear(), this.getMonth());
};
Date.prototype.moveToFirstDayOfMonth = function () {
    return this.set({day: 1});
};
Date.prototype.moveToLastDayOfMonth = function () {
    return this.set({day: this.getDaysInMonth()});
};
Date.prototype.moveToDayOfWeek = function (day, orient) {
    var diff = (day - this.getDay() + 7 * (orient || +1)) % 7;
    return this.addDays((diff === 0) ? diff += 7 * (orient || +1) : diff);
};
Date.prototype.moveToMonth = function (month, orient) {
    var diff = (month - this.getMonth() + 12 * (orient || +1)) % 12;
    return this.addMonths((diff === 0) ? diff += 12 * (orient || +1) : diff);
};
Date.prototype.getDayOfYear = function () {
    return Math.floor((this - new Date(this.getFullYear(), 0, 1)) / 86400000);
};
Date.prototype.getWeekOfYear = function (firstDayOfWeek) {
    var y = this.getFullYear(), m = this.getMonth(), d = this.getDate();
    var dow = firstDayOfWeek || Date.CultureInfo.firstDayOfWeek;
    var offset = 7 + 1 - new Date(y, 0, 1).getDay();
    if (offset == 8) {
        offset = 1;
    }
    var daynum = ((Date.UTC(y, m, d, 0, 0, 0) - Date.UTC(y, 0, 1, 0, 0, 0)) / 86400000) + 1;
    var w = Math.floor((daynum - offset + 7) / 7);
    if (w === dow) {
        y--;
        var prevOffset = 7 + 1 - new Date(y, 0, 1).getDay();
        if (prevOffset == 2 || prevOffset == 8) {
            w = 53;
        } else {
            w = 52;
        }
    }
    return w;
};
Date.prototype.isDST = function () {
    return this.toString().match(/(E|C|M|P)(S|D)T/)[2] == "D";
};
Date.prototype.getTimezone = function () {
    return Date.getTimezoneAbbreviation(this.getUTCOffset, this.isDST());
};
Date.prototype.setTimezoneOffset = function (s) {
    var here = this.getTimezoneOffset(), there = Number(s) * -6 / 10;
    this.addMinutes(there - here);
    return this;
};
Date.prototype.setTimezone = function (s) {
    return this.setTimezoneOffset(Date.getTimezoneOffset(s));
};
Date.prototype.getUTCOffset = function () {
    var n = this.getTimezoneOffset() * -10 / 6, r;
    if (n < 0) {
        r = (n - 10000).toString();
        return r[0] + r.substr(2);
    } else {
        r = (n + 10000).toString();
        return"+" + r.substr(1);
    }
};
Date.prototype.getDayName = function (abbrev) {
    return abbrev ? Date.CultureInfo.abbreviatedDayNames[this.getDay()] : Date.CultureInfo.dayNames[this.getDay()];
};
Date.prototype.getMonthName = function (abbrev) {
    return abbrev ? Date.CultureInfo.abbreviatedMonthNames[this.getMonth()] : Date.CultureInfo.monthNames[this.getMonth()];
};
Date.prototype._toString = Date.prototype.toString;
Date.prototype.toString = function (format) {
    var self = this;
    var p = function p(s) {
        return(s.toString().length == 1) ? "0" + s : s;
    };
    return format ? format.replace(/dd?d?d?|MM?M?M?|yy?y?y?|hh?|HH?|mm?|ss?|tt?|zz?z?/g, function (format) {
        switch (format) {
            case"hh":
                return p(self.getHours() < 13 ? self.getHours() : (self.getHours() - 12));
            case"h":
                return self.getHours() < 13 ? self.getHours() : (self.getHours() - 12);
            case"HH":
                return p(self.getHours());
            case"H":
                return self.getHours();
            case"mm":
                return p(self.getMinutes());
            case"m":
                return self.getMinutes();
            case"ss":
                return p(self.getSeconds());
            case"s":
                return self.getSeconds();
            case"yyyy":
                return self.getFullYear();
            case"yy":
                return self.getFullYear().toString().substring(2, 4);
            case"dddd":
                return self.getDayName();
            case"ddd":
                return self.getDayName(true);
            case"dd":
                return p(self.getDate());
            case"d":
                return self.getDate().toString();
            case"MMMM":
                return self.getMonthName();
            case"MMM":
                return self.getMonthName(true);
            case"MM":
                return p((self.getMonth() + 1));
            case"M":
                return self.getMonth() + 1;
            case"t":
                return self.getHours() < 12 ? Date.CultureInfo.amDesignator.substring(0, 1) : Date.CultureInfo.pmDesignator.substring(0, 1);
            case"tt":
                return self.getHours() < 12 ? Date.CultureInfo.amDesignator : Date.CultureInfo.pmDesignator;
            case"zzz":
            case"zz":
            case"z":
                return"";
        }
    }) : this._toString();
};
Date.now = function () {
    return new Date();
};
Date.today = function () {
    return Date.now().clearTime();
};
Date.prototype._orient = +1;
Date.prototype.next = function () {
    this._orient = +1;
    return this;
};
Date.prototype.last = Date.prototype.prev = Date.prototype.previous = function () {
    this._orient = -1;
    return this;
};
Date.prototype._is = false;
Date.prototype.is = function () {
    this._is = true;
    return this;
};
Number.prototype._dateElement = "day";
Number.prototype.fromNow = function () {
    var c = {};
    c[this._dateElement] = this;
    return Date.now().add(c);
};
Number.prototype.ago = function () {
    var c = {};
    c[this._dateElement] = this * -1;
    return Date.now().add(c);
};
(function () {
    var $D = Date.prototype, $N = Number.prototype;
    var dx = ("sunday monday tuesday wednesday thursday friday saturday").split(/\s/), mx = ("january february march april may june july august september october november december").split(/\s/), px = ("Millisecond Second Minute Hour Day Week Month Year").split(/\s/), de;
    var df = function (n) {
        return function () {
            if (this._is) {
                this._is = false;
                return this.getDay() == n;
            }
            return this.moveToDayOfWeek(n, this._orient);
        };
    };
    for (var i = 0; i < dx.length; i++) {
        $D[dx[i]] = $D[dx[i].substring(0, 3)] = df(i);
    }
    var mf = function (n) {
        return function () {
            if (this._is) {
                this._is = false;
                return this.getMonth() === n;
            }
            return this.moveToMonth(n, this._orient);
        };
    };
    for (var j = 0; j < mx.length; j++) {
        $D[mx[j]] = $D[mx[j].substring(0, 3)] = mf(j);
    }
    var ef = function (j) {
        return function () {
            if (j.substring(j.length - 1) != "s") {
                j += "s";
            }
            return this["add" + j](this._orient);
        };
    };
    var nf = function (n) {
        return function () {
            this._dateElement = n;
            return this;
        };
    };
    for (var k = 0; k < px.length; k++) {
        de = px[k].toLowerCase();
        $D[de] = $D[de + "s"] = ef(px[k]);
        $N[de] = $N[de + "s"] = nf(de);
    }
}());
Date.prototype.toJSONString = function () {
    return this.toString("yyyy-MM-ddThh:mm:ssZ");
};
Date.prototype.toShortDateString = function () {
    return this.toString(Date.CultureInfo.formatPatterns.shortDatePattern);
};
Date.prototype.toLongDateString = function () {
    return this.toString(Date.CultureInfo.formatPatterns.longDatePattern);
};
Date.prototype.toShortTimeString = function () {
    return this.toString(Date.CultureInfo.formatPatterns.shortTimePattern);
};
Date.prototype.toLongTimeString = function () {
    return this.toString(Date.CultureInfo.formatPatterns.longTimePattern);
};
Date.prototype.getOrdinal = function () {
    switch (this.getDate()) {
        case 1:
        case 21:
        case 31:
            return"st";
        case 2:
        case 22:
            return"nd";
        case 3:
        case 23:
            return"rd";
        default:
            return"th";
    }
};
(function () {
    Date.Parsing = {Exception: function (s) {
        this.message = "Parse error at '" + s.substring(0, 10) + " ...'";
    }};
    var $P = Date.Parsing;
    var _ = $P.Operators = {rtoken: function (r) {
        return function (s) {
            var mx = s.match(r);
            if (mx) {
                return([mx[0], s.substring(mx[0].length)]);
            } else {
                throw new $P.Exception(s);
            }
        };
    }, token: function (s) {
        return function (s) {
            return _.rtoken(new RegExp("^\s*" + s + "\s*"))(s);
        };
    }, stoken: function (s) {
        return _.rtoken(new RegExp("^" + s));
    }, until: function (p) {
        return function (s) {
            var qx = [], rx = null;
            while (s.length) {
                try {
                    rx = p.call(this, s);
                } catch (e) {
                    qx.push(rx[0]);
                    s = rx[1];
                    continue;
                }
                break;
            }
            return[qx, s];
        };
    }, many: function (p) {
        return function (s) {
            var rx = [], r = null;
            while (s.length) {
                try {
                    r = p.call(this, s);
                } catch (e) {
                    return[rx, s];
                }
                rx.push(r[0]);
                s = r[1];
            }
            return[rx, s];
        };
    }, optional: function (p) {
        return function (s) {
            var r = null;
            try {
                r = p.call(this, s);
            } catch (e) {
                return[null, s];
            }
            return[r[0], r[1]];
        };
    }, not: function (p) {
        return function (s) {
            try {
                p.call(this, s);
            } catch (e) {
                return[null, s];
            }
            throw new $P.Exception(s);
        };
    }, ignore: function (p) {
        return p ? function (s) {
            var r = null;
            r = p.call(this, s);
            return[null, r[1]];
        } : null;
    }, product: function () {
        var px = arguments[0], qx = Array.prototype.slice.call(arguments, 1), rx = [];
        for (var i = 0; i < px.length; i++) {
            rx.push(_.each(px[i], qx));
        }
        return rx;
    }, cache: function (rule) {
        var cache = {}, r = null;
        return function (s) {
            try {
                r = cache[s] = (cache[s] || rule.call(this, s));
            } catch (e) {
                r = cache[s] = e;
            }
            if (r instanceof $P.Exception) {
                throw r;
            } else {
                return r;
            }
        };
    }, any: function () {
        var px = arguments;
        return function (s) {
            var r = null;
            for (var i = 0; i < px.length; i++) {
                if (px[i] == null) {
                    continue;
                }
                try {
                    r = (px[i].call(this, s));
                } catch (e) {
                    r = null;
                }
                if (r) {
                    return r;
                }
            }
            throw new $P.Exception(s);
        };
    }, each: function () {
        var px = arguments;
        return function (s) {
            var rx = [], r = null;
            for (var i = 0; i < px.length; i++) {
                if (px[i] == null) {
                    continue;
                }
                try {
                    r = (px[i].call(this, s));
                } catch (e) {
                    throw new $P.Exception(s);
                }
                rx.push(r[0]);
                s = r[1];
            }
            return[rx, s];
        };
    }, all: function () {
        var px = arguments, _ = _;
        return _.each(_.optional(px));
    }, sequence: function (px, d, c) {
        d = d || _.rtoken(/^\s*/);
        c = c || null;
        if (px.length == 1) {
            return px[0];
        }
        return function (s) {
            var r = null, q = null;
            var rx = [];
            for (var i = 0; i < px.length; i++) {
                try {
                    r = px[i].call(this, s);
                } catch (e) {
                    break;
                }
                rx.push(r[0]);
                try {
                    q = d.call(this, r[1]);
                } catch (ex) {
                    q = null;
                    break;
                }
                s = q[1];
            }
            if (!r) {
                throw new $P.Exception(s);
            }
            if (q) {
                throw new $P.Exception(q[1]);
            }
            if (c) {
                try {
                    r = c.call(this, r[1]);
                } catch (ey) {
                    throw new $P.Exception(r[1]);
                }
            }
            return[rx, (r ? r[1] : s)];
        };
    }, between: function (d1, p, d2) {
        d2 = d2 || d1;
        var _fn = _.each(_.ignore(d1), p, _.ignore(d2));
        return function (s) {
            var rx = _fn.call(this, s);
            return[
                [rx[0][0], r[0][2]],
                rx[1]
            ];
        };
    }, list: function (p, d, c) {
        d = d || _.rtoken(/^\s*/);
        c = c || null;
        return(p instanceof Array ? _.each(_.product(p.slice(0, -1), _.ignore(d)), p.slice(-1), _.ignore(c)) : _.each(_.many(_.each(p, _.ignore(d))), px, _.ignore(c)));
    }, set: function (px, d, c) {
        d = d || _.rtoken(/^\s*/);
        c = c || null;
        return function (s) {
            var r = null, p = null, q = null, rx = null, best = [
                [],
                s
            ], last = false;
            for (var i = 0; i < px.length; i++) {
                q = null;
                p = null;
                r = null;
                last = (px.length == 1);
                try {
                    r = px[i].call(this, s);
                } catch (e) {
                    continue;
                }
                rx = [
                    [r[0]],
                    r[1]
                ];
                if (r[1].length > 0 && !last) {
                    try {
                        q = d.call(this, r[1]);
                    } catch (ex) {
                        last = true;
                    }
                } else {
                    last = true;
                }
                if (!last && q[1].length === 0) {
                    last = true;
                }
                if (!last) {
                    var qx = [];
                    for (var j = 0; j < px.length; j++) {
                        if (i != j) {
                            qx.push(px[j]);
                        }
                    }
                    p = _.set(qx, d).call(this, q[1]);
                    if (p[0].length > 0) {
                        rx[0] = rx[0].concat(p[0]);
                        rx[1] = p[1];
                    }
                }
                if (rx[1].length < best[1].length) {
                    best = rx;
                }
                if (best[1].length === 0) {
                    break;
                }
            }
            if (best[0].length === 0) {
                return best;
            }
            if (c) {
                try {
                    q = c.call(this, best[1]);
                } catch (ey) {
                    throw new $P.Exception(best[1]);
                }
                best[1] = q[1];
            }
            return best;
        };
    }, forward: function (gr, fname) {
        return function (s) {
            return gr[fname].call(this, s);
        };
    }, replace: function (rule, repl) {
        return function (s) {
            var r = rule.call(this, s);
            return[repl, r[1]];
        };
    }, process: function (rule, fn) {
        return function (s) {
            var r = rule.call(this, s);
            return[fn.call(this, r[0]), r[1]];
        };
    }, min: function (min, rule) {
        return function (s) {
            var rx = rule.call(this, s);
            if (rx[0].length < min) {
                throw new $P.Exception(s);
            }
            return rx;
        };
    }};
    var _generator = function (op) {
        return function () {
            var args = null, rx = [];
            if (arguments.length > 1) {
                args = Array.prototype.slice.call(arguments);
            } else if (arguments[0]instanceof Array) {
                args = arguments[0];
            }
            if (args) {
                for (var i = 0, px = args.shift(); i < px.length; i++) {
                    args.unshift(px[i]);
                    rx.push(op.apply(null, args));
                    args.shift();
                    return rx;
                }
            } else {
                return op.apply(null, arguments);
            }
        };
    };
    var gx = "optional not ignore cache".split(/\s/);
    for (var i = 0; i < gx.length; i++) {
        _[gx[i]] = _generator(_[gx[i]]);
    }
    var _vector = function (op) {
        return function () {
            if (arguments[0]instanceof Array) {
                return op.apply(null, arguments[0]);
            } else {
                return op.apply(null, arguments);
            }
        };
    };
    var vx = "each any all".split(/\s/);
    for (var j = 0; j < vx.length; j++) {
        _[vx[j]] = _vector(_[vx[j]]);
    }
}());
(function () {
    var flattenAndCompact = function (ax) {
        var rx = [];
        for (var i = 0; i < ax.length; i++) {
            if (ax[i]instanceof Array) {
                rx = rx.concat(flattenAndCompact(ax[i]));
            } else {
                if (ax[i]) {
                    rx.push(ax[i]);
                }
            }
        }
        return rx;
    };
    Date.Grammar = {};
    Date.Translator = {hour: function (s) {
        return function () {
            this.hour = Number(s);
        };
    }, minute: function (s) {
        return function () {
            this.minute = Number(s);
        };
    }, second: function (s) {
        return function () {
            this.second = Number(s);
        };
    }, meridian: function (s) {
        return function () {
            this.meridian = s.slice(0, 1).toLowerCase();
        };
    }, timezone: function (s) {
        return function () {
            var n = s.replace(/[^\d\+\-]/g, "");
            if (n.length) {
                this.timezoneOffset = Number(n);
            } else {
                this.timezone = s.toLowerCase();
            }
        };
    }, day: function (x) {
        var s = x[0];
        return function () {
            this.day = Number(s.match(/\d+/)[0]);
        };
    }, month: function (s) {
        return function () {
            this.month = ((s.length == 3) ? Date.getMonthNumberFromName(s) : (Number(s) - 1));
        };
    }, year: function (s) {
        return function () {
            var n = Number(s);
            this.year = ((s.length > 2) ? n : (n + (((n + 2000) < Date.CultureInfo.twoDigitYearMax) ? 2000 : 1900)));
        };
    }, rday: function (s) {
        return function () {
            switch (s) {
                case"yesterday":
                    this.days = -1;
                    break;
                case"tomorrow":
                    this.days = 1;
                    break;
                case"today":
                    this.days = 0;
                    break;
                case"now":
                    this.days = 0;
                    this.now = true;
                    break;
            }
        };
    }, finishExact: function (x) {
        x = (x instanceof Array) ? x : [x];
        var now = new Date();
        this.year = now.getFullYear();
        this.month = now.getMonth();
        this.day = 1;
        this.hour = 0;
        this.minute = 0;
        this.second = 0;
        for (var i = 0; i < x.length; i++) {
            if (x[i]) {
                x[i].call(this);
            }
        }
        this.hour = (this.meridian == "p" && this.hour < 13) ? this.hour + 12 : this.hour;
        if (this.day > Date.getDaysInMonth(this.year, this.month)) {
            throw new RangeError(this.day + " is not a valid value for days.");
        }
        var r = new Date(this.year, this.month, this.day, this.hour, this.minute, this.second);
        if (this.timezone) {
            r.set({timezone: this.timezone});
        } else if (this.timezoneOffset) {
            r.set({timezoneOffset: this.timezoneOffset});
        }
        return r;
    }, finish: function (x) {
        x = (x instanceof Array) ? flattenAndCompact(x) : [x];
        if (x.length === 0) {
            return null;
        }
        for (var i = 0; i < x.length; i++) {
            if (typeof x[i] == "function") {
                x[i].call(this);
            }
        }
        if (this.now) {
            return new Date();
        }
        var today = Date.today();
        var method = null;
        var expression = !!(this.days != null || this.orient || this.operator);
        if (expression) {
            var gap, mod, orient;
            orient = ((this.orient == "past" || this.operator == "subtract") ? -1 : 1);
            if (this.weekday) {
                this.unit = "day";
                gap = (Date.getDayNumberFromName(this.weekday) - today.getDay());
                mod = 7;
                this.days = gap ? ((gap + (orient * mod)) % mod) : (orient * mod);
            }
            if (this.month) {
                this.unit = "month";
                gap = (this.month - today.getMonth());
                mod = 12;
                this.months = gap ? ((gap + (orient * mod)) % mod) : (orient * mod);
                this.month = null;
            }
            if (!this.unit) {
                this.unit = "day";
            }
            if (this[this.unit + "s"] == null || this.operator != null) {
                if (!this.value) {
                    this.value = 1;
                }
                if (this.unit == "week") {
                    this.unit = "day";
                    this.value = this.value * 7;
                }
                this[this.unit + "s"] = this.value * orient;
            }
            return today.add(this);
        } else {
            if (this.meridian && this.hour) {
                this.hour = (this.hour < 13 && this.meridian == "p") ? this.hour + 12 : this.hour;
            }
            if (this.weekday && !this.day) {
                this.day = (today.addDays((Date.getDayNumberFromName(this.weekday) - today.getDay()))).getDate();
            }
            if (this.month && !this.day) {
                this.day = 1;
            }
            return today.set(this);
        }
    }};
    var _ = Date.Parsing.Operators, g = Date.Grammar, t = Date.Translator, _fn;
    g.datePartDelimiter = _.rtoken(/^([\s\-\.\,\/\x27]+)/);
    g.timePartDelimiter = _.stoken(":");
    g.whiteSpace = _.rtoken(/^\s*/);
    g.generalDelimiter = _.rtoken(/^(([\s\,]|at|on)+)/);
    var _C = {};
    g.ctoken = function (keys) {
        var fn = _C[keys];
        if (!fn) {
            var c = Date.CultureInfo.regexPatterns;
            var kx = keys.split(/\s+/), px = [];
            for (var i = 0; i < kx.length; i++) {
                px.push(_.replace(_.rtoken(c[kx[i]]), kx[i]));
            }
            fn = _C[keys] = _.any.apply(null, px);
        }
        return fn;
    };
    g.ctoken2 = function (key) {
        return _.rtoken(Date.CultureInfo.regexPatterns[key]);
    };
    g.h = _.cache(_.process(_.rtoken(/^(0[0-9]|1[0-2]|[1-9])/), t.hour));
    g.hh = _.cache(_.process(_.rtoken(/^(0[0-9]|1[0-2])/), t.hour));
    g.H = _.cache(_.process(_.rtoken(/^([0-1][0-9]|2[0-3]|[0-9])/), t.hour));
    g.HH = _.cache(_.process(_.rtoken(/^([0-1][0-9]|2[0-3])/), t.hour));
    g.m = _.cache(_.process(_.rtoken(/^([0-5][0-9]|[0-9])/), t.minute));
    g.mm = _.cache(_.process(_.rtoken(/^[0-5][0-9]/), t.minute));
    g.s = _.cache(_.process(_.rtoken(/^([0-5][0-9]|[0-9])/), t.second));
    g.ss = _.cache(_.process(_.rtoken(/^[0-5][0-9]/), t.second));
    g.hms = _.cache(_.sequence([g.H, g.mm, g.ss], g.timePartDelimiter));
    g.t = _.cache(_.process(g.ctoken2("shortMeridian"), t.meridian));
    g.tt = _.cache(_.process(g.ctoken2("longMeridian"), t.meridian));
    g.z = _.cache(_.process(_.rtoken(/^(\+|\-)?\s*\d\d\d\d?/), t.timezone));
    g.zz = _.cache(_.process(_.rtoken(/^(\+|\-)\s*\d\d\d\d/), t.timezone));
    g.zzz = _.cache(_.process(g.ctoken2("timezone"), t.timezone));
    g.timeSuffix = _.each(_.ignore(g.whiteSpace), _.set([g.tt, g.zzz]));
    g.time = _.each(_.optional(_.ignore(_.stoken("T"))), g.hms, g.timeSuffix);
    g.d = _.cache(_.process(_.each(_.rtoken(/^([0-2]\d|3[0-1]|\d)/), _.optional(g.ctoken2("ordinalSuffix"))), t.day));
    g.dd = _.cache(_.process(_.each(_.rtoken(/^([0-2]\d|3[0-1])/), _.optional(g.ctoken2("ordinalSuffix"))), t.day));
    g.ddd = g.dddd = _.cache(_.process(g.ctoken("sun mon tue wed thu fri sat"), function (s) {
        return function () {
            this.weekday = s;
        };
    }));
    g.M = _.cache(_.process(_.rtoken(/^(1[0-2]|0\d|\d)/), t.month));
    g.MM = _.cache(_.process(_.rtoken(/^(1[0-2]|0\d)/), t.month));
    g.MMM = g.MMMM = _.cache(_.process(g.ctoken("jan feb mar apr may jun jul aug sep oct nov dec"), t.month));
    g.y = _.cache(_.process(_.rtoken(/^(\d\d?)/), t.year));
    g.yy = _.cache(_.process(_.rtoken(/^(\d\d)/), t.year));
    g.yyy = _.cache(_.process(_.rtoken(/^(\d\d?\d?\d?)/), t.year));
    g.yyyy = _.cache(_.process(_.rtoken(/^(\d\d\d\d)/), t.year));
    _fn = function () {
        return _.each(_.any.apply(null, arguments), _.not(g.ctoken2("timeContext")));
    };
    g.day = _fn(g.d, g.dd);
    g.month = _fn(g.M, g.MMM);
    g.year = _fn(g.yyyy, g.yy);
    g.orientation = _.process(g.ctoken("past future"), function (s) {
        return function () {
            this.orient = s;
        };
    });
    g.operator = _.process(g.ctoken("add subtract"), function (s) {
        return function () {
            this.operator = s;
        };
    });
    g.rday = _.process(g.ctoken("yesterday tomorrow today now"), t.rday);
    g.unit = _.process(g.ctoken("minute hour day week month year"), function (s) {
        return function () {
            this.unit = s;
        };
    });
    g.value = _.process(_.rtoken(/^\d\d?(st|nd|rd|th)?/), function (s) {
        return function () {
            this.value = s.replace(/\D/g, "");
        };
    });
    g.expression = _.set([g.rday, g.operator, g.value, g.unit, g.orientation, g.ddd, g.MMM]);
    _fn = function () {
        return _.set(arguments, g.datePartDelimiter);
    };
    g.mdy = _fn(g.ddd, g.month, g.day, g.year);
    g.ymd = _fn(g.ddd, g.year, g.month, g.day);
    g.dmy = _fn(g.ddd, g.day, g.month, g.year);
    g.date = function (s) {
        return((g[Date.CultureInfo.dateElementOrder] || g.mdy).call(this, s));
    };
    g.format = _.process(_.many(_.any(_.process(_.rtoken(/^(dd?d?d?|MM?M?M?|yy?y?y?|hh?|HH?|mm?|ss?|tt?|zz?z?)/), function (fmt) {
        if (g[fmt]) {
            return g[fmt];
        } else {
            throw Date.Parsing.Exception(fmt);
        }
    }), _.process(_.rtoken(/^[^dMyhHmstz]+/), function (s) {
        return _.ignore(_.stoken(s));
    }))), function (rules) {
        return _.process(_.each.apply(null, rules), t.finishExact);
    });
    var _F = {};
    var _get = function (f) {
        return _F[f] = (_F[f] || g.format(f)[0]);
    };
    g.formats = function (fx) {
        if (fx instanceof Array) {
            var rx = [];
            for (var i = 0; i < fx.length; i++) {
                rx.push(_get(fx[i]));
            }
            return _.any.apply(null, rx);
        } else {
            return _get(fx);
        }
    };
    g._formats = g.formats(["yyyy-MM-ddTHH:mm:ss", "ddd, MMM dd, yyyy H:mm:ss tt", "ddd MMM d yyyy HH:mm:ss zzz", "d"]);
    g._start = _.process(_.set([g.date, g.time, g.expression], g.generalDelimiter, g.whiteSpace), t.finish);
    g.start = function (s) {
        try {
            var r = g._formats.call({}, s);
            if (r[1].length === 0) {
                return r;
            }
        } catch (e) {
        }
        return g._start.call({}, s);
    };
}());
Date._parse = Date.parse;
Date.parse = function (s) {
    var r = null;
    if (!s) {
        return null;
    }
    try {
        r = Date.Grammar.start.call({}, s);
    } catch (e) {
        return null;
    }
    return((r[1].length === 0) ? r[0] : null);
};
Date.getParseFunction = function (fx) {
    var fn = Date.Grammar.formats(fx);
    return function (s) {
        var r = null;
        try {
            r = fn.call({}, s);
        } catch (e) {
            return null;
        }
        return((r[1].length === 0) ? r[0] : null);
    };
};
Date.parseExact = function (s, fx) {
    return Date.getParseFunction(fx)(s);
};
var TimeSpan = function (days, hours, minutes, seconds, milliseconds) {
    var attrs = "days hours minutes seconds milliseconds".split(/\s+/);
    var gFn = function (attr) {
        return function () {
            return this[attr];
        };
    };
    var sFn = function (attr) {
        return function (val) {
            this[attr] = val;
            return this;
        };
    };
    for (var i = 0; i < attrs.length; i++) {
        var $a = attrs[i], $b = $a.slice(0, 1).toUpperCase() + $a.slice(1);
        TimeSpan.prototype[$a] = 0;
        TimeSpan.prototype["get" + $b] = gFn($a);
        TimeSpan.prototype["set" + $b] = sFn($a);
    }
    if (arguments.length == 4) {
        this.setDays(days);
        this.setHours(hours);
        this.setMinutes(minutes);
        this.setSeconds(seconds);
    } else if (arguments.length == 5) {
        this.setDays(days);
        this.setHours(hours);
        this.setMinutes(minutes);
        this.setSeconds(seconds);
        this.setMilliseconds(milliseconds);
    } else if (arguments.length == 1 && typeof days == "number") {
        var orient = (days < 0) ? -1 : +1;
        this.setMilliseconds(Math.abs(days));
        this.setDays(Math.floor(this.getMilliseconds() / 86400000) * orient);
        this.setMilliseconds(this.getMilliseconds() % 86400000);
        this.setHours(Math.floor(this.getMilliseconds() / 3600000) * orient);
        this.setMilliseconds(this.getMilliseconds() % 3600000);
        this.setMinutes(Math.floor(this.getMilliseconds() / 60000) * orient);
        this.setMilliseconds(this.getMilliseconds() % 60000);
        this.setSeconds(Math.floor(this.getMilliseconds() / 1000) * orient);
        this.setMilliseconds(this.getMilliseconds() % 1000);
        this.setMilliseconds(this.getMilliseconds() * orient);
    }
    this.getTotalMilliseconds = function () {
        return(this.getDays() * 86400000) + (this.getHours() * 3600000) + (this.getMinutes() * 60000) + (this.getSeconds() * 1000);
    };
    this.compareTo = function (time) {
        var t1 = new Date(1970, 1, 1, this.getHours(), this.getMinutes(), this.getSeconds()), t2;
        if (time === null) {
            t2 = new Date(1970, 1, 1, 0, 0, 0);
        }
        else {
            t2 = new Date(1970, 1, 1, time.getHours(), time.getMinutes(), time.getSeconds());
        }
        return(t1 < t2) ? -1 : (t1 > t2) ? 1 : 0;
    };
    this.equals = function (time) {
        return(this.compareTo(time) === 0);
    };
    this.add = function (time) {
        return(time === null) ? this : this.addSeconds(time.getTotalMilliseconds() / 1000);
    };
    this.subtract = function (time) {
        return(time === null) ? this : this.addSeconds(-time.getTotalMilliseconds() / 1000);
    };
    this.addDays = function (n) {
        return new TimeSpan(this.getTotalMilliseconds() + (n * 86400000));
    };
    this.addHours = function (n) {
        return new TimeSpan(this.getTotalMilliseconds() + (n * 3600000));
    };
    this.addMinutes = function (n) {
        return new TimeSpan(this.getTotalMilliseconds() + (n * 60000));
    };
    this.addSeconds = function (n) {
        return new TimeSpan(this.getTotalMilliseconds() + (n * 1000));
    };
    this.addMilliseconds = function (n) {
        return new TimeSpan(this.getTotalMilliseconds() + n);
    };
    this.get12HourHour = function () {
        return(this.getHours() > 12) ? this.getHours() - 12 : (this.getHours() === 0) ? 12 : this.getHours();
    };
    this.getDesignator = function () {
        return(this.getHours() < 12) ? Date.CultureInfo.amDesignator : Date.CultureInfo.pmDesignator;
    };
    this.toString = function (format) {
        this._toString = function () {
            if (this.getDays() !== null && this.getDays() > 0) {
                return this.getDays() + "." + this.getHours() + ":" + this.p(this.getMinutes()) + ":" + this.p(this.getSeconds());
            }
            else {
                return this.getHours() + ":" + this.p(this.getMinutes()) + ":" + this.p(this.getSeconds());
            }
        };
        this.p = function (s) {
            return(s.toString().length < 2) ? "0" + s : s;
        };
        var me = this;
        return format ? format.replace(/dd?|HH?|hh?|mm?|ss?|tt?/g, function (format) {
            switch (format) {
                case"d":
                    return me.getDays();
                case"dd":
                    return me.p(me.getDays());
                case"H":
                    return me.getHours();
                case"HH":
                    return me.p(me.getHours());
                case"h":
                    return me.get12HourHour();
                case"hh":
                    return me.p(me.get12HourHour());
                case"m":
                    return me.getMinutes();
                case"mm":
                    return me.p(me.getMinutes());
                case"s":
                    return me.getSeconds();
                case"ss":
                    return me.p(me.getSeconds());
                case"t":
                    return((me.getHours() < 12) ? Date.CultureInfo.amDesignator : Date.CultureInfo.pmDesignator).substring(0, 1);
                case"tt":
                    return(me.getHours() < 12) ? Date.CultureInfo.amDesignator : Date.CultureInfo.pmDesignator;
            }
        }) : this._toString();
    };
    return this;
};
Date.prototype.getTimeOfDay = function () {
    return new TimeSpan(0, this.getHours(), this.getMinutes(), this.getSeconds(), this.getMilliseconds());
};
var TimePeriod = function (years, months, days, hours, minutes, seconds, milliseconds) {
    var attrs = "years months days hours minutes seconds milliseconds".split(/\s+/);
    var gFn = function (attr) {
        return function () {
            return this[attr];
        };
    };
    var sFn = function (attr) {
        return function (val) {
            this[attr] = val;
            return this;
        };
    };
    for (var i = 0; i < attrs.length; i++) {
        var $a = attrs[i], $b = $a.slice(0, 1).toUpperCase() + $a.slice(1);
        TimePeriod.prototype[$a] = 0;
        TimePeriod.prototype["get" + $b] = gFn($a);
        TimePeriod.prototype["set" + $b] = sFn($a);
    }
    if (arguments.length == 7) {
        this.years = years;
        this.months = months;
        this.setDays(days);
        this.setHours(hours);
        this.setMinutes(minutes);
        this.setSeconds(seconds);
        this.setMilliseconds(milliseconds);
    } else if (arguments.length == 2 && arguments[0]instanceof Date && arguments[1]instanceof Date) {
        var d1 = years.clone();
        var d2 = months.clone();
        var temp = d1.clone();
        var orient = (d1 > d2) ? -1 : +1;
        this.years = d2.getFullYear() - d1.getFullYear();
        temp.addYears(this.years);
        if (orient == +1) {
            if (temp > d2) {
                if (this.years !== 0) {
                    this.years--;
                }
            }
        } else {
            if (temp < d2) {
                if (this.years !== 0) {
                    this.years++;
                }
            }
        }
        d1.addYears(this.years);
        if (orient == +1) {
            while (d1 < d2 && d1.clone().addDays(Date.getDaysInMonth(d1.getYear(), d1.getMonth())) < d2) {
                d1.addMonths(1);
                this.months++;
            }
        }
        else {
            while (d1 > d2 && d1.clone().addDays(-d1.getDaysInMonth()) > d2) {
                d1.addMonths(-1);
                this.months--;
            }
        }
        var diff = d2 - d1;
        if (diff !== 0) {
            var ts = new TimeSpan(diff);
            this.setDays(ts.getDays());
            this.setHours(ts.getHours());
            this.setMinutes(ts.getMinutes());
            this.setSeconds(ts.getSeconds());
            this.setMilliseconds(ts.getMilliseconds());
        }
    }
    return this;
};
jQuery.fn.countdown = function (userOptions) {
    var options = {stepTime: 60, format: "dd:hh:mm:ss", startTime: "01:12:32:55", digitImages: 6, digitWidth: 53, digitHeight: 77, timerEnd: function () {
    }, timerBeforeEnd: function () {
    }, image: "digits.png"};
    var digits = [], interval;
    var createDigits = function (where) {
        var c = 0;
        for (var i = 0; i < options.startTime.length; i++) {
            if (parseInt(options.startTime[i]) >= 0) {
                elem = $('<div id="cnt_' + i + '" class="digit" />').css({height: options.digitHeight * options.digitImages * 10, float: 'left', background: 'url(\'' + options.image + '\')', width: options.digitWidth});
                digits.push(elem);
                margin(c, -((parseInt(options.startTime[i]) * options.digitHeight * options.digitImages)));
                digits[c].__max = 9;
                switch (options.format[i]) {
                    case'h':
                        digits[c].__max = (c % 2 == 0) ? 2 : 9;
                        if (c % 2 == 0)
                            digits[c].__condmax = 4;
                        break;
                    case'd':
                        digits[c].__max = 9;
                        break;
                    case'm':
                    case's':
                        digits[c].__max = (c % 2 == 0) ? 5 : 9;
                }
                ++c;
            }
            else
                elem = $('<div class="separator"/>').css({float: 'left'}).text(options.startTime[i]);
            where.append(elem)
        }
    };
    var margin = function (elem, val) {
        if (val !== undefined)
            return digits[elem].css({'marginTop': val + 'px'});
        return parseInt(digits[elem].css('marginTop').replace('px', ''));
    };
    var moveStep = function (elem) {
        digits[elem]._digitInitial = -(digits[elem].__max * options.digitHeight * options.digitImages);
        return function _move() {
            mtop = margin(elem) + options.digitHeight;
            if (mtop == options.digitHeight) {
                margin(elem, digits[elem]._digitInitial);
                if (elem < 10 && elem > 8) {
                }
                if (elem > 0)moveStep(elem - 1)(); else {
                    clearInterval(interval);
                    for (var i = 0; i < digits.length; i++)margin(i, 0);
                    options.timerEnd();
                    return;
                }
                if ((elem > 0) && (digits[elem].__condmax !== undefined) && (digits[elem - 1]._digitInitial == margin(elem - 1)))
                    margin(elem, -(digits[elem].__condmax * options.digitHeight * options.digitImages));
                return;
            }
            margin(elem, mtop);
            if (margin(elem) / options.digitHeight % options.digitImages != 0)
                setTimeout(_move, options.stepTime);
            if (mtop == 0)digits[elem].__ismax = true;
        }
    };
    $.extend(options, userOptions);
    this.css({height: options.digitHeight, overflow: 'hidden'});
    createDigits(this);
    interval = setInterval(moveStep(digits.length - 1), 1000);
};
(function (jQuery) {
    jQuery.fn.smartupdater = function (options, callback) {
        return this.each(function () {
            var elem = this;
            elem.settings = jQuery.extend({url: '', type: 'get', data: '', dataType: 'text', minTimeout: 60000, maxTimeout: ((1000 * 60) * 60), multiplier: 2, maxFailedRequests: 10}, options);
            elem.smartupdaterStatus = {};
            elem.smartupdaterStatus.state = '';
            elem.smartupdaterStatus.timeout = 0;
            var es = elem.settings;
            es.prevContent = '';
            es.originalMinTimeout = es.minTimeout;
            es.failedRequests = 0;
            es.response = '';
            function start() {
                $.ajax({url: es.url, type: es.type, data: es.data, dataType: es.dataType, cache: false, success: function (data, statusText, xhr) {
                    if (es.dataType == 'json' && data.smartupdater) {
                        es.originalMinTimeout = data.smartupdater;
                    }
                    if (es.prevContent != xhr.responseText) {
                        es.prevContent = xhr.responseText;
                        es.minTimeout = es.originalMinTimeout;
                        elem.smartupdaterStatus.timeout = es.minTimeout;
                        es.periodicalUpdater = setTimeout(start, es.minTimeout);
                        callback(data);
                    } else if (es.multiplier > 1) {
                        es.minTimeout = (es.minTimeout < es.maxTimeout) ? Math.round(es.minTimeout * es.multiplier) : es.maxTimeout;
                        elem.smartupdaterStatus.timeout = es.minTimeout;
                        es.periodicalUpdater = setTimeout(start, es.minTimeout);
                    } else if (es.multiplier <= 1) {
                        es.minTimeout = es.originalMinTimeout;
                        elem.smartupdaterStatus.timeout = es.minTimeout;
                        es.periodicalUpdater = setTimeout(start, es.minTimeout);
                    }
                    es.failedRequests = 0;
                    elem.smartupdaterStatus.state = 'ON';
                }, error: function () {
                    if (++es.failedRequests < es.maxFailedRequests) {
                        es.periodicalUpdater = setTimeout(start, es.minTimeout);
                        elem.smartupdaterStatus.timeout = es.minTimeout;
                    } else {
                        clearTimeout(es.periodicalUpdater);
                        elem.smartupdaterStatus.state = 'OFF';
                    }
                }});
            }

            es.fnStart = start;
            start();
        });
    };
    jQuery.fn.smartupdaterStop = function () {
        return this.each(function () {
            var elem = this;
            clearTimeout(elem.settings.periodicalUpdater);
            elem.smartupdaterStatus.state = 'OFF';
        });
    };
    jQuery.fn.smartupdaterRestart = function () {
        return this.each(function () {
            var elem = this;
            clearTimeout(elem.settings.periodicalUpdater);
            elem.settings.minTimeout = elem.settings.originalMinTimeout;
            elem.settings.fnStart();
        });
    };
    jQuery.fn.smartupdaterSetTimeout = function (period) {
        return this.each(function () {
            var elem = this;
            clearTimeout(elem.settings.periodicalUpdater);
            this.settings.originalMinTimeout = period;
            this.settings.fnStart();
        });
    };
})(jQuery);
(function ($) {
    var version = '3.09';
    $.taconite = function (xml) {
        processDoc(xml);
    };
    $.taconite.debug = 0;
    $.taconite.defaults = {cdataWrap: 'div'};
    if (typeof $.fn.replace == 'undefined')
        $.fn.replace = function (a) {
            return this.after(a).remove();
        };
    if (typeof $.fn.replaceContent == 'undefined')
        $.fn.replaceContent = function (a) {
            return this.empty().append(a);
        };
    $.expr[':'].taconiteTag = function (a) {
        return a.taconiteTag === 1;
    };
    var _httpData = $.httpData;
    $.httpData = $.taconite.detect = function (xhr, type) {
        var ct = xhr.getResponseHeader('content-type');
        if ($.taconite.debug) {
            log('[AJAX response] content-type: ', ct, ';  status: ', xhr.status, ' ', xhr.statusText, ';  has responseXML: ', xhr.responseXML != null);
            log('type arg: ' + type);
            log('responseXML: ' + xhr.responseXML);
        }
        var data = _httpData(xhr, type);
        if (data && data.documentElement) {
            $.taconite(data);
        }
        else {
            log('jQuery core httpData returned: ' + data);
            log('httpData: response is not XML (or not "valid" XML)');
        }
        return data;
    };
    $.taconite.enableAutoDetection = function (b) {
        $.httpData = b ? $.taconite.detect : _httpData;
    };
    var logCount = 0;

    function log() {
        if (!$.taconite.debug || !window.console || !window.console.log)return;
        if (!logCount++)
            log('Plugin Version: ' + version);
        window.console.log('[taconite] ' + [].join.call(arguments, ''));
    };
    function processDoc(xml) {
        var status = true, ex;
        try {
            if (typeof xml == 'string')
                xml = convert(xml);
            if (!xml) {
                log('$.taconite invoked without valid document; nothing to process');
                return false;
            }
            var root = xml.documentElement.tagName;
            log('XML document root: ', root);
            var taconiteDoc = $('taconite', xml)[0];
            if (!taconiteDoc) {
                log('document does not contain <taconite> element; nothing to process');
                return false;
            }
            $.event.trigger('taconite-begin-notify', [taconiteDoc]);
            status = go(taconiteDoc);
        } catch (e) {
            status = ex = e;
        }
        $.event.trigger('taconite-complete-notify', [xml, !!status, status === true ? null : status]);
        if (ex)throw ex;
    };
    function convert(s) {
        var doc;
        log('attempting string to document conversion');
        try {
            if (window.DOMParser) {
                var parser = new DOMParser();
                doc = parser.parseFromString(s, 'text/xml');
            }
            else {
                doc = $("<xml>")[0];
                doc.async = 'false';
                doc.loadXML(s);
            }
        }
        catch (e) {
            if (window.console && window.console.error)
                window.console.error('[taconite] ERROR parsing XML string for conversion: ' + e);
            throw e;
        }
        var ok = doc && doc.documentElement && doc.documentElement.tagName != 'parsererror';
        log('conversion ', ok ? 'successful!' : 'FAILED');
        return doc;
    };
    function go(xml) {
        var trimHash = {wrap: 1};
        try {
            var t = new Date().getTime();
            process(xml.childNodes);
            $.taconite.lastTime = (new Date().getTime()) - t;
            log('time to process response: ' + $.taconite.lastTime + 'ms');
        } catch (e) {
            if (window.console && window.console.error)
                window.console.error('[taconite] ERROR processing document: ' + e);
            throw e;
        }
        return true;
        function process(commands) {
            var doPostProcess = 0;
            for (var i = 0; i < commands.length; i++) {
                if (commands[i].nodeType != 1)
                    continue;
                var cmdNode = commands[i], cmd = cmdNode.tagName;
                if (cmd == 'eval') {
                    var js = (cmdNode.firstChild ? cmdNode.firstChild.nodeValue : null);
                    log('invoking "eval" command: ', js);
                    if (js)$.globalEval(js);
                    continue;
                }
                var q = cmdNode.getAttribute('select');
                var jq = $(q);
                if (!jq[0]) {
                    log('No matching targets for selector: ', q);
                    continue;
                }
                var cdataWrap = cmdNode.getAttribute('cdataWrap') || $.taconite.defaults.cdataWrap;
                var a = [];
                if (cmdNode.childNodes.length > 0) {
                    doPostProcess = 1;
                    for (var j = 0, els = []; j < cmdNode.childNodes.length; j++)
                        els[j] = createNode(cmdNode.childNodes[j]);
                    a.push(trimHash[cmd] ? cleanse(els) : els);
                }
                var n = cmdNode.getAttribute('name');
                var v = cmdNode.getAttribute('value');
                if (n !== null)a.push(n);
                if (v !== null)a.push(v);
                for (var j = 1; true; j++) {
                    v = cmdNode.getAttribute('arg' + j);
                    if (v === null)
                        break;
                    var n = Number(v);
                    if (v == n)
                        v = n;
                    a.push(v);
                }
                if ($.taconite.debug) {
                    var args = '';
                    if (els)
                        args = '...'; else {
                        for (var k = 0; k < a.length; k++) {
                            if (k > 0)
                                args += ',';
                            var val = a[k];
                            var isString = typeof val == 'string';
                            if (isString)
                                args += '\'';
                            args += val;
                            if (isString)
                                args += '\'';
                        }
                    }
                    log("invoking command: $('", q, "').", cmd, '(' + args + ')');
                }
                jq[cmd].apply(jq, a);
            }
            if (doPostProcess)
                postProcess();
            function postProcess() {
                if ($.browser.mozilla)return;
                $('select:taconiteTag').each(function () {
                    var sel = this;
                    $('option:taconiteTag', this).each(function () {
                        this.setAttribute('selected', 'selected');
                        this.taconiteTag = null;
                        if (sel.type == 'select-one') {
                            var idx = $('option', sel).index(this);
                            sel.selectedIndex = idx;
                        }
                    });
                    this.taconiteTag = null;
                });
            };
            function cleanse(els) {
                for (var i = 0, a = []; i < els.length; i++)
                    if (els[i].nodeType == 1)a.push(els[i]);
                return a;
            };
            function createNode(node) {
                var type = node.nodeType;
                if (type == 1)return createElement(node);
                if (type == 3)return fixTextNode(node.nodeValue);
                if (type == 4)return handleCDATA(node.nodeValue);
                return null;
            };
            function handleCDATA(s) {
                var el = document.createElement(cdataWrap);
                el.innerHTML = s;
                var $el = $(el), $ch = $el.children();
                if ($ch.size() == 1)
                    return $ch[0];
                return el;
            };
            function fixTextNode(s) {
                if ($.browser.msie)s = s.replace(/\n/g, '\r').replace(/\s+/g, ' ');
                return document.createTextNode(s);
            };
            function createElement(node) {
                var e, tag = node.tagName.toLowerCase();
                if ($.browser.msie) {
                    var type = node.getAttribute('type');
                    if (tag == 'table' || type == 'radio' || type == 'checkbox' || tag == 'button' || (tag == 'select' && node.getAttribute('multiple'))) {
                        e = document.createElement('<' + tag + ' ' + copyAttrs(null, node, true) + '>');
                    }
                }
                if (!e) {
                    e = document.createElement(tag);
                    copyAttrs(e, node);
                }
                if ($.browser.msie && tag == 'td') {
                    var colspan = node.getAttribute('colspan');
                    if (colspan)e.colSpan = parseInt(colspan);
                }
                if ($.browser.msie && !e.canHaveChildren) {
                    if (node.childNodes.length > 0)
                        e.text = node.text;
                }
                else {
                    for (var i = 0, max = node.childNodes.length; i < max; i++) {
                        var child = createNode(node.childNodes[i]);
                        if (child)e.appendChild(child);
                    }
                }
                if (!$.browser.mozilla) {
                    if (tag == 'select' || (tag == 'option' && node.getAttribute('selected')))
                        e.taconiteTag = 1;
                }
                return e;
            };
            function copyAttrs(dest, src, inline) {
                for (var i = 0, attr = ''; i < src.attributes.length; i++) {
                    var a = src.attributes[i], n = $.trim(a.name), v = $.trim(a.value);
                    if (inline)attr += (n + '="' + v + '" '); else if (n == 'style') {
                        dest.style.cssText = v;
                        dest.setAttribute(n, v);
                    }
                    else $.attr(dest, n, v);
                }
                return attr;
            };
        };
    };
})(jQuery);
(function ($, window) {
    var
        defaults = {transition: "elastic", speed: 300, width: false, initialWidth: "600", innerWidth: false, maxWidth: false, height: false, initialHeight: "450", innerHeight: false, maxHeight: false, scalePhotos: true, scrolling: true, inline: false, html: false, iframe: false, photo: false, href: false, title: false, rel: false, opacity: 0.9, preloading: true, current: "image {current} of {total}", previous: "previous", next: "next", close: "close", open: false, returnFocus: true, loop: true, slideshow: false, slideshowAuto: true, slideshowSpeed: 2500, slideshowStart: "start slideshow", slideshowStop: "stop slideshow", onOpen: false, onLoad: false, onComplete: false, onCleanup: false, onClosed: false, overlayClose: true, escKey: true, arrowKey: true}, colorbox = 'colorbox', prefix = 'cbox', event_open = prefix + '_open', event_load = prefix + '_load', event_complete = prefix + '_complete', event_cleanup = prefix + '_cleanup', event_closed = prefix + '_closed', event_purge = prefix + '_purge', event_loaded = prefix + '_loaded', isIE = $.browser.msie && !$.support.opacity, isIE6 = isIE && $.browser.version < 7, event_ie6 = prefix + '_IE6', $overlay, $box, $wrap, $content, $topBorder, $leftBorder, $rightBorder, $bottomBorder, $related, $window, $loaded, $loadingBay, $loadingOverlay, $title, $current, $slideshow, $next, $prev, $close, interfaceHeight, interfaceWidth, loadedHeight, loadedWidth, element, index, settings, open, active, closing = false, publicMethod, boxElement = prefix + 'Element';

    function $div(id, css) {
        id = id ? ' id="' + prefix + id + '"' : '';
        css = css ? ' style="' + css + '"' : '';
        return $('<div' + id + css + '/>');
    }

    function setSize(size, dimension) {
        dimension = dimension === 'x' ? $window.width() : $window.height();
        return(typeof size === 'string') ? Math.round((/%/.test(size) ? (dimension / 100) * parseInt(size, 10) : parseInt(size, 10))) : size;
    }

    function isImage(url) {
        return settings.photo || /\.(gif|png|jpg|jpeg|bmp)(?:\?([^#]*))?(?:#(\.*))?$/i.test(url);
    }

    function process(settings) {
        for (var i in settings) {
            if ($.isFunction(settings[i]) && i.substring(0, 2) !== 'on') {
                settings[i] = settings[i].call(element);
            }
        }
        settings.rel = settings.rel || element.rel || 'nofollow';
        settings.href = settings.href || $(element).attr('href');
        settings.title = settings.title || element.title;
        return settings;
    }

    function trigger(event, callback) {
        if (callback) {
            callback.call(element);
        }
        $.event.trigger(event);
    }

    function slideshow() {
        var
            timeOut, className = prefix + "Slideshow_", click = "click." + prefix, start, stop, clear;
        if (settings.slideshow && $related[1]) {
            start = function () {
                $slideshow.text(settings.slideshowStop).unbind(click).bind(event_complete,function () {
                    if (index < $related.length - 1 || settings.loop) {
                        timeOut = setTimeout(publicMethod.next, settings.slideshowSpeed);
                    }
                }).bind(event_load,function () {
                    clearTimeout(timeOut);
                }).one(click + ' ' + event_cleanup, stop);
                $box.removeClass(className + "off").addClass(className + "on");
                timeOut = setTimeout(publicMethod.next, settings.slideshowSpeed);
            };
            stop = function () {
                clearTimeout(timeOut);
                $slideshow.text(settings.slideshowStart).unbind([event_complete, event_load, event_cleanup, click].join(' ')).one(click, start);
                $box.removeClass(className + "on").addClass(className + "off");
            };
            if (settings.slideshowAuto) {
                start();
            } else {
                stop();
            }
        }
    }

    function launch(elem) {
        if (!closing) {
            element = elem;
            settings = process($.extend({}, $.data(element, colorbox)));
            $related = $(element);
            index = 0;
            if (settings.rel !== 'nofollow') {
                $related = $('.' + boxElement).filter(function () {
                    var relRelated = $.data(this, colorbox).rel || this.rel;
                    return(relRelated === settings.rel);
                });
                index = $related.index(element);
                if (index === -1) {
                    $related = $related.add(element);
                    index = $related.length - 1;
                }
            }
            if (!open) {
                open = active = true;
                $box.show();
                if (settings.returnFocus) {
                    try {
                        element.blur();
                        $(element).one(event_closed, function () {
                            try {
                                this.focus();
                            } catch (e) {
                            }
                        });
                    } catch (e) {
                    }
                }
                $overlay.css({"opacity": +settings.opacity, "cursor": settings.overlayClose ? "pointer" : "auto"}).show();
                settings.w = setSize(settings.initialWidth, 'x');
                settings.h = setSize(settings.initialHeight, 'y');
                publicMethod.position(0);
                if (isIE6) {
                    $window.bind('resize.' + event_ie6 + ' scroll.' + event_ie6,function () {
                        $overlay.css({width: $window.width(), height: $window.height(), top: $window.scrollTop(), left: $window.scrollLeft()});
                    }).trigger('scroll.' + event_ie6);
                }
                trigger(event_open, settings.onOpen);
                $current.add($prev).add($next).add($slideshow).add($title).hide();
                $close.html(settings.close).show();
            }
            publicMethod.load(true);
        }
    }

    publicMethod = $.fn[colorbox] = $[colorbox] = function (options, callback) {
        var $this = this, autoOpen;
        if (!$this[0] && $this.selector) {
            return $this;
        }
        options = options || {};
        if (callback) {
            options.onComplete = callback;
        }
        if (!$this[0] || $this.selector === undefined) {
            $this = $('<a/>');
            options.open = true;
        }
        $this.each(function () {
            $.data(this, colorbox, $.extend({}, $.data(this, colorbox) || defaults, options));
            $(this).addClass(boxElement);
        });
        autoOpen = options.open;
        if ($.isFunction(autoOpen)) {
            autoOpen = autoOpen.call($this);
        }
        if (autoOpen) {
            launch($this[0]);
        }
        return $this;
    };
    publicMethod.init = function () {
        $window = $(window);
        $box = $div().attr({id: colorbox, 'class': isIE ? prefix + 'IE' : ''});
        $overlay = $div("Overlay", isIE6 ? 'position:absolute' : '').hide();
        $wrap = $div("Wrapper");
        $content = $div("Content").append($loaded = $div("LoadedContent", 'width:0; height:0; overflow:hidden'), $loadingOverlay = $div("LoadingOverlay").add($div("LoadingGraphic")), $title = $div("Title"), $current = $div("Current"), $next = $div("Next"), $prev = $div("Previous"), $slideshow = $div("Slideshow").bind(event_open, slideshow), $close = $div("Close"));
        $wrap.append($div().append($div("TopLeft"), $topBorder = $div("TopCenter"), $div("TopRight")), $div(false, 'clear:left').append($leftBorder = $div("MiddleLeft"), $content, $rightBorder = $div("MiddleRight")), $div(false, 'clear:left').append($div("BottomLeft"), $bottomBorder = $div("BottomCenter"), $div("BottomRight"))).children().children().css({'float': 'left'});
        $loadingBay = $div(false, 'position:absolute; width:9999px; visibility:hidden; display:none');
        $('body').prepend($overlay, $box.append($wrap, $loadingBay));
        $content.children().hover(function () {
            $(this).addClass('hover');
        },function () {
            $(this).removeClass('hover');
        }).addClass('hover');
        interfaceHeight = $topBorder.height() + $bottomBorder.height() + $content.outerHeight(true) - $content.height();
        interfaceWidth = $leftBorder.width() + $rightBorder.width() + $content.outerWidth(true) - $content.width();
        loadedHeight = $loaded.outerHeight(true);
        loadedWidth = $loaded.outerWidth(true);
        $box.css({"padding-bottom": interfaceHeight, "padding-right": interfaceWidth}).hide();
        $next.click(publicMethod.next);
        $prev.click(publicMethod.prev);
        $close.click(publicMethod.close);
        $content.children().removeClass('hover');
        $('.' + boxElement).live('click', function (e) {
            if (!((e.button !== 0 && typeof e.button !== 'undefined') || e.ctrlKey || e.shiftKey || e.altKey)) {
                e.preventDefault();
                launch(this);
            }
        });
        $overlay.click(function () {
            if (settings.overlayClose) {
                publicMethod.close();
            }
        });
        $(document).bind("keydown", function (e) {
            if (open && settings.escKey && e.keyCode === 27) {
                e.preventDefault();
                publicMethod.close();
            }
            if (open && settings.arrowKey && !active && $related[1]) {
                if (e.keyCode === 37 && (index || settings.loop)) {
                    e.preventDefault();
                    $prev.click();
                } else if (e.keyCode === 39 && (index < $related.length - 1 || settings.loop)) {
                    e.preventDefault();
                    $next.click();
                }
            }
        });
    };
    publicMethod.remove = function () {
        $box.add($overlay).remove();
        $('.' + boxElement).die('click').removeData(colorbox).removeClass(boxElement);
    };
    publicMethod.position = function (speed, loadedCallback) {
        var
            animate_speed, posTop = Math.max(document.documentElement.clientHeight - settings.h - loadedHeight - interfaceHeight, 0) / 2 + $window.scrollTop(), posLeft = Math.max($window.width() - settings.w - loadedWidth - interfaceWidth, 0) / 2 + $window.scrollLeft();
        animate_speed = ($box.width() === settings.w + loadedWidth && $box.height() === settings.h + loadedHeight) ? 0 : speed;
        $wrap[0].style.width = $wrap[0].style.height = "9999px";
        function modalDimensions(that) {
            $topBorder[0].style.width = $bottomBorder[0].style.width = $content[0].style.width = that.style.width;
            $loadingOverlay[0].style.height = $loadingOverlay[1].style.height = $content[0].style.height = $leftBorder[0].style.height = $rightBorder[0].style.height = that.style.height;
        }

        $box.dequeue().animate({width: settings.w + loadedWidth, height: settings.h + loadedHeight, top: posTop, left: posLeft}, {duration: animate_speed, complete: function () {
            modalDimensions(this);
            active = false;
            $wrap[0].style.width = (settings.w + loadedWidth + interfaceWidth) + "px";
            $wrap[0].style.height = (settings.h + loadedHeight + interfaceHeight) + "px";
            if (loadedCallback) {
                loadedCallback();
            }
        }, step: function () {
            modalDimensions(this);
        }});
    };
    publicMethod.resize = function (options) {
        if (open) {
            options = options || {};
            if (options.width) {
                settings.w = setSize(options.width, 'x') - loadedWidth - interfaceWidth;
            }
            if (options.innerWidth) {
                settings.w = setSize(options.innerWidth, 'x');
            }
            $loaded.css({width: settings.w});
            if (options.height) {
                settings.h = setSize(options.height, 'y') - loadedHeight - interfaceHeight;
            }
            if (options.innerHeight) {
                settings.h = setSize(options.innerHeight, 'y');
            }
            if (!options.innerHeight && !options.height) {
                var $child = $loaded.wrapInner("<div style='overflow:auto'></div>").children();
                settings.h = $child.height();
                $child.replaceWith($child.children());
            }
            $loaded.css({height: settings.h});
            publicMethod.position(settings.transition === "none" ? 0 : settings.speed);
        }
    };
    publicMethod.prep = function (object) {
        if (!open) {
            return;
        }
        var photo, speed = settings.transition === "none" ? 0 : settings.speed;
        $window.unbind('resize.' + prefix);
        $loaded.remove();
        $loaded = $div('LoadedContent').html(object);
        function getWidth() {
            settings.w = settings.w || $loaded.width();
            settings.w = settings.mw && settings.mw < settings.w ? settings.mw : settings.w;
            return settings.w;
        }

        function getHeight() {
            settings.h = settings.h || $loaded.height();
            settings.h = settings.mh && settings.mh < settings.h ? settings.mh : settings.h;
            return settings.h;
        }

        $loaded.hide().appendTo($loadingBay.show()).css({width: getWidth(), overflow: settings.scrolling ? 'auto' : 'hidden'}).css({height: getHeight()}).prependTo($content);
        $loadingBay.hide();
        $('#' + prefix + 'Photo').css({cssFloat: 'none', marginLeft: 'auto', marginRight: 'auto'});
        if (isIE6) {
            $('select').not($box.find('select')).filter(function () {
                return this.style.visibility !== 'hidden';
            }).css({'visibility': 'hidden'}).one(event_cleanup, function () {
                this.style.visibility = 'inherit';
            });
        }
        function setPosition(s) {
            var prev, prevSrc, next, nextSrc, total = $related.length, loop = settings.loop;
            publicMethod.position(s, function () {
                function defilter() {
                    if (isIE) {
                        $box[0].style.removeAttribute("filter");
                    }
                }

                if (!open) {
                    return;
                }
                if (isIE) {
                    if (photo) {
                        $loaded.fadeIn(100);
                    }
                }
                $loaded.show();
                trigger(event_loaded);
                $title.show().html(settings.title);
                if (total > 1) {
                    if (typeof settings.current === "string") {
                        $current.html(settings.current.replace(/\{current\}/, index + 1).replace(/\{total\}/, total)).show();
                    }
                    $next[(loop || index < total - 1) ? "show" : "hide"]().html(settings.next);
                    $prev[(loop || index) ? "show" : "hide"]().html(settings.previous);
                    prev = index ? $related[index - 1] : $related[total - 1];
                    next = index < total - 1 ? $related[index + 1] : $related[0];
                    if (settings.slideshow) {
                        $slideshow.show();
                    }
                    if (settings.preloading) {
                        nextSrc = $.data(next, colorbox).href || next.href;
                        prevSrc = $.data(prev, colorbox).href || prev.href;
                        nextSrc = $.isFunction(nextSrc) ? nextSrc.call(next) : nextSrc;
                        prevSrc = $.isFunction(prevSrc) ? prevSrc.call(prev) : prevSrc;
                        if (isImage(nextSrc)) {
                            $('<img/>')[0].src = nextSrc;
                        }
                        if (isImage(prevSrc)) {
                            $('<img/>')[0].src = prevSrc;
                        }
                    }
                }
                $loadingOverlay.hide();
                if (settings.transition === 'fade') {
                    $box.fadeTo(speed, 1, function () {
                        defilter();
                    });
                } else {
                    defilter();
                }
                $window.bind('resize.' + prefix, function () {
                    publicMethod.position(0);
                });
                trigger(event_complete, settings.onComplete);
            });
        }

        if (settings.transition === 'fade') {
            $box.fadeTo(speed, 0, function () {
                setPosition(0);
            });
        } else {
            setPosition(speed);
        }
    };
    publicMethod.load = function (launched) {
        var href, img, setResize, prep = publicMethod.prep;
        active = true;
        element = $related[index];
        if (!launched) {
            settings = process($.extend({}, $.data(element, colorbox)));
        }
        trigger(event_purge);
        trigger(event_load, settings.onLoad);
        settings.h = settings.height ? setSize(settings.height, 'y') - loadedHeight - interfaceHeight : settings.innerHeight && setSize(settings.innerHeight, 'y');
        settings.w = settings.width ? setSize(settings.width, 'x') - loadedWidth - interfaceWidth : settings.innerWidth && setSize(settings.innerWidth, 'x');
        settings.mw = settings.w;
        settings.mh = settings.h;
        if (settings.maxWidth) {
            settings.mw = setSize(settings.maxWidth, 'x') - loadedWidth - interfaceWidth;
            settings.mw = settings.w && settings.w < settings.mw ? settings.w : settings.mw;
        }
        if (settings.maxHeight) {
            settings.mh = setSize(settings.maxHeight, 'y') - loadedHeight - interfaceHeight;
            settings.mh = settings.h && settings.h < settings.mh ? settings.h : settings.mh;
        }
        href = settings.href;
        $loadingOverlay.show();
        if (settings.inline) {
            $div().hide().insertBefore($(href)[0]).one(event_purge, function () {
                $(this).replaceWith($loaded.children());
            });
            prep($(href));
        } else if (settings.iframe) {
            $box.one(event_loaded, function () {
                var iframe = $("<iframe frameborder='0' style='width:100%; height:100%; border:0; display:block'/>")[0];
                iframe.name = prefix + (+new Date());
                iframe.src = settings.href;
                if (!settings.scrolling) {
                    iframe.scrolling = "no";
                }
                if (isIE) {
                    iframe.allowtransparency = "true";
                }
                $(iframe).appendTo($loaded).one(event_purge, function () {
                    iframe.src = "//about:blank";
                });
            });
            prep(" ");
        } else if (settings.html) {
            prep(settings.html);
        } else if (isImage(href)) {
            img = new Image();
            img.onload = function () {
                var percent;
                img.onload = null;
                img.id = prefix + 'Photo';
                $(img).css({border: 'none', display: 'block', cssFloat: 'left'});
                if (settings.scalePhotos) {
                    setResize = function () {
                        img.height -= img.height * percent;
                        img.width -= img.width * percent;
                    };
                    if (settings.mw && img.width > settings.mw) {
                        percent = (img.width - settings.mw) / img.width;
                        setResize();
                    }
                    if (settings.mh && img.height > settings.mh) {
                        percent = (img.height - settings.mh) / img.height;
                        setResize();
                    }
                }
                if (settings.h) {
                    img.style.marginTop = Math.max(settings.h - img.height, 0) / 2 + 'px';
                }
                if ($related[1] && (index < $related.length - 1 || settings.loop)) {
                    $(img).css({cursor: 'pointer'}).click(publicMethod.next);
                }
                if (isIE) {
                    img.style.msInterpolationMode = 'bicubic';
                }
                setTimeout(function () {
                    prep(img);
                }, 1);
            };
            setTimeout(function () {
                img.src = href;
            }, 1);
        } else if (href) {
            $loadingBay.load(href, function (data, status, xhr) {
                prep(status === 'error' ? 'Request unsuccessful: ' + xhr.statusText : $(this).children());
            });
        }
    };
    publicMethod.next = function () {
        if (!active) {
            index = index < $related.length - 1 ? index + 1 : 0;
            publicMethod.load();
        }
    };
    publicMethod.prev = function () {
        if (!active) {
            index = index ? index - 1 : $related.length - 1;
            publicMethod.load();
        }
    };
    publicMethod.close = function () {
        if (open && !closing) {
            closing = true;
            open = false;
            trigger(event_cleanup, settings.onCleanup);
            $window.unbind('.' + prefix + ' .' + event_ie6);
            $overlay.fadeTo('fast', 0);
            $box.stop().fadeTo('fast', 0, function () {
                trigger(event_purge);
                $loaded.remove();
                $box.add($overlay).css({'opacity': 1, cursor: 'auto'}).hide();
                setTimeout(function () {
                    closing = false;
                    trigger(event_closed, settings.onClosed);
                }, 1);
            });
        }
    };
    publicMethod.element = function () {
        return $(element);
    };
    publicMethod.settings = defaults;
    $(publicMethod.init);
}(jQuery, this));
;
(function ($) {
    var methods = {init: function (settings) {
        return this.each(function () {
            var self = this, $this = $(self).empty();
            self.opt = $.extend(true, {}, $.fn.raty.defaults, settings);
            $this.data('settings', self.opt);
            self.opt.number = methods.between(self.opt.number, 0, 20);
            if (self.opt.path.substring(self.opt.path.length - 1, self.opt.path.length) != '/') {
                self.opt.path += '/';
            }
            if (typeof self.opt.score == 'function') {
                self.opt.score = self.opt.score.call(self);
            }
            if (self.opt.score) {
                self.opt.score = methods.between(self.opt.score, 0, self.opt.number);
            }
            for (var i = 1; i <= self.opt.number; i++) {
                $('<img />', {src: self.opt.path + ((!self.opt.score || self.opt.score < i) ? self.opt.starOff : self.opt.starOn), alt: i, title: (i <= self.opt.hints.length && self.opt.hints[i - 1] !== null) ? self.opt.hints[i - 1] : i}).appendTo(self);
                if (self.opt.space) {
                    $this.append((i < self.opt.number) ? '&#160;' : '');
                }
            }
            self.stars = $this.children('img:not(".raty-cancel")');
            self.score = $('<input />', {type: 'hidden', name: self.opt.scoreName}).appendTo(self);
            if (self.opt.score && self.opt.score > 0) {
                self.score.val(self.opt.score);
                methods.roundStar.call(self, self.opt.score);
            }
            if (self.opt.iconRange) {
                methods.fill.call(self, self.opt.score);
            }
            methods.setTarget.call(self, self.opt.score, self.opt.targetKeep);
            var space = self.opt.space ? 4 : 0, width = self.opt.width || (self.opt.number * self.opt.size + self.opt.number * space);
            if (self.opt.cancel) {
                self.cancel = $('<img />', {src: self.opt.path + self.opt.cancelOff, alt: 'x', title: self.opt.cancelHint, 'class': 'raty-cancel'});
                if (self.opt.cancelPlace == 'left') {
                    $this.prepend('&#160;').prepend(self.cancel);
                } else {
                    $this.append('&#160;').append(self.cancel);
                }
                width += (self.opt.size + space);
            }
            if (self.opt.readOnly) {
                methods.fixHint.call(self);
                if (self.cancel) {
                    self.cancel.hide();
                }
            } else {
                $this.css('cursor', 'pointer');
                methods.bindAction.call(self);
            }
            $this.css('width', width);
        });
    }, between: function (value, min, max) {
        return Math.min(Math.max(parseFloat(value), min), max);
    }, bindAction: function () {
        var self = this, $this = $(self);
        $this.mouseleave(function () {
            var score = self.score.val() || undefined;
            methods.initialize.call(self, score);
            methods.setTarget.call(self, score, self.opt.targetKeep);
            if (self.opt.mouseover) {
                self.opt.mouseover.call(self, score);
            }
        });
        var action = self.opt.half ? 'mousemove' : 'mouseover';
        if (self.opt.cancel) {
            self.cancel.mouseenter(function () {
                $(this).attr('src', self.opt.path + self.opt.cancelOn);
                self.stars.attr('src', self.opt.path + self.opt.starOff);
                methods.setTarget.call(self, null, true);
                if (self.opt.mouseover) {
                    self.opt.mouseover.call(self, null);
                }
            }).mouseleave(function () {
                $(this).attr('src', self.opt.path + self.opt.cancelOff);
                if (self.opt.mouseover) {
                    self.opt.mouseover.call(self, self.score.val() || null);
                }
            }).click(function (evt) {
                self.score.removeAttr('value');
                if (self.opt.click) {
                    self.opt.click.call(self, null, evt);
                }
            });
        }
        self.stars.bind(action,function (evt) {
            var value = parseInt(this.alt, 10);
            if (self.opt.half) {
                var position = parseFloat((evt.pageX - $(this).offset().left) / self.opt.size), diff = (position > .5) ? 1 : .5;
                value = parseFloat(this.alt) - 1 + diff;
                methods.fill.call(self, value);
                if (self.opt.precision) {
                    value = value - diff + position;
                }
                methods.showHalf.call(self, value);
            } else {
                methods.fill.call(self, value);
            }
            $this.data('score', value);
            methods.setTarget.call(self, value, true);
            if (self.opt.mouseover) {
                self.opt.mouseover.call(self, value, evt);
            }
        }).click(function (evt) {
                self.score.val((self.opt.half || self.opt.precision) ? $this.data('score') : this.alt);
                if (self.opt.click) {
                    self.opt.click.call(self, self.score.val(), evt);
                }
            });
    }, cancel: function (isClick) {
        return $(this).each(function () {
            var self = this, $this = $(self);
            if ($this.data('readonly') === true) {
                return this;
            }
            if (isClick) {
                methods.click.call(self, null);
            } else {
                methods.score.call(self, null);
            }
            self.score.removeAttr('value');
        });
    }, click: function (score) {
        return $(this).each(function () {
            if ($(this).data('readonly') === true) {
                return this;
            }
            methods.initialize.call(this, score);
            if (this.opt.click) {
                this.opt.click.call(this, score);
            } else {
                methods.error.call(this, 'you must add the "click: function(score, evt) { }" callback.');
            }
            methods.setTarget.call(this, score, true);
        });
    }, error: function (message) {
        $(this).html(message);
        $.error(message);
    }, fill: function (score) {
        var self = this, number = self.stars.length, count = 0, $star, star, icon;
        for (var i = 1; i <= number; i++) {
            $star = self.stars.eq(i - 1);
            if (self.opt.iconRange && self.opt.iconRange.length > count) {
                star = self.opt.iconRange[count];
                if (self.opt.single) {
                    icon = (i == score) ? (star.on || self.opt.starOn) : (star.off || self.opt.starOff);
                } else {
                    icon = (i <= score) ? (star.on || self.opt.starOn) : (star.off || self.opt.starOff);
                }
                if (i <= star.range) {
                    $star.attr('src', self.opt.path + icon);
                }
                if (i == star.range) {
                    count++;
                }
            } else {
                if (self.opt.single) {
                    icon = (i == score) ? self.opt.starOn : self.opt.starOff;
                } else {
                    icon = (i <= score) ? self.opt.starOn : self.opt.starOff;
                }
                $star.attr('src', self.opt.path + icon);
            }
        }
    }, fixHint: function () {
        var $this = $(this), score = parseInt(this.score.val(), 10), hint = this.opt.noRatedMsg;
        if (!isNaN(score) && score > 0) {
            hint = (score <= this.opt.hints.length && this.opt.hints[score - 1] !== null) ? this.opt.hints[score - 1] : score;
        }
        $this.data('readonly', true).css('cursor', 'default').attr('title', hint);
        this.score.attr('readonly', 'readonly');
        this.stars.attr('title', hint);
    }, getScore: function () {
        var score = [], value;
        $(this).each(function () {
            value = this.score.val();
            score.push(value ? parseFloat(value) : undefined);
        });
        return(score.length > 1) ? score : score[0];
    }, readOnly: function (isReadOnly) {
        return this.each(function () {
            var $this = $(this);
            if ($this.data('readonly') === isReadOnly) {
                return this;
            }
            if (this.cancel) {
                if (isReadOnly) {
                    this.cancel.hide();
                } else {
                    this.cancel.show();
                }
            }
            if (isReadOnly) {
                $this.unbind();
                $this.children('img').unbind();
                methods.fixHint.call(this);
            } else {
                methods.bindAction.call(this);
                methods.unfixHint.call(this);
            }
            $this.data('readonly', isReadOnly);
        });
    }, reload: function () {
        return methods.set.call(this, {});
    }, roundStar: function (score) {
        var diff = (score - Math.floor(score)).toFixed(2);
        if (diff > this.opt.round.down) {
            var icon = this.opt.starOn;
            if (diff < this.opt.round.up && this.opt.halfShow) {
                icon = this.opt.starHalf;
            } else if (diff < this.opt.round.full) {
                icon = this.opt.starOff;
            }
            this.stars.eq(Math.ceil(score) - 1).attr('src', this.opt.path + icon);
        }
    }, score: function () {
        return arguments.length ? methods.setScore.apply(this, arguments) : methods.getScore.call(this);
    }, set: function (settings) {
        this.each(function () {
            var $this = $(this), actual = $this.data('settings'), clone = $this.clone().removeAttr('style').insertBefore($this);
            $this.remove();
            clone.raty($.extend(actual, settings));
        });
        return $(this.selector);
    }, setScore: function (score) {
        return $(this).each(function () {
            if ($(this).data('readonly') === true) {
                return this;
            }
            methods.initialize.call(this, score);
            methods.setTarget.call(this, score, true);
        });
    }, setTarget: function (value, isKeep) {
        if (this.opt.target) {
            var $target = $(this.opt.target);
            if ($target.length == 0) {
                methods.error.call(this, 'target selector invalid or missing!');
            }
            var score = value;
            if (!isKeep || score === undefined) {
                score = this.opt.targetText;
            } else {
                if (this.opt.targetType == 'hint') {
                    score = (score === null && this.opt.cancel) ? this.opt.cancelHint : this.opt.hints[Math.ceil(score - 1)];
                } else {
                    score = this.opt.precision ? parseFloat(score).toFixed(1) : parseInt(score, 10);
                }
            }
            if (this.opt.targetFormat.indexOf('{score}') < 0) {
                methods.error.call(this, 'template "{score}" missing!');
            }
            if (value !== null) {
                score = this.opt.targetFormat.toString().replace('{score}', score);
            }
            if ($target.is(':input')) {
                $target.val(score);
            } else {
                $target.html(score);
            }
        }
    }, showHalf: function (score) {
        var diff = (score - Math.floor(score)).toFixed(1);
        if (diff > 0 && diff < .6) {
            this.stars.eq(Math.ceil(score) - 1).attr('src', this.opt.path + this.opt.starHalf);
        }
    }, initialize: function (score) {
        score = !score ? 0 : methods.between(score, 0, this.opt.number);
        methods.fill.call(this, score);
        if (score > 0) {
            if (this.opt.halfShow) {
                methods.roundStar.call(this, score);
            }
            this.score.val(score);
        }
    }, unfixHint: function () {
        for (var i = 0; i < this.opt.number; i++) {
            this.stars.eq(i).attr('title', (i < this.opt.hints.length && this.opt.hints[i] !== null) ? this.opt.hints[i] : i);
        }
        $(this).data('readonly', false).css('cursor', 'pointer').removeAttr('title');
        this.score.attr('readonly', 'readonly');
    }};
    $.fn.raty = function (method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist!');
        }
    };
    $.fn.raty.defaults = {cancel: false, cancelHint: 'cancel this rating!', cancelOff: 'cancel-off.png', cancelOn: 'cancel-on.png', cancelPlace: 'left', click: undefined, half: false, halfShow: true, hints: ['bad', 'poor', 'regular', 'good', 'gorgeous'], iconRange: undefined, mouseover: undefined, noRatedMsg: 'not rated yet', number: 5, path: 'img/', precision: false, round: {down: .25, full: .6, up: .76}, readOnly: false, score: undefined, scoreName: 'score', single: false, size: 16, space: true, starHalf: 'star-half.png', starOff: 'star-off.png', starOn: 'star-on.png', target: undefined, targetFormat: '{score}', targetKeep: false, targetText: '', targetType: 'hint', width: undefined};
})(jQuery);
(function ($) {
    $.fn.popupWindow = function (instanceSettings) {
        return this.each(function () {
            $(this).click(function () {
                $.fn.popupWindow.defaultSettings = {centerBrowser: 0, centerScreen: 0, height: 500, left: 0, location: 0, menubar: 0, resizable: 0, scrollbars: 0, status: 0, width: 500, windowName: null, windowURL: null, top: 0, toolbar: 0};
                settings = $.extend({}, $.fn.popupWindow.defaultSettings, instanceSettings || {});
                var windowFeatures = 'height=' + settings.height + ',width=' + settings.width + ',toolbar=' + settings.toolbar + ',scrollbars=' + settings.scrollbars + ',status=' + settings.status + ',resizable=' + settings.resizable + ',location=' + settings.location + ',menuBar=' + settings.menubar;
                settings.windowName = this.name || settings.windowName;
                settings.windowURL = this.href || settings.windowURL;
                var centeredY, centeredX;
                if (settings.centerBrowser) {
                    if ($.browser.msie) {
                        centeredY = (window.screenTop - 120) + ((((document.documentElement.clientHeight + 120) / 2) - (settings.height / 2)));
                        centeredX = window.screenLeft + ((((document.body.offsetWidth + 20) / 2) - (settings.width / 2)));
                    } else {
                        centeredY = window.screenY + (((window.outerHeight / 2) - (settings.height / 2)));
                        centeredX = window.screenX + (((window.outerWidth / 2) - (settings.width / 2)));
                    }
                    window.open(settings.windowURL, settings.windowName, windowFeatures + ',left=' + centeredX + ',top=' + centeredY).focus();
                } else if (settings.centerScreen) {
                    centeredY = (screen.height - settings.height) / 2;
                    centeredX = (screen.width - settings.width) / 2;
                    window.open(settings.windowURL, settings.windowName, windowFeatures + ',left=' + centeredX + ',top=' + centeredY).focus();
                } else {
                    window.open(settings.windowURL, settings.windowName, windowFeatures + ',left=' + settings.left + ',top=' + settings.top).focus();
                }
                return false;
            });
        });
    };
})(jQuery);
(function (jQuery) {
    var log = function (object) {
        if (typeof console == 'object')
            console.log(object); else if (typeof opera == 'object')
            opera.postError(object); else
            alert(object);
    }
    jQuery.fn.log = log;
    jQuery.log = log;
})(jQuery);
(function ($) {
    $.fn.marquee = function (klass) {
        var newMarquee = [], last = this.length;

        function getReset(newDir, marqueeRedux, marqueeState) {
            var behavior = marqueeState.behavior, width = marqueeState.width, dir = marqueeState.dir;
            var r = 0;
            if (behavior == 'alternate') {
                r = newDir == 1 ? marqueeRedux[marqueeState.widthAxis] - (width * 2) : width;
            } else if (behavior == 'slide') {
                if (newDir == -1) {
                    r = dir == -1 ? marqueeRedux[marqueeState.widthAxis] : width;
                } else {
                    r = dir == -1 ? marqueeRedux[marqueeState.widthAxis] - (width * 2) : 0;
                }
            } else {
                r = newDir == -1 ? marqueeRedux[marqueeState.widthAxis] : 0;
            }
            return r;
        }

        function animateMarquee() {
            var i = newMarquee.length, marqueeRedux = null, $marqueeRedux = null, marqueeState = {}, newMarqueeList = [], hitedge = false;
            while (i--) {
                marqueeRedux = newMarquee[i];
                $marqueeRedux = $(marqueeRedux);
                marqueeState = $marqueeRedux.data('marqueeState');
                if ($marqueeRedux.data('paused') !== true) {
                    marqueeRedux[marqueeState.axis] += (marqueeState.scrollamount * marqueeState.dir);
                    hitedge = marqueeState.dir == -1 ? marqueeRedux[marqueeState.axis] <= getReset(marqueeState.dir * -1, marqueeRedux, marqueeState) : marqueeRedux[marqueeState.axis] >= getReset(marqueeState.dir * -1, marqueeRedux, marqueeState);
                    if ((marqueeState.behavior == 'scroll' && marqueeState.last == marqueeRedux[marqueeState.axis]) || (marqueeState.behavior == 'alternate' && hitedge && marqueeState.last != -1) || (marqueeState.behavior == 'slide' && hitedge && marqueeState.last != -1)) {
                        if (marqueeState.behavior == 'alternate') {
                            marqueeState.dir *= -1;
                        }
                        marqueeState.last = -1;
                        $marqueeRedux.trigger('stop');
                        marqueeState.loops--;
                        if (marqueeState.loops === 0) {
                            if (marqueeState.behavior != 'slide') {
                                marqueeRedux[marqueeState.axis] = getReset(marqueeState.dir, marqueeRedux, marqueeState);
                            } else {
                                marqueeRedux[marqueeState.axis] = getReset(marqueeState.dir * -1, marqueeRedux, marqueeState);
                            }
                            $marqueeRedux.trigger('end');
                        } else {
                            newMarqueeList.push(marqueeRedux);
                            $marqueeRedux.trigger('start');
                            marqueeRedux[marqueeState.axis] = getReset(marqueeState.dir, marqueeRedux, marqueeState);
                        }
                    } else {
                        newMarqueeList.push(marqueeRedux);
                    }
                    marqueeState.last = marqueeRedux[marqueeState.axis];
                    $marqueeRedux.data('marqueeState', marqueeState);
                } else {
                    newMarqueeList.push(marqueeRedux);
                }
            }
            newMarquee = newMarqueeList;
            if (newMarquee.length) {
                setTimeout(animateMarquee, 25);
            }
        }

        this.each(function (i) {
            var $marquee = $(this), width = $marquee.attr('width') || $marquee.width(), height = $marquee.attr('height') || $marquee.height(), $marqueeRedux = $marquee.after('<div ' + (klass ? 'class="' + klass + '" ' : '') + 'style="display: block-inline; width: ' + width + 'px; height: ' + height + 'px; overflow: hidden;"><div style="float: left; white-space: nowrap;">' + $marquee.html() + '</div></div>').next(), marqueeRedux = $marqueeRedux.get(0), hitedge = 0, direction = ($marquee.attr('direction') || 'left').toLowerCase(), marqueeState = {dir: /down|right/.test(direction) ? -1 : 1, axis: /left|right/.test(direction) ? 'scrollLeft' : 'scrollTop', widthAxis: /left|right/.test(direction) ? 'scrollWidth' : 'scrollHeight', last: -1, loops: $marquee.attr('loop') || -1, scrollamount: $marquee.attr('scrollamount') || this.scrollAmount || 2, behavior: ($marquee.attr('behavior') || 'scroll').toLowerCase(), width: /left|right/.test(direction) ? width : height};
            if ($marquee.attr('loop') == -1 && marqueeState.behavior == 'slide') {
                marqueeState.loops = 1;
            }
            $marquee.remove();
            if (/left|right/.test(direction)) {
                $marqueeRedux.find('> div').css('padding', '0 ' + width + 'px');
            } else {
                $marqueeRedux.find('> div').css('padding', height + 'px 0');
            }
            $marqueeRedux.bind('stop',function () {
                $marqueeRedux.data('paused', true);
            }).bind('pause',function () {
                $marqueeRedux.data('paused', true);
            }).bind('start',function () {
                $marqueeRedux.data('paused', false);
            }).bind('unpause',function () {
                $marqueeRedux.data('paused', false);
            }).data('marqueeState', marqueeState);
            newMarquee.push(marqueeRedux);
            marqueeRedux[marqueeState.axis] = getReset(marqueeState.dir, marqueeRedux, marqueeState);
            $marqueeRedux.trigger('start');
            if (i + 1 == last) {
                animateMarquee();
            }
        });
        return $(newMarquee);
    };
}(jQuery));
{
}
(function ($) {
    var
        _native = false, is_canvasTextSupported, measureContext, measureText, info_identifier = "shorten-info", options_identifier = "shorten-options";
    $.fn.shorten = function () {
        var userOptions = {}, args = arguments, func = args.callee
        if (args.length) {
            if (args[0].constructor == Object) {
                userOptions = args[0];
            } else if (args[0] == "options") {
                return $(this).eq(0).data(options_identifier);
            } else {
                userOptions = {width: parseInt(args[0]), tail: args[1]}
            }
        }
        this.css("visibility", "hidden");
        var options = $.extend({}, func.defaults, userOptions);
        return this.each(function () {
            var
                $this = $(this), text = $this.text(), numChars = text.length, targetWidth, tailText = $("<span/>").html(options.tail).text(), tailWidth, info = {shortened: false, textOverflow: false}
            if ($this.css("float") != "none") {
                targetWidth = options.width || $this.width();
            } else {
                targetWidth = options.width || $this.parent().width();
            }
            if (targetWidth < 0) {
                return true;
            }
            $this.data(options_identifier, options);
            this.style.display = "block";
            this.style.whiteSpace = "nowrap";
            if (is_canvasTextSupported) {
                measureContext = measureText_initCanvas.call(this);
                measureText = measureText_canvas;
            } else {
                measureContext = measureText_initTable.call(this);
                measureText = measureText_table;
            }
            var origLength = measureText.call(this, text, measureContext);
            if (origLength < targetWidth) {
                $this.text(text);
                this.style.visibility = "visible";
                $this.data(info_identifier, info);
                return true;
            }
            if (options.tooltip) {
                this.setAttribute("title", text);
            }
            if (func._native && !userOptions.width) {
                var rendered_tail = $("<span>" + options.tail + "</span>").text();
                if (rendered_tail.length == 1 && rendered_tail.charCodeAt(0) == 8230) {
                    $this.text(text);
                    this.style.overflow = "hidden";
                    this.style[func._native] = "ellipsis";
                    this.style.visibility = "visible";
                    info.shortened = true;
                    info.textOverflow = "ellipsis";
                    $this.data(info_identifier, info);
                    return true;
                }
            }
            tailWidth = measureText.call(this, tailText, measureContext);
            targetWidth = targetWidth - tailWidth;
            var safeGuess = targetWidth * 1.15;
            if (origLength - safeGuess > 0) {
                var cut_ratio = safeGuess / origLength, num_guessText_chars = Math.ceil(numChars * cut_ratio), guessText = text.substring(0, num_guessText_chars), guessTextLength = measureText.call(this, guessText, measureContext);
                if (guessTextLength > targetWidth) {
                    text = guessText;
                    numChars = text.length;
                }
            }
            do {
                numChars--;
                text = text.substring(0, numChars);
            } while (measureText.call(this, text, measureContext) >= targetWidth);
            $this.html($.trim($("<span/>").text(text).html()) + options.tail);
            this.style.visibility = "visible";
            info.shortened = true;
            $this.data(info_identifier, info);
            return true;
        });
        return true;
    };
    var css = document.documentElement.style;
    if ("textOverflow"in css) {
        _native = "textOverflow";
    } else if ("OTextOverflow"in css) {
        _native = "OTextOverflow";
    }
    if (typeof Modernizr != 'undefined' && Modernizr.canvastext) {
        is_canvasTextSupported = Modernizr.canvastext;
    } else {
        var canvas = document.createElement("canvas");
        is_canvasTextSupported = !!(canvas.getContext && canvas.getContext("2d") && (typeof canvas.getContext("2d").fillText === 'function'));
    }
    $.fn.shorten._is_canvasTextSupported = is_canvasTextSupported;
    $.fn.shorten._native = _native;
    function measureText_initCanvas() {
        var $this = $(this);
        var canvas = document.createElement("canvas");
        ctx = canvas.getContext("2d");
        $this.html(canvas);
        ctx.font = $this.css("font-style") + " " + $this.css("font-variant") + " " + $this.css("font-weight") + " " + Math.ceil(parseFloat($this.css("font-size"))) + "px " + $this.css("font-family");
        return ctx;
    }

    function measureText_canvas(text, ctx) {
        return ctx.measureText(text).width;
    };
    function measureText_initTable() {
        var css = "padding:0; margin:0; border:none; font:inherit;";
        var $table = $('<table style="' + css + 'width:auto;zoom:1;position:absolute;"><tr style="' + css + '"><td style="' + css + 'white-space:nowrap;"></td></tr></table>');
        $td = $("td", $table);
        $(this).html($table);
        return $td;
    };
    function measureText_table(text, $td) {
        $td.text(text);
        return $td.width();
    };
    $.fn.shorten.defaults = {tail: "&hellip;", tooltip: true};
})(jQuery);
jQuery.fn.boxy = function (options) {
    options = options || {};
    return this.each(function () {
        var node = this.nodeName.toLowerCase(), self = this;
        if (node == 'a') {
            jQuery(this).click(function () {
                var active = Boxy.linkedTo(this), href = this.getAttribute('href'), localOptions = jQuery.extend({actuator: this, title: this.title}, options);
                if (active) {
                    active.show();
                } else if (href.indexOf('#') >= 0) {
                    var content = jQuery(href.substr(href.indexOf('#'))), newContent = content.clone(true);
                    content.remove();
                    localOptions.unloadOnHide = false;
                    new Boxy(newContent, localOptions);
                } else {
                    if (!localOptions.cache)localOptions.unloadOnHide = true;
                    Boxy.load(this.href, localOptions);
                }
                return false;
            });
        } else if (node == 'form') {
            jQuery(this).bind('submit.boxy', function () {
                Boxy.confirm(options.message || 'Please confirm:', function () {
                    jQuery(self).unbind('submit.boxy').submit();
                });
                return false;
            });
        }
    });
};
function Boxy(element, options) {
    this.boxy = jQuery(Boxy.WRAPPER);
    jQuery.data(this.boxy[0], 'boxy', this);
    this.visible = false;
    this.options = jQuery.extend({}, Boxy.DEFAULTS, options || {});
    if (this.options.modal) {
        this.options = jQuery.extend(this.options, {center: true, draggable: false});
    }
    if (this.options.actuator) {
        jQuery.data(this.options.actuator, 'active.boxy', this);
    }
    this.setContent(element || "<div></div>");
    this._setupTitleBar();
    this.boxy.css('display', 'none').appendTo(document.body);
    this.toTop();
    if (this.options.fixed) {
        if (jQuery.browser.msie && jQuery.browser.version < 7) {
            this.options.fixed = false;
        } else {
            this.boxy.addClass('fixed');
        }
    }
    if (this.options.center && Boxy._u(this.options.x, this.options.y)) {
        this.center();
    } else {
        this.moveTo(Boxy._u(this.options.x) ? this.options.x : Boxy.DEFAULT_X, Boxy._u(this.options.y) ? this.options.y : Boxy.DEFAULT_Y);
    }
    if (this.options.show)this.show();
};
Boxy.EF = function () {
};
jQuery.extend(Boxy, {WRAPPER: "<table cellspacing='0' cellpadding='0' border='0' class='boxy-wrapper'>" + "<tr><td class='top-left'></td><td class='top'></td><td class='top-right'></td></tr>" + "<tr><td class='left'></td><td class='boxy-inner'></td><td class='right'></td></tr>" + "<tr><td class='bottom-left'></td><td class='bottom'></td><td class='bottom-right'></td></tr>" + "</table>", DEFAULTS: {title: null, closeable: true, draggable: true, clone: false, actuator: null, center: true, show: true, modal: false, fixed: true, closeText: '[close]', unloadOnHide: false, clickToFront: false, behaviours: Boxy.EF, afterDrop: Boxy.EF, afterShow: Boxy.EF, afterHide: Boxy.EF, beforeUnload: Boxy.EF}, DEFAULT_X: 50, DEFAULT_Y: 50, zIndex: 1337, dragConfigured: false, resizeConfigured: false, dragging: null, load: function (url, options) {
    options = options || {};
    var ajax = {url: url, type: 'GET', dataType: 'html', cache: false, success: function (html) {
        html = jQuery(html);
        if (options.filter)html = jQuery(options.filter, html);
        new Boxy(html, options);
    }};
    jQuery.each(['type', 'cache'], function () {
        if (this in options) {
            ajax[this] = options[this];
            delete options[this];
        }
    });
    jQuery.ajax(ajax);
}, get: function (ele) {
    var p = jQuery(ele).parents('.boxy-wrapper');
    return p.length ? jQuery.data(p[0], 'boxy') : null;
}, linkedTo: function (ele) {
    return jQuery.data(ele, 'active.boxy');
}, alert: function (message, callback, options) {
    return Boxy.ask(message, ['OK'], callback, options);
}, confirm: function (message, after, options) {
    return Boxy.ask(message, ['OK', 'Cancel'], function (response) {
        if (response == 'OK')after();
    }, options);
}, ask: function (question, answers, callback, options) {
    options = jQuery.extend({modal: true, closeable: false}, options || {}, {show: true, unloadOnHide: true});
    var body = jQuery('<div></div>').append(jQuery('<div class="question"></div>').html(question));
    var map = {}, answerStrings = [];
    if (answers instanceof Array) {
        for (var i = 0; i < answers.length; i++) {
            map[answers[i]] = answers[i];
            answerStrings.push(answers[i]);
        }
    } else {
        for (var k in answers) {
            map[answers[k]] = k;
            answerStrings.push(answers[k]);
        }
    }
    var buttons = jQuery('<form class="answers"></form>');
    buttons.html(jQuery.map(answerStrings,function (v) {
        return"<input type='button' value='" + v + "' />";
    }).join(' '));
    jQuery('input[type=button]', buttons).click(function () {
        var clicked = this;
        Boxy.get(this).hide(function () {
            if (callback)callback(map[clicked.value]);
        });
    });
    body.append(buttons);
    new Boxy(body, options);
}, isModalVisible: function () {
    return jQuery('.boxy-modal-blackout').length > 0;
}, _u: function () {
    for (var i = 0; i < arguments.length; i++)
        if (typeof arguments[i] != 'undefined')return false;
    return true;
}, _handleResize: function (evt) {
    var d = jQuery(document);
    jQuery('.boxy-modal-blackout').css('display', 'none').css({width: d.width(), height: d.height()}).css('display', 'block');
}, _handleDrag: function (evt) {
    var d;
    if (d = Boxy.dragging) {
        d[0].boxy.css({left: evt.pageX - d[1], top: evt.pageY - d[2]});
    }
}, _nextZ: function () {
    return Boxy.zIndex++;
}, _viewport: function () {
    var d = document.documentElement, b = document.body, w = window;
    return jQuery.extend(jQuery.browser.msie ? {left: b.scrollLeft || d.scrollLeft, top: b.scrollTop || d.scrollTop} : {left: w.pageXOffset, top: w.pageYOffset}, !Boxy._u(w.innerWidth) ? {width: w.innerWidth, height: w.innerHeight} : (!Boxy._u(d) && !Boxy._u(d.clientWidth) && d.clientWidth != 0 ? {width: d.clientWidth, height: d.clientHeight} : {width: b.clientWidth, height: b.clientHeight}));
}});
Boxy.prototype = {estimateSize: function () {
    this.boxy.css({visibility: 'hidden', display: 'block'});
    var dims = this.getSize();
    this.boxy.css('display', 'none').css('visibility', 'visible');
    return dims;
}, getSize: function () {
    return[this.boxy.width(), this.boxy.height()];
}, getContentSize: function () {
    var c = this.getContent();
    return[c.width(), c.height()];
}, getPosition: function () {
    var b = this.boxy[0];
    return[b.offsetLeft, b.offsetTop];
}, getCenter: function () {
    var p = this.getPosition();
    var s = this.getSize();
    return[Math.floor(p[0] + s[0] / 2), Math.floor(p[1] + s[1] / 2)];
}, getInner: function () {
    return jQuery('.boxy-inner', this.boxy);
}, getContent: function () {
    return jQuery('.boxy-content', this.boxy);
}, setContent: function (newContent) {
    newContent = jQuery(newContent).css({display: 'block'}).addClass('boxy-content');
    if (this.options.clone)newContent = newContent.clone(true);
    this.getContent().remove();
    this.getInner().append(newContent);
    this._setupDefaultBehaviours(newContent);
    this.options.behaviours.call(this, newContent);
    return this;
}, moveTo: function (x, y) {
    this.moveToX(x).moveToY(y);
    return this;
}, moveToX: function (x) {
    if (typeof x == 'number')this.boxy.css({left: x}); else this.centerX();
    return this;
}, moveToY: function (y) {
    if (typeof y == 'number')this.boxy.css({top: y}); else this.centerY();
    return this;
}, centerAt: function (x, y) {
    var s = this[this.visible ? 'getSize' : 'estimateSize']();
    if (typeof x == 'number')this.moveToX(x - s[0] / 2);
    if (typeof y == 'number')this.moveToY(y - s[1] / 2);
    return this;
}, centerAtX: function (x) {
    return this.centerAt(x, null);
}, centerAtY: function (y) {
    return this.centerAt(null, y);
}, center: function (axis) {
    var v = Boxy._viewport();
    var o = this.options.fixed ? [0, 0] : [v.left, v.top];
    if (!axis || axis == 'x')this.centerAt(o[0] + v.width / 2, null);
    if (!axis || axis == 'y')this.centerAt(null, o[1] + v.height / 2);
    return this;
}, centerX: function () {
    return this.center('x');
}, centerY: function () {
    return this.center('y');
}, resize: function (width, height, after) {
    if (!this.visible)return;
    var bounds = this._getBoundsForResize(width, height);
    this.boxy.css({left: bounds[0], top: bounds[1]});
    this.getContent().css({width: bounds[2], height: bounds[3]});
    if (after)after(this);
    return this;
}, tween: function (width, height, after) {
    if (!this.visible)return;
    var bounds = this._getBoundsForResize(width, height);
    var self = this;
    this.boxy.stop().animate({left: bounds[0], top: bounds[1]});
    this.getContent().stop().animate({width: bounds[2], height: bounds[3]}, function () {
        if (after)after(self);
    });
    return this;
}, isVisible: function () {
    return this.visible;
}, show: function () {
    if (this.visible)return;
    if (this.options.modal) {
        var self = this;
        if (!Boxy.resizeConfigured) {
            Boxy.resizeConfigured = true;
            jQuery(window).resize(function () {
                Boxy._handleResize();
            });
        }
        this.modalBlackout = jQuery('<div class="boxy-modal-blackout"></div>').css({zIndex: Boxy._nextZ(), opacity: 0.7, width: jQuery(document).width(), height: jQuery(document).height()}).appendTo(document.body);
        this.toTop();
        if (this.options.closeable) {
            jQuery(document.body).bind('keypress.boxy', function (evt) {
                var key = evt.which || evt.keyCode;
                if (key == 27) {
                    self.hide();
                    jQuery(document.body).unbind('keypress.boxy');
                }
            });
        }
    }
    this.boxy.stop().css({opacity: 1}).show();
    this.visible = true;
    this._fire('afterShow');
    return this;
}, hide: function (after) {
    if (!this.visible)return;
    var self = this;
    if (this.options.modal) {
        jQuery(document.body).unbind('keypress.boxy');
        this.modalBlackout.animate({opacity: 0}, function () {
            jQuery(this).remove();
        });
    }
    this.boxy.stop().animate({opacity: 0}, 300, function () {
        self.boxy.css({display: 'none'});
        self.visible = false;
        self._fire('afterHide');
        if (after)after(self);
        if (self.options.unloadOnHide)self.unload();
    });
    return this;
}, toggle: function () {
    this[this.visible ? 'hide' : 'show']();
    return this;
}, hideAndUnload: function (after) {
    this.options.unloadOnHide = true;
    this.hide(after);
    return this;
}, unload: function () {
    this._fire('beforeUnload');
    this.boxy.remove();
    if (this.options.actuator) {
        jQuery.data(this.options.actuator, 'active.boxy', false);
    }
}, toTop: function () {
    this.boxy.css({zIndex: Boxy._nextZ()});
    return this;
}, getTitle: function () {
    return jQuery('> .title-bar h2', this.getInner()).html();
}, setTitle: function (t) {
    jQuery('> .title-bar h2', this.getInner()).html(t);
    return this;
}, _getBoundsForResize: function (width, height) {
    var csize = this.getContentSize();
    var delta = [width - csize[0], height - csize[1]];
    var p = this.getPosition();
    return[Math.max(p[0] - delta[0] / 2, 0), Math.max(p[1] - delta[1] / 2, 0), width, height];
}, _setupTitleBar: function () {
    if (this.options.title) {
        var self = this;
        var tb = jQuery("<div class='title-bar'></div>").html("<h2>" + this.options.title + "</h2>");
        if (this.options.closeable) {
            tb.append(jQuery("<a href='#' class='close'></a>").html(this.options.closeText));
        }
        if (this.options.draggable) {
            tb[0].onselectstart = function () {
                return false;
            }
            tb[0].unselectable = 'on';
            tb[0].style.MozUserSelect = 'none';
            if (!Boxy.dragConfigured) {
                jQuery(document).mousemove(Boxy._handleDrag);
                Boxy.dragConfigured = true;
            }
            tb.mousedown(function (evt) {
                self.toTop();
                Boxy.dragging = [self, evt.pageX - self.boxy[0].offsetLeft, evt.pageY - self.boxy[0].offsetTop];
                jQuery(this).addClass('dragging');
            }).mouseup(function () {
                jQuery(this).removeClass('dragging');
                Boxy.dragging = null;
                self._fire('afterDrop');
            });
        }
        this.getInner().prepend(tb);
        this._setupDefaultBehaviours(tb);
    }
}, _setupDefaultBehaviours: function (root) {
    var self = this;
    if (this.options.clickToFront) {
        root.click(function () {
            self.toTop();
        });
    }
    jQuery('.close', root).click(function () {
        self.hide();
        return false;
    }).mousedown(function (evt) {
        evt.stopPropagation();
    });
}, _fire: function (event) {
    this.options[event].call(this);
}};
(function ($) {
    $.fn.autoGrowInput = function (o) {
        o = $.extend({maxWidth: 1000, minWidth: 0, comfortZone: 70}, o);
        this.filter('input:text').each(function () {
            var minWidth = o.minWidth || $(this).width(), val = '', input = $(this), testSubject = $('<tester/>').css({position: 'absolute', top: -9999, left: -9999, width: 'auto', fontSize: input.css('fontSize'), fontFamily: input.css('fontFamily'), fontWeight: input.css('fontWeight'), letterSpacing: input.css('letterSpacing'), whiteSpace: 'nowrap'}), check = function () {
                if (val === (val = input.val())) {
                    return;
                }
                var escaped = val.replace(/&/g, '&amp;').replace(/\s/g, ' ').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                testSubject.html(escaped);
                var testerWidth = testSubject.width(), newWidth = (testerWidth + o.comfortZone) >= minWidth ? testerWidth + o.comfortZone : minWidth, currentWidth = input.width(), isValidWidthChange = (newWidth < currentWidth && newWidth >= minWidth) || (newWidth > minWidth && newWidth < o.maxWidth);
                if (isValidWidthChange) {
                    input.width(newWidth);
                }
            };
            testSubject.insertAfter(input);
            $(this).bind('keyup keydown blur update', check);
        });
        return this;
    };
})(jQuery);
(function (window, document, undefined) {
    (function (factory) {
        "use strict";
        if (typeof define === 'function' && define.amd) {
            define(['jquery'], factory);
        }
        else if (jQuery && !jQuery.fn.qtip) {
            factory(jQuery);
        }
    }
    (function ($) {
        var TRUE = true, FALSE = false, NULL = null, X = 'x', Y = 'y', WIDTH = 'width', HEIGHT = 'height', TOP = 'top', LEFT = 'left', BOTTOM = 'bottom', RIGHT = 'right', CENTER = 'center', FLIP = 'flip', FLIPINVERT = 'flipinvert', SHIFT = 'shift', QTIP, PLUGINS, MOUSE, NAMESPACE = 'qtip', usedIDs = {}, widget = ['ui-widget', 'ui-tooltip'], selector = 'div.qtip.' + NAMESPACE, defaultClass = NAMESPACE + '-default', focusClass = NAMESPACE + '-focus', hoverClass = NAMESPACE + '-hover', replaceSuffix = '_replacedByqTip', oldtitle = 'oldtitle', trackingBound;

        function storeMouse(event) {
            MOUSE = {pageX: event.pageX, pageY: event.pageY, type: 'mousemove', scrollX: window.pageXOffset || document.body.scrollLeft || document.documentElement.scrollLeft, scrollY: window.pageYOffset || document.body.scrollTop || document.documentElement.scrollTop};
        }

        function sanitizeOptions(opts) {
            var invalid = function (a) {
                return a === NULL || 'object' !== typeof a;
            }, invalidContent = function (c) {
                return!$.isFunction(c) && ((!c && !c.attr) || c.length < 1 || ('object' === typeof c && !c.jquery && !c.then));
            };
            if (!opts || 'object' !== typeof opts) {
                return FALSE;
            }
            if (invalid(opts.metadata)) {
                opts.metadata = {type: opts.metadata};
            }
            if ('content'in opts) {
                if (invalid(opts.content) || opts.content.jquery) {
                    opts.content = {text: opts.content};
                }
                if (invalidContent(opts.content.text || FALSE)) {
                    opts.content.text = FALSE;
                }
                if ('title'in opts.content) {
                    if (invalid(opts.content.title)) {
                        opts.content.title = {text: opts.content.title};
                    }
                    if (invalidContent(opts.content.title.text || FALSE)) {
                        opts.content.title.text = FALSE;
                    }
                }
            }
            if ('position'in opts && invalid(opts.position)) {
                opts.position = {my: opts.position, at: opts.position};
            }
            if ('show'in opts && invalid(opts.show)) {
                opts.show = opts.show.jquery ? {target: opts.show} : {event: opts.show};
            }
            if ('hide'in opts && invalid(opts.hide)) {
                opts.hide = opts.hide.jquery ? {target: opts.hide} : {event: opts.hide};
            }
            if ('style'in opts && invalid(opts.style)) {
                opts.style = {classes: opts.style};
            }
            $.each(PLUGINS, function () {
                if (this.sanitize) {
                    this.sanitize(opts);
                }
            });
            return opts;
        }

        function QTip(target, options, id, attr) {
            var self = this, docBody = document.body, tooltipID = NAMESPACE + '-' + id, isPositioning = 0, isDrawing = 0, tooltip = $(), namespace = '.qtip-' + id, disabledClass = 'qtip-disabled', elements, cache;
            self.id = id;
            self.rendered = FALSE;
            self.destroyed = FALSE;
            self.elements = elements = {target: target};
            self.timers = {img: {}};
            self.options = options;
            self.checks = {};
            self.plugins = {};
            self.cache = cache = {event: {}, target: $(), disabled: FALSE, attr: attr, onTarget: FALSE, lastClass: ''};
            function convertNotation(notation) {
                var i = 0, obj, option = options, levels = notation.split('.');
                while (option = option[levels[i++]]) {
                    if (i < levels.length) {
                        obj = option;
                    }
                }
                return[obj || options, levels.pop()];
            }

            function createWidgetClass(cls) {
                return widget.concat('').join(cls ? '-' + cls + ' ' : ' ');
            }

            function setWidget() {
                var on = options.style.widget, disabled = tooltip.hasClass(disabledClass);
                tooltip.removeClass(disabledClass);
                disabledClass = on ? 'ui-state-disabled' : 'qtip-disabled';
                tooltip.toggleClass(disabledClass, disabled);
                tooltip.toggleClass('ui-helper-reset ' + createWidgetClass(), on).toggleClass(defaultClass, options.style.def && !on);
                if (elements.content) {
                    elements.content.toggleClass(createWidgetClass('content'), on);
                }
                if (elements.titlebar) {
                    elements.titlebar.toggleClass(createWidgetClass('header'), on);
                }
                if (elements.button) {
                    elements.button.toggleClass(NAMESPACE + '-icon', !on);
                }
            }

            function removeTitle(reposition) {
                if (elements.title) {
                    elements.titlebar.remove();
                    elements.titlebar = elements.title = elements.button = NULL;
                    if (reposition !== FALSE) {
                        self.reposition();
                    }
                }
            }

            function createButton() {
                var button = options.content.title.button, isString = typeof button === 'string', close = isString ? button : 'Close tooltip';
                if (elements.button) {
                    elements.button.remove();
                }
                if (button.jquery) {
                    elements.button = button;
                }
                else {
                    elements.button = $('<a />', {'class': 'qtip-close ' + (options.style.widget ? '' : NAMESPACE + '-icon'), 'title': close, 'aria-label': close}).prepend($('<span />', {'class': 'ui-icon ui-icon-close', 'html': '&times;'}));
                }
                elements.button.appendTo(elements.titlebar || tooltip).attr('role', 'button').click(function (event) {
                    if (!tooltip.hasClass(disabledClass)) {
                        self.hide(event);
                    }
                    return FALSE;
                });
            }

            function createTitle() {
                var id = tooltipID + '-title';
                if (elements.titlebar) {
                    removeTitle();
                }
                elements.titlebar = $('<div />', {'class': NAMESPACE + '-titlebar ' + (options.style.widget ? createWidgetClass('header') : '')}).append(elements.title = $('<div />', {'id': id, 'class': NAMESPACE + '-title', 'aria-atomic': TRUE})).insertBefore(elements.content).delegate('.qtip-close', 'mousedown keydown mouseup keyup mouseout',function (event) {
                    $(this).toggleClass('ui-state-active ui-state-focus', event.type.substr(-4) === 'down');
                }).delegate('.qtip-close', 'mouseover mouseout', function (event) {
                    $(this).toggleClass('ui-state-hover', event.type === 'mouseover');
                });
                if (options.content.title.button) {
                    createButton();
                }
            }

            function updateButton(button) {
                var elem = elements.button;
                if (!self.rendered) {
                    return FALSE;
                }
                if (!button) {
                    elem.remove();
                }
                else {
                    createButton();
                }
            }

            function updateTitle(content, reposition) {
                var elem = elements.title;
                if (!self.rendered || !content) {
                    return FALSE;
                }
                if ($.isFunction(content)) {
                    content = content.call(target, cache.event, self);
                }
                if (content === FALSE || (!content && content !== '')) {
                    return removeTitle(FALSE);
                }
                else if (content.jquery && content.length > 0) {
                    elem.empty().append(content.css({display: 'block'}));
                }
                else {
                    elem.html(content);
                }
                if (reposition !== FALSE && self.rendered && tooltip[0].offsetWidth > 0) {
                    self.reposition(cache.event);
                }
            }

            function deferredContent(deferred) {
                if (deferred && $.isFunction(deferred.done)) {
                    deferred.done(function (c) {
                        updateContent(c, null, FALSE);
                    });
                }
            }

            function updateContent(content, reposition, checkDeferred) {
                var elem = elements.content;
                if (!self.rendered || !content) {
                    return FALSE;
                }
                if ($.isFunction(content)) {
                    content = content.call(target, cache.event, self) || '';
                }
                if (checkDeferred !== FALSE) {
                    deferredContent(options.content.deferred);
                }
                if (content.jquery && content.length > 0) {
                    elem.empty().append(content.css({display: 'block'}));
                }
                else {
                    elem.html(content);
                }
                function detectImages(next) {
                    var images, srcs = {};

                    function imageLoad(image) {
                        if (image) {
                            delete srcs[image.src];
                            clearTimeout(self.timers.img[image.src]);
                            $(image).unbind(namespace);
                        }
                        if ($.isEmptyObject(srcs)) {
                            if (reposition !== FALSE) {
                                self.reposition(cache.event);
                            }
                            next();
                        }
                    }

                    if ((images = elem.find('img[src]:not([height]):not([width])')).length === 0) {
                        return imageLoad();
                    }
                    images.each(function (i, elem) {
                        if (srcs[elem.src] !== undefined) {
                            return;
                        }
                        var iterations = 0, maxIterations = 3;
                        (function timer() {
                            if (elem.height || elem.width || (iterations > maxIterations)) {
                                return imageLoad(elem);
                            }
                            iterations += 1;
                            self.timers.img[elem.src] = setTimeout(timer, 700);
                        }());
                        $(elem).bind('error' + namespace + ' load' + namespace, function () {
                            imageLoad(this);
                        });
                        srcs[elem.src] = elem;
                    });
                }

                if (self.rendered < 0) {
                    tooltip.queue('fx', detectImages);
                }
                else {
                    isDrawing = 0;
                    detectImages($.noop);
                }
                return self;
            }

            function assignEvents() {
                var posOptions = options.position, targets = {show: options.show.target, hide: options.hide.target, viewport: $(posOptions.viewport), document: $(document), body: $(document.body), window: $(window)}, events = {show: $.trim('' + options.show.event).split(' '), hide: $.trim('' + options.hide.event).split(' ')}, IE6 = $.browser.msie && parseInt($.browser.version, 10) === 6;

                function showMethod(event) {
                    if (tooltip.hasClass(disabledClass)) {
                        return FALSE;
                    }
                    clearTimeout(self.timers.show);
                    clearTimeout(self.timers.hide);
                    var callback = function () {
                        self.toggle(TRUE, event);
                    };
                    if (options.show.delay > 0) {
                        self.timers.show = setTimeout(callback, options.show.delay);
                    }
                    else {
                        callback();
                    }
                }

                function hideMethod(event) {
                    if (tooltip.hasClass(disabledClass) || isPositioning || isDrawing) {
                        return FALSE;
                    }
                    var relatedTarget = $(event.relatedTarget || event.target), ontoTooltip = relatedTarget.closest(selector)[0] === tooltip[0], ontoTarget = relatedTarget[0] === targets.show[0];
                    clearTimeout(self.timers.show);
                    clearTimeout(self.timers.hide);
                    if ((posOptions.target === 'mouse' && ontoTooltip) || (options.hide.fixed && ((/mouse(out|leave|move)/).test(event.type) && (ontoTooltip || ontoTarget)))) {
                        try {
                            event.preventDefault();
                            event.stopImmediatePropagation();
                        } catch (e) {
                        }
                        return;
                    }
                    if (options.hide.delay > 0) {
                        self.timers.hide = setTimeout(function () {
                            self.hide(event);
                        }, options.hide.delay);
                    }
                    else {
                        self.hide(event);
                    }
                }

                function inactiveMethod(event) {
                    if (tooltip.hasClass(disabledClass)) {
                        return FALSE;
                    }
                    clearTimeout(self.timers.inactive);
                    self.timers.inactive = setTimeout(function () {
                        self.hide(event);
                    }, options.hide.inactive);
                }

                function repositionMethod(event) {
                    if (self.rendered && tooltip[0].offsetWidth > 0) {
                        self.reposition(event);
                    }
                }

                tooltip.bind('mouseenter' + namespace + ' mouseleave' + namespace, function (event) {
                    var state = event.type === 'mouseenter';
                    if (state) {
                        self.focus(event);
                    }
                    tooltip.toggleClass(hoverClass, state);
                });
                if (/mouse(out|leave)/i.test(options.hide.event)) {
                    if (options.hide.leave === 'window') {
                        targets.window.bind('mouseout' + namespace + ' blur' + namespace, function (event) {
                            if (!/select|option/.test(event.target.nodeName) && !event.relatedTarget) {
                                self.hide(event);
                            }
                        });
                    }
                }
                if (options.hide.fixed) {
                    targets.hide = targets.hide.add(tooltip);
                    tooltip.bind('mouseover' + namespace, function () {
                        if (!tooltip.hasClass(disabledClass)) {
                            clearTimeout(self.timers.hide);
                        }
                    });
                }
                else if (/mouse(over|enter)/i.test(options.show.event)) {
                    targets.hide.bind('mouseleave' + namespace, function (event) {
                        clearTimeout(self.timers.show);
                    });
                }
                if (('' + options.hide.event).indexOf('unfocus') > -1) {
                    posOptions.container.closest('html').bind('mousedown' + namespace + ' touchstart' + namespace, function (event) {
                        var elem = $(event.target), enabled = self.rendered && !tooltip.hasClass(disabledClass) && tooltip[0].offsetWidth > 0, isAncestor = elem.parents(selector).filter(tooltip[0]).length > 0;
                        if (elem[0] !== target[0] && elem[0] !== tooltip[0] && !isAncestor && !target.has(elem[0]).length && !elem.attr('disabled')) {
                            self.hide(event);
                        }
                    });
                }
                if ('number' === typeof options.hide.inactive) {
                    targets.show.bind('qtip-' + id + '-inactive', inactiveMethod);
                    $.each(QTIP.inactiveEvents, function (index, type) {
                        targets.hide.add(elements.tooltip).bind(type + namespace + '-inactive', inactiveMethod);
                    });
                }
                $.each(events.hide, function (index, type) {
                    var showIndex = $.inArray(type, events.show), targetHide = $(targets.hide);
                    if ((showIndex > -1 && targetHide.add(targets.show).length === targetHide.length) || type === 'unfocus') {
                        targets.show.bind(type + namespace, function (event) {
                            if (tooltip[0].offsetWidth > 0) {
                                hideMethod(event);
                            }
                            else {
                                showMethod(event);
                            }
                        });
                        delete events.show[showIndex];
                    }
                    else {
                        targets.hide.bind(type + namespace, hideMethod);
                    }
                });
                $.each(events.show, function (index, type) {
                    targets.show.bind(type + namespace, showMethod);
                });
                if ('number' === typeof options.hide.distance) {
                    targets.show.add(tooltip).bind('mousemove' + namespace, function (event) {
                        var origin = cache.origin || {}, limit = options.hide.distance, abs = Math.abs;
                        if (abs(event.pageX - origin.pageX) >= limit || abs(event.pageY - origin.pageY) >= limit) {
                            self.hide(event);
                        }
                    });
                }
                if (posOptions.target === 'mouse') {
                    targets.show.bind('mousemove' + namespace, storeMouse);
                    if (posOptions.adjust.mouse) {
                        if (options.hide.event) {
                            tooltip.bind('mouseleave' + namespace, function (event) {
                                if ((event.relatedTarget || event.target) !== targets.show[0]) {
                                    self.hide(event);
                                }
                            });
                            elements.target.bind('mouseenter' + namespace + ' mouseleave' + namespace, function (event) {
                                cache.onTarget = event.type === 'mouseenter';
                            });
                        }
                        targets.document.bind('mousemove' + namespace, function (event) {
                            if (self.rendered && cache.onTarget && !tooltip.hasClass(disabledClass) && tooltip[0].offsetWidth > 0) {
                                self.reposition(event || MOUSE);
                            }
                        });
                    }
                }
                if (posOptions.adjust.resize || targets.viewport.length) {
                    ($.event.special.resize ? targets.viewport : targets.window).bind('resize' + namespace, repositionMethod);
                }
                targets.window.add(posOptions.container).bind('scroll' + namespace, repositionMethod);
            }

            function unassignEvents() {
                var targets = [options.show.target[0], options.hide.target[0], self.rendered && elements.tooltip[0], options.position.container[0], options.position.viewport[0], options.position.container.closest('html')[0], window, document];
                if (self.rendered) {
                    $([]).pushStack($.grep(targets, function (i) {
                        return typeof i === 'object';
                    })).unbind(namespace);
                }
                else {
                    options.show.target.unbind(namespace + '-create');
                }
            }

            self.checks.builtin = {'^id$': function (obj, o, v) {
                var id = v === TRUE ? QTIP.nextid : v, tooltipID = NAMESPACE + '-' + id;
                if (id !== FALSE && id.length > 0 && !$('#' + tooltipID).length) {
                    tooltip[0].id = tooltipID;
                    elements.content[0].id = tooltipID + '-content';
                    elements.title[0].id = tooltipID + '-title';
                }
            }, '^content.text$': function (obj, o, v) {
                updateContent(options.content.text);
            }, '^content.deferred$': function (obj, o, v) {
                deferredContent(options.content.deferred);
            }, '^content.title.text$': function (obj, o, v) {
                if (!v) {
                    return removeTitle();
                }
                if (!elements.title && v) {
                    createTitle();
                }
                updateTitle(v);
            }, '^content.title.button$': function (obj, o, v) {
                updateButton(v);
            }, '^position.(my|at)$': function (obj, o, v) {
                if ('string' === typeof v) {
                    obj[o] = new PLUGINS.Corner(v);
                }
            }, '^position.container$': function (obj, o, v) {
                if (self.rendered) {
                    tooltip.appendTo(v);
                }
            }, '^show.ready$': function () {
                if (!self.rendered) {
                    self.render(1);
                }
                else {
                    self.toggle(TRUE);
                }
            }, '^style.classes$': function (obj, o, v) {
                tooltip.attr('class', NAMESPACE + ' qtip ' + v);
            }, '^style.width|height': function (obj, o, v) {
                tooltip.css(o, v);
            }, '^style.widget|content.title': setWidget, '^events.(render|show|move|hide|focus|blur)$': function (obj, o, v) {
                tooltip[($.isFunction(v) ? '' : 'un') + 'bind']('tooltip' + o, v);
            }, '^(show|hide|position).(event|target|fixed|inactive|leave|distance|viewport|adjust)': function () {
                var posOptions = options.position;
                tooltip.attr('tracking', posOptions.target === 'mouse' && posOptions.adjust.mouse);
                unassignEvents();
                assignEvents();
            }};
            $.extend(self, {_triggerEvent: function (type, args, event) {
                var callback = $.Event('tooltip' + type);
                callback.originalEvent = (event ? $.extend({}, event) : NULL) || cache.event || NULL;
                tooltip.trigger(callback, [self].concat(args || []));
                return!callback.isDefaultPrevented();
            }, render: function (show) {
                if (self.rendered) {
                    return self;
                }
                var text = options.content.text, title = options.content.title, posOptions = options.position;
                $.attr(target[0], 'aria-describedby', tooltipID);
                tooltip = elements.tooltip = $('<div/>', {'id': tooltipID, 'class': [NAMESPACE, defaultClass, options.style.classes, NAMESPACE + '-pos-' + options.position.my.abbrev()].join(' '), 'width': options.style.width || '', 'height': options.style.height || '', 'tracking': posOptions.target === 'mouse' && posOptions.adjust.mouse, 'role': 'alert', 'aria-live': 'polite', 'aria-atomic': FALSE, 'aria-describedby': tooltipID + '-content', 'aria-hidden': TRUE}).toggleClass(disabledClass, cache.disabled).data('qtip', self).appendTo(options.position.container).append(elements.content = $('<div />', {'class': NAMESPACE + '-content', 'id': tooltipID + '-content', 'aria-atomic': TRUE}));
                self.rendered = -1;
                isPositioning = 1;
                if (title.text) {
                    createTitle();
                    if (!$.isFunction(title.text)) {
                        updateTitle(title.text, FALSE);
                    }
                }
                else if (title.button) {
                    createButton();
                }
                if (!$.isFunction(text) || text.then) {
                    updateContent(text, FALSE);
                }
                self.rendered = TRUE;
                setWidget();
                $.each(options.events, function (name, callback) {
                    if ($.isFunction(callback)) {
                        tooltip.bind(name === 'toggle' ? 'tooltipshow tooltiphide' : 'tooltip' + name, callback);
                    }
                });
                $.each(PLUGINS, function () {
                    if (this.initialize === 'render') {
                        this(self);
                    }
                });
                assignEvents();
                tooltip.queue('fx', function (next) {
                    self._triggerEvent('render');
                    isPositioning = 0;
                    if (options.show.ready || show) {
                        self.toggle(TRUE, cache.event, FALSE);
                    }
                    next();
                });
                return self;
            }, get: function (notation) {
                var result, o;
                switch (notation.toLowerCase()) {
                    case'dimensions':
                        result = {height: tooltip.outerHeight(FALSE), width: tooltip.outerWidth(FALSE)};
                        break;
                    case'offset':
                        result = PLUGINS.offset(tooltip, options.position.container);
                        break;
                    default:
                        o = convertNotation(notation.toLowerCase());
                        result = o[0][o[1]];
                        result = result.precedance ? result.string() : result;
                        break;
                }
                return result;
            }, set: function (option, value) {
                var rmove = /^position\.(my|at|adjust|target|container)|style|content|show\.ready/i, rdraw = /^content\.(title|attr)|style/i, reposition = FALSE, checks = self.checks, name;

                function callback(notation, args) {
                    var category, rule, match;
                    for (category in checks) {
                        for (rule in checks[category]) {
                            if (match = (new RegExp(rule, 'i')).exec(notation)) {
                                args.push(match);
                                checks[category][rule].apply(self, args);
                            }
                        }
                    }
                }

                if ('string' === typeof option) {
                    name = option;
                    option = {};
                    option[name] = value;
                }
                else {
                    option = $.extend(TRUE, {}, option);
                }
                $.each(option, function (notation, value) {
                    var obj = convertNotation(notation.toLowerCase()), previous;
                    previous = obj[0][obj[1]];
                    obj[0][obj[1]] = 'object' === typeof value && value.nodeType ? $(value) : value;
                    option[notation] = [obj[0], obj[1], value, previous];
                    reposition = rmove.test(notation) || reposition;
                });
                sanitizeOptions(options);
                isPositioning = 1;
                $.each(option, callback);
                isPositioning = 0;
                if (self.rendered && tooltip[0].offsetWidth > 0 && reposition) {
                    self.reposition(options.position.target === 'mouse' ? NULL : cache.event);
                }
                return self;
            }, toggle: function (state, event) {
                if (event) {
                    if ((/over|enter/).test(event.type) && (/out|leave/).test(cache.event.type) && options.show.target.add(event.target).length === options.show.target.length && tooltip.has(event.relatedTarget).length) {
                        return self;
                    }
                    cache.event = $.extend({}, event);
                }
                if (!self.rendered) {
                    return state ? self.render(1) : self;
                }
                var type = state ? 'show' : 'hide', opts = options[type], otherOpts = options[!state ? 'show' : 'hide'], posOptions = options.position, contentOptions = options.content, visible = tooltip[0].offsetWidth > 0, animate = state || opts.target.length === 1, sameTarget = !event || opts.target.length < 2 || cache.target[0] === event.target, showEvent, delay;
                if ((typeof state).search('boolean|number')) {
                    state = !visible;
                }
                if (!tooltip.is(':animated') && visible === state && sameTarget) {
                    return self;
                }
                if (!self._triggerEvent(type, [90])) {
                    return self;
                }
                $.attr(tooltip[0], 'aria-hidden', !!!state);
                if (state) {
                    cache.origin = $.extend({}, MOUSE);
                    self.focus(event);
                    if ($.isFunction(contentOptions.text)) {
                        updateContent(contentOptions.text, FALSE);
                    }
                    if ($.isFunction(contentOptions.title.text)) {
                        updateTitle(contentOptions.title.text, FALSE);
                    }
                    if (!trackingBound && posOptions.target === 'mouse' && posOptions.adjust.mouse) {
                        $(document).bind('mousemove.qtip', storeMouse);
                        trackingBound = TRUE;
                    }
                    self.reposition(event, arguments[2]);
                    if (!!opts.solo) {
                        (typeof opts.solo === 'string' ? $(opts.solo) : $(selector, opts.solo)).not(tooltip).not(opts.target).qtip('hide', $.Event('tooltipsolo'));
                    }
                }
                else {
                    clearTimeout(self.timers.show);
                    delete cache.origin;
                    if (trackingBound && !$(selector + '[tracking="true"]:visible', opts.solo).not(tooltip).length) {
                        $(document).unbind('mousemove.qtip');
                        trackingBound = FALSE;
                    }
                    self.blur(event);
                }
                function after() {
                    if (state) {
                        if ($.browser.msie) {
                            tooltip[0].style.removeAttribute('filter');
                        }
                        tooltip.css('overflow', '');
                        if ('string' === typeof opts.autofocus) {
                            $(opts.autofocus, tooltip).focus();
                        }
                        opts.target.trigger('qtip-' + id + '-inactive');
                    }
                    else {
                        tooltip.css({display: '', visibility: '', opacity: '', left: '', top: ''});
                    }
                    self._triggerEvent(state ? 'visible' : 'hidden');
                }

                if (opts.effect === FALSE || animate === FALSE) {
                    tooltip[type]();
                    after.call(tooltip);
                }
                else if ($.isFunction(opts.effect)) {
                    tooltip.stop(1, 1);
                    opts.effect.call(tooltip, self);
                    tooltip.queue('fx', function (n) {
                        after();
                        n();
                    });
                }
                else {
                    tooltip.fadeTo(90, state ? 1 : 0, after);
                }
                if (state) {
                    opts.target.trigger('qtip-' + id + '-inactive');
                }
                return self;
            }, show: function (event) {
                return self.toggle(TRUE, event);
            }, hide: function (event) {
                return self.toggle(FALSE, event);
            }, focus: function (event) {
                if (!self.rendered) {
                    return self;
                }
                var qtips = $(selector), curIndex = parseInt(tooltip[0].style.zIndex, 10), newIndex = QTIP.zindex + qtips.length, cachedEvent = $.extend({}, event), focusedElem;
                if (!tooltip.hasClass(focusClass)) {
                    if (self._triggerEvent('focus', [newIndex], cachedEvent)) {
                        if (curIndex !== newIndex) {
                            qtips.each(function () {
                                if (this.style.zIndex > curIndex) {
                                    this.style.zIndex = this.style.zIndex - 1;
                                }
                            });
                            qtips.filter('.' + focusClass).qtip('blur', cachedEvent);
                        }
                        tooltip.addClass(focusClass)[0].style.zIndex = newIndex;
                    }
                }
                return self;
            }, blur: function (event) {
                tooltip.removeClass(focusClass);
                self._triggerEvent('blur', [tooltip.css('zIndex')], event);
                return self;
            }, reposition: function (event, effect) {
                if (!self.rendered || isPositioning) {
                    return self;
                }
                isPositioning = 1;
                var target = options.position.target, posOptions = options.position, my = posOptions.my, at = posOptions.at, adjust = posOptions.adjust, method = adjust.method.split(' '), elemWidth = tooltip.outerWidth(FALSE), elemHeight = tooltip.outerHeight(FALSE), targetWidth = 0, targetHeight = 0, type = tooltip.css('position'), viewport = posOptions.viewport, position = {left: 0, top: 0}, container = posOptions.container, visible = tooltip[0].offsetWidth > 0, isScroll = event && event.type === 'scroll', win = $(window), adjusted, offset;
                if ($.isArray(target) && target.length === 2) {
                    at = {x: LEFT, y: TOP};
                    position = {left: target[0], top: target[1]};
                }
                else if (target === 'mouse' && ((event && event.pageX) || cache.event.pageX)) {
                    at = {x: LEFT, y: TOP};
                    event = MOUSE && MOUSE.pageX && (adjust.mouse || !event || !event.pageX) ? {pageX: MOUSE.pageX, pageY: MOUSE.pageY} : (event && (event.type === 'resize' || event.type === 'scroll') ? cache.event : event && event.pageX && event.type === 'mousemove' ? event : (!adjust.mouse || options.show.distance) && cache.origin && cache.origin.pageX ? cache.origin : event) || event || cache.event || MOUSE || {};
                    if (type !== 'static') {
                        position = container.offset();
                    }
                    position = {left: event.pageX - position.left, top: event.pageY - position.top};
                    if (adjust.mouse && isScroll) {
                        position.left -= MOUSE.scrollX - win.scrollLeft();
                        position.top -= MOUSE.scrollY - win.scrollTop();
                    }
                }
                else {
                    if (target === 'event' && event && event.target && event.type !== 'scroll' && event.type !== 'resize') {
                        cache.target = $(event.target);
                    }
                    else if (target !== 'event') {
                        cache.target = $(target.jquery ? target : elements.target);
                    }
                    target = cache.target;
                    target = $(target).eq(0);
                    if (target.length === 0) {
                        return self;
                    }
                    else if (target[0] === document || target[0] === window) {
                        targetWidth = PLUGINS.iOS ? window.innerWidth : target.width();
                        targetHeight = PLUGINS.iOS ? window.innerHeight : target.height();
                        if (target[0] === window) {
                            position = {top: (viewport || target).scrollTop(), left: (viewport || target).scrollLeft()};
                        }
                    }
                    else if (PLUGINS.imagemap && target.is('area')) {
                        adjusted = PLUGINS.imagemap(self, target, at, PLUGINS.viewport ? method : FALSE);
                    }
                    else if (PLUGINS.svg && target[0].ownerSVGElement) {
                        adjusted = PLUGINS.svg(self, target, at, PLUGINS.viewport ? method : FALSE);
                    }
                    else {
                        targetWidth = target.outerWidth(FALSE);
                        targetHeight = target.outerHeight(FALSE);
                        position = PLUGINS.offset(target, container);
                    }
                    if (adjusted) {
                        targetWidth = adjusted.width;
                        targetHeight = adjusted.height;
                        offset = adjusted.offset;
                        position = adjusted.position;
                    }
                    if ((PLUGINS.iOS > 3.1 && PLUGINS.iOS < 4.1) || (PLUGINS.iOS >= 4.3 && PLUGINS.iOS < 4.33) || (!PLUGINS.iOS && type === 'fixed')) {
                        position.left -= win.scrollLeft();
                        position.top -= win.scrollTop();
                    }
                    position.left += at.x === RIGHT ? targetWidth : at.x === CENTER ? targetWidth / 2 : 0;
                    position.top += at.y === BOTTOM ? targetHeight : at.y === CENTER ? targetHeight / 2 : 0;
                }
                position.left += adjust.x + (my.x === RIGHT ? -elemWidth : my.x === CENTER ? -elemWidth / 2 : 0);
                position.top += adjust.y + (my.y === BOTTOM ? -elemHeight : my.y === CENTER ? -elemHeight / 2 : 0);
                if (PLUGINS.viewport) {
                    position.adjusted = PLUGINS.viewport(self, position, posOptions, targetWidth, targetHeight, elemWidth, elemHeight);
                    if (offset && position.adjusted.left) {
                        position.left += offset.left;
                    }
                    if (offset && position.adjusted.top) {
                        position.top += offset.top;
                    }
                }
                else {
                    position.adjusted = {left: 0, top: 0};
                }
                if (!self._triggerEvent('move', [position, viewport.elem || viewport], event)) {
                    return self;
                }
                delete position.adjusted;
                if (effect === FALSE || !visible || isNaN(position.left) || isNaN(position.top) || target === 'mouse' || !$.isFunction(posOptions.effect)) {
                    tooltip.css(position);
                }
                else if ($.isFunction(posOptions.effect)) {
                    posOptions.effect.call(tooltip, self, $.extend({}, position));
                    tooltip.queue(function (next) {
                        $(this).css({opacity: '', height: ''});
                        if ($.browser.msie) {
                            this.style.removeAttribute('filter');
                        }
                        next();
                    });
                }
                isPositioning = 0;
                return self;
            }, disable: function (state) {
                if ('boolean' !== typeof state) {
                    state = !(tooltip.hasClass(disabledClass) || cache.disabled);
                }
                if (self.rendered) {
                    tooltip.toggleClass(disabledClass, state);
                    $.attr(tooltip[0], 'aria-disabled', state);
                }
                else {
                    cache.disabled = !!state;
                }
                return self;
            }, enable: function () {
                return self.disable(FALSE);
            }, destroy: function () {
                var t = target[0], title = $.attr(t, oldtitle), elemAPI = target.data('qtip');
                self.destroyed = TRUE;
                if (self.rendered) {
                    tooltip.stop(1, 0).remove();
                    $.each(self.plugins, function () {
                        if (this.destroy) {
                            this.destroy();
                        }
                    });
                }
                clearTimeout(self.timers.show);
                clearTimeout(self.timers.hide);
                unassignEvents();
                if (!elemAPI || self === elemAPI) {
                    $.removeData(t, 'qtip');
                    if (options.suppress && title) {
                        $.attr(t, 'title', title);
                        target.removeAttr(oldtitle);
                    }
                    target.removeAttr('aria-describedby');
                }
                target.unbind('.qtip-' + id);
                delete usedIDs[self.id];
                return target;
            }});
        }

        function init(id, opts) {
            var obj, posOptions, attr, config, title, elem = $(this), docBody = $(document.body), newTarget = this === document ? docBody : elem, metadata = (elem.metadata) ? elem.metadata(opts.metadata) : NULL, metadata5 = opts.metadata.type === 'html5' && metadata ? metadata[opts.metadata.name] : NULL, html5 = elem.data(opts.metadata.name || 'qtipopts');
            try {
                html5 = typeof html5 === 'string' ? $.parseJSON(html5) : html5;
            } catch (e) {
            }
            config = $.extend(TRUE, {}, QTIP.defaults, opts, typeof html5 === 'object' ? sanitizeOptions(html5) : NULL, sanitizeOptions(metadata5 || metadata));
            posOptions = config.position;
            config.id = id;
            if ('boolean' === typeof config.content.text) {
                attr = elem.attr(config.content.attr);
                if (config.content.attr !== FALSE && attr) {
                    config.content.text = attr;
                }
                else {
                    return FALSE;
                }
            }
            if (!posOptions.container.length) {
                posOptions.container = docBody;
            }
            if (posOptions.target === FALSE) {
                posOptions.target = newTarget;
            }
            if (config.show.target === FALSE) {
                config.show.target = newTarget;
            }
            if (config.show.solo === TRUE) {
                config.show.solo = posOptions.container.closest('body');
            }
            if (config.hide.target === FALSE) {
                config.hide.target = newTarget;
            }
            if (config.position.viewport === TRUE) {
                config.position.viewport = posOptions.container;
            }
            posOptions.container = posOptions.container.eq(0);
            posOptions.at = new PLUGINS.Corner(posOptions.at);
            posOptions.my = new PLUGINS.Corner(posOptions.my);
            if ($.data(this, 'qtip')) {
                if (config.overwrite) {
                    elem.qtip('destroy');
                }
                else if (config.overwrite === FALSE) {
                    return FALSE;
                }
            }
            if (config.suppress && (title = $.attr(this, 'title'))) {
                $(this).removeAttr('title').attr(oldtitle, title).attr('title', '');
            }
            obj = new QTip(elem, config, id, !!attr);
            $.data(this, 'qtip', obj);
            elem.bind('remove.qtip-' + id + ' removeqtip.qtip-' + id, function () {
                obj.destroy();
            });
            return obj;
        }

        QTIP = $.fn.qtip = function (options, notation, newValue) {
            var command = ('' + options).toLowerCase(), returned = NULL, args = $.makeArray(arguments).slice(1), event = args[args.length - 1], opts = this[0] ? $.data(this[0], 'qtip') : NULL;
            if ((!arguments.length && opts) || command === 'api') {
                return opts;
            }
            else if ('string' === typeof options) {
                this.each(function () {
                    var api = $.data(this, 'qtip');
                    if (!api) {
                        return TRUE;
                    }
                    if (event && event.timeStamp) {
                        api.cache.event = event;
                    }
                    if ((command === 'option' || command === 'options') && notation) {
                        if ($.isPlainObject(notation) || newValue !== undefined) {
                            api.set(notation, newValue);
                        }
                        else {
                            returned = api.get(notation);
                            return FALSE;
                        }
                    }
                    else if (api[command]) {
                        api[command].apply(api[command], args);
                    }
                });
                return returned !== NULL ? returned : this;
            }
            else if ('object' === typeof options || !arguments.length) {
                opts = sanitizeOptions($.extend(TRUE, {}, options));
                return QTIP.bind.call(this, opts, event);
            }
        };
        QTIP.bind = function (opts, event) {
            return this.each(function (i) {
                var options, targets, events, namespace, api, id;
                id = $.isArray(opts.id) ? opts.id[i] : opts.id;
                id = !id || id === FALSE || id.length < 1 || usedIDs[id] ? QTIP.nextid++ : (usedIDs[id] = id);
                namespace = '.qtip-' + id + '-create';
                api = init.call(this, id, opts);
                if (api === FALSE) {
                    return TRUE;
                }
                options = api.options;
                $.each(PLUGINS, function () {
                    if (this.initialize === 'initialize') {
                        this(api);
                    }
                });
                targets = {show: options.show.target, hide: options.hide.target};
                events = {show: $.trim('' + options.show.event).replace(/ /g, namespace + ' ') + namespace, hide: $.trim('' + options.hide.event).replace(/ /g, namespace + ' ') + namespace};
                if (/mouse(over|enter)/i.test(events.show) && !/mouse(out|leave)/i.test(events.hide)) {
                    events.hide += ' mouseleave' + namespace;
                }
                targets.show.bind('mousemove' + namespace, function (event) {
                    storeMouse(event);
                    api.cache.onTarget = TRUE;
                });
                function hoverIntent(event) {
                    function render() {
                        api.render(typeof event === 'object' || options.show.ready);
                        targets.show.add(targets.hide).unbind(namespace);
                    }

                    if (api.cache.disabled) {
                        return FALSE;
                    }
                    api.cache.event = $.extend({}, event);
                    api.cache.target = event ? $(event.target) : [undefined];
                    if (options.show.delay > 0) {
                        clearTimeout(api.timers.show);
                        api.timers.show = setTimeout(render, options.show.delay);
                        if (events.show !== events.hide) {
                            targets.hide.bind(events.hide, function () {
                                clearTimeout(api.timers.show);
                            });
                        }
                    }
                    else {
                        render();
                    }
                }

                targets.show.bind(events.show, hoverIntent);
                if (options.show.ready || options.prerender) {
                    hoverIntent(event);
                }
            }).attr('data-hasqtip', TRUE);
        };
        PLUGINS = QTIP.plugins = {Corner: function (corner) {
            corner = ('' + corner).replace(/([A-Z])/, ' $1').replace(/middle/gi, CENTER).toLowerCase();
            this.x = (corner.match(/left|right/i) || corner.match(/center/) || ['inherit'])[0].toLowerCase();
            this.y = (corner.match(/top|bottom|center/i) || ['inherit'])[0].toLowerCase();
            var f = corner.charAt(0);
            this.precedance = (f === 't' || f === 'b' ? Y : X);
            this.string = function () {
                return this.precedance === Y ? this.y + this.x : this.x + this.y;
            };
            this.abbrev = function () {
                var x = this.x.substr(0, 1), y = this.y.substr(0, 1);
                return x === y ? x : this.precedance === Y ? y + x : x + y;
            };
            this.invertx = function (center) {
                this.x = this.x === LEFT ? RIGHT : this.x === RIGHT ? LEFT : center || this.x;
            };
            this.inverty = function (center) {
                this.y = this.y === TOP ? BOTTOM : this.y === BOTTOM ? TOP : center || this.y;
            };
            this.clone = function () {
                return{x: this.x, y: this.y, precedance: this.precedance, string: this.string, abbrev: this.abbrev, clone: this.clone, invertx: this.invertx, inverty: this.inverty};
            };
        }, offset: function (elem, container) {
            var pos = elem.offset(), docBody = elem.closest('body'), quirks = $.browser.msie && document.compatMode !== 'CSS1Compat', parent = container, scrolled, coffset, overflow;

            function scroll(e, i) {
                pos.left += i * e.scrollLeft();
                pos.top += i * e.scrollTop();
            }

            if (parent) {
                do {
                    if (parent.css('position') !== 'static') {
                        coffset = parent.position();
                        pos.left -= coffset.left + (parseInt(parent.css('borderLeftWidth'), 10) || 0) + (parseInt(parent.css('marginLeft'), 10) || 0);
                        pos.top -= coffset.top + (parseInt(parent.css('borderTopWidth'), 10) || 0) + (parseInt(parent.css('marginTop'), 10) || 0);
                        if (!scrolled && (overflow = parent.css('overflow')) !== 'hidden' && overflow !== 'visible') {
                            scrolled = parent;
                        }
                    }
                }
                while ((parent = $(parent[0].offsetParent)).length);
                if (scrolled && scrolled[0] !== docBody[0] || quirks) {
                    scroll(scrolled || docBody, 1);
                }
            }
            return pos;
        }, iOS: parseFloat(('' + (/CPU.*OS ([0-9_]{1,5})|(CPU like).*AppleWebKit.*Mobile/i.exec(navigator.userAgent) || [0, ''])[1]).replace('undefined', '3_2').replace('_', '.').replace('_', '')) || FALSE, fn: {attr: function (attr, val) {
            if (this.length) {
                var self = this[0], title = 'title', api = $.data(self, 'qtip');
                if (attr === title && api && 'object' === typeof api && api.options.suppress) {
                    if (arguments.length < 2) {
                        return $.attr(self, oldtitle);
                    }
                    if (api && api.options.content.attr === title && api.cache.attr) {
                        api.set('content.text', val);
                    }
                    return this.attr(oldtitle, val);
                }
            }
            return $.fn['attr' + replaceSuffix].apply(this, arguments);
        }, clone: function (keepData) {
            var titles = $([]), title = 'title', elems = $.fn['clone' + replaceSuffix].apply(this, arguments);
            if (!keepData) {
                elems.filter('[' + oldtitle + ']').attr('title',function () {
                    return $.attr(this, oldtitle);
                }).removeAttr(oldtitle);
            }
            return elems;
        }}};
        $.each(PLUGINS.fn, function (name, func) {
            if (!func || $.fn[name + replaceSuffix]) {
                return TRUE;
            }
            var old = $.fn[name + replaceSuffix] = $.fn[name];
            $.fn[name] = function () {
                return func.apply(this, arguments) || old.apply(this, arguments);
            };
        });
        if (!$.ui) {
            $['cleanData' + replaceSuffix] = $.cleanData;
            $.cleanData = function (elems) {
                for (var i = 0, elem; (elem = elems[i]) !== undefined; i++) {
                    try {
                        $(elem).triggerHandler('removeqtip');
                    }
                    catch (e) {
                    }
                }
                $['cleanData' + replaceSuffix](elems);
            };
        }
        QTIP.version = '2.0.1-4-g';
        QTIP.nextid = 0;
        QTIP.inactiveEvents = 'click dblclick mousedown mouseup mousemove mouseleave mouseenter'.split(' ');
        QTIP.zindex = 15000;
        QTIP.defaults = {prerender: FALSE, id: FALSE, overwrite: TRUE, suppress: TRUE, content: {text: TRUE, attr: 'title', deferred: FALSE, title: {text: FALSE, button: FALSE}}, position: {my: 'top left', at: 'bottom right', target: FALSE, container: FALSE, viewport: FALSE, adjust: {x: 0, y: 0, mouse: TRUE, resize: TRUE, method: 'flipinvert flipinvert'}, effect: function (api, pos, viewport) {
            $(this).animate(pos, {duration: 200, queue: FALSE});
        }}, show: {target: FALSE, event: 'mouseenter', effect: TRUE, delay: 90, solo: FALSE, ready: FALSE, autofocus: FALSE}, hide: {target: FALSE, event: 'mouseleave', effect: TRUE, delay: 0, fixed: FALSE, inactive: FALSE, leave: 'window', distance: FALSE}, style: {classes: '', widget: FALSE, width: FALSE, height: FALSE, def: TRUE}, events: {render: NULL, move: NULL, show: NULL, hide: NULL, toggle: NULL, visible: NULL, hidden: NULL, focus: NULL, blur: NULL}};
        PLUGINS.svg = function (api, svg, corner, adjustMethod) {
            var doc = $(document), elem = svg[0], result = {width: 0, height: 0, position: {top: 1e10, left: 1e10}}, box, mtx, root, point, tPoint;
            while (!elem.getBBox) {
                elem = elem.parentNode;
            }
            if (elem.getBBox && elem.parentNode) {
                box = elem.getBBox();
                mtx = elem.getScreenCTM();
                root = elem.farthestViewportElement || elem;
                if (!root.createSVGPoint) {
                    return result;
                }
                point = root.createSVGPoint();
                point.x = box.x;
                point.y = box.y;
                tPoint = point.matrixTransform(mtx);
                result.position.left = tPoint.x;
                result.position.top = tPoint.y;
                point.x += box.width;
                point.y += box.height;
                tPoint = point.matrixTransform(mtx);
                result.width = tPoint.x - result.position.left;
                result.height = tPoint.y - result.position.top;
                result.position.left += doc.scrollLeft();
                result.position.top += doc.scrollTop();
            }
            return result;
        };
        function Ajax(api) {
            var self = this, tooltip = api.elements.tooltip, opts = api.options.content.ajax, defaults = QTIP.defaults.content.ajax, namespace = '.qtip-ajax', rscript = /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, first = TRUE, stop = FALSE, xhr;
            api.checks.ajax = {'^content.ajax': function (obj, name, v) {
                if (name === 'ajax') {
                    opts = v;
                }
                if (name === 'once') {
                    self.init();
                }
                else if (opts && opts.url) {
                    self.load();
                }
                else {
                    tooltip.unbind(namespace);
                }
            }};
            $.extend(self, {init: function () {
                if (opts && opts.url) {
                    tooltip.unbind(namespace)[opts.once ? 'one' : 'bind']('tooltipshow' + namespace, self.load);
                }
                return self;
            }, load: function (event) {
                if (stop) {
                    stop = FALSE;
                    return;
                }
                var hasSelector = opts.url.lastIndexOf(' '), url = opts.url, selector, hideFirst = !opts.loading && first;
                if (hideFirst) {
                    try {
                        event.preventDefault();
                    } catch (e) {
                    }
                }
                else if (event && event.isDefaultPrevented()) {
                    return self;
                }
                if (xhr && xhr.abort) {
                    xhr.abort();
                }
                if (hasSelector > -1) {
                    selector = url.substr(hasSelector);
                    url = url.substr(0, hasSelector);
                }
                function after() {
                    var complete;
                    if (api.destroyed) {
                        return;
                    }
                    first = FALSE;
                    if (hideFirst) {
                        stop = TRUE;
                        api.show(event.originalEvent);
                    }
                    if ((complete = defaults.complete || opts.complete) && $.isFunction(complete)) {
                        complete.apply(opts.context || api, arguments);
                    }
                }

                function successHandler(content, status, jqXHR) {
                    var success;
                    if (api.destroyed) {
                        return;
                    }
                    if (selector && 'string' === typeof content) {
                        content = $('<div/>').append(content.replace(rscript, "")).find(selector);
                    }
                    if ((success = defaults.success || opts.success) && $.isFunction(success)) {
                        success.call(opts.context || api, content, status, jqXHR);
                    }
                    else {
                        api.set('content.text', content);
                    }
                }

                function errorHandler(xhr, status, error) {
                    if (api.destroyed || xhr.status === 0) {
                        return;
                    }
                    api.set('content.text', status + ': ' + error);
                }

                xhr = $.ajax($.extend({error: defaults.error || errorHandler, context: api}, opts, {url: url, success: successHandler, complete: after}));
            }, destroy: function () {
                if (xhr && xhr.abort) {
                    xhr.abort();
                }
                api.destroyed = TRUE;
            }});
            self.init();
        }

        PLUGINS.ajax = function (api) {
            var self = api.plugins.ajax;
            return'object' === typeof self ? self : (api.plugins.ajax = new Ajax(api));
        };
        PLUGINS.ajax.initialize = 'render';
        PLUGINS.ajax.sanitize = function (options) {
            var content = options.content, opts;
            if (content && 'ajax'in content) {
                opts = content.ajax;
                if (typeof opts !== 'object') {
                    opts = options.content.ajax = {url: opts};
                }
                if ('boolean' !== typeof opts.once && opts.once) {
                    opts.once = !!opts.once;
                }
            }
        };
        $.extend(TRUE, QTIP.defaults, {content: {ajax: {loading: TRUE, once: TRUE}}});
        function calculateTip(corner, width, height) {
            var width2 = Math.ceil(width / 2), height2 = Math.ceil(height / 2), tips = {bottomright: [
                [0, 0],
                [width, height],
                [width, 0]
            ], bottomleft: [
                [0, 0],
                [width, 0],
                [0, height]
            ], topright: [
                [0, height],
                [width, 0],
                [width, height]
            ], topleft: [
                [0, 0],
                [0, height],
                [width, height]
            ], topcenter: [
                [0, height],
                [width2, 0],
                [width, height]
            ], bottomcenter: [
                [0, 0],
                [width, 0],
                [width2, height]
            ], rightcenter: [
                [0, 0],
                [width, height2],
                [0, height]
            ], leftcenter: [
                [width, 0],
                [width, height],
                [0, height2]
            ]};
            tips.lefttop = tips.bottomright;
            tips.righttop = tips.bottomleft;
            tips.leftbottom = tips.topright;
            tips.rightbottom = tips.topleft;
            return tips[corner.string()];
        }

        function Tip(qTip, command) {
            var self = this, opts = qTip.options.style.tip, elems = qTip.elements, tooltip = elems.tooltip, cache = {top: 0, left: 0}, size = {width: opts.width, height: opts.height}, color = {}, border = opts.border || 0, namespace = '.qtip-tip', hasCanvas = !!($('<canvas />')[0] || {}).getContext, tiphtml;
            self.corner = NULL;
            self.mimic = NULL;
            self.border = border;
            self.offset = opts.offset;
            self.size = size;
            qTip.checks.tip = {'^position.my|style.tip.(corner|mimic|border)$': function () {
                if (!self.init()) {
                    self.destroy();
                }
                qTip.reposition();
            }, '^style.tip.(height|width)$': function () {
                size = {width: opts.width, height: opts.height};
                self.create();
                self.update();
                qTip.reposition();
            }, '^content.title.text|style.(classes|widget)$': function () {
                if (elems.tip && elems.tip.length) {
                    self.update();
                }
            }};
            function whileVisible(callback) {
                var visible = tooltip.is(':visible');
                tooltip.show();
                callback();
                tooltip.toggle(visible);
            }

            function swapDimensions() {
                size.width = opts.height;
                size.height = opts.width;
            }

            function resetDimensions() {
                size.width = opts.width;
                size.height = opts.height;
            }

            function reposition(event, api, pos, viewport) {
                if (!elems.tip) {
                    return;
                }
                var newCorner = self.corner.clone(), adjust = pos.adjusted, method = qTip.options.position.adjust.method.split(' '), horizontal = method[0], vertical = method[1] || method[0], shift = {left: FALSE, top: FALSE, x: 0, y: 0}, offset, css = {}, props;
                if (self.corner.fixed !== TRUE) {
                    if (horizontal === SHIFT && newCorner.precedance === X && adjust.left && newCorner.y !== CENTER) {
                        newCorner.precedance = newCorner.precedance === X ? Y : X;
                    }
                    else if (horizontal !== SHIFT && adjust.left) {
                        newCorner.x = newCorner.x === CENTER ? (adjust.left > 0 ? LEFT : RIGHT) : (newCorner.x === LEFT ? RIGHT : LEFT);
                    }
                    if (vertical === SHIFT && newCorner.precedance === Y && adjust.top && newCorner.x !== CENTER) {
                        newCorner.precedance = newCorner.precedance === Y ? X : Y;
                    }
                    else if (vertical !== SHIFT && adjust.top) {
                        newCorner.y = newCorner.y === CENTER ? (adjust.top > 0 ? TOP : BOTTOM) : (newCorner.y === TOP ? BOTTOM : TOP);
                    }
                    if (newCorner.string() !== cache.corner.string() && (cache.top !== adjust.top || cache.left !== adjust.left)) {
                        self.update(newCorner, FALSE);
                    }
                }
                offset = self.position(newCorner, adjust);
                offset[newCorner.x] += parseWidth(newCorner, newCorner.x);
                offset[newCorner.y] += parseWidth(newCorner, newCorner.y);
                if (offset.right !== undefined) {
                    offset.left = -offset.right;
                }
                if (offset.bottom !== undefined) {
                    offset.top = -offset.bottom;
                }
                offset.user = Math.max(0, opts.offset);
                if (shift.left = (horizontal === SHIFT && !!adjust.left)) {
                    if (newCorner.x === CENTER) {
                        css['margin-left'] = shift.x = offset['margin-left'];
                    }
                    else {
                        props = offset.right !== undefined ? [adjust.left, -offset.left] : [-adjust.left, offset.left];
                        if ((shift.x = Math.max(props[0], props[1])) > props[0]) {
                            pos.left -= adjust.left;
                            shift.left = FALSE;
                        }
                        css[offset.right !== undefined ? RIGHT : LEFT] = shift.x;
                    }
                }
                if (shift.top = (vertical === SHIFT && !!adjust.top)) {
                    if (newCorner.y === CENTER) {
                        css['margin-top'] = shift.y = offset['margin-top'];
                    }
                    else {
                        props = offset.bottom !== undefined ? [adjust.top, -offset.top] : [-adjust.top, offset.top];
                        if ((shift.y = Math.max(props[0], props[1])) > props[0]) {
                            pos.top -= adjust.top;
                            shift.top = FALSE;
                        }
                        css[offset.bottom !== undefined ? BOTTOM : TOP] = shift.y;
                    }
                }
                elems.tip.css(css).toggle(!((shift.x && shift.y) || (newCorner.x === CENTER && shift.y) || (newCorner.y === CENTER && shift.x)));
                pos.left -= offset.left.charAt ? offset.user : horizontal !== SHIFT || shift.top || !shift.left && !shift.top ? offset.left : 0;
                pos.top -= offset.top.charAt ? offset.user : vertical !== SHIFT || shift.left || !shift.left && !shift.top ? offset.top : 0;
                cache.left = adjust.left;
                cache.top = adjust.top;
                cache.corner = newCorner.clone();
            }

            function parseCorner() {
                var corner = opts.corner, posOptions = qTip.options.position, at = posOptions.at, my = posOptions.my.string ? posOptions.my.string() : posOptions.my;
                if (corner === FALSE || (my === FALSE && at === FALSE)) {
                    return FALSE;
                }
                else {
                    if (corner === TRUE) {
                        self.corner = new PLUGINS.Corner(my);
                    }
                    else if (!corner.string) {
                        self.corner = new PLUGINS.Corner(corner);
                        self.corner.fixed = TRUE;
                    }
                }
                cache.corner = new PLUGINS.Corner(self.corner.string());
                return self.corner.string() !== 'centercenter';
            }

            function parseWidth(corner, side, use) {
                side = !side ? corner[corner.precedance] : side;
                var isTitleTop = elems.titlebar && corner.y === TOP, elem = isTitleTop ? elems.titlebar : tooltip, borderSide = 'border-' + side + '-width', css = function (elem) {
                    return parseInt(elem.css(borderSide), 10);
                }, val;
                whileVisible(function () {
                    val = (use ? css(use) : (css(elems.content) || css(elem) || css(tooltip))) || 0;
                });
                return val;
            }

            function parseRadius(corner) {
                var isTitleTop = elems.titlebar && corner.y === TOP, elem = isTitleTop ? elems.titlebar : elems.content, moz = $.browser.mozilla, prefix = moz ? '-moz-' : $.browser.webkit ? '-webkit-' : '', nonStandard = 'border-radius-' + corner.y + corner.x, standard = 'border-' + corner.y + '-' + corner.x + '-radius', css = function (c) {
                    return parseInt(elem.css(c), 10) || parseInt(tooltip.css(c), 10);
                }, val;
                whileVisible(function () {
                    val = css(standard) || css(prefix + standard) || css(prefix + nonStandard) || css(nonStandard) || 0;
                });
                return val;
            }

            function parseColours(actual) {
                var i, fill, border, tip = elems.tip.css('cssText', ''), corner = actual || self.corner, invalid = /rgba?\(0, 0, 0(, 0)?\)|transparent|#123456/i, borderSide = 'border-' + corner[corner.precedance] + '-color', bgColor = 'background-color', transparent = 'transparent', important = ' !important', titlebar = elems.titlebar, useTitle = titlebar && (corner.y === TOP || (corner.y === CENTER && tip.position().top + (size.height / 2) + opts.offset < titlebar.outerHeight(TRUE))), colorElem = useTitle ? titlebar : elems.content;

                function css(elem, prop, compare) {
                    var val = elem.css(prop) || transparent;
                    if (compare && val === elem.css(compare)) {
                        return FALSE;
                    }
                    else {
                        return invalid.test(val) ? FALSE : val;
                    }
                }

                whileVisible(function () {
                    color.fill = css(tip, bgColor) || css(colorElem, bgColor) || css(elems.content, bgColor) || css(tooltip, bgColor) || tip.css(bgColor);
                    color.border = css(tip, borderSide, 'color') || css(colorElem, borderSide, 'color') || css(elems.content, borderSide, 'color') || css(tooltip, borderSide, 'color') || tooltip.css(borderSide);
                    $('*', tip).add(tip).css('cssText', bgColor + ':' + transparent + important + ';border:0' + important + ';');
                });
            }

            function calculateSize(corner) {
                var y = corner.precedance === Y, width = size[y ? WIDTH : HEIGHT], height = size[y ? HEIGHT : WIDTH], isCenter = corner.string().indexOf(CENTER) > -1, base = width * (isCenter ? 0.5 : 1), pow = Math.pow, round = Math.round, bigHyp, ratio, result, smallHyp = Math.sqrt(pow(base, 2) + pow(height, 2)), hyp = [(border / base) * smallHyp, (border / height) * smallHyp];
                hyp[2] = Math.sqrt(pow(hyp[0], 2) - pow(border, 2));
                hyp[3] = Math.sqrt(pow(hyp[1], 2) - pow(border, 2));
                bigHyp = smallHyp + hyp[2] + hyp[3] + (isCenter ? 0 : hyp[0]);
                ratio = bigHyp / smallHyp;
                result = [round(ratio * height), round(ratio * width)];
                return{height: result[y ? 0 : 1], width: result[y ? 1 : 0]};
            }

            function createVML(tag, props, style) {
                return'<qvml:' + tag + ' xmlns="urn:schemas-microsoft.com:vml" class="qtip-vml" ' + (props || '') + ' style="behavior: url(#default#VML); ' + (style || '') + '" />';
            }

            $.extend(self, {init: function () {
                var enabled = parseCorner() && (hasCanvas || $.browser.msie);
                if (enabled) {
                    self.create();
                    self.update();
                    tooltip.unbind(namespace).bind('tooltipmove' + namespace, reposition);
                }
                return enabled;
            }, create: function () {
                var width = size.width, height = size.height, vml;
                if (elems.tip) {
                    elems.tip.remove();
                }
                elems.tip = $('<div />', {'class': 'qtip-tip'}).css({width: width, height: height}).prependTo(tooltip);
                if (hasCanvas) {
                    $('<canvas />').appendTo(elems.tip)[0].getContext('2d').save();
                }
                else {
                    vml = createVML('shape', 'coordorigin="0,0"', 'position:absolute;');
                    elems.tip.html(vml + vml);
                    $('*', elems.tip).bind('click mousedown', function (event) {
                        event.stopPropagation();
                    });
                }
            }, update: function (corner, position) {
                var tip = elems.tip, inner = tip.children(), width = size.width, height = size.height, mimic = opts.mimic, round = Math.round, precedance, context, coords, translate, newSize;
                if (!corner) {
                    corner = cache.corner || self.corner;
                }
                if (mimic === FALSE) {
                    mimic = corner;
                }
                else {
                    mimic = new PLUGINS.Corner(mimic);
                    mimic.precedance = corner.precedance;
                    if (mimic.x === 'inherit') {
                        mimic.x = corner.x;
                    }
                    else if (mimic.y === 'inherit') {
                        mimic.y = corner.y;
                    }
                    else if (mimic.x === mimic.y) {
                        mimic[corner.precedance] = corner[corner.precedance];
                    }
                }
                precedance = mimic.precedance;
                if (corner.precedance === X) {
                    swapDimensions();
                }
                else {
                    resetDimensions();
                }
                elems.tip.css({width: (width = size.width), height: (height = size.height)});
                parseColours(corner);
                if (color.border !== 'transparent') {
                    border = parseWidth(corner, NULL);
                    if (opts.border === 0 && border > 0) {
                        color.fill = color.border;
                    }
                    self.border = border = opts.border !== TRUE ? opts.border : border;
                }
                else {
                    self.border = border = 0;
                }
                coords = calculateTip(mimic, width, height);
                self.size = newSize = calculateSize(corner);
                tip.css(newSize).css('line-height', newSize.height + 'px');
                if (corner.precedance === Y) {
                    translate = [round(mimic.x === LEFT ? border : mimic.x === RIGHT ? newSize.width - width - border : (newSize.width - width) / 2), round(mimic.y === TOP ? newSize.height - height : 0)];
                }
                else {
                    translate = [round(mimic.x === LEFT ? newSize.width - width : 0), round(mimic.y === TOP ? border : mimic.y === BOTTOM ? newSize.height - height - border : (newSize.height - height) / 2)];
                }
                if (hasCanvas) {
                    inner.attr(newSize);
                    context = inner[0].getContext('2d');
                    context.restore();
                    context.save();
                    context.clearRect(0, 0, 3000, 3000);
                    context.fillStyle = color.fill;
                    context.strokeStyle = color.border;
                    context.lineWidth = border * 2;
                    context.lineJoin = 'miter';
                    context.miterLimit = 100;
                    context.translate(translate[0], translate[1]);
                    context.beginPath();
                    context.moveTo(coords[0][0], coords[0][1]);
                    context.lineTo(coords[1][0], coords[1][1]);
                    context.lineTo(coords[2][0], coords[2][1]);
                    context.closePath();
                    if (border) {
                        if (tooltip.css('background-clip') === 'border-box') {
                            context.strokeStyle = color.fill;
                            context.stroke();
                        }
                        context.strokeStyle = color.border;
                        context.stroke();
                    }
                    context.fill();
                }
                else {
                    coords = 'm' + coords[0][0] + ',' + coords[0][1] + ' l' + coords[1][0] + ',' + coords[1][1] + ' ' + coords[2][0] + ',' + coords[2][1] + ' xe';
                    translate[2] = border && /^(r|b)/i.test(corner.string()) ? parseFloat($.browser.version, 10) === 8 ? 2 : 1 : 0;
                    inner.css({coordsize: (width + border) + ' ' + (height + border), antialias: '' + (mimic.string().indexOf(CENTER) > -1), left: translate[0], top: translate[1], width: width + border, height: height + border}).each(function (i) {
                        var $this = $(this);
                        $this[$this.prop ? 'prop' : 'attr']({coordsize: (width + border) + ' ' + (height + border), path: coords, fillcolor: color.fill, filled: !!i, stroked: !i}).toggle(!!(border || i));
                        if (!i && $this.html() === '') {
                            $this.html(createVML('stroke', 'weight="' + (border * 2) + 'px" color="' + color.border + '" miterlimit="1000" joinstyle="miter"'));
                        }
                    });
                }
                if (position !== FALSE) {
                    self.position(corner);
                }
            }, position: function (corner) {
                var tip = elems.tip, position = {}, userOffset = Math.max(0, opts.offset), precedance, dimensions, corners;
                if (opts.corner === FALSE || !tip) {
                    return FALSE;
                }
                corner = corner || self.corner;
                precedance = corner.precedance;
                dimensions = calculateSize(corner);
                corners = [corner.x, corner.y];
                if (precedance === X) {
                    corners.reverse();
                }
                $.each(corners, function (i, side) {
                    var b, bc, br;
                    if (side === CENTER) {
                        b = precedance === Y ? LEFT : TOP;
                        position[b] = '50%';
                        position['margin-' + b] = -Math.round(dimensions[precedance === Y ? WIDTH : HEIGHT] / 2) + userOffset;
                    }
                    else {
                        b = parseWidth(corner, side);
                        bc = parseWidth(corner, side, elems.content);
                        br = parseRadius(corner);
                        position[side] = i ? bc : (userOffset + (br > b ? br : -b));
                    }
                });
                position[corner[precedance]] -= dimensions[precedance === X ? WIDTH : HEIGHT];
                tip.css({top: '', bottom: '', left: '', right: '', margin: ''}).css(position);
                return position;
            }, destroy: function () {
                if (elems.tip) {
                    elems.tip.remove();
                }
                elems.tip = false;
                tooltip.unbind(namespace);
            }});
            self.init();
        }

        PLUGINS.tip = function (api) {
            var self = api.plugins.tip;
            return'object' === typeof self ? self : (api.plugins.tip = new Tip(api));
        };
        PLUGINS.tip.initialize = 'render';
        PLUGINS.tip.sanitize = function (options) {
            var style = options.style, opts;
            if (style && 'tip'in style) {
                opts = options.style.tip;
                if (typeof opts !== 'object') {
                    options.style.tip = {corner: opts};
                }
                if (!(/string|boolean/i).test(typeof opts['corner'])) {
                    opts['corner'] = TRUE;
                }
                if (typeof opts.width !== 'number') {
                    delete opts.width;
                }
                if (typeof opts.height !== 'number') {
                    delete opts.height;
                }
                if (typeof opts.border !== 'number' && opts.border !== TRUE) {
                    delete opts.border;
                }
                if (typeof opts.offset !== 'number') {
                    delete opts.offset;
                }
            }
        };
        $.extend(TRUE, QTIP.defaults, {style: {tip: {corner: TRUE, mimic: FALSE, width: 6, height: 6, border: TRUE, offset: 0}}});
        function Modal(api) {
            var self = this, options = api.options.show.modal, elems = api.elements, tooltip = elems.tooltip, overlaySelector = '#qtip-overlay', globalNamespace = '.qtipmodal', namespace = globalNamespace + api.id, attr = 'is-modal-qtip', docBody = $(document.body), focusableSelector = PLUGINS.modal.focusable.join(','), focusableElems = {}, overlay;
            api.checks.modal = {'^show.modal.(on|blur)$': function () {
                self.init();
                elems.overlay.toggle(tooltip.is(':visible'));
            }, '^content.text$': function () {
                updateFocusable();
            }};
            function updateFocusable() {
                focusableElems = $(focusableSelector, tooltip).not('[disabled]').map(function () {
                    return typeof this.focus === 'function' ? this : null;
                });
            }

            function focusInputs(blurElems) {
                if (focusableElems.length < 1 && blurElems.length) {
                    blurElems.not('body').blur();
                }
                else {
                    focusableElems.first().focus();
                }
            }

            function stealFocus(event) {
                var target = $(event.target), container = target.closest('.qtip'), targetOnTop;
                targetOnTop = container.length < 1 ? FALSE : (parseInt(container[0].style.zIndex, 10) > parseInt(tooltip[0].style.zIndex, 10));
                if (!targetOnTop && ($(event.target).closest(selector)[0] !== tooltip[0])) {
                    focusInputs(target);
                }
            }

            $.extend(self, {init: function () {
                if (!options.on) {
                    return self;
                }
                overlay = self.create();
                tooltip.attr(attr, TRUE).css('z-index', PLUGINS.modal.zindex + $(selector + '[' + attr + ']').length).unbind(globalNamespace).unbind(namespace).bind('tooltipshow' + globalNamespace + ' tooltiphide' + globalNamespace,function (event, api, duration) {
                    var oEvent = event.originalEvent;
                    if (event.target === tooltip[0]) {
                        if (oEvent && event.type === 'tooltiphide' && /mouse(leave|enter)/.test(oEvent.type) && $(oEvent.relatedTarget).closest(overlay[0]).length) {
                            try {
                                event.preventDefault();
                            } catch (e) {
                            }
                        }
                        else if (!oEvent || (oEvent && !oEvent.solo)) {
                            self[event.type.replace('tooltip', '')](event, duration);
                        }
                    }
                }).bind('tooltipfocus' + globalNamespace,function (event) {
                        if (event.isDefaultPrevented() || event.target !== tooltip[0]) {
                            return;
                        }
                        var qtips = $(selector).filter('[' + attr + ']'), newIndex = PLUGINS.modal.zindex + qtips.length, curIndex = parseInt(tooltip[0].style.zIndex, 10);
                        overlay[0].style.zIndex = newIndex - 2;
                        qtips.each(function () {
                            if (this.style.zIndex > curIndex) {
                                this.style.zIndex -= 1;
                            }
                        });
                        qtips.end().filter('.' + focusClass).qtip('blur', event.originalEvent);
                        tooltip.addClass(focusClass)[0].style.zIndex = newIndex;
                        try {
                            event.preventDefault();
                        } catch (e) {
                        }
                    }).bind('tooltiphide' + globalNamespace, function (event) {
                        if (event.target === tooltip[0]) {
                            $('[' + attr + ']').filter(':visible').not(tooltip).last().qtip('focus', event);
                        }
                    });
                if (options.escape) {
                    $(document).unbind(namespace).bind('keydown' + namespace, function (event) {
                        if (event.keyCode === 27 && tooltip.hasClass(focusClass)) {
                            api.hide(event);
                        }
                    });
                }
                if (options.blur) {
                    elems.overlay.unbind(namespace).bind('click' + namespace, function (event) {
                        if (tooltip.hasClass(focusClass)) {
                            api.hide(event);
                        }
                    });
                }
                updateFocusable();
                return self;
            }, create: function () {
                var elem = $(overlaySelector), win = $(window);
                if (elem.length) {
                    return(elems.overlay = elem.insertAfter($(selector).last()));
                }
                overlay = elems.overlay = $('<div />', {id: overlaySelector.substr(1), html: '<div></div>', mousedown: function () {
                    return FALSE;
                }}).hide().insertAfter($(selector).last());
                function resize() {
                    overlay.css({height: win.height(), width: win.width()});
                }

                win.unbind(globalNamespace).bind('resize' + globalNamespace, resize);
                resize();
                return overlay;
            }, toggle: function (event, state, duration) {
                if (event && event.isDefaultPrevented()) {
                    return self;
                }
                var effect = options.effect, type = state ? 'show' : 'hide', visible = overlay.is(':visible'), modals = $('[' + attr + ']').filter(':visible').not(tooltip), zindex;
                if (!overlay) {
                    overlay = self.create();
                }
                if ((overlay.is(':animated') && visible === state && overlay.data('toggleState') !== FALSE) || (!state && modals.length)) {
                    return self;
                }
                if (state) {
                    overlay.css({left: 0, top: 0});
                    overlay.toggleClass('blurs', options.blur);
                    if (options.stealfocus !== FALSE) {
                        docBody.bind('focusin' + namespace, stealFocus);
                        focusInputs($('body :focus'));
                    }
                }
                else {
                    docBody.unbind('focusin' + namespace);
                }
                overlay.stop(TRUE, FALSE).data('toggleState', state);
                if ($.isFunction(effect)) {
                    effect.call(overlay, state);
                }
                else if (effect === FALSE) {
                    overlay[type]();
                }
                else {
                    overlay.fadeTo(parseInt(duration, 10) || 90, state ? 1 : 0, function () {
                        if (!state) {
                            $(this).hide();
                        }
                    });
                }
                if (!state) {
                    overlay.queue(function (next) {
                        overlay.css({left: '', top: ''}).removeData('toggleState');
                        next();
                    });
                }
                return self;
            }, show: function (event, duration) {
                return self.toggle(event, TRUE, duration);
            }, hide: function (event, duration) {
                return self.toggle(event, FALSE, duration);
            }, destroy: function () {
                var delBlanket = overlay;
                if (delBlanket) {
                    delBlanket = $('[' + attr + ']').not(tooltip).length < 1;
                    if (delBlanket) {
                        elems.overlay.remove();
                        $(document).unbind(globalNamespace);
                    }
                    else {
                        elems.overlay.unbind(globalNamespace + api.id);
                    }
                    docBody.unbind('focusin' + namespace);
                }
                return tooltip.removeAttr(attr).unbind(globalNamespace);
            }});
            self.init();
        }

        PLUGINS.modal = function (api) {
            var self = api.plugins.modal;
            return'object' === typeof self ? self : (api.plugins.modal = new Modal(api));
        };
        PLUGINS.modal.initialize = 'render';
        PLUGINS.modal.sanitize = function (opts) {
            if (opts.show) {
                if (typeof opts.show.modal !== 'object') {
                    opts.show.modal = {on: !!opts.show.modal};
                }
                else if (typeof opts.show.modal.on === 'undefined') {
                    opts.show.modal.on = TRUE;
                }
            }
        };
        PLUGINS.modal.zindex = QTIP.zindex - 200;
        PLUGINS.modal.focusable = ['a[href]', 'area[href]', 'input', 'select', 'textarea', 'button', 'iframe', 'object', 'embed', '[tabindex]', '[contenteditable]'];
        $.extend(TRUE, QTIP.defaults, {show: {modal: {on: FALSE, effect: TRUE, blur: TRUE, stealfocus: TRUE, escape: TRUE}}});
        PLUGINS.viewport = function (api, position, posOptions, targetWidth, targetHeight, elemWidth, elemHeight) {
            var target = posOptions.target, tooltip = api.elements.tooltip, my = posOptions.my, at = posOptions.at, adjust = posOptions.adjust, method = adjust.method.split(' '), methodX = method[0], methodY = method[1] || method[0], viewport = posOptions.viewport, container = posOptions.container, cache = api.cache, tip = api.plugins.tip, adjusted = {left: 0, top: 0}, fixed, newMy, newClass;
            if (!viewport.jquery || target[0] === window || target[0] === document.body || adjust.method === 'none') {
                return adjusted;
            }
            fixed = tooltip.css('position') === 'fixed';
            viewport = {elem: viewport, height: viewport[(viewport[0] === window ? 'h' : 'outerH') + 'eight'](), width: viewport[(viewport[0] === window ? 'w' : 'outerW') + 'idth'](), scrollleft: fixed ? 0 : viewport.scrollLeft(), scrolltop: fixed ? 0 : viewport.scrollTop(), offset: viewport.offset() || {left: 0, top: 0}};
            container = {elem: container, scrollLeft: container.scrollLeft(), scrollTop: container.scrollTop(), offset: container.offset() || {left: 0, top: 0}};
            function calculate(side, otherSide, type, adjust, side1, side2, lengthName, targetLength, elemLength) {
                var initialPos = position[side1], mySide = my[side], atSide = at[side], isShift = type === SHIFT, viewportScroll = -container.offset[side1] + viewport.offset[side1] + viewport['scroll' + side1], myLength = mySide === side1 ? elemLength : mySide === side2 ? -elemLength : -elemLength / 2, atLength = atSide === side1 ? targetLength : atSide === side2 ? -targetLength : -targetLength / 2, tipLength = tip && tip.size ? tip.size[lengthName] || 0 : 0, tipAdjust = tip && tip.corner && tip.corner.precedance === side && !isShift ? tipLength : 0, overflow1 = viewportScroll - initialPos + tipAdjust, overflow2 = initialPos + elemLength - viewport[lengthName] - viewportScroll + tipAdjust, offset = myLength - (my.precedance === side || mySide === my[otherSide] ? atLength : 0) - (atSide === CENTER ? targetLength / 2 : 0);
                if (isShift) {
                    tipAdjust = tip && tip.corner && tip.corner.precedance === otherSide ? tipLength : 0;
                    offset = (mySide === side1 ? 1 : -1) * myLength - tipAdjust;
                    position[side1] += overflow1 > 0 ? overflow1 : overflow2 > 0 ? -overflow2 : 0;
                    position[side1] = Math.max(-container.offset[side1] + viewport.offset[side1] + (tipAdjust && tip.corner[side] === CENTER ? tip.offset : 0), initialPos - offset, Math.min(Math.max(-container.offset[side1] + viewport.offset[side1] + viewport[lengthName], initialPos + offset), position[side1]));
                }
                else {
                    adjust *= (type === FLIPINVERT ? 2 : 0);
                    if (overflow1 > 0 && (mySide !== side1 || overflow2 > 0)) {
                        position[side1] -= offset + adjust;
                        newMy['invert' + side](side1);
                    }
                    else if (overflow2 > 0 && (mySide !== side2 || overflow1 > 0)) {
                        position[side1] -= (mySide === CENTER ? -offset : offset) + adjust;
                        newMy['invert' + side](side2);
                    }
                    if (position[side1] < viewportScroll && -position[side1] > overflow2) {
                        position[side1] = initialPos;
                        newMy = my.clone();
                    }
                }
                return position[side1] - initialPos;
            }

            if (methodX !== 'shift' || methodY !== 'shift') {
                newMy = my.clone();
            }
            adjusted = {left: methodX !== 'none' ? calculate(X, Y, methodX, adjust.x, LEFT, RIGHT, WIDTH, targetWidth, elemWidth) : 0, top: methodY !== 'none' ? calculate(Y, X, methodY, adjust.y, TOP, BOTTOM, HEIGHT, targetHeight, elemHeight) : 0};
            if (newMy && cache.lastClass !== (newClass = NAMESPACE + '-pos-' + newMy.abbrev())) {
                tooltip.removeClass(api.cache.lastClass).addClass((api.cache.lastClass = newClass));
            }
            return adjusted;
        };
        PLUGINS.imagemap = function (api, area, corner, adjustMethod) {
            if (!area.jquery) {
                area = $(area);
            }
            var cache = (api.cache.areas = {}), shape = (area[0].shape || area.attr('shape')).toLowerCase(), coordsString = area[0].coords || area.attr('coords'), baseCoords = coordsString.split(','), coords = [], image = $('img[usemap="#' + area.parent('map').attr('name') + '"]'), imageOffset = image.offset(), result = {width: 0, height: 0, position: {top: 1e10, right: 0, bottom: 0, left: 1e10}}, i = 0, next = 0, dimensions;

            function polyCoordinates(result, coords, corner) {
                var i = 0, compareX = 1, compareY = 1, realX = 0, realY = 0, newWidth = result.width, newHeight = result.height;
                while (newWidth > 0 && newHeight > 0 && compareX > 0 && compareY > 0) {
                    newWidth = Math.floor(newWidth / 2);
                    newHeight = Math.floor(newHeight / 2);
                    if (corner.x === LEFT) {
                        compareX = newWidth;
                    }
                    else if (corner.x === RIGHT) {
                        compareX = result.width - newWidth;
                    }
                    else {
                        compareX += Math.floor(newWidth / 2);
                    }
                    if (corner.y === TOP) {
                        compareY = newHeight;
                    }
                    else if (corner.y === BOTTOM) {
                        compareY = result.height - newHeight;
                    }
                    else {
                        compareY += Math.floor(newHeight / 2);
                    }
                    i = coords.length;
                    while (i--) {
                        if (coords.length < 2) {
                            break;
                        }
                        realX = coords[i][0] - result.position.left;
                        realY = coords[i][1] - result.position.top;
                        if ((corner.x === LEFT && realX >= compareX) || (corner.x === RIGHT && realX <= compareX) || (corner.x === CENTER && (realX < compareX || realX > (result.width - compareX))) || (corner.y === TOP && realY >= compareY) || (corner.y === BOTTOM && realY <= compareY) || (corner.y === CENTER && (realY < compareY || realY > (result.height - compareY)))) {
                            coords.splice(i, 1);
                        }
                    }
                }
                return{left: coords[0][0], top: coords[0][1]};
            }

            imageOffset.left += Math.ceil((image.outerWidth() - image.width()) / 2);
            imageOffset.top += Math.ceil((image.outerHeight() - image.height()) / 2);
            if (shape === 'poly') {
                i = baseCoords.length;
                while (i--) {
                    next = [parseInt(baseCoords[--i], 10), parseInt(baseCoords[i + 1], 10)];
                    if (next[0] > result.position.right) {
                        result.position.right = next[0];
                    }
                    if (next[0] < result.position.left) {
                        result.position.left = next[0];
                    }
                    if (next[1] > result.position.bottom) {
                        result.position.bottom = next[1];
                    }
                    if (next[1] < result.position.top) {
                        result.position.top = next[1];
                    }
                    coords.push(next);
                }
            }
            else {
                i = -1;
                while (i++ < baseCoords.length) {
                    coords.push(parseInt(baseCoords[i], 10));
                }
            }
            switch (shape) {
                case'rect':
                    result = {width: Math.abs(coords[2] - coords[0]), height: Math.abs(coords[3] - coords[1]), position: {left: Math.min(coords[0], coords[2]), top: Math.min(coords[1], coords[3])}};
                    break;
                case'circle':
                    result = {width: coords[2] + 2, height: coords[2] + 2, position: {left: coords[0], top: coords[1]}};
                    break;
                case'poly':
                    result.width = Math.abs(result.position.right - result.position.left);
                    result.height = Math.abs(result.position.bottom - result.position.top);
                    if (corner.abbrev() === 'c') {
                        result.position = {left: result.position.left + (result.width / 2), top: result.position.top + (result.height / 2)};
                    }
                    else {
                        if (!cache[corner + coordsString]) {
                            result.position = polyCoordinates(result, coords.slice(), corner);
                            if (adjustMethod && (adjustMethod[0] === 'flip' || adjustMethod[1] === 'flip')) {
                                result.offset = polyCoordinates(result, coords.slice(), {x: corner.x === LEFT ? RIGHT : corner.x === RIGHT ? LEFT : CENTER, y: corner.y === TOP ? BOTTOM : corner.y === BOTTOM ? TOP : CENTER});
                                result.offset.left -= result.position.left;
                                result.offset.top -= result.position.top;
                            }
                            cache[corner + coordsString] = result;
                        }
                        result = cache[corner + coordsString];
                    }
                    result.width = result.height = 0;
                    break;
            }
            result.position.left += imageOffset.left;
            result.position.top += imageOffset.top;
            return result;
        };
        function IE6(api) {
            var self = this, elems = api.elements, options = api.options, tooltip = elems.tooltip, namespace = '.ie6-' + api.id, bgiframe = $('select, object').length < 1, isDrawing = 0, modalProcessed = FALSE, redrawContainer;
            api.checks.ie6 = {'^content|style$': function (obj, o, v) {
                redraw();
            }};
            $.extend(self, {init: function () {
                var win = $(window), scroll;
                if (bgiframe) {
                    elems.bgiframe = $('<iframe class="qtip-bgiframe" frameborder="0" tabindex="-1" src="javascript:\'\';" ' + ' style="display:block; position:absolute; z-index:-1; filter:alpha(opacity=0); ' + '-ms-filter:"progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";"></iframe>');
                    elems.bgiframe.appendTo(tooltip);
                    tooltip.bind('tooltipmove' + namespace, self.adjustBGIFrame);
                }
                redrawContainer = $('<div/>', {id: 'qtip-rcontainer'}).appendTo(document.body);
                self.redraw();
                if (elems.overlay && !modalProcessed) {
                    scroll = function () {
                        elems.overlay[0].style.top = win.scrollTop() + 'px';
                    };
                    win.bind('scroll.qtip-ie6, resize.qtip-ie6', scroll);
                    scroll();
                    elems.overlay.addClass('qtipmodal-ie6fix');
                    modalProcessed = TRUE;
                }
            }, adjustBGIFrame: function () {
                var dimensions = api.get('dimensions'), plugin = api.plugins.tip, tip = elems.tip, tipAdjust, offset;
                offset = parseInt(tooltip.css('border-left-width'), 10) || 0;
                offset = {left: -offset, top: -offset};
                if (plugin && tip) {
                    tipAdjust = (plugin.corner.precedance === 'x') ? ['width', 'left'] : ['height', 'top'];
                    offset[tipAdjust[1]] -= tip[tipAdjust[0]]();
                }
                elems.bgiframe.css(offset).css(dimensions);
            }, redraw: function () {
                if (api.rendered < 1 || isDrawing) {
                    return self;
                }
                var style = options.style, container = options.position.container, perc, width, max, min;
                isDrawing = 1;
                if (style.height) {
                    tooltip.css(HEIGHT, style.height);
                }
                if (style.width) {
                    tooltip.css(WIDTH, style.width);
                }
                else {
                    tooltip.css(WIDTH, '').appendTo(redrawContainer);
                    width = tooltip.width();
                    if (width % 2 < 1) {
                        width += 1;
                    }
                    max = tooltip.css('max-width') || '';
                    min = tooltip.css('min-width') || '';
                    perc = (max + min).indexOf('%') > -1 ? container.width() / 100 : 0;
                    max = ((max.indexOf('%') > -1 ? perc : 1) * parseInt(max, 10)) || width;
                    min = ((min.indexOf('%') > -1 ? perc : 1) * parseInt(min, 10)) || 0;
                    width = max + min ? Math.min(Math.max(width, min), max) : width;
                    tooltip.css(WIDTH, Math.round(width)).appendTo(container);
                }
                isDrawing = 0;
                return self;
            }, destroy: function () {
                if (bgiframe) {
                    elems.bgiframe.remove();
                }
                tooltip.unbind(namespace);
            }});
            self.init();
        }

        PLUGINS.ie6 = function (api) {
            var browser = $.browser, self = api.plugins.ie6;
            if (!(browser.msie && ('' + browser.version).charAt(0) === '6')) {
                return FALSE;
            }
            return'object' === typeof self ? self : (api.plugins.ie6 = new IE6(api));
        };
        PLUGINS.ie6.initialize = 'render';
    }));
}(window, document));
(function () {
    function f(a, b) {
        if (b)for (var c in b)if (b.hasOwnProperty(c))a[c] = b[c];
        return a
    }

    function l(a, b) {
        var c = [];
        for (var d in a)if (a.hasOwnProperty(d))c[d] = b(a[d]);
        return c
    }

    function m(a, b, c) {
        if (e.isSupported(b.version))a.innerHTML = e.getHTML(b, c); else if (b.expressInstall && e.isSupported([6, 65]))a.innerHTML = e.getHTML(f(b, {src: b.expressInstall}), {MMredirectURL: location.href, MMplayerType: "PlugIn", MMdoctitle: document.title}); else {
            if (!a.innerHTML.replace(/\s/g, "")) {
                a.innerHTML = "<h2>Flash version " + b.version + " or greater is required</h2><h3>" + (g[0] > 0 ? "Your version is " + g : "You have no flash plugin installed") + "</h3>" + (a.tagName == "A" ? "<p>Click here to download latest version</p>" : "<p>Download latest version from <a href='" + k + "'>here</a></p>");
                if (a.tagName == "A")a.onclick = function () {
                    location.href = k
                }
            }
            if (b.onFail) {
                var d = b.onFail.call(this);
                if (typeof d == "string")a.innerHTML = d
            }
        }
        if (i)window[b.id] = document.getElementById(b.id);
        f(this, {getRoot: function () {
            return a
        }, getOptions: function () {
            return b
        }, getConf: function () {
            return c
        }, getApi: function () {
            return a.firstChild
        }})
    }

    var i = document.all, k = "http://www.adobe.com/go/getflashplayer", n = typeof jQuery == "function", o = /(\d+)[^\d]+(\d+)[^\d]*(\d*)/, j = {width: "100%", height: "100%", id: "_" + ("" + Math.random()).slice(9), allowfullscreen: true, allowscriptaccess: "always", quality: "high", version: [3, 0], onFail: null, expressInstall: null, w3c: false, cachebusting: false};
    window.attachEvent && window.attachEvent("onbeforeunload", function () {
        __flash_unloadHandler = function () {
        };
        __flash_savedUnloadHandler = function () {
        }
    });
    window.flashembed = function (a, b, c) {
        if (typeof a == "string")a = document.getElementById(a.replace("#", ""));
        if (a) {
            if (typeof b == "string")b = {src: b};
            return new m(a, f(f({}, j), b), c)
        }
    };
    var e = f(window.flashembed, {conf: j, getVersion: function () {
        var a, b;
        try {
            b = navigator.plugins["Shockwave Flash"].description.slice(16)
        } catch (c) {
            try {
                b = (a = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7")) && a.GetVariable("$version")
            } catch (d) {
                try {
                    b = (a = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6")) && a.GetVariable("$version")
                } catch (h) {
                }
            }
        }
        return(b = o.exec(b)) ? [b[1], b[3]] : [0, 0]
    }, asString: function (a) {
        if (a === null || a === undefined)return null;
        var b = typeof a;
        if (b == "object" && a.push)b = "array";
        switch (b) {
            case"string":
                a = a.replace(new RegExp('(["\\\\])', "g"), "\\$1");
                a = a.replace(/^\s?(\d+\.?\d+)%/, "$1pct");
                return'"' + a + '"';
            case"array":
                return"[" + l(a,function (d) {
                    return e.asString(d)
                }).join(",") + "]";
            case"function":
                return'"function()"';
            case"object":
                b = [];
                for (var c in a)a.hasOwnProperty(c) && b.push('"' + c + '":' + e.asString(a[c]));
                return"{" + b.join(",") + "}"
        }
        return String(a).replace(/\s/g, " ").replace(/\'/g, '"')
    }, getHTML: function (a, b) {
        a = f({}, a);
        var c = '<object width="' + a.width + '" height="' + a.height + '" id="' + a.id + '" name="' + a.id + '"';
        if (a.cachebusting)a.src += (a.src.indexOf("?") != -1 ? "&" : "?") + Math.random();
        c += a.w3c || !i ? ' data="' + a.src + '" type="application/x-shockwave-flash"' : ' classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"';
        c += ">";
        if (a.w3c || i)c += '<param name="movie" value="' + a.src + '" />';
        a.width = a.height = a.id = a.w3c = a.src = null;
        a.onFail = a.version = a.expressInstall = null;
        for (var d in a)if (a[d])c += '<param name="' + d + '" value="' + a[d] + '" />';
        a = "";
        if (b) {
            for (var h in b)if (b[h]) {
                d = b[h];
                a += h + "=" + (/function|object/.test(typeof d) ? e.asString(d) : d) + "&"
            }
            a = a.slice(0, -1);
            c += '<param name="flashvars" value=\'' + a + "' />"
        }
        c += "</object>";
        return c
    }, isSupported: function (a) {
        return g[0] > a[0] || g[0] == a[0] && g[1] >= a[1]
    }}), g = e.getVersion();
    if (n) {
        jQuery.tools = jQuery.tools || {version: "1.2.5"};
        jQuery.tools.flashembed = {conf: j};
        jQuery.fn.flashembed = function (a, b) {
            return this.each(function () {
                $(this).data("flashembed", flashembed(this, a, b))
            })
        }
    }
})();
(function (b) {
    function h(c) {
        if (c) {
            var a = d.contentWindow.document;
            a.open().close();
            a.location.hash = c
        }
    }

    var g, d, f, i;
    b.tools = b.tools || {version: "1.2.5"};
    b.tools.history = {init: function (c) {
        if (!i) {
            if (b.browser.msie && b.browser.version < "8") {
                if (!d) {
                    d = b("<iframe/>").attr("src", "javascript:false;").hide().get(0);
                    b("body").append(d);
                    setInterval(function () {
                        var a = d.contentWindow.document;
                        a = a.location.hash;
                        g !== a && b.event.trigger("hash", a)
                    }, 100);
                    h(location.hash || "#")
                }
            } else setInterval(function () {
                var a = location.hash;
                a !== g && b.event.trigger("hash", a)
            }, 100);
            f = !f ? c : f.add(c);
            c.click(function (a) {
                var e = b(this).attr("href");
                d && h(e);
                if (e.slice(0, 1) != "#") {
                    location.href = "#" + e;
                    return a.preventDefault()
                }
            });
            i = true
        }
    }};
    b(window).bind("hash", function (c, a) {
        a ? f.filter(function () {
            var e = b(this).attr("href");
            return e == a || e == a.replace("#", "")
        }).trigger("history", [a]) : f.eq(0).trigger("history", [a]);
        g = a
    });
    b.fn.history = function (c) {
        b.tools.history.init(this);
        return this.bind("history", c)
    }
})(jQuery);
(function (b) {
    function k() {
        if (b.browser.msie) {
            var a = b(document).height(), d = b(window).height();
            return[window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth, a - d < 20 ? d : a]
        }
        return[b(document).width(), b(document).height()]
    }

    function h(a) {
        if (a)return a.call(b.mask)
    }

    b.tools = b.tools || {version: "1.2.5"};
    var l;
    l = b.tools.expose = {conf: {maskId: "exposeMask", loadSpeed: "slow", closeSpeed: "fast", closeOnClick: true, closeOnEsc: true, zIndex: 9998, opacity: 0.8, startOpacity: 0, color: "#fff", onLoad: null, onClose: null}};
    var c, i, e, g, j;
    b.mask = {load: function (a, d) {
        if (e)return this;
        if (typeof a == "string")a = {color: a};
        a = a || g;
        g = a = b.extend(b.extend({}, l.conf), a);
        c = b("#" + a.maskId);
        if (!c.length) {
            c = b("<div/>").attr("id", a.maskId);
            b("body").append(c)
        }
        var m = k();
        c.css({position: "absolute", top: 0, left: 0, width: m[0], height: m[1], display: "none", opacity: a.startOpacity, zIndex: a.zIndex});
        a.color && c.css("backgroundColor", a.color);
        if (h(a.onBeforeLoad) === false)return this;
        a.closeOnEsc && b(document).bind("keydown.mask", function (f) {
            f.keyCode == 27 && b.mask.close(f)
        });
        a.closeOnClick && c.bind("click.mask", function (f) {
            b.mask.close(f)
        });
        b(window).bind("resize.mask", function () {
            b.mask.fit()
        });
        if (d && d.length) {
            j = d.eq(0).css("zIndex");
            b.each(d, function () {
                var f = b(this);
                /relative|absolute|fixed/i.test(f.css("position")) || f.css("position", "relative")
            });
            i = d.css({zIndex: Math.max(a.zIndex + 1, j == "auto" ? 0 : j)})
        }
        c.css({display: "block"}).fadeTo(a.loadSpeed, a.opacity, function () {
            b.mask.fit();
            h(a.onLoad);
            e = "full"
        });
        e = true;
        return this
    }, close: function () {
        if (e) {
            if (h(g.onBeforeClose) === false)return this;
            c.fadeOut(g.closeSpeed, function () {
                h(g.onClose);
                i && i.css({zIndex: j});
                e = false
            });
            b(document).unbind("keydown.mask");
            c.unbind("click.mask");
            b(window).unbind("resize.mask")
        }
        return this
    }, fit: function () {
        if (e) {
            var a = k();
            c.css({width: a[0], height: a[1]})
        }
    }, getMask: function () {
        return c
    }, isLoaded: function (a) {
        return a ? e == "full" : e
    }, getConf: function () {
        return g
    }, getExposed: function () {
        return i
    }};
    b.fn.mask = function (a) {
        b.mask.load(a);
        return this
    };
    b.fn.expose = function (a) {
        b.mask.load(a, this);
        return this
    }
})(jQuery);
(function (b) {
    function c(a) {
        switch (a.type) {
            case"mousemove":
                return b.extend(a.data, {clientX: a.clientX, clientY: a.clientY, pageX: a.pageX, pageY: a.pageY});
            case"DOMMouseScroll":
                b.extend(a, a.data);
                a.delta = -a.detail / 3;
                break;
            case"mousewheel":
                a.delta = a.wheelDelta / 120;
                break
        }
        a.type = "wheel";
        return b.event.handle.call(this, a, a.delta)
    }

    b.fn.mousewheel = function (a) {
        return this[a ? "bind" : "trigger"]("wheel", a)
    };
    b.event.special.wheel = {setup: function () {
        b.event.add(this, d, c, {})
    }, teardown: function () {
        b.event.remove(this, d, c)
    }};
    var d = !b.browser.mozilla ? "mousewheel" : "DOMMouseScroll" + (b.browser.version < "1.9" ? " mousemove" : "")
})(jQuery);
(function (c) {
    function p(d, b, a) {
        var e = this, l = d.add(this), h = d.find(a.tabs), i = b.jquery ? b : d.children(b), j;
        h.length || (h = d.children());
        i.length || (i = d.parent().find(b));
        i.length || (i = c(b));
        c.extend(this, {click: function (f, g) {
            var k = h.eq(f);
            if (typeof f == "string" && f.replace("#", "")) {
                k = h.filter("[href*=" + f.replace("#", "") + "]");
                f = Math.max(h.index(k), 0)
            }
            if (a.rotate) {
                var n = h.length - 1;
                if (f < 0)return e.click(n, g);
                if (f > n)return e.click(0, g)
            }
            if (!k.length) {
                if (j >= 0)return e;
                f = a.initialIndex;
                k = h.eq(f)
            }
            if (f === j)return e;
            g = g || c.Event();
            g.type = "onBeforeClick";
            l.trigger(g, [f]);
            if (!g.isDefaultPrevented()) {
                o[a.effect].call(e, f, function () {
                    g.type = "onClick";
                    l.trigger(g, [f])
                });
                j = f;
                h.removeClass(a.current);
                k.addClass(a.current);
                return e
            }
        }, getConf: function () {
            return a
        }, getTabs: function () {
            return h
        }, getPanes: function () {
            return i
        }, getCurrentPane: function () {
            return i.eq(j)
        }, getCurrentTab: function () {
            return h.eq(j)
        }, getIndex: function () {
            return j
        }, next: function () {
            return e.click(j + 1)
        }, prev: function () {
            return e.click(j - 1)
        }, destroy: function () {
            h.unbind(a.event).removeClass(a.current);
            i.find("a[href^=#]").unbind("click.T");
            return e
        }});
        c.each("onBeforeClick,onClick".split(","), function (f, g) {
            c.isFunction(a[g]) && c(e).bind(g, a[g]);
            e[g] = function (k) {
                k && c(e).bind(g, k);
                return e
            }
        });
        if (a.history && c.fn.history) {
            c.tools.history.init(h);
            a.event = "history"
        }
        h.each(function (f) {
            c(this).bind(a.event, function (g) {
                e.click(f, g);
                return g.preventDefault()
            })
        });
        i.find("a[href^=#]").bind("click.T", function (f) {
            e.click(c(this).attr("href"), f)
        });
        if (location.hash && a.tabs == "a" && d.find("[href=" + location.hash + "]").length)e.click(location.hash); else if (a.initialIndex === 0 || a.initialIndex > 0)e.click(a.initialIndex)
    }

    c.tools = c.tools || {version: "1.2.5"};
    c.tools.tabs = {conf: {tabs: "a", current: "current", onBeforeClick: null, onClick: null, effect: "default", initialIndex: 0, event: "click", rotate: false, history: false}, addEffect: function (d, b) {
        o[d] = b
    }};
    var o = {"default": function (d, b) {
        this.getPanes().hide().eq(d).show();
        b.call()
    }, fade: function (d, b) {
        var a = this.getConf(), e = a.fadeOutSpeed, l = this.getPanes();
        e ? l.fadeOut(e) : l.hide();
        l.eq(d).fadeIn(a.fadeInSpeed, b)
    }, slide: function (d, b) {
        this.getPanes().slideUp(200);
        this.getPanes().eq(d).slideDown(400, b)
    }, ajax: function (d, b) {
        this.getPanes().eq(0).load(this.getTabs().eq(d).attr("href"), b)
    }}, m;
    c.tools.tabs.addEffect("horizontal", function (d, b) {
        m || (m = this.getPanes().eq(0).width());
        this.getCurrentPane().animate({width: 0}, function () {
            c(this).hide()
        });
        this.getPanes().eq(d).animate({width: m}, function () {
            c(this).show();
            b.call()
        })
    });
    c.fn.tabs = function (d, b) {
        var a = this.data("tabs");
        if (a) {
            a.destroy();
            this.removeData("tabs")
        }
        if (c.isFunction(b))b = {onBeforeClick: b};
        b = c.extend({}, c.tools.tabs.conf, b);
        this.each(function () {
            a = new p(c(this), d, b);
            c(this).data("tabs", a)
        });
        return b.api ? a : this
    }
})(jQuery);
(function (c) {
    function p(g, a) {
        function m(f) {
            var e = c(f);
            return e.length < 2 ? e : g.parent().find(f)
        }

        var b = this, i = g.add(this), d = g.data("tabs"), h, j = true, n = m(a.next).click(function () {
            d.next()
        }), k = m(a.prev).click(function () {
            d.prev()
        });
        c.extend(b, {getTabs: function () {
            return d
        }, getConf: function () {
            return a
        }, play: function () {
            if (h)return b;
            var f = c.Event("onBeforePlay");
            i.trigger(f);
            if (f.isDefaultPrevented())return b;
            h = setInterval(d.next, a.interval);
            j = false;
            i.trigger("onPlay");
            return b
        }, pause: function () {
            if (!h)return b;
            var f = c.Event("onBeforePause");
            i.trigger(f);
            if (f.isDefaultPrevented())return b;
            h = clearInterval(h);
            i.trigger("onPause");
            return b
        }, stop: function () {
            b.pause();
            j = true
        }});
        c.each("onBeforePlay,onPlay,onBeforePause,onPause".split(","), function (f, e) {
            c.isFunction(a[e]) && c(b).bind(e, a[e]);
            b[e] = function (q) {
                return c(b).bind(e, q)
            }
        });
        a.autopause && d.getTabs().add(n).add(k).add(d.getPanes()).hover(b.pause, function () {
            j || b.play()
        });
        a.autoplay && b.play();
        a.clickable && d.getPanes().click(function () {
            d.next()
        });
        if (!d.getConf().rotate) {
            var l = a.disabledClass;
            d.getIndex() || k.addClass(l);
            d.onBeforeClick(function (f, e) {
                k.toggleClass(l, !e);
                n.toggleClass(l, e == d.getTabs().length - 1)
            })
        }
    }

    var o;
    o = c.tools.tabs.slideshow = {conf: {next: ".forward", prev: ".backward", disabledClass: "disabled", autoplay: false, autopause: true, interval: 3E3, clickable: true, api: false}};
    c.fn.slideshow = function (g) {
        var a = this.data("slideshow");
        if (a)return a;
        g = c.extend({}, o.conf, g);
        this.each(function () {
            a = new p(c(this), g);
            c(this).data("slideshow", a)
        });
        return g.api ? a : this
    }
})(jQuery);
(function (f) {
    function p(a, b, c) {
        var h = c.relative ? a.position().top : a.offset().top, d = c.relative ? a.position().left : a.offset().left, i = c.position[0];
        h -= b.outerHeight() - c.offset[0];
        d += a.outerWidth() + c.offset[1];
        if (/iPad/i.test(navigator.userAgent))h -= f(window).scrollTop();
        var j = b.outerHeight() + a.outerHeight();
        if (i == "center")h += j / 2;
        if (i == "bottom")h += j;
        i = c.position[1];
        a = b.outerWidth() + a.outerWidth();
        if (i == "center")d -= a / 2;
        if (i == "left")d -= a;
        return{top: h, left: d}
    }

    function u(a, b) {
        var c = this, h = a.add(c), d, i = 0, j = 0, m = a.attr("title"), q = a.attr("data-tooltip"), r = o[b.effect], l, s = a.is(":input"), v = s && a.is(":checkbox, :radio, select, :button, :submit"), t = a.attr("type"), k = b.events[t] || b.events[s ? v ? "widget" : "input" : "def"];
        if (!r)throw'Nonexistent effect "' + b.effect + '"';
        k = k.split(/,\s*/);
        if (k.length != 2)throw"Tooltip: bad events configuration for " + t;
        a.bind(k[0],function (e) {
            clearTimeout(i);
            if (b.predelay)j = setTimeout(function () {
                c.show(e)
            }, b.predelay); else c.show(e)
        }).bind(k[1], function (e) {
            clearTimeout(j);
            if (b.delay)i = setTimeout(function () {
                c.hide(e)
            }, b.delay); else c.hide(e)
        });
        if (m && b.cancelDefault) {
            a.removeAttr("title");
            a.data("title", m)
        }
        f.extend(c, {show: function (e) {
            if (!d) {
                if (q)d = f(q); else if (b.tip)d = f(b.tip).eq(0); else if (m)d = f(b.layout).addClass(b.tipClass).appendTo(document.body).hide().append(m); else {
                    d = a.next();
                    d.length || (d = a.parent().next())
                }
                if (!d.length)throw"Cannot find tooltip for " + a;
            }
            if (c.isShown())return c;
            d.stop(true, true);
            var g = p(a, d, b);
            b.tip && d.html(a.data("title"));
            e = e || f.Event();
            e.type = "onBeforeShow";
            h.trigger(e, [g]);
            if (e.isDefaultPrevented())return c;
            g = p(a, d, b);
            d.css({position: "absolute", top: g.top, left: g.left});
            l = true;
            r[0].call(c, function () {
                e.type = "onShow";
                l = "full";
                h.trigger(e)
            });
            g = b.events.tooltip.split(/,\s*/);
            if (!d.data("__set")) {
                d.bind(g[0], function () {
                    clearTimeout(i);
                    clearTimeout(j)
                });
                g[1] && !a.is("input:not(:checkbox, :radio), textarea") && d.bind(g[1], function (n) {
                    n.relatedTarget != a[0] && a.trigger(k[1].split(" ")[0])
                });
                d.data("__set", true)
            }
            return c
        }, hide: function (e) {
            if (!d || !c.isShown())return c;
            e = e || f.Event();
            e.type = "onBeforeHide";
            h.trigger(e);
            if (!e.isDefaultPrevented()) {
                l = false;
                o[b.effect][1].call(c, function () {
                    e.type = "onHide";
                    h.trigger(e)
                });
                return c
            }
        }, isShown: function (e) {
            return e ? l == "full" : l
        }, getConf: function () {
            return b
        }, getTip: function () {
            return d
        }, getTrigger: function () {
            return a
        }});
        f.each("onHide,onBeforeShow,onShow,onBeforeHide".split(","), function (e, g) {
            f.isFunction(b[g]) && f(c).bind(g, b[g]);
            c[g] = function (n) {
                n && f(c).bind(g, n);
                return c
            }
        })
    }

    f.tools = f.tools || {version: "1.2.5"};
    f.tools.tooltip = {conf: {effect: "toggle", fadeOutSpeed: "fast", predelay: 0, delay: 30, opacity: 1, tip: 0, position: ["top", "center"], offset: [0, 0], relative: false, cancelDefault: true, events: {def: "mouseenter,mouseleave", input: "focus,blur", widget: "focus mouseenter,blur mouseleave", tooltip: "mouseenter,mouseleave"}, layout: "<div/>", tipClass: "tooltip"}, addEffect: function (a, b, c) {
        o[a] = [b, c]
    }};
    var o = {toggle: [function (a) {
        var b = this.getConf(), c = this.getTip();
        b = b.opacity;
        b < 1 && c.css({opacity: b});
        c.show();
        a.call()
    }, function (a) {
        this.getTip().hide();
        a.call()
    }], fade: [function (a) {
        var b = this.getConf();
        this.getTip().fadeTo(b.fadeInSpeed, b.opacity, a)
    }, function (a) {
        this.getTip().fadeOut(this.getConf().fadeOutSpeed, a)
    }]};
    f.fn.tooltip = function (a) {
        var b = this.data("tooltip");
        if (b)return b;
        a = f.extend(true, {}, f.tools.tooltip.conf, a);
        if (typeof a.position == "string")a.position = a.position.split(/,?\s/);
        this.each(function () {
            b = new u(f(this), a);
            f(this).data("tooltip", b)
        });
        return a.api ? b : this
    }
})(jQuery);
(function (d) {
    var i = d.tools.tooltip;
    d.extend(i.conf, {direction: "up", bounce: false, slideOffset: 10, slideInSpeed: 200, slideOutSpeed: 200, slideFade: !d.browser.msie});
    var e = {up: ["-", "top"], down: ["+", "top"], left: ["-", "left"], right: ["+", "left"]};
    i.addEffect("slide", function (g) {
        var a = this.getConf(), f = this.getTip(), b = a.slideFade ? {opacity: a.opacity} : {}, c = e[a.direction] || e.up;
        b[c[1]] = c[0] + "=" + a.slideOffset;
        a.slideFade && f.css({opacity: 0});
        f.show().animate(b, a.slideInSpeed, g)
    }, function (g) {
        var a = this.getConf(), f = a.slideOffset, b = a.slideFade ? {opacity: 0} : {}, c = e[a.direction] || e.up, h = "" + c[0];
        if (a.bounce)h = h == "+" ? "-" : "+";
        b[c[1]] = h + "=" + f;
        this.getTip().animate(b, a.slideOutSpeed, function () {
            d(this).hide();
            g.call()
        })
    })
})(jQuery);
(function (g) {
    function j(a) {
        var c = g(window), d = c.width() + c.scrollLeft(), h = c.height() + c.scrollTop();
        return[a.offset().top <= c.scrollTop(), d <= a.offset().left + a.width(), h <= a.offset().top + a.height(), c.scrollLeft() >= a.offset().left]
    }

    function k(a) {
        for (var c = a.length; c--;)if (a[c])return false;
        return true
    }

    var i = g.tools.tooltip;
    i.dynamic = {conf: {classNames: "top right bottom left"}};
    g.fn.dynamic = function (a) {
        if (typeof a == "number")a = {speed: a};
        a = g.extend({}, i.dynamic.conf, a);
        var c = a.classNames.split(/\s/), d;
        this.each(function () {
            var h = g(this).tooltip().onBeforeShow(function (e, f) {
                e = this.getTip();
                var b = this.getConf();
                d || (d = [b.position[0], b.position[1], b.offset[0], b.offset[1], g.extend({}, b)]);
                g.extend(b, d[4]);
                b.position = [d[0], d[1]];
                b.offset = [d[2], d[3]];
                e.css({visibility: "hidden", position: "absolute", top: f.top, left: f.left}).show();
                f = j(e);
                if (!k(f)) {
                    if (f[2]) {
                        g.extend(b, a.top);
                        b.position[0] = "top";
                        e.addClass(c[0])
                    }
                    if (f[3]) {
                        g.extend(b, a.right);
                        b.position[1] = "right";
                        e.addClass(c[1])
                    }
                    if (f[0]) {
                        g.extend(b, a.bottom);
                        b.position[0] = "bottom";
                        e.addClass(c[2])
                    }
                    if (f[1]) {
                        g.extend(b, a.left);
                        b.position[1] = "left";
                        e.addClass(c[3])
                    }
                    if (f[0] || f[2])b.offset[0] *= -1;
                    if (f[1] || f[3])b.offset[1] *= -1
                }
                e.css({visibility: "visible"}).hide()
            });
            h.onBeforeShow(function () {
                var e = this.getConf();
                this.getTip();
                setTimeout(function () {
                    e.position = [d[0], d[1]];
                    e.offset = [d[2], d[3]]
                }, 0)
            });
            h.onHide(function () {
                var e = this.getTip();
                e.removeClass(a.classNames)
            });
            ret = h
        });
        return a.api ? ret : this
    }
})(jQuery);
(function (e) {
    function p(f, c) {
        var b = e(c);
        return b.length < 2 ? b : f.parent().find(c)
    }

    function u(f, c) {
        var b = this, n = f.add(b), g = f.children(), l = 0, j = c.vertical;
        k || (k = b);
        if (g.length > 1)g = e(c.items, f);
        e.extend(b, {getConf: function () {
            return c
        }, getIndex: function () {
            return l
        }, getSize: function () {
            return b.getItems().size()
        }, getNaviButtons: function () {
            return o.add(q)
        }, getRoot: function () {
            return f
        }, getItemWrap: function () {
            return g
        }, getItems: function () {
            return g.children(c.item).not("." + c.clonedClass)
        }, move: function (a, d) {
            return b.seekTo(l +
                a, d)
        }, next: function (a) {
            return b.move(1, a)
        }, prev: function (a) {
            return b.move(-1, a)
        }, begin: function (a) {
            return b.seekTo(0, a)
        }, end: function (a) {
            return b.seekTo(b.getSize() - 1, a)
        }, focus: function () {
            return k = b
        }, addItem: function (a) {
            a = e(a);
            if (c.circular) {
                g.children("." + c.clonedClass + ":last").before(a);
                g.children("." + c.clonedClass + ":first").replaceWith(a.clone().addClass(c.clonedClass))
            } else g.append(a);
            n.trigger("onAddItem", [a]);
            return b
        }, seekTo: function (a, d, h) {
            a.jquery || (a *= 1);
            if (c.circular && a === 0 && l == -1 && d !== 0)return b;
            if (!c.circular && a < 0 || a > b.getSize() || a < -1)return b;
            var i = a;
            if (a.jquery)a = b.getItems().index(a); else i = b.getItems().eq(a);
            var r = e.Event("onBeforeSeek");
            if (!h) {
                n.trigger(r, [a, d]);
                if (r.isDefaultPrevented() || !i.length)return b
            }
            i = j ? {top: -i.position().top} : {left: -i.position().left};
            l = a;
            k = b;
            if (d === undefined)d = c.speed;
            g.animate(i, d, c.easing, h || function () {
                n.trigger("onSeek", [a])
            });
            return b
        }});
        e.each(["onBeforeSeek", "onSeek", "onAddItem"], function (a, d) {
            e.isFunction(c[d]) && e(b).bind(d, c[d]);
            b[d] = function (h) {
                h && e(b).bind(d, h);
                return b
            }
        });
        if (c.circular) {
            var s = b.getItems().slice(-1).clone().prependTo(g), t = b.getItems().eq(1).clone().appendTo(g);
            s.add(t).addClass(c.clonedClass);
            b.onBeforeSeek(function (a, d, h) {
                if (!a.isDefaultPrevented())if (d == -1) {
                    b.seekTo(s, h, function () {
                        b.end(0)
                    });
                    return a.preventDefault()
                } else d == b.getSize() && b.seekTo(t, h, function () {
                    b.begin(0)
                })
            });
            b.seekTo(0, 0, function () {
            })
        }
        var o = p(f, c.prev).click(function () {
            b.prev()
        }), q = p(f, c.next).click(function () {
            b.next()
        });
        if (!c.circular && b.getSize() > 1) {
            b.onBeforeSeek(function (a, d) {
                setTimeout(function () {
                    if (!a.isDefaultPrevented()) {
                        o.toggleClass(c.disabledClass, d <= 0);
                        q.toggleClass(c.disabledClass, d >= b.getSize() - 1)
                    }
                }, 1)
            });
            c.initialIndex || o.addClass(c.disabledClass)
        }
        c.mousewheel && e.fn.mousewheel && f.mousewheel(function (a, d) {
            if (c.mousewheel) {
                b.move(d < 0 ? 1 : -1, c.wheelSpeed || 50);
                return false
            }
        });
        if (c.touch) {
            var m = {};
            g[0].ontouchstart = function (a) {
                a = a.touches[0];
                m.x = a.clientX;
                m.y = a.clientY
            };
            g[0].ontouchmove = function (a) {
                if (a.touches.length == 1 && !g.is(":animated")) {
                    var d = a.touches[0], h = m.x - d.clientX;
                    d = m.y - d.clientY;
                    b[j && d > 0 || !j && h > 0 ? "next" : "prev"]();
                    a.preventDefault()
                }
            }
        }
        c.keyboard && e(document).bind("keydown.scrollable", function (a) {
            if (!(!c.keyboard || a.altKey || a.ctrlKey || e(a.target).is(":input")))if (!(c.keyboard != "static" && k != b)) {
                var d = a.keyCode;
                if (j && (d == 38 || d == 40)) {
                    b.move(d == 38 ? -1 : 1);
                    return a.preventDefault()
                }
                if (!j && (d == 37 || d == 39)) {
                    b.move(d == 37 ? -1 : 1);
                    return a.preventDefault()
                }
            }
        });
        c.initialIndex && b.seekTo(c.initialIndex, 0, function () {
        })
    }

    e.tools = e.tools || {version: "1.2.5"};
    e.tools.scrollable = {conf: {activeClass: "active", circular: false, clonedClass: "cloned", disabledClass: "disabled", easing: "swing", initialIndex: 0, item: null, items: ".items", keyboard: true, mousewheel: false, next: ".next", prev: ".prev", speed: 400, vertical: false, touch: true, wheelSpeed: 0}};
    var k;
    e.fn.scrollable = function (f) {
        var c = this.data("scrollable");
        if (c)return c;
        f = e.extend({}, e.tools.scrollable.conf, f);
        this.each(function () {
            c = new u(e(this), f);
            e(this).data("scrollable", c)
        });
        return f.api ? c : this
    }
})(jQuery);
(function (b) {
    var f = b.tools.scrollable;
    f.autoscroll = {conf: {autoplay: true, interval: 3E3, autopause: true}};
    b.fn.autoscroll = function (c) {
        if (typeof c == "number")c = {interval: c};
        var d = b.extend({}, f.autoscroll.conf, c), g;
        this.each(function () {
            var a = b(this).data("scrollable");
            if (a)g = a;
            var e, h = true;
            a.play = function () {
                if (!e) {
                    h = false;
                    e = setInterval(function () {
                        a.next()
                    }, d.interval)
                }
            };
            a.pause = function () {
                e = clearInterval(e)
            };
            a.stop = function () {
                a.pause();
                h = true
            };
            d.autopause && a.getRoot().add(a.getNaviButtons()).hover(a.pause, a.play);
            d.autoplay && a.play()
        });
        return d.api ? g : this
    }
})(jQuery);
(function (d) {
    function p(b, g) {
        var h = d(g);
        return h.length < 2 ? h : b.parent().find(g)
    }

    var m = d.tools.scrollable;
    m.navigator = {conf: {navi: ".navi", naviItem: null, activeClass: "active", indexed: false, idPrefix: null, history: false}};
    d.fn.navigator = function (b) {
        if (typeof b == "string")b = {navi: b};
        b = d.extend({}, m.navigator.conf, b);
        var g;
        this.each(function () {
            function h(a, c, i) {
                e.seekTo(c);
                if (j) {
                    if (location.hash)location.hash = a.attr("href").replace("#", "")
                } else return i.preventDefault()
            }

            function f() {
                return k.find(b.naviItem || "> *")
            }

            function n(a) {
                var c = d("<" + (b.naviItem || "a") + "/>").click(function (i) {
                    h(d(this), a, i)
                }).attr("href", "#" + a);
                a === 0 && c.addClass(l);
                b.indexed && c.text(a + 1);
                b.idPrefix && c.attr("id", b.idPrefix + a);
                return c.appendTo(k)
            }

            function o(a, c) {
                a = f().eq(c.replace("#", ""));
                a.length || (a = f().filter("[href=" + c + "]"));
                a.click()
            }

            var e = d(this).data("scrollable"), k = b.navi.jquery ? b.navi : p(e.getRoot(), b.navi), q = e.getNaviButtons(), l = b.activeClass, j = b.history && d.fn.history;
            if (e)g = e;
            e.getNaviButtons = function () {
                return q.add(k)
            };
            f().length ? f().each(function (a) {
                d(this).click(function (c) {
                    h(d(this), a, c)
                })
            }) : d.each(e.getItems(), function (a) {
                n(a)
            });
            e.onBeforeSeek(function (a, c) {
                setTimeout(function () {
                    if (!a.isDefaultPrevented()) {
                        var i = f().eq(c);
                        !a.isDefaultPrevented() && i.length && f().removeClass(l).eq(c).addClass(l)
                    }
                }, 1)
            });
            e.onAddItem(function (a, c) {
                c = n(e.getItems().index(c));
                j && c.history(o)
            });
            j && f().history(o)
        });
        return b.api ? g : this
    }
})(jQuery);
(function (a) {
    function t(d, b) {
        var c = this, j = d.add(c), o = a(window), k, f, m, g = a.tools.expose && (b.mask || b.expose), n = Math.random().toString().slice(10);
        if (g) {
            if (typeof g == "string")g = {color: g};
            g.closeOnClick = g.closeOnEsc = false
        }
        var p = b.target || d.attr("rel");
        f = p ? a(p) : d;
        if (!f.length)throw"Could not find Overlay: " + p;
        d && d.index(f) == -1 && d.click(function (e) {
            c.load(e);
            return e.preventDefault()
        });
        a.extend(c, {load: function (e) {
            if (c.isOpened())return c;
            var h = q[b.effect];
            if (!h)throw'Overlay: cannot find effect : "' + b.effect + '"';
            b.oneInstance && a.each(s, function () {
                this.close(e)
            });
            e = e || a.Event();
            e.type = "onBeforeLoad";
            j.trigger(e);
            if (e.isDefaultPrevented())return c;
            m = true;
            g && a(f).expose(g);
            var i = b.top, r = b.left, u = f.outerWidth({margin: true}), v = f.outerHeight({margin: true});
            if (typeof i == "string")i = i == "center" ? Math.max((o.height() - v) / 2, 0) : parseInt(i, 10) / 100 * o.height();
            if (r == "center")r = Math.max((o.width() - u) / 2, 0);
            h[0].call(c, {top: i, left: r}, function () {
                if (m) {
                    e.type = "onLoad";
                    j.trigger(e)
                }
            });
            g && b.closeOnClick && a.mask.getMask().one("click", c.close);
            b.closeOnClick && a(document).bind("click." + n, function (l) {
                a(l.target).parents(f).length || c.close(l)
            });
            b.closeOnEsc && a(document).bind("keydown." + n, function (l) {
                l.keyCode == 27 && c.close(l)
            });
            return c
        }, close: function (e) {
            if (!c.isOpened())return c;
            e = e || a.Event();
            e.type = "onBeforeClose";
            j.trigger(e);
            if (!e.isDefaultPrevented()) {
                m = false;
                q[b.effect][1].call(c, function () {
                    e.type = "onClose";
                    j.trigger(e)
                });
                a(document).unbind("click." + n).unbind("keydown." + n);
                g && a.mask.close();
                return c
            }
        }, getOverlay: function () {
            return f
        }, getTrigger: function () {
            return d
        }, getClosers: function () {
            return k
        }, isOpened: function () {
            return m
        }, getConf: function () {
            return b
        }});
        a.each("onBeforeLoad,onStart,onLoad,onBeforeClose,onClose".split(","), function (e, h) {
            a.isFunction(b[h]) && a(c).bind(h, b[h]);
            c[h] = function (i) {
                i && a(c).bind(h, i);
                return c
            }
        });
        k = f.find(b.close || ".close");
        if (!k.length && !b.close) {
            k = a('<a class="close"></a>');
            f.prepend(k)
        }
        k.click(function (e) {
            c.close(e)
        });
        b.load && c.load()
    }

    a.tools = a.tools || {version: "1.2.5"};
    a.tools.overlay = {addEffect: function (d, b, c) {
        q[d] = [b, c]
    }, conf: {close: null, closeOnClick: true, closeOnEsc: true, closeSpeed: "fast", effect: "default", fixed: !a.browser.msie || a.browser.version > 6, left: "center", load: false, mask: null, oneInstance: true, speed: "normal", target: null, top: "10%"}};
    var s = [], q = {};
    a.tools.overlay.addEffect("default", function (d, b) {
        var c = this.getConf(), j = a(window);
        if (!c.fixed) {
            d.top += j.scrollTop();
            d.left += j.scrollLeft()
        }
        d.position = c.fixed ? "fixed" : "absolute";
        this.getOverlay().css(d).fadeIn(c.speed, b)
    }, function (d) {
        this.getOverlay().fadeOut(this.getConf().closeSpeed, d)
    });
    a.fn.overlay = function (d) {
        var b = this.data("overlay");
        if (b)return b;
        if (a.isFunction(d))d = {onBeforeLoad: d};
        d = a.extend(true, {}, a.tools.overlay.conf, d);
        this.each(function () {
            b = new t(a(this), d);
            s.push(b);
            a(this).data("overlay", b)
        });
        return d.api ? b : this
    }
})(jQuery);
(function (h) {
    function k(d) {
        var e = d.offset();
        return{top: e.top + d.height() / 2, left: e.left + d.width() / 2}
    }

    var l = h.tools.overlay, f = h(window);
    h.extend(l.conf, {start: {top: null, left: null}, fadeInSpeed: "fast", zIndex: 9999});
    function o(d, e) {
        var a = this.getOverlay(), c = this.getConf(), g = this.getTrigger(), p = this, m = a.outerWidth({margin: true}), b = a.data("img"), n = c.fixed ? "fixed" : "absolute";
        if (!b) {
            b = a.css("backgroundImage");
            if (!b)throw"background-image CSS property not set for overlay";
            b = b.slice(b.indexOf("(") + 1, b.indexOf(")")).replace(/\"/g, "");
            a.css("backgroundImage", "none");
            b = h('<img src="' + b + '"/>');
            b.css({border: 0, display: "none"}).width(m);
            h("body").append(b);
            a.data("img", b)
        }
        var i = c.start.top || Math.round(f.height() / 2), j = c.start.left || Math.round(f.width() / 2);
        if (g) {
            g = k(g);
            i = g.top;
            j = g.left
        }
        if (c.fixed) {
            i -= f.scrollTop();
            j -= f.scrollLeft()
        } else {
            d.top += f.scrollTop();
            d.left += f.scrollLeft()
        }
        b.css({position: "absolute", top: i, left: j, width: 0, zIndex: c.zIndex}).show();
        d.position = n;
        a.css(d);
        b.animate({top: a.css("top"), left: a.css("left"), width: m}, c.speed,function () {
            a.css("zIndex", c.zIndex + 1).fadeIn(c.fadeInSpeed, function () {
                p.isOpened() && !h(this).index(a) ? e.call() : a.hide()
            })
        }).css("position", n)
    }

    function q(d) {
        var e = this.getOverlay().hide(), a = this.getConf(), c = this.getTrigger();
        e = e.data("img");
        var g = {top: a.start.top, left: a.start.left, width: 0};
        c && h.extend(g, k(c));
        a.fixed && e.css({position: "absolute"}).animate({top: "+=" + f.scrollTop(), left: "+=" + f.scrollLeft()}, 0);
        e.animate(g, a.closeSpeed, d)
    }

    l.addEffect("apple", o, q)
})(jQuery);
(function (d) {
    function R(a, c) {
        return 32 - (new Date(a, c, 32)).getDate()
    }

    function S(a, c) {
        a = "" + a;
        for (c = c || 2; a.length < c;)a = "0" + a;
        return a
    }

    function T(a, c, j) {
        var q = a.getDate(), h = a.getDay(), r = a.getMonth();
        a = a.getFullYear();
        var f = {d: q, dd: S(q), ddd: B[j].shortDays[h], dddd: B[j].days[h], m: r + 1, mm: S(r + 1), mmm: B[j].shortMonths[r], mmmm: B[j].months[r], yy: String(a).slice(2), yyyy: a};
        c = c.replace(X, function (s) {
            return s in f ? f[s] : s.slice(1, s.length - 1)
        });
        return Y.html(c).html()
    }

    function v(a) {
        return parseInt(a, 10)
    }

    function U(a, c) {
        return a.getFullYear() === c.getFullYear() && a.getMonth() == c.getMonth() && a.getDate() == c.getDate()
    }

    function C(a) {
        if (a) {
            if (a.constructor == Date)return a;
            if (typeof a == "string") {
                var c = a.split("-");
                if (c.length == 3)return new Date(v(c[0]), v(c[1]) - 1, v(c[2]));
                if (!/^-?\d+$/.test(a))return;
                a = v(a)
            }
            c = new Date;
            c.setDate(c.getDate() + a);
            return c
        }
    }

    function Z(a, c) {
        function j(b, e, g) {
            n = b;
            D = b.getFullYear();
            E = b.getMonth();
            G = b.getDate();
            g = g || d.Event("api");
            g.type = "change";
            H.trigger(g, [b]);
            if (!g.isDefaultPrevented()) {
                a.val(T(b, e.format, e.lang));
                a.data("date", b);
                h.hide(g)
            }
        }

        function q(b) {
            b.type = "onShow";
            H.trigger(b);
            d(document).bind("keydown.d", function (e) {
                if (e.ctrlKey)return true;
                var g = e.keyCode;
                if (g == 8) {
                    a.val("");
                    return h.hide(e)
                }
                if (g == 27)return h.hide(e);
                if (d(V).index(g) >= 0) {
                    if (!w) {
                        h.show(e);
                        return e.preventDefault()
                    }
                    var i = d("#" + f.weeks + " a"), t = d("." + f.focus), o = i.index(t);
                    t.removeClass(f.focus);
                    if (g == 74 || g == 40)o += 7; else if (g == 75 || g == 38)o -= 7; else if (g == 76 || g == 39)o += 1; else if (g == 72 || g == 37)o -= 1;
                    if (o > 41) {
                        h.addMonth();
                        t = d("#" +
                            f.weeks + " a:eq(" + (o - 42) + ")")
                    } else if (o < 0) {
                        h.addMonth(-1);
                        t = d("#" + f.weeks + " a:eq(" + (o + 42) + ")")
                    } else t = i.eq(o);
                    t.addClass(f.focus);
                    return e.preventDefault()
                }
                if (g == 34)return h.addMonth();
                if (g == 33)return h.addMonth(-1);
                if (g == 36)return h.today();
                if (g == 13)d(e.target).is("select") || d("." + f.focus).click();
                return d([16, 17, 18, 9]).index(g) >= 0
            });
            d(document).bind("click.d", function (e) {
                var g = e.target;
                if (!d(g).parents("#" + f.root).length && g != a[0] && (!L || g != L[0]))h.hide(e)
            })
        }

        var h = this, r = new Date, f = c.css, s = B[c.lang], k = d("#" + f.root), M = k.find("#" + f.title), L, I, J, D, E, G, n = a.attr("data-value") || c.value || a.val(), m = a.attr("min") || c.min, p = a.attr("max") || c.max, w;
        if (m === 0)m = "0";
        n = C(n) || r;
        m = C(m || c.yearRange[0] * 365);
        p = C(p || c.yearRange[1] * 365);
        if (!s)throw"Dateinput: invalid language: " + c.lang;
        if (a.attr("type") == "date") {
            var N = d("<input/>");
            d.each("class,disabled,id,maxlength,name,readonly,required,size,style,tabindex,title,value".split(","), function (b, e) {
                N.attr(e, a.attr(e))
            });
            a.replaceWith(N);
            a = N
        }
        a.addClass(f.input);
        var H = a.add(h);
        if (!k.length) {
            k = d("<div><div><a/><div/><a/></div><div><div/><div/></div></div>").hide().css({position: "absolute"}).attr("id", f.root);
            k.children().eq(0).attr("id", f.head).end().eq(1).attr("id", f.body).children().eq(0).attr("id", f.days).end().eq(1).attr("id", f.weeks).end().end().end().find("a").eq(0).attr("id", f.prev).end().eq(1).attr("id", f.next);
            M = k.find("#" + f.head).find("div").attr("id", f.title);
            if (c.selectors) {
                var z = d("<select/>").attr("id", f.month), A = d("<select/>").attr("id", f.year);
                M.html(z.add(A))
            }
            for (var $ = k.find("#" + f.days), O = 0; O < 7; O++)$.append(d("<span/>").text(s.shortDays[(O + c.firstDay) % 7]));
            d("body").append(k)
        }
        if (c.trigger)L = d("<a/>").attr("href", "#").addClass(f.trigger).click(function (b) {
            h.show();
            return b.preventDefault()
        }).insertAfter(a);
        var K = k.find("#" + f.weeks);
        A = k.find("#" + f.year);
        z = k.find("#" + f.month);
        d.extend(h, {show: function (b) {
            if (!(a.attr("readonly") || a.attr("disabled") || w)) {
                b = b || d.Event();
                b.type = "onBeforeShow";
                H.trigger(b);
                if (!b.isDefaultPrevented()) {
                    d.each(W, function () {
                        this.hide()
                    });
                    w = true;
                    z.unbind("change").change(function () {
                        h.setValue(A.val(), d(this).val())
                    });
                    A.unbind("change").change(function () {
                        h.setValue(d(this).val(), z.val())
                    });
                    I = k.find("#" + f.prev).unbind("click").click(function () {
                        I.hasClass(f.disabled) || h.addMonth(-1);
                        return false
                    });
                    J = k.find("#" + f.next).unbind("click").click(function () {
                        J.hasClass(f.disabled) || h.addMonth();
                        return false
                    });
                    h.setValue(n);
                    var e = a.offset();
                    if (/iPad/i.test(navigator.userAgent))e.top -= d(window).scrollTop();
                    k.css({top: e.top + a.outerHeight({margins: true}) +
                        c.offset[0], left: e.left + c.offset[1]});
                    if (c.speed)k.show(c.speed, function () {
                        q(b)
                    }); else {
                        k.show();
                        q(b)
                    }
                    return h
                }
            }
        }, setValue: function (b, e, g) {
            var i = v(e) >= -1 ? new Date(v(b), v(e), v(g || 1)) : b || n;
            if (i < m)i = m; else if (i > p)i = p;
            b = i.getFullYear();
            e = i.getMonth();
            g = i.getDate();
            if (e == -1) {
                e = 11;
                b--
            } else if (e == 12) {
                e = 0;
                b++
            }
            if (!w) {
                j(i, c);
                return h
            }
            E = e;
            D = b;
            g = new Date(b, e, 1 - c.firstDay);
            g = g.getDay();
            var t = R(b, e), o = R(b, e - 1), P;
            if (c.selectors) {
                z.empty();
                d.each(s.months, function (x, F) {
                    m < new Date(b, x + 1, -1) && p > new Date(b, x, 0) && z.append(d("<option/>").html(F).attr("value", x))
                });
                A.empty();
                i = r.getFullYear();
                for (var l = i + c.yearRange[0]; l < i + c.yearRange[1]; l++)m <= new Date(l + 1, -1, 1) && p > new Date(l, 0, 0) && A.append(d("<option/>").text(l));
                z.val(e);
                A.val(b)
            } else M.html(s.months[e] + " " + b);
            K.empty();
            I.add(J).removeClass(f.disabled);
            l = !g ? -7 : 0;
            for (var u, y; l < (!g ? 35 : 42); l++) {
                u = d("<a/>");
                if (l % 7 === 0) {
                    P = d("<div/>").addClass(f.week);
                    K.append(P)
                }
                if (l < g) {
                    u.addClass(f.off);
                    y = o - g + l + 1;
                    i = new Date(b, e - 1, y)
                } else if (l >= g + t) {
                    u.addClass(f.off);
                    y = l - t - g + 1;
                    i = new Date(b, e + 1, y)
                } else {
                    y = l - g + 1;
                    i = new Date(b, e, y);
                    if (U(n, i))u.attr("id", f.current).addClass(f.focus); else U(r, i) && u.attr("id", f.today)
                }
                m && i < m && u.add(I).addClass(f.disabled);
                p && i > p && u.add(J).addClass(f.disabled);
                u.attr("href", "#" + y).text(y).data("date", i);
                P.append(u)
            }
            K.find("a").click(function (x) {
                var F = d(this);
                if (!F.hasClass(f.disabled)) {
                    d("#" + f.current).removeAttr("id");
                    F.attr("id", f.current);
                    j(F.data("date"), c, x)
                }
                return false
            });
            f.sunday && K.find(f.week).each(function () {
                var x = c.firstDay ? 7 - c.firstDay : 0;
                d(this).children().slice(x, x + 1).addClass(f.sunday)
            });
            return h
        }, setMin: function (b, e) {
            m = C(b);
            e && n < m && h.setValue(m);
            return h
        }, setMax: function (b, e) {
            p = C(b);
            e && n > p && h.setValue(p);
            return h
        }, today: function () {
            return h.setValue(r)
        }, addDay: function (b) {
            return this.setValue(D, E, G + (b || 1))
        }, addMonth: function (b) {
            return this.setValue(D, E + (b || 1), G)
        }, addYear: function (b) {
            return this.setValue(D + (b || 1), E, G)
        }, hide: function (b) {
            if (w) {
                b = d.Event();
                b.type = "onHide";
                H.trigger(b);
                d(document).unbind("click.d").unbind("keydown.d");
                if (b.isDefaultPrevented())return;
                k.hide();
                w = false
            }
            return h
        }, getConf: function () {
            return c
        }, getInput: function () {
            return a
        }, getCalendar: function () {
            return k
        }, getValue: function (b) {
            return b ? T(n, b, c.lang) : n
        }, isOpen: function () {
            return w
        }});
        d.each(["onBeforeShow", "onShow", "change", "onHide"], function (b, e) {
            d.isFunction(c[e]) && d(h).bind(e, c[e]);
            h[e] = function (g) {
                g && d(h).bind(e, g);
                return h
            }
        });
        a.bind("focus click", h.show).keydown(function (b) {
            var e = b.keyCode;
            if (!w && d(V).index(e) >= 0) {
                h.show(b);
                return b.preventDefault()
            }
            return b.shiftKey || b.ctrlKey || b.altKey || e == 9 ? true : b.preventDefault()
        });
        C(a.val()) && j(n, c)
    }

    d.tools = d.tools || {version: "1.2.5"};
    var W = [], Q, V = [75, 76, 38, 39, 74, 72, 40, 37], B = {};
    Q = d.tools.dateinput = {conf: {format: "mm/dd/yy", selectors: false, yearRange: [-5, 5], lang: "en", offset: [0, 0], speed: 0, firstDay: 0, min: undefined, max: undefined, trigger: false, css: {prefix: "cal", input: "date", root: 0, head: 0, title: 0, prev: 0, next: 0, month: 0, year: 0, days: 0, body: 0, weeks: 0, today: 0, current: 0, week: 0, off: 0, sunday: 0, focus: 0, disabled: 0, trigger: 0}}, localize: function (a, c) {
        d.each(c, function (j, q) {
            c[j] = q.split(",")
        });
        B[a] = c
    }};
    Q.localize("en", {months: "January,February,March,April,May,June,July,August,September,October,November,December", shortMonths: "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec", days: "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", shortDays: "Sun,Mon,Tue,Wed,Thu,Fri,Sat"});
    var X = /d{1,4}|m{1,4}|yy(?:yy)?|"[^"]*"|'[^']*'/g, Y = d("<a/>");
    d.expr[":"].date = function (a) {
        var c = a.getAttribute("type");
        return c && c == "date" || !!d(a).data("dateinput")
    };
    d.fn.dateinput = function (a) {
        if (this.data("dateinput"))return this;
        a = d.extend(true, {}, Q.conf, a);
        d.each(a.css, function (j, q) {
            if (!q && j != "prefix")a.css[j] = (a.css.prefix || "") + (q || j)
        });
        var c;
        this.each(function () {
            var j = new Z(d(this), a);
            W.push(j);
            j = j.getInput().data("dateinput", j);
            c = c ? c.add(j) : j
        });
        return c ? c : this
    }
})(jQuery);
(function (e) {
    function F(d, a) {
        a = Math.pow(10, a);
        return Math.round(d * a) / a
    }

    function q(d, a) {
        if (a = parseInt(d.css(a), 10))return a;
        return(d = d[0].currentStyle) && d.width && parseInt(d.width, 10)
    }

    function C(d) {
        return(d = d.data("events")) && d.onSlide
    }

    function G(d, a) {
        function h(c, b, f, j) {
            if (f === undefined)f = b / k * z; else if (j)f -= a.min;
            if (s)f = Math.round(f / s) * s;
            if (b === undefined || s)b = f * k / z;
            if (isNaN(f))return g;
            b = Math.max(0, Math.min(b, k));
            f = b / k * z;
            if (j || !n)f += a.min;
            if (n)if (j)b = k - b; else f = a.max - f;
            f = F(f, t);
            var r = c.type == "click";
            if (D && l !== undefined && !r) {
                c.type = "onSlide";
                A.trigger(c, [f, b]);
                if (c.isDefaultPrevented())return g
            }
            j = r ? a.speed : 0;
            r = r ? function () {
                c.type = "change";
                A.trigger(c, [f])
            } : null;
            if (n) {
                m.animate({top: b}, j, r);
                a.progress && B.animate({height: k - b + m.width() / 2}, j)
            } else {
                m.animate({left: b}, j, r);
                a.progress && B.animate({width: b + m.width() / 2}, j)
            }
            l = f;
            H = b;
            d.val(f);
            return g
        }

        function o() {
            if (n = a.vertical || q(i, "height") > q(i, "width")) {
                k = q(i, "height") - q(m, "height");
                u = i.offset().top + k
            } else {
                k = q(i, "width") - q(m, "width");
                u = i.offset().left
            }
        }

        function v() {
            o();
            g.setValue(a.value !== undefined ? a.value : a.min)
        }

        var g = this, p = a.css, i = e("<div><div/><a href='#'/></div>").data("rangeinput", g), n, l, u, k, H;
        d.before(i);
        var m = i.addClass(p.slider).find("a").addClass(p.handle), B = i.find("div").addClass(p.progress);
        e.each("min,max,step,value".split(","), function (c, b) {
            c = d.attr(b);
            if (parseFloat(c))a[b] = parseFloat(c, 10)
        });
        var z = a.max - a.min, s = a.step == "any" ? 0 : a.step, t = a.precision;
        if (t === undefined)try {
            t = s.toString().split(".")[1].length
        } catch (I) {
            t = 0
        }
        if (d.attr("type") == "range") {
            var w = e("<input/>");
            e.each("class,disabled,id,maxlength,name,readonly,required,size,style,tabindex,title,value".split(","), function (c, b) {
                w.attr(b, d.attr(b))
            });
            w.val(a.value);
            d.replaceWith(w);
            d = w
        }
        d.addClass(p.input);
        var A = e(g).add(d), D = true;
        e.extend(g, {getValue: function () {
            return l
        }, setValue: function (c, b) {
            o();
            return h(b || e.Event("api"), undefined, c, true)
        }, getConf: function () {
            return a
        }, getProgress: function () {
            return B
        }, getHandle: function () {
            return m
        }, getInput: function () {
            return d
        }, step: function (c, b) {
            b = b || e.Event();
            var f = a.step == "any" ? 1 : a.step;
            g.setValue(l + f * (c || 1), b)
        }, stepUp: function (c) {
            return g.step(c || 1)
        }, stepDown: function (c) {
            return g.step(-c || -1)
        }});
        e.each("onSlide,change".split(","), function (c, b) {
            e.isFunction(a[b]) && e(g).bind(b, a[b]);
            g[b] = function (f) {
                f && e(g).bind(b, f);
                return g
            }
        });
        m.drag({drag: false}).bind("dragStart",function () {
            o();
            D = C(e(g)) || C(d)
        }).bind("drag",function (c, b, f) {
            if (d.is(":disabled"))return false;
            h(c, n ? b : f)
        }).bind("dragEnd",function (c) {
            if (!c.isDefaultPrevented()) {
                c.type = "change";
                A.trigger(c, [l])
            }
        }).click(function (c) {
            return c.preventDefault()
        });
        i.click(function (c) {
            if (d.is(":disabled") || c.target == m[0])return c.preventDefault();
            o();
            var b = m.width() / 2;
            h(c, n ? k - u - b + c.pageY : c.pageX - u - b)
        });
        a.keyboard && d.keydown(function (c) {
            if (!d.attr("readonly")) {
                var b = c.keyCode, f = e([75, 76, 38, 33, 39]).index(b) != -1, j = e([74, 72, 40, 34, 37]).index(b) != -1;
                if ((f || j) && !(c.shiftKey || c.altKey || c.ctrlKey)) {
                    if (f)g.step(b == 33 ? 10 : 1, c); else if (j)g.step(b == 34 ? -10 : -1, c);
                    return c.preventDefault()
                }
            }
        });
        d.blur(function (c) {
            var b = e(this).val();
            b !== l && g.setValue(b, c)
        });
        e.extend(d[0], {stepUp: g.stepUp, stepDown: g.stepDown});
        v();
        k || e(window).load(v)
    }

    e.tools = e.tools || {version: "1.2.5"};
    var E;
    E = e.tools.rangeinput = {conf: {min: 0, max: 100, step: "any", steps: 0, value: 0, precision: undefined, vertical: 0, keyboard: true, progress: false, speed: 100, css: {input: "range", slider: "slider", progress: "progress", handle: "handle"}}};
    var x, y;
    e.fn.drag = function (d) {
        document.ondragstart = function () {
            return false
        };
        d = e.extend({x: true, y: true, drag: true}, d);
        x = x || e(document).bind("mousedown mouseup", function (a) {
            var h = e(a.target);
            if (a.type == "mousedown" && h.data("drag")) {
                var o = h.position(), v = a.pageX - o.left, g = a.pageY - o.top, p = true;
                x.bind("mousemove.drag", function (i) {
                    var n = i.pageX - v;
                    i = i.pageY - g;
                    var l = {};
                    if (d.x)l.left = n;
                    if (d.y)l.top = i;
                    if (p) {
                        h.trigger("dragStart");
                        p = false
                    }
                    d.drag && h.css(l);
                    h.trigger("drag", [i, n]);
                    y = h
                });
                a.preventDefault()
            } else try {
                y && y.trigger("dragEnd")
            } finally {
                x.unbind("mousemove.drag");
                y = null
            }
        });
        return this.data("drag", true)
    };
    e.expr[":"].range = function (d) {
        var a = d.getAttribute("type");
        return a && a == "range" || !!e(d).filter("input").data("rangeinput")
    };
    e.fn.rangeinput = function (d) {
        if (this.data("rangeinput"))return this;
        d = e.extend(true, {}, E.conf, d);
        var a;
        this.each(function () {
            var h = new G(e(this), e.extend(true, {}, d));
            h = h.getInput().data("rangeinput", h);
            a = a ? a.add(h) : h
        });
        return a ? a : this
    }
})(jQuery);
(function (e) {
    function t(a, b, c) {
        var k = a.offset().top, f = a.offset().left, l = c.position.split(/,?\s+/), p = l[0];
        l = l[1];
        k -= b.outerHeight() - c.offset[0];
        f += a.outerWidth() + c.offset[1];
        if (/iPad/i.test(navigator.userAgent))k -= e(window).scrollTop();
        c = b.outerHeight() + a.outerHeight();
        if (p == "center")k += c / 2;
        if (p == "bottom")k += c;
        a = a.outerWidth();
        if (l == "center")f -= (a + b.outerWidth()) / 2;
        if (l == "left")f -= a;
        return{top: k, left: f}
    }

    function y(a) {
        function b() {
            return this.getAttribute("type") == a
        }

        b.key = "[type=" + a + "]";
        return b
    }

    function u(a, b, c) {
        function k(g, d, i) {
            if (!(!c.grouped && g.length)) {
                var j;
                if (i === false || e.isArray(i)) {
                    j = h.messages[d.key || d] || h.messages["*"];
                    j = j[c.lang] || h.messages["*"].en;
                    (d = j.match(/\$\d/g)) && e.isArray(i) && e.each(d, function (m) {
                        j = j.replace(this, i[m])
                    })
                } else j = i[c.lang] || i;
                g.push(j)
            }
        }

        var f = this, l = b.add(f);
        a = a.not(":button, :image, :reset, :submit");
        e.extend(f, {getConf: function () {
            return c
        }, getForm: function () {
            return b
        }, getInputs: function () {
            return a
        }, reflow: function () {
            a.each(function () {
                var g = e(this), d = g.data("msg.el");
                if (d) {
                    g = t(g, d, c);
                    d.css({top: g.top, left: g.left})
                }
            });
            return f
        }, invalidate: function (g, d) {
            if (!d) {
                var i = [];
                e.each(g, function (j, m) {
                    j = a.filter("[name='" + j + "']");
                    if (j.length) {
                        j.trigger("OI", [m]);
                        i.push({input: j, messages: [m]})
                    }
                });
                g = i;
                d = e.Event()
            }
            d.type = "onFail";
            l.trigger(d, [g]);
            d.isDefaultPrevented() || q[c.effect][0].call(f, g, d);
            return f
        }, reset: function (g) {
            g = g || a;
            g.removeClass(c.errorClass).each(function () {
                var d = e(this).data("msg.el");
                if (d) {
                    d.remove();
                    e(this).data("msg.el", null)
                }
            }).unbind(c.errorInputEvent || "");
            return f
        }, destroy: function () {
            b.unbind(c.formEvent + ".V").unbind("reset.V");
            a.unbind(c.inputEvent + ".V").unbind("change.V");
            return f.reset()
        }, checkValidity: function (g, d) {
            g = g || a;
            g = g.not(":disabled");
            if (!g.length)return true;
            d = d || e.Event();
            d.type = "onBeforeValidate";
            l.trigger(d, [g]);
            if (d.isDefaultPrevented())return d.result;
            var i = [];
            g.not(":radio:not(:checked)").each(function () {
                var m = [], n = e(this).data("messages", m), v = r && n.is(":date") ? "onHide.v" : c.errorInputEvent + ".v";
                n.unbind(v);
                e.each(w, function () {
                    var o = this, s = o[0];
                    if (n.filter(s).length) {
                        o = o[1].call(f, n, n.val());
                        if (o !== true) {
                            d.type = "onBeforeFail";
                            l.trigger(d, [n, s]);
                            if (d.isDefaultPrevented())return false;
                            var x = n.attr(c.messageAttr);
                            if (x) {
                                m = [x];
                                return false
                            } else k(m, s, o)
                        }
                    }
                });
                if (m.length) {
                    i.push({input: n, messages: m});
                    n.trigger("OI", [m]);
                    c.errorInputEvent && n.bind(v, function (o) {
                        f.checkValidity(n, o)
                    })
                }
                if (c.singleError && i.length)return false
            });
            var j = q[c.effect];
            if (!j)throw'Validator: cannot find effect "' + c.effect + '"';
            if (i.length) {
                f.invalidate(i, d);
                return false
            } else {
                j[1].call(f, g, d);
                d.type = "onSuccess";
                l.trigger(d, [g]);
                g.unbind(c.errorInputEvent + ".v")
            }
            return true
        }});
        e.each("onBeforeValidate,onBeforeFail,onFail,onSuccess".split(","), function (g, d) {
            e.isFunction(c[d]) && e(f).bind(d, c[d]);
            f[d] = function (i) {
                i && e(f).bind(d, i);
                return f
            }
        });
        c.formEvent && b.bind(c.formEvent + ".V", function (g) {
            if (!f.checkValidity(null, g))return g.preventDefault()
        });
        b.bind("reset.V", function () {
            f.reset()
        });
        a[0] && a[0].validity && a.each(function () {
            this.oninvalid = function () {
                return false
            }
        });
        if (b[0])b[0].checkValidity = f.checkValidity;
        c.inputEvent && a.bind(c.inputEvent + ".V", function (g) {
            f.checkValidity(e(this), g)
        });
        a.filter(":checkbox, select").filter("[required]").bind("change.V", function (g) {
            var d = e(this);
            if (this.checked || d.is("select") && e(this).val())q[c.effect][1].call(f, d, g)
        });
        var p = a.filter(":radio").change(function (g) {
            f.checkValidity(p, g)
        });
        e(window).resize(function () {
            f.reflow()
        })
    }

    e.tools = e.tools || {version: "1.2.5"};
    var z = /\[type=([a-z]+)\]/, A = /^-?[0-9]*(\.[0-9]+)?$/, r = e.tools.dateinput, B = /^([a-z0-9_\.\-\+]+)@([\da-z\.\-]+)\.([a-z\.]{2,6})$/i, C = /^(https?:\/\/)?[\da-z\.\-]+\.[a-z\.]{2,6}[#&+_\?\/\w \.\-=]*$/i, h;
    h = e.tools.validator = {conf: {grouped: false, effect: "default", errorClass: "invalid", inputEvent: null, errorInputEvent: "keyup", formEvent: "submit", lang: "en", message: "<div/>", messageAttr: "data-message", messageClass: "error", offset: [0, 0], position: "center right", singleError: false, speed: "normal"}, messages: {"*": {en: "Please correct this value"}}, localize: function (a, b) {
        e.each(b, function (c, k) {
            h.messages[c] = h.messages[c] || {};
            h.messages[c][a] = k
        })
    }, localizeFn: function (a, b) {
        h.messages[a] = h.messages[a] || {};
        e.extend(h.messages[a], b)
    }, fn: function (a, b, c) {
        if (e.isFunction(b))c = b; else {
            if (typeof b == "string")b = {en: b};
            this.messages[a.key || a] = b
        }
        if (b = z.exec(a))a = y(b[1]);
        w.push([a, c])
    }, addEffect: function (a, b, c) {
        q[a] = [b, c]
    }};
    var w = [], q = {"default": [function (a) {
        var b = this.getConf();
        e.each(a, function (c, k) {
            c = k.input;
            c.addClass(b.errorClass);
            var f = c.data("msg.el");
            if (!f) {
                f = e(b.message).addClass(b.messageClass).appendTo(document.body);
                c.data("msg.el", f)
            }
            f.css({visibility: "hidden"}).find("p").remove();
            e.each(k.messages, function (l, p) {
                e("<p/>").html(p).appendTo(f)
            });
            f.outerWidth() == f.parent().width() && f.add(f.find("p")).css({display: "inline"});
            k = t(c, f, b);
            f.css({visibility: "visible", position: "absolute", top: k.top, left: k.left}).fadeIn(b.speed)
        })
    }, function (a) {
        var b = this.getConf();
        a.removeClass(b.errorClass).each(function () {
            var c = e(this).data("msg.el");
            c && c.css({visibility: "hidden"})
        })
    }]};
    e.each("email,url,number".split(","), function (a, b) {
        e.expr[":"][b] = function (c) {
            return c.getAttribute("type") === b
        }
    });
    e.fn.oninvalid = function (a) {
        return this[a ? "bind" : "trigger"]("OI", a)
    };
    h.fn(":email", "Please enter a valid email address", function (a, b) {
        return!b || B.test(b)
    });
    h.fn(":url", "Please enter a valid URL", function (a, b) {
        return!b || C.test(b)
    });
    h.fn(":number", "Please enter a numeric value.", function (a, b) {
        return A.test(b)
    });
    h.fn("[max]", "Please enter a value smaller than $1", function (a, b) {
        if (b === "" || r && a.is(":date"))return true;
        a = a.attr("max");
        return parseFloat(b) <= parseFloat(a) ? true : [a]
    });
    h.fn("[min]", "Please enter a value larger than $1", function (a, b) {
        if (b === "" || r && a.is(":date"))return true;
        a = a.attr("min");
        return parseFloat(b) >= parseFloat(a) ? true : [a]
    });
    h.fn("[required]", "Please complete this mandatory field.", function (a, b) {
        if (a.is(":checkbox"))return a.is(":checked");
        return!!b
    });
    h.fn("[pattern]", function (a) {
        var b = new RegExp("^" + a.attr("pattern") + "$");
        return b.test(a.val())
    });
    e.fn.validator = function (a) {
        var b = this.data("validator");
        if (b) {
            b.destroy();
            this.removeData("validator")
        }
        a = e.extend(true, {}, h.conf, a);
        if (this.is("form"))return this.each(function () {
            var c = e(this);
            b = new u(c.find(":input"), c, a);
            c.data("validator", b)
        }); else {
            b = new u(this, this.eq(0).closest("form"), a);
            return this.data("validator", b)
        }
    }
})(jQuery);
jQuery.fn.pulse = function (prop, speed, times, easing, callback) {
    if (isNaN(times)) {
        callback = easing;
        easing = times;
        times = 1;
    }
    var optall = jQuery.speed(speed, easing, callback), queue = optall.queue !== false, largest = 0;
    for (var p in prop) {
        largest = Math.max(prop[p].length, largest);
    }
    optall.times = optall.times || times;
    return this[queue ? 'queue' : 'each'](function () {
        var counts = {}, opt = jQuery.extend({}, optall), self = jQuery(this);
        pulse();
        function pulse() {
            var propsSingle = {}, doAnimate = false;
            for (var p in prop) {
                counts[p] = counts[p] || {runs: 0, cur: -1};
                if (counts[p].cur < prop[p].length - 1) {
                    ++counts[p].cur;
                } else {
                    counts[p].cur = 0;
                    ++counts[p].runs;
                }
                if (prop[p].length === largest) {
                    doAnimate = opt.times > counts[p].runs;
                }
                propsSingle[p] = prop[p][counts[p].cur];
            }
            opt.complete = pulse;
            opt.queue = false;
            if (doAnimate) {
                self.animate(propsSingle, opt);
            } else {
                optall.complete.call(self[0]);
            }
        }
    });
};

(function ($) {
    $.watch = function (props, callback, timeout) {
        if (!timeout)
            timeout = 100;
        return this.each(function () {
            var el = $(this), func = function () {
                __check.call(this, el)
            }, data = {props: props.split(","), func: callback, vals: []};
            $.each(data.props, function (i) {
                data.vals[i] = el.data(data.props[i]);
            });
            el.data(data);
            setInterval(func, timeout);
        });
        function __check(el) {
            var data = el.data(), changed = false, temp = "";
            for (var i = 0; i < data.props.length; i++) {
                temp = el.data(data.props[i]);
                if (data.vals[i] != temp) {
                    data.vals[i] = temp;
                    changed = true;
                    break;
                }
            }
            if (changed && data.func) {
                data.func.call(el, data);
            }
        }
    }
})(jQuery);

(function ($) {
    $.scrollFollow = function (box, options) {
        box = $(box);
        var position = box.css('position');

        function ani() {
            box.queue([]);
            var viewportHeight = parseInt($(window).height());
            var pageScroll = parseInt($(document).scrollTop());
            var parentTop = parseInt(box.cont.offset().top);
            var parentHeight = parseInt(box.cont.attr('offsetHeight'));
            var boxHeight = parseInt(box.attr('offsetHeight') + (parseInt(box.css('marginTop')) || 0) + (parseInt(box.css('marginBottom')) || 0));
            var aniTop;
            if (isActive) {
                if (options.relativeTo == 'top') {
                    if (box.initialOffsetTop >= (pageScroll + options.offset)) {
                        aniTop = box.initialTop;
                    }
                    else {
                        aniTop = Math.min((Math.max((-parentTop), (pageScroll - box.initialOffsetTop + box.initialTop)) + options.offset), (parentHeight - boxHeight - box.paddingAdjustment));
                    }
                }
                else if (options.relativeTo == 'bottom') {
                    if ((box.initialOffsetTop + boxHeight) >= (pageScroll + options.offset + viewportHeight)) {
                        aniTop = box.initialTop;
                    }
                    else {
                        aniTop = Math.min((pageScroll + viewportHeight - boxHeight - options.offset), (parentHeight - boxHeight));
                    }
                }
                if ((new Date().getTime() - box.lastScroll) >= (options.delay - 20)) {
                    box.animate({top: aniTop}, options.speed, options.easing);
                }
            }
        };
        var isActive = true;
        if ($.cookie != undefined) {
            if ($.cookie('scrollFollowSetting' + box.attr('id')) == 'false') {
                var isActive = false;
                $('#' + options.killSwitch).text(options.offText).toggle(function () {
                    isActive = true;
                    $(this).text(options.onText);
                    $.cookie('scrollFollowSetting' + box.attr('id'), true, {expires: 365, path: '/'});
                    ani();
                }, function () {
                    isActive = false;
                    $(this).text(options.offText);
                    box.animate({top: box.initialTop}, options.speed, options.easing);
                    $.cookie('scrollFollowSetting' + box.attr('id'), false, {expires: 365, path: '/'});
                });
            }
            else {
                $('#' + options.killSwitch).text(options.onText).toggle(function () {
                    isActive = false;
                    $(this).text(options.offText);
                    box.animate({top: box.initialTop}, 0);
                    $.cookie('scrollFollowSetting' + box.attr('id'), false, {expires: 365, path: '/'});
                }, function () {
                    isActive = true;
                    $(this).text(options.onText);
                    $.cookie('scrollFollowSetting' + box.attr('id'), true, {expires: 365, path: '/'});
                    ani();
                });
            }
        }
        if (options.container == '') {
            box.cont = box.parent();
        }
        else {
            box.cont = $('#' + options.container);
        }
        box.initialOffsetTop = parseInt(box.offset().top);
        box.initialTop = parseInt(box.css('top')) || 0;
        if (box.css('position') == 'relative') {
            box.paddingAdjustment = parseInt(box.cont.css('paddingTop')) + parseInt(box.cont.css('paddingBottom'));
        }
        else {
            box.paddingAdjustment = 0;
        }
        $(window).scroll(function () {
            $.fn.scrollFollow.interval = setTimeout(function () {
                ani();
            }, options.delay);
            box.lastScroll = new Date().getTime();
        });
        $(window).resize(function () {
            $.fn.scrollFollow.interval = setTimeout(function () {
                ani();
            }, options.delay);
            box.lastScroll = new Date().getTime();
        });
        box.lastScroll = 0;
        ani();
    };
    $.fn.scrollFollow = function (options) {
        options = options || {};
        options.relativeTo = options.relativeTo || 'top';
        options.speed = options.speed || 500;
        options.offset = options.offset || 0;
        options.easing = options.easing || 'swing';
        options.container = options.container || this.parent().attr('id');
        options.killSwitch = options.killSwitch || 'killSwitch';
        options.onText = options.onText || 'Turn Slide Off';
        options.offText = options.offText || 'Turn Slide On';
        options.delay = options.delay || 0;
        this.each(function () {
            new $.scrollFollow(this, options);
        });
        return this;
    };
})(jQuery);
(function ($, window, document) {
    "use strict";
    var BROWSER_IS_IE7, BROWSER_SCROLLBAR_WIDTH, DOMSCROLL, DOWN, DRAG, KEYDOWN, KEYUP, MOUSEDOWN, MOUSEMOVE, MOUSEUP, MOUSEWHEEL, NanoScroll, PANEDOWN, RESIZE, SCROLL, SCROLLBAR, TOUCHMOVE, UP, WHEEL, defaults, getBrowserScrollbarWidth;
    defaults = {paneClass: 'pane', sliderClass: 'slider', contentClass: 'content', iOSNativeScrolling: false, preventPageScrolling: false, disableResize: false, alwaysVisible: false, flashDelay: 1500, sliderMinHeight: 20, sliderMaxHeight: null, documentContext: null, windowContext: null};
    SCROLLBAR = 'scrollbar';
    SCROLL = 'scroll';
    MOUSEDOWN = 'mousedown';
    MOUSEMOVE = 'mousemove';
    MOUSEWHEEL = 'mousewheel';
    MOUSEUP = 'mouseup';
    RESIZE = 'resize';
    DRAG = 'drag';
    UP = 'up';
    PANEDOWN = 'panedown';
    DOMSCROLL = 'DOMMouseScroll';
    DOWN = 'down';
    WHEEL = 'wheel';
    KEYDOWN = 'keydown';
    KEYUP = 'keyup';
    TOUCHMOVE = 'touchmove';
    BROWSER_IS_IE7 = window.navigator.appName === 'Microsoft Internet Explorer' && /msie 7./i.test(window.navigator.appVersion) && window.ActiveXObject;
    BROWSER_SCROLLBAR_WIDTH = null;
    getBrowserScrollbarWidth = function () {
        var outer, outerStyle, scrollbarWidth;
        outer = document.createElement('div');
        outerStyle = outer.style;
        outerStyle.position = 'absolute';
        outerStyle.width = '100px';
        outerStyle.height = '100px';
        outerStyle.overflow = SCROLL;
        outerStyle.top = '-9999px';
        document.body.appendChild(outer);
        scrollbarWidth = outer.offsetWidth - outer.clientWidth;
        document.body.removeChild(outer);
        return scrollbarWidth;
    };
    NanoScroll = (function () {
        function NanoScroll(el, options) {
            this.el = el;
            this.options = options;
            BROWSER_SCROLLBAR_WIDTH || (BROWSER_SCROLLBAR_WIDTH = getBrowserScrollbarWidth());
            this.$el = $(this.el);
            this.doc = $(this.options.documentContext || document);
            this.win = $(this.options.windowContext || window);
            this.$content = this.$el.children("." + options.contentClass);
            this.$content.attr('tabindex', this.options.tabIndex || 0);
            this.content = this.$content[0];
            if (this.options.iOSNativeScrolling && (this.el.style.WebkitOverflowScrolling != null)) {
                this.nativeScrolling();
            } else {
                this.generate();
            }
            this.createEvents();
            this.addEvents();
            this.reset();
        }

        NanoScroll.prototype.preventScrolling = function (e, direction) {
            if (!this.isActive) {
                return;
            }
            if (e.type === DOMSCROLL) {
                if (direction === DOWN && e.originalEvent.detail > 0 || direction === UP && e.originalEvent.detail < 0) {
                    e.preventDefault();
                }
            } else if (e.type === MOUSEWHEEL) {
                if (!e.originalEvent || !e.originalEvent.wheelDelta) {
                    return;
                }
                if (direction === DOWN && e.originalEvent.wheelDelta < 0 || direction === UP && e.originalEvent.wheelDelta > 0) {
                    e.preventDefault();
                }
            }
        };
        NanoScroll.prototype.nativeScrolling = function () {
            this.$content.css({WebkitOverflowScrolling: 'touch'});
            this.iOSNativeScrolling = true;
            this.isActive = true;
        };
        NanoScroll.prototype.updateScrollValues = function () {
            var content;
            content = this.content;
            this.maxScrollTop = content.scrollHeight - content.clientHeight;
            this.prevScrollTop = this.contentScrollTop || 0;
            this.contentScrollTop = content.scrollTop;
            if (!this.iOSNativeScrolling) {
                this.maxSliderTop = this.paneHeight - this.sliderHeight;
                this.sliderTop = this.maxScrollTop === 0 ? 0 : this.contentScrollTop * this.maxSliderTop / this.maxScrollTop;
            }
        };
        NanoScroll.prototype.createEvents = function () {
            var _this = this;
            this.events = {down: function (e) {
                _this.isBeingDragged = true;
                _this.offsetY = e.pageY - _this.slider.offset().top;
                _this.pane.addClass('active');
                _this.doc.bind(MOUSEMOVE, _this.events[DRAG]).bind(MOUSEUP, _this.events[UP]);
                return false;
            }, drag: function (e) {
                _this.sliderY = e.pageY - _this.$el.offset().top - _this.offsetY;
                _this.scroll();
                _this.updateScrollValues();
                if (_this.contentScrollTop >= _this.maxScrollTop && _this.prevScrollTop !== _this.maxScrollTop) {
                    _this.$el.trigger('scrollend');
                } else if (_this.contentScrollTop === 0 && _this.prevScrollTop !== 0) {
                    _this.$el.trigger('scrolltop');
                }
                return false;
            }, up: function (e) {
                _this.isBeingDragged = false;
                _this.pane.removeClass('active');
                _this.doc.unbind(MOUSEMOVE, _this.events[DRAG]).unbind(MOUSEUP, _this.events[UP]);
                return false;
            }, resize: function (e) {
                _this.reset();
            }, panedown: function (e) {
                _this.sliderY = (e.offsetY || e.originalEvent.layerY) - (_this.sliderHeight * 0.5);
                _this.scroll();
                _this.events.down(e);
                return false;
            }, scroll: function (e) {
                if (_this.isBeingDragged) {
                    return;
                }
                _this.updateScrollValues();
                if (!_this.iOSNativeScrolling) {
                    _this.sliderY = _this.sliderTop;
                    _this.slider.css({top: _this.sliderTop});
                }
                if (e == null) {
                    return;
                }
                if (_this.contentScrollTop >= _this.maxScrollTop) {
                    if (_this.options.preventPageScrolling) {
                        _this.preventScrolling(e, DOWN);
                    }
                    if (_this.prevScrollTop !== _this.maxScrollTop) {
                        _this.$el.trigger('scrollend');
                    }
                } else if (_this.contentScrollTop === 0) {
                    if (_this.options.preventPageScrolling) {
                        _this.preventScrolling(e, UP);
                    }
                    if (_this.prevScrollTop !== 0) {
                        _this.$el.trigger('scrolltop');
                    }
                }
            }, wheel: function (e) {
                var delta;
                if (e == null) {
                    return;
                }
                delta = e.delta || e.wheelDelta || (e.originalEvent && e.originalEvent.wheelDelta) || -e.detail || (e.originalEvent && -e.originalEvent.detail);
                if (delta) {
                    _this.sliderY += -delta / 3;
                }
                _this.scroll();
                return false;
            }};
        };
        NanoScroll.prototype.addEvents = function () {
            var events;
            this.removeEvents();
            events = this.events;
            if (!this.options.disableResize) {
                this.win.bind(RESIZE, events[RESIZE]);
            }
            if (!this.iOSNativeScrolling) {
                this.slider.bind(MOUSEDOWN, events[DOWN]);
                this.pane.bind(MOUSEDOWN, events[PANEDOWN]).bind("" + MOUSEWHEEL + " " + DOMSCROLL, events[WHEEL]);
            }
            this.$content.bind("" + SCROLL + " " + MOUSEWHEEL + " " + DOMSCROLL + " " + TOUCHMOVE, events[SCROLL]);
        };
        NanoScroll.prototype.removeEvents = function () {
            var events;
            events = this.events;
            this.win.unbind(RESIZE, events[RESIZE]);
            if (!this.iOSNativeScrolling) {
                this.slider.unbind();
                this.pane.unbind();
            }
            this.$content.unbind("" + SCROLL + " " + MOUSEWHEEL + " " + DOMSCROLL + " " + TOUCHMOVE, events[SCROLL]);
        };
        NanoScroll.prototype.generate = function () {
            var contentClass, cssRule, options, paneClass, sliderClass;
            options = this.options;
            paneClass = options.paneClass, sliderClass = options.sliderClass, contentClass = options.contentClass;
            if (!this.$el.find("" + paneClass).length && !this.$el.find("" + sliderClass).length) {
                this.$el.append("<div class=\"" + paneClass + "\"><div class=\"" + sliderClass + "\" /></div>");
            }
            this.pane = this.$el.children("." + paneClass);
            this.slider = this.pane.find("." + sliderClass);
            if (BROWSER_SCROLLBAR_WIDTH) {
                cssRule = {right: -BROWSER_SCROLLBAR_WIDTH};
                this.$el.addClass('has-scrollbar');
            }
            if (cssRule != null) {
                this.$content.css(cssRule);
            }
            return this;
        };
        NanoScroll.prototype.restore = function () {
            this.stopped = false;
            this.pane.show();
            this.addEvents();
        };
        NanoScroll.prototype.reset = function () {
            var content, contentHeight, contentStyle, contentStyleOverflowY, paneBottom, paneHeight, paneOuterHeight, paneTop, parentMaxHeight, sliderHeight;
            if (this.iOSNativeScrolling) {
                this.contentHeight = this.content.scrollHeight;
                return;
            }
            if (!this.$el.find("." + this.options.paneClass).length) {
                this.generate().stop();
            }
            if (this.stopped) {
                this.restore();
            }
            content = this.content;
            contentStyle = content.style;
            contentStyleOverflowY = contentStyle.overflowY;
            if (BROWSER_IS_IE7) {
                this.$content.css({height: this.$content.height()});
            }
            contentHeight = content.scrollHeight + BROWSER_SCROLLBAR_WIDTH;
            parentMaxHeight = parseInt(this.$el.css("max-height"), 10);
            if (parentMaxHeight > 0) {
                this.$el.height("");
                this.$el.height(content.scrollHeight > parentMaxHeight ? parentMaxHeight : content.scrollHeight);
            }
            paneHeight = this.pane.outerHeight(false);
            paneTop = parseInt(this.pane.css('top'), 10);
            paneBottom = parseInt(this.pane.css('bottom'), 10);
            paneOuterHeight = paneHeight + paneTop + paneBottom;
            sliderHeight = Math.round(paneOuterHeight / contentHeight * paneOuterHeight);
            if (sliderHeight < this.options.sliderMinHeight) {
                sliderHeight = this.options.sliderMinHeight;
            } else if ((this.options.sliderMaxHeight != null) && sliderHeight > this.options.sliderMaxHeight) {
                sliderHeight = this.options.sliderMaxHeight;
            }
            if (contentStyleOverflowY === SCROLL && contentStyle.overflowX !== SCROLL) {
                sliderHeight += BROWSER_SCROLLBAR_WIDTH;
            }
            this.maxSliderTop = paneOuterHeight - sliderHeight;
            this.contentHeight = contentHeight;
            this.paneHeight = paneHeight;
            this.paneOuterHeight = paneOuterHeight;
            this.sliderHeight = sliderHeight;
            this.slider.height(sliderHeight);
            this.events.scroll();
            this.pane.show();
            this.isActive = true;
            if ((content.scrollHeight === content.clientHeight) || (this.pane.outerHeight(true) >= content.scrollHeight && contentStyleOverflowY !== SCROLL)) {
                this.pane.hide();
                this.isActive = false;
            } else if (this.el.clientHeight === content.scrollHeight && contentStyleOverflowY === SCROLL) {
                this.slider.hide();
            } else {
                this.slider.show();
            }
            this.pane.css({opacity: (this.options.alwaysVisible ? 1 : ''), visibility: (this.options.alwaysVisible ? 'visible' : '')});
            return this;
        };
        NanoScroll.prototype.scroll = function () {
            if (!this.isActive) {
                return;
            }
            this.sliderY = Math.max(0, this.sliderY);
            this.sliderY = Math.min(this.maxSliderTop, this.sliderY);
            this.$content.scrollTop((this.paneHeight - this.contentHeight + BROWSER_SCROLLBAR_WIDTH) * this.sliderY / this.maxSliderTop * -1);
            if (!this.iOSNativeScrolling) {
                this.slider.css({top: this.sliderY});
            }
            return this;
        };
        NanoScroll.prototype.scrollBottom = function (offsetY) {
            if (!this.isActive) {
                return;
            }
            this.reset();
            this.$content.scrollTop(this.contentHeight - this.$content.height() - offsetY).trigger(MOUSEWHEEL);
            return this;
        };
        NanoScroll.prototype.scrollTop = function (offsetY) {
            if (!this.isActive) {
                return;
            }
            this.reset();
            this.$content.scrollTop(+offsetY).trigger(MOUSEWHEEL);
            return this;
        };
        NanoScroll.prototype.scrollTo = function (node) {
            if (!this.isActive) {
                return;
            }
            this.reset();
            this.scrollTop($(node).get(0).offsetTop);
            return this;
        };
        NanoScroll.prototype.stop = function () {
            this.stopped = true;
            this.removeEvents();
            this.pane.hide();
            return this;
        };
        NanoScroll.prototype.destroy = function () {
            if (!this.stopped) {
                this.stop();
            }
            if (this.pane.length) {
                this.pane.remove();
            }
            if (BROWSER_IS_IE7) {
                this.$content.height('');
            }
            this.$content.removeAttr('tabindex');
            if (this.$el.hasClass('has-scrollbar')) {
                this.$el.removeClass('has-scrollbar');
                this.$content.css({right: ''});
            }
            return this;
        };
        NanoScroll.prototype.flash = function () {
            var _this = this;
            if (!this.isActive) {
                return;
            }
            this.reset();
            this.pane.addClass('flashed');
            setTimeout(function () {
                _this.pane.removeClass('flashed');
            }, this.options.flashDelay);
            return this;
        };
        return NanoScroll;
    })();
    $.fn.nanoScroller = function (settings) {
        return this.each(function () {
            var options, scrollbar;
            if (!(scrollbar = this.nanoscroller)) {
                options = $.extend({}, defaults, settings);
                this.nanoscroller = scrollbar = new NanoScroll(this, options);
            }
            if (settings && typeof settings === "object") {
                $.extend(scrollbar.options, settings);
                if (settings.scrollBottom) {
                    return scrollbar.scrollBottom(settings.scrollBottom);
                }
                if (settings.scrollTop) {
                    return scrollbar.scrollTop(settings.scrollTop);
                }
                if (settings.scrollTo) {
                    return scrollbar.scrollTo(settings.scrollTo);
                }
                if (settings.scroll === 'bottom') {
                    return scrollbar.scrollBottom(0);
                }
                if (settings.scroll === 'top') {
                    return scrollbar.scrollTop(0);
                }
                if (settings.scroll && settings.scroll instanceof $) {
                    return scrollbar.scrollTo(settings.scroll);
                }
                if (settings.stop) {
                    return scrollbar.stop();
                }
                if (settings.destroy) {
                    return scrollbar.destroy();
                }
                if (settings.flash) {
                    return scrollbar.flash();
                }
            }
            return scrollbar.reset();
        });
    };
})(jQuery, window, document);
(function (jQuery, undefined) {
    var oldManip = jQuery.fn.domManip, tmplItmAtt = "_tmplitem", htmlExpr = /^[^<]*(<[\w\W]+>)[^>]*$|\{\{\! /, newTmplItems = {}, wrappedItems = {}, appendToTmplItems, topTmplItem = {key: 0, data: {}}, itemKey = 0, cloneIndex = 0, stack = [];

    function newTmplItem(options, parentItem, fn, data) {
        var newItem = {data: data || (data === 0 || data === false) ? data : (parentItem ? parentItem.data : {}), _wrap: parentItem ? parentItem._wrap : null, tmpl: null, parent: parentItem || null, nodes: [], calls: tiCalls, nest: tiNest, wrap: tiWrap, html: tiHtml, update: tiUpdate};
        if (options) {
            jQuery.extend(newItem, options, {nodes: [], parent: parentItem});
        }
        if (fn) {
            newItem.tmpl = fn;
            newItem._ctnt = newItem._ctnt || newItem.tmpl(jQuery, newItem);
            newItem.key = ++itemKey;
            (stack.length ? wrappedItems : newTmplItems)[itemKey] = newItem;
        }
        return newItem;
    }

    jQuery.each({appendTo: "append", prependTo: "prepend", insertBefore: "before", insertAfter: "after", replaceAll: "replaceWith"}, function (name, original) {
        jQuery.fn[name] = function (selector) {
            var ret = [], insert = jQuery(selector), elems, i, l, tmplItems, parent = this.length === 1 && this[0].parentNode;
            appendToTmplItems = newTmplItems || {};
            if (parent && parent.nodeType === 11 && parent.childNodes.length === 1 && insert.length === 1) {
                insert[original](this[0]);
                ret = this;
            } else {
                for (i = 0, l = insert.length; i < l; i++) {
                    cloneIndex = i;
                    elems = (i > 0 ? this.clone(true) : this).get();
                    jQuery(insert[i])[original](elems);
                    ret = ret.concat(elems);
                }
                cloneIndex = 0;
                ret = this.pushStack(ret, name, insert.selector);
            }
            tmplItems = appendToTmplItems;
            appendToTmplItems = null;
            jQuery.tmpl.complete(tmplItems);
            return ret;
        };
    });
    jQuery.fn.extend({tmpl: function (data, options, parentItem) {
        return jQuery.tmpl(this[0], data, options, parentItem);
    }, tmplItem: function () {
        return jQuery.tmplItem(this[0]);
    }, template: function (name) {
        return jQuery.template(name, this[0]);
    }, domManip: function (args, table, callback, options) {
        if (args[0] && jQuery.isArray(args[0])) {
            var dmArgs = jQuery.makeArray(arguments), elems = args[0], elemsLength = elems.length, i = 0, tmplItem;
            while (i < elemsLength && !(tmplItem = jQuery.data(elems[i++], "tmplItem"))) {
            }
            if (tmplItem && cloneIndex) {
                dmArgs[2] = function (fragClone) {
                    jQuery.tmpl.afterManip(this, fragClone, callback);
                };
            }
            oldManip.apply(this, dmArgs);
        } else {
            oldManip.apply(this, arguments);
        }
        cloneIndex = 0;
        if (!appendToTmplItems) {
            jQuery.tmpl.complete(newTmplItems);
        }
        return this;
    }});
    jQuery.extend({tmpl: function (tmpl, data, options, parentItem) {
        var ret, topLevel = !parentItem;
        if (topLevel) {
            parentItem = topTmplItem;
            tmpl = jQuery.template[tmpl] || jQuery.template(null, tmpl);
            wrappedItems = {};
        } else if (!tmpl) {
            tmpl = parentItem.tmpl;
            newTmplItems[parentItem.key] = parentItem;
            parentItem.nodes = [];
            if (parentItem.wrapped) {
                updateWrapped(parentItem, parentItem.wrapped);
            }
            return jQuery(build(parentItem, null, parentItem.tmpl(jQuery, parentItem)));
        }
        if (!tmpl) {
            return[];
        }
        if (typeof data === "function") {
            data = data.call(parentItem || {});
        }
        if (options && options.wrapped) {
            updateWrapped(options, options.wrapped);
        }
        ret = jQuery.isArray(data) ? jQuery.map(data, function (dataItem) {
            return dataItem ? newTmplItem(options, parentItem, tmpl, dataItem) : null;
        }) : [newTmplItem(options, parentItem, tmpl, data)];
        return topLevel ? jQuery(build(parentItem, null, ret)) : ret;
    }, tmplItem: function (elem) {
        var tmplItem;
        if (elem instanceof jQuery) {
            elem = elem[0];
        }
        while (elem && elem.nodeType === 1 && !(tmplItem = jQuery.data(elem, "tmplItem")) && (elem = elem.parentNode)) {
        }
        return tmplItem || topTmplItem;
    }, template: function (name, tmpl) {
        if (tmpl) {
            if (typeof tmpl === "string") {
                tmpl = buildTmplFn(tmpl);
            } else if (tmpl instanceof jQuery) {
                tmpl = tmpl[0] || {};
            }
            if (tmpl.nodeType) {
                tmpl = jQuery.data(tmpl, "tmpl") || jQuery.data(tmpl, "tmpl", buildTmplFn(tmpl.innerHTML));
            }
            return typeof name === "string" ? (jQuery.template[name] = tmpl) : tmpl;
        }
        return name ? (typeof name !== "string" ? jQuery.template(null, name) : (jQuery.template[name] || jQuery.template(null, htmlExpr.test(name) ? name : jQuery(name)))) : null;
    }, encode: function (text) {
        return("" + text).split("<").join("&lt;").split(">").join("&gt;").split('"').join("&#34;").split("'").join("&#39;");
    }});
    jQuery.extend(jQuery.tmpl, {tag: {"tmpl": {_default: {$2: "null"}, open: "if($notnull_1){__=__.concat($item.nest($1,$2));}"}, "wrap": {_default: {$2: "null"}, open: "$item.calls(__,$1,$2);__=[];", close: "call=$item.calls();__=call._.concat($item.wrap(call,__));"}, "each": {_default: {$2: "$index, $value"}, open: "if($notnull_1){$.each($1a,function($2){with(this){", close: "}});}"}, "if": {open: "if(($notnull_1) && $1a){", close: "}"}, "else": {_default: {$1: "true"}, open: "}else if(($notnull_1) && $1a){"}, "html": {open: "if($notnull_1){__.push($1a);}"}, "=": {_default: {$1: "$data"}, open: "if($notnull_1){__.push($.encode($1a));}"}, "!": {open: ""}}, complete: function (items) {
        newTmplItems = {};
    }, afterManip: function afterManip(elem, fragClone, callback) {
        var content = fragClone.nodeType === 11 ? jQuery.makeArray(fragClone.childNodes) : fragClone.nodeType === 1 ? [fragClone] : [];
        callback.call(elem, fragClone);
        storeTmplItems(content);
        cloneIndex++;
    }});
    function build(tmplItem, nested, content) {
        var frag, ret = content ? jQuery.map(content, function (item) {
            return(typeof item === "string") ? (tmplItem.key ? item.replace(/(<\w+)(?=[\s>])(?![^>]*_tmplitem)([^>]*)/g, "$1 " + tmplItmAtt + "=\"" + tmplItem.key + "\" $2") : item) : build(item, tmplItem, item._ctnt);
        }) : tmplItem;
        if (nested) {
            return ret;
        }
        ret = ret.join("");
        ret.replace(/^\s*([^<\s][^<]*)?(<[\w\W]+>)([^>]*[^>\s])?\s*$/, function (all, before, middle, after) {
            frag = jQuery(middle).get();
            storeTmplItems(frag);
            if (before) {
                frag = unencode(before).concat(frag);
            }
            if (after) {
                frag = frag.concat(unencode(after));
            }
        });
        return frag ? frag : unencode(ret);
    }

    function unencode(text) {
        var el = document.createElement("div");
        el.innerHTML = text;
        return jQuery.makeArray(el.childNodes);
    }

    function buildTmplFn(markup) {
        return new Function("jQuery", "$item", "var $=jQuery,call,__=[],$data=$item.data;" + "with($data){__.push('" +
            jQuery.trim(markup).replace(/([\\'])/g, "\\$1").replace(/[\r\t\n]/g, " ").replace(/\$\{([^\}]*)\}/g, "{{= $1}}").replace(/\{\{(\/?)(\w+|.)(?:\(((?:[^\}]|\}(?!\}))*?)?\))?(?:\s+(.*?)?)?(\(((?:[^\}]|\}(?!\}))*?)\))?\s*\}\}/g, function (all, slash, type, fnargs, target, parens, args) {
                var tag = jQuery.tmpl.tag[type], def, expr, exprAutoFnDetect;
                if (!tag) {
                    throw"Unknown template tag: " + type;
                }
                def = tag._default || [];
                if (parens && !/\w$/.test(target)) {
                    target += parens;
                    parens = "";
                }
                if (target) {
                    target = unescape(target);
                    args = args ? ("," + unescape(args) + ")") : (parens ? ")" : "");
                    expr = parens ? (target.indexOf(".") > -1 ? target + unescape(parens) : ("(" + target + ").call($item" + args)) : target;
                    exprAutoFnDetect = parens ? expr : "(typeof(" + target + ")==='function'?(" + target + ").call($item):(" + target + "))";
                } else {
                    exprAutoFnDetect = expr = def.$1 || "null";
                }
                fnargs = unescape(fnargs);
                return"');" +
                    tag[slash ? "close" : "open"].split("$notnull_1").join(target ? "typeof(" + target + ")!=='undefined' && (" + target + ")!=null" : "true").split("$1a").join(exprAutoFnDetect).split("$1").join(expr).split("$2").join(fnargs || def.$2 || "") + "__.push('";
            }) + "');}return __;");
    }

    function updateWrapped(options, wrapped) {
        options._wrap = build(options, true, jQuery.isArray(wrapped) ? wrapped : [htmlExpr.test(wrapped) ? wrapped : jQuery(wrapped).html()]).join("");
    }

    function unescape(args) {
        return args ? args.replace(/\\'/g, "'").replace(/\\\\/g, "\\") : null;
    }

    function outerHtml(elem) {
        var div = document.createElement("div");
        div.appendChild(elem.cloneNode(true));
        return div.innerHTML;
    }

    function storeTmplItems(content) {
        var keySuffix = "_" + cloneIndex, elem, elems, newClonedItems = {}, i, l, m;
        for (i = 0, l = content.length; i < l; i++) {
            if ((elem = content[i]).nodeType !== 1) {
                continue;
            }
            elems = elem.getElementsByTagName("*");
            for (m = elems.length - 1; m >= 0; m--) {
                processItemKey(elems[m]);
            }
            processItemKey(elem);
        }
        function processItemKey(el) {
            var pntKey, pntNode = el, pntItem, tmplItem, key;
            if ((key = el.getAttribute(tmplItmAtt))) {
                while (pntNode.parentNode && (pntNode = pntNode.parentNode).nodeType === 1 && !(pntKey = pntNode.getAttribute(tmplItmAtt))) {
                }
                if (pntKey !== key) {
                    pntNode = pntNode.parentNode ? (pntNode.nodeType === 11 ? 0 : (pntNode.getAttribute(tmplItmAtt) || 0)) : 0;
                    if (!(tmplItem = newTmplItems[key])) {
                        tmplItem = wrappedItems[key];
                        tmplItem = newTmplItem(tmplItem, newTmplItems[pntNode] || wrappedItems[pntNode]);
                        tmplItem.key = ++itemKey;
                        newTmplItems[itemKey] = tmplItem;
                    }
                    if (cloneIndex) {
                        cloneTmplItem(key);
                    }
                }
                el.removeAttribute(tmplItmAtt);
            } else if (cloneIndex && (tmplItem = jQuery.data(el, "tmplItem"))) {
                cloneTmplItem(tmplItem.key);
                newTmplItems[tmplItem.key] = tmplItem;
                pntNode = jQuery.data(el.parentNode, "tmplItem");
                pntNode = pntNode ? pntNode.key : 0;
            }
            if (tmplItem) {
                pntItem = tmplItem;
                while (pntItem && pntItem.key != pntNode) {
                    pntItem.nodes.push(el);
                    pntItem = pntItem.parent;
                }
                delete tmplItem._ctnt;
                delete tmplItem._wrap;
                jQuery.data(el, "tmplItem", tmplItem);
            }
            function cloneTmplItem(key) {
                key = key + keySuffix;
                tmplItem = newClonedItems[key] = (newClonedItems[key] || newTmplItem(tmplItem, newTmplItems[tmplItem.parent.key + keySuffix] || tmplItem.parent));
            }
        }
    }

    function tiCalls(content, tmpl, data, options) {
        if (!content) {
            return stack.pop();
        }
        stack.push({_: content, tmpl: tmpl, item: this, data: data, options: options});
    }

    function tiNest(tmpl, data, options) {
        return jQuery.tmpl(jQuery.template(tmpl), data, options, this);
    }

    function tiWrap(call, wrapped) {
        var options = call.options || {};
        options.wrapped = wrapped;
        return jQuery.tmpl(jQuery.template(call.tmpl), call.data, options, call.item);
    }

    function tiHtml(filter, textOnly) {
        var wrapped = this._wrap;
        return jQuery.map(jQuery(jQuery.isArray(wrapped) ? wrapped.join("") : wrapped).filter(filter || "*"), function (e) {
            return textOnly ? e.innerText || e.textContent : e.outerHTML || outerHtml(e);
        });
    }

    function tiUpdate() {
        var coll = this.nodes;
        jQuery.tmpl(null, null, null, this).insertBefore(coll[0]);
        jQuery(coll).remove();
    }
})(jQuery);
window.JsViews || window.jQuery && jQuery.views || (function (window, undefined) {
    var $, _$, JsViews, viewsNs, tmplEncode, render, rTag, registerTags, registerHelpers, extend, FALSE = false, TRUE = true, jQuery = window.jQuery, document = window.document, htmlExpr = /^[^<]*(<[\w\W]+>)[^>]*$|\{\{\! /, rPath = /^(true|false|null|[\d\.]+)|(\w+|\$(view|data|ctx|(\w+)))([\w\.]*)|((['"])(?:\\\1|.)*\7)$/g, rParams = /(\$?[\w\.\[\]]+)(?:(\()|\s*(===|!==|==|!=|<|>|<=|>=)\s*|\s*(\=)\s*)?|(\,\s*)|\\?(\')|\\?(\")|(\))|(\s+)/g, rNewLine = /\r?\n/g, rUnescapeQuotes = /\\(['"])/g, rEscapeQuotes = /\\?(['"])/g, rBuildHash = /\x08([^\x08]+)\x08/g, autoName = 0, escapeMapForHtml = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}, htmlSpecialChar = /[\x00"&'<>]/g, slice = Array.prototype.slice;
    if (jQuery) {
        $ = jQuery;
        $.fn.extend({render: function (data, context, parentView, path) {
            return render(data, this[0], context, parentView, path);
        }, template: function (name, context) {
            return $.template(name, this[0], context);
        }});
    } else {
        _$ = window.$;
        window.JsViews = JsViews = window.$ = $ = {extend: function (target, source) {
            var name;
            for (name in source) {
                target[name] = source[name];
            }
            return target;
        }, isArray: Array.isArray || function (obj) {
            return Object.prototype.toString.call(obj) === "[object Array]";
        }, noConflict: function () {
            if (window.$ === JsViews) {
                window.$ = _$;
            }
            return JsViews;
        }};
    }
    extend = $.extend;
    function View(context, path, parentView, data, template) {
        parentView = parentView || {viewsCount: 0, ctx: viewsNs.helpers};
        var parentContext = parentView && parentView.ctx;
        return{jsViews: "v1.0pre", path: path || "", itemNumber: ++parentView.viewsCount || 1, viewsCount: 0, tmpl: template, data: data || parentView.data || {}, ctx: context && context === parentContext ? parentContext : (parentContext ? extend(extend({}, parentContext), context) : context || {}), parent: parentView};
    }

    extend($, {views: viewsNs = {templates: {}, tags: {"if": function () {
        var ifTag = this, view = ifTag._view;
        view.onElse = function (presenter, args) {
            var i = 0, l = args.length;
            while (l && !args[i++]) {
                if (i === l) {
                    return"";
                }
            }
            view.onElse = undefined;
            return render(view.data, presenter.tmpl, view.ctx, view);
        };
        return view.onElse(this, arguments);
    }, "else": function () {
        var view = this._view;
        return view.onElse ? view.onElse(this, arguments) : "";
    }, each: function () {
        var i, self = this, result = "", args = arguments, l = args.length, content = self.tmpl, view = self._view;
        for (i = 0; i < l; i++) {
            result += args[i] ? render(args[i], content, self.ctx || view.ctx, view, self._path, self._ctor) : "";
        }
        return l ? result : result + render(view.data, content, view.ctx, view, self._path, self.tag);
    }, "=": function (value) {
        return value;
    }, "*": function (value) {
        return value;
    }}, helpers: {not: function (value) {
        return!value;
    }}, allowCode: FALSE, debugMode: TRUE, err: function (e) {
        return viewsNs.debugMode ? ("<br/><b>Error:</b> <em> " + (e.message || e) + ". </em>") : '""';
    }, setDelimiters: function (openTag, closeTag) {
        var firstCloseChar = closeTag.charAt(0), secondCloseChar = closeTag.charAt(1);
        openTag = "\\" + openTag.charAt(0) + "\\" + openTag.charAt(1);
        closeTag = "\\" + firstCloseChar + "\\" + secondCloseChar;
        rTag = openTag
            + "(?:(?:(\\#)?(\\w+(?=[!\\s\\" + firstCloseChar + "]))" + "|(?:(\\=)|(\\*)))"
            + "\\s*((?:[^\\" + firstCloseChar + "]|\\" + firstCloseChar + "(?!\\" + secondCloseChar + "))*?)"
            + "(!(\\w*))?"
            + "|(?:\\/([\\w\\$\\.\\[\\]]+)))"
            + closeTag;
        rTag = new RegExp(rTag, "g");
    }, registerTags: registerTags = function (name, tagFn) {
        var key;
        if (typeof name === "object") {
            for (key in name) {
                registerTags(key, name[key]);
            }
        } else {
            viewsNs.tags[name] = tagFn;
        }
        return this;
    }, registerHelpers: registerHelpers = function (name, helper) {
        if (typeof name === "object") {
            var key;
            for (key in name) {
                registerHelpers(key, name[key]);
            }
        } else {
            viewsNs.helpers[name] = helper;
        }
        return this;
    }, encode: function (encoding, text) {
        return text ? (tmplEncode[encoding || "html"] || tmplEncode.html)(text) : "";
    }, encoders: tmplEncode = {"none": function (text) {
        return text;
    }, "html": function (text) {
        return String(text).replace(htmlSpecialChar, replacerForHtml);
    }}, renderTag: function (tag, view, encode, content, tagProperties) {
        var ret, ctx, name, args = arguments, presenters = viewsNs.presenters;
        hash = tagProperties._hash, tagFn = viewsNs.tags[tag];
        if (!tagFn) {
            return"";
        }
        content = content && view.tmpl.nested[content - 1];
        tagProperties.tmpl = tagProperties.tmpl || content || undefined;
        if (presenters && presenters[tag]) {
            ctx = extend(extend({}, tagProperties.ctx), tagProperties);
            delete ctx.ctx;
            delete ctx._path;
            delete ctx.tmpl;
            tagProperties.ctx = ctx;
            tagProperties._ctor = tag + (hash ? "=" + hash.slice(0, -1) : "");
            tagProperties = extend(extend({}, tagFn), tagProperties);
            tagFn = viewsNs.tags.each;
        }
        tagProperties._encode = encode;
        tagProperties._view = view;
        ret = tagFn.apply(tagProperties, args.length > 5 ? slice.call(args, 5) : [view.data]);
        return ret || (ret === undefined ? "" : ret.toString());
    }}, render: render = function (data, tmpl, context, parentView, path, tagName) {
        var i, l, dataItem, arrayView, content, result = "";
        if (arguments.length === 2 && data.jsViews) {
            parentView = data;
            context = parentView.ctx;
            data = parentView.data;
        }
        tmpl = $.template(tmpl);
        if (!tmpl) {
            return"";
        }
        if ($.isArray(data)) {
            arrayView = new View(context, path, parentView, data);
            l = data.length;
            for (i = 0, l = data.length; i < l; i++) {
                dataItem = data[i];
                content = dataItem ? tmpl(dataItem, new View(context, path, arrayView, dataItem, tmpl, this)) : "";
                result += viewsNs.activeViews ? "<!--item-->" + content + "<!--/item-->" : content;
            }
        } else {
            result += tmpl(data, new View(context, path, parentView, data, tmpl));
        }
        return viewsNs.activeViews ? "<!--tmpl(" + (path || "") + ") " + (tagName ? "tag=" + tagName : tmpl._name) + "-->" + result + "<!--/tmpl-->" : result;
    }, template: function (name, tmpl) {
        if (tmpl) {
            if ("" + tmpl === tmpl) {
                tmpl = compile(tmpl);
            } else if (jQuery && tmpl instanceof $) {
                tmpl = tmpl[0];
            }
            if (tmpl) {
                if (jQuery && tmpl.nodeType) {
                    tmpl = $.data(tmpl, "tmpl") || $.data(tmpl, "tmpl", compile(tmpl.innerHTML));
                }
                viewsNs.templates[tmpl._name = tmpl._name || name || "_" + autoName++] = tmpl;
            }
            return tmpl;
        }
        return name ? "" + name !== name ? (name._name ? name : $.template(null, name)) : viewsNs.templates[name] || $.template(null, htmlExpr.test(name) ? name : try$(name)) : null;
    }});
    viewsNs.setDelimiters("{{", "}}");
    function parsePath(all, comp, object, viewDataCtx, viewProperty, path, string, quot) {
        return object ? ((viewDataCtx ? viewProperty ? ("$view." + viewProperty) : object : ("$data." + object)) + (path || "")) : string || (comp || "");
    }

    function compile(markup) {
        var newNode, loc = 0, stack = [], topNode = [], content = topNode, current = [, , topNode];

        function pushPreceedingContent(shift) {
            shift -= loc;
            if (shift) {
                content.push(markup.substr(loc, shift).replace(rNewLine, "\\n"));
            }
        }

        function parseTag(all, isBlock, tagName, equals, code, params, useEncode, encode, closeBlock, index) {
            var named, hash = "", parenDepth = 0, quoted = FALSE, aposed = FALSE;

            function parseParams(all, path, paren, comp, eq, comma, apos, quot, rightParen, space, index) {
                return aposed ? (aposed = !apos, (aposed ? all : '"')) : quoted ? (quoted = !quot, (quoted ? all : '"')) : comp ? (path.replace(rPath, parsePath) + comp) : eq ? parenDepth ? "" : (named = TRUE, '\b' + path + ':') : paren ? (parenDepth++, path.replace(rPath, parsePath) + '(') : rightParen ? (parenDepth--, ")") : path ? path.replace(rPath, parsePath) : comma ? "," : space ? (parenDepth ? "" : named ? (named = FALSE, "\b") : ",") : (aposed = apos, quoted = quot, '"');
            }

            tagName = tagName || equals;
            pushPreceedingContent(index);
            if (code) {
                if (viewsNs.allowCode) {
                    content.push(["*", params.replace(rUnescapeQuotes, "$1")]);
                }
            } else if (tagName) {
                if (tagName === "else") {
                    current = stack.pop();
                    content = current[2];
                    isBlock = TRUE;
                }
                params = (params ? (params + " ").replace(rParams, parseParams).replace(rBuildHash, function (all, keyValue, index) {
                    hash += keyValue + ",";
                    return"";
                }) : "");
                params = params.slice(0, -1);
                newNode = [tagName, useEncode ? encode || "none" : "", isBlock && [], "{" + hash + "_hash:'" + hash + "',_path:'" + params + "'}", params];
                if (isBlock) {
                    stack.push(current);
                    current = newNode;
                }
                content.push(newNode);
            } else if (closeBlock) {
                current = stack.pop();
            }
            loc = index + all.length;
            if (!current) {
                throw"Expected block tag";
            }
            content = current[2];
        }

        markup = markup.replace(rEscapeQuotes, "\\$1");
        markup.replace(rTag, parseTag);
        pushPreceedingContent(markup.length);
        return buildTmplFunction(topNode);
    }

    function buildTmplFunction(nodes) {
        var ret, node, i, nested = [], l = nodes.length, code = "try{var views="
            + (jQuery ? "jQuery" : "JsViews")
            + '.views,tag=views.renderTag,enc=views.encode,html=views.encoders.html,$ctx=$view && $view.ctx,result=""+\n\n';
        for (i = 0; i < l; i++) {
            node = nodes[i];
            if (node[0] === "*") {
                code = code.slice(0, i ? -1 : -3) + ";" + node[1] + (i + 1 < l ? "result+=" : "");
            } else if ("" + node === node) {
                code += '"' + node + '"+';
            } else {
                var tag = node[0], encode = node[1], content = node[2], obj = node[3], params = node[4], paramsOrEmptyString = params + '||"")+';
                if (content) {
                    nested.push(buildTmplFunction(content));
                }
                code += tag === "=" ? (!encode || encode === "html" ? "html(" + paramsOrEmptyString : encode === "none" ? ("(" + paramsOrEmptyString) : ('enc("' + encode + '",' + paramsOrEmptyString)) : 'tag("' + tag + '",$view,"' + (encode || "") + '",'
                    + (content ? nested.length : '""')
                    + "," + obj + (params ? "," : "") + params + ")+";
            }
        }
        ret = new Function("$data, $view", code.slice(0, -1) + ";return result;\n\n}catch(e){return views.err(e);}");
        ret.nested = nested;
        return ret;
    }

    function replacerForHtml(ch) {
        return escapeMapForHtml[ch] || (escapeMapForHtml[ch] = "&#" + ch.charCodeAt(0) + ";");
    }

    function try$(selector) {
        try {
            return $(selector);
        } catch (e) {
        }
        return selector;
    }
})(window);
(function ($) {
    $.fn.noUiSlider = function (options, flag) {
        var EVENT = window.navigator.msPointerEnabled ? 2 : 'ontouchend'in document ? 3 : 1;
        if (window.debug && console) {
            console.log(EVENT);
        }
        function call(f, scope, args) {
            if (typeof f === "function") {
                f.call(scope, args);
            }
        }

        var percentage = {to: function (range, value) {
            value = range[0] < 0 ? value + Math.abs(range[0]) : value - range[0];
            return(value * 100) / this._length(range);
        }, from: function (range, value) {
            return(value * 100) / this._length(range);
        }, is: function (range, value) {
            return((value * this._length(range)) / 100) + range[0];
        }, _length: function (range) {
            return(range[0] > range[1] ? range[0] - range[1] : range[1] - range[0]);
        }}

        function correct(proposal, slider, handle) {
            var
                setup = slider.data('setup'), handles = setup.handles, settings = setup.settings, pos = setup.pos;
            proposal = proposal < 0 ? 0 : proposal > 100 ? 100 : proposal;
            if (settings.handles == 2) {
                if (handle.is(':first-child')) {
                    var other = parseFloat(handles[1][0].style[pos]) - settings.margin;
                    proposal = proposal > other ? other : proposal;
                } else {
                    var other = parseFloat(handles[0][0].style[pos]) + settings.margin;
                    proposal = proposal < other ? other : proposal;
                }
            }
            if (settings.step) {
                var per = percentage.from(settings.range, settings.step);
                proposal = Math.round(proposal / per) * per;
            }
            return proposal;
        }

        function client(f) {
            try {
                return[(f.clientX || f.originalEvent.clientX || f.originalEvent.touches[0].clientX), (f.clientY || f.originalEvent.clientY || f.originalEvent.touches[0].clientY)];
            } catch (e) {
                return['x', 'y'];
            }
        }

        function place(handle, pos) {
            return parseFloat(handle[0].style[pos]);
        }

        var defaults = {handles: 2, serialization: {to: ['', ''], resolution: 0.01}};
        methods = {create: function () {
            return this.each(function () {
                function setHandle(handle, to, slider) {
                    handle.css(pos, to + '%').data('input').val(percentage.is(settings.range, to).toFixed(res));
                }

                var
                    settings = $.extend(defaults, options), handlehtml = '<a><div></div></a>', slider = $(this).data('_isnS_', true), handles = [], pos, orientation, classes = "", num = function (e) {
                        return!isNaN(parseFloat(e)) && isFinite(e);
                    }, split = (settings.serialization.resolution = settings.serialization.resolution || 0.01).toString().split('.'), res = split[0] == 1 ? 0 : split[1].length;
                settings.start = num(settings.start) ? [settings.start, 0] : settings.start;
                $.each(settings, function (a, b) {
                    if (num(b)) {
                        settings[a] = parseFloat(b);
                    } else if (typeof b == "object" && num(b[0])) {
                        b[0] = parseFloat(b[0]);
                        if (num(b[1])) {
                            b[1] = parseFloat(b[1]);
                        }
                    }
                    var e = false;
                    b = typeof b == "undefined" ? "x" : b;
                    switch (a) {
                        case'range':
                        case'start':
                            e = b.length != 2 || !num(b[0]) || !num(b[1]);
                            break;
                        case'handles':
                            e = (b < 1 || b > 2 || !num(b));
                            break;
                        case'connect':
                            e = b != "lower" && b != "upper" && typeof b != "boolean";
                            break;
                        case'orientation':
                            e = (b != "vertical" && b != "horizontal");
                            break;
                        case'margin':
                        case'step':
                            e = typeof b != "undefined" && !num(b);
                            break;
                        case'serialization':
                            e = typeof b != "object" || !num(b.resolution) || (typeof b.to == 'object' && b.to.length < settings.handles);
                            break;
                        case'slide':
                            e = typeof b != "function";
                            break;
                    }
                    if (e && console) {
                        console.error('Bad input for ' + a + ' on slider:', slider);
                    }
                });
                settings.margin = settings.margin ? percentage.from(settings.range, settings.margin) : 0;
                if (settings.serialization.to instanceof jQuery || typeof settings.serialization.to == 'string' || settings.serialization.to === false) {
                    settings.serialization.to = [settings.serialization.to];
                }
                if (settings.orientation == "vertical") {
                    classes += "vertical";
                    pos = 'top';
                    orientation = 1;
                } else {
                    classes += "horizontal";
                    pos = 'left';
                    orientation = 0;
                }
                classes += settings.connect ? settings.connect == "lower" ? " connect lower" : " connect" : "";
                slider.addClass(classes);
                for (var i = 0; i < settings.handles; i++) {
                    handles[i] = slider.append(handlehtml).children(':last');
                    var setTo = percentage.to(settings.range, settings.start[i]);
                    handles[i].css(pos, setTo + '%');
                    if (setTo == 100 && handles[i].is(':first-child')) {
                        handles[i].css('z-index', 2);
                    }
                    var bind = '.noUiSlider', onEvent = (EVENT === 1 ? 'mousedown' : EVENT === 2 ? 'MSPointerDown' : 'touchstart') + bind + 'X', moveEvent = (EVENT === 1 ? 'mousemove' : EVENT === 2 ? 'MSPointerMove' : 'touchmove') + bind, offEvent = (EVENT === 1 ? 'mouseup' : EVENT === 2 ? 'MSPointerUp' : 'touchend') + bind
                    handles[i].find('div').on(onEvent,function (e) {
                        $('body').bind('selectstart' + bind, function () {
                            return false;
                        });
                        if (!slider.hasClass('disabled')) {
                            $('body').addClass('TOUCH');
                            var handle = $(this).addClass('active').parent(), unbind = handle.add($(document)).add('body'), originalPosition = parseFloat(handle[0].style[pos]), originalClick = client(e), previousClick = originalClick, previousProposal = false;
                            $(document).on(moveEvent,function (f) {
                                f.preventDefault();
                                var currentClick = client(f);
                                if (currentClick[0] == "x") {
                                    return;
                                }
                                currentClick[0] -= originalClick[0];
                                currentClick[1] -= originalClick[1];
                                var movement = [previousClick[0] != currentClick[0], previousClick[1] != currentClick[1]], proposal = originalPosition + ((currentClick[orientation] * 100) / (orientation ? slider.height() : slider.width()));
                                proposal = correct(proposal, slider, handle);
                                if (movement[orientation] && proposal != previousProposal) {
                                    handle.css(pos, proposal + '%').data('input').val(percentage.is(settings.range, proposal).toFixed(res));
                                    call(settings.slide, slider.data('_n', true));
                                    previousProposal = proposal;
                                    handle.css('z-index', handles.length == 2 && proposal == 100 && handle.is(':first-child') ? 2 : 1);
                                }
                                previousClick = currentClick;
                            }).on(offEvent, function () {
                                    unbind.off(bind);
                                    $('body').removeClass('TOUCH');
                                    if (slider.find('.active').removeClass('active').end().data('_n')) {
                                        slider.data('_n', false).change();
                                    }
                                });
                        }
                    }).on('click', function (e) {
                            e.stopPropagation();
                        });
                }
                if (EVENT == 1) {
                    slider.on('click', function (f) {
                        if (!slider.hasClass('disabled')) {
                            var currentClick = client(f), proposal = ((currentClick[orientation] - slider.offset()[pos]) * 100) / (orientation ? slider.height() : slider.width()), handle = handles.length > 1 ? (currentClick[orientation] < (handles[0].offset()[pos] + handles[1].offset()[pos]) / 2 ? handles[0] : handles[1]) : handles[0];
                            setHandle(handle, correct(proposal, slider, handle), slider);
                            call(settings.slide, slider);
                            slider.change();
                        }
                    });
                }
                for (var i = 0; i < handles.length; i++) {
                    var val = percentage.is(settings.range, place(handles[i], pos)).toFixed(res);
                    if (typeof settings.serialization.to[i] == 'string') {
                        handles[i].data('input', slider.append('<input type="hidden" name="' + settings.serialization.to[i] + '">').find('input:last').val(val).change(function (a) {
                            a.stopPropagation();
                        }));
                    } else if (settings.serialization.to[i] == false) {
                        handles[i].data('input', {val: function (a) {
                            if (typeof a != 'undefined') {
                                this.handle.data('noUiVal', a);
                            } else {
                                return this.handle.data('noUiVal');
                            }
                        }, handle: handles[i]});
                    } else {
                        handles[i].data('input', settings.serialization.to[i].data('handleNR', i).val(val).change(function () {
                            var arr = [null, null];
                            arr[$(this).data('handleNR')] = $(this).val();
                            slider.val(arr);
                        }));
                    }
                }
                $(this).data('setup', {settings: settings, handles: handles, pos: pos, res: res});
            });
        }, val: function () {
            if (typeof arguments[0] !== 'undefined') {
                var val = typeof arguments[0] == 'number' ? [arguments[0]] : arguments[0];
                return this.each(function () {
                    var setup = $(this).data('setup');
                    for (var i = 0; i < setup.handles.length; i++) {
                        if (val[i] != null) {
                            var proposal = correct(percentage.to(setup.settings.range, val[i]), $(this), setup.handles[i]);
                            setup.handles[i].css(setup.pos, proposal + '%').data('input').val(percentage.is(setup.settings.range, proposal).toFixed(setup.res));
                        }
                    }
                });
            } else {
                var handles = $(this).data('setup').handles, re = [];
                for (var i = 0; i < handles.length; i++) {
                    re.push(parseFloat(handles[i].data('input').val()));
                }
                return re.length == 1 ? re[0] : re;
            }
        }, disabled: function () {
            return flag ? $(this).addClass('disabled') : $(this).removeClass('disabled');
        }}
        var $_val = jQuery.fn.val;
        jQuery.fn.val = function () {
            return this.data('_isnS_') ? methods.val.apply(this, arguments) : $_val.apply(this, arguments);
        }
        return options == "disabled" ? methods.disabled.apply(this) : methods.create.apply(this);
    }
})(jQuery);
tl = window.tl || {};
tl.pg = tl.pg || {};
tl.pg.default_prefs = {'auto_show_first': true, 'loading_selector': '#loading', 'track_events_cb': function () {
    return;
}, 'handle_doc_switch': null, 'custom_open_button': null, 'pg_caption': 'page guide', 'check_welcome_dismissed': function () {
    var key = 'tlypageguide_welcome_shown_' + tl.pg.hashUrl();
    try {
        if (localStorage.getItem(key)) {
            return true;
        }
    } catch (e) {
        if (document.cookie.indexOf(key) > -1) {
            return true;
        }
    }
    return false;
}, 'dismiss_welcome': function () {
    var key = 'tlypageguide_welcome_shown_' + tl.pg.hashUrl();
    try {
        localStorage.setItem(key, true);
    } catch (e) {
        var exp = new Date();
        exp.setDate(exp.getDate() + 365);
        document.cookie = (key + '=true; expires=' + exp.toUTCString());
    }
}};
tl.pg.init = function (preferences) {
    preferences = jQuery.extend({}, tl.pg.default_prefs, preferences);
    if (jQuery("#tlyPageGuide").length === 0) {
        return;
    }
    jQuery('#tlyPageGuideWrapper').remove();
    var guide = jQuery("#tlyPageGuide"), wrapper = jQuery('<div>', {id: 'tlyPageGuideWrapper'}), message = jQuery('<div>', {id: 'tlyPageGuideMessages'}), $welcome = jQuery('#tlyPageGuideWelcome');
    message.append('<a href="#" class="tlypageguide_close" title="Close Guide">close</a>').append('<span></span>').append('<div></div>').append('<a href="#" class="tlypageguide_back" title="Previous">Previous</a>').append('<a href="#" class="tlypageguide_fwd" title="Next">Next</a>');
    if (preferences.custom_open_button == null && $('.tlypageguide_toggle').length < 1) {
        jQuery('<div/>', {'title': 'Launch Page Guide', 'class': 'tlypageguide_toggle'}).append(preferences.pg_caption).append('<div><span>' + guide.data('tourtitle') + '</span></div>').append('<a href="#" class="tlypageguide_close" title="close guide">close guide &raquo;</a>').appendTo(wrapper);
    }
    if ($welcome.length > 0) {
        preferences.show_welcome = !preferences.check_welcome_dismissed();
        if (preferences.show_welcome) {
            jQuery('body').prepend('<div id="tlyPageGuideOverlay"></div>');
            $welcome.appendTo(wrapper);
        }
    }
    wrapper.append(guide);
    wrapper.append(message);
    jQuery('body').append(wrapper);
    var pg = new tl.pg.PageGuide(jQuery('#tlyPageGuideWrapper'), preferences);
    pg.ready(function () {
        pg.setup_handlers();
        pg.$base.children(".tlypageguide_toggle").animate({"right": "-120px"}, 250);
    });
    if (pg.preferences.show_welcome) {
        pg.pop_welcome();
    }
    return pg;
};
tl.pg.PageGuide = function (pg_elem, preferences) {
    this.preferences = preferences;
    this.$base = pg_elem;
    this.$all_items = jQuery('#tlyPageGuide > li', this.$base);
    this.$items = jQuery([]);
    this.$message = jQuery('#tlyPageGuideMessages');
    this.$fwd = jQuery('a.tlypageguide_fwd', this.$base);
    this.$back = jQuery('a.tlypageguide_back', this.$base);
    this.$welcome = jQuery('#tlyPageGuideWelcome');
    this.cur_idx = 0;
    this.track_event = this.preferences.track_events_cb;
    this.handle_doc_switch = this.preferences.handle_doc_switch;
    this.custom_open_button = this.preferences.custom_open_button;
    this.is_open = false;
};
tl.pg.hashUrl = function () {
    var str = window.location.href;
    var hash = 0, i, char;
    if (str.length === 0) {
        return hash;
    }
    for (i = 0; i < str.length; i++) {
        char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return hash.toString();
};
tl.pg.isScrolledIntoView = function (elem) {
    var dvtop = jQuery(window).scrollTop(), dvbtm = dvtop + jQuery(window).height(), eltop = jQuery(elem).offset().top, elbtm = eltop + jQuery(elem).height();
    return(elbtm >= dvtop) && (eltop <= dvbtm - 100);
};
tl.pg.PageGuide.prototype.ready = function (callback) {
    var that = this, interval = window.setInterval(function () {
        if (!jQuery(that.preferences.loading_selector).is(':visible')) {
            callback();
            clearInterval(interval);
        }
    }, 250);
    return this;
};
tl.pg.PageGuide.prototype._on_expand = function () {
    var that = this, $d = document, $w = window;
    this.position_tour();
    this.cur_idx = 0;
    var ns = $d.createElement('style');
    $d.getElementsByTagName('head')[0].appendChild(ns);
    if (!$w.createPopup) {
        ns.appendChild($d.createTextNode(''));
        ns.setAttribute("type", "text/css");
    }
    var sh = $d.styleSheets[$d.styleSheets.length - 1];
    var ie = "";
    this.$items.each(function (i) {
        var $p = jQuery(jQuery(this).data('tourtarget') + ":visible:first");
        $p.addClass("tlypageguide_shadow tlypageguide_shadow" + i);
        var node_text = '.tlypageguide_shadow' + i + ':after { height: ' +
            $p.outerHeight() + 'px; width: ' + $p.outerWidth(false) + 'px; }';
        if (!$w.createPopup) {
            var k = $d.createTextNode(node_text, 0);
            ns.appendChild(k);
        } else {
            ie += node_text;
        }
        jQuery(this).prepend('<ins>' + (i + 1) + '</ins>');
        jQuery(this).data('idx', i);
    });
    if ($w.createPopup) {
        sh.cssText = ie;
    }
    if (this.preferences.auto_show_first && this.$items.length > 0) {
        this.show_message(0);
    }
};
tl.pg.PageGuide.prototype.open = function () {
    if (this.preferences.show_welcome) {
        this.preferences.dismiss_welcome();
        this.close_welcome();
    }
    if (this.is_open) {
        return;
    } else {
        this.is_open = true;
    }
    this.track_event('PG.open');
    this._on_expand();
    this.$items.toggleClass('expanded');
    jQuery('body').addClass('tlypageguide-open');
};
tl.pg.PageGuide.prototype.close = function () {
    if (!this.is_open) {
        return;
    } else {
        this.is_open = false;
    }
    this.track_event('PG.close');
    this.$items.toggleClass('expanded');
    this.$message.animate({height: "0"}, 500, function () {
        jQuery(this).hide();
    });
    $('[class~="tlypageguide_shadow"]').removeClass(function (i, c) {
        return c.match(/tlypageguide_shadow.*?\b/g).join(" ");
    });
    jQuery('ins').remove();
    jQuery('body').removeClass('tlypageguide-open');
};
tl.pg.PageGuide.prototype.setup_handlers = function () {
    var that = this;
    var interactor = (that.custom_open_button == null) ? jQuery('.tlypageguide_toggle', this.$base) : jQuery(that.custom_open_button);
    interactor.on('click', function () {
        if (that.is_open) {
            that.close();
        } else if (that.preferences.show_welcome && !that.preferences.check_welcome_dismissed() && !jQuery('body').hasClass('tlyPageGuideWelcomeOpen')) {
            that.pop_welcome();
        } else {
            that.open();
        }
        return false;
    });
    jQuery('.tlypageguide_close', this.$message.add(jQuery('.tlypageguide_toggle'))).on('click', function () {
        that.close();
        return false;
    });
    this.$all_items.on('click', function () {
        var new_index = jQuery(this).data('idx');
        that.track_event('PG.specific_elt');
        that.show_message(new_index);
    });
    this.$fwd.on('click', function () {
        var new_index = (that.cur_idx + 1) % that.$items.length;
        that.track_event('PG.fwd');
        that.show_message(new_index);
        return false;
    });
    this.$back.on('click', function () {
        var new_index = (that.cur_idx + that.$items.length - 1) % that.$items.length;
        that.track_event('PG.back');
        that.show_message(new_index, true);
        return false;
    });
    if (this.$welcome.length) {
        if (this.$welcome.find('.tlypageguide_ignore').length) {
            this.$welcome.on('click', '.tlypageguide_ignore', function () {
                that.close_welcome();
            });
        }
        if (this.$welcome.find('.tlypageguide_dismiss').length) {
            this.$welcome.on('click', '.tlypageguide_dismiss', function () {
                that.close_welcome();
                that.preferences.dismiss_welcome();
            });
        }
        this.$welcome.on('click', '.tlypageguide_start', function () {
            that.open();
        });
    }
    jQuery(window).resize(function () {
        that.position_tour();
    });
};
tl.pg.PageGuide.prototype.show_message = function (new_index, left) {
    var old_idx = this.cur_idx, old_item = this.$items[old_idx], new_item = this.$items[new_index];
    this.cur_idx = new_index;
    if (this.handle_doc_switch) {
        this.handle_doc_switch(jQuery(new_item).data('tourtarget'), jQuery(old_item).data('tourtarget'));
    }
    jQuery('div', this.$message).html(jQuery(new_item).children('div').html());
    this.$items.removeClass("tlypageguide-active");
    jQuery(new_item).addClass("tlypageguide-active");
    if (!tl.pg.isScrolledIntoView(jQuery(new_item))) {
        jQuery('html,body').animate({scrollTop: jQuery(new_item).offset().top - 50}, 500);
    }
    var defaultHeight = 100;
    var oldHeight = this.$message.css("height");
    this.$message.css("height", "auto");
    var height = this.$message.height();
    this.$message.css("height", oldHeight);
    if (height < defaultHeight) {
        height = defaultHeight;
    }
    if (height > jQuery(window).height() / 2) {
        height = jQuery(window).height() / 2;
    }
    height = height + "px";
    this.$message.not(':visible').show().animate({'height': height}, 500);
    this.roll_number(jQuery('span', this.$message), jQuery(new_item).children('ins').html(), left);
};
tl.pg.PageGuide.prototype.roll_number = function (num_wrapper, new_text, left) {
    num_wrapper.animate({'text-indent': (left ? '' : '-') + '50px'}, 'fast', function () {
        num_wrapper.html(new_text);
        num_wrapper.css({'text-indent': (left ? '-' : '') + '50px'}, 'fast').animate({'text-indent': "0"}, 'fast');
    });
};
tl.pg.PageGuide.prototype.position_tour = function () {
    this.$items = this.$all_items.filter(function () {
        return jQuery(jQuery(this).data('tourtarget')).is(':visible');
    });
    this.$items.each(function () {
        var arrow = jQuery(this), target = jQuery(arrow.data('tourtarget')).filter(':visible:first'), position = arrow.data('position'), setLeft = target.offset().left, setTop = target.offset().top;
        if (position == "fixed") {
            setTop -= jQuery(window).scrollTop();
        }
        if (arrow.hasClass("tlypageguide_top")) {
            setTop -= 60;
        } else if (arrow.hasClass("tlypageguide_bottom")) {
            setTop += target.outerHeight() + 15;
        } else {
            setTop += 5;
        }
        if (arrow.hasClass("tlypageguide_right")) {
            setLeft += target.outerWidth(false) + 15;
        } else if (arrow.hasClass("tlypageguide_left")) {
            setLeft -= 65;
        } else {
            setLeft += 5;
        }
        arrow.css({"left": setLeft + "px", "top": setTop + "px", "position": position});
    });
};
tl.pg.PageGuide.prototype.pop_welcome = function () {
    jQuery('body').addClass('tlyPageGuideWelcomeOpen');
};
tl.pg.PageGuide.prototype.close_welcome = function () {
    jQuery('body').removeClass('tlyPageGuideWelcomeOpen');
};
(function (a, b) {
    "use strict";
    var c = a.History = a.History || {}, d = a.jQuery;
    if (typeof c.Adapter != "undefined")throw new Error("History.js Adapter has already been loaded...");
    c.Adapter = {bind: function (a, b, c) {
        d(a).bind(b, c)
    }, trigger: function (a, b, c) {
        d(a).trigger(b, c)
    }, extractEventData: function (a, c, d) {
        var e = c && c.originalEvent && c.originalEvent[a] || d && d[a] || b;
        return e
    }, onDomLoad: function (a) {
        d(a)
    }}, typeof c.init != "undefined" && c.init()
})(window), function (a, b) {
    "use strict";
    var c = a.console || b, d = a.document, e = a.navigator, f = a.sessionStorage || !1, g = a.setTimeout, h = a.clearTimeout, i = a.setInterval, j = a.clearInterval, k = a.JSON, l = a.alert, m = a.History = a.History || {}, n = a.history;
    k.stringify = k.stringify || k.encode, k.parse = k.parse || k.decode;
    if (typeof m.init != "undefined")throw new Error("History.js Core has already been loaded...");
    m.init = function () {
        return typeof m.Adapter == "undefined" ? !1 : (typeof m.initCore != "undefined" && m.initCore(), typeof m.initHtml4 != "undefined" && m.initHtml4(), !0)
    }, m.initCore = function () {
        if (typeof m.initCore.initialized != "undefined")return!1;
        m.initCore.initialized = !0, m.options = m.options || {}, m.options.hashChangeInterval = m.options.hashChangeInterval || 100, m.options.safariPollInterval = m.options.safariPollInterval || 500, m.options.doubleCheckInterval = m.options.doubleCheckInterval || 500, m.options.storeInterval = m.options.storeInterval || 1e3, m.options.busyDelay = m.options.busyDelay || 250, m.options.debug = m.options.debug || !1, m.options.initialTitle = m.options.initialTitle || d.title, m.intervalList = [], m.clearAllIntervals = function () {
            var a, b = m.intervalList;
            if (typeof b != "undefined" && b !== null) {
                for (a = 0; a < b.length; a++)j(b[a]);
                m.intervalList = null
            }
        }, m.debug = function () {
            (m.options.debug || !1) && m.log.apply(m, arguments)
        }, m.log = function () {
            var a = typeof c != "undefined" && typeof c.log != "undefined" && typeof c.log.apply != "undefined", b = d.getElementById("log"), e, f, g, h, i;
            a ? (h = Array.prototype.slice.call(arguments), e = h.shift(), typeof c.debug != "undefined" ? c.debug.apply(c, [e, h]) : c.log.apply(c, [e, h])) : e = "\n" + arguments[0] + "\n";
            for (f = 1, g = arguments.length; f < g; ++f) {
                i = arguments[f];
                if (typeof i == "object" && typeof k != "undefined")try {
                    i = k.stringify(i)
                } catch (j) {
                }
                e += "\n" + i + "\n"
            }
            return b ? (b.value += e + "\n-----\n", b.scrollTop = b.scrollHeight - b.clientHeight) : a || l(e), !0
        }, m.getInternetExplorerMajorVersion = function () {
            var a = m.getInternetExplorerMajorVersion.cached = typeof m.getInternetExplorerMajorVersion.cached != "undefined" ? m.getInternetExplorerMajorVersion.cached : function () {
                var a = 3, b = d.createElement("div"), c = b.getElementsByTagName("i");
                while ((b.innerHTML = "<!--[if gt IE " + ++a + "]><i></i><![endif]-->") && c[0]);
                return a > 4 ? a : !1
            }();
            return a
        }, m.isInternetExplorer = function () {
            var a = m.isInternetExplorer.cached = typeof m.isInternetExplorer.cached != "undefined" ? m.isInternetExplorer.cached : Boolean(m.getInternetExplorerMajorVersion());
            return a
        }, m.emulated = {pushState: !Boolean(a.history && a.history.pushState && a.history.replaceState && !/ Mobile\/([1-7][a-z]|(8([abcde]|f(1[0-8]))))/i.test(e.userAgent) && !/AppleWebKit\/5([0-2]|3[0-2])/i.test(e.userAgent)), hashChange: Boolean(!("onhashchange"in a || "onhashchange"in d) || m.isInternetExplorer() && m.getInternetExplorerMajorVersion() < 8)}, m.enabled = !m.emulated.pushState, m.bugs = {setHash: Boolean(!m.emulated.pushState && e.vendor === "Apple Computer, Inc." && /AppleWebKit\/5([0-2]|3[0-3])/.test(e.userAgent)), safariPoll: Boolean(!m.emulated.pushState && e.vendor === "Apple Computer, Inc." && /AppleWebKit\/5([0-2]|3[0-3])/.test(e.userAgent)), ieDoubleCheck: Boolean(m.isInternetExplorer() && m.getInternetExplorerMajorVersion() < 8), hashEscape: Boolean(m.isInternetExplorer() && m.getInternetExplorerMajorVersion() < 7)}, m.isEmptyObject = function (a) {
            for (var b in a)return!1;
            return!0
        }, m.cloneObject = function (a) {
            var b, c;
            return a ? (b = k.stringify(a), c = k.parse(b)) : c = {}, c
        }, m.getRootUrl = function () {
            var a = d.location.protocol + "//" + (d.location.hostname || d.location.host);
            if (d.location.port || !1)a += ":" + d.location.port;
            return a += "/", a
        }, m.getBaseHref = function () {
            var a = d.getElementsByTagName("base"), b = null, c = "";
            return a.length === 1 && (b = a[0], c = b.href.replace(/[^\/]+$/, "")), c = c.replace(/\/+$/, ""), c && (c += "/"), c
        }, m.getBaseUrl = function () {
            var a = m.getBaseHref() || m.getBasePageUrl() || m.getRootUrl();
            return a
        }, m.getPageUrl = function () {
            var a = m.getState(!1, !1), b = (a || {}).url || d.location.href, c;
            return c = b.replace(/\/+$/, "").replace(/[^\/]+$/, function (a, b, c) {
                return/\./.test(a) ? a : a + "/"
            }), c
        }, m.getBasePageUrl = function () {
            var a = d.location.href.replace(/[#\?].*/, "").replace(/[^\/]+$/,function (a, b, c) {
                return/[^\/]$/.test(a) ? "" : a
            }).replace(/\/+$/, "") + "/";
            return a
        }, m.getFullUrl = function (a, b) {
            var c = a, d = a.substring(0, 1);
            return b = typeof b == "undefined" ? !0 : b, /[a-z]+\:\/\//.test(a) || (d === "/" ? c = m.getRootUrl() + a.replace(/^\/+/, "") : d === "#" ? c = m.getPageUrl().replace(/#.*/, "") + a : d === "?" ? c = m.getPageUrl().replace(/[\?#].*/, "") + a : b ? c = m.getBaseUrl() + a.replace(/^(\.\/)+/, "") : c = m.getBasePageUrl() + a.replace(/^(\.\/)+/, "")), c.replace(/\#$/, "")
        }, m.getShortUrl = function (a) {
            var b = a, c = m.getBaseUrl(), d = m.getRootUrl();
            return m.emulated.pushState && (b = b.replace(c, "")), b = b.replace(d, "/"), m.isTraditionalAnchor(b) && (b = "./" + b), b = b.replace(/^(\.\/)+/g, "./").replace(/\#$/, ""), b
        }, m.store = {}, m.idToState = m.idToState || {}, m.stateToId = m.stateToId || {}, m.urlToId = m.urlToId || {}, m.storedStates = m.storedStates || [], m.savedStates = m.savedStates || [], m.normalizeStore = function () {
            m.store.idToState = m.store.idToState || {}, m.store.urlToId = m.store.urlToId || {}, m.store.stateToId = m.store.stateToId || {}
        }, m.getState = function (a, b) {
            typeof a == "undefined" && (a = !0), typeof b == "undefined" && (b = !0);
            var c = m.getLastSavedState();
            return!c && b && (c = m.createStateObject()), a && (c = m.cloneObject(c), c.url = c.cleanUrl || c.url), c
        }, m.getIdByState = function (a) {
            var b = m.extractId(a.url), c;
            if (!b) {
                c = m.getStateString(a);
                if (typeof m.stateToId[c] != "undefined")b = m.stateToId[c]; else if (typeof m.store.stateToId[c] != "undefined")b = m.store.stateToId[c]; else {
                    for (; ;) {
                        b = (new Date).getTime() + String(Math.random()).replace(/\D/g, "");
                        if (typeof m.idToState[b] == "undefined" && typeof m.store.idToState[b] == "undefined")break
                    }
                    m.stateToId[c] = b, m.idToState[b] = a
                }
            }
            return b
        }, m.normalizeState = function (a) {
            var b, c;
            if (!a || typeof a != "object")a = {};
            if (typeof a.normalized != "undefined")return a;
            if (!a.data || typeof a.data != "object")a.data = {};
            b = {}, b.normalized = !0, b.title = a.title || "", b.url = m.getFullUrl(m.unescapeString(a.url || d.location.href)), b.hash = m.getShortUrl(b.url), b.data = m.cloneObject(a.data), b.id = m.getIdByState(b), b.cleanUrl = b.url.replace(/\??\&_suid.*/, ""), b.url = b.cleanUrl, c = !m.isEmptyObject(b.data);
            if (b.title || c)b.hash = m.getShortUrl(b.url).replace(/\??\&_suid.*/, ""), /\?/.test(b.hash) || (b.hash += "?"), b.hash += "&_suid=" + b.id;
            return b.hashedUrl = m.getFullUrl(b.hash), (m.emulated.pushState || m.bugs.safariPoll) && m.hasUrlDuplicate(b) && (b.url = b.hashedUrl), b
        }, m.createStateObject = function (a, b, c) {
            var d = {data: a, title: b, url: c};
            return d = m.normalizeState(d), d
        }, m.getStateById = function (a) {
            a = String(a);
            var c = m.idToState[a] || m.store.idToState[a] || b;
            return c
        }, m.getStateString = function (a) {
            var b, c, d;
            return b = m.normalizeState(a), c = {data: b.data, title: a.title, url: a.url}, d = k.stringify(c), d
        }, m.getStateId = function (a) {
            var b, c;
            return b = m.normalizeState(a), c = b.id, c
        }, m.getHashByState = function (a) {
            var b, c;
            return b = m.normalizeState(a), c = b.hash, c
        }, m.extractId = function (a) {
            var b, c, d;
            return c = /(.*)\&_suid=([0-9]+)$/.exec(a), d = c ? c[1] || a : a, b = c ? String(c[2] || "") : "", b || !1
        }, m.isTraditionalAnchor = function (a) {
            var b = !/[\/\?\.]/.test(a);
            return b
        }, m.extractState = function (a, b) {
            var c = null, d, e;
            return b = b || !1, d = m.extractId(a), d && (c = m.getStateById(d)), c || (e = m.getFullUrl(a), d = m.getIdByUrl(e) || !1, d && (c = m.getStateById(d)), !c && b && !m.isTraditionalAnchor(a) && (c = m.createStateObject(null, null, e))), c
        }, m.getIdByUrl = function (a) {
            var c = m.urlToId[a] || m.store.urlToId[a] || b;
            return c
        }, m.getLastSavedState = function () {
            return m.savedStates[m.savedStates.length - 1] || b
        }, m.getLastStoredState = function () {
            return m.storedStates[m.storedStates.length - 1] || b
        }, m.hasUrlDuplicate = function (a) {
            var b = !1, c;
            return c = m.extractState(a.url), b = c && c.id !== a.id, b
        }, m.storeState = function (a) {
            return m.urlToId[a.url] = a.id, m.storedStates.push(m.cloneObject(a)), a
        }, m.isLastSavedState = function (a) {
            var b = !1, c, d, e;
            return m.savedStates.length && (c = a.id, d = m.getLastSavedState(), e = d.id, b = c === e), b
        }, m.saveState = function (a) {
            return m.isLastSavedState(a) ? !1 : (m.savedStates.push(m.cloneObject(a)), !0)
        }, m.getStateByIndex = function (a) {
            var b = null;
            return typeof a == "undefined" ? b = m.savedStates[m.savedStates.length - 1] : a < 0 ? b = m.savedStates[m.savedStates.length + a] : b = m.savedStates[a], b
        }, m.getHash = function () {
            var a = m.unescapeHash(d.location.hash);
            return a
        }, m.unescapeString = function (b) {
            var c = b, d;
            for (; ;) {
                d = a.unescape(c);
                if (d === c)break;
                c = d
            }
            return c
        }, m.unescapeHash = function (a) {
            var b = m.normalizeHash(a);
            return b = m.unescapeString(b), b
        }, m.normalizeHash = function (a) {
            var b = a.replace(/[^#]*#/, "").replace(/#.*/, "");
            return b
        }, m.setHash = function (a, b) {
            var c, e, f;
            return b !== !1 && m.busy() ? (m.pushQueue({scope: m, callback: m.setHash, args: arguments, queue: b}), !1) : (c = m.escapeHash(a), m.busy(!0), e = m.extractState(a, !0), e && !m.emulated.pushState ? m.pushState(e.data, e.title, e.url, !1) : d.location.hash !== c && (m.bugs.setHash ? (f = m.getPageUrl(), m.pushState(null, null, f + "#" + c, !1)) : d.location.hash = c), m)
        }, m.escapeHash = function (b) {
            var c = m.normalizeHash(b);
            return c = a.escape(c), m.bugs.hashEscape || (c = c.replace(/\%21/g, "!").replace(/\%26/g, "&").replace(/\%3D/g, "=").replace(/\%3F/g, "?")), c
        }, m.getHashByUrl = function (a) {
            var b = String(a).replace(/([^#]*)#?([^#]*)#?(.*)/, "$2");
            return b = m.unescapeHash(b), b
        }, m.setTitle = function (a) {
            var b = a.title, c;
            b || (c = m.getStateByIndex(0), c && c.url === a.url && (b = c.title || m.options.initialTitle));
            try {
                d.getElementsByTagName("title")[0].innerHTML = b.replace("<", "&lt;").replace(">", "&gt;").replace(" & ", " &amp; ")
            } catch (e) {
            }
            return d.title = b, m
        }, m.queues = [], m.busy = function (a) {
            typeof a != "undefined" ? m.busy.flag = a : typeof m.busy.flag == "undefined" && (m.busy.flag = !1);
            if (!m.busy.flag) {
                h(m.busy.timeout);
                var b = function () {
                    var a, c, d;
                    if (m.busy.flag)return;
                    for (a = m.queues.length - 1; a >= 0; --a) {
                        c = m.queues[a];
                        if (c.length === 0)continue;
                        d = c.shift(), m.fireQueueItem(d), m.busy.timeout = g(b, m.options.busyDelay)
                    }
                };
                m.busy.timeout = g(b, m.options.busyDelay)
            }
            return m.busy.flag
        }, m.busy.flag = !1, m.fireQueueItem = function (a) {
            return a.callback.apply(a.scope || m, a.args || [])
        }, m.pushQueue = function (a) {
            return m.queues[a.queue || 0] = m.queues[a.queue || 0] || [], m.queues[a.queue || 0].push(a), m
        }, m.queue = function (a, b) {
            return typeof a == "function" && (a = {callback: a}), typeof b != "undefined" && (a.queue = b), m.busy() ? m.pushQueue(a) : m.fireQueueItem(a), m
        }, m.clearQueue = function () {
            return m.busy.flag = !1, m.queues = [], m
        }, m.stateChanged = !1, m.doubleChecker = !1, m.doubleCheckComplete = function () {
            return m.stateChanged = !0, m.doubleCheckClear(), m
        }, m.doubleCheckClear = function () {
            return m.doubleChecker && (h(m.doubleChecker), m.doubleChecker = !1), m
        }, m.doubleCheck = function (a) {
            return m.stateChanged = !1, m.doubleCheckClear(), m.bugs.ieDoubleCheck && (m.doubleChecker = g(function () {
                return m.doubleCheckClear(), m.stateChanged || a(), !0
            }, m.options.doubleCheckInterval)), m
        }, m.safariStatePoll = function () {
            var b = m.extractState(d.location.href), c;
            if (!m.isLastSavedState(b))c = b; else return;
            return c || (c = m.createStateObject()), m.Adapter.trigger(a, "popstate"), m
        }, m.back = function (a) {
            return a !== !1 && m.busy() ? (m.pushQueue({scope: m, callback: m.back, args: arguments, queue: a}), !1) : (m.busy(!0), m.doubleCheck(function () {
                m.back(!1)
            }), n.go(-1), !0)
        }, m.forward = function (a) {
            return a !== !1 && m.busy() ? (m.pushQueue({scope: m, callback: m.forward, args: arguments, queue: a}), !1) : (m.busy(!0), m.doubleCheck(function () {
                m.forward(!1)
            }), n.go(1), !0)
        }, m.go = function (a, b) {
            var c;
            if (a > 0)for (c = 1; c <= a; ++c)m.forward(b); else {
                if (!(a < 0))throw new Error("History.go: History.go requires a positive or negative integer passed.");
                for (c = -1; c >= a; --c)m.back(b)
            }
            return m
        };
        if (m.emulated.pushState) {
            var o = function () {
            };
            m.pushState = m.pushState || o, m.replaceState = m.replaceState || o
        } else m.onPopState = function (b, c) {
            var e = !1, f = !1, g, h;
            return m.doubleCheckComplete(), g = m.getHash(), g ? (h = m.extractState(g || d.location.href, !0), h ? m.replaceState(h.data, h.title, h.url, !1) : (m.Adapter.trigger(a, "anchorchange"), m.busy(!1)), m.expectedStateId = !1, !1) : (e = m.Adapter.extractEventData("state", b, c) || !1, e ? f = m.getStateById(e) : m.expectedStateId ? f = m.getStateById(m.expectedStateId) : f = m.extractState(d.location.href), f || (f = m.createStateObject(null, null, d.location.href)), m.expectedStateId = !1, m.isLastSavedState(f) ? (m.busy(!1), !1) : (m.storeState(f), m.saveState(f), m.setTitle(f), m.Adapter.trigger(a, "statechange"), m.busy(!1), !0))
        }, m.Adapter.bind(a, "popstate", m.onPopState), m.pushState = function (b, c, d, e) {
            if (m.getHashByUrl(d) && m.emulated.pushState)throw new Error("History.js does not support states with fragement-identifiers (hashes/anchors).");
            if (e !== !1 && m.busy())return m.pushQueue({scope: m, callback: m.pushState, args: arguments, queue: e}), !1;
            m.busy(!0);
            var f = m.createStateObject(b, c, d);
            return m.isLastSavedState(f) ? m.busy(!1) : (m.storeState(f), m.expectedStateId = f.id, n.pushState(f.id, f.title, f.url), m.Adapter.trigger(a, "popstate")), !0
        }, m.replaceState = function (b, c, d, e) {
            if (m.getHashByUrl(d) && m.emulated.pushState)throw new Error("History.js does not support states with fragement-identifiers (hashes/anchors).");
            if (e !== !1 && m.busy())return m.pushQueue({scope: m, callback: m.replaceState, args: arguments, queue: e}), !1;
            m.busy(!0);
            var f = m.createStateObject(b, c, d);
            return m.isLastSavedState(f) ? m.busy(!1) : (m.storeState(f), m.expectedStateId = f.id, n.replaceState(f.id, f.title, f.url), m.Adapter.trigger(a, "popstate")), !0
        };
        if (f) {
            try {
                m.store = k.parse(f.getItem("History.store")) || {}
            } catch (p) {
                m.store = {}
            }
            m.normalizeStore()
        } else m.store = {}, m.normalizeStore();
        m.Adapter.bind(a, "beforeunload", m.clearAllIntervals), m.Adapter.bind(a, "unload", m.clearAllIntervals), m.saveState(m.storeState(m.extractState(d.location.href, !0))), f && (m.onUnload = function () {
            var a, b;
            try {
                a = k.parse(f.getItem("History.store")) || {}
            } catch (c) {
                a = {}
            }
            a.idToState = a.idToState || {}, a.urlToId = a.urlToId || {}, a.stateToId = a.stateToId || {};
            for (b in m.idToState) {
                if (!m.idToState.hasOwnProperty(b))continue;
                a.idToState[b] = m.idToState[b]
            }
            for (b in m.urlToId) {
                if (!m.urlToId.hasOwnProperty(b))continue;
                a.urlToId[b] = m.urlToId[b]
            }
            for (b in m.stateToId) {
                if (!m.stateToId.hasOwnProperty(b))continue;
                a.stateToId[b] = m.stateToId[b]
            }
            m.store = a, m.normalizeStore(), f.setItem("History.store", k.stringify(a))
        }, m.intervalList.push(i(m.onUnload, m.options.storeInterval)), m.Adapter.bind(a, "beforeunload", m.onUnload), m.Adapter.bind(a, "unload", m.onUnload));
        if (!m.emulated.pushState) {
            m.bugs.safariPoll && m.intervalList.push(i(m.safariStatePoll, m.options.safariPollInterval));
            if (e.vendor === "Apple Computer, Inc." || (e.appCodeName || "") === "Mozilla")m.Adapter.bind(a, "hashchange", function () {
                m.Adapter.trigger(a, "popstate")
            }), m.getHash() && m.Adapter.onDomLoad(function () {
                m.Adapter.trigger(a, "hashchange")
            })
        }
    }, m.init()
}(window)
$(document).ready(function () {
    var History = window.History;
    if (!History.enabled) {
        return false;
    }
    $(window).bind('load statechange', function () {
        var State = History.getState();
        var hash = History.getHash();
        if (!State.data || !State.data.tab) {
            if (hash) {
                State.data.tab = hash;
                window.location.hash = '';
            } else {
                State.data.tab = 'DEFAULT ACTIVE TAB';
            }
        }
        $('ul.nav-tabs > li > a[href="#' + State.data.tab + '"]').tab('show');
    });
    $('a[data-toggle="tab"]').on('shown', function (event) {
        var url = event.target.href.split("#")[0];
        var tab = event.target.href.split("#")[1];
        var State = History.getState();
        if (State.data.tab != tab) {
            History.pushState({'tab': tab}, null, url);
        }
    });
});
!function ($) {
    "use strict";
    var Tooltip = function (element, options) {
        this.init('tooltip', element, options)
    }
    Tooltip.prototype = {constructor: Tooltip, init: function (type, element, options) {
        var eventIn, eventOut
        this.type = type
        this.$element = $(element)
        this.options = this.getOptions(options)
        this.enabled = true
        if (this.options.trigger != 'manual') {
            eventIn = this.options.trigger == 'hover' ? 'mouseenter' : 'focus'
            eventOut = this.options.trigger == 'hover' ? 'mouseleave' : 'blur'
            this.$element.on(eventIn, this.options.selector, $.proxy(this.enter, this))
            this.$element.on(eventOut, this.options.selector, $.proxy(this.leave, this))
        }
        this.options.selector ? (this._options = $.extend({}, this.options, {trigger: 'manual', selector: ''})) : this.fixTitle()
    }, getOptions: function (options) {
        options = $.extend({}, $.fn[this.type].defaults, options, this.$element.data())
        if (options.delay && typeof options.delay == 'number') {
            options.delay = {show: options.delay, hide: options.delay}
        }
        return options
    }, enter: function (e) {
        var self = $(e.currentTarget)[this.type](this._options).data(this.type)
        if (!self.options.delay || !self.options.delay.show)return self.show()
        clearTimeout(this.timeout)
        self.hoverState = 'in'
        this.timeout = setTimeout(function () {
            if (self.hoverState == 'in')self.show()
        }, self.options.delay.show)
    }, leave: function (e) {
        var self = $(e.currentTarget)[this.type](this._options).data(this.type)
        if (this.timeout)clearTimeout(this.timeout)
        if (!self.options.delay || !self.options.delay.hide)return self.hide()
        self.hoverState = 'out'
        this.timeout = setTimeout(function () {
            if (self.hoverState == 'out')self.hide()
        }, self.options.delay.hide)
    }, show: function () {
        var $tip, inside, pos, actualWidth, actualHeight, placement, tp
        if (this.hasContent() && this.enabled) {
            $tip = this.tip()
            this.setContent()
            if (this.options.animation) {
                $tip.addClass('fade')
            }
            placement = typeof this.options.placement == 'function' ? this.options.placement.call(this, $tip[0], this.$element[0]) : this.options.placement
            inside = /in/.test(placement)
            $tip.remove().css({top: 0, left: 0, display: 'block'}).appendTo(inside ? this.$element : document.body)
            pos = this.getPosition(inside)
            actualWidth = $tip[0].offsetWidth
            actualHeight = $tip[0].offsetHeight
            switch (inside ? placement.split(' ')[1] : placement) {
                case'bottom':
                    tp = {top: pos.top + pos.height, left: pos.left + pos.width / 2 - actualWidth / 2}
                    break
                case'top':
                    tp = {top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2}
                    break
                case'left':
                    tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth}
                    break
                case'right':
                    tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width}
                    break
            }
            $tip.css(tp).addClass(placement).addClass('in')
        }
    }, isHTML: function (text) {
        return typeof text != 'string' || (text.charAt(0) === "<" && text.charAt(text.length - 1) === ">" && text.length >= 3) || /^(?:[^<]*<[\w\W]+>[^>]*$)/.exec(text)
    }, setContent: function () {
        var $tip = this.tip(), title = this.getTitle()
        $tip.find('.tooltip-inner')[this.isHTML(title) ? 'html' : 'text'](title)
        $tip.removeClass('fade in top bottom left right')
    }, hide: function () {
        var that = this, $tip = this.tip()
        $tip.removeClass('in')
        function removeWithAnimation() {
            var timeout = setTimeout(function () {
                $tip.off($.support.transition.end).remove()
            }, 500)
            $tip.one($.support.transition.end, function () {
                clearTimeout(timeout)
                $tip.remove()
            })
        }

        $.support.transition && this.$tip.hasClass('fade') ? removeWithAnimation() : $tip.remove()
    }, fixTitle: function () {
        var $e = this.$element
        if ($e.attr('title') || typeof($e.attr('data-original-title')) != 'string') {
            $e.attr('data-original-title', $e.attr('title') || '').removeAttr('title')
        }
    }, hasContent: function () {
        return this.getTitle()
    }, getPosition: function (inside) {
        return $.extend({}, (inside ? {top: 0, left: 0} : this.$element.offset()), {width: this.$element[0].offsetWidth, height: this.$element[0].offsetHeight})
    }, getTitle: function () {
        var title, $e = this.$element, o = this.options
        title = $e.attr('data-original-title') || (typeof o.title == 'function' ? o.title.call($e[0]) : o.title)
        return title
    }, tip: function () {
        return this.$tip = this.$tip || $(this.options.template)
    }, validate: function () {
        if (!this.$element[0].parentNode) {
            this.hide()
            this.$element = null
            this.options = null
        }
    }, enable: function () {
        this.enabled = true
    }, disable: function () {
        this.enabled = false
    }, toggleEnabled: function () {
        this.enabled = !this.enabled
    }, toggle: function () {
        this[this.tip().hasClass('in') ? 'hide' : 'show']()
    }}
    $.fn.tooltip = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data('tooltip'), options = typeof option == 'object' && option
            if (!data)$this.data('tooltip', (data = new Tooltip(this, options)))
            if (typeof option == 'string')data[option]()
        })
    }
    $.fn.tooltip.Constructor = Tooltip
    $.fn.tooltip.defaults = {animation: true, placement: 'top', selector: false, template: '<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>', trigger: 'hover', title: '', delay: 0}
}(window.jQuery);
!function ($) {
    "use strict";
    var Popover = function (element, options) {
        this.init('popover', element, options)
    }
    Popover.prototype = $.extend({}, $.fn.tooltip.Constructor.prototype, {constructor: Popover, setContent: function () {
        var $tip = this.tip(), title = this.getTitle(), content = this.getContent()
        $tip.find('.popover-title')[this.options.html ? 'html' : 'text'](title)
        $tip.find('.popover-content')[this.options.html ? 'html' : 'text'](content)
        $tip.removeClass('fade top bottom left right in')
    }, hasContent: function () {
        return this.getTitle() || this.getContent()
    }, getContent: function () {
        var content, $e = this.$element, o = this.options
        content = (typeof o.content == 'function' ? o.content.call($e[0]) : o.content) || $e.attr('data-content')
        return content
    }, tip: function () {
        if (!this.$tip) {
            this.$tip = $(this.options.template)
        }
        return this.$tip
    }, destroy: function () {
        this.hide().$element.off('.' + this.type).removeData(this.type)
    }})
    var old = $.fn.popover
    $.fn.popover = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data('popover'), options = typeof option == 'object' && option
            if (!data)$this.data('popover', (data = new Popover(this, options)))
            if (typeof option == 'string')data[option]()
        })
    }
    $.fn.popover.Constructor = Popover
    $.fn.popover.defaults = $.extend({}, $.fn.tooltip.defaults, {placement: 'right', trigger: 'click', content: '', template: '<div class="popover"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'})
    $.fn.popover.noConflict = function () {
        $.fn.popover = old
        return this
    }
}(window.jQuery);
!function ($) {
    "use strict";
    var Tab = function (element) {
        this.element = $(element)
    }
    Tab.prototype = {constructor: Tab, show: function () {
        var $this = this.element, $ul = $this.closest('ul:not(.dropdown-menu)'), selector = $this.attr('data-target'), previous, $target, e
        if (!selector) {
            selector = $this.attr('href')
            selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '')
        }
        if ($this.parent('li').hasClass('active'))return
        previous = $ul.find('.active a').last()[0]
        e = $.Event('show', {relatedTarget: previous})
        $this.trigger(e)
        if (e.isDefaultPrevented())return
        $target = $(selector)
        this.activate($this.parent('li'), $ul)
        this.activate($target, $target.parent(), function () {
            $this.trigger({type: 'shown', relatedTarget: previous})
        })
    }, activate: function (element, container, callback) {
        var $active = container.find('> .active'), transition = callback && $.support.transition && $active.hasClass('fade')

        function next() {
            $active.removeClass('active').find('> .dropdown-menu > .active').removeClass('active')
            element.addClass('active')
            if (transition) {
                element[0].offsetWidth
                element.addClass('in')
            } else {
                element.removeClass('fade')
            }
            if (element.parent('.dropdown-menu')) {
                element.closest('li.dropdown').addClass('active')
            }
            callback && callback()
        }

        transition ? $active.one($.support.transition.end, next) : next()
        $active.removeClass('in')
    }}
    $.fn.tab = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data('tab')
            if (!data)$this.data('tab', (data = new Tab(this)))
            if (typeof option == 'string')data[option]()
        })
    }
    $.fn.tab.Constructor = Tab
    $(function () {
        $('body').on('click.tab.data-api', '[data-toggle="tab"], [data-toggle="pill"]', function (e) {
            e.preventDefault()
            $(this).tab('show')
        })
    })
}(window.jQuery);
!function ($) {
    "use strict";
    var toggle = '[data-toggle=dropdown]', Dropdown = function (element) {
        var $el = $(element).on('click.dropdown.data-api', this.toggle)
        $('html').on('click.dropdown.data-api', function () {
            $el.parent().removeClass('open')
        })
    }
    Dropdown.prototype = {constructor: Dropdown, toggle: function (e) {
        var $this = $(this), $parent, isActive
        if ($this.is('.disabled, :disabled'))return
        $parent = getParent($this)
        isActive = $parent.hasClass('open')
        clearMenus()
        if (!isActive) {
            $parent.toggleClass('open')
            $this.focus()
        }
        return false
    }, keydown: function (e) {
        var $this, $items, $active, $parent, isActive, index
        if (!/(38|40|27)/.test(e.keyCode))return
        $this = $(this)
        e.preventDefault()
        e.stopPropagation()
        if ($this.is('.disabled, :disabled'))return
        $parent = getParent($this)
        isActive = $parent.hasClass('open')
        if (!isActive || (isActive && e.keyCode == 27))return $this.click()
        $items = $('[role=menu] li:not(.divider) a', $parent)
        if (!$items.length)return
        index = $items.index($items.filter(':focus'))
        if (e.keyCode == 38 && index > 0)index--
        if (e.keyCode == 40 && index < $items.length - 1)index++
        if (!~index)index = 0
        $items.eq(index).focus()
    }}
    function clearMenus() {
        getParent($(toggle)).removeClass('open')
    }

    function getParent($this) {
        var selector = $this.attr('data-target'), $parent
        if (!selector) {
            selector = $this.attr('href')
            selector = selector && /#/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '')
        }
        $parent = $(selector)
        $parent.length || ($parent = $this.parent())
        return $parent
    }

    $.fn.dropdown = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data('dropdown')
            if (!data)$this.data('dropdown', (data = new Dropdown(this)))
            if (typeof option == 'string')data[option].call($this)
        })
    }
    $.fn.dropdown.Constructor = Dropdown
    $(function () {
        $('html').on('click.dropdown.data-api touchstart.dropdown.data-api', clearMenus)
        $('body').on('click.dropdown touchstart.dropdown.data-api', '.dropdown form',function (e) {
            e.stopPropagation()
        }).on('click.dropdown.data-api touchstart.dropdown.data-api', toggle, Dropdown.prototype.toggle).on('keydown.dropdown.data-api touchstart.dropdown.data-api', toggle + ', [role=menu]', Dropdown.prototype.keydown)
    })
}(window.jQuery);
!function ($) {
    "use strict";
    var Button = function (element, options) {
        this.$element = $(element)
        this.options = $.extend({}, $.fn.button.defaults, options)
    }
    Button.prototype.setState = function (state) {
        var d = 'disabled', $el = this.$element, data = $el.data(), val = $el.is('input') ? 'val' : 'html'
        state = state + 'Text'
        data.resetText || $el.data('resetText', $el[val]())
        $el[val](data[state] || this.options[state])
        setTimeout(function () {
            state == 'loadingText' ? $el.addClass(d).attr(d, d) : $el.removeClass(d).removeAttr(d)
        }, 0)
    }
    Button.prototype.toggle = function () {
        var $parent = this.$element.closest('[data-toggle="buttons-radio"]')
        $parent && $parent.find('.active').removeClass('active')
        this.$element.toggleClass('active')
    }
    $.fn.button = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data('button'), options = typeof option == 'object' && option
            if (!data)$this.data('button', (data = new Button(this, options)))
            if (option == 'toggle')data.toggle()
            else if (option)data.setState(option)
        })
    }
    $.fn.button.defaults = {loadingText: 'loading...'}
    $.fn.button.Constructor = Button
    $(function () {
        $('body').on('click.button.data-api', '[data-toggle^=button]', function (e) {
            var $btn = $(e.target)
            if (!$btn.hasClass('btn'))$btn = $btn.closest('.btn')
            $btn.button('toggle')
        })
    })
}(window.jQuery);
(function () {
    var Mustache = function () {
        var _toString = Object.prototype.toString;
        Array.isArray = Array.isArray || function (obj) {
            return _toString.call(obj) == "[object Array]";
        }
        var _trim = String.prototype.trim, trim;
        if (_trim) {
            trim = function (text) {
                return text == null ? "" : _trim.call(text);
            }
        } else {
            var trimLeft, trimRight;
            if ((/\S/).test("\xA0")) {
                trimLeft = /^[\s\xA0]+/;
                trimRight = /[\s\xA0]+$/;
            } else {
                trimLeft = /^\s+/;
                trimRight = /\s+$/;
            }
            trim = function (text) {
                return text == null ? "" : text.toString().replace(trimLeft, "").replace(trimRight, "");
            }
        }
        var escapeMap = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': '&quot;', "'": '&#39;'};

        function escapeHTML(string) {
            return String(string).replace(/&(?!\w+;)|[<>"']/g, function (s) {
                return escapeMap[s] || s;
            });
        }

        var regexCache = {};
        var Renderer = function () {
        };
        Renderer.prototype = {otag: "{{", ctag: "}}", pragmas: {}, buffer: [], pragmas_implemented: {"IMPLICIT-ITERATOR": true}, context: {}, render: function (template, context, partials, in_recursion) {
            if (!in_recursion) {
                this.context = context;
                this.buffer = [];
            }
            if (!this.includes("", template)) {
                if (in_recursion) {
                    return template;
                } else {
                    this.send(template);
                    return;
                }
            }
            template = this.render_pragmas(template);
            var html = this.render_section(template, context, partials);
            if (html === false) {
                html = this.render_tags(template, context, partials, in_recursion);
            }
            if (in_recursion) {
                return html;
            } else {
                this.sendLines(html);
            }
        }, send: function (line) {
            if (line !== "") {
                this.buffer.push(line);
            }
        }, sendLines: function (text) {
            if (text) {
                var lines = text.split("\n");
                for (var i = 0; i < lines.length; i++) {
                    this.send(lines[i]);
                }
            }
        }, render_pragmas: function (template) {
            if (!this.includes("%", template)) {
                return template;
            }
            var that = this;
            var regex = this.getCachedRegex("render_pragmas", function (otag, ctag) {
                return new RegExp(otag + "%([\\w-]+) ?([\\w]+=[\\w]+)?" + ctag, "g");
            });
            return template.replace(regex, function (match, pragma, options) {
                if (!that.pragmas_implemented[pragma]) {
                    throw({message: "This implementation of mustache doesn't understand the '" +
                        pragma + "' pragma"});
                }
                that.pragmas[pragma] = {};
                if (options) {
                    var opts = options.split("=");
                    that.pragmas[pragma][opts[0]] = opts[1];
                }
                return"";
            });
        }, render_partial: function (name, context, partials) {
            name = trim(name);
            if (!partials || partials[name] === undefined) {
                throw({message: "unknown_partial '" + name + "'"});
            }
            if (!context || typeof context[name] != "object") {
                return this.render(partials[name], context, partials, true);
            }
            return this.render(partials[name], context[name], partials, true);
        }, render_section: function (template, context, partials) {
            if (!this.includes("#", template) && !this.includes("^", template)) {
                return false;
            }
            var that = this;
            var regex = this.getCachedRegex("render_section", function (otag, ctag) {
                return new RegExp("^([\\s\\S]*?)" +
                    otag + "(\\^|\\#)\\s*(.+)\\s*" +
                    ctag + "\n*([\\s\\S]*?)" +
                    otag + "\\/\\s*\\3\\s*" +
                    ctag + "\\s*([\\s\\S]*)$", "g");
            });
            return template.replace(regex, function (match, before, type, name, content, after) {
                var renderedBefore = before ? that.render_tags(before, context, partials, true) : "", renderedAfter = after ? that.render(after, context, partials, true) : "", renderedContent, value = that.find(name, context);
                if (type === "^") {
                    if (!value || Array.isArray(value) && value.length === 0) {
                        renderedContent = that.render(content, context, partials, true);
                    } else {
                        renderedContent = "";
                    }
                } else if (type === "#") {
                    if (Array.isArray(value)) {
                        renderedContent = that.map(value,function (row) {
                            return that.render(content, that.create_context(row), partials, true);
                        }).join("");
                    } else if (that.is_object(value)) {
                        renderedContent = that.render(content, that.create_context(value), partials, true);
                    } else if (typeof value == "function") {
                        renderedContent = value.call(context, content, function (text) {
                            return that.render(text, context, partials, true);
                        });
                    } else if (value) {
                        renderedContent = that.render(content, context, partials, true);
                    } else {
                        renderedContent = "";
                    }
                }
                return renderedBefore + renderedContent + renderedAfter;
            });
        }, render_tags: function (template, context, partials, in_recursion) {
            var that = this;
            var new_regex = function () {
                return that.getCachedRegex("render_tags", function (otag, ctag) {
                    return new RegExp(otag + "(=|!|>|&|\\{|%)?([^#\\^]+?)\\1?" + ctag + "+", "g");
                });
            };
            var regex = new_regex();
            var tag_replace_callback = function (match, operator, name) {
                switch (operator) {
                    case"!":
                        return"";
                    case"=":
                        that.set_delimiters(name);
                        regex = new_regex();
                        return"";
                    case">":
                        return that.render_partial(name, context, partials);
                    case"{":
                    case"&":
                        return that.find(name, context);
                    default:
                        return escapeHTML(that.find(name, context));
                }
            };
            var lines = template.split("\n");
            for (var i = 0; i < lines.length; i++) {
                lines[i] = lines[i].replace(regex, tag_replace_callback, this);
                if (!in_recursion) {
                    this.send(lines[i]);
                }
            }
            if (in_recursion) {
                return lines.join("\n");
            }
        }, set_delimiters: function (delimiters) {
            var dels = delimiters.split(" ");
            this.otag = this.escape_regex(dels[0]);
            this.ctag = this.escape_regex(dels[1]);
        }, escape_regex: function (text) {
            if (!arguments.callee.sRE) {
                var specials = ['/', '.', '*', '+', '?', '|', '(', ')', '[', ']', '{', '}', '\\'];
                arguments.callee.sRE = new RegExp('(\\' + specials.join('|\\') + ')', 'g');
            }
            return text.replace(arguments.callee.sRE, '\\$1');
        }, find: function (name, context) {
            name = trim(name);
            function is_kinda_truthy(bool) {
                return bool === false || bool === 0 || bool;
            }

            var value;
            if (name.match(/([a-z_]+)\./ig)) {
                var childValue = this.walk_context(name, context);
                if (is_kinda_truthy(childValue)) {
                    value = childValue;
                }
            } else {
                if (is_kinda_truthy(context[name])) {
                    value = context[name];
                } else if (is_kinda_truthy(this.context[name])) {
                    value = this.context[name];
                }
            }
            if (typeof value == "function") {
                return value.apply(context);
            }
            if (value !== undefined) {
                return value;
            }
            return"";
        }, walk_context: function (name, context) {
            var path = name.split('.');
            var value_context = (context[path[0]] != undefined) ? context : this.context;
            var value = value_context[path.shift()];
            while (value != undefined && path.length > 0) {
                value_context = value;
                value = value[path.shift()];
            }
            if (typeof value == "function") {
                return value.apply(value_context);
            }
            return value;
        }, includes: function (needle, haystack) {
            return haystack.indexOf(this.otag + needle) != -1;
        }, create_context: function (_context) {
            if (this.is_object(_context)) {
                return _context;
            } else {
                var iterator = ".";
                if (this.pragmas["IMPLICIT-ITERATOR"]) {
                    iterator = this.pragmas["IMPLICIT-ITERATOR"].iterator;
                }
                var ctx = {};
                ctx[iterator] = _context;
                return ctx;
            }
        }, is_object: function (a) {
            return a && typeof a == "object";
        }, map: function (array, fn) {
            if (typeof array.map == "function") {
                return array.map(fn);
            } else {
                var r = [];
                var l = array.length;
                for (var i = 0; i < l; i++) {
                    r.push(fn(array[i]));
                }
                return r;
            }
        }, getCachedRegex: function (name, generator) {
            var byOtag = regexCache[this.otag];
            if (!byOtag) {
                byOtag = regexCache[this.otag] = {};
            }
            var byCtag = byOtag[this.ctag];
            if (!byCtag) {
                byCtag = byOtag[this.ctag] = {};
            }
            var regex = byCtag[name];
            if (!regex) {
                regex = byCtag[name] = generator(this.otag, this.ctag);
            }
            return regex;
        }};
        return({name: "mustache.js", version: "0.4.0", to_html: function (template, view, partials, send_fun) {
            var renderer = new Renderer();
            if (send_fun) {
                renderer.send = send_fun;
            }
            renderer.render(template, view || {}, partials);
            if (!send_fun) {
                return renderer.buffer.join("\n");
            }
        }});
    }();
    (function () {
        function trim(stuff) {
            if (''.trim)return stuff.trim(); else return stuff.replace(/^\s+/, '').replace(/\s+$/, '');
        }

        var ich = {VERSION: "0.10", templates: {}, $: (typeof window !== 'undefined') ? window.jQuery || window.Zepto || null : null, addTemplate: function (name, templateString) {
            if (typeof name === 'object') {
                for (var template in name) {
                    this.addTemplate(template, name[template]);
                }
                return;
            }
            if (ich[name]) {
                console.error("Invalid name: " + name + ".");
            } else if (ich.templates[name]) {
                console.error("Template \"" + name + "  \" exists");
            } else {
                ich.templates[name] = templateString;
                ich[name] = function (data, raw) {
                    data = data || {};
                    var result = Mustache.to_html(ich.templates[name], data, ich.templates);
                    return(ich.$ && !raw) ? ich.$(result) : result;
                };
            }
        }, clearAll: function () {
            for (var key in ich.templates) {
                delete ich[key];
            }
            ich.templates = {};
        }, refresh: function () {
            ich.clearAll();
            ich.grabTemplates();
        }, grabTemplates: function () {
            var i, scripts = document.getElementsByTagName('script'), script, trash = [];
            for (i = 0, l = scripts.length; i < l; i++) {
                script = scripts[i];
                if (script && script.innerHTML && script.id && (script.type === "text/html" || script.type === "text/x-icanhaz")) {
                    ich.addTemplate(script.id, trim(script.innerHTML));
                    trash.unshift(script);
                }
            }
            for (i = 0, l = trash.length; i < l; i++) {
                trash[i].parentNode.removeChild(trash[i]);
            }
        }};
        if (typeof require !== 'undefined') {
            module.exports = ich;
        } else {
            window.ich = ich;
        }
        if (typeof document !== 'undefined') {
            if (ich.$) {
                ich.$(function () {
                    ich.grabTemplates();
                });
            } else {
                document.addEventListener('DOMContentLoaded', function () {
                    ich.grabTemplates();
                }, true);
            }
        }
    })();
})();
var Markdown;
if (typeof exports === "object" && typeof require === "function")
    Markdown = exports; else
    Markdown = {};
(function () {
    function identity(x) {
        return x;
    }

    function returnFalse(x) {
        return false;
    }

    function HookCollection() {
    }

    HookCollection.prototype = {chain: function (hookname, func) {
        var original = this[hookname];
        if (!original)
            throw new Error("unknown hook " + hookname);
        if (original === identity)
            this[hookname] = func; else
            this[hookname] = function (x) {
                return func(original(x));
            }
    }, set: function (hookname, func) {
        if (!this[hookname])
            throw new Error("unknown hook " + hookname);
        this[hookname] = func;
    }, addNoop: function (hookname) {
        this[hookname] = identity;
    }, addFalse: function (hookname) {
        this[hookname] = returnFalse;
    }};
    Markdown.HookCollection = HookCollection;
    function SaveHash() {
    }

    SaveHash.prototype = {set: function (key, value) {
        this["s_" + key] = value;
    }, get: function (key) {
        return this["s_" + key];
    }};
    Markdown.Converter = function () {
        var pluginHooks = this.hooks = new HookCollection();
        pluginHooks.addNoop("plainLinkText");
        pluginHooks.addNoop("preConversion");
        pluginHooks.addNoop("postConversion");
        var g_urls;
        var g_titles;
        var g_html_blocks;
        var g_list_level;
        this.makeHtml = function (text) {
            if (g_urls)
                throw new Error("Recursive call to converter.makeHtml");
            g_urls = new SaveHash();
            g_titles = new SaveHash();
            g_html_blocks = [];
            g_list_level = 0;
            text = pluginHooks.preConversion(text);
            text = text.replace(/~/g, "~T");
            text = text.replace(/\$/g, "~D");
            text = text.replace(/\r\n/g, "\n");
            text = text.replace(/\r/g, "\n");
            text = "\n\n" + text + "\n\n";
            text = _Detab(text);
            text = text.replace(/^[ \t]+$/mg, "");
            text = _HashHTMLBlocks(text);
            text = _StripLinkDefinitions(text);
            text = _RunBlockGamut(text);
            text = _UnescapeSpecialChars(text);
            text = text.replace(/~D/g, "$$");
            text = text.replace(/~T/g, "~");
            text = pluginHooks.postConversion(text);
            g_html_blocks = g_titles = g_urls = null;
            return text;
        };
        function _StripLinkDefinitions(text) {
            text = text.replace(/^[ ]{0,3}\[(.+)\]:[ \t]*\n?[ \t]*<?(\S+?)>?(?=\s|$)[ \t]*\n?[ \t]*((\n*)["(](.+?)[")][ \t]*)?(?:\n+)/gm, function (wholeMatch, m1, m2, m3, m4, m5) {
                m1 = m1.toLowerCase();
                g_urls.set(m1, _EncodeAmpsAndAngles(m2));
                if (m4) {
                    return m3;
                } else if (m5) {
                    g_titles.set(m1, m5.replace(/"/g, "&quot;"));
                }
                return"";
            });
            return text;
        }

        function _HashHTMLBlocks(text) {
            var block_tags_a = "p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|noscript|form|fieldset|iframe|math|ins|del"
            var block_tags_b = "p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|noscript|form|fieldset|iframe|math"
            text = text.replace(/^(<(p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|noscript|form|fieldset|iframe|math|ins|del)\b[^\r]*?\n<\/\2>[ \t]*(?=\n+))/gm, hashElement);
            text = text.replace(/^(<(p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|noscript|form|fieldset|iframe|math)\b[^\r]*?.*<\/\2>[ \t]*(?=\n+)\n)/gm, hashElement);
            text = text.replace(/\n[ ]{0,3}((<(hr)\b([^<>])*?\/?>)[ \t]*(?=\n{2,}))/g, hashElement);
            text = text.replace(/\n\n[ ]{0,3}(<!(--(?:|(?:[^>-]|-[^>])(?:[^-]|-[^-])*)--)>[ \t]*(?=\n{2,}))/g, hashElement);
            text = text.replace(/(?:\n\n)([ ]{0,3}(?:<([?%])[^\r]*?\2>)[ \t]*(?=\n{2,}))/g, hashElement);
            return text;
        }

        function hashElement(wholeMatch, m1) {
            var blockText = m1;
            blockText = blockText.replace(/^\n+/, "");
            blockText = blockText.replace(/\n+$/g, "");
            blockText = "\n\n~K" + (g_html_blocks.push(blockText) - 1) + "K\n\n";
            return blockText;
        }

        function _RunBlockGamut(text, doNotUnhash) {
            text = _DoHeaders(text);
            var replacement = "<hr />\n";
            text = text.replace(/^[ ]{0,2}([ ]?\*[ ]?){3,}[ \t]*$/gm, replacement);
            text = text.replace(/^[ ]{0,2}([ ]?-[ ]?){3,}[ \t]*$/gm, replacement);
            text = text.replace(/^[ ]{0,2}([ ]?_[ ]?){3,}[ \t]*$/gm, replacement);
            text = _DoLists(text);
            text = _DoCodeBlocks(text);
            text = _DoBlockQuotes(text);
            text = _HashHTMLBlocks(text);
            text = _FormParagraphs(text, doNotUnhash);
            return text;
        }

        function _RunSpanGamut(text) {
            text = _DoCodeSpans(text);
            text = _EscapeSpecialCharsWithinTagAttributes(text);
            text = _EncodeBackslashEscapes(text);
            text = _DoImages(text);
            text = _DoAnchors(text);
            text = _DoAutoLinks(text);
            text = text.replace(/~P/g, "://");
            text = _EncodeAmpsAndAngles(text);
            text = _DoItalicsAndBold(text);
            text = text.replace(/  +\n/g, " <br>\n");
            return text;
        }

        function _EscapeSpecialCharsWithinTagAttributes(text) {
            var regex = /(<[a-z\/!$]("[^"]*"|'[^']*'|[^'">])*>|<!(--(?:|(?:[^>-]|-[^>])(?:[^-]|-[^-])*)--)>)/gi;
            text = text.replace(regex, function (wholeMatch) {
                var tag = wholeMatch.replace(/(.)<\/?code>(?=.)/g, "$1`");
                tag = escapeCharacters(tag, wholeMatch.charAt(1) == "!" ? "\\`*_/" : "\\`*_");
                return tag;
            });
            return text;
        }

        function _DoAnchors(text) {
            text = text.replace(/(\[((?:\[[^\]]*\]|[^\[\]])*)\][ ]?(?:\n[ ]*)?\[(.*?)\])()()()()/g, writeAnchorTag);
            text = text.replace(/(\[((?:\[[^\]]*\]|[^\[\]])*)\]\([ \t]*()<?((?:\([^)]*\)|[^()])*?)>?[ \t]*((['"])(.*?)\6[ \t]*)?\))/g, writeAnchorTag);
            text = text.replace(/(\[([^\[\]]+)\])()()()()()/g, writeAnchorTag);
            return text;
        }

        function writeAnchorTag(wholeMatch, m1, m2, m3, m4, m5, m6, m7) {
            if (m7 == undefined)m7 = "";
            var whole_match = m1;
            var link_text = m2.replace(/:\/\//g, "~P");
            var link_id = m3.toLowerCase();
            var url = m4;
            var title = m7;
            if (url == "") {
                if (link_id == "") {
                    link_id = link_text.toLowerCase().replace(/ ?\n/g, " ");
                }
                url = "#" + link_id;
                if (g_urls.get(link_id) != undefined) {
                    url = g_urls.get(link_id);
                    if (g_titles.get(link_id) != undefined) {
                        title = g_titles.get(link_id);
                    }
                }
                else {
                    if (whole_match.search(/\(\s*\)$/m) > -1) {
                        url = "";
                    } else {
                        return whole_match;
                    }
                }
            }
            url = encodeProblemUrlChars(url);
            url = escapeCharacters(url, "*_");
            var result = "<a href=\"" + url + "\"";
            if (title != "") {
                title = attributeEncode(title);
                title = escapeCharacters(title, "*_");
                result += " title=\"" + title + "\"";
            }
            result += ">" + link_text + "</a>";
            return result;
        }

        function _DoImages(text) {
            text = text.replace(/(!\[(.*?)\][ ]?(?:\n[ ]*)?\[(.*?)\])()()()()/g, writeImageTag);
            text = text.replace(/(!\[(.*?)\]\s?\([ \t]*()<?(\S+?)>?[ \t]*((['"])(.*?)\6[ \t]*)?\))/g, writeImageTag);
            return text;
        }

        function attributeEncode(text) {
            return text.replace(/>/g, "&gt;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
        }

        function writeImageTag(wholeMatch, m1, m2, m3, m4, m5, m6, m7) {
            var whole_match = m1;
            var alt_text = m2;
            var link_id = m3.toLowerCase();
            var url = m4;
            var title = m7;
            if (!title)title = "";
            if (url == "") {
                if (link_id == "") {
                    link_id = alt_text.toLowerCase().replace(/ ?\n/g, " ");
                }
                url = "#" + link_id;
                if (g_urls.get(link_id) != undefined) {
                    url = g_urls.get(link_id);
                    if (g_titles.get(link_id) != undefined) {
                        title = g_titles.get(link_id);
                    }
                }
                else {
                    return whole_match;
                }
            }
            alt_text = escapeCharacters(attributeEncode(alt_text), "*_[]()");
            url = escapeCharacters(url, "*_");
            var result = "<img src=\"" + url + "\" alt=\"" + alt_text + "\"";
            title = attributeEncode(title);
            title = escapeCharacters(title, "*_");
            result += " title=\"" + title + "\"";
            result += " />";
            return result;
        }

        function _DoHeaders(text) {
            text = text.replace(/^(.+)[ \t]*\n=+[ \t]*\n+/gm, function (wholeMatch, m1) {
                return"<h1>" + _RunSpanGamut(m1) + "</h1>\n\n";
            });
            text = text.replace(/^(.+)[ \t]*\n-+[ \t]*\n+/gm, function (matchFound, m1) {
                return"<h2>" + _RunSpanGamut(m1) + "</h2>\n\n";
            });
            text = text.replace(/^(\#{1,6})[ \t]*(.+?)[ \t]*\#*\n+/gm, function (wholeMatch, m1, m2) {
                var h_level = m1.length;
                return"<h" + h_level + ">" + _RunSpanGamut(m2) + "</h" + h_level + ">\n\n";
            });
            return text;
        }

        function _DoLists(text) {
            text += "~0";
            var whole_list = /^(([ ]{0,3}([*+-]|\d+[.])[ \t]+)[^\r]+?(~0|\n{2,}(?=\S)(?![ \t]*(?:[*+-]|\d+[.])[ \t]+)))/gm;
            if (g_list_level) {
                text = text.replace(whole_list, function (wholeMatch, m1, m2) {
                    var list = m1;
                    var list_type = (m2.search(/[*+-]/g) > -1) ? "ul" : "ol";
                    var result = _ProcessListItems(list, list_type);
                    result = result.replace(/\s+$/, "");
                    result = "<" + list_type + ">" + result + "</" + list_type + ">\n";
                    return result;
                });
            } else {
                whole_list = /(\n\n|^\n?)(([ ]{0,3}([*+-]|\d+[.])[ \t]+)[^\r]+?(~0|\n{2,}(?=\S)(?![ \t]*(?:[*+-]|\d+[.])[ \t]+)))/g;
                text = text.replace(whole_list, function (wholeMatch, m1, m2, m3) {
                    var runup = m1;
                    var list = m2;
                    var list_type = (m3.search(/[*+-]/g) > -1) ? "ul" : "ol";
                    var result = _ProcessListItems(list, list_type);
                    result = runup + "<" + list_type + ">\n" + result + "</" + list_type + ">\n";
                    return result;
                });
            }
            text = text.replace(/~0/, "");
            return text;
        }

        var _listItemMarkers = {ol: "\\d+[.]", ul: "[*+-]"};

        function _ProcessListItems(list_str, list_type) {
            g_list_level++;
            list_str = list_str.replace(/\n{2,}$/, "\n");
            list_str += "~0";
            var marker = _listItemMarkers[list_type];
            var re = new RegExp("(^[ \\t]*)(" + marker + ")[ \\t]+([^\\r]+?(\\n+))(?=(~0|\\1(" + marker + ")[ \\t]+))", "gm");
            var last_item_had_a_double_newline = false;
            list_str = list_str.replace(re, function (wholeMatch, m1, m2, m3) {
                var item = m3;
                var leading_space = m1;
                var ends_with_double_newline = /\n\n$/.test(item);
                var contains_double_newline = ends_with_double_newline || item.search(/\n{2,}/) > -1;
                if (contains_double_newline || last_item_had_a_double_newline) {
                    item = _RunBlockGamut(_Outdent(item), true);
                }
                else {
                    item = _DoLists(_Outdent(item));
                    item = item.replace(/\n$/, "");
                    item = _RunSpanGamut(item);
                }
                last_item_had_a_double_newline = ends_with_double_newline;
                return"<li>" + item + "</li>\n";
            });
            list_str = list_str.replace(/~0/g, "");
            g_list_level--;
            return list_str;
        }

        function _DoCodeBlocks(text) {
            text += "~0";
            text = text.replace(/(?:\n\n|^)((?:(?:[ ]{4}|\t).*\n+)+)(\n*[ ]{0,3}[^ \t\n]|(?=~0))/g, function (wholeMatch, m1, m2) {
                var codeblock = m1;
                var nextChar = m2;
                codeblock = _EncodeCode(_Outdent(codeblock));
                codeblock = _Detab(codeblock);
                codeblock = codeblock.replace(/^\n+/g, "");
                codeblock = codeblock.replace(/\n+$/g, "");
                codeblock = "<pre><code>" + codeblock + "\n</code></pre>";
                return"\n\n" + codeblock + "\n\n" + nextChar;
            });
            text = text.replace(/~0/, "");
            return text;
        }

        function hashBlock(text) {
            text = text.replace(/(^\n+|\n+$)/g, "");
            return"\n\n~K" + (g_html_blocks.push(text) - 1) + "K\n\n";
        }

        function _DoCodeSpans(text) {
            text = text.replace(/(^|[^\\])(`+)([^\r]*?[^`])\2(?!`)/gm, function (wholeMatch, m1, m2, m3, m4) {
                var c = m3;
                c = c.replace(/^([ \t]*)/g, "");
                c = c.replace(/[ \t]*$/g, "");
                c = _EncodeCode(c);
                c = c.replace(/:\/\//g, "~P");
                return m1 + "<code>" + c + "</code>";
            });
            return text;
        }

        function _EncodeCode(text) {
            text = text.replace(/&/g, "&amp;");
            text = text.replace(/</g, "&lt;");
            text = text.replace(/>/g, "&gt;");
            text = escapeCharacters(text, "\*_{}[]\\", false);
            return text;
        }

        function _DoItalicsAndBold(text) {
            text = text.replace(/([\W_]|^)(\*\*|__)(?=\S)([^\r]*?\S[\*_]*)\2([\W_]|$)/g, "$1<strong>$3</strong>$4");
            text = text.replace(/([\W_]|^)(\*|_)(?=\S)([^\r\*_]*?\S)\2([\W_]|$)/g, "$1<em>$3</em>$4");
            return text;
        }

        function _DoBlockQuotes(text) {
            text = text.replace(/((^[ \t]*>[ \t]?.+\n(.+\n)*\n*)+)/gm, function (wholeMatch, m1) {
                var bq = m1;
                bq = bq.replace(/^[ \t]*>[ \t]?/gm, "~0");
                bq = bq.replace(/~0/g, "");
                bq = bq.replace(/^[ \t]+$/gm, "");
                bq = _RunBlockGamut(bq);
                bq = bq.replace(/(^|\n)/g, "$1  ");
                bq = bq.replace(/(\s*<pre>[^\r]+?<\/pre>)/gm, function (wholeMatch, m1) {
                    var pre = m1;
                    pre = pre.replace(/^  /mg, "~0");
                    pre = pre.replace(/~0/g, "");
                    return pre;
                });
                return hashBlock("<blockquote>\n" + bq + "\n</blockquote>");
            });
            return text;
        }

        function _FormParagraphs(text, doNotUnhash) {
            text = text.replace(/^\n+/g, "");
            text = text.replace(/\n+$/g, "");
            var grafs = text.split(/\n{2,}/g);
            var grafsOut = [];
            var markerRe = /~K(\d+)K/;
            var end = grafs.length;
            for (var i = 0; i < end; i++) {
                var str = grafs[i];
                if (markerRe.test(str)) {
                    grafsOut.push(str);
                }
                else if (/\S/.test(str)) {
                    str = _RunSpanGamut(str);
                    str = str.replace(/^([ \t]*)/g, "<p>");
                    str += "</p>"
                    grafsOut.push(str);
                }
            }
            if (!doNotUnhash) {
                end = grafsOut.length;
                for (var i = 0; i < end; i++) {
                    var foundAny = true;
                    while (foundAny) {
                        foundAny = false;
                        grafsOut[i] = grafsOut[i].replace(/~K(\d+)K/g, function (wholeMatch, id) {
                            foundAny = true;
                            return g_html_blocks[id];
                        });
                    }
                }
            }
            return grafsOut.join("\n\n");
        }

        function _EncodeAmpsAndAngles(text) {
            text = text.replace(/&(?!#?[xX]?(?:[0-9a-fA-F]+|\w+);)/g, "&amp;");
            text = text.replace(/<(?![a-z\/?\$!])/gi, "&lt;");
            return text;
        }

        function _EncodeBackslashEscapes(text) {
            text = text.replace(/\\(\\)/g, escapeCharacters_callback);
            text = text.replace(/\\([`*_{}\[\]()>#+-.!])/g, escapeCharacters_callback);
            return text;
        }

        function _DoAutoLinks(text) {
            text = text.replace(/(^|\s)(https?|ftp)(:\/\/[-A-Z0-9+&@#\/%?=~_|\[\]\(\)!:,\.;]*[-A-Z0-9+&@#\/%=~_|\[\]])($|\W)/gi, "$1<$2$3>$4");
            var replacer = function (wholematch, m1) {
                return"<a href=\"" + m1 + "\">" + pluginHooks.plainLinkText(m1) + "</a>";
            }
            text = text.replace(/<((https?|ftp):[^'">\s]+)>/gi, replacer);
            return text;
        }

        function _UnescapeSpecialChars(text) {
            text = text.replace(/~E(\d+)E/g, function (wholeMatch, m1) {
                var charCodeToReplace = parseInt(m1);
                return String.fromCharCode(charCodeToReplace);
            });
            return text;
        }

        function _Outdent(text) {
            text = text.replace(/^(\t|[ ]{1,4})/gm, "~0");
            text = text.replace(/~0/g, "")
            return text;
        }

        function _Detab(text) {
            if (!/\t/.test(text))
                return text;
            var spaces = ["    ", "   ", "  ", " "], skew = 0, v;
            return text.replace(/[\n\t]/g, function (match, offset) {
                if (match === "\n") {
                    skew = offset + 1;
                    return match;
                }
                v = (offset - skew) % 4;
                skew = offset + 1;
                return spaces[v];
            });
        }

        var _problemUrlChars = /(?:["'*()[\]:]|~D)/g;

        function encodeProblemUrlChars(url) {
            if (!url)
                return"";
            var len = url.length;
            return url.replace(_problemUrlChars, function (match, offset) {
                if (match == "~D")
                    return"%24";
                if (match == ":") {
                    if (offset == len - 1 || /[0-9\/]/.test(url.charAt(offset + 1)))
                        return":"
                }
                return"%" + match.charCodeAt(0).toString(16);
            });
        }

        function escapeCharacters(text, charsToEscape, afterBackslash) {
            var regexString = "([" + charsToEscape.replace(/([\[\]\\])/g, "\\$1") + "])";
            if (afterBackslash) {
                regexString = "\\\\" + regexString;
            }
            var regex = new RegExp(regexString, "g");
            text = text.replace(regex, escapeCharacters_callback);
            return text;
        }

        function escapeCharacters_callback(wholeMatch, m1) {
            var charCodeToEscape = m1.charCodeAt(0);
            return"~E" + charCodeToEscape + "E";
        }
    };
})();
(function () {
    var output, Converter;
    if (typeof exports === "object" && typeof require === "function") {
        output = exports;
        Converter = require("./Markdown.Converter").Converter;
    } else {
        output = window.Markdown;
        Converter = output.Converter;
    }
    output.getSanitizingConverter = function () {
        var converter = new Converter();
        converter.hooks.chain("postConversion", sanitizeHtml);
        converter.hooks.chain("postConversion", balanceTags);
        return converter;
    }
    function sanitizeHtml(html) {
        return html.replace(/<[^>]*>?/gi, sanitizeTag);
    }

    var basic_tag_whitelist = /^(<\/?(b|blockquote|code|del|dd|dl|dt|em|h1|h2|h3|i|kbd|li|ol|p|pre|s|sup|sub|strong|strike|ul)>|<(br|hr)\s?\/?>)$/i;
    var a_white = /^(<a\shref="((https?|ftp):\/\/|\/)[-A-Za-z0-9+&@#\/%?=~_|!:,.;\(\)]+"(\stitle="[^"<>]+")?\s?>|<\/a>)$/i;
    var img_white = /^(<img\ssrc="(https?:\/\/|\/)[-A-Za-z0-9+&@#\/%?=~_|!:,.;\(\)]+"(\swidth="\d{1,3}")?(\sheight="\d{1,3}")?(\salt="[^"<>]*")?(\stitle="[^"<>]*")?\s?\/?>)$/i;

    function sanitizeTag(tag) {
        if (tag.match(basic_tag_whitelist) || tag.match(a_white) || tag.match(img_white))
            return tag; else
            return"";
    }

    function balanceTags(html) {
        if (html == "")
            return"";
        var re = /<\/?\w+[^>]*(\s|$|>)/g;
        var tags = html.toLowerCase().match(re);
        var tagcount = (tags || []).length;
        if (tagcount == 0)
            return html;
        var tagname, tag;
        var ignoredtags = "<p><img><br><li><hr>";
        var match;
        var tagpaired = [];
        var tagremove = [];
        var needsRemoval = false;
        for (var ctag = 0; ctag < tagcount; ctag++) {
            tagname = tags[ctag].replace(/<\/?(\w+).*/, "$1");
            if (tagpaired[ctag] || ignoredtags.search("<" + tagname + ">") > -1)
                continue;
            tag = tags[ctag];
            match = -1;
            if (!/^<\//.test(tag)) {
                for (var ntag = ctag + 1; ntag < tagcount; ntag++) {
                    if (!tagpaired[ntag] && tags[ntag] == "</" + tagname + ">") {
                        match = ntag;
                        break;
                    }
                }
            }
            if (match == -1)
                needsRemoval = tagremove[ctag] = true; else
                tagpaired[match] = true;
        }
        if (!needsRemoval)
            return html;
        var ctag = 0;
        html = html.replace(re, function (match) {
            var res = tagremove[ctag] ? "" : match;
            ctag++;
            return res;
        });
        return html;
    }
})();
﻿
(function () {
    var util = {}, position = {}, ui = {}, doc = window.document, re = window.RegExp, nav = window.navigator, SETTINGS = {lineLength: 72}, uaSniffed = {isIE: /msie/.test(nav.userAgent.toLowerCase()), isIE_5or6: /msie 6/.test(nav.userAgent.toLowerCase()) || /msie 5/.test(nav.userAgent.toLowerCase()), isOpera: /opera/.test(nav.userAgent.toLowerCase())};
    var linkDialogText = "<p><b>Insert Hyperlink</b></p><p>http://example.com/ \"optional title\"</p>";
    var imageDialogText = "<p><b>Insert Image</b></p><p>http://example.com/images/diagram.jpg \"optional title\"<br><br>Need <a href='http://www.google.com/search?q=free+image+hosting' target='_blank'>free image hosting?</a></p>";
    var imageDefaultText = "http://";
    var linkDefaultText = "http://";
    var defaultHelpHoverTitle = "Markdown Editing Help";
    Markdown.Editor = function (markdownConverter, selectors, idPostfix, help) {
        idPostfix = idPostfix || "";
        idButton = "wmd-button-bar";
        idPreview = "wmd-preview";
        idInput = "wmd-input";
        if (selectors) {
            if (selectors.hasOwnProperty('button'))
                idButton = selectors['button']
            if (selectors.hasOwnProperty('preview'))
                idPreview = selectors['preview']
            if (selectors.hasOwnProperty('input'))
                idInput = selectors['input']
        }
        var hooks = this.hooks = new Markdown.HookCollection();
        hooks.addNoop("onPreviewRefresh");
        hooks.addNoop("postBlockquoteCreation");
        hooks.addFalse("insertImageDialog");
        this.getConverter = function () {
            return markdownConverter;
        }
        var that = this, panels;
        this.run = function () {
            if (panels)
                return;
            panels = new PanelCollection(idButton, idPreview, idInput, idPostfix);
            var commandManager = new CommandManager(hooks);
            var previewManager = new PreviewManager(markdownConverter, panels, function () {
                hooks.onPreviewRefresh();
            });
            var undoManager, uiManager;
            if (!/\?noundo/.test(doc.location.href)) {
                undoManager = new UndoManager(function () {
                    previewManager.refresh();
                    if (uiManager)
                        uiManager.setUndoRedoButtonStates();
                }, panels);
                this.textOperation = function (f) {
                    undoManager.setCommandMode();
                    f();
                    that.refreshPreview();
                }
            }
            uiManager = new UIManager(idPostfix, panels, undoManager, previewManager, commandManager, help);
            uiManager.setUndoRedoButtonStates();
            var forceRefresh = that.refreshPreview = function () {
                previewManager.refresh(true);
            };
            forceRefresh();
        };
    }
    function Chunks() {
    }

    Chunks.prototype.findTags = function (startRegex, endRegex) {
        var chunkObj = this;
        var regex;
        if (startRegex) {
            regex = util.extendRegExp(startRegex, "", "$");
            this.before = this.before.replace(regex, function (match) {
                chunkObj.startTag = chunkObj.startTag + match;
                return"";
            });
            regex = util.extendRegExp(startRegex, "^", "");
            this.selection = this.selection.replace(regex, function (match) {
                chunkObj.startTag = chunkObj.startTag + match;
                return"";
            });
        }
        if (endRegex) {
            regex = util.extendRegExp(endRegex, "", "$");
            this.selection = this.selection.replace(regex, function (match) {
                chunkObj.endTag = match + chunkObj.endTag;
                return"";
            });
            regex = util.extendRegExp(endRegex, "^", "");
            this.after = this.after.replace(regex, function (match) {
                chunkObj.endTag = match + chunkObj.endTag;
                return"";
            });
        }
    };
    Chunks.prototype.trimWhitespace = function (remove) {
        var beforeReplacer, afterReplacer, that = this;
        if (remove) {
            beforeReplacer = afterReplacer = "";
        } else {
            beforeReplacer = function (s) {
                that.before += s;
                return"";
            }
            afterReplacer = function (s) {
                that.after = s + that.after;
                return"";
            }
        }
        this.selection = this.selection.replace(/^(\s*)/, beforeReplacer).replace(/(\s*)$/, afterReplacer);
    };
    Chunks.prototype.skipLines = function (nLinesBefore, nLinesAfter, findExtraNewlines) {
        if (nLinesBefore === undefined) {
            nLinesBefore = 1;
        }
        if (nLinesAfter === undefined) {
            nLinesAfter = 1;
        }
        nLinesBefore++;
        nLinesAfter++;
        var regexText;
        var replacementText;
        if (navigator.userAgent.match(/Chrome/)) {
            "X".match(/()./);
        }
        this.selection = this.selection.replace(/(^\n*)/, "");
        this.startTag = this.startTag + re.$1;
        this.selection = this.selection.replace(/(\n*$)/, "");
        this.endTag = this.endTag + re.$1;
        this.startTag = this.startTag.replace(/(^\n*)/, "");
        this.before = this.before + re.$1;
        this.endTag = this.endTag.replace(/(\n*$)/, "");
        this.after = this.after + re.$1;
        if (this.before) {
            regexText = replacementText = "";
            while (nLinesBefore--) {
                regexText += "\\n?";
                replacementText += "\n";
            }
            if (findExtraNewlines) {
                regexText = "\\n*";
            }
            this.before = this.before.replace(new re(regexText + "$", ""), replacementText);
        }
        if (this.after) {
            regexText = replacementText = "";
            while (nLinesAfter--) {
                regexText += "\\n?";
                replacementText += "\n";
            }
            if (findExtraNewlines) {
                regexText = "\\n*";
            }
            this.after = this.after.replace(new re(regexText, ""), replacementText);
        }
    };
    function PanelCollection(idButton, idPreview, idInput, postfix) {
        this.buttonBar = doc.getElementById(idButton + postfix);
        this.preview = doc.getElementById(idPreview + postfix);
        this.input = doc.getElementById(idInput + postfix);
    };
    util.isVisible = function (elem) {
        if (window.getComputedStyle) {
            return window.getComputedStyle(elem, null).getPropertyValue("display") !== "none";
        }
        else if (elem.currentStyle) {
            return elem.currentStyle["display"] !== "none";
        }
    };
    util.addEvent = function (elem, event, listener) {
        if (elem.attachEvent) {
            elem.attachEvent("on" + event, listener);
        }
        else {
            elem.addEventListener(event, listener, false);
        }
    };
    util.removeEvent = function (elem, event, listener) {
        if (elem.detachEvent) {
            elem.detachEvent("on" + event, listener);
        }
        else {
            elem.removeEventListener(event, listener, false);
        }
    };
    util.fixEolChars = function (text) {
        text = text.replace(/\r\n/g, "\n");
        text = text.replace(/\r/g, "\n");
        return text;
    };
    util.extendRegExp = function (regex, pre, post) {
        if (pre === null || pre === undefined) {
            pre = "";
        }
        if (post === null || post === undefined) {
            post = "";
        }
        var pattern = regex.toString();
        var flags;
        pattern = pattern.replace(/\/([gim]*)$/, function (wholeMatch, flagsPart) {
            flags = flagsPart;
            return"";
        });
        pattern = pattern.replace(/(^\/|\/$)/g, "");
        pattern = pre + pattern + post;
        return new re(pattern, flags);
    }
    position.getTop = function (elem, isInner) {
        var result = elem.offsetTop;
        if (!isInner) {
            while (elem = elem.offsetParent) {
                result += elem.offsetTop;
            }
        }
        return result;
    };
    position.getHeight = function (elem) {
        return elem.offsetHeight || elem.scrollHeight;
    };
    position.getWidth = function (elem) {
        return elem.offsetWidth || elem.scrollWidth;
    };
    position.getPageSize = function () {
        var scrollWidth, scrollHeight;
        var innerWidth, innerHeight;
        if (self.innerHeight && self.scrollMaxY) {
            scrollWidth = doc.body.scrollWidth;
            scrollHeight = self.innerHeight + self.scrollMaxY;
        }
        else if (doc.body.scrollHeight > doc.body.offsetHeight) {
            scrollWidth = doc.body.scrollWidth;
            scrollHeight = doc.body.scrollHeight;
        }
        else {
            scrollWidth = doc.body.offsetWidth;
            scrollHeight = doc.body.offsetHeight;
        }
        if (self.innerHeight) {
            innerWidth = self.innerWidth;
            innerHeight = self.innerHeight;
        }
        else if (doc.documentElement && doc.documentElement.clientHeight) {
            innerWidth = doc.documentElement.clientWidth;
            innerHeight = doc.documentElement.clientHeight;
        }
        else if (doc.body) {
            innerWidth = doc.body.clientWidth;
            innerHeight = doc.body.clientHeight;
        }
        var maxWidth = Math.max(scrollWidth, innerWidth);
        var maxHeight = Math.max(scrollHeight, innerHeight);
        return[maxWidth, maxHeight, innerWidth, innerHeight];
    };
    function UndoManager(callback, panels) {
        var undoObj = this;
        var undoStack = [];
        var stackPtr = 0;
        var mode = "none";
        var lastState;
        var timer;
        var inputStateObj;
        var setMode = function (newMode, noSave) {
            if (mode != newMode) {
                mode = newMode;
                if (!noSave) {
                    saveState();
                }
            }
            if (!uaSniffed.isIE || mode != "moving") {
                timer = setTimeout(refreshState, 1);
            }
            else {
                inputStateObj = null;
            }
        };
        var refreshState = function (isInitialState) {
            inputStateObj = new TextareaState(panels, isInitialState);
            timer = undefined;
        };
        this.setCommandMode = function () {
            mode = "command";
            saveState();
            timer = setTimeout(refreshState, 0);
        };
        this.canUndo = function () {
            return stackPtr > 1;
        };
        this.canRedo = function () {
            if (undoStack[stackPtr + 1]) {
                return true;
            }
            return false;
        };
        this.undo = function () {
            if (undoObj.canUndo()) {
                if (lastState) {
                    lastState.restore();
                    lastState = null;
                }
                else {
                    undoStack[stackPtr] = new TextareaState(panels);
                    undoStack[--stackPtr].restore();
                    if (callback) {
                        callback();
                    }
                }
            }
            mode = "none";
            panels.input.focus();
            refreshState();
        };
        this.redo = function () {
            if (undoObj.canRedo()) {
                undoStack[++stackPtr].restore();
                if (callback) {
                    callback();
                }
            }
            mode = "none";
            panels.input.focus();
            refreshState();
        };
        var saveState = function () {
            var currState = inputStateObj || new TextareaState(panels);
            if (!currState) {
                return false;
            }
            if (mode == "moving") {
                if (!lastState) {
                    lastState = currState;
                }
                return;
            }
            if (lastState) {
                if (undoStack[stackPtr - 1].text != lastState.text) {
                    undoStack[stackPtr++] = lastState;
                }
                lastState = null;
            }
            undoStack[stackPtr++] = currState;
            undoStack[stackPtr + 1] = null;
            if (callback) {
                callback();
            }
        };
        var handleCtrlYZ = function (event) {
            var handled = false;
            if (event.ctrlKey || event.metaKey) {
                var keyCode = event.charCode || event.keyCode;
                var keyCodeChar = String.fromCharCode(keyCode);
                switch (keyCodeChar) {
                    case"y":
                        undoObj.redo();
                        handled = true;
                        break;
                    case"z":
                        if (!event.shiftKey) {
                            undoObj.undo();
                        }
                        else {
                            undoObj.redo();
                        }
                        handled = true;
                        break;
                }
            }
            if (handled) {
                if (event.preventDefault) {
                    event.preventDefault();
                }
                if (window.event) {
                    window.event.returnValue = false;
                }
                return;
            }
        };
        var handleModeChange = function (event) {
            if (!event.ctrlKey && !event.metaKey) {
                var keyCode = event.keyCode;
                if ((keyCode >= 33 && keyCode <= 40) || (keyCode >= 63232 && keyCode <= 63235)) {
                    setMode("moving");
                }
                else if (keyCode == 8 || keyCode == 46 || keyCode == 127) {
                    setMode("deleting");
                }
                else if (keyCode == 13) {
                    setMode("newlines");
                }
                else if (keyCode == 27) {
                    setMode("escape");
                }
                else if ((keyCode < 16 || keyCode > 20) && keyCode != 91) {
                    setMode("typing");
                }
            }
        };
        var setEventHandlers = function () {
            util.addEvent(panels.input, "keypress", function (event) {
                if ((event.ctrlKey || event.metaKey) && (event.keyCode == 89 || event.keyCode == 90)) {
                    event.preventDefault();
                }
            });
            var handlePaste = function () {
                if (uaSniffed.isIE || (inputStateObj && inputStateObj.text != panels.input.value)) {
                    if (timer == undefined) {
                        mode = "paste";
                        saveState();
                        refreshState();
                    }
                }
            };
            util.addEvent(panels.input, "keydown", handleCtrlYZ);
            util.addEvent(panels.input, "keydown", handleModeChange);
            util.addEvent(panels.input, "mousedown", function () {
                setMode("moving");
            });
            panels.input.onpaste = handlePaste;
            panels.input.ondrop = handlePaste;
        };
        var init = function () {
            setEventHandlers();
            refreshState(true);
            saveState();
        };
        init();
    }

    function TextareaState(panels, isInitialState) {
        var stateObj = this;
        var inputArea = panels.input;
        this.init = function () {
            if (!util.isVisible(inputArea)) {
                return;
            }
            if (!isInitialState && doc.activeElement && doc.activeElement !== inputArea) {
                return;
            }
            this.setInputAreaSelectionStartEnd();
            this.scrollTop = inputArea.scrollTop;
            if (!this.text && inputArea.selectionStart || inputArea.selectionStart === 0) {
                this.text = inputArea.value;
            }
        }
        this.setInputAreaSelection = function () {
            if (!util.isVisible(inputArea)) {
                return;
            }
            if (inputArea.selectionStart !== undefined && !uaSniffed.isOpera) {
                inputArea.focus();
                inputArea.selectionStart = stateObj.start;
                inputArea.selectionEnd = stateObj.end;
                inputArea.scrollTop = stateObj.scrollTop;
            }
            else if (doc.selection) {
                if (doc.activeElement && doc.activeElement !== inputArea) {
                    return;
                }
                inputArea.focus();
                var range = inputArea.createTextRange();
                range.moveStart("character", -inputArea.value.length);
                range.moveEnd("character", -inputArea.value.length);
                range.moveEnd("character", stateObj.end);
                range.moveStart("character", stateObj.start);
                range.select();
            }
        };
        this.setInputAreaSelectionStartEnd = function () {
            if (!panels.ieCachedRange && (inputArea.selectionStart || inputArea.selectionStart === 0)) {
                stateObj.start = inputArea.selectionStart;
                stateObj.end = inputArea.selectionEnd;
            }
            else if (doc.selection) {
                stateObj.text = util.fixEolChars(inputArea.value);
                var range = panels.ieCachedRange || doc.selection.createRange();
                var fixedRange = util.fixEolChars(range.text);
                var marker = "\x07";
                var markedRange = marker + fixedRange + marker;
                range.text = markedRange;
                var inputText = util.fixEolChars(inputArea.value);
                range.moveStart("character", -markedRange.length);
                range.text = fixedRange;
                stateObj.start = inputText.indexOf(marker);
                stateObj.end = inputText.lastIndexOf(marker) - marker.length;
                var len = stateObj.text.length - util.fixEolChars(inputArea.value).length;
                if (len) {
                    range.moveStart("character", -fixedRange.length);
                    while (len--) {
                        fixedRange += "\n";
                        stateObj.end += 1;
                    }
                    range.text = fixedRange;
                }
                if (panels.ieCachedRange)
                    stateObj.scrollTop = panels.ieCachedScrollTop;
                panels.ieCachedRange = null;
                this.setInputAreaSelection();
            }
        };
        this.restore = function () {
            if (stateObj.text != undefined && stateObj.text != inputArea.value) {
                inputArea.value = stateObj.text;
            }
            this.setInputAreaSelection();
            inputArea.scrollTop = stateObj.scrollTop;
        };
        this.getChunks = function () {
            var chunk = new Chunks();
            chunk.before = util.fixEolChars(stateObj.text.substring(0, stateObj.start));
            chunk.startTag = "";
            chunk.selection = util.fixEolChars(stateObj.text.substring(stateObj.start, stateObj.end));
            chunk.endTag = "";
            chunk.after = util.fixEolChars(stateObj.text.substring(stateObj.end));
            chunk.scrollTop = stateObj.scrollTop;
            return chunk;
        };
        this.setChunks = function (chunk) {
            chunk.before = chunk.before + chunk.startTag;
            chunk.after = chunk.endTag + chunk.after;
            this.start = chunk.before.length;
            this.end = chunk.before.length + chunk.selection.length;
            this.text = chunk.before + chunk.selection + chunk.after;
            this.scrollTop = chunk.scrollTop;
        };
        this.init();
    };
    function PreviewManager(converter, panels, previewRefreshCallback) {
        var managerObj = this;
        var timeout;
        var elapsedTime;
        var oldInputText;
        var maxDelay = 3000;
        var startType = "delayed";
        var setupEvents = function (inputElem, listener) {
            util.addEvent(inputElem, "input", listener);
            inputElem.onpaste = listener;
            inputElem.ondrop = listener;
            util.addEvent(inputElem, "keypress", listener);
            util.addEvent(inputElem, "keydown", listener);
        };
        var getDocScrollTop = function () {
            var result = 0;
            if (window.innerHeight) {
                result = window.pageYOffset;
            }
            else if (doc.documentElement && doc.documentElement.scrollTop) {
                result = doc.documentElement.scrollTop;
            }
            else if (doc.body) {
                result = doc.body.scrollTop;
            }
            return result;
        };
        var makePreviewHtml = function () {
            if (!panels.preview)
                return;
            var text = panels.input.value;
            if (text && text == oldInputText) {
                return;
            }
            else {
                oldInputText = text;
            }
            var prevTime = new Date().getTime();
            text = converter.makeHtml(text);
            var currTime = new Date().getTime();
            elapsedTime = currTime - prevTime;
            pushPreviewHtml(text);
        };
        var applyTimeout = function () {
            if (timeout) {
                clearTimeout(timeout);
                timeout = undefined;
            }
            if (startType !== "manual") {
                var delay = 0;
                if (startType === "delayed") {
                    delay = elapsedTime;
                }
                if (delay > maxDelay) {
                    delay = maxDelay;
                }
                timeout = setTimeout(makePreviewHtml, delay);
            }
        };
        var getScaleFactor = function (panel) {
            if (panel.scrollHeight <= panel.clientHeight) {
                return 1;
            }
            return panel.scrollTop / (panel.scrollHeight - panel.clientHeight);
        };
        var setPanelScrollTops = function () {
            if (panels.preview) {
                panels.preview.scrollTop = (panels.preview.scrollHeight - panels.preview.clientHeight) * getScaleFactor(panels.preview);
            }
        };
        this.refresh = function (requiresRefresh) {
            if (requiresRefresh) {
                oldInputText = "";
                makePreviewHtml();
            }
            else {
                applyTimeout();
            }
        };
        this.processingTime = function () {
            return elapsedTime;
        };
        var isFirstTimeFilled = true;
        var ieSafePreviewSet = function (text) {
            var preview = panels.preview;
            var parent = preview.parentNode;
            var sibling = preview.nextSibling;
            parent.removeChild(preview);
            preview.innerHTML = text;
            if (!sibling)
                parent.appendChild(preview); else
                parent.insertBefore(preview, sibling);
        }
        var nonSuckyBrowserPreviewSet = function (text) {
            panels.preview.innerHTML = text;
        }
        var previewSetter;
        var previewSet = function (text) {
            if (previewSetter)
                return previewSetter(text);
            try {
                nonSuckyBrowserPreviewSet(text);
                previewSetter = nonSuckyBrowserPreviewSet;
            } catch (e) {
                previewSetter = ieSafePreviewSet;
                previewSetter(text);
            }
        };
        var pushPreviewHtml = function (text) {
            var emptyTop = position.getTop(panels.input) - getDocScrollTop();
            if (panels.preview) {
                previewSet(text);
                previewRefreshCallback();
            }
            setPanelScrollTops();
            if (isFirstTimeFilled) {
                isFirstTimeFilled = false;
                return;
            }
            var fullTop = position.getTop(panels.input) - getDocScrollTop();
            if (uaSniffed.isIE) {
                setTimeout(function () {
                    window.scrollBy(0, fullTop - emptyTop);
                }, 0);
            }
            else {
                window.scrollBy(0, fullTop - emptyTop);
            }
        };
        var init = function () {
            setupEvents(panels.input, applyTimeout);
            makePreviewHtml();
            if (panels.preview) {
                panels.preview.scrollTop = 0;
            }
        };
        init();
    };
    ui.createBackground = function () {
        var background = doc.createElement("div"), style = background.style;
        background.className = "wmd-prompt-background";
        style.position = "absolute";
        style.top = "0";
        style.zIndex = "1000";
        if (uaSniffed.isIE) {
            style.filter = "alpha(opacity=50)";
        }
        else {
            style.opacity = "0.5";
        }
        var pageSize = position.getPageSize();
        style.height = pageSize[1] + "px";
        if (uaSniffed.isIE) {
            style.left = doc.documentElement.scrollLeft;
            style.width = doc.documentElement.clientWidth;
        }
        else {
            style.left = "0";
            style.width = "100%";
        }
        doc.body.appendChild(background);
        return background;
    };
    ui.prompt = function (text, defaultInputText, callback) {
        var dialog;
        var input;
        if (defaultInputText === undefined) {
            defaultInputText = "";
        }
        var checkEscape = function (key) {
            var code = (key.charCode || key.keyCode);
            if (code === 27) {
                close(true);
            }
        };
        var close = function (isCancel) {
            util.removeEvent(doc.body, "keydown", checkEscape);
            var text = input.value;
            if (isCancel) {
                text = null;
            }
            else {
                text = text.replace(/^http:\/\/(https?|ftp):\/\//, '$1://');
                if (!/^(?:https?|ftp):\/\//.test(text))
                    text = 'http://' + text;
            }
            dialog.parentNode.removeChild(dialog);
            callback(text);
            return false;
        };
        var createDialog = function () {
            dialog = doc.createElement("div");
            dialog.className = "wmd-prompt-dialog";
            dialog.style.padding = "10px;";
            dialog.style.position = "fixed";
            dialog.style.width = "400px";
            dialog.style.zIndex = "1001";
            var question = doc.createElement("div");
            question.innerHTML = text;
            question.style.padding = "5px";
            dialog.appendChild(question);
            var form = doc.createElement("form"), style = form.style;
            form.onsubmit = function () {
                return close(false);
            };
            style.padding = "0";
            style.margin = "0";
            style.cssFloat = "left";
            style.width = "100%";
            style.textAlign = "center";
            style.position = "relative";
            dialog.appendChild(form);
            input = doc.createElement("input");
            input.type = "text";
            input.value = defaultInputText;
            style = input.style;
            style.display = "block";
            style.width = "80%";
            style.marginLeft = style.marginRight = "auto";
            form.appendChild(input);
            var okButton = doc.createElement("input");
            okButton.type = "button";
            okButton.onclick = function () {
                return close(false);
            };
            okButton.value = "OK";
            style = okButton.style;
            style.margin = "10px";
            style.display = "inline";
            style.width = "7em";
            var cancelButton = doc.createElement("input");
            cancelButton.type = "button";
            cancelButton.onclick = function () {
                return close(true);
            };
            cancelButton.value = "Cancel";
            style = cancelButton.style;
            style.margin = "10px";
            style.display = "inline";
            style.width = "7em";
            form.appendChild(okButton);
            form.appendChild(cancelButton);
            util.addEvent(doc.body, "keydown", checkEscape);
            dialog.style.top = "50%";
            dialog.style.left = "50%";
            dialog.style.display = "block";
            if (uaSniffed.isIE_5or6) {
                dialog.style.position = "absolute";
                dialog.style.top = doc.documentElement.scrollTop + 200 + "px";
                dialog.style.left = "50%";
            }
            doc.body.appendChild(dialog);
            dialog.style.marginTop = -(position.getHeight(dialog) / 2) + "px";
            dialog.style.marginLeft = -(position.getWidth(dialog) / 2) + "px";
        };
        setTimeout(function () {
            createDialog();
            var defTextLen = defaultInputText.length;
            if (input.selectionStart !== undefined) {
                input.selectionStart = 0;
                input.selectionEnd = defTextLen;
            }
            else if (input.createTextRange) {
                var range = input.createTextRange();
                range.collapse(false);
                range.moveStart("character", -defTextLen);
                range.moveEnd("character", defTextLen);
                range.select();
            }
            input.focus();
        }, 0);
    };
    function UIManager(postfix, panels, undoManager, previewManager, commandManager, helpOptions) {
        var inputBox = panels.input, buttons = {};
        makeSpritedButtonRow();
        var keyEvent = "keydown";
        if (uaSniffed.isOpera) {
            keyEvent = "keypress";
        }
        util.addEvent(inputBox, keyEvent, function (key) {
            if ((key.ctrlKey || key.metaKey) && !key.altKey && !key.shiftKey) {
                var keyCode = key.charCode || key.keyCode;
                var keyCodeStr = String.fromCharCode(keyCode).toLowerCase();
                switch (keyCodeStr) {
                    case"b":
                        doClick(buttons.bold);
                        break;
                    case"i":
                        doClick(buttons.italic);
                        break;
                    case"l":
                        doClick(buttons.link);
                        break;
                    case"q":
                        doClick(buttons.quote);
                        break;
                    case"k":
                        doClick(buttons.code);
                        break;
                    case"g":
                        doClick(buttons.image);
                        break;
                    case"o":
                        doClick(buttons.olist);
                        break;
                    case"u":
                        doClick(buttons.ulist);
                        break;
                    case"h":
                        doClick(buttons.heading);
                        break;
                    case"r":
                        doClick(buttons.hr);
                        break;
                    case"y":
                        doClick(buttons.redo);
                        break;
                    case"z":
                        if (key.shiftKey) {
                            doClick(buttons.redo);
                        }
                        else {
                            doClick(buttons.undo);
                        }
                        break;
                    default:
                        return;
                }
                if (key.preventDefault) {
                    key.preventDefault();
                }
                if (window.event) {
                    window.event.returnValue = false;
                }
            }
        });
        util.addEvent(inputBox, "keyup", function (key) {
            if (key.shiftKey && !key.ctrlKey && !key.metaKey) {
                var keyCode = key.charCode || key.keyCode;
                if (keyCode === 13) {
                    var fakeButton = {};
                    fakeButton.textOp = bindCommand("doAutoindent");
                    doClick(fakeButton);
                }
            }
        });
        if (uaSniffed.isIE) {
            util.addEvent(inputBox, "keydown", function (key) {
                var code = key.keyCode;
                if (code === 27) {
                    return false;
                }
            });
        }
        function doClick(button) {
            inputBox.focus();
            if (button.textOp) {
                if (undoManager) {
                    undoManager.setCommandMode();
                }
                var state = new TextareaState(panels);
                if (!state) {
                    return;
                }
                var chunks = state.getChunks();
                var fixupInputArea = function () {
                    inputBox.focus();
                    if (chunks) {
                        state.setChunks(chunks);
                    }
                    state.restore();
                    previewManager.refresh();
                };
                var noCleanup = button.textOp(chunks, fixupInputArea);
                if (!noCleanup) {
                    fixupInputArea();
                }
            }
            if (button.execute) {
                button.execute(undoManager);
            }
        };
        function setupButton(button, isEnabled) {
            var normalYShift = "0px";
            var disabledYShift = "-20px";
            var highlightYShift = "-40px";
            var image = button.getElementsByTagName("span")[0];
            if (isEnabled) {
                image.style.backgroundPosition = button.XShift + " " + normalYShift;
                button.onmouseover = function () {
                    image.style.backgroundPosition = this.XShift + " " + highlightYShift;
                };
                button.onmouseout = function () {
                    image.style.backgroundPosition = this.XShift + " " + normalYShift;
                };
                if (uaSniffed.isIE) {
                    button.onmousedown = function () {
                        if (doc.activeElement && doc.activeElement !== panels.input) {
                            return;
                        }
                        panels.ieCachedRange = document.selection.createRange();
                        panels.ieCachedScrollTop = panels.input.scrollTop;
                    };
                }
                if (!button.isHelp) {
                    button.onclick = function () {
                        if (this.onmouseout) {
                            this.onmouseout();
                        }
                        doClick(this);
                        return false;
                    }
                }
            }
            else {
                image.style.backgroundPosition = button.XShift + " " + disabledYShift;
                button.onmouseover = button.onmouseout = button.onclick = function () {
                };
            }
        }

        function bindCommand(method) {
            if (typeof method === "string")
                method = commandManager[method];
            return function () {
                method.apply(commandManager, arguments);
            }
        }

        function makeSpritedButtonRow() {
            var buttonBar = panels.buttonBar;
            var normalYShift = "0px";
            var disabledYShift = "-20px";
            var highlightYShift = "-40px";
            var buttonRow = document.createElement("ul");
            buttonRow.id = "wmd-button-row" + postfix;
            buttonRow.className = 'wmd-button-row';
            buttonRow = buttonBar.appendChild(buttonRow);
            var xPosition = 0;
            var makeButton = function (id, title, XShift, textOp) {
                var button = document.createElement("li");
                button.className = "wmd-button";
                button.style.left = xPosition + "px";
                xPosition += 25;
                var buttonImage = document.createElement("span");
                button.id = id + postfix;
                button.appendChild(buttonImage);
                button.title = title;
                button.XShift = XShift;
                if (textOp)
                    button.textOp = textOp;
                setupButton(button, true);
                buttonRow.appendChild(button);
                return button;
            };
            var makeSpacer = function (num) {
                var spacer = document.createElement("li");
                spacer.className = "wmd-spacer wmd-spacer" + num;
                spacer.id = "wmd-spacer" + num + postfix;
                buttonRow.appendChild(spacer);
                xPosition += 25;
            }
            buttons.bold = makeButton("wmd-bold-button", "Strong <strong> Ctrl+B", "0px", bindCommand("doBold"));
            buttons.italic = makeButton("wmd-italic-button", "Emphasis <em> Ctrl+I", "-20px", bindCommand("doItalic"));
            makeSpacer(1);
            buttons.link = makeButton("wmd-link-button", "Hyperlink <a> Ctrl+L", "-40px", bindCommand(function (chunk, postProcessing) {
                return this.doLinkOrImage(chunk, postProcessing, false);
            }));
            buttons.quote = makeButton("wmd-quote-button", "Blockquote <blockquote> Ctrl+Q", "-60px", bindCommand("doBlockquote"));
            buttons.code = makeButton("wmd-code-button", "Code Sample <pre><code> Ctrl+K", "-80px", bindCommand("doCode"));
            buttons.image = makeButton("wmd-image-button", "Image <img> Ctrl+G", "-100px", bindCommand(function (chunk, postProcessing) {
                return this.doLinkOrImage(chunk, postProcessing, true);
            }));
            makeSpacer(2);
            buttons.olist = makeButton("wmd-olist-button", "Numbered List <ol> Ctrl+O", "-120px", bindCommand(function (chunk, postProcessing) {
                this.doList(chunk, postProcessing, true);
            }));
            buttons.ulist = makeButton("wmd-ulist-button", "Bulleted List <ul> Ctrl+U", "-140px", bindCommand(function (chunk, postProcessing) {
                this.doList(chunk, postProcessing, false);
            }));
            buttons.heading = makeButton("wmd-heading-button", "Heading <h1>/<h2> Ctrl+H", "-160px", bindCommand("doHeading"));
            buttons.hr = makeButton("wmd-hr-button", "Horizontal Rule <hr> Ctrl+R", "-180px", bindCommand("doHorizontalRule"));
            makeSpacer(3);
            buttons.undo = makeButton("wmd-undo-button", "Undo - Ctrl+Z", "-200px", null);
            buttons.undo.execute = function (manager) {
                if (manager)manager.undo();
            };
            var redoTitle = /win/.test(nav.platform.toLowerCase()) ? "Redo - Ctrl+Y" : "Redo - Ctrl+Shift+Z";
            buttons.redo = makeButton("wmd-redo-button", redoTitle, "-220px", null);
            buttons.redo.execute = function (manager) {
                if (manager)manager.redo();
            };
            if (helpOptions) {
                var helpButton = document.createElement("li");
                var helpButtonImage = document.createElement("span");
                helpButton.appendChild(helpButtonImage);
                helpButton.className = "wmd-button wmd-help-button";
                helpButton.id = "wmd-help-button" + postfix;
                helpButton.XShift = "-240px";
                helpButton.isHelp = true;
                helpButton.style.right = "0px";
                helpButton.title = helpOptions.title || defaultHelpHoverTitle;
                helpButton.onclick = helpOptions.handler;
                setupButton(helpButton, true);
                buttonRow.appendChild(helpButton);
                buttons.help = helpButton;
            }
            setUndoRedoButtonStates();
        }

        function setUndoRedoButtonStates() {
            if (undoManager) {
                setupButton(buttons.undo, undoManager.canUndo());
                setupButton(buttons.redo, undoManager.canRedo());
            }
        };
        this.setUndoRedoButtonStates = setUndoRedoButtonStates;
    }

    function CommandManager(pluginHooks) {
        this.hooks = pluginHooks;
    }

    var commandProto = CommandManager.prototype;
    commandProto.prefixes = "(?:\\s{4,}|\\s*>|\\s*-\\s+|\\s*\\d+\\.|=|\\+|-|_|\\*|#|\\s*\\[[^\n]]+\\]:)";
    commandProto.unwrap = function (chunk) {
        var txt = new re("([^\\n])\\n(?!(\\n|" + this.prefixes + "))", "g");
        chunk.selection = chunk.selection.replace(txt, "$1 $2");
    };
    commandProto.wrap = function (chunk, len) {
        this.unwrap(chunk);
        var regex = new re("(.{1," + len + "})( +|$\\n?)", "gm"), that = this;
        chunk.selection = chunk.selection.replace(regex, function (line, marked) {
            if (new re("^" + that.prefixes, "").test(line)) {
                return line;
            }
            return marked + "\n";
        });
        chunk.selection = chunk.selection.replace(/\s+$/, "");
    };
    commandProto.doBold = function (chunk, postProcessing) {
        return this.doBorI(chunk, postProcessing, 2, "strong text");
    };
    commandProto.doItalic = function (chunk, postProcessing) {
        return this.doBorI(chunk, postProcessing, 1, "emphasized text");
    };
    commandProto.doBorI = function (chunk, postProcessing, nStars, insertText) {
        chunk.trimWhitespace();
        chunk.selection = chunk.selection.replace(/\n{2,}/g, "\n");
        var starsBefore = /(\**$)/.exec(chunk.before)[0];
        var starsAfter = /(^\**)/.exec(chunk.after)[0];
        var prevStars = Math.min(starsBefore.length, starsAfter.length);
        if ((prevStars >= nStars) && (prevStars != 2 || nStars != 1)) {
            chunk.before = chunk.before.replace(re("[*]{" + nStars + "}$", ""), "");
            chunk.after = chunk.after.replace(re("^[*]{" + nStars + "}", ""), "");
        }
        else if (!chunk.selection && starsAfter) {
            chunk.after = chunk.after.replace(/^([*_]*)/, "");
            chunk.before = chunk.before.replace(/(\s?)$/, "");
            var whitespace = re.$1;
            chunk.before = chunk.before + starsAfter + whitespace;
        }
        else {
            if (!chunk.selection && !starsAfter) {
                chunk.selection = insertText;
            }
            var markup = nStars <= 1 ? "*" : "**";
            chunk.before = chunk.before + markup;
            chunk.after = markup + chunk.after;
        }
        return;
    };
    commandProto.stripLinkDefs = function (text, defsToAdd) {
        text = text.replace(/^[ ]{0,3}\[(\d+)\]:[ \t]*\n?[ \t]*<?(\S+?)>?[ \t]*\n?[ \t]*(?:(\n*)["(](.+?)[")][ \t]*)?(?:\n+|$)/gm, function (totalMatch, id, link, newlines, title) {
            defsToAdd[id] = totalMatch.replace(/\s*$/, "");
            if (newlines) {
                defsToAdd[id] = totalMatch.replace(/["(](.+?)[")]$/, "");
                return newlines + title;
            }
            return"";
        });
        return text;
    };
    commandProto.addLinkDef = function (chunk, linkDef) {
        var refNumber = 0;
        var defsToAdd = {};
        chunk.before = this.stripLinkDefs(chunk.before, defsToAdd);
        chunk.selection = this.stripLinkDefs(chunk.selection, defsToAdd);
        chunk.after = this.stripLinkDefs(chunk.after, defsToAdd);
        var defs = "";
        var regex = /(\[)((?:\[[^\]]*\]|[^\[\]])*)(\][ ]?(?:\n[ ]*)?\[)(\d+)(\])/g;
        var addDefNumber = function (def) {
            refNumber++;
            def = def.replace(/^[ ]{0,3}\[(\d+)\]:/, "  [" + refNumber + "]:");
            defs += "\n" + def;
        };
        var getLink = function (wholeMatch, before, inner, afterInner, id, end) {
            inner = inner.replace(regex, getLink);
            if (defsToAdd[id]) {
                addDefNumber(defsToAdd[id]);
                return before + inner + afterInner + refNumber + end;
            }
            return wholeMatch;
        };
        chunk.before = chunk.before.replace(regex, getLink);
        if (linkDef) {
            addDefNumber(linkDef);
        }
        else {
            chunk.selection = chunk.selection.replace(regex, getLink);
        }
        var refOut = refNumber;
        chunk.after = chunk.after.replace(regex, getLink);
        if (chunk.after) {
            chunk.after = chunk.after.replace(/\n*$/, "");
        }
        if (!chunk.after) {
            chunk.selection = chunk.selection.replace(/\n*$/, "");
        }
        chunk.after += "\n\n" + defs;
        return refOut;
    };
    function properlyEncoded(linkdef) {
        return linkdef.replace(/^\s*(.*?)(?:\s+"(.+)")?\s*$/, function (wholematch, link, title) {
            link = link.replace(/\?.*$/, function (querypart) {
                return querypart.replace(/\+/g, " ");
            });
            link = decodeURIComponent(link);
            link = encodeURI(link).replace(/'/g, '%27').replace(/\(/g, '%28').replace(/\)/g, '%29');
            link = link.replace(/\?.*$/, function (querypart) {
                return querypart.replace(/\+/g, "%2b");
            });
            if (title) {
                title = title.trim ? title.trim() : title.replace(/^\s*/, "").replace(/\s*$/, "");
                title = $.trim(title).replace(/"/g, "quot;").replace(/\(/g, "&#40;").replace(/\)/g, "&#41;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
            }
            return title ? link + ' "' + title + '"' : link;
        });
    }

    commandProto.doLinkOrImage = function (chunk, postProcessing, isImage) {
        chunk.trimWhitespace();
        chunk.findTags(/\s*!?\[/, /\][ ]?(?:\n[ ]*)?(\[.*?\])?/);
        var background;
        if (chunk.endTag.length > 1 && chunk.startTag.length > 0) {
            chunk.startTag = chunk.startTag.replace(/!?\[/, "");
            chunk.endTag = "";
            this.addLinkDef(chunk, null);
        }
        else {
            chunk.selection = chunk.startTag + chunk.selection + chunk.endTag;
            chunk.startTag = chunk.endTag = "";
            if (/\n\n/.test(chunk.selection)) {
                this.addLinkDef(chunk, null);
                return;
            }
            var that = this;
            var linkEnteredCallback = function (link) {
                background.parentNode.removeChild(background);
                if (link !== null) {
                    chunk.selection = (" " + chunk.selection).replace(/([^\\](?:\\\\)*)(?=[[\]])/g, "$1\\").substr(1);
                    var linkDef = " [999]: " + properlyEncoded(link);
                    var num = that.addLinkDef(chunk, linkDef);
                    chunk.startTag = isImage ? "![" : "[";
                    chunk.endTag = "][" + num + "]";
                    if (!chunk.selection) {
                        if (isImage) {
                            chunk.selection = "enter image description here";
                        }
                        else {
                            chunk.selection = "enter link description here";
                        }
                    }
                }
                postProcessing();
            };
            background = ui.createBackground();
            if (isImage) {
                if (!this.hooks.insertImageDialog(linkEnteredCallback))
                    ui.prompt(imageDialogText, imageDefaultText, linkEnteredCallback);
            }
            else {
                ui.prompt(linkDialogText, linkDefaultText, linkEnteredCallback);
            }
            return true;
        }
    };
    commandProto.doAutoindent = function (chunk, postProcessing) {
        var commandMgr = this, fakeSelection = false;
        chunk.before = chunk.before.replace(/(\n|^)[ ]{0,3}([*+-]|\d+[.])[ \t]*\n$/, "\n\n");
        chunk.before = chunk.before.replace(/(\n|^)[ ]{0,3}>[ \t]*\n$/, "\n\n");
        chunk.before = chunk.before.replace(/(\n|^)[ \t]+\n$/, "\n\n");
        if (!chunk.selection && !/^[ \t]*(?:\n|$)/.test(chunk.after)) {
            chunk.after = chunk.after.replace(/^[^\n]*/, function (wholeMatch) {
                chunk.selection = wholeMatch;
                return"";
            });
            fakeSelection = true;
        }
        if (/(\n|^)[ ]{0,3}([*+-]|\d+[.])[ \t]+.*\n$/.test(chunk.before)) {
            if (commandMgr.doList) {
                commandMgr.doList(chunk);
            }
        }
        if (/(\n|^)[ ]{0,3}>[ \t]+.*\n$/.test(chunk.before)) {
            if (commandMgr.doBlockquote) {
                commandMgr.doBlockquote(chunk);
            }
        }
        if (/(\n|^)(\t|[ ]{4,}).*\n$/.test(chunk.before)) {
            if (commandMgr.doCode) {
                commandMgr.doCode(chunk);
            }
        }
        if (fakeSelection) {
            chunk.after = chunk.selection + chunk.after;
            chunk.selection = "";
        }
    };
    commandProto.doBlockquote = function (chunk, postProcessing) {
        chunk.selection = chunk.selection.replace(/^(\n*)([^\r]+?)(\n*)$/, function (totalMatch, newlinesBefore, text, newlinesAfter) {
            chunk.before += newlinesBefore;
            chunk.after = newlinesAfter + chunk.after;
            return text;
        });
        chunk.before = chunk.before.replace(/(>[ \t]*)$/, function (totalMatch, blankLine) {
            chunk.selection = blankLine + chunk.selection;
            return"";
        });
        chunk.selection = chunk.selection.replace(/^(\s|>)+$/, "");
        chunk.selection = chunk.selection || "Blockquote";
        var match = "", leftOver = "", line;
        if (chunk.before) {
            var lines = chunk.before.replace(/\n$/, "").split("\n");
            var inChain = false;
            for (var i = 0; i < lines.length; i++) {
                var good = false;
                line = lines[i];
                inChain = inChain && line.length > 0;
                if (/^>/.test(line)) {
                    good = true;
                    if (!inChain && line.length > 1)
                        inChain = true;
                } else if (/^[ \t]*$/.test(line)) {
                    good = true;
                } else {
                    good = inChain;
                }
                if (good) {
                    match += line + "\n";
                } else {
                    leftOver += match + line;
                    match = "\n";
                }
            }
            if (!/(^|\n)>/.test(match)) {
                leftOver += match;
                match = "";
            }
        }
        chunk.startTag = match;
        chunk.before = leftOver;
        if (chunk.after) {
            chunk.after = chunk.after.replace(/^\n?/, "\n");
        }
        chunk.after = chunk.after.replace(/^(((\n|^)(\n[ \t]*)*>(.+\n)*.*)+(\n[ \t]*)*)/, function (totalMatch) {
            chunk.endTag = totalMatch;
            return"";
        });
        var replaceBlanksInTags = function (useBracket) {
            var replacement = useBracket ? "> " : "";
            if (chunk.startTag) {
                chunk.startTag = chunk.startTag.replace(/\n((>|\s)*)\n$/, function (totalMatch, markdown) {
                    return"\n" + markdown.replace(/^[ ]{0,3}>?[ \t]*$/gm, replacement) + "\n";
                });
            }
            if (chunk.endTag) {
                chunk.endTag = chunk.endTag.replace(/^\n((>|\s)*)\n/, function (totalMatch, markdown) {
                    return"\n" + markdown.replace(/^[ ]{0,3}>?[ \t]*$/gm, replacement) + "\n";
                });
            }
        };
        if (/^(?![ ]{0,3}>)/m.test(chunk.selection)) {
            this.wrap(chunk, SETTINGS.lineLength - 2);
            chunk.selection = chunk.selection.replace(/^/gm, "> ");
            replaceBlanksInTags(true);
            chunk.skipLines();
        } else {
            chunk.selection = chunk.selection.replace(/^[ ]{0,3}> ?/gm, "");
            this.unwrap(chunk);
            replaceBlanksInTags(false);
            if (!/^(\n|^)[ ]{0,3}>/.test(chunk.selection) && chunk.startTag) {
                chunk.startTag = chunk.startTag.replace(/\n{0,2}$/, "\n\n");
            }
            if (!/(\n|^)[ ]{0,3}>.*$/.test(chunk.selection) && chunk.endTag) {
                chunk.endTag = chunk.endTag.replace(/^\n{0,2}/, "\n\n");
            }
        }
        chunk.selection = this.hooks.postBlockquoteCreation(chunk.selection);
        if (!/\n/.test(chunk.selection)) {
            chunk.selection = chunk.selection.replace(/^(> *)/, function (wholeMatch, blanks) {
                chunk.startTag += blanks;
                return"";
            });
        }
    };
    commandProto.doCode = function (chunk, postProcessing) {
        var hasTextBefore = /\S[ ]*$/.test(chunk.before);
        var hasTextAfter = /^[ ]*\S/.test(chunk.after);
        if ((!hasTextAfter && !hasTextBefore) || /\n/.test(chunk.selection)) {
            chunk.before = chunk.before.replace(/[ ]{4}$/, function (totalMatch) {
                chunk.selection = totalMatch + chunk.selection;
                return"";
            });
            var nLinesBack = 1;
            var nLinesForward = 1;
            if (/(\n|^)(\t|[ ]{4,}).*\n$/.test(chunk.before)) {
                nLinesBack = 0;
            }
            if (/^\n(\t|[ ]{4,})/.test(chunk.after)) {
                nLinesForward = 0;
            }
            chunk.skipLines(nLinesBack, nLinesForward);
            if (!chunk.selection) {
                chunk.startTag = "    ";
                chunk.selection = "enter code here";
            }
            else {
                if (/^[ ]{0,3}\S/m.test(chunk.selection)) {
                    if (/\n/.test(chunk.selection))
                        chunk.selection = chunk.selection.replace(/^/gm, "    "); else
                        chunk.before += "    ";
                }
                else {
                    chunk.selection = chunk.selection.replace(/^[ ]{4}/gm, "");
                }
            }
        }
        else {
            chunk.trimWhitespace();
            chunk.findTags(/`/, /`/);
            if (!chunk.startTag && !chunk.endTag) {
                chunk.startTag = chunk.endTag = "`";
                if (!chunk.selection) {
                    chunk.selection = "enter code here";
                }
            }
            else if (chunk.endTag && !chunk.startTag) {
                chunk.before += chunk.endTag;
                chunk.endTag = "";
            }
            else {
                chunk.startTag = chunk.endTag = "";
            }
        }
    };
    commandProto.doList = function (chunk, postProcessing, isNumberedList) {
        var previousItemsRegex = /(\n|^)(([ ]{0,3}([*+-]|\d+[.])[ \t]+.*)(\n.+|\n{2,}([*+-].*|\d+[.])[ \t]+.*|\n{2,}[ \t]+\S.*)*)\n*$/;
        var nextItemsRegex = /^\n*(([ ]{0,3}([*+-]|\d+[.])[ \t]+.*)(\n.+|\n{2,}([*+-].*|\d+[.])[ \t]+.*|\n{2,}[ \t]+\S.*)*)\n*/;
        var bullet = "-";
        var num = 1;
        var getItemPrefix = function () {
            var prefix;
            if (isNumberedList) {
                prefix = " " + num + ". ";
                num++;
            }
            else {
                prefix = " " + bullet + " ";
            }
            return prefix;
        };
        var getPrefixedItem = function (itemText) {
            if (isNumberedList === undefined) {
                isNumberedList = /^\s*\d/.test(itemText);
            }
            itemText = itemText.replace(/^[ ]{0,3}([*+-]|\d+[.])\s/gm, function (_) {
                return getItemPrefix();
            });
            return itemText;
        };
        chunk.findTags(/(\n|^)*[ ]{0,3}([*+-]|\d+[.])\s+/, null);
        if (chunk.before && !/\n$/.test(chunk.before) && !/^\n/.test(chunk.startTag)) {
            chunk.before += chunk.startTag;
            chunk.startTag = "";
        }
        if (chunk.startTag) {
            var hasDigits = /\d+[.]/.test(chunk.startTag);
            chunk.startTag = "";
            chunk.selection = chunk.selection.replace(/\n[ ]{4}/g, "\n");
            this.unwrap(chunk);
            chunk.skipLines();
            if (hasDigits) {
                chunk.after = chunk.after.replace(nextItemsRegex, getPrefixedItem);
            }
            if (isNumberedList == hasDigits) {
                return;
            }
        }
        var nLinesUp = 1;
        chunk.before = chunk.before.replace(previousItemsRegex, function (itemText) {
            if (/^\s*([*+-])/.test(itemText)) {
                bullet = re.$1;
            }
            nLinesUp = /[^\n]\n\n[^\n]/.test(itemText) ? 1 : 0;
            return getPrefixedItem(itemText);
        });
        if (!chunk.selection) {
            chunk.selection = "List item";
        }
        var prefix = getItemPrefix();
        var nLinesDown = 1;
        chunk.after = chunk.after.replace(nextItemsRegex, function (itemText) {
            nLinesDown = /[^\n]\n\n[^\n]/.test(itemText) ? 1 : 0;
            return getPrefixedItem(itemText);
        });
        chunk.trimWhitespace(true);
        chunk.skipLines(nLinesUp, nLinesDown, true);
        chunk.startTag = prefix;
        var spaces = prefix.replace(/./g, " ");
        this.wrap(chunk, SETTINGS.lineLength - spaces.length);
        chunk.selection = chunk.selection.replace(/\n/g, "\n" + spaces);
    };
    commandProto.doHeading = function (chunk, postProcessing) {
        chunk.selection = chunk.selection.replace(/\s+/g, " ");
        chunk.selection = chunk.selection.replace(/(^\s+|\s+$)/g, "");
        if (!chunk.selection) {
            chunk.startTag = "## ";
            chunk.selection = "Heading";
            chunk.endTag = " ##";
            return;
        }
        var headerLevel = 0;
        chunk.findTags(/#+[ ]*/, /[ ]*#+/);
        if (/#+/.test(chunk.startTag)) {
            headerLevel = re.lastMatch.length;
        }
        chunk.startTag = chunk.endTag = "";
        chunk.findTags(null, /\s?(-+|=+)/);
        if (/=+/.test(chunk.endTag)) {
            headerLevel = 1;
        }
        if (/-+/.test(chunk.endTag)) {
            headerLevel = 2;
        }
        chunk.startTag = chunk.endTag = "";
        chunk.skipLines(1, 1);
        var headerLevelToCreate = headerLevel == 0 ? 2 : headerLevel - 1;
        if (headerLevelToCreate > 0) {
            var headerChar = headerLevelToCreate >= 2 ? "-" : "=";
            var len = chunk.selection.length;
            if (len > SETTINGS.lineLength) {
                len = SETTINGS.lineLength;
            }
            chunk.endTag = "\n";
            while (len--) {
                chunk.endTag += headerChar;
            }
        }
    };
    commandProto.doHorizontalRule = function (chunk, postProcessing) {
        chunk.startTag = "----------\n";
        chunk.selection = "";
        chunk.skipLines(2, 1, true);
    }
})();
(function ($) {
    var scrollElement = 'html, body';
    var active_input = '';
    var COMMENT_SCROLL_TOP_OFFSET = 40;
    var PREVIEW_SCROLL_TOP_OFFSET = 20;
    $.fn.ready(function () {
        var commentform = $('form.js-comments-form');
        if (commentform.length > 0) {
            commentform.find(':input').focus(setActiveInput).mousedown(setActiveInput);
            commentform.submit(onCommentFormSubmit);
            $('.textarea', commentform).on('keypress', function (e) {
                if (e.keyCode == 13) {
                    if (!e.shiftKey) {
                        e.target = commentform;
                        onCommentFormSubmit(e);
                    }
                    ;
                }
                ;
            });
        }
        $('html, body').each(function () {
            var $rootEl = $(this);
            var initScrollTop = $rootEl.attr('scrollTop');
            $rootEl.attr('scrollTop', initScrollTop + 1);
            if ($rootEl.attr('scrollTop') == initScrollTop + 1) {
                scrollElement = this.nodeName.toLowerCase();
                $rootEl.attr('scrollTop', initScrollTop);
                return false;
            }
        });
        var hash = window.location.hash;
        if (hash.substring(0, 2) == "#c") {
            var id = parseInt(hash.substring(2));
            if (!isNaN(id))
                scrollToComment(id, 1000);
        }
    });
    function setActiveInput() {
        active_input = this.name;
    }

    function onCommentFormSubmit(event) {
        event.preventDefault();
        var form = event.target;
        var preview = (active_input == 'preview');
        ajaxComment(form, {onsuccess: (preview ? null : onCommentPosted), preview: preview});
        return false;
    }

    function scrollToComment(id, speed) {
        var $comment = $("#c" + id);
        if ($comment.length == 0) {
            if (window.console)console.warn("scrollToComment() - #c" + id + " not found.");
            return;
        }
        if (window.on_scroll_to_comment && window.on_scroll_to_comment({comment: $comment}) === false)
            return;
        scrollToElement($comment, speed, COMMENT_SCROLL_TOP_OFFSET);
    }

    function scrollToElement($element, speed, offset) {
        if ($element.length)
            $(scrollElement).animate({scrollTop: $element.offset().top - (offset || 0)}, speed || 1000);
    }

    function onCommentPosted(comment_id, is_moderated, $comment) {
        var $message_span;
        if (is_moderated)
            $message_span = $("#comment-moderated-message").fadeIn(200); else
            $message_span = $("#comment-added-message").fadeIn(200);
    }

    var commentBusy = false;
    var previewAutoAdded = false;

    function ajaxComment(form, args) {
        var onsuccess = args.onsuccess;
        var preview = !!args.preview;
        $('div.comment-error').remove();
        if (commentBusy) {
            return false;
        }
        commentBusy = true;
        var $form = $(form);
        var comment = $form.serialize() + (preview ? '&preview=1' : '');
        var url = $form.attr('action') || './';
        var ajaxurl = $form.attr('data-ajax-action');
        if (!preview)
            $('#comment-waiting').fadeIn(1000);
        $.ajax({type: 'POST', url: ajaxurl || url, data: comment, dataType: 'json', success: function (data) {
            commentBusy = false;
            removeWaitAnimation();
            removeErrors();
            if (data.success) {
                var $added;
                if (preview)
                    $added = commentPreview(data); else
                    $added = commentSuccess(data);
                if (onsuccess)
                    args.onsuccess(data.comment_id, data.is_moderated, $added);
            }
            else {
                commentFailure(data);
            }
        }, error: function (data) {
            commentBusy = false;
            removeWaitAnimation();
        }});
        return false;
    }

    function commentSuccess(data) {
        $('form.js-comments-form textarea').last().val("");
        $('#id_comment').val('');
        var had_preview = removePreview();
        var $comments = getCommentsDiv();
        $comments.prepend(data['html']).removeClass('empty');
        var $new_comment = $comments.children("div.comment-item:last");
        if (had_preview)
            $new_comment.hide().fadeIn(600); else
            $new_comment.hide().show(600);
        return $new_comment;
    }

    function commentPreview(data) {
        var $previewarea = $("#comment-preview-area");
        if ($previewarea.length == 0) {
            getCommentsDiv().append('<div id="comment-preview-area"></div>').addClass('has-preview');
            $previewarea = $("#comment-preview-area");
            previewAutoAdded = true;
        }
        var had_preview = $previewarea.hasClass('has-preview-loaded');
        $previewarea.html(data.html).addClass('has-preview-loaded');
        if (!had_preview)
            $previewarea.hide().show(600);
    }

    function commentFailure(data) {
        for (var field_name in data.errors) {
            if (field_name) {
                var $field = $('#id_' + field_name);
                $field.after('<span class="js-errors">' + data.errors[field_name] + '</span>');
                $field.closest('.control-group').addClass('error');
            }
        }
    }

    function removeErrors() {
        $('form.js-comments-form .js-errors').remove();
        $('form.js-comments-form .control-group.error').removeClass('error');
    }

    function getCommentsDiv() {
        var $comments = $("#comments");
        if ($comments.length == 0)
            alert("Internal error - unable to display comment.\n\nreason: container is missing in the page.");
        return $comments;
    }

    function removePreview() {
        var $previewarea = $("#comment-preview-area");
        var had_preview = $previewarea.hasClass('has-preview-loaded');
        if (previewAutoAdded)
            $previewarea.remove(); else
            $previewarea.html('');
        $previewarea.removeClass('has-preview-loaded')
        $("#comments").removeClass('has-preview');
        return had_preview;
    }

    function removeWaitAnimation() {
        $('#comment-waiting').hide().stop();
    }
})(window.jQuery);
if (!jQuery)var jQuery = django.jQuery;
window.django_autocomplete_max_reached = false;
function init_jQueryTagit(options) {
    jQuery('#' + options.objectId).tagit({singleFieldDelimiter: ', ', fieldName: options.fieldName, tagSource: function (request, response) {
        jQuery.getJSON(options.sourceUrl, {term: request.term}, response);
    }, minLength: options.minLength, removeConfirmation: options.removeConfirmation, caseSensitive: options.caseSensitive, animate: options.animate, maxLength: options.maxLength, maxTags: options.maxTags, onTagAdded: options.onTagAdded, onTagRemoved: options.onTagRemoved, onTagClicked: options.onTagClicked, onMaxTagsExceeded: options.onMaxTagsExceeded});
};
$(document).ready(function () {
    $('ul.arating a').live('click', function (e) {
        e.preventDefault();
        var el = $(this);
        var base_url = el.attr('href').slice(0, -2);
        var url = base_url + el.attr('data-vote') + '/';
        $.getJSON(url, function (data) {
            var items = [];
            $.each(data.choices, function (key, val) {
                var choice = val
                var cel = $('ul.arating a.vote' + choice.key, el.parent().parent().parent());
                $('span.count', cel).html(choice.count);
                if (choice.active) {
                    cel.addClass('active')
                    cel.attr('data-vote', 0);
                } else {
                    cel.removeClass('active');
                    cel.attr('data-vote', choice.key);
                }
            });
        });
    });
});
var util = util || {};
util.uri_param_insert = function (sourceUrl, parameterName, parameterValue, replaceDuplicates) {
    if ((sourceUrl == null) || (sourceUrl.length == 0))
        sourceUrl = document.location.href;
    var urlParts = sourceUrl.split("?");
    var newQueryString = "";
    if (urlParts.length > 1) {
        var parameters = urlParts[1].split("&");
        for (var i = 0; (i < parameters.length); i++) {
            var parameterParts = parameters[i].split("=");
            if (!(replaceDuplicates && parameterParts[0] == parameterName)) {
                if (newQueryString == "")
                    newQueryString = "?"; else
                    newQueryString += "&";
                newQueryString += parameterParts[0] + "=" + parameterParts[1];
            }
        }
    }
    if (newQueryString == "")
        newQueryString = "?"; else
        newQueryString += "&";
    newQueryString += parameterName + "=" + parameterValue;
    return urlParts[0] + newQueryString;
};
util.string_random = function (length) {
    var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz'.split('');
    if (!length) {
        length = Math.floor(Math.random() * chars.length);
    }
    var str = '';
    for (var i = 0; i < length; i++) {
        str += chars[Math.floor(Math.random() * chars.length)];
    }
    return str;
};
util.format_time = function (secs) {
    var t = new Date(1970, 0, 1);
    t.setSeconds(secs);
    if (secs < 3600) {
        var s = t.toTimeString().substr(3, 5);
    } else {
        var s = t.toTimeString().substr(0, 8);
    }
    if (secs > 86399)
        s = Math.floor((t - Date.parse("1/1/70")) / 3600000) + s.substr(2);
    return s;
}
$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};
$(document).ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sameOrigin(url) {
        var host = document.location.host;
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return(url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
util.get_position = function (e) {
    var targ;
    if (!e)
        e = window.event;
    if (e.target)
        targ = e.target; else if (e.srcElement)
        targ = e.srcElement;
    if (targ.nodeType == 3)
        targ = targ.parentNode;
    var x = e.pageX - $(targ).offset().left;
    var y = e.pageY - $(targ).offset().top;
    return{"x": x, "y": y};
};
var base = base || {};
base.ui = base.ui || {};
base.ui.use_effects = true;
sm2 = function () {
};
$.cookie.defaults = {};
UiStates = function () {
    var self = this;
    this.css_selector = '.ui-persistent';
    this.cookie_name = 'ui_states';
    this.values = new HashTable();
    this.load = function () {
        $.log('load states');
        if ($.cookie(this.cookie_name)) {
            self.values.items = JSON.parse($.cookie(this.cookie_name));
        }
        $.log(['(load) current states', self.values.items]);
        this.apply_states();
    }, this.get_states = function (key) {
        $.log('get_states: ' + key);
        if (key !== undefined) {
            return self.values.getItem(key);
        } else {
            return false;
        }
    }, this.apply_states = function (key) {
        $.log('apply_states: ' + key);
        if (key !== undefined) {
            alert('not implemented');
        } else {
            $(this.css_selector).each(function (i, el) {
                var id = $(el).attr('id');
                var state = self.values.getItem(id);
                if (base.ui.states_custom_update(id, state)) {
                    return;
                }
                if (state == 'expanded') {
                    $(el).show();
                }
                ;
                if (state == 'hidden') {
                    $(el).hide();
                }
                ;
            });
        }
    }, this.set_states = function (key, value) {
        $.log('set_states: ' + key + ' - ' + value);
        if (key !== undefined && value !== undefined) {
            self.values.setItem(key, value);
        } else {
            $(this.css_selector).each(function (i, el) {
                self.values.setItem($(el).attr('id'), $(el).data('uistate'));
            });
        }
        $.log(['(set_states) current states', self.values.items]);
    }, this.save = function () {
        $.log('save');
        $.cookie(this.cookie_name, JSON.stringify(self.values.items));
        $.log('post-save');
    }
}
BaseUi = function () {
    var self = this;
    this.states = new UiStates();
    this.init = function () {
        $('.ui-persistent').watch('uistate', function () {
            var state = $(this).data('uistate');
            $.log('watched:' + state);
            self.states.set_states($(this).attr('id'), state);
            self.states.apply_states();
        });
        this.states.load();
    }, this.unload = function () {
        this.states.save();
    }
};
base.ui = new BaseUi();
base.ui.states_custom_update = function (id, state) {
    var el = $('#' + id);
    if (id == 'tagcloud_inline') {
        if (state == 'expanded') {
            $('#tagcloud_inline_toggle').addClass('active');
            el.css('display', 'block');
        }
        if (state == 'hidden') {
            $('#tagcloud_inline_toggle').removeClass('active');
            el.css('display', 'none');
        }
        return true;
    }
    if (id == 'playlist_basket') {
        if (state == 'expanded') {
            el.addClass('expanded');
        }
        if (state == 'hidden') {
            el.removeClass('expanded');
        }
        return true;
    }
    if (id == 'jingle_basket') {
        if (state == 'expanded') {
            el.addClass('expanded');
        }
        if (state == 'hidden') {
            el.removeClass('expanded');
        }
        return true;
    }
    if (id == 'default_jingle_set') {
        el.data('resource_uri', state);
        return true;
    }
    if (id.substring(0, 9) == 'filterbox') {
        $.log('custom state-update: ' + 'filterbox');
        if (state == 'expanded') {
            el.addClass('boxon');
            el.parent().addClass('boxon');
            $('.boxcontent', el.parent()).show();
        }
        if (state == 'hidden') {
            el.removeClass('boxon');
            el.parent().removeClass('boxon');
            $('.boxcontent', el.parent()).hide();
        }
        return true;
    }
    if (id == 'editor_mode') {
        $('body').removeClass('editor-mode-s');
        $('body').removeClass('editor-mode-m');
        $('body').removeClass('editor-mode-l');
        $('body').addClass('editor-mode-' + state);
        return true;
    }
    return false;
}
function HashTable(obj) {
    this.length = 0;
    this.items = {};
    for (var p in obj) {
        if (obj.hasOwnProperty(p)) {
            this.items[p] = obj[p];
            this.length++;
        }
    }
    this.setItem = function (key, value) {
        var previous = undefined;
        if (this.hasItem(key)) {
            previous = this.items[key];
        }
        else {
            this.length++;
        }
        this.items[key] = value;
        return previous;
    }
    this.getItem = function (key) {
        return this.hasItem(key) ? this.items[key] : undefined;
    }
    this.hasItem = function (key) {
        return this.items.hasOwnProperty(key);
    }
    this.removeItem = function (key) {
        if (this.hasItem(key)) {
            previous = this.items[key];
            this.length--;
            delete this.items[key];
            return previous;
        }
        else {
            return undefined;
        }
    }
    this.keys = function () {
        var keys = [];
        for (var k in this.items) {
            if (this.hasItem(k)) {
                keys.push(k);
            }
        }
        return keys;
    }
    this.values = function () {
        var values = [];
        for (var k in this.items) {
            if (this.hasItem(k)) {
                values.push(this.items[k]);
            }
        }
        return values;
    }
    this.each = function (fn) {
        for (var k in this.items) {
            if (this.hasItem(k)) {
                fn(k, this.items[k]);
            }
        }
    }
    this.clear = function () {
        this.items = {}
        this.length = 0;
    }
}
base.ui.loading = function () {
    $(document).ajaxStart(function () {
        $('.navbar .container').addClass('active');
        $('body').addClass('ajax_loading');
    }).ajaxStop(function () {
        $('.navbar .container').removeClass('active');
        $('body').removeClass('ajax_loading');
    });
}
base.ui.refresh = function () {
    $('#refresh').smartupdater({url: '/ui/refresh', minTimeout: 10000, multiplier: 2}, function (data) {
        $.taconite(data);
    });
};
base.ui.iface = function () {
    Boxy.DEFAULTS.title = '&nbsp;';
    if (window.console && console.firebug) {
        console.warn('You should disable firebug, else performance can be very low!');
    }
    $('.tooltipable').tooltip({delay: {show: 50, hide: 10}});
    $('.hoverable').live('mouseenter', function (e) {
        $(this).addClass('hover');
    });
    $('.hoverable').live('mouseleave', function (e) {
        $(this).removeClass('hover');
    });
    $('.linkable').live('click', function (e) {
        var href = $('a.link-main', this).attr('href');
        window.location.href = href;
    });
    $('a.transform-post.reload').live('click', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        $.post(href, function (d) {
        });
        $(this).parents('.item').hide(300);
    });
    jQuery(window).bind("focus",function (event) {
        if (base.ui.use_effects) {
            $('body').animate({opacity: 1}, {queue: true, duration: 200});
        } else {
            $('body').css('opacity', 1);
        }
        $('body').removeClass('blur');
    }).bind("blur", function (event) {
            if (base.ui.use_effects) {
            } else {
            }
            $('body').addClass('blur');
        });
    $('.action a').live('click', function (e) {
        if ($(this).parents('li').hasClass('disabled') || $(this).parents('li').hasClass('locked')) {
            alert('prevent');
            e.stopPropagation();
            return false;
        }
    });
    $('body').bind('DOMSubtreeModified', function (e) {
        try {
            if (e.target.innerHTML.length > 0) {
                $("a:not(.skip-external)").filter(function () {
                    return this.hostname && this.hostname !== location.hostname;
                }).addClass('external');
            }
        } catch (e) {
        }
    });
    $('.action.selection_delete a').live('click', function (e) {
        var item_type = $(this).attr('href').substring(1);
        items = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            items.push({item_type: item_type, item_id: item_id, format: 'mp3'});
        });
        var url = base.vars.base_url + 'ajax/items_delete';
        var data = {items: items};
        base.ui.ajax(url, data);
        return false;
    });
    $('.boxy-wrapper .inline.merge a.merge').live('click', function () {
        var master_id = $('input[name=merge_master_id]:checked').val();
        var item_type = $('input[name=item_type]').val();
        item_ids = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            if (item_id != master_id) {
                item_ids.push(item_id);
            }
        });
        var url = base.vars.base_url + 'ajax/items_merge';
        var data = {master_id: master_id, item_ids: item_ids.join(','), item_type: item_type, action: 'reload'};
        base.ui.ajax(url, data);
        Boxy.get(this).hide();
        return false;
    });
    $('.action.selection_reassign a').live('click', function () {
        if ($(this).hasClass('disabled')) {
            return false;
        }
        var item_type = $(this).attr('href').substring(1);
        item_ids = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            item_ids.push(item_id);
        });
        var url = '/ui/items_reassign?item_type=' + item_type + '&item_ids=' + item_ids.join(',');
        boxy = new Boxy.load(url, {modal: true});
        return boxy;
        return false;
    });
    $('.boxy-wrapper .inline.reassign a.reassign').live('click', function () {
        var create_name = $('input[name=release_name]').val();
        item_ids = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            item_ids.push(item_id);
        });
        var url = base.vars.base_url + 'ajax/items_reassign';
        var item_type = base.vars.subset.slice(0, -1);
        var data = {create_name: create_name, item_ids: item_ids.join(','), item_type: item_type};
        base.ui.ajax(url, data);
        Boxy.get(this).hide();
        return false;
    });
    $('.action.selection_play a').live('click', function () {
        if ($(this).hasClass('disabled')) {
            return false;
        }
        var item_type = $(this).attr('href').substring(1);
        var uri = base.vars.base_url + 'multiplay/play.json?' + item_type + '_ids=';
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            uri = uri + item_id + ',';
            if (base.ui.use_effects) {
                $(this).effect("transfer", {to: "#pplayer_inline"}, 300);
            }
        });
        var offset = 0;
        var mode = 'replace';
        var token = 'xx-yy-zz';
        base.ui.play_popup(uri, token, offset, mode);
        return false;
    });
    $('.___collectable').live('click', function (e) {
        e.preventDefault();
        var action = $(this).attr('href').substr(1).split(':');
        var item_type = action[0];
        var item_id = action[1];
        var format = action[2];
        items = new Array;
        items.push({item_type: item_type, item_id: item_id, format: format});
        if (base.ui.use_effects) {
            $('#list_item_' + item_id).effect("transfer", {to: ".playlist.basket"}, 300);
        }
        var data = {items: items};
        base.ui.collector.collect(items, false);
    });
    $('.action.selection_collect a').live('click', function () {
        if ($(this).hasClass('disabled')) {
            return false;
        }
        var item_type = $(this).attr('href').substring(1);
        items = new Array;
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            items.push({item_type: item_type, item_id: item_id, format: 'default'});
            if (base.ui.use_effects) {
                $(this).effect("transfer", {to: ".playlist.basket"}, 300);
            }
        });
        var url = base.vars.base_url + 'ajax/collect';
        var data = {items: items};
        $.ajax({url: url, type: "POST", data: data, dataType: "json", success: function (result) {
            if (true == result['status']) {
                $('#element').load('/ui/sidebar_playlist' + '?r=' + util.string_random(20));
            } else {
                base.ui.ui_message(result['message']);
            }
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            base.ui.ui_message(errorThrown);
        }});
        return false;
    });
    $('.shorten').shorten();
    $('#sitemessages .message a.action').live('click', function () {
        var attr = $(this).attr('href').substr(1).split(':');
        var context = 'messages';
        var command = attr[0];
        var id = attr[1];
        base.ui.ajax_action(context, command, id);
        return false;
    });
    $.fn.on_focus_input = function () {
        return this.focus(function () {
            $(this).addClass('focus');
            $(this).removeClass('blur');
            if (this.value == this.defaultValue) {
                this.value = "";
            }
        }).blur(function () {
            $(this).removeClass('focus');
            $(this).addClass('blur');
            if (!this.value.length) {
                this.value = this.defaultValue;
            }
        });
    };
    $('div.slideout.base').css('display', 'block');
    $('#feedback_submit').click(function () {
        var topic = $('div.slideout.base select[name=topic]').val();
        var subject = $('div.slideout.base input[name=subject]').val();
        var message = $('div.slideout.base textarea[name=message]').val();
        var from = $('div.slideout.base input[name=from]').val();
        var location = $('div.slideout.base input[name=location]').val();
        var request = $('div.slideout.base input[name=request]').val();
        $('div.slideout.base textarea, div.slideout.base select, div.slideout.base input').removeClass('error');
        if (topic && subject && message && from) {
            var url = base.vars.base_url + 'ajax/feedback_send';
            var data = {topic: topic, subject: subject, message: message, from: from, location: location, request: request};
            $.ajax({url: url, type: "POST", data: data, dataType: "json", success: function (result) {
                if (true == result['status']) {
                    $('.inner.feedback').html(result['message']);
                } else {
                    base.ui.ui_message(result['message']);
                }
            }, error: function (XMLHttpRequest, textStatus, errorThrown) {
                base.ui.ui_message(errorThrown);
            }});
        } else {
            if (!topic) {
                $('div.slideout.base select[name=topic]').addClass('error');
            }
            if (!subject) {
                $('div.slideout.base input[name=subject]').addClass('error');
            }
            if (!from) {
                $('div.slideout.base input[name=from]').addClass('error');
            }
            if (!message) {
                $('div.slideout.base textarea[name=message]').addClass('error');
            }
        }
        return false;
    });
    $('dd.limit').on('click', 'a.toggle', function (e) {
        e.preventDefault();
        $('.limited', $(this).parents('dd')).toggle();
    });
};
base.ui.ajax_action = function (context, command, id) {
    var url = base.vars.base_url + 'ajax/' + context + '/' + command + '/' + id;
    var data = {command: command, id: id};
    var result = false
    $.ajax({url: url, async: false, type: "POST", data: data, dataType: "json", success: function (result) {
        if (true == result['status']) {
            if (false != result['message']) {
                base.ui.ui_message(result['message'], 10000);
            }
            switch (result['post_action']) {
                case'message_remove':
                    $('#sitemessages #message_' + id).fadeOut();
            }
        } else {
            if (false != result['message']) {
                base.ui.ui_message(result['message']);
            }
        }
    }, error: function (XMLHttpRequest, textStatus, errorThrown) {
        base.ui.ui_message(errorThrown);
    }});
};
base.ui.skeleton = function () {
    $('a.action.beta_notes').live('click', function (event) {
        var uri = $(this).attr('href').substr(1);
        if ($('#slider_top').hasClass('open')) {
            $('#slider_top').removeClass('open');
            $('#slider_top').fadeOut();
            $('#slider_top').html('');
        } else {
            $('#slider_top').addClass('open');
            $('#slider_top').fadeIn();
            $('#slider_top').load('/static/element/' + uri);
        }
        return false;
    });
};
base.ui.toolbar = function () {
    $('a', 'ul.navigation-main').live('click', function (e) {
        e.preventDefault();
        var section = $(this).parent().attr('id').substring(9);
        $('ul.navigation-sub').hide();
        $('ul#nav_sub-' + section).show();
        return false;
    });
    $('.navigation-sub > li.descendant').parent().css('display', 'block');
    $('.navigation-sub > li.selected').parent().css('display', 'block');
    $('.navigation-sub > li.ancestor').parent().css('display', 'block');
    $("#toolbar #username").on_focus_input();
    $("#toolbar #password").on_focus_input();
    $(".nav_sub a.chat_irc").live('click', function (e) {
        e.preventDefault();
        uri = base.vars.irc_chat_url + '&nick=' + base.vars.username;
        var chat_win = window.open('', 'chat', 'width=650, height=720');
        if (chat_win) {
            if (typeof(chat_win.loaded) == 'undefined') {
                chat_win.location.href = uri;
            }
        } else {
            alert('sorry - chat could not be loaded');
        }
        chat_win.focus();
        return false;
    });
};
AutocompleteApp = function () {
    var self = this;
    this.api_url;
    this.container;
    this.ct;
    this.template = 'alibrary/nj/release/autocomplete.html';
    this.q_min = 2;
    this.search = function (q) {
        console.log('AutocompleteApp - search', q);
        if (q.length >= this.q_min) {
            $.get(this.api_url + '?q=' + q, function (data) {
                self.display(data);
            });
        } else {
            self.container.html('');
        }
    };
    this.display = function (data) {
        console.log(data);
        html = nj.render(self.template, data);
        self.container.html(html);
    };
};
base.ui.searchbar = function () {
    var self = this;
    var container = $('#searchbar');
    var ct = container.data('ct');
    this.autocomplete = new AutocompleteApp();
    this.autocomplete.ct = ct;
    this.autocomplete.template = 'alibrary/nj/' + ct + '/autocomplete.html';
    if (ct == 'media') {
        ct = 'track';
    }
    this.autocomplete.api_url = '/api/v1/' + ct + '/autocomplete/';
    this.autocomplete.container = $('#autocomplete_holder');
    $("#searchbar_input", container).live('keyup', function (e) {
        var q = $(this).val();
        if (e.keyCode == 13 || e.keyCode == 9) {
            var uri = util.uri_param_insert(window.location.href, 'q', q, true);
            uri = util.uri_param_insert(uri, 'page', 1, true);
            window.location = uri;
            return false;
        } else {
            debug.debug('query:', q);
            self.autocomplete.search(q);
        }
    });
    $('a.tbtag.search').live('click', function (e) {
        if ($(e.target).is("input")) {
            e.preventDefault();
            return false;
        }
    });
    $('input.autosize').each(function () {
        $(this).attr("size", $(this).val().length);
    });
    $('input.autosize').autoGrowInput({comfortZone: 5, minWidth: 5, maxWidth: 170});
    $("#searchbar_input").on_focus_input();
};
base.ui.tagcloud = function () {
    $('a#tagcloud_inline_toggle').live('click', function (e) {
        e.preventDefault();
        var display = $('#tagcloud_inline').css('display');
        if (display == 'none') {
            $('#tagcloud_inline').data('uistate', 'expanded');
        }
        if (display == 'block') {
            $('#tagcloud_inline').data('uistate', 'hidden');
        }
    });
    total_count = 0;
    $('#tagcloud_inline .toggle-level').each(function (i, e) {
    });
    $('.tag-level a', '#tagcloud_inline').live('click', function (e) {
        e.preventDefault();
        var level = $(this).data('taglevel');
        for (i = 1; i <= level; i++) {
            console.log('show:', i);
            $('a.level' + (i), '#tagcloud_inline').removeClass('tag-hidden');
        }
        for (i = 6; i > level; i--) {
            console.log('hide:', i);
            $('a.level' + (i), '#tagcloud_inline').addClass('tag-hidden');
        }
    });
};
base.ui.sidebar = function () {
    $('div.box div.boxtitle').live('click', function (e) {
        e.preventDefault();
        if (!$(this).hasClass('boxon')) {
            $(this).data('uistate', 'expanded');
        } else {
            $(this).data('uistate', 'hidden');
        }
    });
    $('.box select.range').live('change', function (e) {
        var key = $(this).attr('id');
        var value = $(this).val();
        var rel = base.vars.context + '_' + base.vars.section + '_' + base.vars.subset;
        var url = base.vars.base_url + 'ajax/filter_set_value';
        var active = $(this).parent().parent().find('a.filterbox_item').hasClass('on');
        var action = false;
        if (active) {
            action = 'reload';
        }
        var data = {'key': key, 'rel': rel, 'value': value, 'action': action};
        $.ajax({url: url, type: "POST", data: data, dataType: "json", success: function (result) {
            if (true == result['status']) {
                if (result['message']) {
                    base.ui.ui_message(result['message'], 10000);
                }
                if (result['action'] == 'reload') {
                    window.location.reload();
                }
            } else {
                base.ui.ui_message(result['message']);
            }
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            base.ui.ui_message(errorThrown);
        }});
        return false;
    });
    $('.box select.country').live('change', function (e) {
        var key = $(this).attr('id');
        var value = $(this).val();
        var uri = util.uri_param_insert(window.location.href, key, value, true);
        uri = util.uri_param_insert(uri, 'page', 1, true);
        window.location = uri;
        return false;
    });
    $('.box select.sorting').live('change', function (e) {
        e.preventDefault();
        var id = $(this).attr('id');
        var value = $(this).val();
        var key = false;
        switch (id) {
            case'sort_key':
                key = 'order_by';
                break;
            case'sort_direction':
                key = 'direction';
                break;
        }
        var uri = util.uri_param_insert(window.location.href, key, value, true);
        window.location = uri;
        return false;
    });
    $('.action.download_delete a').live('click', function () {
        if ($(this).hasClass('disabled')) {
            return false;
        }
        var range = false;
        if ($(this).parents('li').hasClass('delete_all')) {
            range = 'delete_all';
        }
        if ($(this).parents('li').hasClass('delete_completed')) {
            range = 'delete_completed';
        }
        var url = base.vars.base_url + 'ajax/downloads_delete';
        var data = {range: range, action: 'reload'};
        $.ajax({url: url, type: "POST", data: data, dataType: "json", success: function (result) {
            if (true == result['status']) {
                if (result['message']) {
                    base.ui.ui_message(result['message'], 10000);
                }
                if ('reload' == result['action']) {
                    window.location.reload();
                }
            } else {
                base.ui.ui_message(result['message']);
            }
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            base.ui.ui_message(errorThrown);
        }});
        return false;
    });
    $('.sidebar .box').each(function (i, el) {
        var list = $(this).find('.boxcontent');
        var count_available = $('> div', list).size();
        var count_active = $('> div.minus', list).size();
        if (count_active > 0) {
            $(this).find('.boxtitle span').append('<span style="float: right"><span class="opt" style="text-align: right; color: #00BB00;">' + count_active + '</span><span class="opt" style="color: #999999;">/' + count_available + '</span>&nbsp;&nbsp;</span>');
            $(this).addClass('has_active');
        } else {
            $(this).find('.boxtitle span').append('<span style="float: right"><span class="opt" style="text-align: right; color: #999999;">' + count_active + '/' + count_available + '</span>&nbsp;&nbsp;</span>');
            $(this).removeClass('has_active');
        }
    });
};
base.ui.itemview = function () {
    var zoomable_defaults = {transition: "none", width: "520px", height: "520px"};
    $("a.zoomable").colorbox(zoomable_defaults);
    $("a.zoomable").hover(function () {
        $(this).addClass("hover");
    }, function () {
        $(this).removeClass("hover");
    });
    var rate_defaults = {showHalf: true, path: '/media/css/img/raty/', score: 'rate_score'};
    $('.rate').raty(rate_defaults);
};
base.ui.listview = function () {
    $('div.listview.container div.list_body_row').hover(function (event) {
        $(this).addClass("hover");
    }, function (event) {
        $(this).removeClass("hover");
    });
    $('div.listview.container div.list_body_row.selectable').live('click', function (event) {
        if ($(event.target).is("a") || $(event.target).is("img") || $(event.target).is("i")) {
        }
        else {
            $(this).toggleClass('selection');
            base.ui.listview.selection_update();
        }
    });
    $('div.listview.footer #control_selection a.action').live('click', function (event) {
        var options = $(this).attr('href').substr(1).split(':');
        var context = options[0];
        var action = options[1];
        switch (action) {
            case'invert':
                $('div.listview.container div.list_body_row.selectable.selection').addClass('selection_old');
                $('div.listview.container div.list_body_row.selectable').addClass('selection');
                $('div.listview.container div.list_body_row.selectable.selection_old').removeClass('selection').removeClass('selection_old');
                break;
            case'all':
                $('div.listview.container div.list_body_row.selectable').addClass('selection');
                break;
            case'clear':
                $('div.listview.container div.list_body_row.selectable').removeClass('selection');
                break;
        }
        base.ui.listview.selection_update();
        return false;
    });
    if (base.vars.list_highlight) {
        var hls = base.vars.list_highlight.split(' ');
        for (i in hls) {
            $('.listview.container .list_body').highlight(hls[i]);
        }
    }
};
base.ui.listview.selection_update = function () {
    var current_selection = [];
    $('div.list_body_row.selectable.selection').each(function () {
        var item_id = $(this).attr('id').split("_").pop();
        current_selection.push(item_id);
    });
    $('.action .selection-required').addClass('disabled');
    $('.action .selection-required.selection-multiple small').html('');
    $('.action .selection-required.selection-any small').html('');
    var count = current_selection.length;
    switch (count) {
        case 0:
            $('.action .selection-required').addClass('disabled');
            break;
        case 1:
            $('.action .selection-required.selection-single').removeClass('disabled');
            $('.action .selection-required.selection-any').removeClass('disabled');
            $('.action .selection-required.selection-any small').html(count);
            break;
        default:
            $('.action .selection-required.selection-multiple').removeClass('disabled');
            $('.action .selection-required.selection-any').removeClass('disabled');
            $('.action .selection-required.selection-multiple small').html(count);
            $('.action .selection-required.selection-any small').html(count);
            break;
    }
    base.ui.listview.selection_current = [];
    $('div.listview.container div.list_body_row.selectable.selection').each(function () {
        var item_id = $(this).attr('id').split("_").pop();
        base.ui.listview.selection_current.push(item_id);
    });
    var selected_count = base.ui.listview.selection_current.length;
    $('.action.selection_required').addClass('disabled');
    $('.action.selection_required.selection_multiple span.opt').html('');
    $('.action.selection_required.selection_any span.opt').html('');
    switch (selected_count) {
        case 0:
            $('.action.selection_required').addClass('disabled');
            break;
        case 1:
            $('.action.selection_required.selection_single').removeClass('disabled');
            $('.action.selection_required.selection_any').removeClass('disabled');
            break;
        default:
            $('.action.selection_required.selection_multiple').removeClass('disabled');
            $('.action.selection_required.selection_any').removeClass('disabled');
            $('.action.selection_required.selection_multiple span.opt').html('(' + selected_count + ')');
            $('.action.selection_required.selection_any span.opt').html('(' + selected_count + ')');
            break;
    }
};
base.ui.listview.selection_current = new Array;
base.ui.tracklist = function () {
};
sm2.test = function (param) {
    $.playable(base.vars.js_path + 'lib/sm2/swf/', {debugMode: true});
    $('div.sm2').playable();
};
sm2.rtmp = function (param) {
    soundManager.url = '/media/js/lib/sm2/swf/';
    soundManager.useMovieStar = true;
    soundManager.flashVersion = 9;
    soundManager.debugMode = true;
    soundManager.debugFlash = true;
    soundManager.useConsole = true;
    soundManager.useHTML5Audio = true;
    soundManager.onready(function () {
        soundManager.createSound({id: 'rtmp_live', serverURL: 'rtmp://yoddha.anorg.net/recast/', url: 'mp3:obp.stream', autoPlay: true});
    });
};
$.jGrowl.defaults.position = 'bottom-center';
base.ui.ui_message = function (message, life) {
    if (typeof(life) == 'undefined') {
        life = 2000;
    }
    $.jGrowl(message, {life: life});
    return true;
};
base.ui.load_state = function () {
    base.ui.state = $.cookie('ui_state');
    return true;
};
base.ui.save_state = function (key, val, action) {
    if (action === undefined) {
        action = "reload";
    }
    var url = base.vars.base_url + 'ui/state_save';
    var data = {key: key, val: val, action: action};
    $.ajax({url: url, type: "POST", data: data, dataType: "json", success: function (result) {
        if (true == result['status']) {
            if ('reload' == result['action']) {
                window.location.reload();
            }
            if ('reset_page' == result['action']) {
                var uri = util.uri_param_insert(window.location.href, 'page', 1, true);
                window.location = uri;
            }
        } else {
            base.ui.ui_message(result['message']);
        }
    }, error: function (XMLHttpRequest, textStatus, errorThrown) {
        alert(errorThrown);
    }});
};
base.ui.play = new Object;
base.ui.play_popup = function (uri, token, offset, mode) {
    if (mode === undefined) {
        mode = "replace";
    }
    if (offset === undefined) {
        offset = 0;
    }
    base.ui.play.uri = uri;
    base.ui.play.token = token;
    base.ui.play.offset = offset;
    base.ui.play.mode = mode;
    pplayer = base.ui.grab_player(true, true);
};
base.ui.pplayer_do_grab = function () {
    pplayer = base.ui.grab_player(true, false);
};
base.ui.pplayer_ready = function (pplayer) {
    pplayer.load(base.ui.play.uri, base.ui.play.token, base.ui.play.offset, base.ui.play.mode);
    pplayer = pplayer;
};
base.ui.pplayer_status = function (obj) {
};
base.ui.pplayer_update = function (item) {
    if (!item) {
        item = new Object;
        item.name = '';
        item.release = '';
        item.artist = '';
        item.id = 0;
        item.release_id = 0;
    }
    var name = (item.name != undefined) ? item.name : '';
    var release = (item.release != undefined) ? item.release : '';
    var artist = (item.artist != undefined) ? item.artist : '';
    $('#pplayer_inline_scroll .name').html('<a href="' + item.release_url + '">' + name + '</a>');
    $('#pplayer_inline_scroll .release').html('<a href="' + item.release_url + '">' + release + '</a>');
    $('#pplayer_inline_scroll .artist').html('<a href="' + item.artist_url + '">' + artist + '</a>');
    $('.listview.container.medias .list_body_row').removeClass('playing');
    $('.listview.container.medias #list_item_' + item.id).addClass('playing');
    $('.listview.container.releases .list_body_row').removeClass('playing');
    $('.listview.container.releases #list_item_' + item.release_id).addClass('playing');
};
base.ui.pplayer_progress_update = function (sound) {
};
base.ui.grab_player = function (force, focus) {
    if (force === undefined) {
        force = false;
    }
    if (focus === undefined) {
        focus = false;
    }
    var pplayer_win = window.open('', 'pplayer', 'width=362, height=570');
    if (pplayer_win) {
        pplayer_win.opener = window;
        pplayer = pplayer_win.pplayer;
        if (typeof(pplayer_win.loaded) == 'undefined') {
            pplayer_win.location.href = '/player';
        } else {
            if (pplayer && force) {
                base.ui.pplayer_ready(pplayer);
            }
        }
    } else {
        var message = '<p><br />&nbsp;Unable to open the Player-window. Please set your browser to allow popups from this site.<br /><br /></p>';
        boxy = new Boxy(message);
    }
    if (focus) {
        pplayer_win.focus();
    }
    try {
        var index = pplayer.sound_current.split("_").pop();
        var item = pplayer.current_item;
        base.ui.pplayer_update(item);
    }
    catch (err) {
    }
    ;
    return pplayer;
};
base.ui.dialog = function (url, title) {
    $('.boxy-wrapper .close').live('click', function () {
        Boxy.get(this).hide();
        return false;
    });
    $('a.dialog.info').live('click', function () {
        base.ui.dialog_show(false, $(this).attr('href'));
        return false;
    });
    $('a.dialog.modal').live('click', function () {
        base.ui.dialog_show(true, $(this).attr('href'));
        return false;
    });
};
base.ui.dialog_show = function (modal, url, title) {
    if (modal === undefined) {
        modal = false;
    }
    if (title === undefined) {
        title = '&nbsp;';
    }
    boxy = new Boxy.load(url, {modal: modal, closeText: 'X'});
    return boxy;
};
base.ui.dialog_static = function (dialog) {
    message = '<div class="message ' + dialog.type + '">' + dialog.message + '</div>';
    boxy = new Boxy(message, {title: dialog.title});
    return boxy;
};
base.ui.ajax = function (url, data) {
    if (base.vars.ga_track_events) {
        _gaq.push(['_trackEvent', 'AJAX', 'call', url]);
    }
    $.ajax({url: url, type: "POST", data: data, dataType: "json", success: function (result) {
        if (true == result['status']) {
            if (result['message']) {
                base.ui.ui_message(result['message'], 10000);
            }
            if (result['dialog']) {
                base.ui.dialog_static(result['dialog']);
            }
            if (result['action'] == 'reload') {
                window.location.reload();
            }
            if (result['redirect']) {
                window.location = result['redirect'];
            }
            if ('reset_page' == result['action']) {
                var uri = util.uri_param_insert(window.location.href, 'page', 1, true);
                window.location = uri;
            }
        } else {
            if (result['message']) {
                base.ui.ui_message(result['message']);
            }
            if (result['dialog']) {
                base.ui.dialog_static(result['dialog']);
            }
        }
        if (result['eval']) {
            eval(result['eval']);
        }
    }, error: function (XMLHttpRequest, textStatus, errorThrown) {
        base.ui.ui_message(errorThrown);
    }});
};
$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};
base.ui.state___ = {options: {layoutName: 'myLayout', keys: 'north__size,south__size,east__size,west__size,' + 'north__isClosed,south__isClosed,east__isClosed,west__isClosed,' + 'north__isHidden,south__isHidden,east__isHidden,west__isHidden', domain: '', path: '', expires: '', secure: false}, data: {}, clear: function (layoutName) {
    this.save(layoutName, 'dummyKey', {expires: -1});
}, save: function (layoutName, keys, opts) {
    var
        o = jQuery.extend({}, this.options, opts || {}), layout = window[layoutName || o.layoutName];
    if (!keys)keys = o.keys;
    if (typeof keys == 'string')keys = keys.split(',');
    if (!layout || !layout.state || !keys.length)return false;
    var
        isNum = typeof o.expires == 'number', date = new Date(), params = '', clear = false;
    if (isNum || o.expires.toUTCString) {
        if (isNum) {
            if (o.expires <= 0) {
                date.setYear(1970);
                clear = true;
            }
            else
                date.setTime(date.getTime() + (o.expires * 24 * 60 * 60 * 1000));
        }
        else
            date = o.expires;
        params += ';expires=' + date.toUTCString();
    }
    if (o.path)params += ';path=' + o.path;
    if (o.domain)params += ';domain=' + o.domain;
    if (o.secure)params += ';secure';
    if (clear) {
        this.data = {};
        document.cookie = (layoutName || o.layoutName) + '=' + params;
    }
    else {
        this.data = readState(layout, keys);
        document.cookie = (layoutName || o.layoutName) + '=' + encodeURIComponent(JSON.stringify(this.data)) + params;
    }
    return this.data;
    function readState(layout, keys) {
        var
            state = layout.state, data = {}, panes = 'north,south,east,west,center', alt = {isClosed: 'initClosed', isHidden: 'initHidden'}, delim = (keys[0].indexOf('__') > 0 ? '__' : '.'), pair, pane, key, val;
        for (var i = 0; i < keys.length; i++) {
            pair = keys[i].split(delim);
            pane = pair[0];
            key = pair[1];
            if (panes.indexOf(pane) < 0)continue;
            if (key == 'isClosed')
                val = state[pane][key] || state[pane]['isSliding']; else
                val = state[pane][key];
            if (val != undefined) {
                if (delim == '.') {
                    if (!data[pane])data[pane] = {};
                    data[pane][alt[key] ? alt[key] : key] = val;
                }
                else
                    data[pane + delim + (alt[key] ? alt[key] : key)] = val;
            }
        }
        return data;
    }
}, load: function (layoutName) {
    if (!layoutName)layoutName = this.options.layoutName;
    if (!layoutName)return{};
    var
        data = {}, c = document.cookie, cs, pair, i;
    if (c && c != '') {
        cs = c.split(';');
        for (i = 0; i < cs.length; i++) {
            c = jQuery.trim(cs[i]);
            pair = c.split('=');
            if (pair[0] == layoutName) {
                data = JSON.parse(decodeURIComponent(pair[1]));
                break;
            }
        }
    }
    return(this.data = data);
}};
(function (jQuery) {
    var union = function (array1, array2) {
        var hash = {}, union = [];
        $.each($.merge($.merge([], array1), array2), function (index, value) {
            hash[value] = value;
        });
        $.each(hash, function (key, value) {
            union.push(key);
        });
        return union;
    };
    jQuery.fn.union = union;
    jQuery.union = union;
})(jQuery);
(function (jQuery) {
    var decodeHTMLEntities = function (str) {
        if (str && typeof str === 'string') {
            var element = document.createElement('div');
            str = str.replace(/<script[^>]*>([\S\s]*?)<\/script>/gmi, '');
            str = str.replace(/<\/?\w(?:[^"'>]|"[^"]*"|'[^']*')*>/gmi, '');
            element.innerHTML = str;
            str = element.textContent;
            element.textContent = '';
        }
        return str;
    }
    jQuery.fn.decodeHTML = decodeHTMLEntities;
    jQuery.decodeHTML = decodeHTMLEntities;
})(jQuery);
if (typeof String.prototype.endsWith !== 'function') {
    String.prototype.endsWith = function (suffix) {
        return this.indexOf(suffix, this.length - suffix.length) !== -1;
    };
}
function arrRemove(arr, from, to) {
    var rest = arr.slice((to || from) + 1 || arr.length);
    this.length = from < 0 ? arr.length + from : from;
    return arr.push.apply(arr, rest);
}
function isInt(value) {
    return!isNaN(parseInt(value, 10)) && (parseFloat(value, 10) == parseInt(value, 10));
}
(function (window, undefined) {
    util = util || {};
    var UtilNotify = (function () {
        var self = this;
        this.init = (function () {
            if (!this.havePermission && window.webkitNotifications) {
                $('.util.notify.enable').show().live('click', function () {
                    self.requestPermission();
                });
            }
            ;
        });
        this.requestPermission = function () {
            window.webkitNotifications.requestPermission();
        };
        this.havePermission = function () {
            if (window.webkitNotifications.checkPermission() == 0) {
                return true;
            } else {
                return false;
            }
        };
        this.notify = function (noteObject, targetUrl) {
            if (self.havePermission) {
                var n = window.webkitNotifications.createNotification(null, 'Download ready!', 'Here is the notification text');
                n.onclick = function (x) {
                    window.focus();
                    this.cancel();
                }
                n.show();
            } else {
                self.requestPermission();
            }
        };
    });
    util.notify = new UtilNotify;
    util.notify.init();
})(window);
(function (window, undefined) {
    util = util || {};
    var UtilDialog = (function () {
        var self = this;
        this.init = (function () {
            console.log('UtilDialog: init');
        });
        this.show = function (object) {
            if (object.url) {
                $('<div />').qtip({content: {text: '<div class="loading"><span class="throbber large"></span></loading>', title: {text: 'aa&nbsp;', button: true}}, position: {my: 'center', at: 'center', target: $(window)}, show: {ready: true, modal: {on: true, blur: false}}, hide: false, style: 'dialog dialog-base', events: {render: function (event, api) {
                }, hide: function (event, api) {
                    api.destroy();
                }}});
            } else {
                $('<div />').qtip({content: {text: '<div>' + object.text + '</div>', title: {text: object.title, button: true}}, position: {my: 'center', at: 'center', target: $(window)}, show: {ready: true, modal: {on: true, blur: true}}, hide: false, style: 'dialog dialog-base qtip-rounded', events: {render: function (event, api) {
                }, hide: function (event, api) {
                    api.destroy();
                }}});
            }
        };
    });
    util.dialog = new UtilDialog;
    util.dialog.init();
})(window);
PushyAssetApp = function () {
    var self = this;
    this.socket_url;
    this.socket;
    this.debug = true;
    this.subscriptions = [];
    this.init = function () {
        debug.debug('PushyAssetApp - init');
        pushy.subscribe('pushy_asset/refresh/', function () {
            debug.debug('pushy callback');
            self.refresh();
        });
    };
    this.refresh = function () {
        debug.debug('PushyAssetApp - refresh');
        var q = '?reload=' + new Date().getTime();
        $('link[rel="stylesheet"]').each(function () {
            if (this.href.indexOf("wip.css") != -1) {
                this.href = this.href.replace(/\?.*|$/, q);
            } else {
                console.log(this.href)
                console.log('not refreshing, is external one.')
            }
        });
    };
};
var pa;
$(function () {
    pa = new PushyAssetApp();
    pa.init();
})
jQuery.fn.liScroll = function (settings) {
    settings = jQuery.extend({travelocity: 0.07}, settings);
    return this.each(function () {
        var $strip = jQuery(this);
        $strip.addClass("newsticker")
        var stripWidth = 1;
        $strip.find("li").each(function (i) {
            stripWidth += jQuery(this, i).outerWidth(true);
        });
        var $mask = $strip.wrap("<div class='mask'></div>");
        var $tickercontainer = $strip.parent().wrap("<div class='tickercontainer'></div>");
        var containerWidth = $strip.parent().parent().width();
        $strip.width(stripWidth);
        var totalTravel = stripWidth + containerWidth;
        var defTiming = totalTravel / settings.travelocity;

        function scrollnews(spazio, tempo) {
            $strip.animate({left: '-=' + spazio}, tempo, "linear", function () {
                $strip.css("left", containerWidth);
                scrollnews(totalTravel, defTiming);
            });
        }

        scrollnews(totalTravel, defTiming);
        $strip.hover(function () {
            jQuery(this).stop();
        }, function () {
            var offset = jQuery(this).offset();
            var residualSpace = offset.left + stripWidth;
            var residualTime = residualSpace / settings.travelocity;
            scrollnews(residualSpace, residualTime);
        });
    });
};
var loaded = true;
var aplayer = aplayer || {};
aplayer.base = aplayer.base || {};
aplayer.vars = aplayer.vars || {};
var local = local || {};
local.timer = local.timer || false;
aplayer.backend = aplayer.backend || 'jwp';
var initial_states = {current: 0, uuid: false, next: false, prev: false};
aplayer.states = aplayer.states || initial_states;
aplayer.states_last = aplayer.states_last || false;
aplayer.vars.states = {current: 0, next: false, prev: false};
aplayer.vars.len_interval = 300;
aplayer.vars.debug = true;
aplayer.vars.version = '0.2.17b';
aplayer.vars.stream_mode = 'html5';
aplayer.base.init = function () {
    if (aplayer.vars.mode === undefined) {
        aplayer.vars.mode = "replace";
    }
    if (aplayer.vars.playlist_api_url === undefined) {
        aplayer.vars.playlist_api_url = false;
    }
    if (aplayer.backend == 'jwp') {
        aplayer.player = aplayer.jwp('aplayer_container');
    }
};
aplayer.jwp = function (container) {
    try {
        jwplayer(container).remove();
    } catch (e) {
    }
    ;
    return jwplayer(container).setup({id: container, flashplayer: aplayer.vars.swf_url, height: 10, width: 610, repeat: false, rtmp: {bufferlength: 1.0, securetoken: "Kosif093n203a"}, events: {onReady: function () {
        aplayer.jwp.on_ready();
    }, onPlaylist: function (event) {
        aplayer.jwp.on_playlist(event);
    }, onComplete: function (event) {
        aplayer.jwp.on_complete(event);
    }}, modes: [
        {type: 'flash', src: aplayer.vars.swf_url},
        {type: 'html5'}
    ], });
};
aplayer.jwp.on_ready = function () {
    aplayer.base.debug('aplayer.jwp.on_ready()');
    aplayer.base.ready();
};
aplayer.jwp.on_playlist = function (event) {
    var uuid = event.playlist[0].mediaid;
    var index = parseFloat(event.playlist[0].index);
    aplayer.base.on_play(index, uuid);
};
aplayer.jwp.on_complete = function (event) {
    aplayer.base.on_complete();
};
aplayer.base.ready = function () {
    aplayer.base.debug('initial load. calling remote window');
    parent_win.aplayer.base.remote_player_ready(aplayer);
    $(window).unload(function () {
        parent_win.aplayer.base.release_remote_player();
    });
};
aplayer.base.load = function (play) {
    console.log('aplayer.base.load - callback from remote window. object to play:', play);
    if (play.source == 'abcast') {
        $('body').removeClass('alibrary');
        $('body').addClass('abcast');
        $('.nav li[data-source="alibrary"]').removeClass('active');
        $('.nav li[data-source="abcast"]').addClass('active');
    } else {
        $('body').addClass('alibrary');
        $('body').removeClass('abcast');
        $('.nav li[data-source="alibrary"]').addClass('active');
        $('.nav li[data-source="abcast"]').removeClass('active');
    }
    aplayer.vars.uri = play.uri;
    if (play.mode === undefined) {
        aplayer.vars.mode = "replace";
    } else {
        aplayer.vars.mode = play.mode;
    }
    if (play.offset === undefined) {
        aplayer.vars.offset = 0;
    } else {
        aplayer.vars.offset = play.offset;
    }
    if (play.force_seek === undefined) {
        aplayer.vars.force_seek = false;
    } else {
        aplayer.vars.force_seek = play.force_seek;
    }
    aplayer.vars.source = play.source;
    console.log('uri - ' + play.uri);
    aplayer.ui.hide_overlay();
    aplayer.base.load_playlist(play.uri);
};
aplayer.base.load_playlist = function (uri) {
    console.log('aplayer.base.load_playlist', uri);
    if (uri) {
        data = {};
        if (uri.indexOf("playlist") != -1) {
            uri += '?all=true';
        }
        $.ajax({url: uri, traditional: true, type: "GET", data: data, dataType: "json", success: function (result, textStatus, jqXHR) {
            console.log('loaded playlist:', result);
            if (uri.indexOf("release") != -1) {
                aplayer.base.set_playlist(result.media);
            } else if (uri.indexOf("track") != -1) {
                if (result.objects) {
                    aplayer.base.set_playlist(result.objects);
                } else {
                    aplayer.base.set_playlist([result]);
                }
            } else if (uri.indexOf("playlist") != -1) {
                var media = [];
                $.each(result.items, function (i, item) {
                    console.log('co:', item.item.content_object)
                    media.push(item.item.content_object);
                })
                aplayer.base.set_playlist(media);
                aplayer.base.complete_playlist()
            } else if (uri.indexOf("channel") != -1) {
                aplayer.base.set_playlist([result]);
            } else {
                aplayer.base.set_playlist(result.objects);
            }
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            aplayer.base.debug('error: ' + errorThrown);
            $('#wrap .screen.controls').css('padding-top', '17px').append('<p>error: ' + errorThrown + '</p>');
        }});
    }
};
aplayer.base.complete_playlist = function () {
    $.each(aplayer.vars.playlist, function (i, item) {
        if (!item.release) {
            $.get(item.resource_uri, function (data) {
                item.release = data.release;
                item.artist = data.artist;
                console.log('got data:', data)
                aplayer.vars.playlist[i] = el;
                aplayer.ui.playlist_display(aplayer, $('#aplayer_playlist'));
            })
        }
    });
}
aplayer.base.set_playlist = function (media) {
    console.log('setting playlist to:', media);
    playlist = media;
    aplayer.vars.playlist = aplayer.vars.playlist || [];
    if (aplayer.vars.mode == 'replace') {
        aplayer.vars.playlist = playlist;
    }
    if (aplayer.vars.mode == 'queue') {
        aplayer.vars.playlist = aplayer.vars.playlist.concat(playlist);
        aplayer.base.prev_next(aplayer.states.current);
    }
    if (aplayer.vars.mode == 'replace') {
        aplayer.base.controls({action: 'play', index: aplayer.vars.offset, force_seek: aplayer.vars.force_seek});
    }
    aplayer.vars.uuid_map = new Array();
    for (i in aplayer.vars.playlist) {
        item = aplayer.vars.playlist[i];
        aplayer.vars.uuid_map[item.uuid] = i;
    }
    aplayer.base.debug('done - aplayer.base.set_playlist()');
    aplayer.ui.playlist_display(aplayer, $('#aplayer_playlist'));
};
aplayer.base.play_in_popup = function (uri, token, offset, mode, force_seek, source) {
    if (mode === undefined) {
        mode = "replace";
    }
    if (offset === undefined) {
        offset = 0;
    }
    if (force_seek === undefined) {
        force_seek = false;
    }
    if (source === undefined) {
        source = 'alibrary';
    }
    if (aplayer.vars.debug) {
        console.log('aplayer.base.play_in_popup() | uri, token, offset, mode, force_seek');
        console.log(uri, token, offset, mode, force_seek);
    }
    var play = {uri: uri, token: token, offset: offset, mode: mode, force_seek: force_seek, source: source};
    local.play = play;
    aplayer.base.grab_player(false);
};
aplayer.base.grab_player = function (focus) {
    this.aplayer = false;
    if (typeof(local.aplayer) != 'undefined') {
        this.aplayer = local.aplayer;
        this.aplayer.base.ready();
    } else {
        if (aplayer.vars.debug) {
            console.log('found no player. create the popup or try to attach');
        }
        aplayer.base.lock_popup(2000);
        var aplayer_win = window.open('', 'aplayer', 'width=' + 400 + ', height=' + 800);
        if (aplayer_win) {
            local.aplayer_win = aplayer_win;
            aplayer_win.opener = window;
            if (typeof(aplayer_win.aplayer) == 'undefined') {
                aplayer_win.location.href = '/player/popup/';
            } else {
                this.aplayer = aplayer_win.aplayer;
                this.aplayer.base.ready();
            }
        } else {
            var message = 'Unable to open the Player-window. Please set your browser to allow popups from this site.';
            alert(message);
        }
    }
    if (focus) {
        try {
            local.aplayer_win.focus();
        } catch (err) {
        }
        ;
    }
    return this.aplayer;
};
aplayer.base.remote_player_ready = function (remote_aplayer) {
    local.aplayer = remote_aplayer;
    local.aplayer.base.load(local.play);
};
aplayer.base.release_remote_player = function () {
    try {
        delete local.aplayer;
    }
    catch (err) {
    }
    ;
    aplayer.base.stop_polling();
    aplayer.ui.reset();
};
aplayer.base.interval = function () {
    if (local.type == 'popup') {
        var states = aplayer.states;
        if (aplayer.backend == 'jwp') {
            states.position = aplayer.player.getPosition();
            states.duration = Math.round(aplayer.player.getDuration());
            try {
                states.state = aplayer.player.getState().toLowerCase();
            } catch (err) {
                states.state = 'unknown';
            }
            ;
            states.buffer = aplayer.player.getBuffer();
        }
        states.position_rel = (((states.position + 1.4) / states.duration) * 100);
        states.total_tracks = aplayer.vars.playlist.length;
        aplayer.states_last = aplayer.states;
        aplayer.states = states;
        aplayer.ui.update(aplayer);
        try {
            parent_win.aplayer.ui.update(aplayer);
            if (parent_win.local.aplayer_updated === undefined) {
                parent_win.local.aplayer_updated = 0;
            }
            parent_win.local.aplayer_updated += 1;
            if (!parent_win.local.timer) {
                parent_win.aplayer.base.start_polling(2000);
            }
        }
        catch (err) {
        }
        ;
        try {
        }
        catch (err) {
        }
        ;
    }
    if (local.type == 'main') {
        if (local.aplayer_updated < 1) {
            aplayer.base.release_remote_player();
        }
        local.aplayer_updated = 0;
    }
};
aplayer.base.prev_next = function (index, uuid) {
    if (index === undefined) {
        var index = 0;
    }
    aplayer.states.current = index;
    aplayer.states.uuid = uuid;
    if (index > 0) {
        aplayer.states.prev = index - 1;
    } else {
        aplayer.states.prev = false;
    }
    if (index < (aplayer.vars.playlist.length - 1)) {
        aplayer.states.next = index + 1;
    } else {
        aplayer.states.next = false;
    }
};
aplayer.base.on_play = function (index, uuid) {
    if (uuid === undefined) {
        var uuid = false;
    }
    aplayer.base.prev_next(index, uuid);
};
aplayer.base.on_complete = function () {
    if (aplayer.states.next) {
        aplayer.base.controls({action: 'play', index: aplayer.states.next});
    }
};
aplayer.base.subscribe_channel_data = function (channel) {
    console.log('aplayer.base.subscribe_channel_data: ', channel)
    try {
        aplayer.vars.playlist[aplayer.states.current].media = {name: 'loading'}
    } catch (e) {
    }
    aplayer.base.update_channel_data(channel);
    pushy.subscribe(channel.resource_uri, function (data) {
        console.log('pushy callbackk with data:', data);
        aplayer.base.update_channel_data(channel);
    });
}
aplayer.base.unsubscribe_channel_data = function () {
    console.log('aplayer.base.unsubscribe_channel_data: ')
}
aplayer.base.update_channel_data = function (channel) {
    console.log('aplayer.base.update_channel_data: ', channel)
    $.get(channel.resource_uri, function (data) {
        console.log('ON-AIR', data.on_air)
        var on_air = data.on_air;
        var media;
        var emission;
        if (on_air.item) {
            $.get(on_air.item, function (media) {
                console.log('media on air:', media)
                aplayer.vars.playlist[aplayer.states.current].media = media;
                aplayer.ui.screen_display(aplayer.states.current);
            })
        }
        if (on_air.emission) {
            setTimeout(function () {
                $.get(on_air.emission, function (data) {
                    console.log('emission on air:', data)
                    aplayer.vars.playlist[aplayer.states.current].emission = emission;
                    aplayer.ui.screen_display(aplayer.states.current);
                    aplayer.ui.update_emission(data);
                })
            }, 500);
        }
    });
}
aplayer.base.controls = function (args) {
    console.log('aplayer.base.controls:', args);
    var action = args.action || false;
    var index = args.index || false;
    if (args.index === undefined) {
        var index = false;
    } else {
        var index = args.index;
    }
    var uuid = args.uuid || false;
    var position = args.position || false;
    var fast_polling = false;
    var update_ui = false;
    aplayer.base.stop_polling();
    if (aplayer.backend == 'jwp') {
        var jwp = aplayer.player;
    }
    if (action == 'pause') {
        if (aplayer.states.state != 'playing') {
            fast_polling = true;
        }
        jwp.pause();
    }
    if (action == 'stop') {
        jwp.stop();
        fast_polling = false;
        update_ui = true;
    }
    if (action == 'play' && index !== false) {
        var stream;
        aplayer.base.unsubscribe_channel_data();
        if (aplayer.vars.source && aplayer.vars.source == 'alibrary') {
            stream = aplayer.vars.playlist[index].stream;
            console.log('stream:', stream);
            var el = aplayer.vars.playlist[index]
            var idx = index;
            console.log('ELEMENT:', aplayer.vars.playlist[index])
        }
        if (aplayer.vars.source && aplayer.vars.source == 'abcast') {
            var channel = aplayer.vars.playlist[index]
            stream = channel.stream;
            console.log('channel:', channel);
            console.log('stream:', stream);
            aplayer.base.subscribe_channel_data(channel);
        }
        setTimeout(function () {
            aplayer.ui.screen_display(index);
        }, 2000)
        if (aplayer.vars.stream_mode == 'rtmp') {
            var pl = {'file': stream.file + '?peter&muster', 'streamer': stream.rtmp_host + stream.rtmp_app + '/', 'title': stream.media_name, 'mediaid': stream.uuid, 'index': index}
            aplayer.base.debug('mode: ' + 'rtmp');
            aplayer.base.debug('file: ' + stream.file);
            aplayer.base.debug('streamer: ' + stream.rtmp_host + stream.rtmp_app + '/');
            aplayer.base.debug('title: ' + stream.media_name);
            aplayer.base.debug('mediaid: ' + stream.uuid);
            aplayer.base.debug('index: ' + index);
        }
        if (aplayer.vars.stream_mode == 'html5') {
            var pl = {'file': stream.uri, 'title': stream.media_name, 'mediaid': stream.uuid, 'index': index}
            aplayer.base.debug('mode: ' + 'html5');
            aplayer.base.debug('uri: ' + stream.uri);
        }
        jwprun = jwp.stop().load(pl).play();
        if (args.force_seek) {
            jwp.seek(args.force_seek);
        }
        fast_polling = true;
        update_ui = true;
    }
    if (action == 'seek' && position) {
        var p = aplayer.states.duration;
        p = p / 100 * position;
        if (uuid && uuid == aplayer.states.uuid) {
            jwp.seek(p);
            fast_polling = true;
            update_ui = true;
        } else if (uuid) {
            var new_index = aplayer.vars.uuid_map[uuid];
            aplayer.base.controls({action: 'play', index: aplayer.vars.uuid_map[uuid]});
            fast_polling = true;
            update_ui = true;
        } else {
            var vc = aplayer.player.getVolume();
            var vc = 80;
            for (var v = vc; v > 0; v -= 3) {
                aplayer.player.setVolume(v)
            }
            jwp.seek(p);
            for (var v = 0; v < vc; v += 3) {
                aplayer.player.setVolume(v)
            }
            fast_polling = true;
            update_ui = true;
        }
        if (uuid) {
        } else {
            uuid = aplayer.states.uuid;
        }
    }
    if (fast_polling) {
        aplayer.base.start_polling();
    } else {
        aplayer.base.start_polling(2000);
    }
    if (update_ui) {
        aplayer.ui.playlist_display(aplayer, $('#aplayer_playlist'));
        if (index !== false) {
            aplayer.ui.screen_display(index);
        }
    }
    aplayer.base.log(action, index, uuid);
    aplayer.base.interval();
};
aplayer.controls = function (action, index, uuid) {
    var jwp = aplayer.player;
    if (aplayer.timer) {
        clearInterval(aplayer.timer);
    }
    switch (action) {
        case'play':
            var stream = aplayer.vars.playlist[index].stream;
            jwp.stop();
            var tpl = {'file': stream.file, 'streamer': stream.rtmp_host + stream.rtmp_app + '/', 'title': stream.media_name, 'mediaid': stream.uuid, 'index': index}
            jwp.load(tpl).play();
            aplayer.timer = setInterval("aplayer.interval()", aplayer.vars.len_interval);
            aplayer.ui.screen_display(index);
            break;
        case'pause':
            jwp.pause();
            break;
        case'stop':
            jwp.stop();
            break;
        case'next':
            jwp.pause();
            break;
        case'seek':
            jwp.pause();
            break;
        case'seek_p':
            var p = aplayer.vars.states.duration;
            p = p / 100 * index;
            jwp.seek(p);
            aplayer.timer = setInterval("aplayer.interval()", aplayer.vars.len_interval);
            break;
        case'seek_by_uuid':
            var p = aplayer.vars.states.duration;
            p = p / 100 * index;
            var current_uuid = aplayer.vars.playlist[aplayer.vars.states.current].uuid;
            if (uuid == current_uuid) {
                jwp.seek(p);
            } else {
                var new_index = aplayer.vars.uuid_map[uuid];
                aplayer.controls('play', new_index);
                aplayer.controls('seek_p', index);
            }
            aplayer.timer = setInterval("aplayer.interval()", aplayer.vars.len_interval);
            break;
        default:
            break;
    }
    aplayer.base.log(action, index, uuid);
    aplayer.interval();
};
aplayer.on_playlist = function (event) {
    var uuid = event.playlist[0].mediaid;
    var index = parseFloat(event.playlist[0].index);
    aplayer.vars.states.current = index;
    if (index > 0) {
        aplayer.vars.states.prev = index - 1;
    } else {
        aplayer.vars.states.prev = false;
    }
    if (index < (aplayer.vars.playlist.length - 1)) {
        aplayer.vars.states.next = index + 1;
    } else {
        aplayer.vars.states.next = false;
    }
};
aplayer.on_complete = function (event) {
    if (aplayer.vars.states.next) {
        aplayer.controls('play', aplayer.vars.states.next);
    }
};
aplayer.base.reload = function (uri, token, offset, mode) {
    if (offset === undefined) {
        offset = 0;
    }
    jwplayer().stop().load({});
    aplayer.base.load(uri, offset, mode);
};
aplayer.interval = function () {
};
aplayer.base.start_polling = function (interval) {
    if (interval === undefined) {
        interval = interval = aplayer.vars.len_interval;
    }
    if (local.timer) {
        clearInterval(local.timer);
    }
    local.timer = setInterval("aplayer.base.interval()", interval);
};
aplayer.base.stop_polling = function () {
    if (local.timer) {
        clearInterval(local.timer);
    }
};
aplayer.base.get_popup_lock = function () {
    if (typeof(local.popup_lock) != 'undefined') {
        return local.popup_lock;
    }
    return false;
};
aplayer.base.lock_popup = function (time) {
    if (time === undefined) {
        time = 3000;
    }
    local.popup_lock = true;
    setTimeout("aplayer.base.unlock_popup()", time);
    return time;
};
aplayer.base.unlock_popup = function () {
    local.popup_lock = false;
    return true;
};
aplayer.base.log = function (action, index, uuid) {
    try {
        var item = aplayer.vars.playlist[aplayer.vars.states.current];
        var log_value = false;
        if (action == 'seek_by_uuid') {
            log_value = Math.round(index);
        }
        var log_string = item.name + ' - ' + item.artist.name;
    } catch (err) {
        var log_string = uuid;
    }
    ;
};
aplayer.base.debug = function (text) {
    var d = new Date();
    var hour = d.getHours();
    var min = d.getMinutes();
    var sec = d.getSeconds();
    var time = hour + ':' + min + ':' + sec;
    try {
        console.log(text);
    } catch (err) {
    }
    ;
};
var aplayer = aplayer || {};
aplayer.ui = aplayer.ui || {};
aplayer.ui.player = aplayer.ui.player || {};
aplayer.ui.use_effects = true;
aplayer.ui.init = function () {
    aplayer.ui.bind();
};
aplayer.ui.bind = function () {
    $('.___playable.popup').live('click', function (e) {
        e.preventDefault();
        var ct = $(this).data('ct');
        var action = $(this).attr('href').split('#');
        console.log('action: ', action)
        var uri = action[0];
        var offset = action[1];
        var mode = action[2];
        var token = 'xx-yy-zz';
        var source = 'alibrary';
        if (ct == 'media_set') {
            var item_ids = [];
            var item_id = $(this).parents('.item').data('item_id');
            var container = $(this).parents('.container');
            $('.item.media', container).each(function (i, el) {
                var current_id = $(el).data('item_id');
                if (current_id == item_id) {
                    offset = i;
                }
                item_ids.push(current_id)
            })
            uri = '/api/v1/library/track/?id__in=' + item_ids.join(',')
        }
        aplayer.base.play_in_popup(uri, token, offset, mode, false, source);
    });
    $('.___streamable.popup').live('click', function (e) {
        e.preventDefault();
        var resource_uri = $(this).data('resource_uri');
        console.log(resource_uri);
        var action = $(this).attr('href').split('#');
        var uri = resource_uri;
        var offset = 0;
        var mode = 'replace';
        var token = 'xx-yy-zz';
        var source = 'abcast';
        aplayer.base.play_in_popup(uri, token, offset, mode, false, source);
        return false;
    });
    $('body').on('click', '.playable.popup:not(".disabled")', function (e) {
        e.preventDefault();
        var ct = $(this).data('ct');
        var uri = $(this).data('resource_uri');
        var offset = $(this).data('offset');
        var mode = $(this).data('mode');
        var token = 'xx-yy-zz';
        var source = 'alibrary';
        if (ct == 'media_set') {
            var item_ids = [];
            var item_id = $(this).parents('.item').data('item_id');
            var container = $(this).parents('.container');
            $('.item.media', container).each(function (i, el) {
                var current_id = $(el).data('item_id');
                if (current_id == item_id) {
                    offset = i;
                }
                item_ids.push(current_id)
            })
            uri = '/api/v1/library/track/?id__in=' + item_ids.join(',');
        }
        aplayer.base.play_in_popup(uri, token, offset, mode, false, source);
    });
    $('body').on('click', '.streamable.popup:not(".disabled")', function (e) {
        e.preventDefault();
        var uri = $(this).data('resource_uri');
        var offset = 0;
        var mode = 'replace';
        var token = 'xx-yy-zz';
        var source = 'abcast';
        aplayer.base.play_in_popup(uri, token, offset, mode, false, source);
    });
    $('a.cuepoint', '.content').live('click', function (e) {
        e.preventDefault();
        var container = $(this).parents('.cms_plugin');
        var action = $('.info a', $('.item', container)).attr('href').split('#');
        var uri = action[0];
        var offset = action[1];
        var mode = action[2];
        var token = 'xx-yy-zz';
        var seek = $(this).attr('href').substring(1);
        var force_seek = seek;
        aplayer.base.play_in_popup(uri, token, offset, mode, force_seek);
    });
    $('a.cuepoint', '.content').live('hover', function (e) {
        e.preventDefault();
        var container = $(this).parents('.cms_plugin');
        var playhead = $('> .item', container);
        var duration = parseInt($('.item', container).data('duration') / 1000);
        var seek = parseInt($(this).attr('href').substring(1));
        var relative_position = parseInt(seek / duration * 100);
        $('.handler', playhead).css('background-position', relative_position + '% 0');
        playhead.addClass("hover");
    });
    $('a.cuepoint', '.content').live('mouseleave', function (e) {
        e.preventDefault();
        var container = $(this).parents('.cms_plugin');
        var playhead = $('> .item', container);
        playhead.removeClass("hover");
    });
    $("a.parent_link").live('click', function (e) {
        var href = $(this).attr('href');
        parent_win.location.href = href;
        return false;
    });
    $("#aplayer_playlist div.listing.item").live('click', function (e) {
        var id = $(this).attr('id');
        id = id.split('_')[2];
        if ($(this).hasClass('active')) {
            aplayer.controls('pause');
        } else {
            aplayer.controls('play', id);
        }
    });
    $('.playlist .item.playlist').live('click', function (e) {
        var uuid = $(this).attr('id');
        try {
            var index = aplayer.vars.uuid_map[uuid];
        } catch (e) {
            var index = 0;
        }
        var args = {action: 'play', index: index}
        aplayer.base.controls(args)
    });
    aplayer.ui.bind_controls($("div.aplayer-controls li > a", '.aplayer'));
    $('#aplayer_mode', $('footer')).html(aplayer.vars.stream_mode)
    $('#aplayer_version', $('footer')).html(aplayer.vars.version)
    $('#aplayer_volume', $('footer')).noUiSlider({range: [0, 100], start: 80, step: 1, handles: 1, connect: 'lower', slide: function () {
        var values = $(this).val();
        aplayer.player.setVolume(values)
    }});
    aplayer.ui.rebind();
};
aplayer.ui.rebind = function () {
    $(document).bind('keydown.modal', function (event) {
        switch (event.which) {
            case 32:
                aplayer.base.controls({action: 'pause'});
                break;
            case 39:
                if (aplayer.states.next) {
                    aplayer.base.controls({action: 'play', index: aplayer.states.next});
                }
                break;
            case 37:
                if (aplayer.states.prev !== false) {
                    aplayer.base.controls({action: 'play', index: aplayer.states.prev});
                }
                break;
        }
    });
};
aplayer.ui.bind_controls = function (obj) {
    obj.live('click', function (e) {
        e.preventDefault();
        aplayer = local.aplayer;
        var action = $(this).attr('href').substring(1);
        if (action == 'pause') {
            aplayer.base.controls({action: 'pause'});
        }
        if (action == 'play' && aplayer.states.state) {
            aplayer.base.controls({action: 'pause'});
        }
        if (action == 'next') {
            if (aplayer.states.next) {
                aplayer.base.controls({action: 'play', index: aplayer.states.next});
            }
        }
        if (action == 'prev') {
            if (aplayer.states.prev !== false) {
                aplayer.base.controls({action: 'play', index: aplayer.states.prev});
            }
        }
    });
    $('.indicator .wrapper', 'body.popup #progress_bar').live('click', function (e) {
        outer_width = $(this).css('width').slice(0, -2);
        base_width = outer_width;
        var pos = util.get_position(e);
        var x_percent = pos['x'] / (base_width) * 100;
        var uuid = $(this).parents('.item').attr('id');
        var args = {action: 'seek', position: x_percent, uuid: uuid}
        aplayer.base.controls(args);
    });
    $('.indicator .wrapper', 'body.popup #progress_bar').live('mousemove', function (e) {
        var pos = util.get_position(e);
        $(this).css('background-position', pos['x'] + 'px' + ' 0px');
    });
};
aplayer.ui.update = function (aplayer) {
    local.aplayer = aplayer;
    this.type = local.type;
    this.state_changed = (aplayer.states.state != aplayer.states_last.state);
    this.media_changed = (aplayer.states.uuid != aplayer.states_last.uuid);
    var media = false;
    if (aplayer.vars.source && aplayer.vars.source == 'alibrary') {
        media = aplayer.vars.playlist[aplayer.states.current];
    }
    if (aplayer.vars.source && aplayer.vars.source == 'abcast') {
        var channel = aplayer.vars.playlist[aplayer.states.current];
        if (!channel.media) {
            console.log('no channel media available.');
        } else {
            media = channel.media;
        }
    }
    if (media) {
        $('div.item.playlist').not('div.item.playlist.' + media.uuid).removeClass('active playing');
        $('div.item.playlist.' + media.uuid).addClass('active playing');
        $('div.listview.medias .item').not('div.item.playlist.' + media.uuid).removeClass('active playing');
        $('div.listview.medias .item.' + media.uuid).addClass('active playing');
        var container = $('div.aplayer.inline');
        var active_playhead = $('.playhead .indicator', container_screen);
        if (active_playhead.html()) {
            outer_width = active_playhead.css('width');
            try {
                base_width = outer_width.slice(0, -2);
            } catch (err) {
                base_width = 700;
            }
            ;
            active_playhead.css('background-position', (aplayer.states.position_rel * base_width / 100) + 'px' + ' 0px');
        }
        var body = $('body');
        $('body').addClass('aplayer-active');
        $('div.content.aplayer').addClass('active');
        body.removeClass('buffering playing paused idle');
        body.addClass(aplayer.states.state);
        if (window.aplayer.inline) {
            if (!window.aplayer.inline.player) {
                window.aplayer.inline.player = aplayer;
            }
            window.aplayer.inline.update(aplayer, media);
        }
        ;
        if (window.detail_player != undefined) {
            window.detail_player.update(aplayer);
        }
        var container_screen = $('#progress_bar');
        if (container_screen) {
            $('div.time-current > span', container_screen).html(util.format_time(aplayer.states.position));
            $('div.time-total > span', container_screen).html(util.format_time(aplayer.states.duration));
            $('.indicator .inner', '.item.playlist.playing').css('width', aplayer.states.position_rel + '%');
        }
        if (this.type == 'popup') {
        }
    }
};
aplayer.ui.screen_display = function (index) {
    if (aplayer.vars.playlist[index].media) {
        var item = aplayer.vars.playlist[index].media;
        item.source = 'abcast';
    } else {
        var item = aplayer.vars.playlist[index];
        item.source = 'alibrary';
    }
    try {
        item.images = []
        item.images.push(item.release.main_image);
    } catch (err) {
    }
    ;
    var html = nj.render('aplayer/nj/popup_screen.html', {object: item});
    $("#aplayer_screen").html(html);
};
aplayer.ui.update_emission = function (data) {
    console.log('update_emission - data:', data)
    var html = nj.render('aplayer/nj/popup_emission.html', {object: data});
    $("#aplayer_emission").html(html);
}
aplayer.ui.playlist_display = function (aplayer, target) {
    target.html('');
    var media_listing = new Array();
    for (x in aplayer.vars.playlist) {
        var media = aplayer.vars.playlist[x];
        var media_name = 'unknown';
        var artist_name = 'unknown';
        if (media.name) {
            media_name = media.name;
        }
        if (media.artist) {
            artist_name = media.artist.name;
        }
        media_listing[x] = {media: media, name: media.name, };
        media.formated_duration = util.format_time(Number(media.duration / 1000))
        var html = ich.tpl_media({'media': media});
        target.append(html);
    }
    ;
};
aplayer.ui.scale_waveform = function (direction) {
    var waveform = $('.playhead .waveform');
    var height = parseFloat(waveform.css('height').slice(0, -2));
    switch (direction) {
        case'up':
            waveform.css('height', (height + 5) + 'px');
            break;
        case'down':
            waveform.css('height', (height - 5) + 'px');
            break;
    }
};
aplayer.ui.hide_overlay = function () {
    $('#overlay_container').hide();
};
aplayer.ui.reset = function () {
    if (window.aplayer.inline) {
        window.aplayer.inline.reset();
    }
    ;
};
aplayer.ui.playhead = function (base_width) {
    if (base_width === undefined) {
        base_width = 610;
    }
    $('.playhead .handler').live('mousemove', function (e) {
        var pos = util.get_position(e);
        $(this).css('background-position', pos['x'] + 'px' + ' 0px');
    });
    $('.playhead .handler', 'body.popup').live('click', function (e) {
        outer_width = $(this).parents('.playhead').css('width').slice(0, -2);
        base_width = outer_width;
        var pos = util.get_position(e);
        var x_percent = pos['x'] / (base_width) * 100;
        var uuid = $(this).parents('.item').attr('id');
        var args = {action: 'seek', position: x_percent, uuid: uuid}
        aplayer.base.controls(args);
    });
    $('.playhead .handler', 'body.base').live('click', function (e) {
        outer_width = $(this).parents('.playhead').css('width').slice(0, -2);
        base_width = outer_width;
        var pos = util.get_position(e);
        var x_percent = pos['x'] / (base_width) * 100;
        var uuid = $(this).parents('.item').attr('id');
        try {
            var is_loaded = (uuid in local.aplayer.vars.uuid_map)
        }
        catch (err) {
            var is_loaded = false;
        }
        ;
        if (typeof(local.aplayer) != 'undefined' && is_loaded == true) {
            var args = {action: 'seek', position: x_percent, uuid: uuid}
            local.aplayer.base.controls(args);
        }
        else {
            var action = $('.info a', $(this).parents('.item')).attr('href').split('#');
            var uri = action[0];
            var offset = action[1];
            var mode = action[2];
            var token = 'xx-yy-zz';
            aplayer.base.play_in_popup(uri, token, offset, mode);
        }
    });
    var loaded = 0;
    var num_images = $("img", '.playhead .waveform').length;
    $('img', '.playhead .waveform').one('load',function () {
        ++loaded;
        if (loaded === num_images) {
            $('div.playhead').removeClass('loading');
        }
        ;
    }).each(function () {
        if (this.complete)
            $(this).load();
    });
};
AplayerApp = function (context) {
    var self = this;
    this.version = '0.2.17b';
    this.stream_mode = 'html5';
    this.loaded = true;
    this.states = {current: 0, next: false, prev: false};
    this.interval_duration = 500;
    this.container_id = 'aplayer_container';
    this.player;
    this.context = context;
    var vars = {swf_url: ''};
    this.init = function () {
        console.log('AplayerApp: init');
        if (self.context == 'main') {
            self.init_main();
            self.bindings_main();
        }
        if (self.context == 'popup') {
            self.init_popup();
            self.bindings_popup();
        }
    };
    this.init_main = function () {
        console.log('AplayerApp: init_main');
    };
    this.init_popup = function () {
        console.log('AplayerApp: init_popup');
        self.player = JWP(self);
    };
    this.bindings_main = function () {
        $('body').on('click', '.playable.popup:not(".disabled")', function (e) {
            e.preventDefault();
            var ct = $(this).data('ct');
            var uri = $(this).data('resource_uri');
            var offset = $(this).data('offset');
            var mode = $(this).data('mode');
            var token = 'xx-yy-zz';
            var source = 'alibrary';
            if (ct == 'media_set') {
                var item_ids = [];
                var item_id = $(this).parents('.item').data('item_id');
                var container = $(this).parents('.container');
                $('.item.media', container).each(function (i, el) {
                    var current_id = $(el).data('item_id');
                    if (current_id == item_id) {
                        offset = i;
                    }
                    item_ids.push(current_id)
                })
                uri = '/api/v1/library/track/?id__in=' + item_ids.join(',');
            }
            aplayer.base.play_in_popup(uri, token, offset, mode, false, source);
        });
        $('body').on('click', '.streamable.popup:not(".disabled")', function (e) {
            e.preventDefault();
            var uri = $(this).data('resource_uri');
            var offset = 0;
            var mode = 'replace';
            var token = 'xx-yy-zz';
            var source = 'abcast';
            aplayer.base.play_in_popup(uri, token, offset, mode, false, source);
        });
    };
    this.bindings_popup = function () {
    };
    this.update = function (aplayer, media) {
    };
    this.events = {classes: ['playing', 'paused'], play: function () {
        console.log('events: ', 'play');
        self.dom_element.removeClass('paused');
        self.dom_element.addClass('playing');
    }, stop: function () {
        console.log('events: ', 'stop');
        self.dom_element.removeClass('paused');
        self.dom_element.removeClass('playing');
        self.el_indicator.attr({x: -10})
    }, pause: function () {
        console.log('events: ', 'pause');
        self.dom_element.removeClass('playing');
        self.dom_element.addClass('paused');
    }, resume: function () {
        console.log('events: ', 'resume');
        self.dom_element.removeClass('paused');
        self.dom_element.addClass('playing');
    }, finish: function () {
        console.log('events: ', 'finish');
        self.dom_element.removeClass('paused');
        self.dom_element.removeClass('playing');
    }}
}
JWP = function (aplayer) {
    try {
        jwplayer(aplayer.container_id).remove();
    } catch (e) {
        debug.debug(e)
    }
    return jwplayer(container).setup({id: container, flashplayer: aplayer.vars.swf_url, height: 10, width: 610, repeat: false, rtmp: {bufferlength: 1.0, securetoken: "Kosif093n203a"}, events: {onReady: function () {
    }, onPlaylist: function (event) {
    }, onComplete: function (event) {
    }}, modes: [
        {type: 'flash', src: aplayer.vars.swf_url},
        {type: 'html5'}
    ], });
}
InlinePlayer = function () {
    var self = this;
    this.item;
    this.dom_id = 'aplayer_inline';
    this.dom_element;
    this.player;
    this.state = false;
    this.source = false;
    this.current_uuid = false;
    this.current_media = false;
    this.init = function () {
        self.dom_element = $('#' + self.dom_id);
        debug.debug('InlinePlayer: init');
        self.bindings();
    };
    this.bindings = function () {
        debug.debug('InlinePlayer: bindings');
        var timeout;
        $(self.dom_element).on('mouseover', 'div.display', function () {
            self.dom_element.addClass('hover');
            self.display_listing();
        });
        $(self.dom_element).on('mouseover', function () {
            if (timeout) {
                window.clearTimeout(timeout);
            }
        });
        $(self.dom_element).on('mouseleave', function () {
            self.dom_element.removeClass('hover');
            timeout = window.setTimeout(function () {
                if (!$('.popup-select-playlist').length) {
                    self.hide_listing();
                }
            }, 300)
        });
        $(self.dom_element).on('click', 'a[data-action]', function (e) {
            e.preventDefault();
            var action = $(this).data('action');
            console.log('action', action);
            if (action == 'pause') {
                self.player.base.controls({action: 'pause'});
            }
            if (action == 'play' && self.player.states.state) {
                self.player.base.controls({action: 'pause'});
            }
            if (action == 'next') {
                if (self.player.states.next) {
                    self.player.base.controls({action: 'play', index: self.player.states.next});
                }
            }
            if (action == 'prev') {
                if (self.player.states.prev !== false) {
                    self.player.base.controls({action: 'play', index: self.player.states.prev});
                }
            }
        });
        $(self.dom_element).on('click', '.listing .item', function (e) {
            if ($(e.target).is("a") || $(e.target).is("i")) {
            } else {
                var uuid = $(this).attr('id');
                var index = self.player.vars.uuid_map[uuid]
                var args = {action: 'play', index: index}
                self.player.base.controls(args)
            }
        });
        $(self.dom_element).on('mousemove', '.playhead .handler', function (e) {
            var pos = util.get_position(e);
            $(this).css('background-position', pos['x'] + 'px' + ' 0px');
        });
        $(self.dom_element).on('click', '.playhead .handler', function (e) {
            outer_width = $(this).css('width').slice(0, -2);
            base_width = outer_width;
            var pos = util.get_position(e);
            var x_percent = pos['x'] / (base_width) * 100;
            var uuid = $(this).parents('.item').attr('id');
            var args = {action: 'seek', position: x_percent, uuid: uuid}
            self.player.base.controls(args);
        });
    };
    this.display_listing = function () {
        var container = $('.listing', self.dom_element);
        var container_listing = $('.inner', container);
        container_listing.html('');
        container.show();
        if (self.player && self.source == 'alibrary') {
            var playlist = self.player.vars.playlist;
            $.each(playlist, function (i, item) {
                var html = nj.render('aplayer/nj/inline_player_item.html', {object: item});
                container_listing.append(html);
            });
        }
        if (self.player && self.source == 'abcast') {
            var html = nj.render('aplayer/nj/inline_player_item.html', {object: self.current_media});
            container_listing.append(html);
        }
    };
    this.hide_listing = function () {
        var container = $('.listing', self.dom_element);
        container.fadeOut(100);
    };
    this.update = function (aplayer, media) {
        var container = self.dom_element;
        var states = aplayer.states;
        if (self.state !== states.state) {
            console.log('state changed');
            self.state = states.state;
            self.current_media = media;
            self.update_state();
        }
        if (self.current_uuid !== media.uuid) {
            console.log('media changed');
            self.current_uuid = media.uuid;
            self.update_media();
        }
        if (aplayer.vars.source) {
            self.source = aplayer.vars.source
        }
        if (aplayer.vars.source && aplayer.vars.source == 'alibrary') {
            container.addClass('alibrary');
            container.removeClass('abcast');
            $('li.current', container).html(util.format_time(states.position));
            $('li.total', container).html(util.format_time(states.duration));
            $('ul.timing', container).fadeIn(500);
            $('.media_name a', container).html(media.name);
            $('.media_name a', container).attr('href', media.absolute_url);
            $('.listing .inner .indicator', container).css('width', states.position_rel + '%');
        }
        if (aplayer.vars.source && aplayer.vars.source == 'abcast') {
            container.addClass('abcast');
            container.removeClass('alibrary');
            $('li.current', container).html('');
            $('li.total', container).html('');
            $('ul.timing', container).hide();
            $('.media_name a', container).html(media.name);
            $('.media_name a', container).attr('href', media.absolute_url);
            $('.listing .inner .indicator', container).css('width', '0%');
        }
    };
    this.update_state = function () {
        self.dom_element.removeClass();
        self.dom_element.addClass(self.state);
    }
    this.update_media = function () {
        console.log('self.current_media', self.current_media)
        $('.playhead .waveform img').attr('src', self.current_media.waveform_image);
    }
    this.reset = function () {
        debug.debug('InlinePlayer: reset');
        var container = self.dom_element;
        $('.media_name a').html('&nbsp;');
        $('.artist_name a').html('&nbsp;');
        $('.release_name a').html('&nbsp;');
        $('ul.timing', container).fadeOut(500);
    };
    this.events = {classes: ['playing', 'paused'], play: function () {
        console.log('events: ', 'play');
        self.dom_element.removeClass('paused');
        self.dom_element.addClass('playing');
    }, stop: function () {
        console.log('events: ', 'stop');
        self.dom_element.removeClass('paused');
        self.dom_element.removeClass('playing');
        self.el_indicator.attr({x: -10})
    }, pause: function () {
        console.log('events: ', 'pause');
        self.dom_element.removeClass('playing');
        self.dom_element.addClass('paused');
    }, resume: function () {
        console.log('events: ', 'resume');
        self.dom_element.removeClass('paused');
        self.dom_element.addClass('playing');
    }, finish: function () {
        console.log('events: ', 'finish');
        self.dom_element.removeClass('paused');
        self.dom_element.removeClass('playing');
    }}
}
var aplayer = aplayer || {};
var player_app = player_app || {};
$(function () {
    aplayer.inline = new InlinePlayer();
    aplayer.inline.init();
});
var Dajaxice = {alibrary: {provider_update: function (callback_function, argv, custom_settings) {
    Dajaxice.call('alibrary.provider_update', 'POST', callback_function, argv, custom_settings);
}, merge_items: function (callback_function, argv, custom_settings) {
    Dajaxice.call('alibrary.merge_items', 'POST', callback_function, argv, custom_settings);
}, api_lookup: function (callback_function, argv, custom_settings) {
    Dajaxice.call('alibrary.api_lookup', 'POST', callback_function, argv, custom_settings);
}, provider_search: function (callback_function, argv, custom_settings) {
    Dajaxice.call('alibrary.provider_search', 'POST', callback_function, argv, custom_settings);
}, provider_search_query: function (callback_function, argv, custom_settings) {
    Dajaxice.call('alibrary.provider_search_query', 'POST', callback_function, argv, custom_settings);
}}, importer: {get_import: function (callback_function, argv, custom_settings) {
    Dajaxice.call('importer.get_import', 'POST', callback_function, argv, custom_settings);
}}, get_cookie: function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].toString().replace(/^\s+/, "").replace(/\s+$/, "");
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}, call: function (dajaxice_function, method, dajaxice_callback, argv, custom_settings) {
    var custom_settings = custom_settings || {}, error_callback = Dajaxice.get_setting('default_exception_callback');
    if ('error_callback'in custom_settings && typeof(custom_settings['error_callback']) == 'function') {
        error_callback = custom_settings['error_callback'];
    }
    var send_data = 'argv=' + encodeURIComponent(JSON.stringify(argv));
    var oXMLHttpRequest = new XMLHttpRequest;
    oXMLHttpRequest.open(method, '/dajaxice/' + dajaxice_function + '/');
    oXMLHttpRequest.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    oXMLHttpRequest.setRequestHeader("X-CSRFToken", Dajaxice.get_cookie('csrftoken'));
    oXMLHttpRequest.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            if (this.responseText == Dajaxice.EXCEPTION || !(this.status in Dajaxice.valid_http_responses())) {
                error_callback();
            }
            else {
                var response;
                try {
                    response = JSON.parse(this.responseText);
                }
                catch (exception) {
                    response = this.responseText;
                }
                dajaxice_callback(response);
            }
        }
    }
    oXMLHttpRequest.send(send_data);
    return oXMLHttpRequest;
}, setup: function (settings) {
    this.settings = settings;
}, get_setting: function (key) {
    if (this.settings == undefined || this.settings[key] == undefined) {
        return Dajaxice.default_settings[key];
    }
    return this.settings[key];
}, valid_http_responses: function () {
    return{200: null, 301: null, 302: null, 304: null}
}, EXCEPTION: 'DAJAXICE_EXCEPTION', default_settings: {'default_exception_callback': function () {
    console.log('Dajaxice: Something went wrong.')
}}};
window['Dajaxice'] = Dajaxice;
(function () {
    function n() {
        this._object = h && !p ? new h : new window.ActiveXObject("Microsoft.XMLHTTP");
        this._listeners = []
    }

    function a() {
        return new n
    }

    function j(b) {
        a.onreadystatechange && a.onreadystatechange.apply(b);
        b.dispatchEvent({type: "readystatechange", bubbles: !1, cancelable: !1, timeStamp: new Date + 0})
    }

    function o(b) {
        try {
            b.responseText = b._object.responseText
        } catch (a) {
        }
        try {
            var d;
            var g = b._object, c = g.responseXML, f = g.responseText;
            i && (f && c && !c.documentElement && g.getResponseHeader("Content-Type").match(/[^\/]+\/[^\+]+\+xml/)) && (c = new window.ActiveXObject("Microsoft.XMLDOM"), c.async = !1, c.validateOnParse = !1, c.loadXML(f));
            d = c && (i && 0 !== c.parseError || !c.documentElement || c.documentElement && "parsererror" == c.documentElement.tagName) ? null : c;
            b.responseXML = d
        } catch (h) {
        }
        try {
            b.status = b._object.status
        } catch (k) {
        }
        try {
            b.statusText = b._object.statusText
        } catch (j) {
        }
    }

    function l(b) {
        b._object.onreadystatechange = new window.Function
    }

    var h = window.XMLHttpRequest, m = !!window.controllers, i = window.document.all && !window.opera, p = i && window.navigator.userAgent.match(/MSIE 7.0/);
    a.prototype = n.prototype;
    m && h.wrapped && (a.wrapped = h.wrapped);
    a.UNSENT = 0;
    a.OPENED = 1;
    a.HEADERS_RECEIVED = 2;
    a.LOADING = 3;
    a.DONE = 4;
    a.prototype.readyState = a.UNSENT;
    a.prototype.responseText = "";
    a.prototype.responseXML = null;
    a.prototype.status = 0;
    a.prototype.statusText = "";
    a.prototype.priority = "NORMAL";
    a.prototype.onreadystatechange = null;
    a.onreadystatechange = null;
    a.onopen = null;
    a.onsend = null;
    a.onabort = null;
    a.prototype.open = function (b, e, d, g, c) {
        delete this._headers;
        arguments.length < 3 && (d = true);
        this._async = d;
        var f = this, h = this.readyState, k = null;
        if (i && d) {
            k = function () {
                if (h != a.DONE) {
                    l(f);
                    f.abort()
                }
            };
            window.attachEvent("onunload", k)
        }
        a.onopen && a.onopen.apply(this, arguments);
        arguments.length > 4 ? this._object.open(b, e, d, g, c) : arguments.length > 3 ? this._object.open(b, e, d, g) : this._object.open(b, e, d);
        this.readyState = a.OPENED;
        j(this);
        this._object.onreadystatechange = function () {
            if (!m || d) {
                f.readyState = f._object.readyState;
                o(f);
                if (f._aborted)f.readyState = a.UNSENT; else if (f.readyState == a.DONE) {
                    delete f._data;
                    l(f);
                    i && d && window.detachEvent("onunload", k);
                    h != f.readyState && j(f);
                    h = f.readyState
                }
            }
        }
    };
    a.prototype.send = function (b) {
        a.onsend && a.onsend.apply(this, arguments);
        arguments.length || (b = null);
        if (b && b.nodeType) {
            b = window.XMLSerializer ? (new window.XMLSerializer).serializeToString(b) : b.xml;
            this._headers["Content-Type"] || this._object.setRequestHeader("Content-Type", "application/xml")
        }
        this._data = b;
        a:{
            this._object.send(this._data);
            if (m && !this._async) {
                this.readyState = a.OPENED;
                for (o(this); this.readyState < a.DONE;) {
                    this.readyState++;
                    j(this);
                    if (this._aborted)break a
                }
            }
        }
    };
    a.prototype.abort = function () {
        a.onabort && a.onabort.apply(this, arguments);
        if (this.readyState > a.UNSENT)this._aborted = true;
        this._object.abort();
        l(this);
        this.readyState = a.UNSENT;
        delete this._data
    };
    a.prototype.getAllResponseHeaders = function () {
        return this._object.getAllResponseHeaders()
    };
    a.prototype.getResponseHeader = function (b) {
        return this._object.getResponseHeader(b)
    };
    a.prototype.setRequestHeader = function (b, a) {
        if (!this._headers)this._headers = {};
        this._headers[b] = a;
        return this._object.setRequestHeader(b, a)
    };
    a.prototype.addEventListener = function (a, e, d) {
        for (var g = 0, c; c = this._listeners[g]; g++)if (c[0] == a && c[1] == e && c[2] == d)return;
        this._listeners.push([a, e, d])
    };
    a.prototype.removeEventListener = function (a, e, d) {
        for (var g = 0, c; c = this._listeners[g]; g++)if (c[0] == a && c[1] == e && c[2] == d)break;
        c && this._listeners.splice(g, 1)
    };
    a.prototype.dispatchEvent = function (a) {
        a = {type: a.type, target: this, currentTarget: this, eventPhase: 2, bubbles: a.bubbles, cancelable: a.cancelable, timeStamp: a.timeStamp, stopPropagation: function () {
        }, preventDefault: function () {
        }, initEvent: function () {
        }};
        a.type == "readystatechange" && this.onreadystatechange && (this.onreadystatechange.handleEvent || this.onreadystatechange).apply(this, [a]);
        for (var e = 0, d; d = this._listeners[e]; e++)d[0] == a.type && !d[2] && (d[1].handleEvent || d[1]).apply(this, [a])
    };
    a.prototype.toString = function () {
        return"[object XMLHttpRequest]"
    };
    a.toString = function () {
        return"[XMLHttpRequest]"
    };
    window.Function.prototype.apply || (window.Function.prototype.apply = function (a, e) {
        e || (e = []);
        a.__func = this;
        a.__func(e[0], e[1], e[2], e[3], e[4]);
        delete a.__func
    });
    window.XMLHttpRequest = a
})();
var JSON;
JSON || (JSON = {});
(function () {
    function k(a) {
        return 10 > a ? "0" + a : a
    }

    function o(a) {
        p.lastIndex = 0;
        return p.test(a) ? '"' + a.replace(p, function (a) {
            var c = r[a];
            return"string" === typeof c ? c : "\\u" + ("0000" + a.charCodeAt(0).toString(16)).slice(-4)
        }) + '"' : '"' + a + '"'
    }

    function m(a, j) {
        var c, d, h, n, g = e, f, b = j[a];
        b && ("object" === typeof b && "function" === typeof b.toJSON) && (b = b.toJSON(a));
        "function" === typeof i && (b = i.call(j, a, b));
        switch (typeof b) {
            case"string":
                return o(b);
            case"number":
                return isFinite(b) ? String(b) : "null";
            case"boolean":
            case"null":
                return String(b);
            case"object":
                if (!b)return"null";
                e += l;
                f = [];
                if ("[object Array]" === Object.prototype.toString.apply(b)) {
                    n = b.length;
                    for (c = 0; c < n; c += 1)f[c] = m(c, b) || "null";
                    h = 0 === f.length ? "[]" : e ? "[\n" + e + f.join(",\n" + e) + "\n" + g + "]" : "[" + f.join(",") + "]";
                    e = g;
                    return h
                }
                if (i && "object" === typeof i) {
                    n = i.length;
                    for (c = 0; c < n; c += 1)"string" === typeof i[c] && (d = i[c], (h = m(d, b)) && f.push(o(d) + (e ? ": " : ":") + h))
                } else for (d in b)Object.prototype.hasOwnProperty.call(b, d) && (h = m(d, b)) && f.push(o(d) + (e ? ": " : ":") + h);
                h = 0 === f.length ? "{}" : e ? "{\n" + e + f.join(",\n" + e) + "\n" + g + "}" : "{" + f.join(",") + "}";
                e = g;
                return h
        }
    }

    "function" !== typeof Date.prototype.toJSON && (Date.prototype.toJSON = function () {
        return isFinite(this.valueOf()) ? this.getUTCFullYear() + "-" + k(this.getUTCMonth() + 1) + "-" + k(this.getUTCDate()) + "T" + k(this.getUTCHours()) + ":" + k(this.getUTCMinutes()) + ":" + k(this.getUTCSeconds()) + "Z" : null
    }, String.prototype.toJSON = Number.prototype.toJSON = Boolean.prototype.toJSON = function () {
        return this.valueOf()
    });
    var q = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g, p = /[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g, e, l, r = {"\b": "\\b", "\t": "\\t", "\n": "\\n", "\f": "\\f", "\r": "\\r", '"': '\\"', "\\": "\\\\"}, i;
    "function" !== typeof JSON.stringify && (JSON.stringify = function (a, j, c) {
        var d;
        l = e = "";
        if (typeof c === "number")for (d = 0; d < c; d = d + 1)l = l + " "; else typeof c === "string" && (l = c);
        if ((i = j) && typeof j !== "function" && (typeof j !== "object" || typeof j.length !== "number"))throw Error("JSON.stringify");
        return m("", {"": a})
    });
    "function" !== typeof JSON.parse && (JSON.parse = function (a, e) {
        function c(a, d) {
            var g, f, b = a[d];
            if (b && typeof b === "object")for (g in b)if (Object.prototype.hasOwnProperty.call(b, g)) {
                f = c(b, g);
                f !== void 0 ? b[g] = f : delete b[g]
            }
            return e.call(a, d, b)
        }

        var d, a = String(a);
        q.lastIndex = 0;
        q.test(a) && (a = a.replace(q, function (a) {
            return"\\u" + ("0000" + a.charCodeAt(0).toString(16)).slice(-4)
        }));
        if (/^[\],:{}\s]*$/.test(a.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:\s*\[)+/g, ""))) {
            d = eval("(" + a + ")");
            return typeof e === "function" ? c({"": d}, "") : d
        }
        throw new SyntaxError("JSON.parse");
    })
})();
ListEditUi = function () {
    var self = this;
    this.ct = false;
    this.item_ids = [];
    this.selected = false;
    this.current_data = {item_type: null, item_id: null, provider: null, query: null, uri: null};
    this.dialog_window = false;
    this.init = function () {
        self.bindings();
        self.iface();
    };
    this.iface = function () {
    };
    this.bindings = function () {
        var container = $('.action-group');
        $(container).on('click', "li.action a:not('.disabled')", function (e) {
            e.preventDefault();
            var action = $(this).data('action');
            var ct = $(this).data('ct');
            self.ct = ct;
            switch (action) {
                case'merge':
                    self.merge_items_dialog();
                    break;
                default:
            }
        });
        $('#merge_dialog_container .item').live('mouseover', function () {
            $(this).addClass('hover');
        });
        $('#merge_dialog_container .item').live('mouseout', function () {
            $(this).removeClass('hover');
        });
        $('#merge_dialog_container .item').live('click', function () {
            $('#merge_dialog_container .item').removeClass('selected master slave');
            $(this).addClass('selected master');
            $('#merge_dialog_container .item').not($(this)).addClass('slave');
            self.selected = $(this).data('id');
            debug.debug('selected id:', self.selected)
        });
        $('#merge_dialog_container .action a').live('click', function (e) {
            e.preventDefault();
            var action = $(this).data('action');
            if (action == 'confirm') {
                var data = {item_ids: self.item_ids, item_type: self.ct, master_id: self.selected}
                if (!self.selected) {
                    alert('Selection required');
                    return false;
                }
                debug.debug('local', data);
                Dajaxice.alibrary.merge_items(function (data) {
                    debug.debug('remote', data);
                    try {
                        var api = self.dialog_window.qtip('api');
                        api.destroy();
                    } catch (e) {
                    }
                    if (data.status) {
                        document.location.reload();
                    } else {
                        alert(data.error);
                    }
                }, data);
            }
            if (action == 'cancel') {
                try {
                    var api = self.dialog_window.qtip('api');
                    api.destroy();
                } catch (e) {
                }
            }
        });
    };
    this.get_selection = function () {
        var item_ids = [];
        $('.list_body_row.selection').each(function (index) {
            var item_id = $(this).attr('id').split("_").pop();
            item_ids.push(item_id);
        });
        return item_ids;
    };
    this.merge_items_dialog = function () {
        self.item_ids = [];
        self.item_ids = this.get_selection();
        debug.debug('ids:', self.item_ids);
        var data = {item_ids: self.item_ids, item_type: self.ct}
        self.merge_dialog();
        self.merge_dialog_update(data);
    };
    this.merge_dialog = function () {
        try {
            var api = self.dialog_window.qtip('api');
            api.destroy();
        } catch (e) {
        }
        self.dialog_window = $('<div />').qtip({content: {text: function (api) {
            return'<div id="merge_dialog_container">loading</div>'
        }}, position: {my: 'center', at: 'center', target: $(window)}, show: {ready: true, modal: {on: true, blur: true}}, hide: false, style: 'qtip-dark qtip-dialogue qtip-shadow qtip-rounded popup-merge', events: {render: function (event, api) {
            $('a.btn', api.elements.content).click(api.hide);
        }}});
    };
    this.merge_dialog_update = function (data) {
        var item_type = data.item_type;
        var _item_type = item_type;
        if (_item_type == 'media') {
            _item_type = 'track';
        }
        var url = '/api/v1/' + _item_type + '/';
        var query = '?id__in=' + data.item_ids.join(',');
        $.get(url + query, function (data) {
            debug.debug(data);
            data.item_type = item_type;
            var html = nj.render('alibrary/nj/merge/merge_dialog.html', data);
            setTimeout(function () {
                $('#merge_dialog_container').html(html);
            }, 100)
        });
    };
};
ExporterMain = function () {
    var self = this;
    this.api_url = false;
    this.dom_id = 'export_list_holder';
    this.dom_element;
    this.pushy_key;
    this.export_items = [];
    this.init = function () {
        debug.debug('exporter: init');
        debug.debug(self.api_url);
        this.dom_element = $('#' + this.dom_id);
        self.iface();
        self.bindings();
        self.load();
        pushy.subscribe(self.pushy_key, function () {
            self.load()
        });
    };
    this.iface = function () {
    };
    this.bindings = function () {
    };
    this.load = function () {
        $.getJSON(self.api_url, function (data) {
            self.display(data);
        });
    };
    this.display = function (data) {
        $(data.objects).each(function (i, item) {
            if (!(item.uuid in self.export_items)) {
                var export_item = new ExporterItem;
                export_item.local_data = item;
                export_item.exporter_app = self;
                export_item.container = self.dom_element;
                export_item.api_url = item.resource_uri;
                export_item.init(true);
                self.export_items[item.uuid] = export_item;
            } else {
                debug.debug('Item exists on stage');
            }
        });
    };
};
ExporterItem = function () {
    var self = this;
    this.api_url;
    this.container;
    this.dom_element = false;
    this.exporter_app;
    this.offset;
    this.local_data = false;
    this.init = function (use_local_data) {
        debug.debug('ExporterItem - init');
        self.load(use_local_data);
        pushy.subscribe(self.api_url, function () {
            self.load()
        });
    };
    this.load = function (use_local_data) {
        debug.debug('ExporterItem - load');
        if (use_local_data) {
            debug.debug('ExporterItem - load: using local data');
            self.display(self.local_data);
        } else {
            debug.debug('ExporterItem - load: using remote data');
            var url = self.api_url;
            $.get(url, function (data) {
                self.local_data = data;
                self.display(data);
            })
        }
    };
    this.bindings = function () {
        $(self.dom_element).on('click', 'a[data-action="download"]', function (e) {
            e.preventDefault();
            var download_url = self.local_data.download_url;
            if (self.local_data.status == 1) {
                window.location.href = download_url;
            }
            if (self.local_data.status == 4) {
                window.location.href = download_url;
                var dialog = {title: 'Error', text: 'Already downloaded.'}
            }
        });
        $(self.dom_element).on('click', 'a[data-action="delete"]', function (e) {
            e.preventDefault();
            $.ajax({url: self.api_url, type: 'DELETE'}).done(function () {
                self.dom_element.fadeOut(300)
            });
        });
    };
    this.display = function (data) {
        debug.debug('ExporterItem - display');
        debug.debug(data);
        var status_map = new Array;
        status_map[0] = 'init';
        status_map[1] = 'done';
        status_map[2] = 'ready';
        status_map[3] = 'progress';
        status_map[4] = 'downloaded';
        status_map[99] = 'error';
        data.status_display = status_map[data.status]
        var html = nj.render('exporter/nj/export.html', {object: data});
        if (!self.dom_element) {
            console.log('create:', data);
            self.container.prepend(html);
            self.dom_element = $('#' + data.uuid, self.container);
        } else {
            $(self.dom_element).replaceWith(html);
            self.dom_element = $('#' + data.uuid, self.container);
        }
        self.bindings();
    };
};
ExporterApp = (function () {
    var self = this;
    this.api_url;
    this.init = function () {
        debug.debug('ExporterApp: init');
        self.bindings();
    };
    this.bindings = function () {
        $('body').on('click', 'a[data-action].disabled', function (e) {
            e.preventDefault();
            e.stopPropagation();
        });
        $('.action-group').on('click', 'a[data-action="download"].selection-any:not(".disabled")', function (e) {
            e.preventDefault();
            e.stopPropagation();
            var format = 'mp3';
            items = new Array;
            $('.list_body_row.selection').each(function (index) {
                var item_id = $(this).data('id');
                var item_type = $(this).data('ct');
                items.push({item_type: item_type, item_id: item_id, format: format});
                if (base.ui.use_effects) {
                }
            });
            self.queue(items, false);
        });
        $('.listview , .action-group').on('click', 'a[data-action="download"]:not(".selection-any"):not(".disabled")', function (e) {
            e.preventDefault();
            var item_type = $(this).data('ct');
            var item_id = $(this).data('id');
            var format = 'mp3';
            items = new Array;
            items.push({item_type: item_type, item_id: item_id, format: format});
            self.queue(items, false);
        });
    };
    this.queue = function (items, redirect) {
        var objects;
        var export_session;
        jQuery.ajax({url: self.api_url + '?status=0', success: function (data) {
            objects = data.objects;
        }, async: false});
        if (objects.length < 1) {
            jQuery.ajax({url: self.api_url, type: 'POST', data: JSON.stringify({filename: 'export - init'}), dataType: "json", contentType: "application/json", processData: false, success: function (data) {
                debug.debug(data);
                export_session = data;
            }, async: false});
        } else {
            export_session = objects[0];
        }
        debug.debug('export session:', export_session);
        for (i in items) {
            var item = items[i];
            debug.debug('exporter item:', item);
            var data = {export_session_id: export_session.id, item: item}
            jQuery.ajax({url: '/api/v1/exportitem/', type: 'POST', data: JSON.stringify(data), dataType: "json", contentType: "application/json", processData: false, success: function (data) {
                debug.debug(data);
            }, async: false});
        }
        self.run(export_session, redirect);
        base.ui.ui_message('Download queued', 10000);
    };
    this.run = function (export_session, redirect) {
        jQuery.ajax({url: export_session.resource_uri, type: 'PATCH', data: JSON.stringify({status: 2}), dataType: "json", contentType: "application/json", processData: false, success: function (data) {
            debug.debug('queue:', data);
            export_session = data;
            if (redirect) {
                window.location.href = export_session.download_url;
            }
        }, async: true});
    };
});
var list_edit = list_edit || {};
$(function () {
    list_edit = new ListEditUi();
    list_edit.init();
    exporter = new ExporterApp();
    exporter.api_url = '/api/v1/export/';
    exporter.init();
});
$(function () {
    tl.pg.init({});
    $('#tlyPageGuide').css('display', 'block');
})