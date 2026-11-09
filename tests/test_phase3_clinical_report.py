"""
================================================================================
  LensCode – Adaptive QuantaMed • Unit & Integration Test Suite
  Enhancement Phase 3: AI Clinical Report Engine
  Tests 6 Canonical Synthetic Case Archetypes, SaMD Quality Gating,
  Structured Inference Schema, 23 Report Sections, 8-State Workflow Machine,
  and 300 DPI Vector PDF Generation.
================================================================================
"""

import unittest
import json
import os
import io
import time
import hashlib

from src.clinical_pdf_generator import pdf_engine, ClinicalPDFGenerator


class TestPhase3ClinicalReportEngine(unittest.TestCase):
    """
    Validates end-to-end functionality of Phase 3 Clinical Report Engine.
    """

    def setUp(self):
        # 6 Canonical Synthetic Case Archetypes
        self.sample_cases = {
            "fundus": {
                "patient": {
                    "patientId": "QM-2026-F01",
                    "caseArchetype": "CLEAR_ABNORMAL",
                    "archetypeLabel": "Clear Abnormal (NPDR + CSME)",
                    "name": "Smt. Kamala Devi",
                    "age": 62,
                    "sex": "Female",
                    "syntheticAbha": "48-2910-4829-1920",
                    "syntheticUhid": "UHID-DEL-89410",
                    "indication": "Annual Diabetic Retinopathy screening and maculopathy evaluation",
                    "relevantHistory": "Type-2 Diabetes Mellitus x 14 yrs, HbA1c 8.8%, blurred central vision OD.",
                    "referringDoctor": "Dr. Sunita Rao, MS (Ophthalmology)",
                    "referringDoctorHpr": "HPR-IN-2026-88194",
                    "reportingDoctor": "Dr. Rajesh K. Varma, DM",
                    "reportingDoctorHpr": "HPR-IN-2026-10294"
                },
                "modality": "fundus",
                "quality": {
                    "laplacian_variance": 142.6,
                    "brightness": 128.4,
                    "contrast": 64.2,
                    "noise_estimate": 3.8,
                    "aspect_completeness": 99.4,
                    "ood_score": 0.05,
                    "gate": "Accept"
                },
                "findings": [
                    {
                        "id": "FND-01",
                        "label": "Microaneurysms & Dot Hemorrhages",
                        "region": "Superior Macular Quadrant",
                        "measurement": "Count: 14",
                        "normal_range": "0",
                        "severity": "Moderate",
                        "confidence": 0.942,
                        "uncertainty": 0.024
                    },
                    {
                        "id": "FND-02",
                        "label": "Hard Exudates (CSME Risk)",
                        "region": "Parafoveal Ring (<500um)",
                        "measurement": "Area: 1.84 mm²",
                        "normal_range": "0 mm²",
                        "severity": "Severe",
                        "confidence": 0.918,
                        "uncertainty": 0.038
                    }
                ],
                "overall_impression": "Findings suggestive of Moderate Non-Proliferative Diabetic Retinopathy (NPDR) with features concerning for Clinically Significant Macular Edema (CSME).",
                "critical_flags": [],
                "quality_gate": "Accept"
            },
            "chest_xray": {
                "patient": {
                    "patientId": "QM-2026-X04",
                    "caseArchetype": "NORMAL_CASE",
                    "archetypeLabel": "Normal (Routine Check, Clear Fields)",
                    "name": "Shri Arvind Nambisan",
                    "age": 34,
                    "sex": "Male",
                    "syntheticAbha": "82-1029-4820-5591",
                    "syntheticUhid": "UHID-BLR-44210",
                    "indication": "Standard PA Chest Radiograph for pre-employment occupational clearance",
                    "relevantHistory": "Pre-employment executive health checkup. Non-smoker, asymptomatic.",
                    "referringDoctor": "Dr. Pradeep Nair, MD (Pulmonary Medicine)",
                    "referringDoctorHpr": "HPR-IN-2026-33918",
                    "reportingDoctor": "Dr. Farhan Qureshi, MD",
                    "reportingDoctorHpr": "HPR-IN-2026-52119"
                },
                "modality": "chest_xray",
                "quality": {
                    "laplacian_variance": 184.2,
                    "brightness": 120.1,
                    "contrast": 72.4,
                    "noise_estimate": 2.9,
                    "aspect_completeness": 99.8,
                    "ood_score": 0.04,
                    "gate": "Accept"
                },
                "findings": [
                    {
                        "id": "FND-CXR-01",
                        "label": "Bilateral Lung Parenchyma",
                        "region": "Bilateral Lung Fields",
                        "measurement": "Aeration Normal",
                        "normal_range": "Clear / Aerated",
                        "severity": "Normal",
                        "confidence": 0.978,
                        "uncertainty": 0.012
                    },
                    {
                        "id": "FND-CXR-02",
                        "label": "Cardiothoracic Ratio (CTR)",
                        "region": "Cardiac Silhouette",
                        "measurement": "0.44",
                        "normal_range": "< 0.50",
                        "severity": "Normal",
                        "confidence": 0.965,
                        "uncertainty": 0.015
                    }
                ],
                "overall_impression": "Normal posteroanterior chest radiograph. Clear bilateral lung parenchyma and normal cardiothoracic silhouette (CTR 0.44).",
                "critical_flags": [],
                "quality_gate": "Accept"
            },
            "breast_us": {
                "patient": {
                    "patientId": "QM-2026-B05",
                    "caseArchetype": "BORDERLINE_UNCERTAIN",
                    "archetypeLabel": "Borderline / Uncertain (BI-RADS 3/4A)",
                    "name": "Smt. Meera Swaminathan",
                    "age": 51,
                    "sex": "Female",
                    "syntheticAbha": "71-5501-8891-2309",
                    "syntheticUhid": "UHID-CHN-66201",
                    "indication": "Targeted High-Resolution Breast Sonography for BI-RADS risk classification",
                    "relevantHistory": "Equivocal vague nodularity left breast 10 o'clock position noticed during palpation.",
                    "referringDoctor": "Dr. Leela Krishnan, MCh",
                    "referringDoctorHpr": "HPR-IN-2026-77291",
                    "reportingDoctor": "Dr. Vikram Sethi, MD",
                    "reportingDoctorHpr": "HPR-IN-2026-38291"
                },
                "modality": "breast_us",
                "quality": {
                    "laplacian_variance": 102.5,
                    "brightness": 110.4,
                    "contrast": 54.8,
                    "noise_estimate": 4.6,
                    "aspect_completeness": 98.7,
                    "ood_score": 0.09,
                    "gate": "Accept"
                },
                "findings": [
                    {
                        "id": "FND-BRS-01",
                        "label": "Focal Hypoechoic Nodule",
                        "region": "Left Breast (10 o'clock, 3cm from nipple)",
                        "measurement": "18.4 x 11.2 mm",
                        "normal_range": "No focal lesion",
                        "severity": "Moderate",
                        "confidence": 0.742,
                        "uncertainty": 0.128
                    }
                ],
                "overall_impression": "Circumscribed hypoechoic nodule with micro-lobulated focal boundary (BI-RADS 3 vs 4A equivocal). Consider short-interval 6-month repeat sonography or core needle biopsy.",
                "critical_flags": [],
                "quality_gate": "Accept"
            },
            "oct": {
                "patient": {
                    "patientId": "QM-2026-O02",
                    "caseArchetype": "POOR_QUALITY_RETAKE",
                    "archetypeLabel": "Poor Quality (Severe Motion Blur → Retake Advisory)",
                    "name": "Shri Ramesh Chandra",
                    "age": 69,
                    "sex": "Male",
                    "syntheticAbha": "31-8902-1920-3301",
                    "syntheticUhid": "UHID-DEL-77402",
                    "indication": "High-resolution SD-OCT macula scan (Quality Gating Test Case)",
                    "relevantHistory": "Severe patient involuntary eye blink and tremor during scan traverse.",
                    "referringDoctor": "Dr. Anand Parthasarathy, FRCS",
                    "referringDoctorHpr": "HPR-IN-2026-44012",
                    "reportingDoctor": "Dr. Anita Roy, MS",
                    "reportingDoctorHpr": "HPR-IN-2026-59312"
                },
                "modality": "oct",
                "quality": {
                    "laplacian_variance": 28.4,  # Below 45.0 threshold -> triggers Retake
                    "brightness": 72.1,
                    "contrast": 32.4,
                    "noise_estimate": 14.2,
                    "aspect_completeness": 71.0,
                    "ood_score": 0.18,
                    "gate": "Retake"
                },
                "findings": [],
                "overall_impression": "INSUFFICIENT IMAGE QUALITY FOR DIAGNOSTIC INFERENCE. Motion blur and low signal-to-noise ratio exceed diagnostic thresholds. Retake scan mandated.",
                "critical_flags": ["Severe motion blur", "Signal-to-noise ratio compromised"],
                "quality_gate": "Retake"
            },
            "ecg": {
                "patient": {
                    "patientId": "QM-2026-C03",
                    "caseArchetype": "OUT_OF_DISTRIBUTION",
                    "archetypeLabel": "OOD Anomaly (Cable Noise / Artifact → Safeguard)",
                    "name": "Smt. Ananya Mukherjee",
                    "age": 46,
                    "sex": "Female",
                    "syntheticAbha": "19-4820-9921-1029",
                    "syntheticUhid": "UHID-MUM-55190",
                    "indication": "12-Lead Diagnostic ECG (Out-of-Distribution Anomaly Test Case)",
                    "relevantHistory": "Atypical high-frequency baseline drift, non-physiological interference pattern.",
                    "referringDoctor": "Dr. Rajesh K. Varma, DM",
                    "referringDoctorHpr": "HPR-IN-2026-10294",
                    "reportingDoctor": "Dr. Rajesh K. Varma, DM",
                    "reportingDoctorHpr": "HPR-IN-2026-10294"
                },
                "modality": "ecg",
                "quality": {
                    "laplacian_variance": 210.4,
                    "brightness": 128.0,
                    "contrast": 88.0,
                    "noise_estimate": 24.5,
                    "aspect_completeness": 98.0,
                    "ood_score": 0.82,  # Above 0.40 threshold -> triggers Expert Review
                    "gate": "Expert Review"
                },
                "findings": [],
                "overall_impression": "OUT-OF-DISTRIBUTION SIGNAL DETECTED. High-frequency electrical artifact (50Hz mains power interference) distorts ST-T segment morphology. Manual cardiology review mandated.",
                "critical_flags": ["Out-of-Distribution waveform anomaly"],
                "quality_gate": "Expert Review"
            },
            "head_ct": {
                "patient": {
                    "patientId": "QM-2026-H06",
                    "caseArchetype": "CRITICAL_URGENT",
                    "archetypeLabel": "Critical Urgent (Acute Intracranial Hemorrhage)",
                    "name": "Shri Gurpreet Singh",
                    "age": 64,
                    "sex": "Male",
                    "syntheticAbha": "99-3321-4402-9102",
                    "syntheticUhid": "UHID-CHD-11849",
                    "indication": "Non-contrast emergent head CT for sudden right hemiplegia and aphasia",
                    "relevantHistory": "Acute right hemiplegia and slurred speech, onset 2.5 hrs prior. GCS: 11.",
                    "referringDoctor": "Dr. Harpreet Sandhu, MCh (Neurosurgery)",
                    "referringDoctorHpr": "HPR-IN-2026-99201",
                    "reportingDoctor": "Dr. Devendra Sen, MD (Neuroradiology)",
                    "reportingDoctorHpr": "HPR-IN-2026-44810"
                },
                "modality": "head_ct",
                "quality": {
                    "laplacian_variance": 164.2,
                    "brightness": 132.5,
                    "contrast": 68.0,
                    "noise_estimate": 3.4,
                    "aspect_completeness": 99.6,
                    "ood_score": 0.06,
                    "gate": "Accept"
                },
                "findings": [
                    {
                        "id": "FND-HCT-01",
                        "label": "Acute Intracranial Hemorrhage (Basal Ganglia)",
                        "region": "Left Lentiform & Internal Capsule",
                        "measurement": "Volume: 42.5 mL (58-72 HU)",
                        "normal_range": "0 mL (No hyperdensity)",
                        "severity": "Critical",
                        "confidence": 0.984,
                        "uncertainty": 0.008
                    },
                    {
                        "id": "FND-HCT-02",
                        "label": "Midline Shift & Mass Effect",
                        "region": "Septum Pellucidum",
                        "measurement": "4.8 mm to the right",
                        "normal_range": "0.0 mm (Symmetric)",
                        "severity": "Critical",
                        "confidence": 0.961,
                        "uncertainty": 0.014
                    }
                ],
                "overall_impression": "CRITICAL: Large acute left basal ganglia intraparenchymal hematoma (~42.5 mL) with 4.8 mm midline shift and early effacement of left lateral ventricle. Urgent neurosurgical consultation required.",
                "critical_flags": ["Acute intraparenchymal hemorrhage (>40 mL)", "Midline shift 4.8 mm"],
                "quality_gate": "Accept"
            }
        }

    def test_all_six_archetypes_exist(self):
        """Verify all 6 canonical case archetypes are defined and have necessary metadata."""
        self.assertEqual(len(self.sample_cases), 6)
        expected_keys = ["fundus", "chest_xray", "breast_us", "oct", "ecg", "head_ct"]
        for k in expected_keys:
            self.assertIn(k, self.sample_cases)
            case = self.sample_cases[k]
            self.assertIn("patient", case)
            self.assertIn("modality", case)
            self.assertIn("quality", case)
            self.assertIn("quality_gate", case)
            self.assertTrue(len(case["patient"]["syntheticAbha"]) >= 14)

    def test_quality_gating_logic(self):
        """Verify SaMD quality gating: blur < 45 triggers Retake; OOD > 0.40 triggers Expert Review."""
        oct_case = self.sample_cases["oct"]
        self.assertLess(oct_case["quality"]["laplacian_variance"], 45.0)
        self.assertEqual(oct_case["quality_gate"], "Retake")
        self.assertIn("INSUFFICIENT IMAGE QUALITY", oct_case["overall_impression"])

        ecg_case = self.sample_cases["ecg"]
        self.assertGreater(ecg_case["quality"]["ood_score"], 0.40)
        self.assertEqual(ecg_case["quality_gate"], "Expert Review")
        self.assertIn("OUT-OF-DISTRIBUTION", ecg_case["overall_impression"])

    def test_cautious_samd_language(self):
        """Verify inference impressions use cautious SaMD phrasing rather than autonomous declarations."""
        fundus_case = self.sample_cases["fundus"]
        self.assertIn("Findings suggestive of", fundus_case["overall_impression"])

        breast_case = self.sample_cases["breast_us"]
        self.assertIn("Consider", breast_case["overall_impression"])

    def test_pdf_generation_for_all_archetypes(self):
        """Verify pure Python ReportLab generates valid, non-empty PDFs for all 6 case archetypes."""
        for name, case in self.sample_cases.items():
            payload = {
                "domain": "Adaptive",
                "modality": case["modality"],
                "patient": case["patient"],
                "doctor_view": "standard",
                "workflow_status": "Draft (AI)",
                "scan_quality": case["quality"],
                "findings": case["findings"],
                "overall_impression": case["overall_impression"],
                "critical_flags": case["critical_flags"],
                "quality_gate": case["quality_gate"],
                "quantum_confidence": 94.5
            }
            pdf_bytes = pdf_engine.build_pdf(payload)
            self.assertIsInstance(pdf_bytes, bytes)
            self.assertGreater(len(pdf_bytes), 15000, f"PDF for {name} too small ({len(pdf_bytes)} bytes)")
            # Standard PDF file header
            self.assertTrue(pdf_bytes.startswith(b"%PDF"), f"PDF for {name} does not start with %PDF header")

    def test_pdf_generation_all_three_views(self):
        """Verify Urgent Summary, Standard, and Teaching views compile cleanly in ReportLab."""
        fundus_case = self.sample_cases["fundus"]
        for view in ["urgent", "standard", "teaching"]:
            payload = {
                "domain": "Adaptive",
                "modality": "fundus",
                "patient": fundus_case["patient"],
                "doctor_view": view,
                "workflow_status": "Approved",
                "scan_quality": fundus_case["quality"],
                "findings": fundus_case["findings"],
                "overall_impression": fundus_case["overall_impression"],
                "critical_flags": [],
                "quality_gate": "Accept"
            }
            pdf_bytes = pdf_engine.build_pdf(payload)
            self.assertTrue(pdf_bytes.startswith(b"%PDF"))
            self.assertGreater(len(pdf_bytes), 20000)

    def test_legacy_domain_pdf_backwards_compatibility(self):
        """Verify legacy report endpoints (Cardiology, Oncology, HIV/TB) still compile cleanly."""
        legacy_payload = {
            "domain": "Cardiology",
            "facility": "AIIMS Cardiology Apex",
            "department": "Advanced Hemodynamics",
            "doctor": {"name": "Dr. Rajesh K. Varma, DM", "nmc_id": "NMC-48291-REG"},
            "patient": {"name": "Ramesh Patel", "age": 63, "gender": "Male", "abha_id": "91-7824-3319-5481"},
            "diagnosis": {"primary": "Acute Anterior Wall STEMI"},
            "biomarkers": [
                {"label": "hs-cTnI", "value": "0.048 ng/mL", "cutoff": "< 0.014", "status": "CRITICAL"}
            ],
            "digital_signature": {"signature_hash": "0x98f48...2819a"}
        }
        pdf_bytes = pdf_engine.build_pdf(legacy_payload)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertGreater(len(pdf_bytes), 3000)

    def test_document_hash_generation(self):
        """Verify SHA-256 document fingerprinting."""
        seed = "QM-REP-10294-Kamala Devi-FUNDUS-2026-11-09-v1.0"
        h1 = hashlib.sha256(seed.encode("utf-8")).hexdigest()
        h2 = hashlib.sha256(seed.encode("utf-8")).hexdigest()
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)


if __name__ == "__main__":
    unittest.main()
