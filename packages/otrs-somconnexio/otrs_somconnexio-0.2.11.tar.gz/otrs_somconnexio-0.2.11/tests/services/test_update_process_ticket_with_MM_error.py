# coding: utf-8
import unittest
from mock import Mock, patch
from pyotrs.lib import DynamicField

from otrs_somconnexio.services.update_process_ticket_with_MM_error import UpdateProcessTicketWithMMError


class UpdateProcessTicketWithMMErrorTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.services.update_process_ticket_with_MM_error.OTRSClient', return_value=Mock(spec=['update_ticket']),
           )
    @patch('otrs_somconnexio.services.update_process_ticket_with_MM_error.MMErrorArticle')
    @patch('otrs_somconnexio.services.update_process_ticket_with_MM_error.DynamicField')
    def test_run(self, MockDF, MockMMErrorArticle, MockOTRSClient):

        self.ticket_id = '1111'
        self.object_str = "OrderItem"
        self.expected_error = {
            "statusCode": "400",
            "message": "El documentType no contiene un valor apto: 2",
            "fields": "documentType"
        }
        self.df = DynamicField(name="errorPeticio", value=1)

        mock_MM_error_article = Mock(spec=['call'])
        MM_error_article = object()

        def mock_MM_error_article_side_effect(error, action, builded_object):
            if (error == self.expected_error and action == "creació"
                    and builded_object == self.object_str):
                mock_MM_error_article.call.return_value = MM_error_article
                return mock_MM_error_article

        MockMMErrorArticle.side_effect = mock_MM_error_article_side_effect

        def mock_df_side_effect(name, value):
            if name == "errorPeticio" and value == 1:
                return self.df

        MockDF.side_effect = mock_df_side_effect

        UpdateProcessTicketWithMMError(self.ticket_id, self.expected_error,
                                       "creació", self.object_str).run()

        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            self.ticket_id,
            MM_error_article,
            dynamic_fields=[self.df]
        )
