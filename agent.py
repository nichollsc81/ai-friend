"""claude agent orchestration for credit bureau assistant.

handles the conversational flow: extraction, validation, confirmation,
investigation, and summarisation.
"""

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

from mcp_server import (
    validate_id,
    verify_identity_check,
    credit_check,
    fraud_check,
    affordability_check,
)
from prompts import AGENT_SYSTEM_PROMPT

load_dotenv()

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

# tool definitions for the anthropic API
TOOLS = [
    {
        "name": "validate_id_number",
        "description": (
            "Validates a South African ID number's format and Luhn checksum. "
            "Extracts date of birth, gender, and citizenship status from the "
            "ID number."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "id_number": {
                    "type": "string",
                    "description": (
                        "The 13-digit South African ID number to validate"
                    ),
                }
            },
            "required": ["id_number"],
        },
    },
    {
        "name": "verify_identity",
        "description": (
            "Verifies an applicant's identity against the Department of Home "
            "Affairs registry. Returns match confidence and any discrepancies."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The applicant's full name",
                },
                "id_number": {
                    "type": "string",
                    "description": "The 13-digit South African ID number",
                },
                "dob": {
                    "type": "string",
                    "description": (
                        "Date of birth in YYYY-MM-DD format (optional)"
                    ),
                },
            },
            "required": ["name", "id_number"],
        },
    },
    {
        "name": "run_credit_check",
        "description": (
            "Runs a full credit bureau check. Returns credit score, risk "
            "rating, account details, payment history, enquiry history, and "
            "adverse information."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "id_number": {
                    "type": "string",
                    "description": "The 13-digit South African ID number",
                },
                "name": {
                    "type": "string",
                    "description": (
                        "The applicant's name (for record matching)"
                    ),
                },
                "product_type": {
                    "type": "string",
                    "description": (
                        "Type of credit product (e.g. personal loan, home "
                        "loan, credit card)"
                    ),
                },
                "requested_amount": {
                    "type": "number",
                    "description": "The credit amount requested in ZAR",
                },
            },
            "required": ["id_number"],
        },
    },
    {
        "name": "check_fraud",
        "description": (
            "Screens for fraud indicators, identity fraud flags, and "
            "blacklisted details. Returns a fraud risk score and any flags."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "id_number": {
                    "type": "string",
                    "description": "The 13-digit South African ID number",
                },
                "name": {
                    "type": "string",
                    "description": "The applicant's name",
                },
                "address": {
                    "type": "string",
                    "description": "The applicant's residential address",
                },
            },
            "required": ["id_number"],
        },
    },
    {
        "name": "assess_affordability",
        "description": (
            "Evaluates debt-to-income ratio and repayment capacity. "
            "Calculates whether the applicant can afford the requested credit "
            "based on income, expenses, and existing obligations."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_income": {
                    "type": "number",
                    "description": "Gross monthly income in ZAR",
                },
                "monthly_expenses": {
                    "type": "number",
                    "description": (
                        "Total monthly living expenses in ZAR"
                    ),
                },
                "existing_debt": {
                    "type": "number",
                    "description": (
                        "Total existing monthly debt payments in ZAR"
                    ),
                },
                "requested_amount": {
                    "type": "number",
                    "description": (
                        "The new credit amount being requested in ZAR"
                    ),
                },
                "loan_term_months": {
                    "type": "integer",
                    "description": (
                        "Loan repayment period in months (default: 60)"
                    ),
                },
                "interest_rate": {
                    "type": "number",
                    "description": (
                        "Annual interest rate as percentage (default: 15.0)"
                    ),
                },
            },
            "required": ["monthly_income"],
        },
    },
]

# map tool names to callable functions
TOOL_FUNCTIONS = {
    "validate_id_number": lambda args: validate_id(args["id_number"]),
    "verify_identity": lambda args: verify_identity_check(
        args["name"], args["id_number"], args.get("dob")
    ),
    "run_credit_check": lambda args: credit_check(
        args["id_number"],
        args.get("name"),
        args.get("product_type"),
        args.get("requested_amount"),
    ),
    "check_fraud": lambda args: fraud_check(
        args["id_number"], args.get("name"), args.get("address")
    ),
    "assess_affordability": lambda args: affordability_check(
        args["monthly_income"],
        args.get("monthly_expenses", 0),
        args.get("existing_debt", 0),
        args.get("requested_amount", 0),
        args.get("loan_term_months", 60),
        args.get("interest_rate", 15.0),
    ),
}


class CreditCheckAgent:
    """orchestrates the credit check workflow using claude and MCP tools."""

    def __init__(self):
        self.client = Anthropic()
        self.messages = []
        self.tool_call_log = []

    def process_message(self, user_message: str) -> dict:
        """processes a user message through the agent workflow.

        returns a dict with:
            - response: the assistant's text response
            - tool_calls: list of tool calls made this turn
        """
        self.messages.append({"role": "user", "content": user_message})

        tool_calls = []
        response = self._call_claude()

        # tool-use loop: keep going while claude wants to call tools
        while response.stop_reason == "tool_use":
            assistant_content = self._serialise_content(response.content)
            self.messages.append(
                {"role": "assistant", "content": assistant_content}
            )

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = self._execute_tool(block.name, block.input)
                    tool_calls.append(
                        {
                            "tool": block.name,
                            "input": block.input,
                            "output": result,
                        }
                    )
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        }
                    )

            self.messages.append({"role": "user", "content": tool_results})
            response = self._call_claude()

        # extract final text response
        text_response = ""
        for block in response.content:
            if block.type == "text":
                text_response += block.text

        # save final assistant message to conversation history
        assistant_content = self._serialise_content(response.content)
        self.messages.append(
            {"role": "assistant", "content": assistant_content}
        )

        self.tool_call_log.extend(tool_calls)

        return {"response": text_response, "tool_calls": tool_calls}

    def _call_claude(self):
        """makes an API call to claude with the current conversation and tools."""
        return self.client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=AGENT_SYSTEM_PROMPT,
            messages=self.messages,
            tools=TOOLS,
        )

    def _execute_tool(self, tool_name: str, tool_input: dict) -> dict:
        """executes a tool by name and returns the result."""
        if tool_name in TOOL_FUNCTIONS:
            try:
                return TOOL_FUNCTIONS[tool_name](tool_input)
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"unknown tool: {tool_name}"}

    def _serialise_content(self, content) -> list:
        """converts API response content blocks to serialisable dicts."""
        serialised = []
        for block in content:
            if block.type == "text":
                serialised.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                serialised.append(
                    {
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input,
                    }
                )
        return serialised

    def reset(self):
        """resets the conversation state."""
        self.messages = []
        self.tool_call_log = []