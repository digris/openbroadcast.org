import axios from 'axios';

const APIClient = axios.create({
    xsrfHeaderName: 'X-CSRFTOKEN',
    xsrfCookieName: 'csrftoken',
    timeout: 30000,
    headers: {
        'X-Requested-With': 'XMLHttpRequest'
    }
});

export default APIClient;
