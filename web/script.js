const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const velocitySlider = document.getElementById("velocity");
const velocityValue = document.getElementById("velocityValue");
const effect = document.getElementById("effect");
const shiftedLine = document.getElementById("shiftedLine");
const deltaLambda = document.getElementById("deltaLambda");

const C = 299792.458;
const lambda0 = 589.0;

function wavelengthToX(lambda) {
  const min = 560;
  const max = 620;
  return 110 + ((lambda - min) / (max - min)) * 780;
}

function drawStars() {
  for (let i = 0; i < 160; i++) {
    ctx.fillStyle = `rgba(255,255,255,${Math.random() * 0.65})`;
    ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 1.2, 1.2);
  }
}

function drawSpectrum(y, label, shiftedLambda, colour) {
  const x0 = 110;
  const width = 780;

  const grad = ctx.createLinearGradient(x0, 0, x0 + width, 0);
  grad.addColorStop(0, "#2563eb");
  grad.addColorStop(0.25, "#06b6d4");
  grad.addColorStop(0.5, "#22c55e");
  grad.addColorStop(0.72, "#facc15");
  grad.addColorStop(1, "#ef4444");

  ctx.fillStyle = grad;
  ctx.fillRect(x0, y, width, 36);

  ctx.fillStyle = "rgba(0,0,0,0.82)";
  for (let line of [570, 577, 589, 607, 614]) {
    const lx = wavelengthToX(line);
    ctx.fillRect(lx, y, 4, 36);
  }

  const sx = wavelengthToX(shiftedLambda);
  ctx.strokeStyle = colour;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(sx, y - 35);
  ctx.lineTo(sx, y + 65);
  ctx.stroke();

  ctx.fillStyle = colour;
  ctx.font = "16px Arial";
  ctx.fillText(label, x0, y - 15);
  ctx.fillText(`${shiftedLambda.toFixed(3)} nm`, sx - 38, y - 15);
}

function drawWavePanel(velocity) {
  const cx = canvas.width / 2;
  const cy = 145;

  ctx.fillStyle = "#facc15";
  ctx.beginPath();
  ctx.arc(cx, cy, 35, 0, Math.PI * 2);
  ctx.fill();

  const colour = velocity > 0 ? "#f87171" : velocity < 0 ? "#38bdf8" : "#e5e7eb";
  const spacing = velocity > 0 ? 42 : velocity < 0 ? 22 : 32;

  ctx.strokeStyle = colour;
  ctx.lineWidth = 2;

  for (let r = 55; r < 260; r += spacing) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.stroke();
  }

  ctx.fillStyle = "#cbd5e1";
  ctx.font = "16px Arial";
  ctx.fillText("Light waves from moving star", cx - 100, 45);
}

function update() {
  const v = Number(velocitySlider.value);
  const shifted = lambda0 * (1 + v / C);
  const delta = shifted - lambda0;

  velocityValue.textContent = v;
  shiftedLine.textContent = `${shifted.toFixed(3)} nm`;
  deltaLambda.textContent = `${delta >= 0 ? "+" : ""}${delta.toFixed(4)} nm`;

  if (v > 0) effect.textContent = "Redshift";
  else if (v < 0) effect.textContent = "Blueshift";
  else effect.textContent = "No shift";

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#020617";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  drawStars();
  drawWavePanel(v);

  drawSpectrum(300, "Original sodium-like absorption line", lambda0, "#e5e7eb");
  drawSpectrum(390, "Doppler shifted line", shifted, v >= 0 ? "#fb7185" : "#38bdf8");

  ctx.strokeStyle = "#64748b";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(110, 470);
  ctx.lineTo(890, 470);
  ctx.stroke();

  ctx.fillStyle = "#94a3b8";
  ctx.font = "15px Arial";
  ctx.fillText("Shorter wavelength / blue", 110, 495);
  ctx.fillText("Longer wavelength / red", 690, 495);
}

document.querySelectorAll("button[data-v]").forEach(button => {
  button.addEventListener("click", () => {
    velocitySlider.value = button.dataset.v;
    update();
  });
});

velocitySlider.addEventListener("input", update);
update();
