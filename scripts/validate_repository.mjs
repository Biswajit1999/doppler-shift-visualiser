import fs from "node:fs";

const required = [
  "README.md",
  "docs/METHODS.md",
  "docs/VALIDATION.md",
  "docs/DATA_SOURCES.md",
  "docs/LIMITATIONS.md",
  "data/research-reference.json",
  "web/index.html",
  "web/physics.js",
  "web/script.js",
];

const failures = required.filter((file) => !fs.existsSync(file)).map((file) => `${file} missing`);
const references = JSON.parse(fs.readFileSync("data/research-reference.json", "utf8"));
if (!Array.isArray(references.anchors) || references.anchors.length < 3) {
  failures.push("reference anchors missing");
}

const html = fs.readFileSync("web/index.html", "utf8");
const script = fs.readFileSync("web/script.js", "utf8");
const physics = fs.readFileSync("web/physics.js", "utf8");
if (!html.includes('type="module" src="script.js')) failures.push("physics module is not loaded");
if (!script.includes('frame: "telluric"')) failures.push("telluric frame metadata missing");
if (!script.includes('line.frame === "telluric"')) failures.push("telluric line is not held fixed");
if (!physics.includes("Math.sqrt((1 + beta) / (1 - beta))")) {
  failures.push("relativistic Doppler factor missing");
}
if (html.includes("Used for cosmological redshifts")) failures.push("cosmological overclaim remains");
if (html.includes("(c / R)")) failures.push("unsupported RV precision equation remains");

const combined = required.map((file) => fs.readFileSync(file, "utf8")).join("\n").toLowerCase();
for (const token of ["todo", "placeholder", "insert logic", "coming soon"]) {
  if (combined.includes(token)) failures.push(`unfinished token ${token}`);
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}
console.log(`doppler-shift-visualiser: validation passed with ${references.anchors.length} anchors.`);
