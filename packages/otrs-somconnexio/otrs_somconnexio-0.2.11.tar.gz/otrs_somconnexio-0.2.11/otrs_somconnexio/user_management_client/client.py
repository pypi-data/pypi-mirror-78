import requests
import os
import json
import logging

from otrs_somconnexio.user_management_client.user_management_response import UserManagementResponse
from otrs_somconnexio.exceptions import ErrorUserManagementClientCall
from otrs_somconnexio.exceptions import UserManagementResponseEmpty

logger = logging.getLogger('otrs_somconnexio')


class UserManagementClient:
    WEBSERVICES_PATH = 'otrs/nph-genericinterface.pl/Webservice/UserManagement/cuser'

    def __init__(self, user_id):
        self.id = user_id
        self.url = '{}{}'.format(self._url(), self.WEBSERVICES_PATH)

    @staticmethod
    def _password():
        return os.environ['OTRS_PASSW']

    @staticmethod
    def _user():
        return os.environ['OTRS_USER']

    @staticmethod
    def _url():
        return os.environ['OTRS_URL']

    def set_preference(self, key, value):
        payload = {
            "UserLogin": self._user(),
            "Password": self._password(),
            "Object": "Kernel::System::CustomerUser",
            "Method": "SetPreferences",
            "Parameter": {
                "Key": key,
                "Value": value,
                "UserID": self.id
            }
        }
        json_payload = json.dumps(payload)
        try:
            UserManagementResponse(requests.post(self.url, data=json_payload))
        except UserManagementResponseEmpty:
            raise ErrorUserManagementClientCall(
                "Error setting the preference {} to user {}".format(key, self.id)
            )

    def get_preferences(self):
        payload = {
            "UserLogin": self._user(),
            "Password": self._password(),
            "Object": "Kernel::System::CustomerUser",
            "Method": "GetPreferences",
            "Parameter": {
                "UserID": self.id
            }
        }
        json_payload = json.dumps(payload)
        try:
            response = UserManagementResponse(requests.post(self.url, data=json_payload),
                                              self.id, "GetPreferences")
        except UserManagementResponseEmpty:
            raise ErrorUserManagementClientCall(
                "Error getting preferences from user {}".format(self.id)
            )

        return response.get_data()

    def get_data(self):
        payload = {
            "UserLogin": self._user(),
            "Password": self._password(),
            "Object": "Kernel::System::CustomerUser",
            "Method": "CustomerUserDataGet",
            "Parameter": {
                "User": self.id
            }
        }
        json_payload = json.dumps(payload)

        try:
            response = UserManagementResponse(requests.post(self.url, data=json_payload),
                                              self.id, "CustomerUserDataGet")
        except UserManagementResponseEmpty:
            raise ErrorUserManagementClientCall(
                "Error getting CustomerUser data from user {}".format(self.id)
            )

        return response.get_data()
