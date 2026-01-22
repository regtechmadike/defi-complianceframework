"""
DeFi Protocol Regulatory Risk Scoring Tool
Author: Magdalene Madike (@Nobody3120 / @regtechmadike on X)
Version: 1.0 (January 2026)

Implements the quantitative scorecard from the DeFi Compliance Framework.
Scores 6 dimensions (total 100 points) and assigns risk tier + basic recommendations.
"""

# Dimension max scores (from framework)
MAX_SCORES = {
    'decentralization': 20,
    'transaction_monitoring': 20,
    'user_identification': 15,
    'token_classification': 15,
    'jurisdictional_exposure': 15,
    'governance_disclosure': 15
}

TOTAL_MAX = sum(MAX_SCORES.values())  # 100

# Risk tier thresholds (aligned with framework)
RISK_TIERS = [
    (61, 100, "LOW", "Strong compliance posture – well-positioned for regulated environments"),
    (31, 60,  "MODERATE", "Partial measures in place – significant gaps remain"),
    (0,  30,  "HIGH", "Critical compliance gaps – high regulatory enforcement risk")
]

# Basic recommendations per dimension (expandable)
RECOMMENDATIONS = {
    'decentralization': "Further decentralize governance (remove multisigs/admin keys) and reduce frontend dependency.",
    'transaction_monitoring': "Integrate sanctions oracles (Chainalysis/Refinitiv) and on-chain anomaly detection.",
    'user_identification': "Implement privacy-preserving KYC (ZK-proofs, credential attestation) or optional verified tiers.",
    'token_classification': "Enhance utility focus, issue legal opinions, reduce perceived investment expectations.",
    'jurisdictional_exposure': "Add geo-blocking, enforceable ToS restrictions, and multi-jurisdiction compliance layers.",
    'governance_disclosure': "Establish compliance committee, publish risk/transparency reports, add incident response plans."
}

def clamp(value, min_val=0, max_val=100):
    """Clamp value to valid range."""
    return max(min_val, min(value, max_val))


def assess_protocol(protocol_data):
    """
    Assess regulatory risk for a DeFi protocol.
    
    Args:
        protocol_data (dict): Contains 'name' and dimension scores.
                              Example keys: 'decentralization_score', etc.
    
    Returns:
        tuple: (total_score: int, assessment: dict)
    """
    # Extract and clamp scores
    scores = {}
    for dim, max_score in MAX_SCORES.items():
        key = f"{dim}_score"
        raw = protocol_data.get(key, 0)
        scores[dim] = clamp(raw, 0, max_score)
    
    total_score = sum(scores.values())
    
    # Determine risk tier
    risk_level = "UNKNOWN"
    risk_description = "Invalid score range"
    for low, high, level, desc in RISK_TIERS:
        if low <= total_score <= high:
            risk_level = level
            risk_description = desc
            break
    
    # Generate recommendations for low scores
    recs = []
    for dim, score in scores.items():
        max_s = MAX_SCORES[dim]
        if score < max_s * 0.5:  # Less than 50% of max → flag
            recs.append(f"{dim.replace('_', ' ').title()}: {RECOMMENDATIONS[dim]} (Score: {score}/{max_s})")
    
    assessment = {
        'protocol_name': protocol_data.get('name', 'Unknown Protocol'),
        'total_score': total_score,
        'max_score': TOTAL_MAX,
        'percentage': round((total_score / TOTAL_MAX) * 100, 1),
        'risk_level': risk_level,
        'risk_description': risk_description,
        'scores_breakdown': scores,
        'recommendations': recs if recs else ["Strong across most dimensions – maintain and monitor."]
    }
    
    return total_score, assessment


def print_assessment(assessment):
    """Pretty-print the risk assessment report to console."""
    name = assessment['protocol_name']
    score = assessment['total_score']
    pct = assessment['percentage']
    level = assessment['risk_level']
    desc = assessment['risk_description']
    
    print("\n" + "=" * 80)
    print("  DEFI PROTOCOL REGULATORY RISK ASSESSMENT  ".center(80))
    print("=" * 80)
    print(f"\nProtocol: {name}")
    print(f"Overall Score: {score}/{assessment['max_score']} ({pct}%)")
    print(f"Risk Level:   {level}")
    print(f"Description:  {desc}\n")
    
    print("-" * 80)
    print("SCORES BREAKDOWN")
    print("-" * 80)
    for dim, score in assessment['scores_breakdown'].items():
        max_s = MAX_SCORES[dim]
        print(f"{dim.replace('_', ' ').title():28} {score:3}/{max_s:3}  ({round(score/max_s*100,1):5.1f}%)")
    
    print("\n" + "-" * 80)
    print("RECOMMENDATIONS FOR IMPROVEMENT")
    print("-" * 80)
    for rec in assessment['recommendations']:
        print(f"• {rec}")
    
    print("\n" + "=" * 80 + "\n")


# ────────────────────────────────────────────────
# Example usage (Uniswap V3 from your case study)
# ────────────────────────────────────────────────
if __name__ == "__main__":
    # Example input data
    example_data = {
        "name": "Uniswap V3",
        "decentralization_score": 18,
        "transaction_monitoring": 2,
        "user_identification": 0,
        "token_classification": 10,
        "jurisdictional_exposure": 5,
        "governance_disclosure": 7
    }
    
    total, result = assess_protocol(example_data)
    print_assessment(result)
