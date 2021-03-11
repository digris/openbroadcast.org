import applyConverters from 'axios-case-converter';
import axios from 'axios';

const MAX_REQUESTS_COUNT = 4;
const INTERVAL_MS = 10;
let PENDING_REQUESTS = 0;

const APIClient = applyConverters(axios.create({
  xsrfHeaderName: 'X-CSRFTOKEN',
  xsrfCookieName: 'csrftoken',
  timeout: 30000,
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
}));

/**
 * Axios Request Interceptor
 */
APIClient.interceptors.request.use((config) => new Promise((resolve) => {
    const interval = setInterval(() => {
      if (PENDING_REQUESTS < MAX_REQUESTS_COUNT) {
        PENDING_REQUESTS += 1;
        clearInterval(interval);
        resolve(config);
      }
    }, INTERVAL_MS);
  }));

/**
 * Axios Response Interceptor
 */
APIClient.interceptors.response.use((response) => {
  PENDING_REQUESTS = Math.max(0, PENDING_REQUESTS - 1);
  console.debug('PENDING_REQUESTS', PENDING_REQUESTS);
  return Promise.resolve(response);
}, (error) => {
  PENDING_REQUESTS = Math.max(0, PENDING_REQUESTS - 1);
  return Promise.reject(error);
});

// const sleep = (delay) => new Promise((resolve) => {
//   console.debug('sleep', delay);
//     setTimeout(resolve, delay);
//   });
//
// APIClient.interceptors.response.use(async (response) => {
//     await sleep(1000);
//     return response;
//   }, (error) => {
//     // Do something with response error
//     console.error(error);
//     return Promise.reject(error);
//   });

export default APIClient;
