import unittest
from models.risk_analysis import is_high_risk, calculate_claim_frequency
from datetime import datetime, timedelta

class TestRiskAnalysis(unittest.TestCase):

    def setUp(self):
        # Creating test policyholder
        self.policyholder = {
            "policyholder_id": 1,
            "name": "Test User",
            "sum_insured": 10000
        }

    def test_high_claim_ratio(self):
        # Total claim > 80% of sum insured,then high risk candidate/policyholder
        claims = [
            {"policyholder_id": 1, "amount": 9000, "claim_date": "2025-01-01"}
        ]
        self.assertTrue(is_high_risk(claims, self.policyholder))

    def test_high_frequency(self):
        today = datetime.today()
        recent_date = today.strftime('%Y-%m-%d')

        
        claims = [{"policyholder_id": 1, "amount": 1000, "claim_date": recent_date} for _ in range(4)]
        self.assertTrue(is_high_risk(claims, self.policyholder))

    def test_not_high_risk(self):
        # Low claim amount + low frequency
        claims = [
            {"policyholder_id": 1, "amount": 1000, "claim_date": "2025-01-01"}
        ]
        self.assertFalse(is_high_risk(claims, self.policyholder))

    def test_claim_frequency(self):
        today = datetime.today()
        past = (today - timedelta(days=200)).strftime('%Y-%m-%d')
        claims = [
            {"policyholder_id": 1, "amount": 1000, "claim_date": past},
            {"policyholder_id": 1, "amount": 2000, "claim_date": past},
        ]
        freq = calculate_claim_frequency(claims, 1)
        self.assertEqual(freq, 2)

if __name__ == '__main__':
    unittest.main()
