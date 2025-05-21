from datetime import datetime

class Claim:
    def __init__(self, claim_id, policyholder_id, amount, reason, status, claim_date=None):
        self.claim_id = claim_id
        self.policyholder_id = policyholder_id
        self.amount = amount
        self.reason = reason
        self.status = status
        self.claim_date = claim_date or datetime.today().strftime('%Y-%m-%d')

    def to_dict(self):
        return self.__dict__
