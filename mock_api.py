"""mock credit bureau API responses for demo purposes.

all data is synthetic. no real customer information is used.
"""

import random


# credit reports keyed by ID number for deterministic demo scenarios
MOCK_CREDIT_REPORTS = {
    # scenario 1: sarah johnson - clean profile, personal loan
    "9001012000088": {
        "applicant": {
            "name": "Sarah Johnson",
            "id_number": "9001012000088",
            "date_of_birth": "1990-01-01",
        },
        "credit_score": 720,
        "risk_rating": "low",
        "accounts": {
            "total_open": 3,
            "total_closed": 2,
            "details": [
                {
                    "type": "credit card",
                    "provider": "FNB",
                    "limit": 45000,
                    "balance": 12300,
                    "status": "current",
                    "opened": "2018-03-15",
                    "payment_history": "good - no missed payments",
                },
                {
                    "type": "personal loan",
                    "provider": "Capitec",
                    "original_amount": 80000,
                    "balance": 23400,
                    "monthly_instalment": 2850,
                    "status": "current",
                    "opened": "2022-06-01",
                    "payment_history": "good - no missed payments",
                },
                {
                    "type": "retail account",
                    "provider": "Woolworths",
                    "limit": 15000,
                    "balance": 3200,
                    "status": "current",
                    "opened": "2019-11-20",
                    "payment_history": "good - 1 late payment (2021-08, since rectified)",
                },
            ],
        },
        "payment_profile": {
            "on_time_percentage": 98.5,
            "total_payments_tracked": 72,
            "late_payments": 1,
            "defaults": 0,
            "judgements": 0,
            "write_offs": 0,
        },
        "enquiry_history": {
            "last_30_days": 0,
            "last_90_days": 1,
            "last_12_months": 2,
            "details": [
                {
                    "date": "2025-11-15",
                    "provider": "TymeBank",
                    "type": "personal loan enquiry",
                },
                {
                    "date": "2025-06-22",
                    "provider": "FNB",
                    "type": "credit limit increase",
                },
            ],
        },
        "adverse_information": {
            "defaults": [],
            "judgements": [],
            "administration_orders": [],
            "sequestrations": [],
            "debt_review": False,
        },
        "total_monthly_obligations": 6050,
    },
    # scenario 2: james mbeki - high-value home loan, full investigation
    "8805125012082": {
        "applicant": {
            "name": "James Mbeki",
            "id_number": "8805125012082",
            "date_of_birth": "1988-05-12",
        },
        "credit_score": 685,
        "risk_rating": "medium",
        "accounts": {
            "total_open": 5,
            "total_closed": 3,
            "details": [
                {
                    "type": "vehicle finance",
                    "provider": "WesBank",
                    "original_amount": 420000,
                    "balance": 185000,
                    "monthly_instalment": 8000,
                    "status": "current",
                    "opened": "2023-02-10",
                    "payment_history": "good - no missed payments",
                },
                {
                    "type": "credit card",
                    "provider": "Nedbank",
                    "limit": 80000,
                    "balance": 35600,
                    "status": "current",
                    "opened": "2017-08-01",
                    "payment_history": "1 late payment (2024-01)",
                },
                {
                    "type": "credit card",
                    "provider": "ABSA",
                    "limit": 50000,
                    "balance": 8900,
                    "status": "current",
                    "opened": "2020-04-15",
                    "payment_history": "good - no missed payments",
                },
                {
                    "type": "personal loan",
                    "provider": "Standard Bank",
                    "original_amount": 150000,
                    "balance": 67000,
                    "monthly_instalment": 4200,
                    "status": "current",
                    "opened": "2023-09-01",
                    "payment_history": "good - no missed payments",
                },
                {
                    "type": "retail account",
                    "provider": "Edgars",
                    "limit": 12000,
                    "balance": 0,
                    "status": "current",
                    "opened": "2016-12-01",
                    "payment_history": "good - account inactive",
                },
            ],
        },
        "payment_profile": {
            "on_time_percentage": 97.2,
            "total_payments_tracked": 108,
            "late_payments": 3,
            "defaults": 0,
            "judgements": 0,
            "write_offs": 0,
        },
        "enquiry_history": {
            "last_30_days": 1,
            "last_90_days": 2,
            "last_12_months": 4,
            "details": [
                {
                    "date": "2026-02-20",
                    "provider": "Standard Bank",
                    "type": "home loan enquiry",
                },
                {
                    "date": "2025-12-05",
                    "provider": "FNB",
                    "type": "home loan pre-qualification",
                },
                {
                    "date": "2025-09-10",
                    "provider": "Nedbank",
                    "type": "credit limit review",
                },
                {
                    "date": "2025-05-01",
                    "provider": "Discovery Bank",
                    "type": "account opening",
                },
            ],
        },
        "adverse_information": {
            "defaults": [],
            "judgements": [],
            "administration_orders": [],
            "sequestrations": [],
            "debt_review": False,
        },
        "total_monthly_obligations": 12200,
    },
    # scenario 3: thandi nkosi - risk flags, triggers deeper investigation
    "8503203456087": {
        "applicant": {
            "name": "Thandi Nkosi",
            "id_number": "8503203456087",
            "date_of_birth": "1985-03-20",
        },
        "credit_score": 480,
        "risk_rating": "high",
        "accounts": {
            "total_open": 6,
            "total_closed": 4,
            "details": [
                {
                    "type": "personal loan",
                    "provider": "African Bank",
                    "original_amount": 50000,
                    "balance": 48200,
                    "monthly_instalment": 2100,
                    "status": "default",
                    "opened": "2025-01-15",
                    "payment_history": "defaulted after 3 payments",
                },
                {
                    "type": "credit card",
                    "provider": "Capitec",
                    "limit": 25000,
                    "balance": 24800,
                    "status": "arrears - 90 days",
                    "opened": "2023-06-01",
                    "payment_history": "irregular - multiple missed payments",
                },
                {
                    "type": "personal loan",
                    "provider": "Wonga",
                    "original_amount": 15000,
                    "balance": 18500,
                    "monthly_instalment": 3200,
                    "status": "default",
                    "opened": "2025-04-20",
                    "payment_history": "defaulted - balance includes penalties",
                },
                {
                    "type": "retail account",
                    "provider": "Mr Price",
                    "limit": 8000,
                    "balance": 7600,
                    "status": "arrears - 60 days",
                    "opened": "2022-03-10",
                    "payment_history": "deteriorating - was current until 2025",
                },
                {
                    "type": "cellphone contract",
                    "provider": "Vodacom",
                    "monthly_instalment": 899,
                    "balance": 5400,
                    "status": "arrears - 30 days",
                    "opened": "2024-01-01",
                    "payment_history": "late payments from mid-2025",
                },
                {
                    "type": "credit card",
                    "provider": "FNB",
                    "limit": 40000,
                    "balance": 39500,
                    "status": "current - minimum payments only",
                    "opened": "2019-07-15",
                    "payment_history": "switched to minimum payments in 2025",
                },
            ],
        },
        "payment_profile": {
            "on_time_percentage": 62.3,
            "total_payments_tracked": 96,
            "late_payments": 18,
            "defaults": 2,
            "judgements": 0,
            "write_offs": 0,
        },
        "enquiry_history": {
            "last_30_days": 8,
            "last_90_days": 14,
            "last_12_months": 22,
            "details": [
                {
                    "date": "2026-03-05",
                    "provider": "Capitec",
                    "type": "personal loan enquiry",
                },
                {
                    "date": "2026-03-02",
                    "provider": "TymeBank",
                    "type": "personal loan enquiry",
                },
                {
                    "date": "2026-02-28",
                    "provider": "African Bank",
                    "type": "personal loan enquiry",
                },
                {
                    "date": "2026-02-25",
                    "provider": "Wonga",
                    "type": "short-term loan enquiry",
                },
                {
                    "date": "2026-02-20",
                    "provider": "DirectAxis",
                    "type": "personal loan enquiry",
                },
                {
                    "date": "2026-02-18",
                    "provider": "Bayport",
                    "type": "personal loan enquiry",
                },
                {
                    "date": "2026-02-15",
                    "provider": "Old Mutual",
                    "type": "personal loan enquiry",
                },
                {
                    "date": "2026-02-10",
                    "provider": "Nedbank",
                    "type": "personal loan enquiry",
                },
            ],
        },
        "adverse_information": {
            "defaults": [
                {
                    "provider": "African Bank",
                    "amount": 48200,
                    "date": "2025-07-01",
                    "status": "active",
                },
                {
                    "provider": "Wonga",
                    "amount": 18500,
                    "date": "2025-10-15",
                    "status": "active",
                },
            ],
            "judgements": [],
            "administration_orders": [],
            "sequestrations": [],
            "debt_review": False,
        },
        "total_monthly_obligations": 7099,
    },
}


