# Hung Hexapole Magnetic Tweezers — CAD Files

## Overview
This folder contains CAD files for the Hung hexapole magnetic tweezers design.
The design features 6 tilted poles arranged on a sphere (R = 0.5 mm) at magic angle (54.74°),
with upper poles tilted 35° above horizontal and lower poles tilted 5.71° below horizontal.

## Folder Structure

```
hung/
├── step_for_fem/    STEP files of individual parts (used in FEM simulation)
├── reference/       Reference materials (drawings, datasheets, etc.)
└── README.md        This file
```

## Related Projects
- **FEM simulation**: `magnetic-tweezers-sim/hung/` — ANSYS APDL magnetostatic simulation
- **IGES exports**: `magnetic-tweezers-sim/hung/IGES/` — IGES files generated from simulation geometry

## Design Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| R_sphere | 0.5 mm | Working sphere radius (tip-to-center distance) |
| Magic angle | 54.74° | Polar angle of pole arrangement |
| TILT_UP | 35° | Upper pole tilt (P2, P4, P5) |
| TILT_DN | 5.71° | Lower pole tilt (P1, P3, P6) |
| Pole total length | 43.0 mm | From tip to far end |
| Pole shaft radius | 3.175 mm (1/8 inch) | Cylindrical section |
| Pole cone length | 15.875 mm | Conical taper section |
| Pole flat length | 28.0 mm | D-shape flat cut section |
| Steel permeability | mu_r = 280 | 1018 steel |
