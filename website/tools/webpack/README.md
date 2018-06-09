# Django Webpack Handler

Minimal module that helps combining Django wirt Webpack-Devserver

When using `devServer` (with `hot: true`) as a proxy static assets are injected dynamically. 
However - we also want to serve static files when working on non-js/style parts.


## Usage

Add `webpack.middleware.WebpackDevserverMiddleware` to `MIDDLEWARE_CLASSES`

and `webpack.middleware.WebpackDevserverMiddleware` to template `context_processors`.


Then you can use different paths for static files in your templates, like:

    {% if webpack_devserver %}
        <link rel="stylesheet" href="{% static 'css/bundle.css' %}"/>
    {% else %}
        <link rel="stylesheet" href="{% static 'dist/css/bundle.css' %}"/>
    {% endif %} 


As a default a request header `X-WEBPACK-DEVSERVER` is used to determine proxy origin.  
So configure Webpack like:


    const DEVSERVER_HEADER = 'X-WEBPACK-DEVSERVER';
    
    devServer: {
        ...
        proxy: {
            '/': {
                target: 'http://127.0.0.1:8080',
                onProxyReq: proxyReq => {
                    proxyReq.setHeader(DEVSERVER_HEADER, 'on');
                }
            },
        }
    }
