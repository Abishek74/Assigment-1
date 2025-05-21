from datetime import datetime

class Policyholder:
    def __init__(self, policyholder_id, name, age, policy_type, sum_insured, registration_date=None):
        self.policyholder_id = policyholder_id
        self.name = name
        self.age = age
        self.policy_type = policy_type
        self.sum_insured = sum_insured
        self.registration_date = registration_date or datetime.today().strftime('%Y-%m-%d')

    def to_dict(self):
        return self.__dict__