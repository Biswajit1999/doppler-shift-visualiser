"use strict";

/* ──────────────────────────────────────────────
   PHYSICAL CONSTANTS & LINE DATA
────────────────────────────────────────────── */
const C = 299792.458;          // km s⁻¹
const LAMBDA0 = 589.592;       // nm  —  Na I D₁ rest wavelength (NIST)

// Spectral line catalogue used in the display
// All wavelengths in nm, formatted as { lambda, element, label, strength (0–1) }
const LINES = [
  { lambda: 393.368, element: "Ca II K",  label: "Ca K",  strength: 0.90 },
  { lambda: 396.847, element: "Ca II H",  label: "Ca H",  strength: 0.85 },
  { lambda: 430.790, element: "Fe I",     label: "Fe I",  strength: 0.55 },
  { lambda: 438.355, element: "Fe I",     label: "Fe I",  strength: 0.45 },
  { lambda: 486.134, element: "Hβ",       label: "Hβ",    strength: 0.70 },
  { lambda: 516.733, element: "Mg I b",   label: "Mg b",  strength: 0.60 },
  { lambda: 526.955, element: "Fe I",     label: "Fe I",  strength: 0.40 },
  { lambda: 588.995, element: "Na I D₂",  label: "Na D₂", strength: 0.92, primary: true },
  { lambda: 589.592, element: "Na I D₁",  label: "Na D₁", strength: 0.95, primary: true },
  { lambda: 630.031, element: "O I",      label: "O I",   strength: 0.30 },
  { lambda: 656.281, element: "Hα",       label: "Hα",    strength: 0.88 },
  { lambda: 686.719, element: "O₂ A",     label: "O₂ A",  strength: 0.45 },
  { lambda: 718.536, element: "Ca I",     label: "Ca I",  strength: 0.35 },
];

/* ──────────────────────────────────────────────
   DOM REFERENCES
────────────────────────────────────────────── */
const velocitySlider  = document.getElementById("velocity");
const sliderReadout   = document.getElementById("sliderReadout");
const statVelocity    = document.getElementById("statVelocity");
const statLambda      = document.getElementById("statLambda");
const statDelta       = document.getElementById("statDelta");
const statFrac        = document.getElementById("statFrac");
const statEffect      = document.getElementById("statEffect");
const liveMath        = document.getElementById("liveMath");

const waveCanvas = document.getElementById("waveCanvas");
const wctx       = waveCanvas.getContext("2d");

const specCanvas = document.getElementById("specCanvas");
const sctx       = specCanvas.getContext("2d");

/* ──────────────────────────────────────────────
   SPECTRUM HELPERS
────────────────────────────────────────────── */
const SPEC_MIN = 380;  // nm
const SPEC_MAX = 750;  // nm

function lambdaToX(lambda, canvasWidth, padL, padR) {
  return padL + ((lambda - SPEC_MIN) / (SPEC_MAX - SPEC_MIN)) * (canvasWidth - padL - padR);
}

// Approximate visible-spectrum RGB from wavelength (nm)
function wavelengthToRGB(wl) {
  let r = 0, g = 0, b = 0;
  if      (wl >= 380 && wl < 440) { r = -(wl - 440) / 60; b = 1; g = 0; }
  else if (wl >= 440 && wl < 490) { r = 0; b = 1; g = (wl - 440) / 50; }
  else if (wl >= 490 && wl < 510) { r = 0; b = -(wl - 510) / 20; g = 1; }
  else if (wl >= 510 && wl < 580) { r = (wl - 510) / 70; b = 0; g = 1; }
  else if (wl >= 580 && wl < 645) { r = 1; b = 0; g = -(wl - 645) / 65; }
  else if (wl >= 645 && wl <= 750) { r = 1; b = 0; g = 0; }

  let factor = 1;
  if      (wl >= 380 && wl < 420) factor = 0.3 + 0.7 * (wl - 380) / 40;
  else if (wl >= 700 && wl <= 750) factor = 0.3 + 0.7 * (750 - wl) / 50;

  r = Math.round(255 * Math.pow(r * factor, 0.8));
  g = Math.round(255 * Math.pow(g * factor, 0.8));
  b = Math.round(255 * Math.pow(b * factor, 0.8));
  return `rgb(${r},${g},${b})`;
}

