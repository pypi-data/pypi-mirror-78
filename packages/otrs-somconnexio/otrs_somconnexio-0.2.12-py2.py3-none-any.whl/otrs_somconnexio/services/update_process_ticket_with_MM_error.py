from pyotrs.lib import DynamicField
from otrs_somconnexio.client import OTRSClient
from otrs_somconnexio.otrs_models.mm_error_article import MMErrorArticle


class UpdateProcessTicketWithMMError:
    """
    Update the ticket process adding articles with the MM error data.

    Receives a ticket_id (str), the HTTP response error (as dict) provided by the MM API,
    and an object, a string indicating which MM class building object failed (ex: account).
    When an error happens trying to build an account or an order-item into the MM system,
    this process creates an article with the information about how the process failed
    and it sends it to OTRS as an article.
    """

    def __init__(self, ticket_id, error, action, object):
        self.ticket_id = ticket_id
        self.error = error
        self.action = action
        self.object = object
        self.df = [DynamicField(name="errorPeticio", value=1)]

    def run(self):
        otrs_client = OTRSClient()

        article = MMErrorArticle(self.error, self.action, self.object).call()
        otrs_client.update_ticket(self.ticket_id, article, dynamic_fields=self.df)
