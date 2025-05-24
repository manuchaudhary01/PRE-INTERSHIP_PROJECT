import unittest
from unittest.mock import patch, MagicMock
import requests
import integration_service  

class TestIntegrationService(unittest.TestCase):

    @patch("integration_service.requests.get")
    def test_fetch_customers_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Alice"}]
        mock_get.return_value = mock_response

        customers = integration_service.fetch_customers_with_retry()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]["name"], "Alice")

    @patch("integration_service.requests.get")
    def test_fetch_customers_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        customers = integration_service.fetch_customers_with_retry()
        self.assertEqual(customers, [])

    @patch("integration_service.requests.get", side_effect=requests.exceptions.Timeout)
    def test_fetch_customers_timeout(self, mock_get):
        customers = integration_service.fetch_customers_with_retry()
        self.assertEqual(customers, [])

    @patch("integration_service.requests.post")
    def test_send_package_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        result = integration_service.send_package_request_with_retry("Alice")
        self.assertTrue(result)

    @patch("integration_service.requests.post")
    def test_send_package_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        result = integration_service.send_package_request_with_retry("Alice")
        self.assertFalse(result)

    @patch("integration_service.requests.post", side_effect=requests.exceptions.ConnectionError)
    def test_send_package_exception(self, mock_post):
        result = integration_service.send_package_request_with_retry("Bob")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