/* ──────────────────────────────────────────────
   DRAW: SPECTRUM CANVAS
────────────────────────────────────────────── */
function drawSpectrum(velocity) {
  const W = specCanvas.width;
  const H = specCanvas.height;
  const PAD_L = 12, PAD_R = 12;
  const barTop = 40, barH = 90;
  const shiftedBarTop = barTop + barH + 48;
  const shiftedBarH   = barH;

  sctx.clearRect(0, 0, W, H);
  sctx.fillStyle = "#04090f";
  sctx.fillRect(0, 0, W, H);

  const doppler = velocity / C;
  const lambdaObs = LAMBDA0 * (1 + doppler);

  /* ── Draw background spectrum gradient ── */
  function drawSpecBar(top, height) {
    const grad = sctx.createLinearGradient(PAD_L, 0, W - PAD_R, 0);
    const steps = 80;
    for (let i = 0; i <= steps; i++) {
      const t   = i / steps;
      const wl  = SPEC_MIN + t * (SPEC_MAX - SPEC_MIN);
      grad.addColorStop(t, wavelengthToRGB(wl));
    }
    sctx.fillStyle = grad;
    sctx.fillRect(PAD_L, top, W - PAD_L - PAD_R, height);

    // Vignette edges
    const vigL = sctx.createLinearGradient(PAD_L, 0, PAD_L + 60, 0);
    vigL.addColorStop(0, "rgba(4,9,15,0.9)");
    vigL.addColorStop(1, "rgba(4,9,15,0)");
    sctx.fillStyle = vigL;
    sctx.fillRect(PAD_L, top, 60, height);

    const vigR = sctx.createLinearGradient(W - PAD_R - 60, 0, W - PAD_R, 0);
    vigR.addColorStop(0, "rgba(4,9,15,0)");
    vigR.addColorStop(1, "rgba(4,9,15,0.9)");
    sctx.fillStyle = vigR;
    sctx.fillRect(W - PAD_R - 60, top, 60, height);
  }

  /* ── Row labels ── */
  function rowLabel(text, y, color) {
    sctx.font = "500 22px 'JetBrains Mono', monospace";
    sctx.fillStyle = color;
    sctx.fillText(text, PAD_L, y);
  }

  // Original spectrum bar
  rowLabel("Rest frame  λ₀ (Na D₁ = 589.592 nm)", barTop - 8, "rgba(180,200,230,0.7)");
  drawSpecBar(barTop, barH);

  // Shifted spectrum bar
  const shiftLabel = velocity > 0
    ? `Redshifted   λ_obs = ${lambdaObs.toFixed(3)} nm  [v = +${velocity} km s⁻¹]`
    : velocity < 0
    ? `Blueshifted  λ_obs = ${lambdaObs.toFixed(3)} nm  [v = ${velocity} km s⁻¹]`
    : `No shift     λ_obs = ${lambdaObs.toFixed(3)} nm  [v = 0 km s⁻¹]`;
  const shiftLabelColor = velocity > 0
    ? "rgba(248,113,113,0.85)"
    : velocity < 0
    ? "rgba(56,189,248,0.85)"
    : "rgba(180,200,230,0.7)";

  rowLabel(shiftLabel, shiftedBarTop - 8, shiftLabelColor);
  drawSpecBar(shiftedBarTop, shiftedBarH);

  /* ── Draw absorption lines on both bars ── */
  function drawAbsorptionLines(barTopY, barHeight, shift) {
    for (const line of LINES) {
      const shifted = line.lambda * (1 + shift);
      if (shifted < SPEC_MIN || shifted > SPEC_MAX) continue;
      const x = lambdaToX(shifted, W, PAD_L, PAD_R);
      const alpha = 0.15 + line.strength * 0.75;

      // Black absorption dip
      const grad = sctx.createLinearGradient(x, barTopY, x, barTopY + barHeight);
      grad.addColorStop(0,   `rgba(0,0,0,0)`);
      grad.addColorStop(0.1, `rgba(0,0,0,${alpha})`);
      grad.addColorStop(0.9, `rgba(0,0,0,${alpha})`);
      grad.addColorStop(1,   `rgba(0,0,0,0)`);
      sctx.fillStyle = grad;

      const lineW = line.primary ? 5 : 3;
      sctx.fillRect(x - lineW / 2, barTopY, lineW, barHeight);
    }
  }

  drawAbsorptionLines(barTop,        barH,        0);       // rest
  drawAbsorptionLines(shiftedBarTop, shiftedBarH, doppler); // shifted

  /* ── Na D indicator lines (prominent) ── */
  function drawNaDIndicator(topY, height, lambda, color, shift) {
    const sx = lambdaToX(lambda * (1 + shift), W, PAD_L, PAD_R);
    if (sx < PAD_L || sx > W - PAD_R) return;

    // Glow
    const grd = sctx.createLinearGradient(sx - 18, 0, sx + 18, 0);
    grd.addColorStop(0,   "rgba(0,0,0,0)");
    grd.addColorStop(0.4, color.replace("1)", "0.25)"));
    grd.addColorStop(0.5, color.replace("1)", "0.5)"));
    grd.addColorStop(0.6, color.replace("1)", "0.25)"));
    grd.addColorStop(1,   "rgba(0,0,0,0)");
    sctx.fillStyle = grd;
    sctx.fillRect(sx - 18, topY - 12, 36, height + 24);

    // Crisp line
    sctx.strokeStyle = color;
    sctx.lineWidth = 2.5;
    sctx.setLineDash([]);
    sctx.beginPath();
    sctx.moveTo(sx, topY - 12);
    sctx.lineTo(sx, topY + height + 12);
    sctx.stroke();

    // Tick + label
    sctx.font = "500 18px 'JetBrains Mono', monospace";
    sctx.fillStyle = color;
    sctx.fillText((lambda * (1 + shift)).toFixed(2) + " nm", sx - 36, topY + height + 32);
  }

  const restColor    = "rgba(230,240,255,1)";
  const shiftedColor = velocity > 0
    ? "rgba(248,113,113,1)"
    : velocity < 0
    ? "rgba(56,189,248,1)"
    : "rgba(230,240,255,0.6)";

  drawNaDIndicator(barTop,        barH,        LAMBDA0, restColor,    0);
  drawNaDIndicator(shiftedBarTop, shiftedBarH, LAMBDA0, shiftedColor, doppler);

  /* ── Connecting dashed line between bars ── */
  if (Math.abs(velocity) > 0) {
    const x0  = lambdaToX(LAMBDA0, W, PAD_L, PAD_R);
    const x1  = lambdaToX(lambdaObs, W, PAD_L, PAD_R);
    const y0  = barTop + barH + 12;
    const y1  = shiftedBarTop - 12;
    const mid = (y0 + y1) / 2;

    sctx.strokeStyle = "rgba(74,240,200,0.35)";
    sctx.lineWidth = 1.5;
    sctx.setLineDash([5, 5]);
    sctx.beginPath();
    sctx.moveTo(x0, y0);
    sctx.bezierCurveTo(x0, mid, x1, mid, x1, y1);
    sctx.stroke();
    sctx.setLineDash([]);

    // Δλ arrow label
    const midX = (x0 + x1) / 2;
    const delta = lambdaObs - LAMBDA0;
    sctx.font = "500 17px 'JetBrains Mono', monospace";
    sctx.fillStyle = "rgba(74,240,200,0.9)";
    const sign = delta >= 0 ? "+" : "";
    sctx.fillText(`Δλ = ${sign}${delta.toFixed(4)} nm`, midX - 50, mid + 6);
  }
}

