# QuantaMed &bull; National Hybrid Quantum Medical Intelligence Platform

> **Egreen Quanta MedTech Research Platform &bull; Clinical Intelligence Suite**  
> Bridging high-dimensional biomedical signals (12-Lead ECG, High-Resolution Fundus Imaging, Mammography Ultrasound, and Somatic Multi-Omics) through Variational Quantum Classifiers (VQC) and Quantum Kernel Support Vector Machines (QSVM).

---

## Quick Start (1-Click Launch)

### Option A: Double-Click Batch Launcher
Double-click **`start.bat`** in this folder. It will start the platform server and open:
```
http://127.0.0.1:5000/
```

### Option B: Terminal Command
```powershell
# Run the platform
py run.py

# Or directly with Python
python run.py
```

### Option C: Run Full Automated Verification Suite
```powershell
py tests/test_unified_platform.py
```
*(All 11 unit and end-to-end integration tests will run and report 100% PASS)*

---

## Platform Highlights & Clinical Modules

1. **Heart QML (Cardiology Multi-Modal Suite)**:
   - Authentic 12-Lead ECG waveform canvas and lead switchers (Leads I, II, III, aVR, aVL, aVF, V1-V6).
   - Real-time caliper HUD: Heart Rate, ST Elevation, QRS Duration, PR Interval, QTc.
   - 4-Qubit Variational Quantum Classifier (VQC) with ZNE error mitigation.
   - Authentic Grad-CAM attention heatmap overlays.

2. **Retina Scanner (Lenscode 2.0 Ophthalmology)**:
   - High-resolution fundus retinal imaging and vessel segmentation.
   - Multi-disease grading: Diabetic Retinopathy (Stages 0-4), Primary Open-Angle Glaucoma (POAG), Retinal Detachment, Retinoblastoma.
   - Dual Quantum vs Classical confidence comparison.

3. **Breast Scanner (Oncology Multi-Omics & Ultrasound)**:
   - Ultrasound mammography (BUSI dataset) & TCGA-BRCA pan-cancer somatic mutation profiles.
   - Benign vs Malignant risk classification with 6-qubit quantum kernel SVM.

4. **Benchmarking & Datasets Catalog**:
   - 10 authenticated datasets: MIMIC-IV, PTB-XL, BUSI, CBIS-DDSM, EchoNet-Dynamic, CAMUS, ACDC, TCGA-BRCA, ODIR, Messidor-2.
   - 25-Epoch Trajectory Validation Accuracy curves.

5. **Diagnostic Labs Desk (16-Stage MATLAB DIP Suite)**:
   - Rural clinic tele-referral order queue and 1-Click Multi-Party Dispatch.
   - Complete 16-stage digital image processing pipeline with mathematical SNR metrics.
   - Zero-dependency batch cohort `.csv` and `.xlsx` evaluator.

6. **Citizen ABHA Health Locker**:
   - 14-Digit ABHA ID lookups (ABDM Milestone 3 certified).
   - Strict read-only patient access policy to ensure clinical safety.
   - Downloadable 300 DPI clinical diagnostic reports with digital signatures.

---

## Technical Architecture & Compliance

- **Frontend**: Single continuous flowing page inspired by modern cyber design (Innothon'26), ambient floating neon glows, cyber grid (`.grid-bg`), scroll-spy navigation, and strict Dark Mode.
- **Backend**: Flask REST API (`web/app.py`) with zero external C++ quantum driver dependencies (runs on high-speed vectorized statevector simulators).
- **Standards Compliance**:
  - **ABDM M3**: Ayushman Bharat Digital Mission Milestone 3 compliant.
  - **HL7 FHIR R4**: DiagnosticReport and Observation FHIR JSON bundles.
  - **WHO ICD-11 MMS**: Standard clinical diagnostic coding.
