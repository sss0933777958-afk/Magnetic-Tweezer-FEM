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

### `long-fei/` — Reference Design (Fei Long 2016)

Reference hexapole from Fei Long's PhD dissertation (Ohio State University, 2016).

| Folder | Contents |
|--------|----------|
| `step_for_fem/` | ANSYS-ready model (`MTmodel.step`) |
| `reference/` | APDL modeling scripts |


## Notes

- Git tracks **STEP files only** — SolidWorks source files (.SLDPRT/.SLDASM) are kept locally
- FEM simulation scripts and post-processing are in a separate repo: [magnetic-tweezers-sim](https://github.com/kevinfan100/magnetic-tweezers-sim)

## Reference

> Fei Long, "Active Control of the Probe-Sample Interaction Force at the Piconewton Scale by a Magnetic Microprobe in Aqueous Solutions," PhD dissertation, Ohio State University, 2016.
