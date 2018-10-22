import APIClient from "../api/client";

const DEBUG = true;

export const visit_by_resource = function (item, scope) {
    if (DEBUG) console.debug('visit:', item, scope);
    const url = (scope === undefined) ? item.url : item[scope];
    APIClient.get(url)
        .then((response) => {
            const detail_url = response.data.detail_url;
            if (DEBUG) console.debug('visit:', detail_url);
            if (window.opener) {
                window.opener.location.href = detail_url;
                window.opener.focus();
            }
        }, (error) => {
            console.error('error loading item', error);
        });
};