# identity verification mock data
MOCK_IDENTITY_RESULTS = {
    "9001012000088": {
        "match_found": True,
        "confidence": "high",
        "verified_name": "Sarah Johnson",
        "verified_dob": "1990-01-01",
        "id_status": "valid - active",
        "discrepancies": [],
        "source": "Department of Home Affairs",
        "last_updated": "2025-12-01",
    },
    "8805125012082": {
        "match_found": True,
        "confidence": "high",
        "verified_name": "James Thabo Mbeki",
        "verified_dob": "1988-05-12",
        "id_status": "valid - active",
        "discrepancies": [
            "registered name includes middle name 'Thabo' not provided in application"
        ],
        "source": "Department of Home Affairs",
        "last_updated": "2026-01-15",
    },
    "8503203456087": {
        "match_found": True,
        "confidence": "medium",
        "verified_name": "Thandi P. Nkosi",
        "verified_dob": "1985-03-20",
        "id_status": "valid - active",
        "discrepancies": [
            "address on file differs from application address",
            "name on application missing initial 'P.'",
        ],
        "source": "Department of Home Affairs",
        "last_updated": "2024-09-20",
    },
}


# fraud check mock data
MOCK_FRAUD_RESULTS = {
    "9001012000088": {
        "fraud_risk_score": 8,
        "risk_level": "low",
        "flags": [],
        "checks_performed": [
            "identity document validation",
            "known fraud database",
            "address verification",
            "device/IP screening",
        ],
        "details": (
            "no fraud indicators detected. applicant details are consistent "
            "across all databases."
        ),
    },
    "8805125012082": {
        "fraud_risk_score": 12,
        "risk_level": "low",
        "flags": [],
        "checks_performed": [
            "identity document validation",
            "known fraud database",
            "address verification",
            "employer verification",
            "device/IP screening",
        ],
        "details": (
            "no fraud indicators detected. minor discrepancy in registered name "
            "(middle name) is common and not a concern."
        ),
    },
    "8503203456087": {
        "fraud_risk_score": 62,
        "risk_level": "high",
        "flags": [
            (
                "address mismatch - application address does not match any "
                "address on credit bureau records"
            ),
            (
                "high enquiry velocity - 8 loan applications in 30 days suggests "
                "possible desperation or application fraud"
            ),
            "recent account defaults following a period of account farming",
            "phone number linked to 3 other recently defaulted accounts",
        ],
        "checks_performed": [
            "identity document validation",
            "known fraud database",
            "address verification",
            "phone number cross-reference",
            "enquiry pattern analysis",
            "device/IP screening",
        ],
        "details": (
            "multiple fraud indicators detected. address does not match bureau "
            "records. phone number appears on other defaulted accounts. enquiry "
            "pattern suggests serial credit applications. recommend enhanced "
            "due diligence."
        ),
    },
}


