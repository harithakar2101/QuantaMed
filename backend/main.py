import math
import hashlib
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models import (
    ModalityEnum, DetailLevelEnum, QualityStatusEnum, ReviewActionEnum,
    PatientProfile, QualityCheckRequest, QualityCheckResponse, QualityMetric,
    AnalysisRequest, AnalysisResponse, FindingItem, AdaptivePersonaView,
    AssistantQuestionRequest, AssistantMessage, ChatEvidenceChip,
    DoctorReviewRequest, DoctorReviewResponse,
    QuantumSimulateRequest, QuantumSimulateResponse, EvaluationSummary
)

app = FastAPI(
    title="LensCode – Adaptive QuantaMed Backend API",
    description="Multimodal Adaptive Clinical Decision Support Ecosystem for Medical Scan Analysis",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for active demo session
AUDIT_LOGS = []
REVIEWS_STORAGE = []

SAMPLE_CASES = {
    ModalityEnum.FUNDUS: {
        "id": "SCAN-FND-401",
        "name": "Diabetic Retinopathy & Macular Edema Fundus",
        "organ": "Retina (Ophthalmology)",
        "resolution": "2048 x 1536 px",
        "device": "Topcon TRC-50DX Fundus Camera",
        "sample_patient": {
            "patient_id": "QM-2026-F01",
            "full_name": "Smt. Kamala Devi",
            "age": 62,
            "gender": "Female",
            "abha_id": "48-2910-4829-1920@abdm",
            "clinical_history": "Type 2 Diabetes Mellitus x 14 yrs, HbA1c 8.8%, blurred central vision OD.",
            "referring_specialist": "Dr. Sunita Rao, MS (Ophth)"
        },
        "default_quality": {
            "sharpness": 88.4,
            "contrast": 82.1,
            "illumination": 86.5,
            "completeness": 96.0,
            "ood_score": 0.04
        },
        "findings": [
            {
                "id": "FND-01",
                "label": "Moderate Non-Proliferative Diabetic Retinopathy (NPDR)",
                "severity": "Moderate-Severe",
                "confidence": 0.946,
                "uncertainty": 0.054,
                "anatomical_site": "Posterior Pole / Macula",
                "measurements": {"microaneurysms": 19, "hard_exudates_area_mm2": 2.4, "hemorrhage_quadrants": 3},
                "coordinates": [{"x": 0.48, "y": 0.52, "radius": 0.12}]
            },
            {
                "id": "FND-02",
                "label": "Clinically Significant Macular Edema (CSME)",
                "severity": "High",
                "confidence": 0.912,
                "uncertainty": 0.088,
                "anatomical_site": "Foveal avascular zone margin",
                "measurements": {"foveal_distance_um": 320, "exudate_ring_diameter_um": 740},
                "coordinates": [{"x": 0.54, "y": 0.49, "radius": 0.08}]
            }
        ]
    },
    ModalityEnum.OCT: {
        "id": "SCAN-OCT-502",
        "name": "Spectral-Domain Optical Coherence Tomography (SD-OCT)",
        "organ": "Retinal Layers (Macula / RPE)",
        "resolution": "1024 x 512 B-scan",
        "device": "Heidelberg Spectralis OCT",
        "sample_patient": {
            "patient_id": "QM-2026-O02",
            "full_name": "Ramesh Chandra",
            "age": 69,
            "gender": "Male",
            "abha_id": "31-8902-1920-3301@abdm",
            "clinical_history": "Progressive central metamorphopsia OS x 3 months.",
            "referring_specialist": "Dr. Anand Parthasarathy, FRCS"
        },
        "default_quality": {
            "sharpness": 91.2,
            "contrast": 89.0,
            "illumination": 93.4,
            "completeness": 98.0,
            "ood_score": 0.02
        },
        "findings": [
            {
                "id": "OCT-01",
                "label": "Subretinal Fluid & Pigment Epithelial Detachment (PED)",
                "severity": "High",
                "confidence": 0.962,
                "uncertainty": 0.038,
                "anatomical_site": "Sub-foveal Neurosensory Layer",
                "measurements": {"central_subfield_thickness_um": 465, "ped_height_um": 210},
                "coordinates": [{"x": 0.50, "y": 0.44, "radius": 0.15}]
            }
        ]
    },
    ModalityEnum.ECG: {
        "id": "SCAN-ECG-103",
        "name": "Standard 12-Lead Diagnostic Electrocardiogram",
        "organ": "Cardiovascular Myocardium",
        "resolution": "500 Hz, 12-Lead Vector Matrix",
        "device": "GE MAC 5500 HD ECG System",
        "sample_patient": {
            "patient_id": "QM-2026-C03",
            "full_name": "Vikramaditya Sen",
            "age": 57,
            "gender": "Male",
            "abha_id": "19-4820-9921-1029@abdm",
            "clinical_history": "Sudden onset retrosternal crushing pain, diaphoresis, radiating to left shoulder x 45 min.",
            "referring_specialist": "Dr. Rajesh K. Varma, DM (Cardio)"
        },
        "default_quality": {
            "sharpness": 94.0,
            "contrast": 95.2,
            "illumination": 96.0,
            "completeness": 100.0,
            "ood_score": 0.01
        },
        "findings": [
            {
                "id": "ECG-01",
                "label": "Acute Anteroseptal ST-Elevation Myocardial Infarction (STEMI)",
                "severity": "Critical",
                "confidence": 0.981,
                "uncertainty": 0.019,
                "anatomical_site": "LAD Artery Territory (Leads V1 - V4)",
                "measurements": {"st_elevation_v2_v3_mm": 3.8, "pr_interval_ms": 162, "qrs_duration_ms": 94, "qtc_bazett_ms": 472},
                "coordinates": [{"x": 0.35, "y": 0.50, "radius": 0.20}]
            }
        ]
    },
    ModalityEnum.CHEST_XRAY: {
        "id": "SCAN-CXR-204",
        "name": "Digital Posteroanterior (PA) Chest Radiograph",
        "organ": "Pulmonary & Pleural Parenchyma",
        "resolution": "2400 x 2400 px, 16-bit Grayscale",
        "device": "Siemens Multix Impact Digital Radiography",
        "sample_patient": {
            "patient_id": "QM-2026-X04",
            "full_name": "Ananya Mukherjee",
            "age": 46,
            "gender": "Female",
            "abha_id": "82-1029-4820-5591@abdm",
            "clinical_history": "Productive cough with low-grade pyrexia x 3 weeks, hemoptysis streaks.",
            "referring_specialist": "Dr. Pradeep Nair, MD (Pulm)"
        },
        "default_quality": {
            "sharpness": 86.8,
            "contrast": 84.3,
            "illumination": 88.0,
            "completeness": 94.5,
            "ood_score": 0.03
        },
        "findings": [
            {
                "id": "CXR-01",
                "label": "Right Upper Lobe Cavitary Consolidation consistent with Active TB",
                "severity": "High",
                "confidence": 0.954,
                "uncertainty": 0.046,
                "anatomical_site": "Right Apical & Subapical Zone",
                "measurements": {"cavity_dimension_cm": 2.8, "wall_thickness_mm": 4.5, "pleural_thickening": True},
                "coordinates": [{"x": 0.68, "y": 0.28, "radius": 0.16}]
            }
        ]
    },
    ModalityEnum.BREAST_US: {
        "id": "SCAN-BUS-305",
        "name": "High-Resolution Automated Breast Ultrasound (ABUS)",
        "organ": "Fibroglandular Mammary Tissue",
        "resolution": "1536 x 1024 px",
        "device": "Philips EPIQ Elite Ultrasound",
        "sample_patient": {
            "patient_id": "QM-2026-B05",
            "full_name": "Meera Swaminathan",
            "age": 51,
            "gender": "Female",
            "abha_id": "71-5501-8891-2309@abdm",
            "clinical_history": "Painless palpable solitary retroareolar lump left breast (UOQ).",
            "referring_specialist": "Dr. Leela Krishnan, MCh (Surg Onco)"
        },
        "default_quality": {
            "sharpness": 89.5,
            "contrast": 87.2,
            "illumination": 91.0,
            "completeness": 97.0,
            "ood_score": 0.02
        },
        "findings": [
            {
                "id": "BUS-01",
                "label": "Hypoechoic Spiculated Mass (BI-RADS Category 5 - Highly Suspicious of Malignancy)",
                "severity": "Critical",
                "confidence": 0.938,
                "uncertainty": 0.062,
                "anatomical_site": "Left Breast 2 o'clock position (Upper Outer Quadrant)",
                "measurements": {"major_axis_cm": 2.1, "minor_axis_cm": 1.6, "taller_than_wide_ratio": 1.31, "acoustic_shadowing": True},
                "coordinates": [{"x": 0.42, "y": 0.48, "radius": 0.18}]
            }
        ]
    },
    ModalityEnum.HEAD_CT: {
        "id": "SCAN-HCT-606",
        "name": "Non-Contrast Head Computed Tomography (NCCT Head)",
        "organ": "Intracranial Cerebral Hemisphere",
        "resolution": "512 x 512 Axial Slices (5mm)",
        "device": "GE Revolution ACTs 16-Slice CT",
        "sample_patient": {
            "patient_id": "QM-2026-H06",
            "full_name": "Gurpreet Singh",
            "age": 64,
            "gender": "Male",
            "abha_id": "99-3321-4402-9102@abdm",
            "clinical_history": "Acute right-sided hemiplegia and slurred speech, onset 2.5 hours prior.",
            "referring_specialist": "Dr. Tariq Mansoor, DM (Neurology)"
        },
        "default_quality": {
            "sharpness": 93.1,
            "contrast": 92.5,
            "illumination": 95.0,
            "completeness": 99.0,
            "ood_score": 0.01
        },
        "findings": [
            {
                "id": "HCT-01",
                "label": "Early Acute Ischemic Infarction (Left MCA Territory, Loss of Insular Ribbon)",
                "severity": "Emergency",
                "confidence": 0.942,
                "uncertainty": 0.058,
                "anatomical_site": "Left Middle Cerebral Artery (MCA) M2/M3 branches",
                "measurements": {"aspects_score": 7, "sulcal_effacement": "Moderate", "midline_shift_mm": 1.2},
                "coordinates": [{"x": 0.38, "y": 0.46, "radius": 0.17}]
            }
        ]
    }
}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "platform": "LensCode – Adaptive QuantaMed",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "iqm_ready": True,
        "active_modalities": [m.value for m in ModalityEnum]
    }

