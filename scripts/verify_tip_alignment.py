"""
Verify colinear alignment of 3 pairs of hexapole pole tips.

Reads Hexapole_Assembly.STEP, finds all conical surfaces matching
the pole tip geometry (semi-angle ~ 11.3 deg), extracts their axes
and apex points, pairs opposing poles, and computes alignment error.
"""

import numpy as np
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.GeomAdaptor import GeomAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cone
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP_PATH = os.path.join(PROJECT_ROOT, "fem", "Hexapole_Assembly_FEM.STEP")

# From Mag_Pole_Bottom.STEP: semi-angle = 0.1974 rad = 11.31 deg
EXPECTED_SEMI_ANGLE_RAD = 0.1974
ANGLE_TOL_RAD = 0.05  # filter tolerance


def load_assembly(path):
    """Load STEP assembly, returning fully instantiated compound shape."""
    reader = STEPControl_Reader()
    status = reader.ReadFile(path)
    if status != 1:
        raise RuntimeError(f"Failed to read STEP: {path} (status={status})")
    reader.TransferRoots()
    return reader.OneShape()


def find_pole_cones(shape):
    """Find conical faces whose semi-angle matches pole tips."""
    cones = []
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
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
                cones.append({
                    "semi_angle_deg": np.degrees(sa),
                    "apex": np.array([apex.X(), apex.Y(), apex.Z()]),
                    "axis": np.array([axis_dir.X(), axis_dir.Y(), axis_dir.Z()]),
                })
        explorer.Next()
    return cones


def pair_opposing_poles(cones):
    """Pair poles whose axes are anti-parallel (opposing in hexapole)."""
    used = set()
    pairs = []
    for i in range(len(cones)):
        if i in used:
            continue
        best_j, best_dot = None, 0
        for j in range(i + 1, len(cones)):
            if j in used:
                continue
            dot = np.dot(cones[i]["axis"], cones[j]["axis"])
            if dot < best_dot:  # most anti-parallel
                best_dot = dot
                best_j = j
        if best_j is not None and best_dot < -0.9:
            pairs.append((i, best_j))
            used.add(i)
            used.add(best_j)
    return pairs


def colinearity_error(a, b):
    """
    Returns (angle_error_deg, perpendicular_distance_mm)
    for two opposing pole axes.
    """
    dot = np.dot(a["axis"], b["axis"])
    angle_err = abs(180.0 - np.degrees(np.arccos(np.clip(dot, -1, 1))))

    d = b["apex"] - a["apex"]
    cross = np.cross(a["axis"], b["axis"])
    cn = np.linalg.norm(cross)

    if cn < 1e-12:  # parallel => point-to-line distance
        t = np.dot(d, a["axis"])
        dist = np.linalg.norm(d - t * a["axis"])
    else:  # skew lines
        dist = abs(np.dot(d, cross)) / cn

    return angle_err, dist


def main():
    print("Loading Hexapole_Assembly.STEP ...")
    shape = load_assembly(STEP_PATH)
    print("Done.\n")

    # --- find all conical surfaces (for debugging) ---
    all_cones = []
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face = TopoDS.Face_s(explorer.Current())
        surf = BRep_Tool.Surface_s(face)
        adaptor = GeomAdaptor_Surface(surf)
        if adaptor.GetType() == GeomAbs_Cone:
            cone = adaptor.Cone()
            apex = cone.Apex()
            all_cones.append({
                "semi_angle_deg": np.degrees(cone.SemiAngle()),
                "apex": (apex.X(), apex.Y(), apex.Z()),
                "radius": cone.RefRadius(),
            })
        explorer.Next()
    print(f"Total conical surfaces in assembly: {len(all_cones)}")
    for i, c in enumerate(all_cones):
        print(f"  cone {i+1}: semi-angle={c['semi_angle_deg']:.2f} deg, "
              f"radius={c['radius']:.2f} mm, "
              f"apex=({c['apex'][0]:.2f}, {c['apex'][1]:.2f}, {c['apex'][2]:.2f})")

    # --- filter pole tip cones ---
    cones = find_pole_cones(shape)
    print(f"\nPole-tip cones (semi-angle ~ 11.3 deg): {len(cones)}\n")

    for i, c in enumerate(cones):
        print(f"  Pole {i+1}:")
        print(f"    Apex  = ({c['apex'][0]:+.4f}, {c['apex'][1]:+.4f}, {c['apex'][2]:+.4f}) mm")
        print(f"    Axis  = ({c['axis'][0]:+.6f}, {c['axis'][1]:+.6f}, {c['axis'][2]:+.6f})")
        print(f"    Semi-angle = {c['semi_angle_deg']:.4f} deg")

    if len(cones) < 2:
        print("\nNot enough pole cones found. Cannot verify alignment.")
        return

    if len(cones) != 6:
        print(f"\nWARNING: expected 6 pole cones, found {len(cones)}")

    # --- pair & verify ---
    pairs = pair_opposing_poles(cones)
    print(f"\nOpposing pairs identified: {len(pairs)}\n")
    print("=" * 60)
    print(" COLINEAR ALIGNMENT VERIFICATION")
    print("=" * 60)

    all_ok = True
    for idx, (i, j) in enumerate(pairs):
        a_err, d_err = colinearity_error(cones[i], cones[j])
        tip_dist = np.linalg.norm(cones[j]["apex"] - cones[i]["apex"])
        ok = a_err < 0.01 and d_err < 0.001
        if not ok:
            all_ok = False

        print(f"\n  Pair {idx+1}: Pole {i+1} <-> Pole {j+1}")
        print(f"    Angle error      : {a_err:.6f} deg")
        print(f"    Axis distance    : {d_err:.6f} mm")
        print(f"    Tip-to-tip dist  : {tip_dist:.3f} mm")
        print(f"    Result           : {'PASS' if ok else '** FAIL **'}")

    print("\n" + "=" * 60)
    if all_ok and len(pairs) == 3:
        print(" ALL 3 PAIRS COLINEARLY ALIGNED")
    elif all_ok:
        print(f" {len(pairs)} PAIR(S) ALIGNED (expected 3)")
    else:
        print(" ALIGNMENT ISSUES DETECTED")
    print("=" * 60)


if __name__ == "__main__":
    main()
