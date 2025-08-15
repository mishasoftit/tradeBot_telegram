import unittest
from utils.currency import convert_currency, format_currency

class TestCurrencyUtils(unittest.TestCase):
    def test_convert_currency_same(self):
        """Test conversion when currencies are the same"""
        result = convert_currency(100, "USD", "USD", {})
        self.assertEqual(result, 100)

    def test_convert_currency_direct(self):
        """Test direct currency conversion"""
        rates = {"USD/EUR": 0.85}
        result = convert_currency(100, "USD", "EUR", rates)
        self.assertEqual(result, 85)

    def test_convert_currency_via_usd(self):
        """Test conversion via USD when no direct rate"""
        rates = {
            "USD/EUR": 0.85,
            "GBP/USD": 1.25
        }
        # Convert 100 EUR to GBP: EUR->USD->GBP
        # 100 EUR = 100 / 0.85 USD ≈ 117.647 USD
        # 117.647 USD = 117.647 / 1.25 GBP ≈ 94.1176 GBP
        result = convert_currency(100, "EUR", "GBP", rates)
        self.assertAlmostEqual(result, 94.1176, places=4)

    def test_convert_currency_missing_rates(self):
        """Test conversion with missing exchange rates"""
        rates = {"USD/EUR": 0.85}
        with self.assertRaises(ValueError):
            convert_currency(100, "EUR", "JPY", rates)

    def test_format_currency_usd(self):
        """Test USD formatting"""
        self.assertEqual(format_currency(123.456, "USD"), "$123.46")
        self.assertEqual(format_currency(0.12345678, "USD"), "$0.12")

    def test_format_currency_btc(self):
        """Test BTC formatting"""
        self.assertEqual(format_currency(0.12345678, "BTC"), "0.12345678 BTC")
        self.assertEqual(format_currency(1.23456789, "BTC"), "1.23456789 BTC")

    def test_format_currency_other(self):
        """Test formatting for other currencies"""
        self.assertEqual(format_currency(123.456, "EUR"), "123.46 EUR")
        self.assertEqual(format_currency(0.12345678, "JPY"), "0.12 JPY")

if __name__ == '__main__':
    unittest.main()