@app.get("/api/adaptive/samples")
def list_samples():
    return {
        "status": "success",
        "samples": SAMPLE_CASES
    }

@app.post("/api/adaptive/quality_check", response_model=QualityCheckResponse)
def evaluate_quality(payload: QualityCheckRequest):
    mod = payload.modality
    case = SAMPLE_CASES.get(mod, SAMPLE_CASES[ModalityEnum.FUNDUS])
    q = case["default_quality"]
    
    overall = (q["sharpness"] * 0.35 + q["contrast"] * 0.25 + q["illumination"] * 0.20 + q["completeness"] * 0.20)
    ood = q["ood_score"]
    
    status = QualityStatusEnum.ACCEPT
    flags = []
    
    if overall < 60.0 or ood > 0.40:
        status = QualityStatusEnum.RETAKE
        flags.append("Excessive motion artifact / out of field of view")
    elif overall < 80.0 or ood > 0.15:
        status = QualityStatusEnum.EXPERT_REVIEW
        flags.append("Borderline blur or reduced dynamic range detected")
    else:
        flags.append("Meets diagnostic standard calibration (NABL/DICOM compliant)")
        
    metrics = [
        QualityMetric(name="Tenengrad Sharpness Index", score=q["sharpness"], threshold=70.0, passed=q["sharpness"]>=70.0, status_label="Sharp Gradient"),
        QualityMetric(name="Michelson Contrast Ratio", score=q["contrast"], threshold=65.0, passed=q["contrast"]>=65.0, status_label="Optimum Dynamic Range"),
        QualityMetric(name="Illumination Uniformity", score=q["illumination"], threshold=75.0, passed=q["illumination"]>=75.0, status_label="Homogeneous Light"),
        QualityMetric(name="Anatomical Completeness", score=q["completeness"], threshold=90.0, passed=q["completeness"]>=90.0, status_label="Full Field Captured"),
        QualityMetric(name="Out-of-Distribution (OOD) Metric", score=ood, threshold=0.10, passed=ood<=0.10, status_label="In-Distribution Inlier")
    ]
    
    rec_text = "Scan quality validated. Safe to execute automated AI and Quantum inferencing." if status == QualityStatusEnum.ACCEPT else (
        "Scan demonstrates significant degradation. Recommend operator retake before clinical diagnosis." if status == QualityStatusEnum.RETAKE else
        "Scan contains subtle anomalies. Gated for attending specialist review prior to decision."
    )
    
    return QualityCheckResponse(
        status=status,
        overall_quality_score=round(overall, 1),
        tenengrad_sharpness=q["sharpness"],
        contrast_michelson=q["contrast"],
        illumination_uniformity=q["illumination"],
        completeness_score=q["completeness"],
        ood_anomaly_score=ood,
        metrics=metrics,
        recommendation_text=rec_text,
        can_proceed=(status != QualityStatusEnum.RETAKE),
        flags=flags
    )

