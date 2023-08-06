import logging

from otrs_somconnexio.exceptions import UserManagementResponseEmpty

logger = logging.getLogger('otrs_somconnexio')


class UserManagementResponse:

    def __init__(self, raw_response, user_id='', call=''):
        self.raw_data = raw_response.json()['Result']
        if self.raw_data == []:
            raise UserManagementResponseEmpty('')
        self.user_id = user_id
        self.call = call

    def get_data(self):
        """
        Recieves a list with elements ordered as key-value pairs and returns a dict
        Ex: ['key1', 'value1', 'key2', 'value2'] -> {'key1': 'value1', 'key2': 'value2'}
        """
        if len(self.raw_data) % 2 != 0:
            logger.error(
                'Got an odd length list from call: {}, user: {}'.format(
                    self.call, self.user_id)
            )
            self.raw_data.append(None)

        iter_list = iter(self.raw_data)
        dct = {}

        for element in iter_list:
            dct[element] = next(iter_list)
        return dct
