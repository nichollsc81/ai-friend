"""MCP server exposing credit bureau tools via FastMCP.

can be run standalone: python mcp_server.py
or imported by agent.py for direct function calls.
"""

import json
import re
from datetime import date

from mcp.server.fastmcp import FastMCP

from mock_api import get_credit_report, get_identity_verification, get_fraud_check


# --- core tool functions (importable by agent.py) ---


def validate_id(id_number: str) -> dict:
    """validates a south african ID number format, checksum, and extracts demographics."""
    errors = []
    result = {
        "valid": False,
        "id_number": id_number,
        "date_of_birth": None,
        "gender": None,
        "citizenship": None,
        "errors": errors,
    }

    # check format
    if not re.match(r"^\d{13}$", id_number):
        errors.append("ID number must be exactly 13 digits")
        return result

    # extract components
    year = int(id_number[0:2])
    month = int(id_number[2:4])
    day = int(id_number[4:6])
    sequence = int(id_number[6:10])
    citizenship_digit = int(id_number[10])

    # determine century (pivot at current year)
    current_year_short = date.today().year % 100
    full_year = 2000 + year if year <= current_year_short else 1900 + year

    # validate date of birth
    try:
        dob = date(full_year, month, day)
        result["date_of_birth"] = dob.isoformat()
    except ValueError:
        errors.append(f"invalid date of birth: {full_year}-{month:02d}-{day:02d}")

    # extract gender
    result["gender"] = "male" if sequence >= 5000 else "female"

    # extract citizenship
    if citizenship_digit == 0:
        result["citizenship"] = "SA citizen"
    elif citizenship_digit == 1:
        result["citizenship"] = "permanent resident"
    else:
        errors.append(f"invalid citizenship digit: {citizenship_digit}")

    # luhn checksum validation
    if not _luhn_check(id_number):
        errors.append("ID number fails checksum validation (Luhn algorithm)")

    result["valid"] = len(errors) == 0
    return result


def verify_identity_check(name: str, id_number: str, dob: str = None) -> dict:
    """verifies applicant identity against the home affairs registry."""
    return get_identity_verification(id_number, name, dob)


def credit_check(
    id_number: str,
    name: str = None,
    product_type: str = None,
    requested_amount: float = None,
) -> dict:
    """runs a full credit bureau check."""
    report = get_credit_report(id_number, name)
    if product_type:
        report["enquiry_context"] = {
            "product_type": product_type,
            "requested_amount": requested_amount,
        }
    return report


def fraud_check(id_number: str, name: str = None, address: str = None) -> dict:
    """checks for fraud indicators and blacklisted details."""
    return get_fraud_check(id_number, name, address)


def affordability_check(
    monthly_income: float,
    monthly_expenses: float = 0,
    existing_debt: float = 0,
    requested_amount: float = 0,
    loan_term_months: int = 60,
    interest_rate: float = 15.0,
) -> dict:
    """evaluates debt-to-income ratio and repayment capacity."""
    # estimate new monthly instalment using simple amortisation
    if requested_amount > 0 and loan_term_months > 0:
        monthly_rate = interest_rate / 100 / 12
        if monthly_rate > 0:
            new_instalment = requested_amount * (
                monthly_rate * (1 + monthly_rate) ** loan_term_months
            ) / ((1 + monthly_rate) ** loan_term_months - 1)
        else:
            new_instalment = requested_amount / loan_term_months
    else:
        new_instalment = 0

    total_obligations = existing_debt + new_instalment
    disposable_income = monthly_income - monthly_expenses
    dti_current = existing_debt / monthly_income if monthly_income > 0 else 0
    dti_proposed = total_obligations / monthly_income if monthly_income > 0 else 0
    surplus = disposable_income - total_obligations

    # NCA guideline: DTI should not exceed ~45%
    affordable = dti_proposed <= 0.45 and surplus > 0

    return {
        "affordable": affordable,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "existing_monthly_debt": existing_debt,
        "estimated_new_instalment": round(new_instalment, 2),
        "total_monthly_obligations": round(total_obligations, 2),
        "disposable_income": round(disposable_income, 2),
        "monthly_surplus_after_new_debt": round(surplus, 2),
        "debt_to_income_current": round(dti_current * 100, 1),
        "debt_to_income_proposed": round(dti_proposed * 100, 1),
        "nca_threshold": "45%",
        "assessment": _affordability_assessment(dti_proposed, surplus),
        "breakdown": {
            "requested_amount": requested_amount,
            "loan_term_months": loan_term_months,
            "interest_rate_annual": interest_rate,
            "estimated_monthly_instalment": round(new_instalment, 2),
        },
    }