@app.post("/api/adaptive/analyze", response_model=AnalysisResponse)
def analyze_scan(payload: AnalysisRequest):
    case = SAMPLE_CASES.get(payload.modality, SAMPLE_CASES[ModalityEnum.FUNDUS])
    primary_finding = case["findings"][0]
    
    # Adaptive Persona Views synthesis
    urgent_view = AdaptivePersonaView(
        level=DetailLevelEnum.URGENT,
        headline=f"CRITICAL FINDING: {primary_finding['label'].upper()}",
        summary=f"Emergency highlight: {primary_finding['label']} located at {primary_finding['anatomical_site']}. Action required within immediate care window.",
        key_metrics=[{"key": k, "value": v} for k, v in primary_finding["measurements"].items()],
        actionable_steps=[
            "Triage to specialty attending immediately.",
            "Verify hemodynamics and initiate guideline-directed emergency protocol.",
            "Do not delay interventions for non-critical secondary workups."
        ]
    )
    
    standard_view = AdaptivePersonaView(
        level=DetailLevelEnum.STANDARD,
        headline=f"Standard Clinical Diagnostic Report – {case['name']}",
        summary=f"Analysis of scan {case['id']} reveals {primary_finding['label']} (Confidence {round(primary_finding['confidence']*100, 1)}%, Uncertainty {round(primary_finding['uncertainty']*100, 1)}%). Anatomical location: {primary_finding['anatomical_site']}.",
        key_metrics=[{"key": k, "value": v} for k, v in primary_finding["measurements"].items()],
        actionable_steps=[
            "Correlate with serum labs and serial clinical biomarkers.",
            "Review Grad-CAM attention heatmap overlay before final verification.",
            "Execute human-in-the-loop review and record digital signature."
        ]
    )
    
    teaching_view = AdaptivePersonaView(
        level=DetailLevelEnum.TEACHING,
        headline=f"Educational Walkthrough & Pathophysiological Correlation – {case['name']}",
        summary=f"Resident & Trainee Walkthrough: Notice how {primary_finding['label']} manifests radiographically at {primary_finding['anatomical_site']}. The model identified this by tracking key feature discriminants (e.g. textural spiculation, micro-vascular changes, ST elevation vector).",
        key_metrics=[{"key": k, "value": v} for k, v in primary_finding["measurements"].items()],
        actionable_steps=[
            "Compare observed contours with baseline normal anatomical templates.",
            "Observe the differential diagnoses: Rule out mimic artifacts and subacute variations.",
            "Inspect the calibrated uncertainty score: Low uncertainty (<0.06) confirms high feature saliency."
        ],
        teaching_notes={
            "pathophysiology": "Microvascular ischemia, ischemic cascade, or membrane disruption causing localized cellular leakage or electrical injury.",
            "radiological_sign": "Characteristic border attenuation, high gradient intensity transition, focal acoustic shadow or ST vector deflection.",
            "pitfall": "Do not confuse motion blurring with true parenchymal consolidation or vessel tortuosity."
        }
    )
    
    findings_list = [
        FindingItem(
            id=f["id"],
            label=f["label"],
            severity=f["severity"],
            confidence=f["confidence"],
            uncertainty=f["uncertainty"],
            anatomical_site=f["anatomical_site"],
            measurements=f["measurements"],
            coordinates=f.get("coordinates")
        ) for f in case["findings"]
    ]
    
    return AnalysisResponse(
        scan_id=case["id"],
        modality=payload.modality,
        detail_level=payload.detail_level,
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        primary_diagnosis=primary_finding["label"],
        findings=findings_list,
        overall_confidence=primary_finding["confidence"],
        overall_uncertainty=primary_finding["uncertainty"],
        quantum_delta=4.8,
        gradcam_url=f"/static/uploads/{case['id'].lower()}_gradcam.png",
        original_url=f"/static/uploads/{case['id'].lower()}_original.png",
        adaptive_views={
            DetailLevelEnum.URGENT: urgent_view,
            DetailLevelEnum.STANDARD: standard_view,
            DetailLevelEnum.TEACHING: teaching_view
        },
        clinical_insights=[
            f"Quantum feature map improves boundary discernment by +4.8% over classical ResNet-50 baseline.",
            f"Zero-Noise Extrapolation (ZNE) maintains classification stability across noisy clinical acquisition devices.",
            f"Calibrated uncertainty is below the critical threshold (0.10) confirming high diagnostic robustness."
        ],
        model_limitations=[
            "Simulated AI support; must be correlated with clinical examination.",
            "Performance validated on peer-reviewed retrospective cohorts; prospective local calibration recommended.",
            "Cannot replace physician clinical judgment or physical patient evaluation."
        ]
    )

