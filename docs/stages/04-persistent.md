# Stage 4 — Persistent Agent

## Task

Investigate an incident or continue a repair across a forced process restart.

## Capability added

The system persists an append-only event log and a compact checkpoint, then reconstructs trustworthy state on resume. Retrieval supplies relevant prior context with provenance.

## Required behavior

- persist executed actions, observations, decisions, and status;
- resume without repeating completed work unnecessarily;
- distinguish retrieved historical context from current observation;
- invalidate stale assumptions after the environment changes;
- survive an interruption without accepting an incomplete finish;
- keep persistence deterministic before adding embeddings.

## Evaluation focus

- restart after partial investigation;
- corrupted or incomplete checkpoint;
- changed workspace after checkpoint creation;
- irrelevant retrieved memories;
- confirmation bias toward an early hypothesis.
