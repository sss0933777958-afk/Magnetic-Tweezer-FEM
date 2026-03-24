# magnetic-tweezer-cad

Hexapole magnetic tweezer CAD model repository. Contains two hexapole designs with STEP geometry files for FEM simulation.

## Designs

### `hung/` — New Hexapole Design (Hung Lab)

Current design under development. Includes original CAD geometry and FEM-ready simplified versions.

| Folder | Contents |
|--------|----------|
| `assembly/` | Full assembly STEP |
| `parts/` | Individual part STEP files (original, with screw holes) |
| `step_for_fem/` | Simplified STEP files for FEM (holes removed, poles aligned to 1.0 mm tip distance) |
| `scripts/` | CadQuery/Python preprocessing scripts (fill holes, align poles, verify geometry) |

### `long-fei/` — Reference Design (Fei Long 2016)

Reference hexapole from Fei Long's PhD dissertation (Ohio State University, 2016).

| Folder | Contents |
|--------|----------|
| `step_for_fem/` | ANSYS-ready model (`MTmodel.step`) |
| `reference/` | APDL modeling scripts |


## Scripts (`hung/scripts/`)

All scripts use [CadQuery](https://cadquery.readthedocs.io/) + OpenCascade. Requires Python 3.10+ and `pip install cadquery`.

| Script | Purpose |
|--------|---------|
| `fill_holes.py` | Remove screw holes from `parts/` → `step_for_fem/` |
| `adjust_pole_z.py` | Adjust upper pole positions for 1.0 mm tip-to-tip distance |
| `verify_tip_alignment.py` | Verify opposing pole pair colinearity |
| `plot_pole_mapping.m` | MATLAB visualization of pole positions (requires MATLAB R2020a+) |

## Notes

- Git tracks **STEP files and scripts** — SolidWorks source files (.SLDPRT/.SLDASM) are kept locally
- FEM simulation scripts and post-processing are in a separate repo: [magnetic-tweezers-sim](https://github.com/kevinfan100/magnetic-tweezers-sim)

## Reference

> Fei Long, "Active Control of the Probe-Sample Interaction Force at the Piconewton Scale by a Magnetic Microprobe in Aqueous Solutions," PhD dissertation, Ohio State University, 2016.
