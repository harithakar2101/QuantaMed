from typing import Dict, Any, List

class CardiacBiomarkerSHAP:
    """
    Layer 5: Cardiac Biomarker SHAP Clinical Attribution Engine.
    Computes percentage contributions of each cardiac biomarker towards pathological risk.
    """
    def __init__(self):
        self.biomarkers_config = [
            ("High-Sens Troponin I (hs-cTnI)", "hs_ctni_ug_l", 0.014, "ug/L"),
            ("Systolic Blood Pressure", "systolic_bp", 120.0, "mmHg"),
            ("Atherogenic LDL-C", "ldl_c_mg_dl", 100.0, "mg/dL"),
            ("ST-Segment Deviation", "st_deviation_mv", 0.05, "mV"),
            ("NT-proBNP Heart Failure", "nt_probnp_pg_ml", 125.0, "pg/mL"),
            ("Vascular hs-CRP", "hs_crp_mg_l", 1.0, "mg/L"),
            ("Corrected QTc Interval", "qtc_bazett_ms", 430.0, "ms"),
            ("Resting Heart Rate", "heart_rate_bpm", 72.0, "BPM")
        ]

    def compute_shap_attribution(
        self,
        biomarkers: Dict[str, float],
        hemodynamics: Dict[str, float],
        ecg_metrics: Dict[str, float],
        risk_prob: float
    ) -> List[Dict[str, Any]]:
        attributions = []
        is_pathological = risk_prob > 0.45
        
        merged = {**biomarkers, **hemodynamics, **ecg_metrics}
        deltas = {}
        total_delta = 0.0
        
        for name, key, ref, unit in self.biomarkers_config:
            val = abs(float(merged.get(key, ref)))
            delta = max(0.0, (val - ref) / ref)
            deltas[name] = delta
            total_delta += delta
            
        if total_delta < 1e-6:
            total_delta = 1.0
            
        for name, key, ref, unit in self.biomarkers_config:
            val = round(float(merged.get(key, ref)), 3)
            pct = (deltas[name] / total_delta) * 100.0 if is_pathological else 12.5
            sign = "+" if is_pathological and deltas[name] > 0.05 else "-"
            attributions.append({
                "biomarker": name,
                "current_value": val,
                "unit": unit,
                "contribution_pct": round(pct, 1),
                "sign": sign,
                "status": "Elevated" if deltas[name] > 0.20 else "Normal Range"
            })
            
        attributions.sort(key=lambda x: x["contribution_pct"], reverse=True)
        return attributions
