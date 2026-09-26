# Changelog

## [2.0.0] - 2026-09-26

### Corrected

- Replaced the unsupported RV-precision expression with the Bouchy–Pepe–Queloz photon-noise quality-factor relation.
- Removed the claim that the longitudinal special-relativistic equation models cosmological redshift.
- Corrected the 686.7 nm oxygen feature to the telluric O₂ B band and hold it fixed in the observer frame.
- Use the exact longitudinal relativistic Doppler factor for displayed source-frame wavelengths, with the first-order residual reported separately.
- Create the Python output directory before saving figures.

### Added

- Shared browser physics module with fail-closed input validation.
- Six JavaScript analytic tests and five independent Python tests.
- Methods, validation, sources, and limitations documents grounded in NIST, IAU terminology, Bouchy et al. (2001), and ESO instrument context.
- Commit-pinned Node 24 and Python 3.12 continuous integration.

### Interface

- Rebalanced the wavefront and numerical-statistic columns at laptop widths.
- Added exact redshift and exact-minus-first-order telemetry.
- Removed public “research upgrade” framing in favour of reader-facing scientific documentation.
