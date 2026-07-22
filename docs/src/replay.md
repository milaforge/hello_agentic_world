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

<style>
.rr {
  --rr-blue: var(--links, #2769a5);
  --rr-green: #17834f;
  --rr-red: #c43d45;
  --rr-amber: #a86f13;
  --rr-border: color-mix(in srgb, var(--fg) 13%, transparent);
  --rr-border-strong: color-mix(in srgb, var(--fg) 21%, transparent);
  --rr-surface: color-mix(in srgb, var(--bg) 96%, var(--fg) 4%);
  --rr-surface-raised: color-mix(in srgb, var(--bg) 91%, var(--fg) 9%);
  --rr-muted: color-mix(in srgb, var(--fg) 62%, transparent);
  display: grid;
  gap: 1rem;
  max-width: 58rem;
  margin: 1.5rem 0 2.5rem;
  color: var(--fg);
}

.rr *, .rr *::before, .rr *::after { box-sizing: border-box; }
.rr-toolbar, .rr-run, .rr-replay { border: 1px solid var(--rr-border); border-radius: 16px; background: var(--rr-surface); }
.rr svg { fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }

.rr-toolbar {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto auto;
  align-items: end;
  gap: .85rem;
  padding: .9rem;
}

.rr-field { display: grid; gap: .4rem; min-width: 0; }
.rr-field > label, .rr-run-meta dt, .rr-section-kicker {
  color: var(--rr-muted);
  font-size: .7rem;
  font-weight: 750;
  letter-spacing: .065em;
  line-height: 1;
  text-transform: uppercase;
}

.rr-select-wrap { position: relative; }
.rr-select-wrap::after { content: ""; position: absolute; top: 50%; right: .95rem; width: .5rem; height: .5rem; border-right: 1.5px solid currentColor; border-bottom: 1.5px solid currentColor; pointer-events: none; transform: translateY(-70%) rotate(45deg); opacity: .65; }
#rr-sample-select, .rr-file-button, .rr-controls button, .rr-copy, .rr-details-button, .rr-modal-close { border: 1px solid var(--rr-border-strong); background: var(--bg); color: var(--fg); font: inherit; }
#rr-sample-select { width: 100%; min-height: 2.85rem; appearance: none; border-radius: 10px; padding: .62rem 2.5rem .62rem .8rem; cursor: pointer; }
.rr-separator { align-self: center; margin-top: 1.05rem; color: var(--rr-muted); font-size: .78rem; }
.rr-file-button { display: inline-flex; align-items: center; justify-content: center; gap: .45rem; min-height: 2.85rem; border-radius: 10px; padding: .62rem .95rem; cursor: pointer; font-size: .9rem; font-weight: 700; white-space: nowrap; transition: border-color 140ms ease, background-color 140ms ease, transform 140ms ease; }
.rr-file-button input { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; }
.rr-file-button:hover, .rr-controls button:not(:disabled):hover, .rr-copy:not(:disabled):hover, .rr-details-button:not(:disabled):hover, .rr-modal-close:hover { border-color: color-mix(in srgb, var(--rr-blue) 65%, var(--rr-border)); background: var(--rr-surface-raised); }
.rr-file-button:active, .rr-controls button:not(:disabled):active { transform: translateY(1px); }

.rr-run { overflow: hidden; }
.rr-run-header { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 1rem; align-items: start; padding: clamp(1.2rem, 3vw, 1.75rem); }
.rr-outcome-icon { display: grid; place-items: center; width: 2.75rem; height: 2.75rem; border-radius: 12px; background: color-mix(in srgb, var(--rr-blue) 12%, transparent); color: var(--rr-blue); }
.rr[data-state="completed"] .rr-outcome-icon { background: color-mix(in srgb, var(--rr-green) 13%, transparent); color: var(--rr-green); }
.rr[data-state="failed"] .rr-outcome-icon, .rr[data-state="error"] .rr-outcome-icon { background: color-mix(in srgb, var(--rr-red) 12%, transparent); color: var(--rr-red); }
.rr-status-line { display: flex; align-items: center; gap: .6rem; min-height: 1.6rem; }
.rr-status-badge, .rr-step-status { display: inline-flex; align-items: center; gap: .35rem; width: fit-content; border-radius: 999px; padding: .28rem .55rem; font-size: .7rem; font-weight: 760; letter-spacing: .035em; text-transform: uppercase; }
.rr-neutral { color: var(--rr-muted); background: color-mix(in srgb, var(--fg) 7%, transparent); }
.rr-success { color: var(--rr-green); background: color-mix(in srgb, var(--rr-green) 12%, transparent); }
.rr-failure { color: var(--rr-red); background: color-mix(in srgb, var(--rr-red) 11%, transparent); }
.rr-warning { color: var(--rr-amber); background: color-mix(in srgb, var(--rr-amber) 12%, transparent); }
.rr-run-id { color: var(--rr-muted); font-family: var(--mono-font, ui-monospace, monospace); font-size: .72rem; overflow-wrap: anywhere; }
.rr-run h2 { margin: .35rem 0 0; font-size: clamp(1.45rem, 3vw, 2rem); font-weight: 730; letter-spacing: -.035em; line-height: 1.15; }
.rr-run-summary { max-width: 46rem; margin: .55rem 0 0; color: color-mix(in srgb, var(--fg) 78%, transparent); line-height: 1.55; }
.rr-run-meta { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; margin: 0; background: var(--rr-border); border-top: 1px solid var(--rr-border); border-bottom: 1px solid var(--rr-border); }
.rr-run-meta > div { min-width: 0; padding: .9rem 1.1rem; background: var(--rr-surface); }
.rr-run-meta dd { margin: .35rem 0 0; font-size: .9rem; font-weight: 680; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.rr-insights { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .75rem; padding: 1rem; }
.rr-insight { min-width: 0; border: 1px solid var(--rr-border); border-radius: 12px; padding: .8rem .85rem; background: var(--bg); }
.rr-insight-label { display: flex; align-items: center; gap: .38rem; color: var(--rr-muted); font-size: .68rem; font-weight: 760; letter-spacing: .05em; text-transform: uppercase; }
.rr-insight-label svg { width: 14px; height: 14px; }
.rr-insight-value { margin-top: .42rem; font-size: .88rem; font-weight: 690; line-height: 1.35; overflow-wrap: anywhere; }
.rr-insight.rr-success { border-color: color-mix(in srgb, var(--rr-green) 25%, var(--rr-border)); }
.rr-insight.rr-failure { border-color: color-mix(in srgb, var(--rr-red) 25%, var(--rr-border)); }
.rr-insight.rr-warning { border-color: color-mix(in srgb, var(--rr-amber) 25%, var(--rr-border)); }

.rr-replay { display: grid; grid-template-rows: auto auto 12.5rem auto; gap: .85rem; padding: clamp(.9rem, 2.2vw, 1.2rem); }
.rr-section-heading { display: flex; justify-content: space-between; align-items: end; gap: 1rem; }
.rr-section-heading h3 { margin: .3rem 0 0; font-size: 1.05rem; letter-spacing: -.015em; }
.rr-step-count { flex: 0 0 auto; color: var(--rr-muted); font-size: .78rem; font-weight: 700; font-variant-numeric: tabular-nums; }
.rr-stepper { display: flex; gap: .45rem; overflow-x: auto; padding: .1rem 0 .35rem; scrollbar-width: thin; }
.rr-step-dot { position: relative; display: inline-flex; align-items: center; justify-content: center; min-width: 2rem; height: 2rem; border: 1px solid var(--rr-border-strong); border-radius: 9px; background: var(--bg); color: var(--rr-muted); cursor: pointer; font: inherit; font-size: .72rem; font-weight: 760; transition: border-color 140ms ease, background-color 140ms ease, transform 140ms ease; }
.rr-step-dot:hover { transform: translateY(-1px); }
.rr-step-dot.rr-success { border-color: color-mix(in srgb, var(--rr-green) 42%, var(--rr-border)); color: var(--rr-green); }
.rr-step-dot.rr-failure { border-color: color-mix(in srgb, var(--rr-red) 42%, var(--rr-border)); color: var(--rr-red); }
.rr-step-dot[aria-current="step"] { outline: 3px solid color-mix(in srgb, currentColor 18%, transparent); outline-offset: 1px; background: var(--rr-surface-raised); }
.rr-step-dot small { position: absolute; top: -.4rem; right: -.35rem; min-width: 1.15rem; height: 1.15rem; border-radius: 999px; padding: 0 .22rem; background: var(--rr-red); color: #fff; font-size: .58rem; line-height: 1.15rem; text-align: center; }

.rr-step-card { display: grid; grid-template-rows: auto minmax(0, 1fr); height: 12.5rem; border: 1px solid var(--rr-border); border-left: 4px solid var(--rr-border-strong); border-radius: 14px; background: var(--bg); overflow: hidden; }
.rr-step-card.rr-success { border-left-color: var(--rr-green); }
.rr-step-card.rr-failure { border-left-color: var(--rr-red); }
.rr-step-card.rr-warning { border-left-color: var(--rr-amber); }
.rr-step-header { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; gap: .8rem; align-items: center; min-height: 4.65rem; padding: .8rem 1rem; border-bottom: 1px solid var(--rr-border); }
.rr-tool-icon { display: grid; place-items: center; width: 2.35rem; height: 2.35rem; border-radius: 10px; color: var(--rr-blue); background: color-mix(in srgb, var(--rr-blue) 10%, transparent); }
.rr-step-card.rr-success .rr-tool-icon { color: var(--rr-green); background: color-mix(in srgb, var(--rr-green) 10%, transparent); }
.rr-step-card.rr-failure .rr-tool-icon { color: var(--rr-red); background: color-mix(in srgb, var(--rr-red) 9%, transparent); }
.rr-step-label { color: var(--rr-muted); font-size: .7rem; font-weight: 740; letter-spacing: .055em; text-transform: uppercase; }
.rr-step-heading h3 { margin: .22rem 0 0; font-size: 1.02rem; font-weight: 720; overflow-wrap: anywhere; }
.rr-step-target { margin: .25rem 0 0; color: var(--rr-muted); font-family: var(--mono-font, ui-monospace, monospace); font-size: .78rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.rr-step-actions { display: inline-flex; align-items: center; gap: .5rem; }
.rr-details-button, .rr-modal-close { display: inline-grid; place-items: center; width: 2rem; height: 2rem; border-radius: 9px; padding: 0; cursor: pointer; }
.rr-details-button:disabled { cursor: not-allowed; opacity: .38; }
.rr-step-body { display: grid; align-items: center; min-height: 0; padding: .8rem 1rem; overflow: hidden; }
.rr-empty-copy { margin: 0; color: var(--rr-muted); }
.rr-result-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .65rem; }
.rr-result-metric { min-width: 0; padding: .72rem .75rem; border-radius: 10px; background: var(--rr-surface); }
.rr-result-metric span { display: block; color: var(--rr-muted); font-size: .68rem; font-weight: 730; letter-spacing: .045em; text-transform: uppercase; }
.rr-result-metric strong { display: -webkit-box; margin-top: .28rem; overflow: hidden; font-size: .92rem; line-height: 1.25; overflow-wrap: anywhere; -webkit-box-orient: vertical; -webkit-line-clamp: 2; }
.rr-entry-list { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: .8rem; }
.rr-entry { display: inline-flex; align-items: center; gap: .35rem; min-width: 0; border: 1px solid var(--rr-border); border-radius: 8px; padding: .35rem .5rem; color: color-mix(in srgb, var(--fg) 82%, transparent); background: var(--rr-surface); font-family: var(--mono-font, ui-monospace, monospace); font-size: .74rem; }
.rr-entry svg { width: 13px; height: 13px; flex: 0 0 auto; }
.rr-entry em { color: var(--rr-amber); font-family: inherit; font-size: .65rem; font-style: normal; }
.rr-error-box { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: .7rem; align-items: start; border-radius: 11px; padding: .8rem; background: color-mix(in srgb, var(--rr-red) 7%, transparent); color: var(--rr-red); }
.rr-error-box svg { width: 19px; height: 19px; }
.rr-error-box strong { display: block; }
.rr-error-box p { margin: .25rem 0 0; color: color-mix(in srgb, var(--fg) 76%, transparent); font-size: .86rem; line-height: 1.45; }
.rr-code { font-family: var(--mono-font, ui-monospace, monospace); font-size: .78rem; }

.rr-controls { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .65rem; }
.rr-controls button { display: inline-flex; align-items: center; justify-content: center; gap: .42rem; min-height: 2.8rem; border-radius: 10px; padding: .65rem .9rem; cursor: pointer; font-size: .88rem; font-weight: 720; transition: border-color 140ms ease, background-color 140ms ease, opacity 140ms ease, transform 140ms ease; }
.rr-controls button:disabled, .rr-copy:disabled { cursor: not-allowed; opacity: .38; }
.rr-controls .rr-primary { border-color: var(--rr-blue); background: var(--rr-blue); color: #fff; }
.rr-controls .rr-primary:not(:disabled):hover { border-color: var(--rr-blue); background: color-mix(in srgb, var(--rr-blue) 88%, #000); }
#rr-play { gap: 0; padding-inline: .9rem; }
.rr-play-visual { --rr-play-visual-size: 2rem; position: relative; display: inline-grid; place-items: center; width: var(--rr-play-visual-size); height: var(--rr-play-visual-size); flex: 0 0 var(--rr-play-visual-size); overflow: hidden; }
.rr-play-progress-ring { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; transform: rotate(-90deg); opacity: 0; transition: opacity 180ms ease; }
.rr-play-progress-track, .rr-play-progress-value { fill: none; stroke-width: 2.2; }
.rr-play-progress-track { stroke: color-mix(in srgb, #fff 26%, transparent); }
.rr-play-progress-value { stroke: #fff; stroke-linecap: round; stroke-dasharray: 100; stroke-dashoffset: 100; transition: stroke-dashoffset 120ms linear; }
#rr-play .rr-play-icon, #rr-play .rr-pause-icon { position: absolute; top: 50%; left: 50%; width: 1.05rem; height: 1.05rem; transform: translate(-50%, -50%); }
#rr-play .rr-play-icon { transform: translate(calc(-50% + .04rem), -50%); }
.rr-play-icon path { fill: currentColor; stroke: currentColor; }
.rr-pause-icon { display: none; }
.rr[data-playing="true"] .rr-play-icon { display: none; }
.rr[data-playing="true"] .rr-pause-icon { display: block; }
.rr[data-playing="true"] .rr-play-progress-ring { opacity: 1; }

.rr-modal { width: min(46rem, calc(100vw - 2rem)); max-width: none; max-height: min(82vh, 44rem); border: 0; padding: 0; background: transparent; color: var(--fg); }
.rr-modal::backdrop { background: color-mix(in srgb, #000 54%, transparent); backdrop-filter: blur(3px); }
.rr-modal-card { display: grid; grid-template-rows: auto minmax(0, 1fr); max-height: min(82vh, 44rem); overflow: hidden; border: 1px solid var(--rr-border-strong); border-radius: 16px; background: var(--bg); box-shadow: 0 24px 80px color-mix(in srgb, #000 28%, transparent); }
.rr-modal-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; padding: 1rem 1.1rem; border-bottom: 1px solid var(--rr-border); }
.rr-modal-header h3 { margin: .3rem 0 0; font-size: 1.1rem; }
.rr-modal-header p { margin: .25rem 0 0; color: var(--rr-muted); font-family: var(--mono-font, ui-monospace, monospace); font-size: .78rem; overflow-wrap: anywhere; }
.rr-modal-body { min-height: 0; overflow: auto; padding: 1rem; }
.rr-modal-extra { display: grid; gap: .75rem; }
.rr-modal-notice { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: .65rem; align-items: start; border-radius: 11px; padding: .8rem; background: color-mix(in srgb, var(--rr-amber) 7%, transparent); color: var(--rr-amber); }
.rr-modal-notice p { margin: .18rem 0 0; color: color-mix(in srgb, var(--fg) 76%, transparent); font-size: .86rem; line-height: 1.45; }
.rr-modal-group { border: 1px solid var(--rr-border); border-radius: 12px; padding: .85rem; background: var(--rr-surface); }
.rr-modal-group h4, .rr-modal-section-heading h4 { margin: 0; font-size: .86rem; }
.rr-modal-group p { margin: .45rem 0 0; color: color-mix(in srgb, var(--fg) 78%, transparent); line-height: 1.5; }
.rr-modal-json-section { margin-top: .9rem; }
.rr-modal-section-heading { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-bottom: .55rem; }
.rr-copy { border-radius: 8px; padding: .35rem .6rem; cursor: pointer; font-size: .72rem; font-weight: 700; }
.rr-json { margin: 0; max-height: 24rem; border: 1px solid var(--rr-border); border-radius: 11px; background: color-mix(in srgb, var(--bg) 97%, #000 3%); padding: 1.15rem; overflow: auto; color: var(--fg); font-family: var(--mono-font, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace); font-size: .82rem; line-height: 1.65; tab-size: 2; white-space: pre; word-break: normal; overflow-wrap: normal; }
.rr-json code { display: block; min-width: max-content; padding: 0; background: transparent; color: inherit; }
.rr-json .key { color: #7c65d1; } .rr-json .string { color: #15815d; } .rr-json .number { color: #bc5b11; } .rr-json .boolean { color: #276fc2; } .rr-json .null { color: #8a667a; }
.ayu .rr-json .key, .coal .rr-json .key, .navy .rr-json .key { color: #b8a5ff; }
.ayu .rr-json .string, .coal .rr-json .string, .navy .rr-json .string { color: #85d6b1; }
.ayu .rr-json .number, .coal .rr-json .number, .navy .rr-json .number { color: #f4ae70; }
.ayu .rr-json .boolean, .coal .rr-json .boolean, .navy .rr-json .boolean { color: #7eb6ff; }
.ayu .rr-json .null, .coal .rr-json .null, .navy .rr-json .null { color: #c39ab3; }
.rr :focus-visible { outline: 3px solid color-mix(in srgb, var(--rr-blue) 30%, transparent); outline-offset: 2px; }
.rr-sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }

@media (max-width: 760px) {
  .rr-insights, .rr-run-meta { grid-template-columns: 1fr; }
  .rr-toolbar { grid-template-columns: 1fr; align-items: stretch; }
  .rr-separator { display: none; }
}

@media (max-width: 480px) {
  .rr-run-header { grid-template-columns: 1fr; }
  .rr-outcome-icon { width: 2.4rem; height: 2.4rem; }
  .rr-step-header { grid-template-columns: auto minmax(0, 1fr) auto; gap: .55rem; }
  .rr-step-actions { gap: .3rem; }
  .rr-step-status { padding-inline: .42rem; }
  .rr-result-grid { gap: .4rem; }
  .rr-result-metric { padding: .6rem .55rem; }
  .rr-controls button span:not(.rr-play-visual) { display: none; }
}

@media (prefers-reduced-motion: reduce) {
  .rr *, .rr *::before, .rr *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; }
}
</style>

<script>
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
    sampleSelect: document.getElementById("rr-sample-select"), runFile: document.getElementById("rr-run-file"), outcomeIcon: document.getElementById("rr-outcome-icon"), statusBadge: document.getElementById("rr-status-badge"), runId: document.getElementById("rr-run-id"), runTitle: document.getElementById("rr-run-title"), runSummary: document.getElementById("rr-run-summary"), scenario: document.getElementById("rr-scenario"), model: document.getElementById("rr-model"), callCount: document.getElementById("rr-call-count"), insights: document.getElementById("rr-insights"), stepCount: document.getElementById("rr-step-count"), stepper: document.getElementById("rr-stepper"), stepCard: document.getElementById("rr-step-card"), toolIcon: document.getElementById("rr-tool-icon"), stepLabel: document.getElementById("rr-step-label"), stepTitle: document.getElementById("rr-step-title"), stepTarget: document.getElementById("rr-step-target"), stepStatus: document.getElementById("rr-step-status"), stepBody: document.getElementById("rr-step-body"), openDetails: document.getElementById("rr-open-details"), modal: document.getElementById("rr-modal"), modalTitle: document.getElementById("rr-modal-title"), modalSubtitle: document.getElementById("rr-modal-subtitle"), modalExtra: document.getElementById("rr-modal-extra"), closeModal: document.getElementById("rr-close-modal"), backButton: document.getElementById("rr-back"), playButton: document.getElementById("rr-play"), playLabel: document.getElementById("rr-play-label"), playProgressValue: document.getElementById("rr-play-progress-value"), nextButton: document.getElementById("rr-next"), stepJson: document.getElementById("rr-step-json"), copyJson: document.getElementById("rr-copy-json"), announcer: document.getElementById("rr-announcer")
  };

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

  function renderInsights(run) {
    elements.insights.innerHTML = deriveInsights(run).map((insight) => `<div class="rr-insight rr-${insight.tone}"><div class="rr-insight-label">${insight.icon}<span>${escapeHtml(insight.label)}</span></div><div class="rr-insight-value">${escapeHtml(insight.value)}</div></div>`).join("");
  }

  function stepTone(step) { return step.observation.result?.ok === true ? "success" : step.observation.result?.ok === false ? "failure" : "neutral"; }
  function stepRange(step) { return step.repeatCount > 1 ? `Steps ${step.stepStart}–${step.stepEnd}` : `Step ${step.stepStart}`; }
  function callTarget(observation) { const args = observation.call?.arguments || {}; if (typeof args.path === "string") return args.path; if (observation.call?.name === "finish") return "Final answer and evidence"; return Object.keys(args).length ? Object.keys(args).join(", ") : ""; }

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

  function currentPayload() { return state.steps[state.index]?.repeatCount > 1 ? state.steps[state.index].observations : state.steps[state.index]?.observation ?? {}; }
  function replayFraction() { if (state.steps.length < 2) return state.steps.length === 1 ? 1 : 0; const lastIndex = state.steps.length - 1; let fraction = state.index / lastIndex; if (state.timer !== null && state.index < lastIndex) { const elapsed = Math.max(0, performance.now() - state.tickStartedAt); fraction += Math.min(elapsed / state.playbackMs, 1) / lastIndex; } return Math.max(0, Math.min(fraction, 1)); }
  function updatePlayProgress() { const fraction = replayFraction(); elements.playProgressValue.style.strokeDashoffset = String(100 * (1 - fraction)); const remaining = Math.max(0, Math.round((1 - fraction) * 100)); elements.playButton.title = state.timer !== null ? `Replay in progress — ${remaining}% left` : "Play replay"; }
  function syncPlaybackProgress() { updatePlayProgress(); if (state.timer === null) return; state.raf = window.requestAnimationFrame(syncPlaybackProgress); }
  function setPlaying(playing) { root.dataset.playing = String(playing); elements.playLabel.textContent = playing ? "Pause" : "Play"; elements.playButton.setAttribute("aria-label", playing ? "Pause replay" : "Play replay"); }
  function setControlsDisabled(disabled) { elements.backButton.disabled = disabled || state.index <= 0; elements.nextButton.disabled = disabled || state.index >= state.steps.length - 1; elements.playButton.disabled = disabled || state.steps.length < 2; elements.openDetails.disabled = disabled; elements.copyJson.disabled = disabled; }
  function stop() { if (state.timer !== null) window.clearInterval(state.timer); if (state.raf !== null) window.cancelAnimationFrame(state.raf); state.timer = null; state.raf = null; setPlaying(false); updatePlayProgress(); }

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
</script>