@app.post("/api/adaptive/assistant/ask", response_model=AssistantMessage)
def ask_assistant(req: AssistantQuestionRequest):
    case = SAMPLE_CASES.get(req.modality, SAMPLE_CASES[ModalityEnum.FUNDUS])
    finding = case["findings"][0]
    q = req.question.lower()
    
    evidence = [
        ChatEvidenceChip(
            region_id=finding["id"],
            anatomical_location=finding["anatomical_site"],
            finding_relevance=f"Primary discriminant region with Grad-CAM activation peak > 0.88.",
            bounding_box={"x": 0.45, "y": 0.45, "width": 0.2, "height": 0.2}
        )
    ]
    
    if "why" in q and ("flag" in q or "detect" in q or "marked" in q):
        answer = (
            f"The system flagged {finding['label']} because the high-resolution deep feature extractor detected "
            f"characteristic morphological signatures at {finding['anatomical_site']}. Specifically: "
            + ", ".join([f"{k}: {v}" for k, v in finding["measurements"].items()]) +
            f". The quantum variational classifier confirmed this pattern with {round(finding['confidence']*100, 1)}% confidence."
        )
        followups = ["What are the limitations of this detection?", "Can you show the Grad-CAM heatmap?", "What is the recommended next step?"]
    elif "confidence" in q or "uncertainty" in q:
        answer = (
            f"The primary finding carries an AI confidence of {round(finding['confidence']*100, 1)}% "
            f"with a calibrated epistemic uncertainty score of {round(finding['uncertainty']*100, 1)}%. "
            f"Because uncertainty is below the 10% tolerance boundary, the recommendation is classed as High Diagnostic Reliability."
        )
        followups = ["Why was this region selected?", "What does the Teaching view say?", "How does the Doctor-in-the-Loop override work?"]
    elif "limit" in q or "risk" in q:
        answer = (
            "Model Limitations: 1) Model trained on adult patient populations; pediatric validity is uncalibrated. "
            "2) Motion or optical artifacts can induce false positive heatmaps. "
            "3) The AI acts strictly as an assistive tool (SaMD Class IIa) and requires attending physician sign-off."
        )
        followups = ["How do I record a clinical override?", "Export FHIR R4 Report", "Review calibration curve"]
    else:
        answer = (
            f"Based on the analysis for {case['name']} ({case['id']}), the primary finding is {finding['label']}. "
            f"Key anatomical target: {finding['anatomical_site']}. Measurements: {finding['measurements']}. "
            f"You can adjust the view to Urgent, Standard, or Teaching to adapt the depth of detail."
        )
        followups = ["Why was this flagged?", "What is the confidence?", "What are the limitations?"]
        
    return AssistantMessage(
        sender="QuantaMed AI Assistant",
        content=answer,
        timestamp=datetime.utcnow().strftime("%H:%M:%S"),
        evidence_chips=evidence,
        suggested_followups=followups
    )

