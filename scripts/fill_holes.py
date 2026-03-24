"""
Fill screw holes in STEP files using OpenCascade Defeaturing.
Removes all cylindrical faces (screw holes) from each part,
outputting simplified geometry for ANSYS FEM simulation.

Output: ../fem/parts/<original_name>.STEP
"""

import os
import glob
import cadquery as cq
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.GeomAdaptor import GeomAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Defeaturing

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP_DIR = os.path.join(PROJECT_ROOT, "cad", "parts")
OUT_DIR = os.path.join(PROJECT_ROOT, "fem", "parts")
os.makedirs(OUT_DIR, exist_ok=True)


def get_cylindrical_faces(shape, max_radius=3.0):
    """Return list of cylindrical faces with radius <= max_radius (screw holes only)."""
    faces = []
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face = TopoDS.Face_s(explorer.Current())
        surf = BRep_Tool.Surface_s(face)
        adaptor = GeomAdaptor_Surface(surf)
        if adaptor.GetType() == GeomAbs_Cylinder:
            cyl = adaptor.Cylinder()
            r = cyl.Radius()
            if r <= max_radius:
                faces.append({
                    "face": face,
                    "radius": r,
                    "center": (
                        cyl.Location().X(),
                        cyl.Location().Y(),
                        cyl.Location().Z(),
                    ),
                    "axis": (
                        cyl.Axis().Direction().X(),
                        cyl.Axis().Direction().Y(),
                        cyl.Axis().Direction().Z(),
                    ),
                })
        explorer.Next()
    return faces


def fill_holes(step_path):
    """Remove all cylindrical hole features from a STEP file."""
    name = os.path.basename(step_path)
    result = cq.importers.importStep(step_path)
    shape = result.val().wrapped

    cyl_faces = get_cylindrical_faces(shape)
    if not cyl_faces:
        print(f"  {name}: no cylindrical faces found, copying as-is")
        out_path = os.path.join(OUT_DIR, name)
        cq.exporters.export(result, out_path)
        return True

    print(f"  {name}: found {len(cyl_faces)} cylindrical faces")
    for f in cyl_faces:
        print(f"    r={f['radius']:.2f}mm @ ({f['center'][0]:.1f}, {f['center'][1]:.1f}, {f['center'][2]:.1f})")

    # Iterative defeaturing: try all at once, then fall back to one-by-one
    defeaturer = BRepAlgoAPI_Defeaturing()
    defeaturer.SetShape(shape)
    for f in cyl_faces:
        defeaturer.AddFaceToRemove(f["face"])
    defeaturer.Build()

    if defeaturer.IsDone():
        new_shape = defeaturer.Shape()
        remaining = get_cylindrical_faces(new_shape)

        # Try a second pass if any cylindrical faces remain
        if remaining:
            d2 = BRepAlgoAPI_Defeaturing()
            d2.SetShape(new_shape)
            for f in remaining:
                d2.AddFaceToRemove(f["face"])
            d2.Build()
            if d2.IsDone():
                new_shape = d2.Shape()
                remaining = get_cylindrical_faces(new_shape)

        removed = len(cyl_faces) - len(remaining)
        print(f"    -> removed {removed}/{len(cyl_faces)} cylindrical faces" +
              (f" ({len(remaining)} remaining - likely structural features)" if remaining else ""))

        out_path = os.path.join(OUT_DIR, name)
        cq.exporters.export(cq.Workplane().add(cq.Shape(new_shape)), out_path)
        print(f"    -> saved to filled/{name}")
        return True
    else:
        print(f"    -> FAILED: defeaturing could not complete for {name}")
        return False


def main():
    step_files = sorted(glob.glob(os.path.join(STEP_DIR, "*.STEP")))
    print(f"Processing {len(step_files)} STEP files...\n")

    success = 0
    failed = 0
    for path in step_files:
        try:
            if fill_holes(path):
                success += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  {os.path.basename(path)}: ERROR - {e}")
            failed += 1
        print()

    print(f"Done: {success} succeeded, {failed} failed")
    print(f"Output directory: {OUT_DIR}")


if __name__ == "__main__":
    main()
