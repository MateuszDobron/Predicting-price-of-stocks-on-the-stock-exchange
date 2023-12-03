import unittest
from calculation_of_technical_indicators.py import calculate_sma, calculate_ema, calculate_rsi, calculate_macd  

class TestIndicatorCalculations(unittest.TestCase):

    def test_calculate_sma(self):
        prices = [10, 11, 12, 13, 14]
        window = 3
        result = calculate_sma(prices, window)
        expected_result = 13  # (12 + 13 + 14) / 3
        self.assertEqual(result, expected_result, "SMA calculation is incorrect")

    def test_calculate_ema(self):
        prices = [10, 11, 12]
        window = 3
        expected_result = 11  
        result = calculate_ema(prices, window)
        self.assertAlmostEqual(result, expected_result, places=5, "EMA calculation is incorrect")

    def test_calculate_rsi(self):
        prices = [10, 11, 12, 13, 14, 15]
        window = 5
        expected_result = 100  
        result = calculate_rsi(prices, window)
        self.assertAlmostEqual(result, expected_result, places=2, "RSI calculation is incorrect")

    def test_calculate_macd(self):
        prices = [10, 12, 14, 16, 18, 20]
        macd, signal, macd_diff = calculate_macd(prices)
        expected_macd = 1  
        expected_signal = 0.9 
        expected_macd_diff = 0.1  
        self.assertAlmostEqual(macd, expected_macd, places=5, "MACD calculation is incorrect")
        self.assertAlmostEqual(signal, expected_signal, places=5, "Signal line calculation is incorrect")
        self.assertAlmostEqual(macd_diff, expected_macd_diff, places=5, "MACD Diff calculation is incorrect")

if __name__ == '__main__':
    unittest.main()