def _luhn_check(number: str) -> bool:
    """validates a number using the luhn algorithm."""
    digits = [int(d) for d in number]
    # from the rightmost digit, double every second digit moving left
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0


def _affordability_assessment(dti: float, surplus: float) -> str:
    """returns a human-readable affordability assessment."""
    if dti <= 0.30 and surplus > 5000:
        return (
            "comfortable - debt-to-income ratio is well within acceptable "
            "limits with healthy surplus"
        )
    elif dti <= 0.40 and surplus > 2000:
        return (
            "adequate - debt-to-income ratio is acceptable with reasonable surplus"
        )
    elif dti <= 0.45 and surplus > 0:
        return (
            "marginal - debt-to-income ratio is near the upper limit; "
            "limited financial buffer"
        )
    elif surplus <= 0:
        return "unaffordable - insufficient income to cover all obligations"
    else:
        return (
            "exceeds guidelines - debt-to-income ratio exceeds the "
            "recommended 45% threshold"
        )


# --- FastMCP server setup ---

mcp = FastMCP("credit-bureau")


@mcp.tool()
def validate_id_number(id_number: str) -> str:
    """validates a south african ID number's format and checksum.
    extracts date of birth, gender, and citizenship status.

    args:
        id_number: the 13-digit south african ID number to validate
    """
    return json.dumps(validate_id(id_number), indent=2)


@mcp.tool()
def verify_identity(name: str, id_number: str, dob: str = "") -> str:
    """verifies an applicant's identity against the home affairs registry.

    args:
        name: the applicant's full name
        id_number: the 13-digit south african ID number
        dob: date of birth in YYYY-MM-DD format (optional)
    """
    return json.dumps(
        verify_identity_check(name, id_number, dob or None), indent=2
    )


@mcp.tool()
def run_credit_check(
    id_number: str,
    name: str = "",
    product_type: str = "",
    requested_amount: float = 0,
) -> str:
    """runs a full credit bureau check returning score, accounts, payment history,
    enquiry history, and adverse information.

    args:
        id_number: the 13-digit south african ID number
        name: the applicant's name (optional, for record matching)
        product_type: type of credit product being applied for (optional)
        requested_amount: the amount being requested in ZAR (optional)
    """
    return json.dumps(
        credit_check(
            id_number,
            name or None,
            product_type or None,
            requested_amount or None,
        ),
        indent=2,
    )


@mcp.tool()
def check_fraud(
    id_number: str, name: str = "", address: str = ""
) -> str:
    """screens for fraud indicators, identity fraud flags, and blacklisted details.

    args:
        id_number: the 13-digit south african ID number
        name: the applicant's name (optional)
        address: the applicant's address (optional, for address verification)
    """
    return json.dumps(
        fraud_check(id_number, name or None, address or None), indent=2
    )


@mcp.tool()
def assess_affordability(
    monthly_income: float,
    monthly_expenses: float = 0,
    existing_debt: float = 0,
    requested_amount: float = 0,
    loan_term_months: int = 60,
    interest_rate: float = 15.0,
) -> str:
    """evaluates debt-to-income ratio and repayment capacity based on income,
    expenses, and existing obligations.

    args:
        monthly_income: gross monthly income in ZAR
        monthly_expenses: total monthly living expenses in ZAR (optional)
        existing_debt: total existing monthly debt payments in ZAR (optional)
        requested_amount: the new credit amount being requested in ZAR (optional)
        loan_term_months: loan repayment period in months (default: 60)
        interest_rate: annual interest rate as percentage (default: 15.0)
    """
    return json.dumps(
        affordability_check(
            monthly_income,
            monthly_expenses,
            existing_debt,
            requested_amount,
            loan_term_months,
            interest_rate,
        ),
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()