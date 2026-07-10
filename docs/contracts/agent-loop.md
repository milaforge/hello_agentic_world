# Agent-loop contract

The same loop is extended across all five stages:

```python
while state.actions_used < limits.max_actions:
    proposal = model.respond(state.messages, tools.available(state))
    action = host.validate(proposal)

    if action.is_finish:
        verdict = verifier.check(action, state.observations)
        if verdict.accepted:
            return completed(action, state, verdict)
        state.record_rejection(verdict)
        continue

    observation = host.execute(action)
    state.record(observation)

return failed("action_budget_exhausted", state)
```

## Invariants

1. Model output is a proposal, not an executed action.
2. Only registered tools can execute.
3. Validation occurs before every execution.
4. Tool results are recorded as immutable observations.
5. Rejected actions and rejected finish attempts consume budget.
6. Completion is accepted only by the host verifier.
7. Every run terminates with a declared status.
8. The agent never imports evaluation ground truth.