def get_credit_report(id_number: str, name: str = None) -> dict:
    """returns a mock credit report for the given ID number."""
    if id_number in MOCK_CREDIT_REPORTS:
        return MOCK_CREDIT_REPORTS[id_number]
    return _generate_generic_report(id_number, name)


def get_identity_verification(
    id_number: str, name: str = None, dob: str = None
) -> dict:
    """returns mock identity verification results."""
    if id_number in MOCK_IDENTITY_RESULTS:
        return MOCK_IDENTITY_RESULTS[id_number]

    return {
        "match_found": True,
        "confidence": "medium",
        "verified_name": name or "Unknown",
        "verified_dob": dob or "unknown",
        "id_status": "valid - active",
        "discrepancies": [
            "unable to verify against primary source - fallback database used"
        ],
        "source": "Secondary verification database",
        "last_updated": "2025-06-01",
    }


def get_fraud_check(
    id_number: str, name: str = None, address: str = None
) -> dict:
    """returns mock fraud check results."""
    if id_number in MOCK_FRAUD_RESULTS:
        return MOCK_FRAUD_RESULTS[id_number]

    return {
        "fraud_risk_score": random.randint(5, 25),
        "risk_level": "low",
        "flags": [],
        "checks_performed": [
            "identity document validation",
            "known fraud database",
            "address verification",
            "device/IP screening",
        ],
        "details": "no fraud indicators detected.",
    }


def _generate_generic_report(id_number: str, name: str = None) -> dict:
    """generates a plausible generic credit report for unknown IDs."""
    score = random.randint(550, 750)
    if score >= 680:
        risk = "low"
    elif score >= 600:
        risk = "medium"
    else:
        risk = "high"

    return {
        "applicant": {
            "name": name or "Unknown Applicant",
            "id_number": id_number,
            "date_of_birth": "unknown",
        },
        "credit_score": score,
        "risk_rating": risk,
        "accounts": {
            "total_open": random.randint(1, 5),
            "total_closed": random.randint(0, 3),
            "details": [
                {
                    "type": "credit card",
                    "provider": "FNB",
                    "limit": 30000,
                    "balance": random.randint(5000, 25000),
                    "status": "current",
                    "opened": "2021-01-15",
                    "payment_history": "satisfactory",
                }
            ],
        },
        "payment_profile": {
            "on_time_percentage": round(random.uniform(85, 99), 1),
            "total_payments_tracked": random.randint(20, 80),
            "late_payments": random.randint(0, 5),
            "defaults": 0,
            "judgements": 0,
            "write_offs": 0,
        },
        "enquiry_history": {
            "last_30_days": random.randint(0, 2),
            "last_90_days": random.randint(0, 4),
            "last_12_months": random.randint(1, 6),
            "details": [],
        },
        "adverse_information": {
            "defaults": [],
            "judgements": [],
            "administration_orders": [],
            "sequestrations": [],
            "debt_review": False,
        },
        "total_monthly_obligations": random.randint(2000, 15000),
    }