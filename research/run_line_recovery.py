"""Reproducible seeded Gaussian-line Doppler/telluric experiment (synthetic only)."""
from __future__ import annotations
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import numpy as np
from research.line_recovery import injection_recovery


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("outputs/line_recovery_synthetic.json"))
    parser.add_argument("--trials", type=int, default=60)
    args = parser.parse_args()
    wavelength = np.linspace(589.25, 589.95, 240)
    result = {
        "kind": "seeded synthetic line experiment; no observed RV",
        "clean": asdict(injection_recovery(wavelength, n_trials=args.trials)),
        "blended_unmasked": asdict(injection_recovery(wavelength, n_trials=args.trials,
                          telluric_centre_nm=589.615, telluric_depth=0.25)),
        "blended_masked": asdict(injection_recovery(wavelength, n_trials=args.trials,
                          telluric_centre_nm=589.615, telluric_depth=0.25,
                          mask_telluric=True)),
        "limitations": ["single Gaussian stellar line", "fixed observer-frame telluric line",
                        "independent Gaussian pixel noise", "no wavelength calibration or barycentric corrections"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote synthetic injection diagnostics to {args.output}")


if __name__ == "__main__":
    main()
