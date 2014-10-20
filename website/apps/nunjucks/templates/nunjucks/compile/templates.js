// nunjucks main object
(function () {

    var templates = {};

    {% for template in templates %}
    templates["{{ template.path|safe }}"] = (function () {
    {{ template.inner|safe }}
    })();  // template container ();
    {% endfor %}

    // register templates
    if (typeof nunjucks === "object") {
        nunjucks.env = new nunjucks.Environment([], null);
        nunjucks.env.registerPrecompiled(templates);
    }
    else {
        console.error("ERROR: You must load nunjucks before the precompiled templates");
    }

})();