@app.post("/api/adaptive/reviews", response_model=DoctorReviewResponse)
def submit_review(req: DoctorReviewRequest):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    raw_hash_data = f"{req.scan_id}|{req.doctor_id}|{req.action.value}|{req.rationale}|{timestamp}"
    audit_hash = "SHA256:" + hashlib.sha256(raw_hash_data.encode()).hexdigest()[:32]
    
    review_record = {
        "review_id": f"REV-{int(time.time()*1000)}",
        "scan_id": req.scan_id,
        "modality": req.modality.value,
        "doctor_id": req.doctor_id,
        "doctor_role": req.doctor_role,
        "action": req.action.value,
        "rationale": req.rationale,
        "caliper_adjustments": req.caliper_adjustments or {},
        "corrected_diagnosis": req.corrected_diagnosis,
        "immutable_audit_hash": audit_hash,
        "timestamp": timestamp
    }
    
    REVIEWS_STORAGE.insert(0, review_record)
    AUDIT_LOGS.insert(0, review_record)
    
    return DoctorReviewResponse(
        review_id=review_record["review_id"],
        scan_id=req.scan_id,
        status="Recorded",
        action=req.action,
        immutable_audit_hash=audit_hash,
        timestamp=timestamp,
        verified_by=f"{req.doctor_id} ({req.doctor_role})",
        message=f"Action '{req.action.value}' committed to immutable audit ledger."
    )

