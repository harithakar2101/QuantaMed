from typing import Dict
from .cardiac_twin import CardiovascularPatientTwin
from .ecg_signal_parser import ECGSignalParser

def get_cardio_preset_patients() -> Dict[str, CardiovascularPatientTwin]:
    """Generates 3 clinical benchmark cardiology patient twins with pre-computed 12-lead ECGs."""
    parser = ECGSignalParser(sampling_rate=250)
    
    # Case 1: Coronary Artery Disease & Ischemia
    ecg1 = parser.generate_synthetic_12lead(
        duration_sec=10.0,
        rhythm_type="normal",
        heart_rate=84.0,
        st_elevation_mv=-0.22, # 2.2 mm ST depression in V4-V6
        qtc_ms=438.0
    )
    p1 = CardiovascularPatientTwin(
        patient_id="CARDIO-CAD-402",
        condition_label="Coronary Artery Disease & Myocardial Ischemia",
        demographics={"age": 62, "gender": "Male", "bmi": 28.6, "smoking_status": "Current Smoker (20 pk-yr)", "family_cad": "Yes"},
        cardiac_biomarkers={
            "hs_ctni_ug_l": 0.084,
            "nt_probnp_pg_ml": 280.0,
            "ldl_c_mg_dl": 168.0,
            "hdl_c_mg_dl": 38.0,
            "total_cholesterol": 242.0,
            "hs_crp_mg_l": 4.8,
            "fasting_glucose_mg_dl": 142.0,
            "hba1c_pct": 7.2
        },
        hemodynamics={"systolic_bp": 158.0, "diastolic_bp": 96.0, "heart_rate_bpm": 84.0, "mean_arterial_pressure": 116.7},
        echocardiogram={"lvef_pct": 48.0, "lvedv_ml": 142.0, "wall_motion": "Hypokinesia of Inferior-Posterior Wall"},
        clinical_history=[
            "Exertional retrosternal chest pain radiating to left arm (CCS Class III)",
            "Stage 2 Essential Hypertension (10 years)",
            "Known hyperlipidemia"
        ],
        ecg_data=ecg1
    )

    # Case 2: Arrhythmia & Conduction Disorder (Atrial Fibrillation + Prolonged QTc)
    ecg2 = parser.generate_synthetic_12lead(
        duration_sec=10.0,
        rhythm_type="atrial_fibrillation",
        heart_rate=108.0,
        st_elevation_mv=0.0,
        qtc_ms=488.0 # Pathological QTc prolongation
    )
    p2 = CardiovascularPatientTwin(
        patient_id="CARDIO-AFIB-189",
        condition_label="Atrial Fibrillation & Conduction Defect",
        demographics={"age": 68, "gender": "Female", "bmi": 26.2, "smoking_status": "Non-Smoker", "family_cad": "No"},
        cardiac_biomarkers={
            "hs_ctni_ug_l": 0.012,
            "nt_probnp_pg_ml": 450.0,
            "ldl_c_mg_dl": 124.0,
            "hdl_c_mg_dl": 46.0,
            "total_cholesterol": 198.0,
            "hs_crp_mg_l": 2.6,
            "fasting_glucose_mg_dl": 104.0,
            "hba1c_pct": 5.9
        },
        hemodynamics={"systolic_bp": 146.0, "diastolic_bp": 88.0, "heart_rate_bpm": 108.0, "mean_arterial_pressure": 107.3},
        echocardiogram={"lvef_pct": 52.0, "lvedv_ml": 128.0, "wall_motion": "Left Atrial Enlargement (LAA Index 4.2 cm)"},
        clinical_history=[
            "Episodic nocturnal palpitations with sudden onset breathlessness",
            "CHA2DS2-VASc score = 3 (Oral anticoagulation indicated)",
            "History of transient presyncope"
        ],
        ecg_data=ecg2
    )

    # Case 3: Healthy Control
    ecg3 = parser.generate_synthetic_12lead(
        duration_sec=10.0,
        rhythm_type="normal",
        heart_rate=62.0,
        st_elevation_mv=0.0,
        qtc_ms=408.0
    )
    p3 = CardiovascularPatientTwin(
        patient_id="CARDIO-HEALTH-012",
        condition_label="Normal Sinus Rhythm / Low Cardiovascular Risk",
        demographics={"age": 32, "gender": "Male", "bmi": 22.8, "smoking_status": "Non-Smoker", "family_cad": "No"},
        cardiac_biomarkers={
            "hs_ctni_ug_l": 0.003,
            "nt_probnp_pg_ml": 42.0,
            "ldl_c_mg_dl": 88.0,
            "hdl_c_mg_dl": 58.0,
            "total_cholesterol": 164.0,
            "hs_crp_mg_l": 0.6,
            "fasting_glucose_mg_dl": 86.0,
            "hba1c_pct": 5.1
        },
        hemodynamics={"systolic_bp": 116.0, "diastolic_bp": 74.0, "heart_rate_bpm": 62.0, "mean_arterial_pressure": 88.0},
        echocardiogram={"lvef_pct": 64.0, "lvedv_ml": 112.0, "wall_motion": "Normal Biventricular Function"},
        clinical_history=[
            "Annual executive sports cardiology evaluation",
            "Asymptomatic with high functional exercise capacity"
        ],
        ecg_data=ecg3
    )

    return {"cad_ischemia": p1, "atrial_fibrillation": p2, "healthy_control": p3}
