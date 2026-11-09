from datetime import datetime, timezone
import uuid
from typing import Dict, Any, List, Optional

class CardiovascularPatientTwin:
    """
    Cardiovascular Digital Patient Twin encapsulating 12-lead ECG,
    cardiac biomarkers, hemodynamics, echocardiogram metrics, and EHR history.
    """
    def __init__(
        self,
        patient_id: Optional[str] = None,
        hospital_id: str = "CARDIO-EXCELLENCE-AIIMS",
        visit_id: Optional[str] = None,
        condition_label: str = "Coronary Artery Disease & Myocardial Ischemia",
        demographics: Optional[Dict[str, Any]] = None,
        cardiac_biomarkers: Optional[Dict[str, float]] = None,
        hemodynamics: Optional[Dict[str, float]] = None,
        echocardiogram: Optional[Dict[str, Any]] = None,
        clinical_history: Optional[List[str]] = None,
        ecg_data: Optional[Dict[str, Any]] = None
    ):
        self.patient_id = patient_id or f"CARDIO-PT-{uuid.uuid4().hex[:8].upper()}"
        self.visit_id = visit_id or f"VST-CVD-{uuid.uuid4().hex[:6].upper()}"
        self.hospital_id = hospital_id
        self.condition_label = condition_label
        self.timestamp = datetime.now(timezone.utc).isoformat()
        
        self.demographics = demographics or {
            "age": 62,
            "gender": "Male",
            "bmi": 28.6,
            "smoking_status": "Current Smoker",
            "family_cad_history": "Positive (Father MI at age 52)"
        }
        
        # Core Cardiac Biomarkers & Lipid Profile
        self.cardiac_biomarkers = cardiac_biomarkers or {
            "hs_ctni_ug_l": 0.084,         # High-sensitivity Troponin I (ref < 0.014 ug/L)
            "nt_probnp_pg_ml": 280.0,       # Heart Failure marker (ref < 125 pg/mL)
            "ldl_c_mg_dl": 168.0,           # Atherogenic LDL (ref < 100 mg/dL)
            "hdl_c_mg_dl": 38.0,            # Protective HDL (ref > 40 mg/dL)
            "total_cholesterol": 242.0,     # Total cholesterol (mg/dL)
            "hs_crp_mg_l": 4.8,             # Systemic vascular inflammation (ref < 1.0 mg/L)
            "fasting_glucose_mg_dl": 142.0, # Fasting glucose (mg/dL)
            "hba1c_pct": 7.2                # HbA1c (%)
        }
        
        # Hemodynamics & Vitals
        self.hemodynamics = hemodynamics or {
            "systolic_bp": 158.0,
            "diastolic_bp": 96.0,
            "heart_rate_bpm": 84.0,
            "mean_arterial_pressure": 116.7
        }
        
        # Echocardiography & Cardiac Imaging
        self.echocardiogram = echocardiogram or {
            "lvef_pct": 48.0,               # Left Ventricular Ejection Fraction (%)
            "lvedv_ml": 142.0,              # LV End-Diastolic Volume (mL)
            "wall_motion": "Hypokinesia of Inferior-Posterior Wall",
            "valvular_regurgitation": "Mild Mitral Regurgitation"
        }
        
        self.clinical_history = clinical_history or [
            "Exertional retrosternal chest pressure (CCS Class II-III Angina)",
            "Stage 2 Essential Hypertension (10 years duration)",
            "Dyslipidemia with statin intolerance history"
        ]
        
        self.ecg_data = ecg_data or {}

    def to_fhir_bundle(self) -> Dict[str, Any]:
        """Convert patient twin state into an official HL7 FHIR R4 Cardiology Bundle."""
        return {
            "resourceType": "Bundle",
            "id": f"fhir-cardio-{self.visit_id}",
            "type": "document",
            "timestamp": self.timestamp,
            "entry": [
                {
                    "resource": {
                        "resourceType": "Patient",
                        "id": self.patient_id,
                        "gender": self.demographics.get("gender", "unknown").lower(),
                        "extension": [{"url": "http://hl7.org/fhir/StructureDefinition/patient-age", "valueInteger": self.demographics.get("age")}]
                    }
                },
                {
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {"coding": [{"system": "http://loinc.org", "code": "10839-9", "display": "High Sensitivity Troponin I"}]},
                        "valueQuantity": {"value": self.cardiac_biomarkers.get("hs_ctni_ug_l"), "unit": "ug/L"}
                    }
                },
                {
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {"coding": [{"system": "http://loinc.org", "code": "33762-6", "display": "NT-proBNP in Serum"}]},
                        "valueQuantity": {"value": self.cardiac_biomarkers.get("nt_probnp_pg_ml"), "unit": "pg/mL"}
                    }
                },
                {
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "code": {"coding": [{"system": "http://loinc.org", "code": "85354-9", "display": "Blood Pressure Panel"}]},
                        "component": [
                            {"code": {"coding": [{"system": "http://loinc.org", "code": "8480-6"}]}, "valueQuantity": {"value": self.hemodynamics.get("systolic_bp"), "unit": "mmHg"}},
                            {"code": {"coding": [{"system": "http://loinc.org", "code": "8462-4"}]}, "valueQuantity": {"value": self.hemodynamics.get("diastolic_bp"), "unit": "mmHg"}}
                        ]
                    }
                },
                {
                    "resource": {
                        "resourceType": "Condition",
                        "clinicalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]},
                        "code": {"coding": [{"system": "http://snomed.info/sct", "code": "53741008", "display": "Coronary Artery Disease"}]}
                    }
                }
            ]
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "hospital_id": self.hospital_id,
            "visit_id": self.visit_id,
            "condition_label": self.condition_label,
            "timestamp": self.timestamp,
            "demographics": self.demographics,
            "cardiac_biomarkers": self.cardiac_biomarkers,
            "hemodynamics": self.hemodynamics,
            "echocardiogram": self.echocardiogram,
            "clinical_history": self.clinical_history,
            "ecg_metrics": self.ecg_data.get("metrics", {})
        }
