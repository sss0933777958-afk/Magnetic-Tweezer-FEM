"""
Adjust upper-plane pole tips (P2, P4, P5) along Z so that all 3
opposing pairs have a tip-to-tip distance of exactly 1.0 mm.

Reads Hexapole_Assembly.STEP, identifies the 3 upper-plane Mag_Pole_Bottom
solids by their conical tip surfaces, translates each along Z, and writes
the adjusted assembly to filled/Hexapole_Assembly_adjusted.STEP.

Pole mapping (corrected, verified against user SolidWorks measurements):
  Upper plane (axis_z < 0): P2 (~-150°), P4 (~+90°), P5 (~-30°)
  Lower plane (axis_z > 0): P1 (~-90°),  P3 (~+150°), P6 (~+30°)
  Pairs: P1<->P2, P3<->P4, P5<->P6
"""

import os
import math
import numpy as np

# OCP low-level imports (needed for solid decomposition, face analysis, and transforms)
from OCP.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.GeomAdaptor import GeomAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cone
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.gp import gp_Trsf, gp_Vec
from OCP.TopoDS import TopoDS_Compound
from OCP.BRep import BRep_Builder

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEM_DIR = os.path.join(PROJECT_ROOT, "fem")
INPUT_PATH = os.path.join(FEM_DIR, "Hexapole_Assembly_filled.STEP")  # Holes removed, original alignment
OUTPUT_PATH = os.path.join(FEM_DIR, "Hexapole_Assembly_FEM.STEP")  # Final FEM-ready output

# Pole tip cone geometry
EXPECTED_SEMI_ANGLE_RAD = 0.1974  # ~11.31 deg
ANGLE_TOL_RAD = 0.05

TARGET_DIST = 1.0  # mm


def load_step(path):
    """Load a STEP file and return the top-level shape."""
    reader = STEPControl_Reader()
    status = reader.ReadFile(path)
    if status != 1:
        raise RuntimeError(f"Failed to read STEP: {path} (status={status})")
    reader.TransferRoots()
    return reader.OneShape()


def get_solids(shape):
    """Decompose a shape into individual solids."""
    solids = []
    explorer = TopExp_Explorer(shape, TopAbs_SOLID)
    while explorer.More():
        solids.append(TopoDS.Solid_s(explorer.Current()))
        explorer.Next()
    return solids


def find_pole_cone_in_solid(solid):
    """
    Check if a solid contains a pole-tip cone (semi-angle ~11.3 deg).
    Returns cone info dict if found, None otherwise.
    """
    explorer = TopExp_Explorer(solid, TopAbs_FACE)
    while explorer.More():
        face = TopoDS.Face_s(explorer.Current())
        surf = BRep_Tool.Surface_s(face)
        adaptor = GeomAdaptor_Surface(surf)
        if adaptor.GetType() == GeomAbs_Cone:
            cone = adaptor.Cone()
            sa = cone.SemiAngle()
            if abs(sa - EXPECTED_SEMI_ANGLE_RAD) < ANGLE_TOL_RAD:
                apex = cone.Apex()
                axis_dir = cone.Axis().Direction()
                return {
                    "apex": np.array([apex.X(), apex.Y(), apex.Z()]),
                    "axis": np.array([axis_dir.X(), axis_dir.Y(), axis_dir.Z()]),
                    "semi_angle_deg": np.degrees(sa),
                }
        explorer.Next()
    return None


def identify_paper_name(cone_info):
    """
    Map a cone to paper pole name (P1-P6) using axis direction.
    Upper plane (axis_z < 0): P2 (~-150°), P4 (~+90°), P5 (~-30°)
    Lower plane (axis_z > 0): P1 (~-90°), P3 (~+150°), P6 (~+30°)
    """
    ax = cone_info["axis"]
    xy_angle = np.degrees(np.arctan2(ax[1], ax[0]))

    # Corrected mapping (verified against user SolidWorks measurements):
    # Opposing pairs must have ~180° XY angle difference
    if ax[2] < 0:  # upper plane
        targets = [("P2", 90), ("P4", -30), ("P5", -150)]
    else:  # lower plane
        targets = [("P1", -90), ("P3", 150), ("P6", 30)]

    best_name, best_diff = None, 999
    for name, target_ang in targets:
        diff = abs(xy_angle - target_ang)
        if diff > 180:
            diff = 360 - diff
        if diff < best_diff:
            best_diff = diff
            best_name = name
    return best_name


def compute_z_shift(lower_apex, upper_apex, target_dist):
    """
    Compute Z shift for the upper pole to achieve target tip-to-tip distance.
    Keeps XY distance unchanged, adjusts only Z.
    """
    d = upper_apex - lower_apex
    dxy = math.sqrt(d[0] ** 2 + d[1] ** 2)

    if dxy >= target_dist:
        raise ValueError(
            f"XY distance ({dxy:.4f} mm) >= target ({target_dist} mm), "
            f"cannot achieve target by Z adjustment alone"
        )

    dz_current = d[2]
    dz_new = math.copysign(math.sqrt(target_dist**2 - dxy**2), dz_current)
    return dz_new - dz_current


