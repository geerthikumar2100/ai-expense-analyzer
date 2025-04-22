import unittest
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from analyzer.utils import custom_parse_csv, categorize_transaction, generate_ai_insight

class TestCustomParseCSV(TestCase):
    def test_valid_csv(self):
        csv_data = "Date,Description,Amount\n2025-04-01,Zomato order,100\n2025-04-02,Uber ride,50"
        file = SimpleUploadedFile("test.csv", csv_data.encode('utf-8'))
        result = custom_parse_csv(file)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['category'], 'Food')

    def test_missing_column(self):
        csv_data = "Date,Description\n2025-04-01,Food"
        file = SimpleUploadedFile("test.csv", csv_data.encode('utf-8'))
        with self.assertRaises(ValueError):
            custom_parse_csv(file)

    def test_malformed_row(self):
        csv_data = "Date,Description,Amount\n2025-04-01,Food,abc"
        file = SimpleUploadedFile("test.csv", csv_data.encode('utf-8'))
        result = custom_parse_csv(file)
        self.assertEqual(len(result), 0)

class TestCategorizeTransaction(unittest.TestCase):
    def test_valid_category(self):
        result = categorize_transaction("Uber ride to airport")
        self.assertEqual(result, "Transport")

    def test_no_match(self):
        result = categorize_transaction("Unrelated transaction note")
        self.assertEqual(result, "Others")

    def test_case_insensitivity(self):
        result = categorize_transaction("Zomato order")
        self.assertEqual(result, "Food")

class TestGenerateAIInsight(unittest.TestCase):
    @patch("analyzer.utils.co.generate")
    def test_api_error_handling(self, mock_generate):
        """If the Cohere API throws, we return a failure string."""
        mock_generate.side_effect = Exception("API failed")
        result = generate_ai_insight({'Food': 100})
        self.assertTrue(result.startswith("⚠️ AI failed: API failed"))

    def test_empty_input(self):
        """Empty summary yields the no‐data message."""
        result = generate_ai_insight({})
        self.assertEqual(result, "No data available for generating AI insights.")

    def test_valid_input(self):
        """Valid summary should produce a text containing at least one ₹ amount."""
        summary = {'Food': 200, 'Transport': 50}
        result = generate_ai_insight(summary)
        self.assertIn("₹", result)


class TestDashboardView(TestCase):
    def test_valid_csv_upload(self):
        csv_data = "Date,Description,Amount\n2025-04-01,Zomato order,100\n2025-04-02,Uber ride,50"
        file = SimpleUploadedFile("test.csv", csv_data.encode('utf-8'))
        response = self.client.post(reverse('dashboard'), {'file': file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You spent the most on Food")

    def test_invalid_file_type(self):
        txt_data = "Date,Description,Amount\n2025-04-01,Food,100"
        file = SimpleUploadedFile("test.txt", txt_data.encode('utf-8'))
        response = self.client.post(reverse('dashboard'), {'file': file})
        self.assertContains(response, "Uploaded file is not a CSV file.")

    def test_missing_columns(self):
        csv_data = "Date,Description\n2025-04-01,Food"
        file = SimpleUploadedFile("test.csv", csv_data.encode('utf-8'))
        response = self.client.post(reverse('dashboard'), {'file': file})
        self.assertContains(response, "CSV missing required columns")

    def test_empty_csv(self):
        csv_data = "Date,Description,Amount\n"
        file = SimpleUploadedFile("test.csv", csv_data.encode('utf-8'))
        response = self.client.post(reverse('dashboard'), {'file': file})
        self.assertContains(response, "No valid transactions found in the uploaded CSV.")
