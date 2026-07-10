# Tool protocol

Every tool has:

- a unique name;
- a typed input schema;
- an authorization check;
- deterministic host execution where practical;
- a structured success or error result;
- an observation record.

A tool must not combine planning with execution. Prefer narrow capabilities such as `list_directory(path)` over open shell access.

Tool errors are observations. They are returned to the model in a structured form and remain visible to the evaluator.
