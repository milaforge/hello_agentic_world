# Stage 2 — File Detective

## Task

Answer bounded repository questions such as:

> Where is application configuration loaded, which sources can override it, and what evidence supports that conclusion?

New capabilities may include:

```text
read_file(path, start_line, end_line)
search_text(query, path)
```

## Capability added

The agent must investigate before concluding. It tracks candidate hypotheses, unanswered questions, inspected areas, and evidence coverage.

## Required behavior

- distinguish a hypothesis from an observed fact;
- read only bounded file ranges;
- cite observations for every material conclusion;
- identify uncertainty when available evidence is incomplete;
- avoid finishing after finding only the first plausible match.

## Evaluation focus

- decoy configuration files;
- dead code and comments that resemble active behavior;
- multiple override layers;
- plausible but incomplete conclusions;
- unnecessary exploration and budget waste.
