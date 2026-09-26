# Validation

JavaScript unit tests verify analytic identities and limits:

- zero velocity leaves wavelength unchanged;
- exact redshift has the declared sign convention;
- low-velocity classical and exact calculations agree;
- Doppler factors at equal positive and negative velocities are reciprocal;
- photon-noise precision matches `c/(Q sqrt(N_e))`; and
- nonphysical inputs fail closed.

The repository validator checks required evidence files, reference anchors, frame metadata for the telluric feature, module loading, and the absence of unfinished tokens. These checks establish implementation consistency, not observational validation.

The painted spectrum has not been compared pixel-by-pixel with a calibrated stellar atlas. Wavelength anchors are educational labels, not a fitted line list.
