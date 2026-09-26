import assert from "node:assert/strict";
import test from "node:test";

import {
  C_KMS,
  classicalObservedWavelength,
  photonNoiseRvPrecisionMs,
  relativisticDopplerFactor,
  relativisticObservedWavelength,
  spectroscopicRedshift,
} from "../web/physics.js";

test("zero velocity leaves wavelength unchanged", () => {
  assert.equal(classicalObservedWavelength(589.592, 0), 589.592);
  assert.equal(relativisticObservedWavelength(589.592, 0), 589.592);
});

test("relativistic Doppler factor obeys reciprocal symmetry", () => {
  const velocity = 30000;
  assert.ok(Math.abs(relativisticDopplerFactor(velocity) * relativisticDopplerFactor(-velocity) - 1) < 1e-14);
});

test("classical approximation agrees at low velocity", () => {
  const rest = 589.592;
  const velocity = 0.03;
  const classical = classicalObservedWavelength(rest, velocity);
  const exact = relativisticObservedWavelength(rest, velocity);
  assert.ok(Math.abs(classical - exact) < 1e-10);
});

test("redshift has the expected sign", () => {
  assert.ok(spectroscopicRedshift(589.592, 30) > 0);
  assert.ok(spectroscopicRedshift(589.592, -30) < 0);
});

test("photon-noise precision follows Bouchy quality-factor form", () => {
  const precision = photonNoiseRvPrecisionMs(20000, 1e8);
  assert.ok(Math.abs(precision - (C_KMS * 1000) / 2e8) < 1e-12);
});

test("nonphysical inputs fail closed", () => {
  assert.throws(() => relativisticObservedWavelength(-1, 0), RangeError);
  assert.throws(() => relativisticObservedWavelength(500, C_KMS), RangeError);
  assert.throws(() => photonNoiseRvPrecisionMs(0, 100), RangeError);
});
