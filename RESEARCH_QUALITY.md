# Research Quality Upgrade

This repository has been upgraded with a compact research-quality layer: reference anchors, validation checks, and explicit scientific/software boundaries.

## Scope

Browser Doppler-shift laboratory for radial velocity, relativistic wavelength shifts and astronomical redshift interpretation.

## Equations And Models

- Relativistic Doppler factor sqrt((1+beta)/(1-beta))
- Low-velocity approximation Delta lambda / lambda = v/c

## Reference Anchors

The file `data/research-reference.json` stores benchmark anchors used by `scripts/validate_repository.mjs`. These are intentionally small and auditable so the repository can be checked without network access.

## Browser Upgrade

If this repository contains a browser interface, `research-overlay.js` adds a non-invasive mission-control quality panel with validation status and benchmark telemetry.

## References

- Rybicki, G.B. and Lightman, A.P., 1979. Radiative Processes in Astrophysics. Wiley.
