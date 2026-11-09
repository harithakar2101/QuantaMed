import numpy as np
from typing import Dict, Any, Tuple

class CardiacLatentEngine:
    """
    Layer 3: Cardiovascular Latent Intelligence Engine.
    Standardizes 16 multimodal cardiac parameters, applies clinical attention gating,
    and scales to L2 unit hypersphere for quantum amplitude encoding.
    """
    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)
        self.feature_names = [
            "hs_cTnI (Troponin I)",
            "NT-proBNP (Heart Failure)",
            "LDL-C (Atherogenic Lipid)",
            "HDL-C (Inverted Protection)",
            "hs-CRP (Vascular Inflam)",
            "Systolic Blood Pressure",
            "Diastolic Blood Pressure",
            "Resting Heart Rate",
            "QTc Bazett Interval",
            "ST-Segment Deviation",
            "HRV SDNN Dispersion",
            "LVEF % (Ejection Fraction)",
            "LVEDV (LV End-Diastolic)",
            "Body Mass Index",
            "Age Risk Coefficient",
            "Cardiometabolic HbA1c"
        ]

    def extract_biomarker_vector(
        self,
        biomarkers: Dict[str, float],
        hemodynamics: Dict[str, float],
        echocardiogram: Dict[str, Any],
        ecg_metrics: Dict[str, float],
        demographics: Dict[str, Any]
    ) -> np.ndarray:
        """Constructs 16-D continuous cardiac risk representation."""
        vec = np.zeros(16, dtype=np.float64)
        
        # 0. hs-cTnI (Troponin I): 0.003 - 0.15 ug/L
        ctni = biomarkers.get("hs_ctni_ug_l", 0.005)
        vec[0] = min(max((ctni - 0.005) / 0.095, 0.02), 0.98)
        
        # 1. NT-proBNP: 30 - 800 pg/mL
        bnp = biomarkers.get("nt_probnp_pg_ml", 60.0)
        vec[1] = min(max((bnp - 50.0) / 600.0, 0.02), 0.98)
        
        # 2. LDL-C: 70 - 220 mg/dL
        ldl = biomarkers.get("ldl_c_mg_dl", 100.0)
        vec[2] = min(max((ldl - 70.0) / 140.0, 0.02), 0.98)
        
        # 3. HDL-C: Inverted protection (lower HDL = higher risk)
        hdl = biomarkers.get("hdl_c_mg_dl", 50.0)
        vec[3] = min(max((65.0 - hdl) / 40.0, 0.02), 0.98)
        
        # 4. hs-CRP: 0.5 - 10.0 mg/L
        crp = biomarkers.get("hs_crp_mg_l", 1.0)
        vec[4] = min(max((crp - 0.5) / 8.0, 0.02), 0.98)
        
        # 5. SBP: 100 - 190 mmHg
        sbp = hemodynamics.get("systolic_bp", 120.0)
        vec[5] = min(max((sbp - 100.0) / 80.0, 0.02), 0.98)
        
        # 6. DBP: 65 - 115 mmHg
        dbp = hemodynamics.get("diastolic_bp", 80.0)
        vec[6] = min(max((dbp - 65.0) / 45.0, 0.02), 0.98)
        
        # 7. Heart Rate: 50 - 130 BPM
        hr = hemodynamics.get("heart_rate_bpm", 72.0)
        vec[7] = min(max((hr - 55.0) / 65.0, 0.02), 0.98)
        
        # 8. QTc Bazett: 380 - 520 ms
        qtc = ecg_metrics.get("qtc_bazett_ms", 415.0)
        vec[8] = min(max((qtc - 390.0) / 110.0, 0.02), 0.98)
        
        # 9. ST Deviation: 0.0 - 0.35 mV
        st = abs(ecg_metrics.get("st_deviation_mv", 0.0))
        vec[9] = min(max(st / 0.30, 0.02), 0.98)
        
        # 10. HRV SDNN: lower = higher autonomic dysfunction
        hrv = ecg_metrics.get("hrv_sdnn_ms", 45.0)
        vec[10] = min(max((70.0 - hrv) / 55.0, 0.02), 0.98)
        
        # 11. LVEF %: Inverted (lower EF = heart failure)
        ef = echocardiogram.get("lvef_pct", 60.0)
        vec[11] = min(max((65.0 - ef) / 35.0, 0.02), 0.98)
        
        # 12. LVEDV: 90 - 180 mL
        edv = echocardiogram.get("lvedv_ml", 110.0)
        vec[12] = min(max((edv - 95.0) / 75.0, 0.02), 0.98)
        
        # 13. BMI: 18 - 40
        bmi = demographics.get("bmi", 24.5)
        vec[13] = min(max((bmi - 19.0) / 18.0, 0.02), 0.98)
        
        # 14. Age: 30 - 85
        age = demographics.get("age", 52.0)
        vec[14] = min(max((age - 30.0) / 50.0, 0.02), 0.98)
        
        # 15. Cardiometabolic HbA1c: 4.8 - 11.0%
        a1c = biomarkers.get("hba1c_pct", 5.4)
        vec[15] = min(max((a1c - 5.0) / 5.0, 0.02), 0.98)
        
        return np.clip(vec, 0.01, 0.99)

    def compute_cardiac_attention(self, raw_16d: np.ndarray, condition_hint: str = "") -> np.ndarray:
        """Dynamic feature gating aligning with AHA/ACC guidelines."""
        weights = np.ones(16, dtype=np.float64)
        
        # If Ischemic CAD / Myocardial Infarction profile:
        if "ischemi" in condition_hint.lower() or "cad" in condition_hint.lower() or "coronary" in condition_hint.lower():
            weights[0] *= 3.4 # hs-cTnI
            weights[2] *= 2.8 # LDL-C
            weights[4] *= 2.4 # hs-CRP
            weights[5] *= 2.6 # SBP
            weights[9] *= 3.6 # ST Deviation
            weights[11] *= 2.2 # LVEF
        # If Arrhythmia / Conduction profile:
        elif "arrhyth" in condition_hint.lower() or "afib" in condition_hint.lower() or "fibril" in condition_hint.lower():
            weights[1] *= 2.5 # NT-proBNP
            weights[7] *= 3.2 # Heart Rate
            weights[8] *= 3.8 # QTc
            weights[10] *= 3.0 # HRV
            weights[5] *= 2.0 # SBP
            
        return raw_16d * weights

    def project_to_quantum_state(self, raw_16d: np.ndarray, condition_hint: str = "") -> Tuple[np.ndarray, np.ndarray]:
        """
        Projects through cardiac attention gate and normalizes to L2 unit hypersphere.
        Returns:
            gated_16d: Scaled feature vector
            amplitudes_16d: L2-normalized vector where sum(|x_i|^2) = 1.0
        """
        gated_16d = self.compute_cardiac_attention(raw_16d, condition_hint)
        exp_vec = np.exp(gated_16d - np.max(gated_16d))
        norm_l2 = np.linalg.norm(exp_vec)
        amplitudes_16d = exp_vec / (norm_l2 + 1e-12)
        return gated_16d, amplitudes_16d
