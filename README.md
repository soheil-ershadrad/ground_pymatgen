# 🧲 Magnetic Ground State Generator (pymatgen + enumlib)

A containerized workflow to generate symmetry-inequivalent magnetic configurations and prepare VASP-ready input files for identifying magnetic ground states.

This tool leverages pymatgen and enumlib to enumerate magnetic orderings and automatically generate calculation folders for high-throughput studies. 

---

## 🚀 Features

- Automatic enumeration of magnetic configurations  
- Symmetry-aware generation using enumlib  
- Fully containerized (Docker + Apptainer compatible)  
- Designed for HPC workflows  

---

## 📦 Requirements

Place the following files in your working directory:


POSCAR
INCAR
POTCAR
KPOINTS
job.sh


---

## 🧱 Usage

### ▶️ HPC (Apptainer)

Build the container:

```bash
apptainer build ground_pymatgen.sif docker://ghcr.io/soheil-ershadrad/ground_pymatgen:latest

Run:

apptainer run -B $PWD:/work ground_pymatgen.sif

▶️ Local (Docker)
docker run -it -v $(pwd):/work ghcr.io/soheil-ershadrad/ground_pymatgen:latest
📂 Output

The script generates folders:

calc_0/
calc_1/
calc_2/
...

Each folder contains:

POSCAR
INCAR
POTCAR
KPOINTS
job.sh

⚙️ Workflow
Reads structure from POSCAR
Uses pymatgen's MagneticStructureEnumerator to generate magnetic configurations
Reorders atoms to match original element ordering
Updates MAGMOM in INCAR
Writes new calculation folders for each configuration

⚠️ Notes
Ensure MAGMOM exists in your INCAR template
Number of configurations can grow rapidly
Suitable for high-throughput magnetic studies

📚 Dependencies
pymatgen
enumlib (compiled inside container)