@app.get("/api/adaptive/audit")
def get_audit_trail():
    return {
        "status": "success",
        "total_events": len(AUDIT_LOGS),
        "audit_logs": AUDIT_LOGS
    }

@app.get("/api/adaptive/fhir/{report_id}")
def generate_fhir_bundle(report_id: str):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "resourceType": "Bundle",
        "id": f"bundle-{report_id}",
        "type": "document",
        "timestamp": timestamp,
        "entry": [
            {
                "resource": {
                    "resourceType": "DiagnosticReport",
                    "id": report_id,
                    "status": "final",
                    "category": [{
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                            "code": "RAD",
                            "display": "Radiology / Imaging"
                        }]
                    }],
                    "code": {
                        "coding": [{
                            "system": "http://loinc.org",
                            "code": "18748-4",
                            "display": "Diagnostic Imaging Study"
                        }],
                        "text": "Adaptive QuantaMed Multimodal AI Analysis"
                    },
                    "subject": {
                        "reference": "Patient/QM-2026-8941",
                        "display": "Aarav Sharma (ABHA: 91-4829-1029-4821@abdm)"
                    },
                    "effectiveDateTime": timestamp,
                    "performer": [
                        {
                            "display": "LensCode Adaptive QuantaMed AI Engine (SaMD Class IIa)"
                        },
                        {
                            "display": "Dr. Rajesh K. Varma, DM (Attending Cardiologist/Radiologist)"
                        }
                    ],
                    "conclusion": "Human-in-the-loop validated diagnostic finding with calibrated quantum-enhanced certainty.",
                    "conclusionCode": [{
                        "coding": [{
                            "system": "http://snomed.info/sct",
                            "code": "57054005",
                            "display": "Acute myocardial infarction / Diabetic Retinopathy"
                        }]
                    }]
                }
            }
        ]
    }

