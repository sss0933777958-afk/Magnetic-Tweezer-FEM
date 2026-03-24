# magnetic-tweezer-fem

六極電磁鑷子 FEM 模擬專案：CAD 幾何預處理 → ANSYS 磁場模擬。

## Commands
```bash
python scripts/fill_holes.py              # Remove screw holes from cad/parts/ → fem/parts/
python scripts/adjust_pole_z.py           # Align pole tips to 1.0 mm distance → fem/Hexapole_Assembly_FEM.STEP
python scripts/verify_tip_alignment.py    # Verify 3 opposing pole pairs on fem/Hexapole_Assembly_FEM.STEP
```

## Architecture
- `cad/` — Original STEP geometry (exported from SolidWorks)
- `fem/` — FEM-ready simplified geometry (holes removed, poles aligned)
- `scripts/` — CadQuery preprocessing scripts
- `reference/` — Fei Long 2016 reference design (MTmodel.step + APDL scripts)
- `figures/` — Visualization outputs

## Pole Naming & Geometry
- Upper plane: P2 (upper-left), P4 (upper-center), P5 (upper-right)
- Lower plane: P6 (lower-left), P3 (lower-center), P1 (lower-right)
- 3 opposing pairs: P1↔P2, P3↔P4, P5↔P6
- Each pair axis must be colinear; the 3 pair axes must intersect at a single center point
- Coordinate systems: (x_m, y_m, z_m) magnetic frame, (x_a, y_a, z_a) actuator frame
- OCP traversal → paper mapping: classify by axis_z sign (upper <0, lower >0), then by axis XY angle:
  - Upper: ~+90°→P2, ~-30°→P4, ~-150°→P5
  - Lower: ~-90°→P1, ~+150°→P3, ~+30°→P6
- Opposing pairs have ~180° XY angle difference: P1(-90°)↔P2(+90°), P3(+150°)↔P4(-30°), P5(-150°)↔P6(+30°)

## Verification
- After modifying fill_holes.py, re-run and confirm all files appear in fem/parts/
- After any geometry change, run verify_tip_alignment.py — all 3 pairs must PASS
- After recalculation, verify 3 pair axes converge to a single center point
- Before adding new scripts, confirm CadQuery imports successfully

## Rules
- Write all code using CadQuery (use OCP low-level API only when necessary, with comments explaining why)
- Code comments in English; communicate with user in Traditional Chinese
- Use English filenames for STEP files
- Discuss with user before changing any geometry parameters
- Use paper pole names P1-P6 (see Pole Naming section above)

## Prohibitions
- NEVER use absolute paths in scripts
- NEVER overwrite original STEP files in cad/ — output only to fem/

## Compact Instructions
When context is compressed, preserve:
1. Pole naming P1-P6: upper (P2,P4,P5), lower (P6,P3,P1); pairs P1↔P2, P3↔P4, P5↔P6
2. Colinearity + single-center-point verification is mandatory after every geometry change
3. All code must use CadQuery — no other CAD libraries
