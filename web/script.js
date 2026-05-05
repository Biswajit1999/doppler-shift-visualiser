const canvas = document.getElementById("spectrumCanvas");
const ctx = canvas.getContext("2d");

const velocitySlider = document.getElementById("velocity");
const velocityValue = document.getElementById("velocityValue");
const resultText = document.getElementById("resultText");

const c = 299792.458;

function drawSpectrum(velocity) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const centreOriginal = 450;
  const shiftPixels = (velocity / c) * 5000;
  const centreShifted = centreOriginal + shiftPixels;

  ctx.fillStyle = "#05070d";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  drawAxis();

  drawAbsorptionLine(centreOriginal, "#60a5fa", "Original line");
  drawAbsorptionLine(centreShifted, velocity >= 0 ? "#f87171" : "#38bdf8", "Shifted line");

  ctx.fillStyle = "#ffffff";
  ctx.font = "16px Arial";
  ctx.fillText("Shorter wavelength / blue", 70, 320);
  ctx.fillText("Longer wavelength / red", 650, 320);
}

function drawAxis() {
  ctx.strokeStyle = "#64748b";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(70, 260);
  ctx.lineTo(830, 260);
  ctx.stroke();

  const gradient = ctx.createLinearGradient(70, 0, 830, 0);
  gradient.addColorStop(0, "#3b82f6");
  gradient.addColorStop(0.5, "#22c55e");
  gradient.addColorStop(1, "#ef4444");

  ctx.fillStyle = gradient;
  ctx.fillRect(70, 220, 760, 25);
}

function drawAbsorptionLine(x, color, label) {
  ctx.strokeStyle = color;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(x, 90);
  ctx.lineTo(x, 260);
  ctx.stroke();

  ctx.fillStyle = color;
  ctx.font = "15px Arial";
  ctx.fillText(label, x - 45, 75);
}

function update() {
  const velocity = Number(velocitySlider.value);
  velocityValue.textContent = velocity;

  let effect = "No shift";
  if (velocity > 0) effect = "Redshift: object moving away";
  if (velocity < 0) effect = "Blueshift: object moving towards us";

  resultText.textContent = effect;
  drawSpectrum(velocity);
}

velocitySlider.addEventListener("input", update);
update();
