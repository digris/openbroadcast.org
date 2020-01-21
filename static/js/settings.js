const getWebsocketHost = function (window) {
    // TODO: this does not seem to be too generic...
    if (parseInt(window.location.port) === 3000) {
        return 'local.openbroadcast.org:8080';
    }
    return window.location.host;
};

// merge with document settings
const settings = Object.assign({}, document.settings || {}, {
    WS_SCHEME: window.location.protocol === "https:" ? "wss" : "ws",
    WS_HOST: getWebsocketHost(window),
    PLACEHOLDER_IMAGE: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAVCAYAAACpF6WWAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyhpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTM4IDc5LjE1OTgyNCwgMjAxNi8wOS8xNC0wMTowOTowMSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKE1hY2ludG9zaCkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6QTZGODUyNzlCNTE2MTFFODlCMTFFRDFEMDAyOTFBRDQiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6QTZGODUyN0FCNTE2MTFFODlCMTFFRDFEMDAyOTFBRDQiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDpBNkY4NTI3N0I1MTYxMUU4OUIxMUVEMUQwMDI5MUFENCIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDpBNkY4NTI3OEI1MTYxMUU4OUIxMUVEMUQwMDI5MUFENCIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PpzFGLUAAABHSURBVHjaYvz//z8DtQETAw3ACDeUBZvghw8fCOkDxS4jiCEgIDAMw/T/sIv9/9Qw9P+g9f5/Wobp/wGPfcbR8nRoGAoQYACJbA8guOHyXAAAAABJRU5ErkJggg==',
});

export default settings;