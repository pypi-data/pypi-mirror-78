# coding: utf-8
import unittest
from mock import Mock, patch
from pyotrs.lib import DynamicField
from otrs_somconnexio.services.update_process_ticket_with_MM_success_answer import \
    UpdateProcessTicketWithMMSuccessAnswer


class UpdateProcessTicketWithMMSuccessTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.services.update_process_ticket_with_MM_success_answer.OTRSClient',
           return_value=Mock(spec=['update_ticket']))
    @patch('otrs_somconnexio.services.update_process_ticket_with_MM_success_answer.'
           + 'MMSuccessArticle')
    @patch('otrs_somconnexio.services.update_process_ticket_with_MM_success_answer.'
           + 'DynamicField')
    def test_run(self, MockDF, MockMMSuccessArticle, MockOTRSClient):

        self.ticket_id = '1111'
        self.account_id = '12345'
        self.df = DynamicField(name="introPlataforma", value=1)

        mock_MM_success_article = Mock(spec=['call'])
        MM_success_article = object()

        def mock_MM_success_article_side_effect(account_id):
            if account_id == self.account_id:
                mock_MM_success_article.call.return_value = MM_success_article
                return mock_MM_success_article

        MockMMSuccessArticle.side_effect = mock_MM_success_article_side_effect

        def mock_df_side_effect(name, value):
            if name == "introPlataforma" and value == 1:
                return self.df

        MockDF.side_effect = mock_df_side_effect

        UpdateProcessTicketWithMMSuccessAnswer(self.ticket_id, self.account_id).run()

        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            self.ticket_id,
            MM_success_article,
            dynamic_fields=[self.df]
        )
