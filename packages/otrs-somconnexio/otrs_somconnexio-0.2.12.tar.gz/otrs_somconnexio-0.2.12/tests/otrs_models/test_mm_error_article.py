# coding: utf-8
import unittest
from mock import Mock, patch

from otrs_somconnexio.otrs_models.mm_error_article import MMErrorArticle


class MMErrorArticleTestCase(unittest.TestCase):

    def test_subject_and_body(self):
        mm_error_article_1 = MMErrorArticle({'statusCode': "400"},
                                            "obtenció", "Account", "1234")
        self.assertEqual(mm_error_article_1.subject,
                         "Error desde Más Móvil en la obtenció d'un/a Account")
        self.assertEqual(mm_error_article_1.body, "mm_account_id: 1234\nstatusCode: 400\n")

        mm_error_article_2 = MMErrorArticle({'statusCode': "400"},
                                            "creació", "OrderItem")
        self.assertEqual(mm_error_article_2.subject,
                         "Error desde Más Móvil en la creació d'un/a OrderItem")
        self.assertEqual(mm_error_article_2.body, "statusCode: 400\n")

    @patch('otrs_somconnexio.otrs_models.abstract_article.Article')
    def test_call_with_account_error(self, MockArticle):

        fake_error = {
            "statusCode": "400",
            "message": "El documentType no es un valor válido: 2",
            "fields": "documentType"
        }
        expected_article_arguments = {
            "Subject": "Error desde Más Móvil en la creació d'un/a Account",
            "Body": u"fields: documentType\nmessage: El documentType no es un valor válido: 2\nstatusCode: 400\n",
            "ContentType": "text/plain; charset=utf8",
        }

        MMErrorArticle(fake_error, "creació", "Account").call()
        MockArticle.assert_called_once_with(expected_article_arguments)

    @patch('otrs_somconnexio.otrs_models.abstract_article.Article')
    def test_call_with_order_item_error(self, MockArticle):

        fake_error = {
            "statusCode": "400",
            "message": "El campo id debe estar relleno.",
            "fields": "id"
        }
        expected_article_arguments = {
            "Subject": "Error desde Más Móvil en la creació d'un/a OrderItem",
            "Body": u"fields: id\nmessage: El campo id debe estar relleno.\nmm_account_id: 12345S\nstatusCode: 400\n",
            "ContentType": "text/plain; charset=utf8",
        }

        MMErrorArticle(fake_error, "creació", "OrderItem", "12345S").call()
        MockArticle.assert_called_once_with(expected_article_arguments)
