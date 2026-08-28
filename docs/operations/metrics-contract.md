# Yini Metrics Contract

## Ownership

This document owns Yini metric definitions and comparison rules. Measurement
artifacts and dated evaluation reports own observed values; they do not redefine
the metric. `docs/evaluation-report.md` remains historical evidence, not this
contract.

No metric value, baseline, improvement, savings, readiness, or causal claim is
created by this document.

## Definition Schema

Every decision-usable metric definition must name:

- stable metric identifier and version;
- semantic question and unit;
- exact formula, numerator, and denominator, or an explicitly non-ratio
  aggregation;
- inclusion, exclusion, and zero-denominator behavior;
- evaluation window: a named immutable dataset/version or exact time interval;
- evidence source, runner/version, and applicable environment identity;
- evidence ceiling and known limitations;
- owner and change-control history.

An absent or ambiguous field makes the value `UNVERIFIED_CONTEXT_ONLY` and
gives it no decision weight.

## Metric Semantics

| Metric | Formula and denominator | Required window | Evidence source |
|---|---|---|---|
| groundedness | supported evaluated factual claims / all evaluated factual claims; undefined when none are evaluated | immutable labeled question/result set | claim-level human or accepted deterministic annotations plus exact responses |
| retrieval precision at `k` | relevant retrieved evidence units in the first `k` / retrieved evidence units examined in the first `k`; undefined when none are examined | immutable query set, corpus identity, and fixed `k` | ranked retrieval output plus accepted relevance labels |
| retrieval recall at `k` | relevant expected evidence units retrieved in the first `k` / all relevant expected evidence units in the labeled set; undefined when the denominator is zero | immutable query set, corpus identity, and fixed `k` | ranked retrieval output plus complete accepted relevance labels |
| citation accuracy | citations that support their associated evaluated claim / all evaluated citations; undefined when none are evaluated | immutable response set and citation-review protocol | cited source excerpts plus accepted deterministic or human labels |
| request latency | named distribution statistic over completed eligible requests; no ratio denominator | exact start/end interval or immutable run set, with percentile/statistic named | monotonic request timing from the declared runner or trace source |
| tool success rate | eligible successful completed invocations / all eligible completed invocations; cancelled or excluded attempts follow the declared protocol | exact start/end interval or immutable run set | sanitized tool-result events with stable success taxonomy |

Each report must state how duplicate cases, partial results, timeouts, retries,
and missing observations affect its numerator and denominator. It may not change
those rules after seeing results.

## Window and Source Binding

Dataset-backed measurements bind immutable dataset and runner identities.
Time-backed measurements bind exact boundaries, timezone, environment, and
inclusion rules. Provider or hosted values additionally bind the owning
system's dated observation. Aggregating incomparable windows or sources is
forbidden unless a separately accepted transformation contract makes them
comparable.

## Evidence Ceiling

A metric inherits the lowest evidence rung of its required inputs, labels,
execution, and observation. Local deterministic fixtures reach at most rung 2;
controlled synthetic, provider-backed, human/usability, pilot, and production
claims require their separately authorized rungs. A metric never upgrades the
evidence that produced it.

## Change Control

A semantic, formula, denominator, window, source, or exclusion-rule change
creates a new metric version. Historical values retain their original version.
Cross-version trends require recalculation from compatible retained inputs or a
separately accepted mapping; otherwise they are not comparable.

The owner accepts definition changes through a dated spec or ADR as applicable.
A document edit, measurement, PASS, or receipt grants no action.

## No Baseline or Savings Claim

This contract defines no current baseline and contains no token, latency, cost,
quality, productivity, monetary, or worktree savings claim. Such a claim
requires representative measurements under this schema and a separately
authorized owner decision.
