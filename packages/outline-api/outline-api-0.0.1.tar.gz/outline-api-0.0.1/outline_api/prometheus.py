import logging
import requests
import json


logger = logging.getLogger(__name__)
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
BASE_URL = 'http://{}:{}/{}'


def get_key_numbers(host, port):
    """returns the number of current keys

    Arguments:
        host {str} -- Server IP or hostname
        port {str} -- Prometheus port

    Returns:
        int -- number of current keys or None in case of any error.
    """
    api_endpoint = '/api/v1/query?query=shadowsocks_keys'
    url = BASE_URL.format(host, port, api_endpoint)
    try:
        req = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=3)
    except Exception as err:
        logger.error(
            'An error occurred during get_key_numbers: %s',
            str(err))
        return None
    if req.status_code != requests.codes['ok']:
        logger.debug(
            '''An API call error during getting access key numbers.
            status: %s''',
            str(req.status_code))
        return None

    try:
        json_data = json.loads(req.text)
    except Exception:
        logger.debug(
            'json load error during getting access key numbers.')
        return []

    if 'data' in json_data:
        number = json_data['data']['result'][0]['value'][1]
        return int(number)
    else:
        return None


def get_created_key_numbers(host, port, duration='1d'):
    """returns the number of created keys in latest 'duration' period.

    Arguments:
        host {str} -- Server IP or hostname
        port {str} -- Prometheus port
        duration {str} -- The time duration string (default: {'1d'})

    Returns:
        int -- number of current keys or None in case of any error.
    """
    api_endpoint = '/api/v1/query?query=delta(shadowsocks_keys [%s])' % (
        duration)
    url = BASE_URL.format(host, port, api_endpoint)
    try:
        req = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=3)
    except Exception as err:
        logger.error(
            'An error occurred during get_created_key_numbers: %s',
            str(err))
        return None
    if req.status_code != requests.codes['ok']:
        logger.debug(
            '''An API call error during get_created_key_numbers.
            status: %s''',
            str(req.status_code))
        return None

    try:
        json_data = json.loads(req.text)
    except Exception:
        logger.debug(
            'json load error during get_created_key_numbers.')
        return []

    if 'data' in json_data:
        number = json_data['data']['result'][0]['value'][1]
        return int(float(number))
    else:
        return None


def get_active_keys(host, port, duration='1d'):
    """Returns the number of active keys in latest 'duration' period.

    Arguments:
        host {str} -- Server IP or hostname
        port {str} -- Prometheus port
        duration {str} -- The time duration string (default: {'1d'})

    Returns:
        int -- number of active keys or None in case of any error.
    """
    api_endpoint = '/api/v1/query?query=sum(max(increase(shadowsocks_data_bytes{access_key!=\"\"} [%s])) by (access_key, location) > bool 0)' % (
        duration)
    url = BASE_URL.format(host, port, api_endpoint)
    try:
        req = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=60)
    except Exception as err:
        logger.error(
            'An error occurred during get_active_keys: %s',
            str(err))
        return None
    if req.status_code != requests.codes['ok']:
        logger.debug(
            '''An API call error during get_active_keys.
            status: %s''',
            str(req.status_code))
        return None

    try:
        json_data = json.loads(req.text)
    except Exception:
        logger.debug(
            'json load error during get_active_keys.')
        return []

    if 'data' in json_data:
        number = json_data['data']['result'][0]['value'][1]
        return int(number)
    else:
        return None


def get_active_keys_list(host, port, duration='1d'):
    """Returns the number of active keys in latest 'duration' period.

    Arguments:
        host {str} -- Server IP or hostname
        port {str} -- Prometheus port
        duration {str} -- The time duration string (default: {'1d'})

    Returns:
        int -- number of active keys or None in case of any error.
    """
    api_endpoint = '/api/v1/query?query=max(increase(shadowsocks_data_bytes{access_key!=\"\"} [%s])) by (access_key, location) > bool 0' % (
        duration)
    url = BASE_URL.format(host, port, api_endpoint)
    try:
        req = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=120)
    except Exception as err:
        logger.error(
            'An error occurred during get_active_keys_list: %s',
            str(err))
        return []
    if req.status_code != requests.codes['ok']:
        logger.debug(
            '''An API call error during get_active_keys_list.
            status: %s''',
            str(req.status_code))
        return []
    all_keys = []

    try:
        json_data = json.loads(req.text)
    except Exception:
        logger.debug(
            'json load error during get_active_keys_list.')
        return []

    if 'data' in json_data:
        for result in json_data['data']['result']:
            if 'access_key' in result['metric']:
                all_keys.append(result['metric']['access_key'])
        return all_keys
    else:
        return []


def get_key_datatransfer(host, port, key='1', duration='1d'):
    """Returns the data transfer during the latest 'duration' for key.

    Arguments:
        host {str} -- Server IP or hostname
        port {str} -- Prometheus port
        key {str} -- The key number (default: {'1'})
        duration {str} -- The time duration string (default: {'1d'})

    Returns:
        int -- data transfer in bytes or None in case of any error.
    """
    api_endpoint = '/api/v1/query?query=sum(increase(shadowsocks_data_bytes{dir=~\"c<p|p>t\", access_key=\"%s\"} [%s]))' % (
        key, duration)
    url = BASE_URL.format(host, port, api_endpoint)
    try:
        req = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=30)
        print(req.status_code)
    except Exception as err:
        logger.error(
            'An error occurred during get_key_datatransfer: %s',
            str(err))
        return None
    if req.status_code != requests.codes['ok']:
        logger.debug(
            '''An API call error during get_key_datatransfer.
            status: %s''',
            str(req.status_code))
        return None

    try:
        json_data = json.loads(req.text)
    except Exception:
        logger.debug(
            'json load error during get_key_datatransfer.')
        return []

    if 'data' in json_data:
        number = json_data['data']['result'][0]['value'][1]
        return float(number)
    else:
        return None


