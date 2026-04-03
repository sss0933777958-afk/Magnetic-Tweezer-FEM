# STEP Files for FEM Simulation

## Description
Individual part STEP files used as dimensional references for the ANSYS magnetostatic simulation.
These parts define the geometry of the Hung hexapole magnetic tweezers.

## Parts List

### Mag_Pole_Bottom.STEP — Magnetic Pole
The conical/cylindrical pole with D-shape flat cut.
6 poles are arranged on a sphere (3 upper, 3 lower).

| Parameter | Value | Note |
|-----------|-------|------|
| Shaft radius | 3.175 mm | 1/8 inch |
| Cone length | 15.875 mm | Taper from tip (R=0) to shaft |
| Flat cut length | 28.0 mm | D-shape section (front) |
| Total length | 43.0 mm | Tip to far end |
| Tip radius | 0 mm | Sharp conical tip (no fillet) |

### Pole_Block_Top.STEP — Upper Pole Block
L-shaped mounting block for upper poles (P2, P4, P5).
Pole penetrates 7.0 mm into the block.

| Parameter | Value |
|-----------|-------|
| Main body | 13.0 x 22.0 x 10.0 mm (side x up x thickness) |
| Extension | 12.0 x 10.0 x 10.0 mm |
| Overall footprint | 25.0 x 22.0 mm |
| Thickness | 10.0 mm |
| Pole penetration | 7.0 mm |

### Pole_Block_Bottom.STEP — Lower Pole Block
L-shaped mounting block for lower poles (P1, P3, P6).
Pole penetrates 4.5 mm into the block.

| Parameter | Value |
|-----------|-------|
| Main body | 7.0 x 22.0 x 10.0 mm |
| Extension | 15.0 x 10.0 x 10.0 mm |
| Overall footprint | 22.0 x 22.0 mm |
| Thickness | 10.0 mm |
| Pole penetration | 4.5 mm |

### Mag_Guide_Post.STEP — Magnetic Guide Post
Cylindrical iron core connecting the yoke to lower pole blocks.
3 guide posts serve the 3 lower poles (P1, P3, P6).
Upper poles use identical "upper cores" connecting to the yoke.

| Parameter | Value |
|-----------|-------|
| Radius | 4.0 mm |
| Height | 46.0 mm |
| Material | 1018 steel (mu_r = 280) |

### Coil.STEP — Excitation Coil
Ring-shaped coil wound around the guide post / upper core, positioned above the block.

| Parameter | Value |
|-----------|-------|
| Inner radius | 10.0 mm |
| Outer radius | 12.0 mm |
| Height | 15.0 mm |
| Turns | 70 |
| Current | 1 A per turn (70 A-turns total) |

### Upper_Ring.STEP — Yoke (Magnetic Iron Ring)
Annular iron plate connecting all 6 guide posts / upper cores.
Provides the return path for magnetic flux.

| Parameter | Value |
|-----------|-------|
| Inner radius | 38.0 mm |
| Outer radius | 62.5 mm |
| Thickness | 2.0 mm |
| Material | 1018 steel (mu_r = 280) |

### Full_Assembly_inch.STEP — Complete Assembly
All parts assembled in the hexapole configuration.
Coordinate system: ANSYS global (X = P1 direction, Z = up).

## Units
All STEP files are in **millimeters**.

## Usage in Simulation
The ANSYS APDL simulation (`magnetic-tweezers-sim/hung/apdl/`) builds geometry parametrically
from code using these dimensions. The STEP files are not imported directly into ANSYS —
they serve as the dimensional reference and for SolidWorks visualization/verification.
