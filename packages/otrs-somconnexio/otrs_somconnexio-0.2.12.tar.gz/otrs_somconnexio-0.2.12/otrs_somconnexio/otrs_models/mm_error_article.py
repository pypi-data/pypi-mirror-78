# coding: utf-8
import operator

from otrs_somconnexio.otrs_models.abstract_article import AbstractArticle


class MMErrorArticle(AbstractArticle):
    """
    Creates an article with the MM error data.

    error -> dictionary comming from the MM API with the error description
    object -> String that indicates which object failed: creation of account, order-item or asset
    """

    def __init__(self, error, action, object, account_id=None):
        self.params = error
        if account_id:
            self.params['mm_account_id'] = account_id
        self.subject = "Error desde Más Móvil en la {} d'un/a {}".format(action, object)
        self.body = self._body()

    def _body(self):
        body = ""
        for key, value in sorted(self.params.items(), key=operator.itemgetter(0)):
            try:
                value = value.decode('utf8')
            except AttributeError:
                # Python3: AttributeError: 'str' object has no attribute 'decode'
                pass
            finally:
                body = u"{}{}: {}\n".format(body, key, value)

        return body