def get_server_datatransfer(host, port, duration='1d'):
    """Returns the total data transfer during the latest 'duration' period.

    Arguments:
        host {str} -- Server IP or hostname
        port {str} -- Prometheus port
        duration {str} -- The time duration string (default: {'1d'})

    Returns:
        float -- total data transfer in bytes or None in case of any error.
    """
    api_endpoint = '/api/v1/query?query=sum(increase(shadowsocks_data_bytes{dir=~\"c<p|p>t\"} [%s]))' % (
        duration)
    url = BASE_URL.format(host, port, api_endpoint)
    try:
        req = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=30)
    except Exception as err:
        logger.error(
            'An error occurred during get_server_datatransfer: %s',
            str(err))
        return None
    if req.status_code != requests.codes['ok']:
        logger.debug(
            '''An API call error during get_server_datatransfer.
            status: %s''',
            str(req.status_code))
        return None

    try:
        json_data = json.loads(req.text)
    except Exception:
        logger.debug(
            'json load error during get_server_datatransfer.')
        return []

    if 'data' in json_data:
        number = json_data['data']['result'][0]['value'][1]
        return float(number)
    else:
        return None


def get_server_datatransfer_history(host, port, duration='1d', offset='1d'):
    """Returns the total data transfer during the latest 'duration' period with offset.

    Arguments:
        host {str} -- Server IP or hostname
        port {str} -- Prometheus port
        duration {str} -- The time duration string (default: {'1d'})
        offset {str} -- Time offset to count the active keys (default: {'1d'})

    Returns:
        float -- total data transfer in bytes or None in case of any error.
    """
    api_endpoint = '/api/v1/query?query=sum(increase(shadowsocks_data_bytes{dir=~\"c<p|p>t\"} [%s] offset %s))' % (
        duration, offset)
    url = BASE_URL.format(host, port, api_endpoint)
    try:
        req = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=30)
    except Exception as err:
        logger.error(
            'An error occurred during get_server_datatransfer_history: %s',
            str(err))
        return None
    if req.status_code != requests.codes['ok']:
        logger.debug(
            '''An API call error during get_server_datatransfer_history.
            status: %s''',
            str(req.status_code))
        return None

    try:
        json_data = json.loads(req.text)
    except Exception:
        logger.debug(
            'json load error during get_server_datatransfer_history.')
        return []

    if 'data' in json_data:
        number = json_data['data']['result'][0]['value'][1]
        return float(number)
    else:
        return None


def get_active_keys_history(host, port, duration='1d', offset='1d'):
    """Returns the number of active keys in latest 'duration' period with offset

    Arguments:
        host {str} -- Server IP or hostname
        port {str} -- Prometheus port
        duration {str} -- The time duration string (default: {'1d'})
        offset {str} -- Time offset to count the active keys (default: {'1d'})

    Returns:
        int -- number of active keys or None in case of any error.
    """
    api_endpoint = '/api/v1/query?query=sum(max(increase(shadowsocks_data_bytes{access_key!=\"\"} [%s] offset %s)) by (access_key) > bool 0)' % (
        duration, offset)
    url = BASE_URL.format(host, port, api_endpoint)
    try:
        req = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=60)
    except Exception as err:
        logger.error(
            'An error occurred during get_active_keys_history: %s',
            str(err))
        return None
    if req.status_code != requests.codes['ok']:
        logger.debug(
            '''An API call error during get_active_keys_history.
            status: %s''',
            str(req.status_code))
        return None

    try:
        json_data = json.loads(req.text)
    except Exception:
        logger.debug(
            'json load error during get_active_keys_history.')
        return []

    if 'data' in json_data:
        number = json_data['data']['result'][0]['value'][1]
        return int(number)
    else:
        return None


def is_blocked(host, port, level=0.005):
    """Returns True if the server is blocked

    Arguments:
        host {str} -- Server IP or hostname
        port {str} -- Prometheus port
        level {float} -- Level to check if the server is blocked

    Returns:
        boolean -- True if the server is blocked, False if not 
                    or None in case of any error.
    """
    api_endpoint = '/api/v1/query?query=((sum by(instance) (increase(shadowsocks_tcp_probes_bucket{error=~"timeout",le="48",status="ERR_CIPHER"}[1d])) - sum by(instance) (increase(shadowsocks_tcp_probes_bucket{error=~"timeout",le="0",status="ERR_CIPHER"}[1d]))) / sum by(instance) (increase(shadowsocks_tcp_connections_closed{status="OK"}[1d])))'
    url = BASE_URL.format(host, port, api_endpoint)
    try:
        req = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=60)
    except Exception as err:
        logger.error(
            'An error occurred during is_blocked: %s',
            str(err))
        return None
    if req.status_code != requests.codes['ok']:
        logger.debug(
            '''An API call error during is_blocked.
            status: %s''',
            str(req.status_code))
        return None

    try:
        json_data = json.loads(req.text)
    except Exception:
        logger.debug(
            'json load error during is_blocked.')
        return []

    if 'data' in json_data:
        results = json_data['data']['result']
        if len(results) > 0:
            logger.debug('Block indicator: {}'.format(
                results[0]['value'][1]))
            return float(results[0]['value'][1]) > level
        else:
            return False
    else:
        return None
