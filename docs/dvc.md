##  Data Version Control (DVC) Setup

To ensure full reproducibility and auditability of the insurance analytics pipeline, DVC is used to version and track all raw datasets. This aligns with industry expectations in financial and insurance environments where reproducibility is mandatory.

---

### 1. Install DVC

```bash
pip install dvc
```
### Initialize DVC

- Run inside your project root:
```bash
dvc init

```
### Configure Local Remote Storage

- A dedicated directory is used as the DVC remote:
```bash
mkdir "D:/10Acadamy/dvc_storage"
dvc remote add -d localstore "D:/10Acadamy/dvc_storage"
```

### Track Raw Data with DVC
```bash
 dvc add data/raw/MachineLearningRating_v3.txt
 ```
``` bash
   git add data/raw/MachineLearningRating_v3.txt.dvc
   git add .gitignore
   git commit -m "Track raw dataset with DVC"
```

### Push Data to Local Remote
```bash
dvc push

```

### Reproduce Pipeline Stages
``` bash
dvc repro
```

## Outcome


- All raw data is version-controlled.
- Raw files are no longer tracked by Git; only .dvc metadata is.
- Anyone can reproduce the same environment and dataset using dvc pull.
- The project now uses industry-standard versioning used in banking, insurance, and regulated analytics environments.
