class OTRSClientException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message


class ErrorCreatingSession(OTRSClientException):
    pass


class TicketNotCreated(OTRSClientException):
    pass


class TicketNotFoundError(OTRSClientException):
    pass


class OTRSIntegrationUnknownError(OTRSClientException):
    pass


class ErrorUserManagementClientCall(OTRSClientException):
    pass


class UserManagementResponseEmpty(OTRSClientException):
    pass
