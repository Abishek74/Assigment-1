from datetime import datetime, timedelta

def calculate_claim_frequency(claims, policyholder_id):
    one_year_ago = datetime.today() - timedelta(days=365)
    return len([
        c for c in claims 
        if c['policyholder_id'] == policyholder_id and 
        datetime.strptime(c['claim_date'], '%Y-%m-%d') > one_year_ago
    ])

def is_high_risk(claims, policyholder):
    total_claim_amount = sum(c['amount'] for c in claims if c['policyholder_id'] == policyholder['policyholder_id'])
    frequency = calculate_claim_frequency(claims, policyholder['policyholder_id'])
    return frequency > 3 or total_claim_amount > 0.8 * policyholder['sum_insured']

def aggregate_by_policy_type(claims, policyholders):
    result = {}
    for c in claims:
        policyholder = next((p for p in policyholders if p['policyholder_id'] == c['policyholder_id']), None)
        if policyholder:
            pt = policyholder['policy_type']
            result[pt] = result.get(pt, 0) + 1
    return result
