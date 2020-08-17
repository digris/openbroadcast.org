import APIClient from '../api/client';


export const visit_by_resource = (item, scope) => {
  const url = (scope === undefined) ? item.url : item[scope];
  APIClient.get(url)
    .then((response) => {
      const { detail_url } = response.data;
      if (window.opener) {
        window.opener.location.href = detail_url;
        window.opener.focus();
      } else {
        window.location.href = detail_url;
      }
    }, (error) => {
      console.error('error loading item', error);
    });
};
