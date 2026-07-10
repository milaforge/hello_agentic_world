# Completion contract

`finish` is a terminal proposal, not a normal tool.

A completion proposal must contain:

- a structured result;
- evidence references;
- any stage-specific verification fields.

The host rejects completion when:

- an evidence reference does not exist;
- a claim contradicts an observation;
- required coverage is missing;
- a declared postcondition has not been checked;
- policy requires an approval that is absent;
- the action or retry budget has already been exhausted.

The rejection is added to the trace so the agent can recover when budget remains.
