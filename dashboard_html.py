"""SCADA Cockpit HTML Template for Greenhouse Capsicum Overseer."""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Greenhouse Overseer SCADA Cockpit - Optical Phenotyping & Environmental Telemetry</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg-void: #f1f5f9;
      --bg-panel: #ffffff;
      --bg-surface: #f8fafc;
      --border-subtle: #e2e8f0;
      --border-strong: #cbd5e1;
      --primary: #059669;
      --primary-glow: rgba(5, 150, 105, 0.2);
      --accent-cyan: #0284c7;
      --accent-amber: #d97706;
      --accent-rose: #e11d48;
      --accent-violet: #7c3aed;
      --text-high: #0f172a;
      --text-medium: #475569;
      --text-low: #64748b;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-void);
      background-image: 
        radial-gradient(circle at 12% 10%, rgba(5, 150, 105, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 88% 90%, rgba(2, 132, 199, 0.05) 0%, transparent 40%),
        linear-gradient(rgba(15, 23, 42, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(15, 23, 42, 0.035) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 28px 28px, 28px 28px;
      color: var(--text-high);
      font-family: var(--font-sans);
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      user-select: none;
    }

    /* Enterprise SCADA Header (Light Mode) */
    header {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.5rem 1.4rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
      z-index: 100;
      transition: max-height 0.25s cubic-bezier(0.16, 1, 0.3, 1), 
                  opacity 0.2s ease, 
                  padding 0.25s ease, 
                  transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      max-height: 56px;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    header.header-collapsed {
      max-height: 0;
      opacity: 0;
      padding-top: 0;
      padding-bottom: 0;
      border-bottom: none;
      pointer-events: none;
      transform: translateY(-100%);
    }

    .btn-topbar-toggle {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      background: #f1f5f9;
      border: 1px solid var(--border-subtle);
      color: var(--text-medium);
      padding: 0.3rem 0.65rem;
      border-radius: 4px;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .btn-topbar-toggle:hover {
      background: #e2e8f0;
      color: var(--text-high);
      border-color: var(--border-strong);
    }

    /* Floating Reveal Pill when Header is Hidden */
    .floating-header-btn {
      position: fixed;
      top: 0;
      left: 50%;
      transform: translate(-50%, -100%);
      background: rgba(255, 255, 255, 0.98);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-strong);
      border-top: none;
      border-radius: 0 0 6px 6px;
      color: var(--text-medium);
      padding: 0.25rem 0.95rem;
      font-family: var(--font-mono);
      font-size: 0.65rem;
      font-weight: 600;
      letter-spacing: 0.04em;
      display: flex;
      align-items: center;
      gap: 0.45rem;
      cursor: pointer;
      z-index: 500;
      opacity: 0;
      pointer-events: none;
      transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease, background 0.15s ease, color 0.15s ease;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    .floating-header-btn:hover {
      background: #f8fafc;
      color: var(--primary);
      border-color: var(--primary);
    }
    .floating-header-btn.visible {
      transform: translate(-50%, 0);
      opacity: 0.96;
      pointer-events: auto;
    }

    .brand-cluster {
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }

    .brand-symbol {
      width: 32px;
      height: 32px;
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.12), rgba(5, 150, 105, 0.18));
      border: 1px solid var(--primary);
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--primary);
      box-shadow: 0 0 10px rgba(5, 150, 105, 0.15);
    }

    .brand-meta h1 {
      font-size: 0.95rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: var(--text-high);
    }
    .brand-meta p {
      font-size: 0.68rem;
      color: var(--text-low);
      font-family: var(--font-mono);
      letter-spacing: 0.02em;
    }

    /* Central Cockpit Navigation Tabs (Light Mode) */
    .cockpit-nav-bar {
      display: flex;
      gap: 0.4rem;
      background: #f1f5f9;
      padding: 0.2rem;
      border-radius: 8px;
      border: 1px solid var(--border-subtle);
    }

    .cockpit-tab-btn {
      display: flex;
      align-items: center;
      gap: 0.55rem;
      padding: 0.35rem 0.85rem;
      background: transparent;
      border: 1px solid transparent;
      border-radius: 6px;
      cursor: pointer;
      color: var(--text-medium);
      font-size: 0.76rem;
      font-family: var(--font-sans);
      font-weight: 600;
      letter-spacing: 0.02em;
      transition: all 0.15s ease;
    }
    .cockpit-tab-btn:hover {
      color: var(--text-high);
      background: #e2e8f0;
    }
    .cockpit-tab-btn.active {
      background: #ffffff;
      border-color: #cbd5e1;
      color: var(--primary);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    .tab-index {
      width: 18px;
      height: 18px;
      border-radius: 4px;
      background: #e2e8f0;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #334155;
    }
    .cockpit-tab-btn.active .tab-index {
      background: var(--primary);
      color: #ffffff;
    }

    /* Header Telemetry Badges */
    .telemetry-badges {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .badge-pill {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      background: #f8fafc;
      border: 1px solid var(--border-subtle);
      color: var(--text-medium);
      padding: 0.3rem 0.65rem;
      border-radius: 4px;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 600;
    }
    .badge-pill.status-green {
      border-color: rgba(5, 150, 105, 0.3);
      color: #047857;
      background: rgba(5, 150, 105, 0.08);
    }
    .badge-pill.status-amber {
      border-color: rgba(217, 119, 6, 0.3);
      color: #b45309;
      background: rgba(217, 119, 6, 0.08);
    }
    .badge-pill.status-blue {
      border-color: rgba(2, 132, 199, 0.3);
      color: #0369a1;
      background: rgba(2, 132, 199, 0.08);
    }
    .badge-pill.status-rose {
      border-color: rgba(225, 29, 72, 0.3);
      color: #be123c;
      background: rgba(225, 29, 72, 0.08);
    }
    .indicator-node {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: currentColor;
      box-shadow: 0 0 6px currentColor;
    }

    /* Main Viewport Workspace */
    .cockpit-viewport {
      flex: 1;
      padding: 0.75rem 1.25rem 0.9rem 1.25rem;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    /* ========================================================================
       1080P EXECUTIVE COCKPIT (EXACT 6-BOX SPECIFICATION)
       ======================================================================== */
    #cockpitView1080 {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      height: 100%;
      overflow: hidden;
    }

    /* Top Row: Stream (Left) + Pathology Surveillance Table (Right) */
    .cockpit-upper-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
      flex: 1.45;
      min-height: 0;
    }

    /* Box 1 (Top Left): Live Stream */
    .stream-module {
      background: #020617;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    #canvasPreview, #canvasPreviewV1 {
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }

    #goproImg, #webcamVideo {
      display: none;
    }

    .stream-scada-hud {
      position: absolute;
      inset: 0;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 0.85rem;
    }
    .hud-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    .hud-metric-chip {
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: blur(8px);
      border: 1px solid #cbd5e1;
      color: #0f172a;
      padding: 0.25rem 0.55rem;
      border-radius: 4px;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      display: flex;
      gap: 0.45rem;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }

    .reticle-bracket {
      position: absolute;
      width: 18px;
      height: 18px;
      border-color: var(--primary);
      border-style: solid;
      pointer-events: none;
      opacity: 0.75;
    }
    .reticle-bracket.tl { top: 12px; left: 12px; border-width: 2px 0 0 2px; }
    .reticle-bracket.tr { top: 12px; right: 12px; border-width: 2px 2px 0 0; }
    .reticle-bracket.bl { bottom: 48px; left: 12px; border-width: 0 0 2px 2px; }
    .reticle-bracket.br { bottom: 48px; right: 12px; border-width: 0 2px 2px 0; }

    .stream-control-strip {
      position: absolute;
      bottom: 0.65rem;
      left: 0.65rem;
      right: 0.65rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 0.35rem 0.75rem;
      pointer-events: auto;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .mode-switch-group {
      display: flex;
      gap: 0.35rem;
    }
    .chip-btn {
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      color: #334155;
      padding: 0.28rem 0.6rem;
      border-radius: 4px;
      font-size: 0.7rem;
      font-family: var(--font-mono);
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .chip-btn:hover {
      background: #e2e8f0;
      color: #0f172a;
    }
    .chip-btn.active {
      background: rgba(5, 150, 105, 0.12);
      border-color: var(--primary);
      color: var(--primary);
    }

    .btn-action-primary {
      display: flex;
      align-items: center;
      gap: 0.4rem;
      background: linear-gradient(135deg, #059669, #0284c7);
      color: #ffffff;
      border: none;
      padding: 0.35rem 0.85rem;
      border-radius: 5px;
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-sans);
      letter-spacing: 0.03em;
      cursor: pointer;
      transition: opacity 0.15s ease;
      box-shadow: 0 2px 6px rgba(5, 150, 105, 0.25);
    }
    .btn-action-primary:hover { opacity: 0.92; }

    .shutter-screen {
      position: absolute;
      inset: 0;
      background: #ffffff;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.06s ease-out;
    }
    .shutter-screen.active { opacity: 0.8; }

    /* Box 2 (Top Right): Processed Images Table with Diagnoses & Solutions */
    .diagnoses-module {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .module-toolbar {
      padding: 0.55rem 0.9rem;
      background: #f8fafc;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }
    .module-toolbar h2 {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-high);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .table-container {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      background: #ffffff;
    }

    .scada-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.72rem;
      text-align: left;
    }
    .scada-table th {
      background: #f1f5f9;
      color: #475569;
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 0.65rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 0.45rem 0.75rem;
      position: sticky;
      top: 0;
      z-index: 10;
      border-bottom: 1px solid var(--border-subtle);
    }
    .scada-table td {
      padding: 0.45rem 0.75rem;
      border-bottom: 1px solid #f1f5f9;
      vertical-align: middle;
      color: #1e293b;
    }
    .scada-table tr:hover {
      background: #f8fafc;
    }

    .specimen-thumb {
      width: 44px;
      height: 33px;
      border-radius: 3px;
      object-fit: cover;
      border: 1px solid #cbd5e1;
      cursor: pointer;
      transition: border-color 0.15s ease;
    }
    .specimen-thumb:hover {
      border-color: var(--accent-cyan);
    }

    .tag-status {
      display: inline-block;
      padding: 0.15rem 0.4rem;
      border-radius: 3px;
      font-family: var(--font-mono);
      font-size: 0.62rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .tag-status.diseased {
      background: #ffe4e6;
      color: #be123c;
      border: 1px solid #fecdd3;
    }
    .tag-status.healthy {
      background: #dcfce7;
      color: #15803d;
      border: 1px solid #bbf7d0;
    }
    .tag-status.unrelated {
      background: #f1f5f9;
      color: #475569;
      border: 1px solid #e2e8f0;
    }

    .remediation-directive {
      color: #334155;
      font-size: 0.7rem;
      line-height: 1.35;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    /* Bottom Row: 4 Detailed SCADA Charts */
    .cockpit-lower-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.75rem;
      flex: 1.05;
      min-height: 0;
    }

    .telemetry-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .card-top-stat {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 0.25rem;
      flex-shrink: 0;
    }
    .channel-title {
      font-size: 0.68rem;
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--text-low);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .channel-kpi {
      font-family: var(--font-mono);
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text-high);
      display: flex;
      align-items: baseline;
      gap: 0.25rem;
    }
    .channel-kpi .unit {
      font-size: 0.72rem;
      color: var(--text-medium);
      font-weight: 500;
    }

    .channel-meta-sub {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.64rem;
      font-family: var(--font-mono);
      color: var(--text-low);
      padding-bottom: 0.25rem;
      border-bottom: 1px solid #f1f5f9;
      margin-bottom: 0.35rem;
      flex-shrink: 0;
    }
    .channel-meta-sub span b {
      color: #1e293b;
    }

    .chart-viewport-box {
      flex: 1;
      width: 100%;
      min-height: 0;
      position: relative;
    }

    /* ========================================================================
       OPTICAL CALIBRATION SUITE (VIEW 1)
       ======================================================================== */
    #cockpitViewLab {
      display: none;
      grid-template-columns: 1fr 380px;
      gap: 1rem;
      height: 100%;
      overflow: hidden;
    }

    .lab-stage {
      display: flex;
      flex-direction: column;
      height: 100%;
    }
    .lab-controls-panel {
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      height: 100%;
    }

    .control-block {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.85rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .block-header {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 0.65rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--text-high);
    }

    .slider-row {
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
      margin-bottom: 0.55rem;
    }
    .slider-text {
      display: flex;
      justify-content: space-between;
      font-size: 0.7rem;
      color: var(--text-medium);
      font-family: var(--font-mono);
    }
    .slider-text .val {
      color: var(--text-high);
      font-weight: 600;
    }
    input[type=range] {
      -webkit-appearance: none;
      width: 100%;
      height: 4px;
      background: #cbd5e1;
      border-radius: 2px;
      outline: none;
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 12px;
      height: 12px;
      background: var(--primary);
      border-radius: 50%;
      cursor: pointer;
    }

    .hue-spectrum-rail {
      position: relative;
      height: 10px;
      border-radius: 4px;
      background: linear-gradient(90deg, #ff0000 0%, #ffff00 16.6%, #00ff00 33.3%, #00ffff 50%, #0000ff 66.6%, #ff00ff 83.3%, #ff0000 100%);
      margin: 0.25rem 0 0.55rem 0;
      overflow: hidden;
    }
    .hue-active-gate {
      position: absolute;
      top: 0; bottom: 0;
      border: 1.5px solid #0f172a;
      box-shadow: 0 0 6px rgba(15, 23, 42, 0.4);
      border-radius: 3px;
      pointer-events: none;
    }

    /* Modal Inspection Frame */
    #specimenModal {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(12px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    #specimenModal.active { display: flex; }
    .modal-frame {
      background: #ffffff;
      border: 1px solid var(--border-strong);
      border-radius: 8px;
      max-width: 860px;
      width: 100%;
      display: grid;
      grid-template-columns: 1fr 1fr;
      overflow: hidden;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.25);
    }
    .modal-symptoms-box {
      background: #f8fafc;
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 0.85rem;
      margin-bottom: 1rem;
    }
    .modal-remediation-box {
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: 6px;
      padding: 0.85rem;
    }
    .modal-close-btn {
      margin-top: 1.5rem;
      padding: 0.6rem;
      background: #f1f5f9;
      border: 1px solid var(--border-strong);
      color: var(--text-high);
      border-radius: 4px;
      cursor: pointer;
      font-family: var(--font-sans);
      font-size: 0.76rem;
      font-weight: 600;
      transition: all 0.15s ease;
    }
    .modal-close-btn:hover {
      background: #e2e8f0;
    }

    /* Toast */
    #toastLog {
      position: fixed;
      bottom: 1.25rem;
      right: 1.25rem;
      background: #0f172a;
      border: 1px solid var(--primary);
      color: #ffffff;
      padding: 0.65rem 1.15rem;
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 0.76rem;
      transform: translateY(80px);
      opacity: 0;
      transition: all 0.2s ease;
      z-index: 2000;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    }
    #toastLog.active {
      transform: translateY(0);
      opacity: 1;
    }
  </style>
</head>
<body>

  <!-- Enterprise SCADA Header -->
  <header>
    <div class="brand-cluster">
      <div class="brand-symbol">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
        </svg>
      </div>
      <div class="brand-meta">
        <h1>Greenhouse Overseer SCADA</h1>
        <p>Optical Phenotyping & Microclimate Telemetry Architecture</p>
      </div>
    </div>

    <!-- Mode Selector Tabs -->
    <div class="cockpit-nav-bar">
      <button id="tabNav1" class="cockpit-tab-btn" onclick="setCockpitView(1)" title="Optical Calibration & Threshold Sliders (Key: 1)">
        <span class="tab-index">1</span>
        <span>Optical Calibration Lab</span>
      </button>

      <button id="tabNav2" class="cockpit-tab-btn active" onclick="setCockpitView(2)" title="1080p SCADA Supervisory Cockpit (Key: 2)">
        <span class="tab-index">2</span>
        <span>1080p Operations Cockpit</span>
      </button>
    </div>

    <div class="telemetry-badges">
      <div class="badge-pill status-blue" id="pillBattery">
        <span class="indicator-node"></span>
        <span id="txtBattery">BATTERY: --%</span>
      </div>

      <div class="badge-pill status-amber" id="pillGateway">
        <span class="indicator-node"></span>
        <span id="txtGateway">ESP32: COM7</span>
      </div>

      <div class="badge-pill status-green">
        <span class="indicator-node"></span>
        <span id="txtStreamFps">STREAM 30.0 FPS</span>
      </div>

      <!-- Live AI API Availability Badge -->
      <div class="badge-pill status-green" id="pillAiApi" title="Gemini AI Diagnostic Engine & Key Rotation Status">
        <span class="indicator-node" id="nodeAiApi"></span>
        <span id="txtAiApi">AI API: ONLINE</span>
      </div>

      <!-- Specimen Pipeline Queue Badge -->
      <div class="badge-pill" id="pillQueue" title="Asynchronous Specimen Ingestion & Diagnostic Pipeline Queue">
        <span class="indicator-node" style="background: #0284c7;"></span>
        <span id="txtQueue">QUEUE: 0 PENDING</span>
      </div>

      <!-- Real 4 Snaps / Hour Schedule Countdown -->
      <div class="badge-pill status-blue" id="pillNextSnap" title="Automated Real Specimen Acquisition Schedule (4 Snaps / Hour = 15m Cadence)">
        <span class="indicator-node" style="background: #d97706;"></span>
        <span id="txtNextSnap">NEXT SNAP: 15m 00s (4/HR)</span>
      </div>

      <button id="btnHideTopBar" class="btn-topbar-toggle" onclick="toggleTopBar()" title="Hide Top Navigation Bar (Shortcut: H)">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="18 15 12 9 6 15"></polyline>
        </svg>
        <span>HIDE BAR [H]</span>
      </button>
    </div>
  </header>

  <!-- Floating Reveal Button when Header is Hidden -->
  <button id="floatingShowHeaderBtn" class="floating-header-btn" onclick="toggleTopBar()" title="Reveal Top Navigation Bar (Shortcut: H)">
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="6 9 12 15 18 9"></polyline>
    </svg>
    <span>SHOW HEADER [H]</span>
  </button>

  <!-- Main Viewport Workspace -->
  <div class="cockpit-viewport">

    <!-- ========================================================================
         VIEW 2: 1080P OPERATIONS COCKPIT (THE EXACT 6-BOX SPECIFICATION)
         ======================================================================== -->
    <div id="cockpitView1080">
      
      <!-- Upper Grid: Live Stream (Left) + Pathology Table (Right) -->
      <div class="cockpit-upper-grid">
        
        <!-- Box 1 (Top Left): Live Stream -->
        <div class="stream-module">
          <img id="goproImg" crossOrigin="anonymous" src="/video_feed" alt="Video Stream">
          <video id="webcamVideo" autoplay playsinline muted></video>

          <canvas id="canvasPreview"></canvas>
          <div class="shutter-screen" id="shutterFx"></div>

          <!-- Technical Corner Brackets -->
          <div class="reticle-bracket tl"></div>
          <div class="reticle-bracket tr"></div>
          <div class="reticle-bracket bl"></div>
          <div class="reticle-bracket br"></div>

          <!-- SCADA HUD Overlay -->
          <div class="stream-scada-hud">
            <div class="hud-header">
              <div class="hud-metric-chip">
                <span style="color: var(--text-low);">FEED:</span>
                <span id="lblActiveShader" style="color: var(--primary);">EXG SPECTRAL HIGHLIGHT</span>
              </div>
              <div class="hud-metric-chip">
                <span style="color: var(--text-low);">CADENCE:</span>
                <span style="color: var(--accent-amber); font-weight: 700;" id="lblHudCadence">4 SNAPS/HR [AUTO]</span>
              </div>
              <div class="hud-metric-chip">
                <span style="color: var(--text-low);">CANOPY:</span>
                <span id="lblCanopyCoverage" style="color: var(--accent-cyan);">0.0%</span>
              </div>
              <div class="hud-metric-chip">
                <span style="color: var(--text-low);">STREAM:</span>
                <span id="lblFps" style="color: var(--primary);">30.0 FPS</span>
              </div>
            </div>
          </div>

          <!-- Bottom Control Bar -->
          <div class="stream-control-strip">
            <div class="mode-switch-group">
              <button class="chip-btn active" onclick="setFilterMode('highlight')">HIGHLIGHT</button>
              <button class="chip-btn" onclick="setFilterMode('isolate')">ISOLATION</button>
              <button class="chip-btn" onclick="setFilterMode('contour')">CONTOUR</button>
              <button class="chip-btn" onclick="setFilterMode('raw')">RAW SENSOR</button>
            </div>
            <button class="btn-action-primary" onclick="triggerSnapshot()">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
              <span>CAPTURE SPECIMEN</span>
            </button>
          </div>
        </div>

        <!-- Box 2 (Top Right): Processed Images Table with Diagnoses & Solutions -->
        <div class="diagnoses-module">
          <div class="module-toolbar">
            <h2>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
              <span>Pathology Surveillance & AI Diagnostic Intake</span>
            </h2>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
              <span id="lblDiagTotal" style="font-family: var(--font-mono); font-size: 0.68rem; color: var(--accent-cyan); font-weight: 700;">14 SPECIMENS LOGGED</span>
              <button onclick="fetchDiagnoses()" style="background: #ffffff; border: 1px solid var(--border-strong); color: var(--text-high); font-size: 0.65rem; font-family: var(--font-mono); font-weight: 600; padding: 0.2rem 0.55rem; border-radius: 4px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">REFRESH</button>
            </div>
          </div>

          <div class="table-container">
            <table class="scada-table">
              <thead>
                <tr>
                  <th style="width: 55px;">Specimen</th>
                  <th style="width: 85px;">Timestamp</th>
                  <th style="width: 130px;">Pathology Classification</th>
                  <th style="width: 80px;">Status</th>
                  <th>Remediation Protocol</th>
                </tr>
              </thead>
              <tbody id="tbodyDiagnoses">
                <tr>
                  <td colspan="5" style="text-align: center; color: var(--text-low); padding: 2.5rem; font-family: var(--font-mono);">
                    INITIALIZING SURVEILLANCE DATABASE INTAKE...
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- Lower Grid: 4 Dedicated Detailed Telemetry Charts -->
      <div class="cockpit-lower-grid">

        <!-- Box 1 (Bottom Left): Relative Humidity -->
        <div class="telemetry-card">
          <div class="card-top-stat">
            <span class="channel-title">Relative Humidity</span>
            <div class="channel-kpi">
              <span id="txtValHumidity">60.2</span>
              <span class="unit">% RH</span>
            </div>
          </div>
          <div class="channel-meta-sub">
            <span>TARGET: <b>55.0% - 75.0%</b></span>
            <span>VPD: <b id="txtVpd">1.05 kPa</b></span>
          </div>
          <div class="chart-viewport-box">
            <canvas id="canvasHumidityChart"></canvas>
          </div>
        </div>

        <!-- Box 2 (Bottom Mid-Left): Temperature -->
        <div class="telemetry-card">
          <div class="card-top-stat">
            <span class="channel-title">Ambient Dry Bulb</span>
            <div class="channel-kpi">
              <span id="txtValTemperature">24.5</span>
              <span class="unit">°C</span>
            </div>
          </div>
          <div class="channel-meta-sub">
            <span>TARGET: <b>21.0°C - 28.0°C</b></span>
            <span>GRADIENT: <b id="txtTempTrend">+0.2°C/hr</b></span>
          </div>
          <div class="chart-viewport-box">
            <canvas id="canvasTemperatureChart"></canvas>
          </div>
        </div>

        <!-- Box 3 (Bottom Mid-Right): Soil Moisture -->
        <div class="telemetry-card">
          <div class="card-top-stat">
            <span class="channel-title">Substrate Volumetric</span>
            <div class="channel-kpi">
              <span id="txtValSoil">2191</span>
              <span class="unit">ADC</span>
            </div>
          </div>
          <div class="channel-meta-sub">
            <span>MOISTURE INDEX: <b id="txtSoilPct">76.2%</b></span>
            <span>CAPACITY: <b>OPTIMAL</b></span>
          </div>
          <div class="chart-viewport-box">
            <canvas id="canvasSoilChart"></canvas>
          </div>
        </div>

        <!-- Box 4 (Bottom Right): Light Intensity -->
        <div class="telemetry-card">
          <div class="card-top-stat">
            <span class="channel-title">Solar Radiance / PAR</span>
            <div class="channel-kpi">
              <span id="txtValLight">1120</span>
              <span class="unit">Lux</span>
            </div>
          </div>
          <div class="channel-meta-sub">
            <span>EST. PPFD: <b id="txtPpfd">~22.4 µmol</b></span>
            <span>PHOTOPERIOD: <b>ACTIVE</b></span>
          </div>
          <div class="chart-viewport-box">
            <canvas id="canvasLightChart"></canvas>
          </div>
        </div>

      </div>

    </div>

    <!-- ========================================================================
         VIEW 1: OPTICAL CALIBRATION LAB (TOGGLEABLE)
         ======================================================================== -->
    <div id="cockpitViewLab">
      <div class="lab-stage">
        <div class="stream-module" style="height: 100%;">
          <canvas id="canvasPreviewV1"></canvas>
        </div>
      </div>

      <div class="lab-controls-panel">
        <div class="control-block">
          <div class="block-header">
            <span>HSV Spectral Wavelength Window</span>
            <span style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--primary);" id="lblHueRange">52° - 168°</span>
          </div>

          <div class="hue-spectrum-rail">
            <div id="boxHueGate" class="hue-active-gate" style="left: 14.4%; width: 32.2%;"></div>
          </div>

          <div class="slider-row">
            <div class="slider-text"><span>HUE LOWER BOUND (YELLOW-GREEN)</span><span class="val" id="valHMin">52°</span></div>
            <input type="range" id="sliderHMin" min="30" max="110" value="52">
          </div>
          <div class="slider-row">
            <div class="slider-text"><span>HUE UPPER BOUND (DEEP GREEN)</span><span class="val" id="valHMax">168°</span></div>
            <input type="range" id="sliderHMax" min="110" max="210" value="168">
          </div>
          <div class="slider-row">
            <div class="slider-text"><span>SATURATION LOWER CUTOFF</span><span class="val" id="valSMin">14%</span></div>
            <input type="range" id="sliderSMin" min="2" max="60" value="14">
          </div>
          <div class="slider-row">
            <div class="slider-text"><span>LUMINANCE / VALUE FLOOR</span><span class="val" id="valVMin">10%</span></div>
            <input type="range" id="sliderVMin" min="2" max="50" value="10">
          </div>
          <div class="slider-row">
            <div class="slider-text"><span>EXG DIFFERENTIAL WEIGHT</span><span class="val" id="valExgW">20%</span></div>
            <input type="range" id="sliderExgW" min="0" max="100" value="20" title="0% = Pure HSV Spectral Isolation">
          </div>
          <div class="slider-row">
            <div class="slider-text"><span>OVERLAY OPACITY</span><span class="val" id="valOp">55%</span></div>
            <input type="range" id="sliderOp" min="10" max="100" value="55">
          </div>
        </div>

        <div class="control-block">
          <div class="block-header"><span>Calibration Presets</span></div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem;">
            <button class="chip-btn active" onclick="applyPreset('standard')">STANDARD CANOPY</button>
            <button class="chip-btn" onclick="applyPreset('shoots')">JUVENILE / LIME</button>
            <button class="chip-btn" onclick="applyPreset('shade')">CANOPY SHADE</button>
            <button class="chip-btn" onclick="applyPreset('wide')">WIDE ADAPTIVE</button>
          </div>
        </div>

        <div class="control-block">
          <div class="block-header"><span>Isolation Matrix Background</span></div>
          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.4rem;">
            <button class="chip-btn active" onclick="setIsolateBg('black')">ZERO BLACK</button>
            <button class="chip-btn" onclick="setIsolateBg('gray')">MONOCHROME</button>
            <button class="chip-btn" onclick="setIsolateBg('white')">HIGH-KEY</button>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Detailed Specimen Modal -->
  <div id="specimenModal" onclick="closeSpecimenModal(event)">
    <div class="modal-frame" onclick="event.stopPropagation()">
      <div style="background: #000; display: flex; align-items: center; justify-content: center; padding: 1.25rem; border-right: 1px solid var(--border-subtle);">
        <img id="modalSpecimenImg" src="" alt="Specimen Inspection" style="max-width: 100%; max-height: 440px; border-radius: 4px;">
      </div>
      <div style="padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
            <span id="modalSpecimenStatus" class="tag-status diseased">DISEASED</span>
            <span id="modalSpecimenTime" style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-low);">2026-10-20 18:19:25</span>
          </div>
          <h3 id="modalSpecimenCondition" style="font-size: 1.25rem; font-weight: 700; color: var(--text-high); margin-bottom: 0.35rem;">Powdery Mildew</h3>
          <p id="modalSpecimenConf" style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--accent-cyan); margin-bottom: 1.25rem;">CONFIDENCE: 94.0%</p>

          <div class="modal-symptoms-box">
            <div style="font-size: 0.68rem; font-family: var(--font-mono); color: var(--text-low); text-transform: uppercase; font-weight: 700; margin-bottom: 0.3rem;">Symptomology Profile:</div>
            <div id="modalSpecimenSymptoms" style="font-size: 0.78rem; line-height: 1.45; color: var(--text-medium);">Localized mycelial superficial colonies and chlorosis.</div>
          </div>

          <div class="modal-remediation-box">
            <div style="font-size: 0.68rem; font-family: var(--font-mono); color: #047857; text-transform: uppercase; font-weight: 700; margin-bottom: 0.3rem;">Agronomic Remediation Protocol:</div>
            <div id="modalSpecimenAction" style="font-size: 0.78rem; line-height: 1.45; color: #065f46; font-weight: 500;">Apply systemic triazole or sulfur foliar treatment. Modulate air ventilation.</div>
          </div>
        </div>

        <button class="modal-close-btn" onclick="document.getElementById('specimenModal').classList.remove('active')">CLOSE SPECIMEN DOSSIER</button>
      </div>
    </div>
  </div>

  <div id="toastLog">Notification Log</div>

  <script>
    // --- SCADA View Controller ---
    let currentViewMode = 2; // Default: 1080p SCADA Operations Cockpit

    function setCockpitView(mode) {
      currentViewMode = mode;
      const v1 = document.getElementById('cockpitViewLab');
      const v2 = document.getElementById('cockpitView1080');
      const t1 = document.getElementById('tabNav1');
      const t2 = document.getElementById('tabNav2');

      if (mode === 1) {
        v1.style.display = 'grid';
        v2.style.display = 'none';
        t1.classList.add('active');
        t2.classList.remove('active');
      } else {
        v1.style.display = 'none';
        v2.style.display = 'flex';
        t1.classList.remove('active');
        t2.classList.add('active');
        fetchDiagnoses();
      }
    }

    // --- Top Navigation Bar Visibility Toggle ---
    let isHeaderHidden = false;

    function toggleTopBar(forceState) {
      const header = document.querySelector('header');
      const floatBtn = document.getElementById('floatingShowHeaderBtn');
      
      if (typeof forceState === 'boolean') {
        isHeaderHidden = forceState;
      } else {
        isHeaderHidden = !isHeaderHidden;
      }

      if (isHeaderHidden) {
        header.classList.add('header-collapsed');
        floatBtn.classList.add('visible');
        showToast('Top Navigation Bar Hidden [Press H to restore]');
      } else {
        header.classList.remove('header-collapsed');
        floatBtn.classList.remove('visible');
        showToast('Top Navigation Bar Restored');
      }

      try {
        localStorage.setItem('scada_header_hidden', isHeaderHidden ? 'true' : 'false');
      } catch (e) {}

      // Trigger resize for Chart.js and video canvas to re-fit expanded 1080p area
      setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
      }, 260);
    }

    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT') return;
      if (e.key === '1') setCockpitView(1);
      if (e.key === '2') setCockpitView(2);
      if (e.key === 'h' || e.key === 'H') toggleTopBar();
      if (e.key === 'Escape' && isHeaderHidden) toggleTopBar(false);
    });

    // --- Stream & Processing Pipeline ---
    const goproImg = document.getElementById('goproImg');
    const canvas = document.getElementById('canvasPreview');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    const canvasV1 = document.getElementById('canvasPreviewV1');
    const ctxV1 = canvasV1 ? canvasV1.getContext('2d') : null;

    const lblFps = document.getElementById('lblFps');
    const txtStreamFps = document.getElementById('txtStreamFps');
    const lblCanopyCoverage = document.getElementById('lblCanopyCoverage');
    const lblActiveShader = document.getElementById('lblActiveShader');
    const shutterFx = document.getElementById('shutterFx');
    const toastLog = document.getElementById('toastLog');

    // Optical Threshold Sliders
    const sliderHMin = document.getElementById('sliderHMin');
    const sliderHMax = document.getElementById('sliderHMax');
    const valHMin = document.getElementById('valHMin');
    const valHMax = document.getElementById('valHMax');
    const lblHueRange = document.getElementById('lblHueRange');
    const boxHueGate = document.getElementById('boxHueGate');

    const sliderSMin = document.getElementById('sliderSMin');
    const valSMin = document.getElementById('valSMin');
    const sliderVMin = document.getElementById('sliderVMin');
    const valVMin = document.getElementById('valVMin');
    const sliderExgW = document.getElementById('sliderExgW');
    const valExgW = document.getElementById('valExgW');
    const sliderOp = document.getElementById('sliderOp');
    const valOp = document.getElementById('valOp');

    let currentFilterMode = 'highlight'; // 'highlight', 'isolate', 'contour', 'raw'
    let currentIsolateBg = 'black';
    let lastFrameTime = performance.now();
    let frameCount = 0;
    let fps = 0;
    let animationId = null;

    function setFilterMode(mode) {
      currentFilterMode = mode;
      lblActiveShader.innerText = mode === 'highlight' ? 'EXG SPECTRAL HIGHLIGHT' :
                                 mode === 'isolate' ? 'FOLIAGE ISOLATION MATRIX' :
                                 mode === 'contour' ? 'CANOPY CONTOUR ISOLINES' : 'UNPROCESSED SENSOR';
      document.querySelectorAll('.stream-control-strip .chip-btn').forEach(b => {
        b.classList.toggle('active', b.innerText.toLowerCase().includes(mode));
      });
    }

    function setIsolateBg(bg) {
      currentIsolateBg = bg;
    }

    function applyPreset(preset) {
      if (preset === 'standard') {
        sliderHMin.value = 52; sliderHMax.value = 168; sliderSMin.value = 14; sliderVMin.value = 10; sliderExgW.value = 20;
      } else if (preset === 'shoots') {
        sliderHMin.value = 42; sliderHMax.value = 145; sliderSMin.value = 10; sliderVMin.value = 14; sliderExgW.value = 10;
      } else if (preset === 'shade') {
        sliderHMin.value = 58; sliderHMax.value = 180; sliderSMin.value = 12; sliderVMin.value = 6; sliderExgW.value = 15;
      } else if (preset === 'wide') {
        sliderHMin.value = 36; sliderHMax.value = 195; sliderSMin.value = 6; sliderVMin.value = 5; sliderExgW.value = 0;
      }
      updateSpectrumGate();
    }

    function initStream() {
      goproImg.src = '/video_feed?' + Date.now();
      goproImg.onload = () => {
        txtStreamFps.innerText = 'GOPRO 11 USB: 30.0 FPS';
        if (!animationId) animationId = requestAnimationFrame(processVideoFrame);
      };
      goproImg.onerror = () => {
        txtStreamFps.innerText = 'RECONNECTING STREAM...';
      };
    }

    function processVideoFrame(now) {
      let sourceElem = goproImg;
      let sWidth = goproImg.naturalWidth || 1280;
      let sHeight = goproImg.naturalHeight || 960;

      if (sourceElem && sWidth > 0 && sHeight > 0) {
        if (canvas.width !== sWidth || canvas.height !== sHeight) {
          canvas.width = sWidth;
          canvas.height = sHeight;
        }

        ctx.drawImage(sourceElem, 0, 0, canvas.width, canvas.height);

        if (currentFilterMode !== 'raw') {
          const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
          const data = imgData.data;
          const totalPixels = canvas.width * canvas.height;

          const uHMin = parseFloat(sliderHMin.value);
          const uHMax = parseFloat(sliderHMax.value);
          const uSMin = parseFloat(sliderSMin.value) / 100.0;
          const uVMin = parseFloat(sliderVMin.value) / 100.0;
          const uExgW = parseFloat(sliderExgW.value) / 100.0;
          const opacity = parseFloat(sliderOp.value) / 100.0;

          let leafCount = 0;

          for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];

            const maxC = Math.max(r, g, b);
            const minC = Math.min(r, g, b);
            const delta = maxC - minC;

            // Value / Luminance Gate
            const val = maxC / 255.0;
            if (val < uVMin) {
              applyBackgroundPixel(data, i, currentFilterMode, currentIsolateBg);
              continue;
            }

            // Saturation Gate
            const sat = maxC === 0 ? 0 : delta / maxC;
            if (sat < uSMin) {
              applyBackgroundPixel(data, i, currentFilterMode, currentIsolateBg);
              continue;
            }

            // Hue Gate
            let hue = 0;
            if (delta > 0) {
              if (maxC === g) hue = 60 * (((b - r) / delta) + 2);
              else if (maxC === r) hue = 60 * (((g - b) / delta) + (g < b ? 6 : 0));
              else hue = 60 * (((r - g) / delta) + 4);
            }

            if (hue < uHMin || hue > uHMax) {
              applyBackgroundPixel(data, i, currentFilterMode, currentIsolateBg);
              continue;
            }

            // ExG Weight
            if (uExgW > 0.05) {
              const exg = 2.0 * g - r - b;
              if (exg < (-25.0 * (1.0 - uExgW))) {
                applyBackgroundPixel(data, i, currentFilterMode, currentIsolateBg);
                continue;
              }
            }

            leafCount++;
            if (currentFilterMode === 'highlight') {
              data[i] = Math.min(255, r * (1 - opacity) + 16 * opacity);
              data[i + 1] = Math.min(255, g * (1 - opacity) + 185 * opacity);
              data[i + 2] = Math.min(255, b * (1 - opacity) + 129 * opacity);
            }
          }

          ctx.putImageData(imgData, 0, 0);
          const cov = ((leafCount / totalPixels) * 100).toFixed(1);
          lblCanopyCoverage.innerText = `${cov}%`;
        } else {
          lblCanopyCoverage.innerText = 'RAW SENSOR';
        }

        if (currentViewMode === 1 && canvasV1) {
          if (canvasV1.width !== canvas.width || canvasV1.height !== canvas.height) {
            canvasV1.width = canvas.width;
            canvasV1.height = canvas.height;
          }
          ctxV1.drawImage(canvas, 0, 0);
        }
      }

      frameCount++;
      if (now - lastFrameTime >= 1000) {
        fps = frameCount;
        frameCount = 0;
        lastFrameTime = now;
        lblFps.innerText = `${fps}.0 FPS`;
      }
      animationId = requestAnimationFrame(processVideoFrame);
    }

    function applyBackgroundPixel(data, i, mode, style) {
      if (mode === 'isolate') {
        if (style === 'black') {
          data[i] = 0; data[i + 1] = 0; data[i + 2] = 0;
        } else if (style === 'white') {
          data[i] = 255; data[i + 1] = 255; data[i + 2] = 255;
        } else {
          const gray = (data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114) * 0.25;
          data[i] = gray; data[i + 1] = gray; data[i + 2] = gray;
        }
      }
    }

    function updateSpectrumGate() {
      const hMin = parseFloat(sliderHMin.value);
      const hMax = parseFloat(sliderHMax.value);
      valHMin.innerText = `${hMin}°`;
      valHMax.innerText = `${hMax}°`;
      lblHueRange.innerText = `${hMin}° - ${hMax}°`;
      valSMin.innerText = `${sliderSMin.value}%`;
      valVMin.innerText = `${sliderVMin.value}%`;
      valExgW.innerText = `${sliderExgW.value}%`;
      valOp.innerText = `${sliderOp.value}%`;

      const leftPct = (hMin / 360.0) * 100.0;
      const widthPct = ((hMax - hMin) / 360.0) * 100.0;
      boxHueGate.style.left = `${leftPct.toFixed(1)}%`;
      boxHueGate.style.width = `${Math.max(2, widthPct).toFixed(1)}%`;
    }
    sliderHMin.addEventListener('input', updateSpectrumGate);
    sliderHMax.addEventListener('input', updateSpectrumGate);
    sliderSMin.addEventListener('input', updateSpectrumGate);
    sliderVMin.addEventListener('input', updateSpectrumGate);
    sliderExgW.addEventListener('input', updateSpectrumGate);
    sliderOp.addEventListener('input', updateSpectrumGate);

    // Snapshot
    function showToast(msg) {
      toastLog.innerText = msg;
      toastLog.classList.add('active');
      setTimeout(() => toastLog.classList.remove('active'), 3200);
    }

    async function triggerSnapshot() {
      shutterFx.classList.add('active');
      setTimeout(() => shutterFx.classList.remove('active'), 80);

      const imageData = canvas.toDataURL('image/jpeg', 0.95);
      const now = new Date();
      const ts = now.toISOString().replace(/[-:T]/g, '').slice(0, 15);
      const filename = `specimen_${ts}.jpg`;

      try {
        const resp = await fetch('/api/capture', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filename, use_native_raw: true, image_data: imageData })
        });
        const res = await resp.json();
        if (res.success) {
          showToast(`Specimen enqueued for AI analysis: ${filename}`);
          setTimeout(fetchDiagnoses, 2500);
        }
      } catch (err) {
        showToast('Capture dispatch fault');
      }
    }

    // --- Processed Images Table with Diagnoses & Solutions ---
    let specimenRecordCache = [];

    async function fetchDiagnoses() {
      try {
        const resp = await fetch('/api/diagnoses');
        const data = await resp.json();
        specimenRecordCache = data;

        document.getElementById('lblDiagTotal').innerText = `${data.length} SPECIMENS LOGGED`;
        const tbody = document.getElementById('tbodyDiagnoses');

        if (!data || data.length === 0) {
          tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:#64748b; padding:2rem; font-family:var(--font-mono);">ZERO SURVEILLANCE SPECIMENS RECORDED</td></tr>';
          return;
        }

        tbody.innerHTML = data.map((item, idx) => {
          const statusCls = item.health_status === 'diseased' ? 'diseased' :
                            item.health_status === 'healthy' ? 'healthy' : 'unrelated';
          const timeFormatted = item.timestamp || '--:--:--';
          const confPercent = Math.round((item.confidence_score || 0) * 100);

          return `
            <tr>
              <td>
                <img class="specimen-thumb" src="${item.image_url}" alt="Specimen" onclick="openSpecimenModal(${idx})" onerror="this.src='/video_feed'">
              </td>
              <td style="font-family: var(--font-mono); color: var(--text-medium); font-size: 0.68rem;">
                ${timeFormatted}
              </td>
              <td>
                <div style="font-weight: 700; color: var(--text-high); font-size: 0.74rem;">${item.primary_condition || 'Undetermined'}</div>
                <div style="font-family: var(--font-mono); font-size: 0.62rem; color: var(--text-low);">Confidence: ${confPercent}% | ${item.severity_level || 'Standard'}</div>
              </td>
              <td>
                <span class="tag-status ${statusCls}">${item.health_status}</span>
              </td>
              <td>
                <div class="remediation-directive" title="${item.recommended_action}">
                  ${item.recommended_action || 'Continuous sensory monitoring active.'}
                </div>
              </td>
            </tr>
          `;
        }).join('');

      } catch (err) {
        console.warn('Diagnoses fetch fault:', err);
      }
    }

    function openSpecimenModal(idx) {
      const item = specimenRecordCache[idx];
      if (!item) return;

      document.getElementById('modalSpecimenImg').src = item.image_url;
      document.getElementById('modalSpecimenCondition').innerText = item.primary_condition || 'Undetermined';
      document.getElementById('modalSpecimenTime').innerText = `TIMESTAMP: ${item.timestamp || ''}`;
      document.getElementById('modalSpecimenConf').innerText = `CONFIDENCE SCORE: ${Math.round(item.confidence_score * 100)}% | SEVERITY: ${(item.severity_level || 'NOMINAL').toUpperCase()}`;
      document.getElementById('modalSpecimenSymptoms').innerText = item.visual_symptoms || 'No anomalous visual lesions noted.';
      document.getElementById('modalSpecimenAction').innerText = item.recommended_action || 'Routine baseline observation protocol.';

      const st = document.getElementById('modalSpecimenStatus');
      st.className = `tag-status ${item.health_status}`;
      st.innerText = item.health_status.toUpperCase();

      document.getElementById('specimenModal').classList.add('active');
    }

    function closeSpecimenModal(e) {
      document.getElementById('specimenModal').classList.remove('active');
    }

    // --- Detailed SCADA Charts (4 Channels) ---
    let chartHumidity = null;
    let chartTemperature = null;
    let chartSoil = null;
    let chartLight = null;

    function initTechnicalCharts() {
      const gridConfig = { color: 'rgba(0, 0, 0, 0.05)', drawBorder: false };
      const tickConfig = { color: '#64748b', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 5 };
      const tooltipConfig = (channelLabel, unitStr) => ({
        backgroundColor: 'rgba(15, 23, 42, 0.94)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        titleFont: { family: 'JetBrains Mono' },
        bodyFont: { family: 'JetBrains Mono' },
        padding: 8,
        cornerRadius: 4,
        callbacks: { label: ctx => `${channelLabel}: ${ctx.parsed.y} ${unitStr}` }
      });

      // 1. Humidity (Cyan Axis)
      const ctxH = document.getElementById('canvasHumidityChart').getContext('2d');
      chartHumidity = new Chart(ctxH, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            data: [],
            borderColor: '#0284c7',
            backgroundColor: 'rgba(2, 132, 199, 0.12)',
            borderWidth: 2.2,
            pointRadius: 2,
            pointHoverRadius: 5,
            fill: true,
            tension: 0.35
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 400, easing: 'easeOutQuad' },
          plugins: {
            legend: { display: false },
            tooltip: tooltipConfig('Relative Humidity', '%')
          },
          scales: {
            x: { grid: gridConfig, ticks: tickConfig },
            y: { grid: gridConfig, ticks: { ...tickConfig, callback: v => v + '%' }, suggestedMin: 50, suggestedMax: 75 }
          }
        }
      });

      // 2. Temperature (Emerald Axis)
      const ctxT = document.getElementById('canvasTemperatureChart').getContext('2d');
      chartTemperature = new Chart(ctxT, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            data: [],
            borderColor: '#059669',
            backgroundColor: 'rgba(5, 150, 105, 0.12)',
            borderWidth: 2.2,
            pointRadius: 2,
            pointHoverRadius: 5,
            fill: true,
            tension: 0.35
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 400, easing: 'easeOutQuad' },
          plugins: {
            legend: { display: false },
            tooltip: tooltipConfig('Dry Bulb Temperature', '°C')
          },
          scales: {
            x: { grid: gridConfig, ticks: tickConfig },
            y: { grid: gridConfig, ticks: { ...tickConfig, callback: v => v + '°C' }, suggestedMin: 20, suggestedMax: 30 }
          }
        }
      });

      // 3. Soil Moisture (Forest Green)
      const ctxS = document.getElementById('canvasSoilChart').getContext('2d');
      chartSoil = new Chart(ctxS, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            data: [],
            borderColor: '#16a34a',
            backgroundColor: 'rgba(22, 163, 74, 0.12)',
            borderWidth: 2.2,
            pointRadius: 2,
            pointHoverRadius: 5,
            fill: true,
            tension: 0.35
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 400, easing: 'easeOutQuad' },
          plugins: {
            legend: { display: false },
            tooltip: tooltipConfig('Substrate Raw ADC', 'counts')
          },
          scales: {
            x: { grid: gridConfig, ticks: tickConfig },
            y: { grid: gridConfig, ticks: { ...tickConfig, callback: v => v + ' ADC' }, suggestedMin: 1800, suggestedMax: 2600 }
          }
        }
      });

      // 4. Light Radiance (Solar Amber)
      const ctxL = document.getElementById('canvasLightChart').getContext('2d');
      chartLight = new Chart(ctxL, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            data: [],
            borderColor: '#d97706',
            backgroundColor: 'rgba(217, 119, 6, 0.12)',
            borderWidth: 2.2,
            pointRadius: 2,
            pointHoverRadius: 5,
            fill: true,
            tension: 0.35
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 400, easing: 'easeOutQuad' },
          plugins: {
            legend: { display: false },
            tooltip: tooltipConfig('Illuminance', 'Lux')
          },
          scales: {
            x: { grid: gridConfig, ticks: tickConfig },
            y: { grid: gridConfig, ticks: { ...tickConfig, callback: v => v + ' lx' }, suggestedMin: 600, suggestedMax: 1400 }
          }
        }
      });
    }

    async function pollTelemetryChannels() {
      try {
        const resp = await fetch('/api/sensor_telemetry');
        const data = await resp.json();
        if (!data || data.status !== 'ok') return;

        const latest = data.latest;
        const history = data.history || [];

        if (latest) {
          if (latest.humidity != null) {
            document.getElementById('txtValHumidity').innerText = Number(latest.humidity).toFixed(1);
            // Calculate Vapor Pressure Deficit (VPD in kPa)
            const T = Number(latest.temperature || 24.5);
            const RH = Number(latest.humidity);
            const VPsat = 0.61078 * Math.exp((17.27 * T) / (T + 237.3));
            const VPact = VPsat * (RH / 100.0);
            const vpd = Math.max(0, VPsat - VPact);
            document.getElementById('txtVpd').innerText = `${vpd.toFixed(2)} kPa`;
          }
          if (latest.temperature != null) {
            document.getElementById('txtValTemperature').innerText = Number(latest.temperature).toFixed(1);
          }
          if (latest.soil_adc != null) {
            document.getElementById('txtValSoil').innerText = latest.soil_adc;
            document.getElementById('txtSoilPct').innerText = `${latest.soil_pct || 76.2}%`;
          }
          if (latest.light_lux != null) {
            const lux = Number(latest.light_lux);
            document.getElementById('txtValLight').innerText = lux.toFixed(0);
            const estPpfd = (lux * 0.0185).toFixed(1);
            document.getElementById('txtPpfd').innerText = `~${estPpfd} µmol`;
          }

          if (data.connection) {
            document.getElementById('txtGateway').innerText = `ESP32: ${data.connection.includes('Live') ? 'COM7 LIVE' : 'SYNCED'}`;
          }
        }

        if (history.length > 0) {
          const labels = history.map(h => {
            const raw = h.timestamp || '';
            return raw.includes(' ') ? raw.split(' ')[1] : raw;
          });
          const hums = history.map(h => h.humidity);
          const temps = history.map(h => h.temperature);
          const soils = history.map(h => h.soil_adc);
          const lights = history.map(h => h.light_lux);

          // Update Temperature Gradient trend display
          if (temps.length >= 2) {
            const dt = (temps[temps.length - 1] - temps[0]);
            const sign = dt >= 0 ? '+' : '';
            const trendEl = document.getElementById('txtTempTrend');
            if (trendEl) trendEl.innerText = `${sign}${dt.toFixed(1)}°C/hr`;
          }

          if (chartHumidity) {
            chartHumidity.data.labels = labels;
            chartHumidity.data.datasets[0].data = hums;
            chartHumidity.update('none');
          }
          if (chartTemperature) {
            chartTemperature.data.labels = labels;
            chartTemperature.data.datasets[0].data = temps;
            chartTemperature.update('none');
          }
          if (chartSoil) {
            chartSoil.data.labels = labels;
            chartSoil.data.datasets[0].data = soils;
            chartSoil.update('none');
          }
          if (chartLight) {
            chartLight.data.labels = labels;
            chartLight.data.datasets[0].data = lights;
            chartLight.update('none');
          }
        }
      } catch (err) {
        console.warn('Telemetry poll error:', err);
      }
    }

    async function pollSystemHeartbeat() {
      try {
        const resp = await fetch('/api/status');
        const data = await resp.json();
        if (data.gopro) {
          const bEl = document.getElementById('txtBattery');
          if (bEl) bEl.innerText = `BATTERY: ${data.gopro.battery || '--%'}`;
        }

        // Live AI API Health & Key Quota Monitoring
        if (data.ai_engine) {
          const pillAi = document.getElementById('pillAiApi');
          const txtAi = document.getElementById('txtAiApi');
          if (pillAi && txtAi) {
            pillAi.classList.remove('status-green', 'status-amber', 'status-rose', 'status-blue');
            if (data.ai_engine.status === 'ONLINE') {
              pillAi.classList.add('status-green');
              txtAi.innerText = `AI API: ONLINE (${data.ai_engine.latency_ms}ms)`;
            } else if (data.ai_engine.status === 'KEY_ROTATED') {
              pillAi.classList.add('status-amber');
              txtAi.innerText = `AI API: ROTATED (${data.ai_engine.keys_available}/${data.ai_engine.total_keys})`;
            } else if (data.ai_engine.status === 'QUOTA_EXHAUSTED') {
              pillAi.classList.add('status-amber');
              txtAi.innerText = `AI API: QUOTA LIMIT`;
            } else {
              pillAi.classList.add('status-rose');
              txtAi.innerText = `AI API: OFFLINE`;
            }
          }
        }

        // Asynchronous Pipeline Queue Monitoring
        if (data.queue) {
          const pillQueue = document.getElementById('pillQueue');
          const txtQueue = document.getElementById('txtQueue');
          if (pillQueue && txtQueue) {
            const backlog = (data.queue.queue_depth || 0) + (data.queue.pending_disk_count || 0);
            txtQueue.innerText = `QUEUE: ${backlog} PENDING`;
            pillQueue.classList.remove('status-green', 'status-amber', 'status-rose', 'status-blue');
            if (backlog > 0) {
              pillQueue.classList.add('status-amber');
            } else {
              pillQueue.classList.add('status-blue');
            }
          }
        }

        // Real 4 Snaps / Hour Schedule Countdown
        if (data.scheduler) {
          const txtNextSnap = document.getElementById('txtNextSnap');
          if (txtNextSnap) {
            txtNextSnap.innerText = `NEXT SNAP: ${data.scheduler.countdown_str} (4/HR)`;
          }
        }
      } catch (e) {}
    }

    // SCADA Initialization
    window.addEventListener('load', () => {
      initStream();
      updateSpectrumGate();
      initTechnicalCharts();
      pollTelemetryChannels();
      fetchDiagnoses();

      try {
        if (localStorage.getItem('scada_header_hidden') === 'true') {
          toggleTopBar(true);
        }
      } catch (e) {}

      setInterval(pollTelemetryChannels, 1500);
      setInterval(pollSystemHeartbeat, 1000);
      setInterval(fetchDiagnoses, 8000);
    });
  </script>
</body>
</html>
"""
