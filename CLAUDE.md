# magnetic-tweezer-cad

六極電磁鑷子 CAD 模型整理庫，包含洪組新設計與龍飛 2016 參考設計。

## Architecture
- `hung/` — 洪組新設計（assembly + parts + step_for_fem）
- `long-fei/` — 龍飛 2016 參考設計（step_for_fem + reference）

## Pole Naming & Geometry
- Upper plane: P2 (+90°), P4 (-30°), P5 (-150°)
- Lower plane: P1 (-90°), P3 (+150°), P6 (+30°)
- 3 opposing pairs: P1↔P2, P3↔P4, P5↔P6
- Opposing pairs have ~180° XY angle difference
- OCP traversal → paper mapping: classify by axis_z sign (upper <0, lower >0), then by axis XY angle

## Rules
- Write all code using CadQuery (use OCP low-level API only when necessary, with comments explaining why)
- Code comments in English; communicate with user in Traditional Chinese
- Use English filenames for STEP files
- Discuss with user before changing any geometry parameters
- Use paper pole names P1-P6

## Prohibitions
- NEVER use absolute paths in scripts
- NEVER overwrite original STEP files in parts/ — output only to step_for_fem/

## Compact Instructions
When context is compressed, preserve:
1. Pole naming P1-P6: upper (P2,P4,P5), lower (P6,P3,P1); pairs P1↔P2, P3↔P4, P5↔P6
2. Two designs: hung/ (new) and long-fei/ (reference)
3. All code must use CadQuery
