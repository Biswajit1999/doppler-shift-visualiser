"""Show where Doppler precision comes from in a simulated absorption line."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from research.doppler_diagnostics import rv_information_mask_sensitivity

ROOT = Path(__file__).resolve().parents[1]
wavelength = np.linspace(589.42, 589.76, 341)
centre = 589.592
width = 0.027
flux = 1 - 0.45 * np.exp(-0.5 * ((wavelength - centre) / width) ** 2)
sigma = np.full_like(flux, 0.01)
offset = np.abs(np.arange(wavelength.size) - np.argmin(np.abs(wavelength - centre)))
core = (offset >= 1) & (offset <= 8)
wings = (offset >= 24) & (offset <= 31)
full, core_only, wings_only = rv_information_mask_sensitivity(
    wavelength, flux, sigma, [np.ones_like(core), core, wings]
)

with plt.rc_context({"svg.fonttype": "none", "svg.hashsalt": "rv-information", "font.size": 11}):
    figure, (spectrum, precision) = plt.subplots(
        1, 2, figsize=(8.8, 3.9), width_ratios=(1.4, 1), layout="constrained"
    )
    figure.suptitle("The steep wings carry more Doppler information", x=0.015, ha="left", fontweight="bold")
    spectrum.plot(wavelength, flux, color="#1d3848", lw=1.5)
    spectrum.fill_between(wavelength, 0.5, 1.03, where=core, color="#b14d33", alpha=0.2)
    spectrum.fill_between(wavelength, 0.5, 1.03, where=wings, color="#1c6f72", alpha=0.23)
    spectrum.set(xlabel="Wavelength (nm)", ylabel="Normalised flux", ylim=(0.51, 1.03))
    spectrum.ticklabel_format(useOffset=False)
    spectrum.set_xticks([589.45, 589.59, 589.73])
    precision.barh(
        [f"All bins ({flux.size})", f"Core ({core.sum()})", f"Wings ({wings.sum()})"],
        [full, core_only, wings_only],
        color=["#1d3848", "#b14d33", "#1c6f72"],
    )
    precision.invert_yaxis()
    precision.set(xlabel="Conditional 1σ RV uncertainty (m/s)")
    precision.grid(axis="x", alpha=0.2)
    precision.set_axisbelow(True)
    for axis in (spectrum, precision):
        axis.spines[["top", "right"]].set_visible(False)
    figure.savefig(ROOT / "web/rv-information.svg", metadata={"Date": None})
    plt.close(figure)