/* ──────────────────────────────────────────────
   DRAW: WAVE ANIMATION CANVAS
────────────────────────────────────────────── */
let waveT = 0;
let lastV = 0;

function drawWaves(velocity) {
  const W = waveCanvas.width;
  const H = waveCanvas.height;

  wctx.clearRect(0, 0, W, H);

  // Background
  wctx.fillStyle = "#04090f";
  wctx.fillRect(0, 0, W, H);

  // Stars
  const rng = mulberry32(42);
  for (let i = 0; i < 80; i++) {
    const x = rng() * W;
    const y = rng() * H;
    const a = 0.2 + rng() * 0.5;
    wctx.fillStyle = `rgba(200,220,255,${a})`;
    const r = 0.5 + rng() * 0.8;
    wctx.beginPath();
    wctx.arc(x, y, r, 0, Math.PI * 2);
    wctx.fill();
  }

  const cx = W * 0.46;
  const cy = H * 0.52;
  const v  = velocity;

  // Observer marker
  const obsX = W - 44;
  const obsY = cy;
  wctx.fillStyle = "rgba(74,240,200,0.15)";
  wctx.strokeStyle = "rgba(74,240,200,0.5)";
  wctx.lineWidth = 1;
  wctx.beginPath();
  wctx.arc(obsX, obsY, 14, 0, Math.PI * 2);
  wctx.fill();
  wctx.stroke();
  wctx.fillStyle = "rgba(74,240,200,0.9)";
  wctx.font = "bold 11px 'JetBrains Mono', monospace";
  wctx.textAlign = "center";
  wctx.fillText("👁", obsX, obsY + 4);

  // Observer label
  wctx.fillStyle = "rgba(74,240,200,0.6)";
  wctx.font = "11px 'JetBrains Mono', monospace";
  wctx.fillText("Observer", obsX, obsY + 28);

  // Source star
  const starGrad = wctx.createRadialGradient(cx, cy, 0, cx, cy, 26);
  starGrad.addColorStop(0,   "#fffbe6");
  starGrad.addColorStop(0.3, "#fef3c7");
  starGrad.addColorStop(1,   "rgba(251,191,36,0)");
  wctx.fillStyle = starGrad;
  wctx.beginPath();
  wctx.arc(cx, cy, 26, 0, Math.PI * 2);
  wctx.fill();

  // Star core
  wctx.fillStyle = "#fde68a";
  wctx.beginPath();
  wctx.arc(cx, cy, 14, 0, Math.PI * 2);
  wctx.fill();

  // Velocity arrow
  if (Math.abs(v) > 0) {
    const arrowDir = v < 0 ? 1 : -1;
    const arrowLen = Math.min(Math.abs(v) / 300 * 80, 80);
    drawArrow(wctx, cx, cy, cx + arrowDir * arrowLen, cy,
              v < 0 ? "rgba(56,189,248,0.9)" : "rgba(248,113,113,0.9)");
  }

  // Wavefronts
  const colour = v < 0 ? "#38bdf8" : v > 0 ? "#f87171" : "#94a3b8";
  const baseSpacing = 38;

  // Doppler: compress/expand spacing in direction of motion
  const betaVis = (v / 300) * 0.45;  // visual exaggeration

  const numWaves = 8;
  for (let i = 0; i < numWaves; i++) {
    const phase = (waveT * 0.9 + i * 1.0) % numWaves;

    // Asymmetric spacing: compressed toward observer (right), expanded away
    const spacingRight = baseSpacing * (1 - betaVis);  // toward observer
    const spacingLeft  = baseSpacing * (1 + betaVis);  // away from observer

    // Draw full-circle wavefront with asymmetric radius
    const r = phase * baseSpacing;
    if (r < 8) continue;

    const alpha = Math.max(0, 0.6 - phase / numWaves * 0.6);

    // Approximate ellipse to show Doppler compression/expansion
    const rxRight = phase * spacingRight;
    const rxLeft  = phase * spacingLeft;
    const ry      = r;

    wctx.strokeStyle = colour.replace(")", `,${alpha})`).replace("rgb", "rgba").replace("rgba(#", "rgba(");
    wctx.lineWidth = 1.4;
    wctx.beginPath();

    // Right half (toward observer): compressed
    wctx.ellipse(cx + (rxRight - r) * 0.5, cy, rxRight, ry, 0, -Math.PI / 2, Math.PI / 2);
    // Left half (away from observer): expanded
    wctx.ellipse(cx - (rxLeft - r) * 0.5,  cy, rxLeft,  ry, 0, Math.PI / 2, 3 * Math.PI / 2);

    wctx.stroke();
  }

  // Labels
  wctx.font = "600 11px 'JetBrains Mono', monospace";
  wctx.textAlign = "left";
  const effLabel = v > 0 ? "REDSHIFT" : v < 0 ? "BLUESHIFT" : "NO SHIFT";
  const effColor = v > 0 ? "#f87171" : v < 0 ? "#38bdf8" : "#94a3b8";
  wctx.fillStyle = effColor;
  wctx.fillText(effLabel, 14, 22);

  if (Math.abs(v) > 0) {
    wctx.fillStyle = "rgba(150,170,200,0.6)";
    wctx.font = "10px 'JetBrains Mono', monospace";
    wctx.fillText("← compressed wavefronts   expanded wavefronts →", 14, H - 14);
  }

  wctx.textAlign = "left";
  waveT += 0.06;
}

