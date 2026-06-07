# Validation — hosted-spaces-deployment-validation-and-evidence

## Intended Validation

- Confirm one real hosted deployment exists.
- Confirm the hosted deployment evidence includes Space URL, deployed commit
  SHA, and actual smoke results.
- Confirm the evidence is durable and specific.

## Executed Checks

- Recorded real hosted deployment evidence from the Hugging Face Space
  container log at `2026-06-07 22:57:11`, including:
  - `startup_diagnostics`
  - `health_check_succeeded`
  - `readiness_check_succeeded`
  - internal `GET /gradio_api/startup-events` → `200 OK`
  - internal `HEAD /` → `200 OK`
- Confirmed the hosted runtime bound successfully on `0.0.0.0:7860`.
- Confirmed public accessibility with external checks:
  - `https://huggingface.co/spaces/Diegoavelez/Yini-insurance-advisor` → `HTTP 200`
  - `https://diegoavelez-yini-insurance-advisor.hf.space` → `HTTP 200`

## Status

- Completed.
