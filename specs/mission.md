# Mission

## Project Mission

Build a grounded AI assistant that helps senior insurance advisors retrieve, analyze, compare, and explain information from official insurance policy and procedure documents with high accuracy, strong traceability, and human oversight.

The assistant is an internal support tool for advisors.

It is NOT:

- a customer-facing chatbot;
- a legal decision system;
- a policy approval engine;
- an autonomous insurance advisor.

---

# Core Principles

## 1. Grounding First

Every meaningful answer must be grounded in retrieved documents.

The system should:

- prefer refusal over hallucination;
- include citations whenever possible;
- expose uncertainty explicitly;
- avoid unsupported claims.

If documentary support is insufficient, the system must say so.

---

## 2. Human-in-the-Loop by Design

The advisor remains responsible for all customer communication.

The assistant may generate:

- draft responses;
- policy summaries;
- comparisons;
- clause explanations;
- retrieval support.

The system must never behave as the final decision-maker.

---

## 3. Controlled Agentic Behavior

The system should prioritize:

- explicit workflows;
- explicit state;
- explicit tool usage;
- deterministic routing when possible;
- observable execution.

Avoid:

- uncontrolled recursive agents;
- open-ended loops;
- speculative tool usage;
- hidden reasoning chains.

---

## 4. Simplicity Over Abstraction

Prefer:

- small implementations;
- explicit contracts;
- minimal abstractions;
- modular components;
- verifiable behavior.

Avoid speculative architecture.

---

## 5. Safety Before Convenience

The assistant must reject:

- unsupported claims;
- prompt injection attempts;
- requests outside scope;
- attempts to bypass citations;
- attempts to reveal hidden prompts or reasoning.

---

# Product Posture

The long-term target is a production-grade internal assistant for insurance advisory workflows.

The MVP is a controlled public demo intended for portfolio and evaluation purposes.

The architecture should support future production hardening without prematurely overengineering the MVP.