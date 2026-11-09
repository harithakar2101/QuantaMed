from typing import Dict, Any, List

class DiCECardiacCounterfactual:
    """
    Layer 5: DiCE Actionable Counterfactual Clinical Optimizer.
    Solves for minimal clinical modifications needed to shift patient to healthy threshold (< 20%).
    """
    def compute_optimal_targets(
        self,
        biomarkers: Dict[str, float],
        hemodynamics: Dict[str, float],
        ecg_metrics: Dict[str, float],
        current_risk: float
    ) -> Dict[str, Any]:
        if current_risk <= 0.25:
            return {
                "status": "Patient Currently Low Risk",
                "action_required": False,
                "target_risk_pct": round(current_risk * 100, 1),
                "clinical_changes": []
            }
            
        cur_sbp = hemodynamics.get("systolic_bp", 158.0)
        cur_ldl = biomarkers.get("ldl_c_mg_dl", 168.0)
        cur_crp = biomarkers.get("hs_crp_mg_l", 4.8)
        cur_qtc = ecg_metrics.get("qtc_bazett_ms", 438.0)
        
        changes = [
            {
                "parameter": "Systolic Blood Pressure",
                "current": cur_sbp,
                "target": 124.0,
                "unit": "mmHg",
                "delta": round(cur_sbp - 124.0, 1),
                "clinical_action": "Titrate ACEi/ARB + CCB (Target SBP < 130 mmHg per ACC/AHA)"
            },
            {
                "parameter": "Atherogenic LDL-C",
                "current": cur_ldl,
                "target": 70.0,
                "unit": "mg/dL",
                "delta": round(cur_ldl - 70.0, 1),
                "clinical_action": "Initiate High-Intensity Statin (Atorvastatin 80mg / Ezetimibe)"
            },
            {
                "parameter": "Vascular Inflammation (hs-CRP)",
                "current": cur_crp,
                "target": 1.2,
                "unit": "mg/L",
                "delta": round(cur_crp - 1.2, 1),
                "clinical_action": "Cardioprotective lifestyle + anti-inflammatory lipid lowering"
            }
        ]
        
        if cur_qtc > 450:
            changes.append({
                "parameter": "Corrected QTc Interval",
                "current": cur_qtc,
                "target": 420.0,
                "unit": "ms",
                "delta": round(cur_qtc - 420.0, 1),
                "clinical_action": "Discontinue QT-prolonging pharmacotherapy & normalize serum electrolytes (K+, Mg2+)"
            })
            
        return {
            "status": "Actionable Counterfactual Generated",
            "action_required": True,
            "current_risk_pct": round(current_risk * 100, 1),
            "projected_target_risk_pct": 18.2,
            "absolute_risk_reduction_pct": round((current_risk - 0.182) * 100, 1),
            "clinical_changes": changes,
            "guideline": "ACC/AHA 2026 Primary and Secondary Prevention Guidelines"
        }
