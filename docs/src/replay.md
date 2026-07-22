# Run Replay

<div class="rr" data-state="empty" data-playing="false">
  <section class="rr-toolbar" aria-label="Load a run">
    <div class="rr-field">
      <label for="rr-sample-select">Scenario</label>
      <div class="rr-select-wrap">
        <select id="rr-sample-select"><option value="">Loading scenarios…</option></select>
      </div>
    </div>
    <span class="rr-separator" aria-hidden="true">or</span>
    <label class="rr-file-button" for="rr-run-file">
      <svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 14v4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4" /></svg>
      <span>Load JSON</span>
      <input id="rr-run-file" type="file" accept="application/json,.json" />
    </label>
  </section>
  <section class="rr-run" aria-live="polite">
    <header class="rr-run-header">
      <div class="rr-outcome-icon" id="rr-outcome-icon" aria-hidden="true"></div>
      <div class="rr-run-heading">
        <div class="rr-status-line"><span id="rr-status-badge" class="rr-status-badge rr-neutral">No run loaded</span><span id="rr-run-id" class="rr-run-id"></span></div>
        <h2 id="rr-run-title">Choose a scenario</h2>
        <p id="rr-run-summary">Load a saved run to see its outcome, root cause, and tool calls without reading the raw trace.</p>
      </div>
    </header>
    <dl class="rr-run-meta">
      <div><dt>Scenario</dt><dd id="rr-scenario">—</dd></div>
      <div><dt>Model</dt><dd id="rr-model">—</dd></div>
      <div><dt>Tool calls</dt><dd id="rr-call-count">—</dd></div>
    </dl>
    <div id="rr-insights" class="rr-insights" aria-label="Run insights"></div>
  </section>
  <section class="rr-replay" aria-label="Step replay">
    <div class="rr-section-heading">
      <div><span class="rr-section-kicker">Execution</span><h3>Tool-call timeline</h3></div>
      <span id="rr-step-count" class="rr-step-count">0 / 0</span>
    </div>
    <nav id="rr-stepper" class="rr-stepper" aria-label="Execution steps"></nav>
    <article id="rr-step-card" class="rr-step-card rr-neutral">
      <header class="rr-step-header">
        <div id="rr-tool-icon" class="rr-tool-icon" aria-hidden="true"></div>
        <div class="rr-step-heading"><span id="rr-step-label" class="rr-step-label">No step selected</span><h3 id="rr-step-title">Load a run to inspect its execution</h3><p id="rr-step-target" class="rr-step-target"></p></div>
        <div class="rr-step-actions">
          <button id="rr-open-details" class="rr-details-button" type="button" aria-label="Open step details" title="Open step details" disabled><svg aria-hidden="true" viewBox="0 0 24 24" width="17" height="17"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01" /></svg></button>
          <span id="rr-step-status" class="rr-step-status rr-neutral">—</span>
        </div>
      </header>
      <div id="rr-step-body" class="rr-step-body"><p class="rr-empty-copy">Each tool call appears once, with its action and result combined.</p></div>
    </article>
    <nav class="rr-controls" aria-label="Replay controls">
      <button id="rr-back" type="button" aria-label="Previous step"><svg aria-hidden="true" viewBox="0 0 24 24" width="17" height="17"><path d="m14.5 6-6 6 6 6" /></svg><span>Back</span></button>
      <button id="rr-play" class="rr-primary" type="button" aria-label="Play replay">
        <span class="rr-play-visual" aria-hidden="true">
          <svg class="rr-play-progress-ring" viewBox="0 0 36 36" width="32" height="32"><rect class="rr-play-progress-track" x="5" y="5" width="26" height="26" rx="8" pathLength="100"></rect><rect id="rr-play-progress-value" class="rr-play-progress-value" x="5" y="5" width="26" height="26" rx="8" pathLength="100"></rect></svg>
          <svg class="rr-play-icon" aria-hidden="true" viewBox="0 0 24 24" width="17" height="17"><path d="m8 5 11 7-11 7V5Z" /></svg>
          <svg class="rr-pause-icon" aria-hidden="true" viewBox="0 0 24 24" width="17" height="17"><path d="M9 5v14M15 5v14" /></svg>
        </span>
        <span id="rr-play-label" class="rr-sr-only">Play</span>
      </button>
      <button id="rr-next" type="button" aria-label="Next step"><span>Next</span><svg aria-hidden="true" viewBox="0 0 24 24" width="17" height="17"><path d="m9.5 6 6 6-6 6" /></svg></button>
    </nav>
  </section>
  <dialog id="rr-modal" class="rr-modal" aria-labelledby="rr-modal-title">
    <div class="rr-modal-card">
      <header class="rr-modal-header">
        <div><span class="rr-section-kicker">Step details</span><h3 id="rr-modal-title">Execution detail</h3><p id="rr-modal-subtitle"></p></div>
        <button id="rr-close-modal" class="rr-modal-close" type="button" aria-label="Close details"><svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path d="m7 7 10 10M17 7 7 17" /></svg></button>
      </header>
      <div class="rr-modal-body">
        <div id="rr-modal-extra" class="rr-modal-extra"></div>
        <section class="rr-modal-json-section" aria-label="Raw step JSON">
          <div class="rr-modal-section-heading"><h4>Raw JSON</h4><button id="rr-copy-json" class="rr-copy" type="button" aria-label="Copy step JSON" disabled>Copy JSON</button></div>
          <pre class="rr-json" tabindex="0"><code id="rr-step-json">{}</code></pre>
        </section>
      </div>
    </div>
  </dialog>
  <p id="rr-announcer" class="rr-sr-only" aria-live="polite"></p>
</div>
