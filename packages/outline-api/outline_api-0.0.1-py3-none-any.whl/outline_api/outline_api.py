import logging
import requests
import json


ACCESS_URL = '{}/access-keys'
METRIC_URL = '{}/metrics/transfer'
KEY_URL = '{}/access-keys/{}'
NAME_URL = '{}/access-keys/{}/name'


class Manager(object):
    """An outline management class to work with outline API endpoints

    Returns:
        Manager -- the manager object to work with outline API
    """

    def __init__(self, apiurl, apicrt):
        super(Manager, self).__init__()
        self._log = logging.getLogger(__name__)
        self.apiurl = apiurl
        self.apicrt = apicrt
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

    def all(self):
        """returns the list of all access key objects

        Returns:
            list of dictionaries -- list of access key objects or None In
                case of any error including timeout. each dictionary is an
                access key object.
        """
        url = ACCESS_URL.format(self.apiurl)
        try:
            req = requests.get(url, verify=False,
                               headers=self.headers, timeout=3)
        except Exception as err:
            self._log.error(
                'An error occurred during getting all access keys: %s',
                str(err))
            return []

        if req.status_code != requests.codes['ok']:
            self._log.debug(
                'An API call error during getting all access key (/access-keys). status: %s',
                str(req.status_code))
            return []
        try:
            json_data = json.loads(req.text)
        except Exception:
            self._log.debug(
                'json load error during getting all access key (/access-keys)')
            return []

        if 'accessKeys' in json_data:
            return json_data['accessKeys']
        else:
            return []

    def all_active(self):
        """returns the dictionary of active access keys in last 30 days

        Returns:
            dictionary -- a dictionary of active access keys id and
                data transfer or None In case of any error including timeout.
        """
        url = METRIC_URL.format(self.apiurl)
        try:
            req = requests.get(url, verify=False,
                               headers=self.headers, timeout=30)
        except Exception as err:
            self._log.error(
                'An error occurred during getting active access keys: %s',
                str(err))
            return []
        if req.status_code != requests.codes['ok']:
            self._log.debug(
                'An API call error during getting active access keys (/metrics/transfer). status: %s',
                str(req.status_code))
            return []

        try:
            json_data = json.loads(req.text)
        except Exception:
            self._log.debug(
                'json load error during getting active access keys (/metrics/transfer)')
            return []

        if 'bytesTransferredByUserId' in json_data:
            return json_data['bytesTransferredByUserId']
        else:
            return []

    def new(self):
        """create new access key and return the key object

        Returns:
            dictionary -- an access key or None In case of any error
                including timeout.
        """
        url = ACCESS_URL.format(self.apiurl)
        try:
            req = requests.post(url, verify=False,
                                headers=self.headers, timeout=3)
        except Exception as err:
            self._log.error(
                'An error occurred during creating a new access key: %s',
                str(err))
            return {}
        if req.status_code != requests.codes['created']:
            self._log.debug(
                'An API call error during creating a new access key (/access-keys). status: %s',
                str(req.status_code))
            return {}

        try:
            json_data = json.loads(req.text)
        except Exception:
            self._log.debug(
                'json load error during creating a new access key (/access-keys).')
            return []
        return json_data

    def delete(self, id):
        """get a key id and delete that key.

        Arguments:
            id {int} -- key id

        Returns:
            bool -- True or False in case of any error.
        """
        url = KEY_URL.format(self.apiurl, id)
        try:
            req = requests.delete(
                url, verify=False, headers=self.headers, timeout=3)
        except Exception as err:
            self._log.error(
                'An error occurred during deleting the access key: %s',
                str(err))
            return False
        if req.status_code != requests.codes['no_content']:
            self._log.debug(
                'An API call error during deleting the access key (/access-keys/). status: %s',
                str(req.status_code))
            return False
        return True

    def rename(self, id, name):
        """changes the name of the key by getting the key's id

        Arguments:
            id {int} -- key id
            name {str} -- new name to save in the outline server for this key

        Returns:
            bool -- True or False in case of any error.
        """
        body = {'name': name}
        url = NAME_URL.format(self.apiurl, id)
        try:
            req = requests.put(url, data=body, verify=False,
                               headers=self.headers, timeout=3)
        except Exception as err:
            self._log.error(
                'An error occurred during renaming the access key: %s',
                str(err))
            return False
        if req.status_code != requests.codes['no_content']:
            self._log.debug(
                'An API call error during renaming the access key (/access-keys/). status: %s',
                str(req.status_code))
            return False
        return True

    def usage(self, id):
        """returns the data usage of a key by getting the key id

        Arguments:
            id {int} -- key id

        Returns:
            int -- data transfer for last 30 days or None in case of any
                error.
        """
        url = METRIC_URL.format(self.apiurl)
        try:
            req = requests.get(url, verify=False,
                               headers=self.headers, timeout=30)
        except Exception as err:
            self._log.error(
                'An error occurred during getting the data transfer: %s',
                str(err))
            return None
        if req.status_code != requests.codes['ok']:
            self._log.debug(
                'An API call error during getting the data transfer (/metrics/transfer). status: %s',
                str(req.status_code))
            return None

        try:
            json_data = json.loads(req.text)
        except Exception:
            self._log.debug(
                'json load error during getting the data transfer (/metrics/transfer).')
            return []

        if ('bytesTransferredByUserId' in json_data
                and str(id) in json_data['bytesTransferredByUserId']):
            return json_data['bytesTransferredByUserId'][str(id)]
        return 0

    def totalusage(self):
        """returns the total data usage in last 30 days

        Returns:
            int -- Total data usage
        """
        url = METRIC_URL.format(self.apiurl)
        try:
            req = requests.get(url, verify=False,
                               headers=self.headers, timeout=30)
        except Exception as err:
            self._log.error(
                'An error occurred during getting total data usage: %s',
                str(err))
            return None
        if req.status_code != requests.codes['ok']:
            self._log.debug(
                'An API call error during getting the total data transfer (/metrics/transfer). status: %s',
                str(req.status_code))
            return None

        try:
            json_data = json.loads(req.text)
        except Exception:
            self._log.debug(
                'json load error during getting the total data transfer (/metrics/transfer).')
            return []

        total = 0
        if 'bytesTransferredByUserId' in json_data:
            for key, value in json_data['bytesTransferredByUserId'].iteritems():
                total = total + value
            return total
        else:
            return None

    def current_keys(self):
        """returns the number of current keys

        Returns:
            int -- number of current keys or None in case of any error.
        """
        url = ACCESS_URL.format(self.apiurl)
        try:
            req = requests.get(url, verify=False,
                               headers=self.headers, timeout=3)
        except Exception as err:
            self._log.error(
                'An error occurred during getting access key numbers: %s',
                str(err))
            return None
        if req.status_code != requests.codes['ok']:
            self._log.debug(
                'An API call error during getting access key numbers (/access-keys). status: %s',
                str(req.status_code))
            return None

        try:
            json_data = json.loads(req.text)
        except Exception:
            self._log.debug(
                'json load error during getting access key numbers (/access-keys).')
            return []

        if 'accessKeys' in json_data:
            return (len(json_data['accessKeys']) - 1)
        return 0

    def active_keys_withtransfer(self):
        """returns the number of active keys in the last 30 days

        Returns:
            int -- Number of active keys in the last 30 days or None in case
                of any error.
        """
        url = METRIC_URL.format(self.apiurl)
        try:
            req = requests.get(url, verify=False,
                               headers=self.headers, timeout=30)
        except Exception as err:
            self._log.error(
                'An error occurred during getting the number of active access keys: %s',
                str(err))
            return None
        if req.status_code != requests.codes['ok']:
            self._log.debug(
                'An API call error during getting the number of active access keys (/metrics/transfer). status: %s',
                str(req.status_code))
            return None

        try:
            json_data = json.loads(req.text)
        except Exception:
            self._log.debug(
                'json load error during getting the number of active access keys (/metrics/transfer).')
            return []

        total = 0
        if 'bytesTransferredByUserId' in json_data:
            for key, value in json_data['bytesTransferredByUserId'].items():
                if value > 0:
                    total = total + 1
            return total
        else:
            return 0