def translate_solid_z(solid, dz):
    """Apply Z-axis translation to a solid, returning the transformed solid."""
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(0, 0, dz))
    transformer = BRepBuilderAPI_Transform(solid, trsf, True)  # True = copy
    transformer.Build()
    return transformer.Shape()


def save_step(shape, path):
    """Write a shape to a STEP file."""
    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_AsIs)
    status = writer.Write(path)
    if status != 1:
        raise RuntimeError(f"Failed to write STEP: {path} (status={status})")


def main():
    print(f"Loading {os.path.basename(INPUT_PATH)} ...")
    assembly = load_step(INPUT_PATH)
    solids = get_solids(assembly)
    print(f"Found {len(solids)} solids in assembly\n")

    # --- Identify pole-tip solids ---
    pole_solids = {}  # paper_name -> (solid_index, cone_info)
    for i, solid in enumerate(solids):
        cone = find_pole_cone_in_solid(solid)
        if cone is not None:
            name = identify_paper_name(cone)
            pole_solids[name] = (i, cone)
            plane = "upper" if cone["axis"][2] < 0 else "lower"
            print(f"  Solid {i}: {name} ({plane}), "
                  f"apex=({cone['apex'][0]:+.4f}, {cone['apex'][1]:+.4f}, {cone['apex'][2]:+.4f})")

    print(f"\nIdentified {len(pole_solids)} pole-tip solids\n")

    # --- Compute Z shifts for upper poles ---
    # Pairs as (lower_plane_pole, upper_plane_pole)
    pairs = [("P1", "P2"), ("P3", "P4"), ("P6", "P5")]
    upper_poles = ["P2", "P4", "P5"]
    shifts = {}  # paper_name -> dz

    print("=== Required Z adjustments ===")
    for p_lower, p_upper in pairs:
        if p_lower not in pole_solids or p_upper not in pole_solids:
            print(f"  WARNING: {p_lower} or {p_upper} not found!")
            continue

        lower_apex = pole_solids[p_lower][1]["apex"]
        upper_apex = pole_solids[p_upper][1]["apex"]
        current_dist = np.linalg.norm(upper_apex - lower_apex)

        dz = compute_z_shift(lower_apex, upper_apex, TARGET_DIST)
        shifts[p_upper] = dz

        print(f"  {p_lower}<->{p_upper}: current={current_dist:.4f} mm, "
              f"shift {p_upper} Z by {dz:+.4f} mm -> target {TARGET_DIST:.1f} mm")

    # --- Apply transforms ---
    print("\n=== Applying Z translations ===")
    new_solids = list(solids)  # shallow copy
    for name in upper_poles:
        if name not in shifts:
            continue
        idx = pole_solids[name][0]
        dz = shifts[name]
        new_solids[idx] = translate_solid_z(solids[idx], dz)
        print(f"  {name} (solid {idx}): Z {dz:+.4f} mm")

    # --- Reassemble compound ---
    builder = BRep_Builder()
    compound = TopoDS_Compound()
    builder.MakeCompound(compound)
    for s in new_solids:
        builder.Add(compound, s)

    # --- Verify distances (use paper pair names for display) ---
    print("\n=== Verification ===")
    all_ok = True
    verify_pairs = [("P1", "P2"), ("P3", "P4"), ("P6", "P5")]
    for p_lower, p_upper in verify_pairs:
        # Re-read cone positions from modified solids
        cone_lower = find_pole_cone_in_solid(new_solids[pole_solids[p_lower][0]])
        cone_upper = find_pole_cone_in_solid(new_solids[pole_solids[p_upper][0]])

        if cone_lower is None or cone_upper is None:
            print(f"  {p_lower}<->{p_upper}: ERROR - cone not found after transform!")
            all_ok = False
            continue

        new_dist = np.linalg.norm(cone_upper["apex"] - cone_lower["apex"])
        ok = abs(new_dist - TARGET_DIST) < 0.001
        if not ok:
            all_ok = False
        print(f"  {p_lower}<->{p_upper}: {new_dist:.4f} mm {'PASS' if ok else '** FAIL **'}")

    if not all_ok:
        print("\nWARNING: Some pairs did not meet target distance!")
        return

    # --- Save ---
    os.makedirs(FEM_DIR, exist_ok=True)
    print(f"\nSaving to {os.path.basename(OUTPUT_PATH)} ...")
    save_step(compound, OUTPUT_PATH)
    print("Done.")


if __name__ == "__main__":
    main()