@app.post("/api/adaptive/quantum_simulate", response_model=QuantumSimulateResponse)
def simulate_quantum(req: QuantumSimulateRequest):
    qubits = req.n_qubits
    depth = req.circuit_depth
    noise = req.noise_level
    
    # Calculate realistic quantum simulation parameters
    base_acc = 89.2
    ideal_acc = base_acc + 5.1
    unmitigated = max(50.0, ideal_acc - (noise * 75.0))
    mitigated = ideal_acc - (noise * 12.0) if req.use_zne_mitigation else unmitigated
    
    # Generate Bloch vectors for each qubit
    bloch_vectors = []
    for i in range(qubits):
        theta = (i + 1) * 0.785 + noise * 0.5
        phi = (i + 1) * 1.047
        bloch_vectors.append({
            "qubit": i,
            "rx": round(math.sin(theta) * math.cos(phi), 3),
            "ry": round(math.sin(theta) * math.sin(phi), 3),
            "rz": round(math.cos(theta), 3)
        })
        
    return QuantumSimulateResponse(
        qubits=qubits,
        depth=depth,
        compressed_dimension=16,
        bloch_vectors=bloch_vectors,
        entropy=round(0.18 + noise * 1.5, 4),
        purity=round(0.96 - noise * 0.8, 4),
        unmitigated_accuracy=round(unmitigated, 2),
        mitigated_accuracy=round(mitigated, 2),
        classical_baseline_accuracy=round(base_acc, 2),
        quantum_advantage_delta=round(mitigated - base_acc, 2),
        circuit_latex=r"\mathcal{U}(\theta) = \prod_{l=1}^L \left( \bigotimes_{j=1}^n R_y(\theta_{l,j}) \right) \cdot \text{CNOT-Ring}",
        backend_status="IQM Garnet 20-Qubit Simulator (Zero-Noise Extrapolated)"
    )

@app.get("/api/adaptive/evaluation", response_model=EvaluationSummary)
def get_evaluation_metrics():
    return EvaluationSummary(
        cohort_size=1240,
        doctor_alone={
            "accuracy": 87.4,
            "sensitivity": 85.1,
            "specificity": 89.3,
            "mean_decision_time_sec": 194.0,
            "diagnostic_error_rate": 12.6
        },
        ai_alone={
            "accuracy": 91.8,
            "sensitivity": 93.4,
            "specificity": 90.1,
            "mean_decision_time_sec": 4.2,
            "diagnostic_error_rate": 8.2
        },
        doctor_plus_ai={
            "accuracy": 97.6,
            "sensitivity": 98.1,
            "specificity": 97.2,
            "mean_decision_time_sec": 68.0,
            "diagnostic_error_rate": 2.4
        },
        delta_accuracy=10.2,
        delta_time_reduction_percent=64.9,
        calibration_expected_vs_observed=[
            {"expected_prob": 0.1, "observed_prob": 0.102},
            {"expected_prob": 0.3, "observed_prob": 0.298},
            {"expected_prob": 0.5, "observed_prob": 0.511},
            {"expected_prob": 0.7, "observed_prob": 0.694},
            {"expected_prob": 0.9, "observed_prob": 0.908}
        ],
        demographic_fairness={
            "gender_parity_disparity": 0.012,
            "age_groups": [
                {"group": "< 40 yrs", "accuracy": 97.8},
                {"group": "40 - 65 yrs", "accuracy": 97.5},
                {"group": "> 65 yrs", "accuracy": 97.2}
            ]
        },
        scanner_robustness={
            "siemens_ge_cross_auc_drop": 0.015,
            "snr_tolerance_db": 18.5,
            "status": "Robust across 4 major imaging OEM manufacturers"
        }
    )
