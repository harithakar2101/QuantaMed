"""
National & Global Biomedical Datasets Catalog & Connectors
Houses direct references, citation schemas, and live demonstration samples for:
- Cardiology: MIMIC-IV-Ext, MIMIC-IV v3.1, MIMIC-IV-ECG, MIMIC-IV-Echo, CARDIO-ML-ED
- Ophthalmology: Lenscode Level 0-4, MBRSET, Hillel Yaffe Glaucoma, Hillel Yaffe Fundus AMD
- Oncology: TCGA PanCanAtlas, PhysioNet Curated Oncology Reports, PhysioNet Oncology Database
"""

class GlobalDatasetsCatalog:
    """Catalog of real-world clinical and genomic datasets integrated into the platform."""

    DATASETS = {
        "cardiology": [
            {
                "id": "mimic-iv-ext-cardiac",
                "name": "MIMIC-IV-Ext Cardiac Disease (v1.0.0)",
                "source": "PhysioNet / Beth Israel Deaconess Medical Center",
                "url": "https://physionet.org/content/mimic-iv-ext-cardiac-disease/1.0.0/",
                "records": "40,000+ ICU Cardiac Admissions",
                "modalities": "12-Lead ECG, Hemodynamics, Inotropic Support, Cardiac Biomarkers",
                "target_diseases": "Acute Myocardial Infarction, Cardiogenic Shock, Congestive Heart Failure",
                "quantum_utility": "4-qubit amplitude encoding on 12-lead multi-lead vector loops"
            },
            {
                "id": "mimic-iv-clinical",
                "name": "MIMIC-IV Clinical Database (v3.1)",
                "source": "PhysioNet / MIT Laboratory for Computational Physiology",
                "url": "https://physionet.org/content/mimiciv/3.1/",
                "records": "73,181 ICU Patients / 299,712 ED Admissions",
                "modalities": "Lab Events, Vital Signs, Prescriptions, ICD-10/11 Diagnostic Codes",
                "target_diseases": "Systemic Sepsis, Severe Hypertension, Arrhythmic Arrest",
                "quantum_utility": "Multi-variate clinical time-series kernel feature mapping"
            },
            {
                "id": "mimic-iv-ecg",
                "name": "MIMIC-IV-ECG Diagnostic Electrocardiogram Database (v1.0)",
                "source": "PhysioNet / BIDMC",
                "url": "https://physionet.org/content/mimic-iv-ecg/1.0/",
                "records": "800,000+ Diagnostic 12-lead ECGs",
                "modalities": "10-second 500 Hz high-fidelity digital ECG waveforms",
                "target_diseases": "Atrial Fibrillation, ST-Elevation MI, Bundle Branch Blocks, Long QT",
                "quantum_utility": "Wavelet-transformed PQC temporal feature extraction"
            },
            {
                "id": "mimic-iv-echo",
                "name": "MIMIC-IV-Echo Transthoracic Echocardiogram Database (v1.0.1)",
                "source": "PhysioNet / BIDMC",
                "url": "https://physionet.org/content/mimic-iv-echo/1.0.1/",
                "records": "100,000+ Echo Reports & Measurement Series",
                "modalities": "Left Ventricular Ejection Fraction (LVEF), Wall Motion, Valvular Regurgitation",
                "target_diseases": "Aortic Stenosis, Heart Failure with Reduced Ejection Fraction (HFrEF)",
                "quantum_utility": "Hemodynamic stress state tensor decomposition"
            },
            {
                "id": "cardio-ml-ed",
                "name": "CARDIO-ML-ED Multi-Modal Clinical ECG Dataset",
                "source": "Clinical Emergency Department Cohort (Local Bundled)",
                "url": "Local / Clinical Benchmark Suite",
                "records": "1,200 Verified Clinical Cases with Troponin-I & NT-proBNP",
                "modalities": "Biomarkers + 12-Lead ECG + Arterial Pressure",
                "target_diseases": "Coronary Artery Disease, Ischemic Heart Disease",
                "quantum_utility": "Active training set for 7-Layer Quantum Cardio Decision Engine"
            },
            {
                "id": "echonet-dynamic",
                "name": "EchoNet-Dynamic Cardiac Ultrasound Video & Image Dataset",
                "source": "Stanford Medicine / Nature (2020)",
                "url": "https://echonet.github.io/dynamic/",
                "records": "10,030 Apical-4-Chamber Echocardiogram Image & Video Series",
                "modalities": "2D B-Mode Ultrasound, LV Endocardial Tracings, LVEF, End-Diastolic & End-Systolic Volumes",
                "target_diseases": "Heart Failure with Reduced Ejection Fraction (HFrEF), Cardiomyopathy, LV Dysfunction",
                "quantum_utility": "Quantum Convolutional Neural Network (QCNN) & VQC feature encoding for cardiac wall motion"
            },
            {
                "id": "camus-echo",
                "name": "CAMUS: Cardiac Acquisitions for Multi-structure Ultrasound Segmentation",
                "source": "CREATIS / University of Lyon / MICCAI",
                "url": "https://www.creatis.insa-lyon.fr/Challenge/camus/",
                "records": "500 Clinical 2-Chamber & 4-Chamber Echo Image Frames",
                "modalities": "2D B-Mode Echocardiography with Endocardium, Epicardium, and Left Atrium Masks",
                "target_diseases": "Myocardial Infarction, Left Atrial Enlargement, Ischemic Heart Failure",
                "quantum_utility": "Quantum variational segmentation & amplitude-encoded myocardial boundary tracing"
            },
            {
                "id": "acdc-cardiac-mri",
                "name": "ACDC: Automated Cardiac Diagnosis Challenge (Cine-MRI Images)",
                "source": "MICCAI / University Hospital of Dijon",
                "url": "https://www.creatis.insa-lyon.fr/Challenge/acdc/",
                "records": "150 Cine-MRI Sequences (Normal, MI, DCM, HCM, RV Abnormal)",
                "modalities": "Short-Axis Cine-MRI Image Slices from Base to Apex",
                "target_diseases": "Myocardial Infarction, Dilated Cardiomyopathy, Hypertrophic Cardiomyopathy",
                "quantum_utility": "Quantum Support Vector Machine (QSVM) kernel classification of myocardial strain tensor"
            },
            {
                "id": "ptb-xl-ecg-images",
                "name": "PTB-XL 12-Lead Paper ECG Scans & Waveform Images",
                "source": "PhysioNet / Physikalisch-Technische Bundesanstalt",
                "url": "https://physionet.org/content/ptb-xl/1.0.3/",
                "records": "21,799 12-Lead Clinical ECG Image Scans & Scalograms",
                "modalities": "300 DPI 12-Lead Millimeter Grid Paper Scans & 2D CWT Scalograms",
                "target_diseases": "STEMI, NSTEMI, Bundle Branch Blocks, Atrial Fibrillation, Ventricular Hypertrophy",
                "quantum_utility": "Continuous Wavelet Transform (CWT) into 2D time-frequency scalograms for Quantum ViT"
            }
        ],
        "ophthalmology": [
            {
                "id": "lenscode-dr-dataset",
                "name": "Lenscode Oculis 5-Level Retinal Dataset (Level 0 - Level 4)",
                "source": "TEAM LENSCODE / Local Verified Clinical Screening Archive",
                "url": "Local Repository (6,739 High-Resolution Fundus Images)",
                "records": "6,739 Fundus Images across ICDR Levels 0 to 4",
                "modalities": "45°/50° Color Digital Fundus Photographs (Topcon / Zeiss / Forus)",
                "target_diseases": "No DR (L0), Mild NPDR (L1), Moderate NPDR (L2), Severe NPDR (L3), Proliferative DR (L4)",
                "quantum_utility": "MATLAB 16-stage DIP feature extraction & Quantum Kernel representation"
            },
            {
                "id": "mbrset-retinal",
                "name": "MBRSET: Multi-Ethnic Breast & Retinal Screening Dataset (v1.0)",
                "source": "PhysioNet Multi-Center Consortium",
                "url": "https://physionet.org/content/mbrset/1.0/",
                "records": "12,500 Multi-Ethnic Paired Fundus & Metabolic Records",
                "modalities": "Fundus Photography + Glycemic & Microvascular Biomarkers",
                "target_diseases": "Microvascular Retinal Caliber Attenuation, Diabetic Microangiopathy",
                "quantum_utility": "Cross-population demographic invariance via quantum kernel mapping"
            },
            {
                "id": "hillel-yaffe-glaucoma",
                "name": "Hillel Yaffe Glaucoma Dataset (v1.1.0)",
                "source": "PhysioNet / Hillel Yaffe Medical Center Ophthalmology Dept.",
                "url": "https://physionet.org/content/hillel-yaffe-glaucoma-dataset/1.1.0/",
                "records": "840 Annotated Optic Disc Images with Confirmatory OCT & Visual Fields",
                "modalities": "Fundus ONH + Active Contour Segmentations + Humphrey 24-2 Grids",
                "target_diseases": "Primary Open-Angle Glaucoma (POAG), Angle-Closure Glaucoma (PACG)",
                "quantum_utility": "vCDR Caliper & ISNT compliance boundary classification"
            },
            {
                "id": "hillel-yaffe-amd",
                "name": "Hillel Yaffe Fundus AMD Dataset (v1.0.0)",
                "source": "PhysioNet / Hillel Yaffe Medical Center",
                "url": "https://physionet.org/content/hillel-yaffe-fundus-amd/1.0.0/",
                "records": "1,120 Macular Images with AREDS Staging",
                "modalities": "High-Definition Macular Fundus Photography",
                "target_diseases": "Dry AMD (Drusen), Wet Neovascular AMD (Geographic Atrophy)",
                "quantum_utility": "Parafoveal drusen spatial cluster quantum entanglement modeling"
            }
        ],
        "oncology": [
            {
                "id": "busi-breast-ultrasound",
                "name": "BUSI: Breast Ultrasound Images Dataset",
                "source": "Faculty of Computers and AI, Cairo University / Mendeley & Kaggle",
                "url": "https://www.kaggle.com/datasets/aryashah2k/breast-ultrasound-images-dataset",
                "records": "780 High-Resolution Ultrasound Images (Malignant, Benign, Normal)",
                "modalities": "B-Mode Breast Ultrasound Images with Ground-Truth Tumor Boundary Masks",
                "target_diseases": "Invasive Ductal Carcinoma, Fibroadenoma, Breast Parenchyma Screening",
                "quantum_utility": "6-Qubit VQC with parameter-shift optimization for malignant margin classification"
            },
            {
                "id": "cbis-ddsm-mammography",
                "name": "CBIS-DDSM: Curated Breast Imaging Subset of Digital Mammograms",
                "source": "The Cancer Imaging Archive (TCIA) / National Cancer Institute",
                "url": "https://www.cancerimagingarchive.net/collection/cbis-ddsm/",
                "records": "2,620 Mammographic Scans with Mass & Calcification Cases",
                "modalities": "Digital Mammography Scans (Craniocaudal & Mediolateral Oblique Views)",
                "target_diseases": "Malignant Calcifications, Invasive Lobular Carcinoma, Benign Fibrocystic Changes",
                "quantum_utility": "Quantum Convolutional Neural Network (QCNN) for microcalcification cluster detection"
            },
            {
                "id": "breakhis-histology",
                "name": "BreakHis: Breast Cancer Histopathological Biopsy Images",
                "source": "Federal University of Paraná (UFPR) / Kaggle",
                "url": "https://www.kaggle.com/datasets/ambarish/breakhis",
                "records": "7,909 Microscopic Biopsy Images (40X, 100X, 200X, 400X)",
                "modalities": "H&E Stained Histopathological Microscopic Biopsy Images",
                "target_diseases": "Ductal Carcinoma, Lobular Carcinoma, Mucinous Carcinoma, Tubular Adenoma",
                "quantum_utility": "Havlíček ZZ-Feature Map capturing cell nuclear pleomorphism in Hilbert space"
            },
            {
                "id": "tcia-tcga-brca",
                "name": "TCIA-TCGA-BRCA Multi-Modal Cancer Imaging Collection",
                "source": "The Cancer Imaging Archive (TCIA) / NIH NCI",
                "url": "https://www.cancerimagingarchive.net/collection/tcga-brca/",
                "records": "1,000+ Multi-Modal Patient Imaging Studies with Matched Genomic Data",
                "modalities": "Digital Mammography, Breast MRI, CT Scans, Whole Slide Histopathology (WSI)",
                "target_diseases": "Triple-Negative Breast Cancer, HER2-Enriched, Luminal A/B Carcinomas",
                "quantum_utility": "Radiogenomic Quantum Multi-Kernel Learning (QMKL) fusing images with somatic DNA mutations"
            },
            {
                "id": "tcga-genomic",
                "name": "The Cancer Genome Atlas (TCGA / PanCanAtlas)",
                "source": "National Cancer Institute (NCI) / NIH",
                "url": "https://www.cancer.gov/ccg/research/genome-sequencing/tcga",
                "records": "20,000+ Primary Cancers across 33 Cancer Types",
                "modalities": "Whole-Exome Sequencing (WES), RNA-Seq, Somatic Mutations (TP53, BRCA, KRAS, EGFR)",
                "target_diseases": "Breast (BRCA), Lung (LUAD), Colorectal (COAD), Prostate (PRAD)",
                "quantum_utility": "Quantum Hilbert space classification of high-dimensional multi-gene expression"
            },
            {
                "id": "curated-oncology-reports",
                "name": "Curated Oncology EHR Reports (v1.0)",
                "source": "PhysioNet / Cancer Surveillance Research Group",
                "url": "https://physionet.org/content/curated-oncology-reports/1.0/",
                "records": "8,400 De-identified Pathology & Diagnostic Oncology Records",
                "modalities": "Histology Text, TNM Stage Staging, Immunohistochemistry (ER/PR/HER2)",
                "target_diseases": "Solid Tumors, Lymphoma, Metastatic Staging",
                "quantum_utility": "Hybrid NLP biomarker entity extraction & risk stratification"
            },
            {
                "id": "physionet-oncology",
                "name": "PhysioNet Cancer & Oncology Resource Collection",
                "source": "PhysioNet Topic Hub",
                "url": "https://physionet.org/content/?topic=oncology",
                "records": "Cross-Modality Oncology Imaging & Clinical Biomarker Repositories",
                "modalities": "PET/CT, Radiogenomics, Circulating Tumor DNA (ctDNA) Markers",
                "target_diseases": "Pan-Cancer Early Screening (MCED)",
                "quantum_utility": "Quantum Support Vector Machine (QSVM) kernel decision boundaries"
            }
        ],
        "hiv_aids": [
            {
                "id": "actg-175-hiv",
                "name": "ACTG 175: Longitudinal Immune Progression Cohort",
                "source": "AIDS Clinical Trials Group (ACTG) / NIH NIAID",
                "url": "https://clinicaltrials.gov/study/NCT00000624",
                "records": "2,139 Clinical Trial Participants with Longitudinal CD4/CD8 Tracking",
                "modalities": "Flow Cytometry CD4/CD8 Counts, Viral Load, Antiretroviral Regimens",
                "target_diseases": "Advanced HIV Disease (AHD), Opportunistic Infections, Virological Rebound",
                "quantum_utility": "4-Qubit VQC with Havlíček ZZ-Feature Map on CD4 trajectory latent dynamics"
            },
            {
                "id": "stanford-hivdb",
                "name": "Stanford HIV Drug Resistance Database (HIVdb)",
                "source": "Stanford University School of Medicine",
                "url": "https://hivdb.stanford.edu/",
                "records": "150,000+ Genotyped HIV-1 Pol Sequences & Phenotypic Susceptibility",
                "modalities": "Viral Genome Sequences, Reverse Transcriptase & Protease Mutation Profiles",
                "target_diseases": "Nucleoside / Non-Nucleoside Reverse Transcriptase Inhibitor Resistance",
                "quantum_utility": "Quantum Kernel Support Vector Machine (QSVM) for multi-drug mutation classification"
            }
        ],
        "tuberculosis": [
            {
                "id": "montgomery-tb-cxr",
                "name": "Montgomery County & Shenzhen TB Chest X-ray Sets",
                "source": "National Library of Medicine (NLM) / NIH & Shenzhen No. 3 People's Hospital",
                "url": "https://lhncbc.nlm.nih.gov/LHC-downloads/downloads.html#tuberculosis-chest-x-ray-computer-aided-diagnosis",
                "records": "800 High-Resolution Digital Chest X-Rays with Radiologist Consensus",
                "modalities": "Posterior-Anterior (PA) Chest Radiographs with Clinical Manifestations",
                "target_diseases": "Active Pulmonary Cavitary TB, Infiltrates, Miliary Pattern, Effusion",
                "quantum_utility": "6-Qubit Quantum Kernel Machine for lung apical cavitary lesion separation"
            },
            {
                "id": "who-rapid-tb-cohort",
                "name": "WHO Multicenter TB Diagnostic & Sputum AFB Repository",
                "source": "World Health Organization (WHO) Global TB Programme",
                "url": "https://www.who.int/teams/global-tuberculosis-programme",
                "records": "4,500 Multi-Site Patients with Paired GeneXpert MTB/RIF & Sputum Smears",
                "modalities": "Sputum AFB Smear Microscopic Grades (0-3+), GeneXpert Ct Values, CRP Levels",
                "target_diseases": "Multidrug-Resistant Tuberculosis (MDR-TB), Rifampicin-Resistant TB",
                "quantum_utility": "Cross-attention multimodal fusion combining radiograph embeddings with bacterial density"
            }
        ]
    }

    @staticmethod
    def get_catalog():
        """Returns the full catalog of datasets."""
        return GlobalDatasetsCatalog.DATASETS