function drawArrow(ctx, x1, y1, x2, y2, color) {
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const len   = Math.hypot(x2 - x1, y2 - y1);
  if (len < 4) return;

  ctx.strokeStyle = color;
  ctx.lineWidth   = 2.5;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();

  const hs = 10;
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - hs * Math.cos(angle - 0.4), y2 - hs * Math.sin(angle - 0.4));
  ctx.lineTo(x2 - hs * Math.cos(angle + 0.4), y2 - hs * Math.sin(angle + 0.4));
  ctx.closePath();
  ctx.fill();
}

// Seeded RNG for stable star positions
function mulberry32(a) {
  return function() {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

/* ──────────────────────────────────────────────
   UPDATE STATS & UI
────────────────────────────────────────────── */
function formatSci(x) {
  if (x === 0) return "0";
  const exp  = Math.floor(Math.log10(Math.abs(x)));
  const mant = (x / Math.pow(10, exp));
  return `${mant.toFixed(3)} × 10${superscript(exp)}`;
}

function superscript(n) {
  const map = {"0":"⁰","1":"¹","2":"²","3":"³","4":"⁴","5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹","-":"⁻"};
  return String(n).split("").map(c => map[c] || c).join("");
}

function updateStats(v) {
  const doppler    = v / C;
  const lambdaObs  = LAMBDA0 * (1 + doppler);
  const delta      = lambdaObs - LAMBDA0;
  const frac       = delta / LAMBDA0;

  // Slider readout
  const sign = v > 0 ? "+" : "";
  sliderReadout.textContent = `v = ${sign}${v} km s⁻¹`;

  // Stat cards
  statVelocity.textContent = `${sign}${v}`;
  statLambda.textContent   = lambdaObs.toFixed(4);
  statDelta.textContent    = (delta >= 0 ? "+" : "") + delta.toFixed(5);
  statFrac.textContent     = formatSci(frac);

  // Effect
  let effText  = "No shift";
  let effColor = "#94a3b8";
  if (v > 0)  { effText = "Redshift  (receding)";   effColor = "#f87171"; }
  if (v < 0)  { effText = "Blueshift  (approaching)"; effColor = "#38bdf8"; }
  statEffect.textContent = effText;
  statEffect.style.color = effColor;

  // Live math
  const deltaStr = (delta >= 0 ? "+" : "") + delta.toFixed(5);
  liveMath.innerHTML = `
    Δλ = λ₀ · (v/c)<br>
    Δλ = ${LAMBDA0} × (${sign}${v} / ${C})<br>
    Δλ = ${LAMBDA0} × ${doppler.toExponential(4)}<br>
    Δλ = <strong>${deltaStr} nm</strong>
  `;
}

/* ──────────────────────────────────────────────
   ANIMATION LOOP
────────────────────────────────────────────── */
function loop() {
  const v = Number(velocitySlider.value);
  drawWaves(v);
  requestAnimationFrame(loop);
}

/* ──────────────────────────────────────────────
   EVENTS
────────────────────────────────────────────── */
function applyVelocity(v) {
  velocitySlider.value = v;
  updateStats(v);
  drawSpectrum(v);
  document.querySelectorAll(".preset-btn").forEach(b => {
    b.classList.toggle("active", Number(b.dataset.v) === v);
  });
}

velocitySlider.addEventListener("input", () => {
  const v = Number(velocitySlider.value);
  applyVelocity(v);
});

document.querySelectorAll(".preset-btn").forEach(btn => {
  btn.addEventListener("click", () => applyVelocity(Number(btn.dataset.v)));
});

/* ──────────────────────────────────────────────
   INIT
────────────────────────────────────────────── */
applyVelocity(0);
loop();
