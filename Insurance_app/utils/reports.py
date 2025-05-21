from datetime import datetime
from collections import defaultdict

def total_claims_per_month(claims):
    monthly = defaultdict(int)
    for c in claims:
        month = datetime.strptime(c['claim_date'], '%Y-%m-%d').strftime('%Y-%m')
        monthly[month] += 1
    return dict(monthly)

def average_claim_by_policy_type(claims, policyholders):
    data = {}
    for c in claims:
        policyholder = next((p for p in policyholders if p['policyholder_id'] == c['policyholder_id']), None)
        if policyholder:
            pt = policyholder['policy_type']
            data.setdefault(pt, []).append(c['amount'])
    return {pt: sum(vals)/len(vals) for pt, vals in data.items()}

def highest_claim(claims):
    return max(claims, key=lambda c: c['amount'], default=None)

def pending_claims(claims, policyholders):
    pending_ids = {c['policyholder_id'] for c in claims if c['status'] == 'Pending'}
    return [p for p in policyholders if p['policyholder_id'] in pending_ids]
