(() => {
  const root = document.querySelector(".rr");
  if (!root || root.dataset.initialized === "true") return;
  root.dataset.initialized = "true";

  const ICONS = {
    check: '<svg viewBox="0 0 24 24" width="21" height="21"><path d="m5 12 4 4L19 6" /></svg>',
    x: '<svg viewBox="0 0 24 24" width="21" height="21"><path d="m7 7 10 10M17 7 7 17" /></svg>',
    info: '<svg viewBox="0 0 24 24" width="21" height="21"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01" /></svg>',
    warning: '<svg viewBox="0 0 24 24" width="19" height="19"><path d="M12 3 2.8 20h18.4L12 3Z"/><path d="M12 9v4M12 16h.01" /></svg>',
    folder: '<svg viewBox="0 0 24 24" width="19" height="19"><path d="M3 6.5h6l2 2h10v9.5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6.5Z" /></svg>',
    file: '<svg viewBox="0 0 24 24" width="19" height="19"><path d="M6 3h8l4 4v14H6V3Z"/><path d="M14 3v5h5" /></svg>',
    finish: '<svg viewBox="0 0 24 24" width="19" height="19"><path d="M5 21V4M6 5h11l-2 4 2 4H6" /></svg>',
    tool: '<svg viewBox="0 0 24 24" width="19" height="19"><path d="M14.5 6.5a4 4 0 0 0-5-5l2.2 2.2-2 2-2.2-2.2a4 4 0 0 0 5 5L20 16l-4 4-7.5-7.5" /></svg>',
    pulse: '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M3 12h4l2-6 4 12 2-6h6" /></svg>',
    evidence: '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M7 12.5 10 15l7-7"/><path d="M5 3h14v18H5z" /></svg>',
    repeat: '<svg viewBox="0 0 24 24" width="14" height="14"><path d="m17 2 4 4-4 4M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4M21 13v2a3 3 0 0 1-3 3H3" /></svg>'
  };

  const state = { run: null, steps: [], index: 0, timer: null, raf: null, tickStartedAt: 0, playbackMs: 1500 };
  const elements = {
    sampleSelect: document.getElementById("rr-sample-select"), runFile: document.getElementById("rr-run-file"), runPanel: document.getElementById("rr-run-panel"), replayPanel: document.getElementById("rr-replay-panel"), outcomeIcon: document.getElementById("rr-outcome-icon"), statusBadge: document.getElementById("rr-status-badge"), runId: document.getElementById("rr-run-id"), runTitle: document.getElementById("rr-run-title"), runSummary: document.getElementById("rr-run-summary"), scenario: document.getElementById("rr-scenario"), model: document.getElementById("rr-model"), callCount: document.getElementById("rr-call-count"), insights: document.getElementById("rr-insights"), stepCount: document.getElementById("rr-step-count"), stepper: document.getElementById("rr-stepper"), stepCard: document.getElementById("rr-step-card"), toolIcon: document.getElementById("rr-tool-icon"), stepLabel: document.getElementById("rr-step-label"), stepTitle: document.getElementById("rr-step-title"), stepTarget: document.getElementById("rr-step-target"), stepStatus: document.getElementById("rr-step-status"), stepBody: document.getElementById("rr-step-body"), openDetails: document.getElementById("rr-open-details"), modal: document.getElementById("rr-modal"), modalTitle: document.getElementById("rr-modal-title"), modalSubtitle: document.getElementById("rr-modal-subtitle"), modalExtra: document.getElementById("rr-modal-extra"), closeModal: document.getElementById("rr-close-modal"), backButton: document.getElementById("rr-back"), playButton: document.getElementById("rr-play"), playLabel: document.getElementById("rr-play-label"), playProgressValue: document.getElementById("rr-play-progress-value"), nextButton: document.getElementById("rr-next"), stepJson: document.getElementById("rr-step-json"), copyJson: document.getElementById("rr-copy-json"), announcer: document.getElementById("rr-announcer")
  };

  /* Formatting helpers */
  function setPanelsVisible({ run, replay }) { elements.runPanel.hidden = !run; elements.replayPanel.hidden = !replay; }
  function escapeHtml(value) { return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;"); }
  function escapeCode(value) { return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;"); }
  function asText(value, fallback = "—") { if (value === null || value === undefined || value === "") return fallback; return typeof value === "string" ? value : JSON.stringify(value); }
  function humanize(value) { return asText(value, "Unknown").replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase()); }
  function formatBytes(value) { if (!Number.isFinite(Number(value))) return "—"; const bytes = Number(value); if (bytes < 1000) return `${bytes} B`; const units = ["kB", "MB", "GB"]; let amount = bytes; let unit = "B"; for (const next of units) { amount /= 1000; unit = next; if (amount < 1000) break; } return `${amount.toFixed(amount >= 10 ? 0 : 1)} ${unit}`; }
  function scenarioLabel(request) { const labels = { basic: "Basic workspace", empty: "Empty workspace", ignore_venv: "Ignore virtual environment" }; return labels[request] || humanize(request); }
  function errorLabel(error) { if (!error) return "Unknown error"; if (error.startsWith("no_progress_duplicate_action:")) return `Repeated ${error.split(":")[1]} blocked`; const labels = { step_budget_exhausted: "Step budget exhausted", unknown_tool: "Unknown tool", path_does_not_exist: "Path does not exist", invalid_arguments: "Invalid arguments" }; return labels[error] || humanize(error); }
  function errorExplanation(error) { if (!error) return "The tool call failed without an error code."; if (error.startsWith("no_progress_duplicate_action:")) return "The no-progress guard stopped the agent before it repeated the same action again."; const labels = { step_budget_exhausted: "The agent used every allowed step without producing a valid final result.", unknown_tool: "The model output did not match any registered tool call.", path_does_not_exist: "The requested path was not present in the observed workspace.", invalid_arguments: "The submitted tool arguments did not satisfy the tool schema." }; return labels[error] || "The operation returned an error."; }
  function toolTitle(name) { const labels = { list_directory: "Scan directory", get_file_metadata: "Inspect file", finish: "Submit final result", invalid_model_response: "Invalid model response" }; return labels[name] || humanize(name || "Unknown tool"); }
  function toolIcon(name) { if (name === "list_directory") return ICONS.folder; if (name === "get_file_metadata") return ICONS.file; if (name === "finish") return ICONS.finish; if (name === "invalid_model_response") return ICONS.warning; return ICONS.tool; }
  function stepSignature(observation) { return JSON.stringify({ call: observation.call || null, result: observation.result || null }); }

  /* Run model */
  function groupObservations(observations) {
    const groups = [];
    for (const observation of Array.isArray(observations) ? observations : []) {
      const signature = stepSignature(observation);
      const previous = groups.at(-1);
      if (previous && previous.signature === signature) {
        previous.repeatCount += 1;
        previous.stepEnd = observation.step ?? previous.stepEnd + 1;
        previous.ids.push(observation.id);
        previous.observations.push(observation);
      } else {
        groups.push({ signature, observation, observations: [observation], repeatCount: 1, stepStart: observation.step ?? groups.length + 1, stepEnd: observation.step ?? groups.length + 1, ids: [observation.id] });
      }
    }
    return groups;
  }

  function runCounts(run) {
    const observations = Array.isArray(run.observations) ? run.observations : [];
    const succeeded = observations.filter((item) => item.result?.ok === true).length;
    const failed = observations.filter((item) => item.result?.ok === false).length;
    return { total: observations.length, succeeded, failed };
  }

  function runHeadline(run) {
    if (run.status === "completed") {
      const count = run.final_result?.python_file_count;
      if (count === 0) return "No Python files found";
      if (Number.isFinite(Number(count))) return `Found ${count} Python file${Number(count) === 1 ? "" : "s"}`;
      return "Run completed";
    }
    if (run.error?.startsWith("no_progress_duplicate_action:")) return "Stopped by the no-progress guard";
    if (run.error === "step_budget_exhausted") return "Step budget exhausted";
    return "Run failed";
  }

  function runSummary(run) {
    if (run.status === "completed") {
      const size = formatBytes(run.final_result?.total_size_bytes);
      const evidence = Array.isArray(run.final_result?.evidence) ? run.final_result.evidence.length : 0;
      return `Total size ${size}. The final result references ${evidence} observation${evidence === 1 ? "" : "s"} as evidence.`;
    }
    return errorExplanation(run.error);
  }

  function deriveInsights(run) {
    const counts = runCounts(run);
    const observations = Array.isArray(run.observations) ? run.observations : [];
    const firstFailure = observations.find((item) => item.result?.ok === false);
    const repeatedInvalid = observations.filter((item) => item.call?.name === "invalid_model_response" && item.result?.error === "unknown_tool").length;
    const evidence = Array.isArray(run.final_result?.evidence) ? run.final_result.evidence : [];
    const failedFinish = observations.find((item) => item.call?.name === "finish" && item.result?.ok === false);
    const insights = [];

    if (run.status === "completed") {
      insights.push({ label: "Result", value: `${run.final_result?.python_file_count ?? "—"} Python file${run.final_result?.python_file_count === 1 ? "" : "s"} · ${formatBytes(run.final_result?.total_size_bytes)}`, tone: "success", icon: ICONS.check });
      insights.push({ label: "Execution", value: `${counts.succeeded}/${counts.total} tool calls succeeded`, tone: counts.failed ? "warning" : "success", icon: ICONS.pulse });
      insights.push({ label: "Evidence", value: evidence.length ? evidence.join(", ") : "No evidence references", tone: evidence.length ? "neutral" : "warning", icon: ICONS.evidence });
    } else {
      insights.push({ label: "Terminal reason", value: errorLabel(run.error), tone: "failure", icon: ICONS.x });
      insights.push({ label: "Execution", value: `${counts.succeeded} succeeded · ${counts.failed} failed`, tone: counts.failed ? "failure" : "neutral", icon: ICONS.pulse });
      if (repeatedInvalid > 1) insights.push({ label: "Failure pattern", value: `${repeatedInvalid} identical protocol failures`, tone: "warning", icon: ICONS.repeat });
      else if (failedFinish) insights.push({ label: "Finish rejected", value: errorLabel(failedFinish.result?.error), tone: "warning", icon: ICONS.warning });
      else if (firstFailure) insights.push({ label: "First failure", value: `Step ${firstFailure.step}: ${errorLabel(firstFailure.result?.error)}`, tone: "warning", icon: ICONS.warning });
    }

    return insights.slice(0, 3);
  }

  /* Run rendering */
  function renderInsights(run) {
    elements.insights.innerHTML = deriveInsights(run).map((insight) => `<div class="rr-insight rr-${insight.tone}"><div class="rr-insight-label">${insight.icon}<span>${escapeHtml(insight.label)}</span></div><div class="rr-insight-value">${escapeHtml(insight.value)}</div></div>`).join("");
  }

  function stepTone(step) { return step.observation.result?.ok === true ? "success" : step.observation.result?.ok === false ? "failure" : "neutral"; }
  function stepRange(step) { return step.repeatCount > 1 ? `Steps ${step.stepStart}–${step.stepEnd}` : `Step ${step.stepStart}`; }
  function callTarget(observation) { const args = observation.call?.arguments || {}; if (typeof args.path === "string") return args.path; if (observation.call?.name === "finish") return "Final answer and evidence"; return Object.keys(args).length ? Object.keys(args).join(", ") : ""; }

  /* Step rendering */
  function renderDirectoryResult(observation) {
    const value = observation.result?.value || {};
    const entries = Array.isArray(value.entries) ? value.entries : [];
    const files = entries.filter((entry) => entry.kind === "file").length;
    const directories = entries.filter((entry) => entry.kind === "directory").length;
    return `<div class="rr-result-grid"><div class="rr-result-metric"><span>Path</span><strong class="rr-code">${escapeHtml(value.path ?? observation.call?.arguments?.path ?? ".")}</strong></div><div class="rr-result-metric"><span>Files</span><strong>${files}</strong></div><div class="rr-result-metric"><span>Directories</span><strong>${directories}</strong></div></div>`;
  }

  function renderMetadataResult(observation) {
    const value = observation.result?.value || {};
    return `<div class="rr-result-grid"><div class="rr-result-metric"><span>Path</span><strong class="rr-code">${escapeHtml(value.path ?? observation.call?.arguments?.path ?? "—")}</strong></div><div class="rr-result-metric"><span>Type</span><strong>${escapeHtml(value.kind ?? "—")}</strong></div><div class="rr-result-metric"><span>Size</span><strong>${escapeHtml(formatBytes(value.size_bytes))}</strong></div></div>`;
  }

  function renderFinishResult(observation) {
    const value = observation.result?.value || observation.call?.arguments || {};
    const evidence = Array.isArray(value.evidence) ? value.evidence : [];
    return `<div class="rr-result-grid"><div class="rr-result-metric"><span>Python files</span><strong>${escapeHtml(value.python_file_count ?? "—")}</strong></div><div class="rr-result-metric"><span>Total size</span><strong>${escapeHtml(formatBytes(value.total_size_bytes))}</strong></div><div class="rr-result-metric"><span>Evidence</span><strong>${evidence.length}</strong></div></div>`;
  }

  function renderFailure(step) {
    const observation = step.observation;
    const error = observation.result?.error;
    if (observation.call?.name === "finish") {
      const submitted = observation.call?.arguments || {};
      const evidence = Array.isArray(submitted.evidence) ? submitted.evidence : [];
      const observationIds = new Set((state.run?.observations || []).map((item) => item.id));
      const validEvidence = evidence.filter((item) => observationIds.has(item)).length;
      return `<div class="rr-result-grid"><div class="rr-result-metric"><span>Error</span><strong>${escapeHtml(errorLabel(error))}</strong></div><div class="rr-result-metric"><span>Submitted count</span><strong>${escapeHtml(submitted.python_file_count ?? "—")}</strong></div><div class="rr-result-metric"><span>Valid evidence</span><strong>${validEvidence}/${evidence.length}</strong></div></div>`;
    }
    return `<div class="rr-result-grid"><div class="rr-result-metric"><span>Error</span><strong>${escapeHtml(errorLabel(error))}</strong></div><div class="rr-result-metric"><span>Code</span><strong class="rr-code">${escapeHtml(error ?? "—")}</strong></div><div class="rr-result-metric"><span>Occurrences</span><strong>${step.repeatCount}</strong></div></div>`;
  }

  function renderStepBody(step) {
    const observation = step.observation;
    if (observation.result?.ok === false) return renderFailure(step);
    const name = observation.call?.name;
    if (name === "list_directory") return renderDirectoryResult(observation);
    if (name === "get_file_metadata") return renderMetadataResult(observation);
    if (name === "finish") return renderFinishResult(observation);
    const value = observation.result?.value;
    return `<div class="rr-result-metric"><span>Result</span><strong>${escapeHtml(value === null || value === undefined ? "Completed" : asText(value))}</strong></div>`;
  }

  /* Modal rendering */
  function renderModalExtra(step) {
    const observation = step.observation;
    const name = observation.call?.name;
    const sections = [];

    if (step.repeatCount > 1) {
      sections.push(`<div class="rr-modal-notice">${ICONS.repeat}<div><strong>Repeated pattern</strong><p>${step.repeatCount} consecutive identical calls were collapsed into this single timeline step.</p></div></div>`);
    }

    if (observation.result?.ok === false) {
      sections.push(`<div class="rr-error-box">${ICONS.warning}<div><strong>${escapeHtml(errorLabel(observation.result?.error))}</strong><p>${escapeHtml(errorExplanation(observation.result?.error))}</p><p class="rr-code">${escapeHtml(observation.result?.error ?? "unknown_error")}</p></div></div>`);
    }

    if (name === "list_directory") {
      const entries = Array.isArray(observation.result?.value?.entries) ? observation.result.value.entries : [];
      const request = state.run?.request;
      const chips = entries.map((entry) => {
        const ignored = request === "ignore_venv" && (entry.path === ".venv" || entry.path?.startsWith(".venv/"));
        return `<span class="rr-entry">${entry.kind === "directory" ? ICONS.folder : ICONS.file}<span>${escapeHtml(entry.path)}</span>${ignored ? "<em>ignored</em>" : ""}</span>`;
      }).join("");
      sections.push(`<div class="rr-modal-group"><h4>Directory entries · ${entries.length}</h4>${chips ? `<div class="rr-entry-list">${chips}</div>` : '<p>No entries returned.</p>'}</div>`);
    }

    if (name === "finish") {
      const submitted = observation.result?.value || observation.call?.arguments || {};
      const evidence = Array.isArray(submitted.evidence) ? submitted.evidence : [];
      sections.push(`<div class="rr-modal-group"><h4>Final answer</h4><p>${escapeHtml(asText(submitted.answer, "No answer submitted."))}</p></div>`);
      sections.push(`<div class="rr-modal-group"><h4>Evidence · ${evidence.length}</h4>${evidence.length ? `<div class="rr-entry-list">${evidence.map((item) => `<span class="rr-entry">${ICONS.evidence}<span>${escapeHtml(item)}</span></span>`).join("")}</div>` : '<p>No evidence references submitted.</p>'}</div>`);
    }

    if (!sections.length) sections.push('<div class="rr-modal-group"><h4>No additional summary</h4><p>The complete observation is available in the raw JSON below.</p></div>');
    return sections.join("");
  }

  function openStepDetails() {
    const step = state.steps[state.index];
    if (!step) return;
    const observation = step.observation;
    elements.modalTitle.textContent = `${stepRange(step)} · ${toolTitle(observation.call?.name)}`;
    elements.modalSubtitle.textContent = callTarget(observation) || "Complete observation";
    elements.modalExtra.innerHTML = renderModalExtra(step);
    elements.stepJson.innerHTML = highlightedJson(currentPayload());
    if (typeof elements.modal.showModal === "function") elements.modal.showModal();
    else elements.modal.setAttribute("open", "");
    elements.closeModal.focus();
  }

  function closeStepDetails() {
    if (typeof elements.modal.close === "function" && elements.modal.open) elements.modal.close();
    else elements.modal.removeAttribute("open");
    elements.openDetails.focus();
  }

  function renderStepper() {
    elements.stepper.innerHTML = state.steps.map((step, index) => {
      const tone = stepTone(step);
      const label = step.repeatCount > 1 ? `${step.stepStart}–${step.stepEnd}` : String(step.stepStart);
      const repeat = step.repeatCount > 1 ? `<small>×${step.repeatCount}</small>` : "";
      return `<button class="rr-step-dot rr-${tone}" type="button" data-index="${index}" aria-label="${escapeHtml(stepRange(step))}: ${escapeHtml(toolTitle(step.observation.call?.name))}"${index === state.index ? ' aria-current="step"' : ""}>${escapeHtml(label)}${repeat}</button>`;
    }).join("");
  }

  function highlightedJson(value) {
    const json = JSON.stringify(value, null, 2) ?? "null";
    const escaped = escapeCode(json);
    return escaped.replace(/("(?:\\u[a-fA-F0-9]{4}|\\[^u]|[^\\"])*"\s*:)|("(?:\\u[a-fA-F0-9]{4}|\\[^u]|[^\\"])*")|\b(true|false)\b|\b(null)\b|(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)/g, (match, key, string, boolean, nullValue, number) => { if (key) return `<span class="key">${key}</span>`; if (string) return `<span class="string">${string}</span>`; if (boolean) return `<span class="boolean">${boolean}</span>`; if (nullValue) return `<span class="null">${nullValue}</span>`; if (number) return `<span class="number">${number}</span>`; return match; });
  }

  /* Playback state */
  function currentPayload() { return state.steps[state.index]?.repeatCount > 1 ? state.steps[state.index].observations : state.steps[state.index]?.observation ?? {}; }
  function replayFraction() { if (state.steps.length < 2) return state.steps.length === 1 ? 1 : 0; const lastIndex = state.steps.length - 1; let fraction = state.index / lastIndex; if (state.timer !== null && state.index < lastIndex) { const elapsed = Math.max(0, performance.now() - state.tickStartedAt); fraction += Math.min(elapsed / state.playbackMs, 1) / lastIndex; } return Math.max(0, Math.min(fraction, 1)); }
  function updatePlayProgress() { const fraction = replayFraction(); elements.playProgressValue.style.strokeDashoffset = String(100 * (1 - fraction)); const remaining = Math.max(0, Math.round((1 - fraction) * 100)); elements.playButton.title = state.timer !== null ? `Replay in progress — ${remaining}% left` : "Play replay"; }
  function syncPlaybackProgress() { updatePlayProgress(); if (state.timer === null) return; state.raf = window.requestAnimationFrame(syncPlaybackProgress); }
  function setPlaying(playing) { root.dataset.playing = String(playing); elements.playLabel.textContent = playing ? "Pause" : "Play"; elements.playButton.setAttribute("aria-label", playing ? "Pause replay" : "Play replay"); }
  function setControlsDisabled(disabled) { elements.backButton.disabled = disabled || state.index <= 0; elements.nextButton.disabled = disabled || state.index >= state.steps.length - 1; elements.playButton.disabled = disabled || state.steps.length < 2; elements.openDetails.disabled = disabled; elements.copyJson.disabled = disabled; }
  function stop() { if (state.timer !== null) window.clearInterval(state.timer); if (state.raf !== null) window.cancelAnimationFrame(state.raf); state.timer = null; state.raf = null; setPlaying(false); updatePlayProgress(); }

  /* Main screen rendering */
  function renderRun() {
    const run = state.run;
    const counts = runCounts(run);
    const completed = run.status === "completed";
    root.dataset.state = completed ? "completed" : "failed";
    elements.outcomeIcon.innerHTML = completed ? ICONS.check : ICONS.x;
    elements.statusBadge.className = `rr-status-badge rr-${completed ? "success" : "failure"}`;
    elements.statusBadge.textContent = completed ? "Completed" : "Failed";
    elements.runId.textContent = run.run_id || "";
    elements.runTitle.textContent = runHeadline(run);
    elements.runSummary.textContent = runSummary(run);
    elements.scenario.textContent = scenarioLabel(run.request);
    elements.scenario.title = elements.scenario.textContent;
    elements.model.textContent = asText(run.model);
    elements.model.title = elements.model.textContent;
    elements.callCount.textContent = state.steps.length === counts.total ? String(counts.total) : `${counts.total} · ${state.steps.length} pattern${state.steps.length === 1 ? "" : "s"}`;
    renderInsights(run);
  }

  function renderStep() {
    const step = state.steps[state.index];
    const hasStep = Boolean(step);
    setControlsDisabled(!hasStep);
    renderStepper();
    if (!hasStep) return;
    const observation = step.observation;
    const tone = stepTone(step);
    elements.stepCard.className = `rr-step-card rr-${tone}`;
    elements.toolIcon.innerHTML = toolIcon(observation.call?.name);
    elements.stepLabel.textContent = step.repeatCount > 1 ? `${stepRange(step)} · ×${step.repeatCount} identical` : stepRange(step);
    elements.stepTitle.textContent = toolTitle(observation.call?.name);
    elements.stepTarget.textContent = callTarget(observation);
    elements.stepStatus.className = `rr-step-status rr-${tone}`;
    elements.stepStatus.textContent = observation.result?.ok === true ? "Success" : observation.result?.ok === false ? "Failed" : "Unknown";
    elements.stepBody.innerHTML = renderStepBody(step);
    elements.stepCount.textContent = `${state.index + 1} / ${state.steps.length}`;
    elements.stepJson.innerHTML = highlightedJson(currentPayload());
    elements.announcer.textContent = `${stepRange(step)}: ${toolTitle(observation.call?.name)}, ${elements.stepStatus.textContent}`;
    elements.stepper.querySelector('[aria-current="step"]')?.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
    updatePlayProgress();
  }

  function loadRun(run) {
    if (!run || typeof run !== "object" || Array.isArray(run)) throw new TypeError("The JSON root must be an object.");
    stop();
    if (elements.modal.open) elements.modal.close();
    setPanelsVisible({ run: true, replay: true });
    state.run = run;
    state.steps = groupObservations(run.observations);
    state.index = 0;
    renderRun();
    if (state.steps.length) {
      renderStep();
    } else {
      elements.stepper.innerHTML = "";
      elements.stepCount.textContent = "0 / 0";
      elements.stepCard.className = "rr-step-card rr-neutral";
      elements.toolIcon.innerHTML = ICONS.info;
      elements.stepLabel.textContent = "No tool calls";
      elements.stepTitle.textContent = "The run contains no observations";
      elements.stepTarget.textContent = "";
      elements.stepStatus.className = "rr-step-status rr-neutral";
      elements.stepStatus.textContent = "Empty";
      elements.stepBody.innerHTML = '<p class="rr-empty-copy">There are no execution steps to replay.</p>';
      elements.stepJson.innerHTML = highlightedJson({});
      setControlsDisabled(true);
    }
  }

  function showMessage(title, summary) {
    stop();
    root.dataset.state = "error";
    setPanelsVisible({ run: true, replay: false });
    elements.outcomeIcon.innerHTML = ICONS.x;
    elements.statusBadge.className = "rr-status-badge rr-failure";
    elements.statusBadge.textContent = "Load error";
    elements.runTitle.textContent = title;
    elements.runSummary.textContent = summary;
    elements.runId.textContent = "";
    elements.scenario.textContent = "—";
    elements.model.textContent = "—";
    elements.callCount.textContent = "—";
    elements.insights.innerHTML = "";
    state.run = null;
    state.steps = [];
    state.index = 0;
    renderStepper();
    elements.stepCount.textContent = "0 / 0";
    setControlsDisabled(true);
  }

  async function loadManifest() { const response = await fetch("replay/manifest.json", { cache: "no-store" }); if (!response.ok) throw new Error(`Manifest request failed with HTTP ${response.status}.`); return response.json(); }
  async function loadPublishedRun(filename) { const response = await fetch(`replay/runs/${encodeURIComponent(filename)}`, { cache: "no-store" }); if (!response.ok) throw new Error(`Run request failed with HTTP ${response.status}.`); loadRun(await response.json()); }
  function step(direction) { stop(); if (elements.modal.open) elements.modal.close(); const next = state.index + direction; if (next < 0 || next >= state.steps.length) return; state.index = next; renderStep(); }

  /* Event wiring */
  elements.sampleSelect.addEventListener("change", () => { const filename = elements.sampleSelect.value; if (!filename) return; elements.sampleSelect.disabled = true; loadPublishedRun(filename).catch((error) => showMessage("Could not load scenario", error.message)).finally(() => { elements.sampleSelect.disabled = false; }); });
  elements.runFile.addEventListener("change", async () => { const file = elements.runFile.files?.[0]; if (!file) return; try { loadRun(JSON.parse(await file.text())); elements.sampleSelect.value = ""; } catch (error) { showMessage("Invalid run JSON", `${file.name}: ${error.message}`); } finally { elements.runFile.value = ""; } });
  elements.backButton.addEventListener("click", () => step(-1));
  elements.nextButton.addEventListener("click", () => step(1));
  elements.stepper.addEventListener("click", (event) => { const button = event.target.closest("button[data-index]"); if (!button) return; stop(); if (elements.modal.open) elements.modal.close(); state.index = Number(button.dataset.index); renderStep(); });
  elements.openDetails.addEventListener("click", openStepDetails);
  elements.closeModal.addEventListener("click", closeStepDetails);
  elements.modal.addEventListener("click", (event) => { if (event.target === elements.modal) closeStepDetails(); });
  elements.playButton.addEventListener("click", () => { if (state.timer !== null) { stop(); return; } if (state.index >= state.steps.length - 1) { state.index = 0; renderStep(); } setPlaying(true); state.tickStartedAt = performance.now(); updatePlayProgress(); state.raf = window.requestAnimationFrame(syncPlaybackProgress); state.timer = window.setInterval(() => { if (state.index >= state.steps.length - 1) { stop(); return; } state.index += 1; state.tickStartedAt = performance.now(); renderStep(); }, state.playbackMs); });
  elements.copyJson.addEventListener("click", async (event) => { event.preventDefault(); event.stopPropagation(); try { await navigator.clipboard.writeText(JSON.stringify(currentPayload(), null, 2)); const label = elements.copyJson.textContent; elements.copyJson.textContent = "Copied"; elements.announcer.textContent = "Step JSON copied."; window.setTimeout(() => { elements.copyJson.textContent = label; }, 1200); } catch { elements.announcer.textContent = "Could not copy step JSON."; } });
  root.addEventListener("keydown", (event) => { if (event.target.closest("input, select, button, summary")) return; if (event.key === "ArrowLeft") { event.preventDefault(); step(-1); } else if (event.key === "ArrowRight") { event.preventDefault(); step(1); } else if (event.key === " ") { event.preventDefault(); elements.playButton.click(); } });

  updatePlayProgress();
  setControlsDisabled(true);
  loadManifest().then((manifest) => { const runs = Array.isArray(manifest.runs) ? manifest.runs : []; elements.sampleSelect.textContent = ""; elements.sampleSelect.appendChild(new Option(runs.length ? "Choose a scenario…" : "No scenarios found", "")); for (const run of runs) { if (!run?.file) continue; elements.sampleSelect.appendChild(new Option(run.title || run.file, run.file)); } }).catch((error) => { elements.sampleSelect.textContent = ""; elements.sampleSelect.appendChild(new Option("Scenarios unavailable", "")); showMessage("Could not load saved scenarios", error.message); });
})();
