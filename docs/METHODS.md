# Methods

The browser uses a signed line-of-sight convention: positive velocity means the source is receding and produces positive redshift; negative velocity means approaching and produces blueshift.

The primary numerical relation is the longitudinal special-relativistic Doppler factor for source and observer in inertial relative motion:

`D = lambda_obs / lambda_0 = sqrt((1 + beta)/(1 - beta))`, where `beta = v/c`.

The first-order comparison is `lambda_obs = lambda_0(1 + v/c)`. Both functions reject non-finite inputs, non-positive wavelengths, and `|v| >= c`.

Stellar features are transformed by the exact factor. The displayed O₂ B feature is tagged as telluric and held fixed in the observer frame. The colored continuum and line depths are illustrative; only the wavelength transformation is used as a quantitative result.

The stated photon-noise floor follows Bouchy, Pepe & Queloz (2001): `sigma_v = c/(Q sqrt(N_e))`. The interface does not derive Q or N_e and therefore does not claim an RV precision for the painted spectrum.
