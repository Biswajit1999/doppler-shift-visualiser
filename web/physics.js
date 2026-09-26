export const C_KMS = 299792.458;

export function validateWavelength(wavelengthNm) {
  if (!Number.isFinite(wavelengthNm) || wavelengthNm <= 0) {
    throw new RangeError("wavelength must be a positive finite value");
  }
}

export function validateVelocity(velocityKms) {
  if (!Number.isFinite(velocityKms) || Math.abs(velocityKms) >= C_KMS) {
    throw new RangeError("velocity must be finite and satisfy |v| < c");
  }
}

export function classicalObservedWavelength(wavelengthNm, velocityKms) {
  validateWavelength(wavelengthNm);
  validateVelocity(velocityKms);
  return wavelengthNm * (1 + velocityKms / C_KMS);
}

export function relativisticDopplerFactor(velocityKms) {
  validateVelocity(velocityKms);
  const beta = velocityKms / C_KMS;
  return Math.sqrt((1 + beta) / (1 - beta));
}

export function relativisticObservedWavelength(wavelengthNm, velocityKms) {
  validateWavelength(wavelengthNm);
  return wavelengthNm * relativisticDopplerFactor(velocityKms);
}

export function spectroscopicRedshift(wavelengthNm, velocityKms) {
  return relativisticObservedWavelength(wavelengthNm, velocityKms) / wavelengthNm - 1;
}

export function photonNoiseRvPrecisionMs(qualityFactor, photoelectrons) {
  if (!Number.isFinite(qualityFactor) || qualityFactor <= 0) {
    throw new RangeError("quality factor must be positive and finite");
  }
  if (!Number.isFinite(photoelectrons) || photoelectrons <= 0) {
    throw new RangeError("photoelectron count must be positive and finite");
  }
  return (C_KMS * 1000) / (qualityFactor * Math.sqrt(photoelectrons));
}
