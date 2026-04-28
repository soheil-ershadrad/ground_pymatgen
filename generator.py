from pymatgen.core import Structure
from pymatgen.analysis.magnetism.analyzer import MagneticStructureEnumerator
from pymatgen.io.vasp import Poscar
from pathlib import Path
import shutil

workdir = Path("/work")

poscar_path = workdir / "POSCAR"
incar_path = workdir / "INCAR"
potcar_path = workdir / "POTCAR"
kpoints_path = workdir / "KPOINTS"
job_path = workdir / "job.sh"

# Safety check
if not poscar_path.exists():
    raise FileNotFoundError("POSCAR not found in working directory")

structure = Structure.from_file(poscar_path)

# --- Extract ORIGINAL element order ---
original_order = []
for site in structure:
    el = site.specie.symbol
    if el not in original_order:
        original_order.append(el)

enumerator = MagneticStructureEnumerator(structure)
mag_structures = enumerator.ordered_structures

for i, s in enumerate(mag_structures):
    folder = workdir / f"calc_{i}"
    folder.mkdir(exist_ok=True)

    # --- Extract magnetic moments ---
    magmoms = []
    for site in s:
        spin = getattr(site.specie, "spin", None)
        magmoms.append(float(spin) if spin is not None else 0.0)

    # --- Reorder structure ---
    ordered_species = []
    ordered_coords = []
    ordered_magmoms = []

    for el in original_order:
        for idx, site in enumerate(s):
            if site.specie.symbol == el:
                ordered_species.append(el)
                ordered_coords.append(site.frac_coords)
                ordered_magmoms.append(magmoms[idx])

    s_clean = Structure(
        lattice=s.lattice,
        species=ordered_species,
        coords=ordered_coords,
        coords_are_cartesian=False
    )

    magmoms = ordered_magmoms

    # --- Write POSCAR ---
    Poscar(s_clean).write_file(folder / "POSCAR")

    # --- Write INCAR ---
    with open(incar_path, "r") as f:
        incar_lines = f.readlines()

    with open(folder / "INCAR", "w") as f:
        for line in incar_lines:
            if line.strip().startswith("MAGMOM"):
                f.write(f"MAGMOM = {' '.join(map(str, magmoms))}\n")
            else:
                f.write(line)

    # --- Copy other files (robust way)
    if potcar_path.exists():
        shutil.copy(potcar_path, folder / "POTCAR")

    if kpoints_path.exists():
        shutil.copy(kpoints_path, folder / "KPOINTS")

    if job_path.exists():
        shutil.copy(job_path, folder / "job.sh")
