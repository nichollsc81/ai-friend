# CLAUDE.md — AI Hackathon Brainstorm Session

## About Me
I am a **Product Manager at a credit bureau**. I am participating in an internal hackathon
focused on implementing AI (LLMs, agents, MCP, etc.) into our existing product workflow.

Use this file to maintain context across our brainstorming sessions so you can give me
consistent, informed, and progressively deeper ideas.

---

## Our Core Product

### What It Does
A UI-based product used by **credit providers** (banks, lenders, retailers, etc.) to
perform credit checks on their customers. The user (typically a credit analyst or
onboarding agent) inputs customer details into a front-end interface which calls our
**credit bureau API**.

### Typical Input Data (Customer Details Submitted)
- Personal: Full name, ID number, date of birth
- Contact: Address (current & historical), phone, email
- Financial: Bank account details, salary/income details, employment info
- Request: Credit amount requested, product type (loan, card, etc.)

### What Our API Returns (Credit Report)
- Credit score / risk rating
- Payment history (on-time, late, defaults)
- Open and closed accounts
- Enquiry history (how often they've been credit-checked)
- Adverse information (judgements, write-offs, sequestrations)
- Derived risk flags

### Current Workflow (No AI)
1. Credit agent opens UI
2. Manually enters or pastes customer details
3. Submits → API call → credit report returned
4. Agent reads through the report
5. Agent or downstream system makes a credit decision

---

## Hackathon Goal

Identify and prototype **meaningful AI integrations** into this workflow using:
- **LLMs** (e.g. Claude) for reasoning, summarisation, generation
- **Agents** for multi-step autonomous task execution
- **MCP (Model Context Protocol)** for tool/API connectivity
- Any combination of the above

The goal is a **working demo or proof of concept** — not production-ready code.
Bias towards ideas that are **impressive, feasible in a hackathon timeframe, and
genuinely useful** to real users.

---

## Constraints & Considerations to Keep in Mind

- **Data privacy is critical** — customer PII and financial data must be handled carefully.
  Flag any idea that has meaningful privacy risk.
- **Regulated environment** — credit decisions in most jurisdictions are subject to
  regulation (e.g. explainability requirements, fair lending laws). Flag ideas where
  regulatory risk is non-trivial.
- **We own the API** — we can expose any endpoints we want as MCP tools.
- **We do not make the final credit decision** — we provide the data/report;
  the lender decides. Keep this in mind when scoping agent autonomy.
- **Users are non-technical** — the UI is used by credit analysts and onboarding agents,
  not developers.
- **Hackathon timeframe** — prefer ideas that can be demoed in days, not weeks.

---

## Brainstorming Preferences

When I ask you to generate or evaluate ideas, please structure your thinking around:

1. **The problem it solves** — what pain point or inefficiency does this address?
2. **The AI approach** — LLM, agent, MCP tool, RAG, etc.?
3. **Rough implementation path** — what would the demo look like?
4. **Privacy / regulatory flags** — any risks to call out?
5. **Hackathon feasibility** — high / medium / low, and why?

Feel free to challenge my assumptions, push back on weak ideas, and connect dots
between ideas across sessions.

---

## Session Log (Update as we go)

### Ideas Explored
- [x] AI credit report summarisation (narrative layer)
- [x] Conversational data entry agent (NLP → structured fields)
- [x] Decision-support reasoning agent (advisory, regulatory concerns noted)
- [x] Anomaly detection & fraud flagging (input vs report comparison)
- [x] MCP multi-tool research agent (autonomous multi-endpoint orchestration)

### Ideas Parked / Deprioritised
- Decision-support reasoning agent — highest regulatory risk, better as a phase 2

### Leading Candidate(s)
- **#2 + #1 + #5 combo:** Conversational input → MCP agent with 5 tools (validate, verify identity, credit check, fraud check, affordability) → AI narrative summary. Full plan in `.claude/plans/sprightly-forging-raven.md`

---

## How to Use This File

- Keep this file updated as we refine ideas across sessions.
- When I start a session with "let's brainstorm", use this full context to ground your responses.
- When I say "log it", add the idea to the Session Log above.
- When I say "go deep on [idea]", produce a detailed breakdown: user story, architecture,
  MCP tool design, agent flow, and a sketch of the demo script.