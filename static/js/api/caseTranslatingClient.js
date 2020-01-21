import applyConverters from 'axios-case-converter';
import axios from 'axios';

const APIClient = applyConverters(axios.create({
    xsrfHeaderName: 'X-CSRFTOKEN',
    xsrfCookieName: 'csrftoken',
    timeout: 30000,
    headers: {
        'X-Requested-With': 'XMLHttpRequest'
    }
}));

export default APIClient;
