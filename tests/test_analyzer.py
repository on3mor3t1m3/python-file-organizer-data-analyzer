import os
import unittest
import pandas as pd
from src.analyzer import get_basic_info, get_numeric_stats

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'Name': ['Ralph', 'Bob', 'Charlie', 'David', 'Eve', 'Bob'],
            'Salary': [1400, 1700, 1600, None, 1800, 1700],
            'Age': [21, 25, None, 28, 24, 25],
            'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Los Angeles']
        })

    def test_basic_info(self):
        info = get_basic_info(self.df)

        self.assertEqual(info['num_rows'], 6)
        self.assertEqual(info['num_columns'], 4)
        self.assertEqual(info['duplicate_rows'], 1)
        self.assertEqual(info['skipped_rows']['Salary'], 1)
        self.assertEqual(info['skipped_rows']['Age'], 1)


    def test_numeric_stats(self):
       stats = get_numeric_stats(self.df)

       self.assertAlmostEqual(stats['Age']['mean'], 24.6)
       self.assertEqual(stats['Age'] ['min'], 21)
       self.assertEqual(stats['Age'] ['max'], 28)
       self.assertAlmostEqual(stats['Salary']['mean'], 1640)

if __name__ == "__main__":
    unittest.main()