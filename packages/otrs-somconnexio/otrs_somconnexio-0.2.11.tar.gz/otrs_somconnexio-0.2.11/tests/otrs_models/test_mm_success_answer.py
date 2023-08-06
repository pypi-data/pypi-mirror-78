# coding: utf-8
import unittest
from mock import Mock, patch

from otrs_somconnexio.otrs_models.mm_success_article import MMSuccessArticle

class MMSuccessArticleTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.otrs_models.abstract_article.Article')
    def test_call(self, MockArticle):

        account_id = '12345'
        expected_article_arguments = {
            "Subject": "Petició d'alta a MM entrada correctament",
            "Body": "mm_account_id: {}".format(account_id),
            "ContentType": "text/plain; charset=utf8"
        }

        MMSuccessArticle(account_id).call()
        MockArticle.assert_called_once_with(expected_article_arguments)
