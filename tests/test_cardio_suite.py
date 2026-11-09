import unittest
import sys
import os
import numpy as np
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cardio_fabric.ecg_signal_parser import ECGSignalParser
from src.cardio_fabric.preset_cardio_cases import get_cardio_preset_patients
from src.cardio_latent.cardiac_attention import CardiacLatentEngine
from src.cardio_quantum.amplitude_encoder import AmplitudeEncoder
from src.cardio_quantum.vqc_classifier import VariationalQuantumClassifier
from src.cardio_quantum.qsvm_kernel import QuantumSVM
from src.cardio_quantum.hybrid_ensemble import HybridQuantumEnsemble
from src.cardio_xai.ecg_gradcam import ECGGradCAM
from src.cardio_xai.biomarker_shap import CardiacBiomarkerSHAP
from src.cardio_xai.counterfactual_dice import DiCECardiacCounterfactual
from src.cardio_decision.staging_engine import CardiologyStagingEngine, CryptoAuditLogger
from web.app import app

class TestCardioQMLPlatform(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.patients = get_cardio_preset_patients()

    def test_12lead_ecg_parser(self):
        parser = ECGSignalParser(sampling_rate=250)
        res = parser.generate_synthetic_12lead(
            duration_sec=10.0, rhythm_type="normal", heart_rate=80.0, st_elevation_mv=-0.20, qtc_ms=430.0
        )
        self.assertEqual(len(res["leads"]), 12)
        self.assertIn("Lead II", res["leads"])
        self.assertIn("V5", res["leads"])
        self.assertAlmostEqual(res["metrics"]["heart_rate_bpm"], 80.0, delta=1.0)
        self.assertAlmostEqual(res["metrics"]["st_deviation_mv"], -0.20, delta=0.01)

    def test_cardiac_twin_and_fhir(self):
        pt = self.patients["cad_ischemia"]
        self.assertEqual(pt.demographics["gender"], "Male")
        self.assertIn("hs_ctni_ug_l", pt.cardiac_biomarkers)
        
        bundle = pt.to_fhir_bundle()
        self.assertEqual(bundle["resourceType"], "Bundle")
        self.assertTrue(len(bundle["entry"]) >= 4)
        self.assertEqual(bundle["entry"][0]["resource"]["resourceType"], "Patient")

    def test_cardiac_attention_and_l2_normalization(self):
        engine = CardiacLatentEngine()
        pt = self.patients["cad_ischemia"]
        raw_16d = engine.extract_biomarker_vector(
            pt.cardiac_biomarkers, pt.hemodynamics, pt.echocardiogram, pt.ecg_data["metrics"], pt.demographics
        )
        self.assertEqual(len(raw_16d), 16)
        
        gated_16d, amps_16d = engine.project_to_quantum_state(raw_16d, pt.condition_label)
        self.assertEqual(len(amps_16d), 16)
        # Verify exact L2 unit hypersphere norm
        norm = np.linalg.norm(amps_16d)
        self.assertAlmostEqual(norm, 1.0, places=5)

    def test_quantum_amplitude_and_classifiers(self):
        encoder = AmplitudeEncoder(n_qubits=4)
        amps = np.ones(16) / 4.0
        state = encoder.prepare_state(amps)
        self.assertEqual(len(state), 16)
        self.assertAlmostEqual(np.linalg.norm(state), 1.0, places=5)
        
        zz_state = encoder.apply_zz_feature_map(state, amps)
        self.assertAlmostEqual(np.linalg.norm(zz_state), 1.0, places=5)
        
        vqc = VariationalQuantumClassifier()
        vqc_res = vqc.predict(zz_state)
        self.assertTrue(0.0 <= vqc_res["vqc_probability"] <= 1.0)
        
        qsvm = QuantumSVM()
        qsvm_res = qsvm.predict(zz_state)
        self.assertTrue(0.0 <= qsvm_res["qsvm_probability"] <= 1.0)

    def test_hybrid_ensemble_calibration(self):
        ensemble = HybridQuantumEnsemble(temperature=1.42)
        raw_16d = np.ones(16) * 0.5
        vqc_res = {"vqc_probability": 0.75}
        qsvm_res = {"qsvm_probability": 0.80, "quantum_margin": 0.40}
        h_res = ensemble.predict_hybrid(raw_16d, vqc_res, qsvm_res)
        
        self.assertIn("calibrated_risk_probability", h_res)
        self.assertTrue(0.0 <= h_res["calibrated_risk_probability"] <= 1.0)
        self.assertIn("epistemic_uncertainty", h_res)

    def test_xai_and_counterfactual(self):
        shap_eng = CardiacBiomarkerSHAP()
        pt = self.patients["cad_ischemia"]
        shap = shap_eng.compute_shap_attribution(
            pt.cardiac_biomarkers, pt.hemodynamics, pt.ecg_data["metrics"], 0.70
        )
        self.assertTrue(len(shap) > 0)
        
        cf_eng = DiCECardiacCounterfactual()
        cf = cf_eng.compute_optimal_targets(
            pt.cardiac_biomarkers, pt.hemodynamics, pt.ecg_data["metrics"], 0.70
        )
        self.assertTrue(cf["action_required"])
        self.assertTrue(len(cf["clinical_changes"]) >= 2)

    def test_web_api_endpoints(self):
        # 1. Homepage UI
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Cardio-QML", resp.data)

        # 2. Patient API
        resp = self.client.get("/api/cardio/patient/cad_ischemia")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("patient", data)
        self.assertIn("ecg_data", data)

        # 3. Hybrid Prediction API
        resp = self.client.post("/api/cardio/predict", json={"patient_key": "cad_ischemia"})
        self.assertEqual(resp.status_code, 200)
        res = resp.get_json()
        self.assertIn("hybrid_result", res)
        self.assertIn("ecg_gradcam_attention", res)
        self.assertIn("staging", res)

        # 4. Counterfactual Real-Time API
        resp = self.client.post("/api/cardio/counterfactual", json={"patient_key": "cad_ischemia"})
        self.assertEqual(resp.status_code, 200)
        res_cf = resp.get_json()
        self.assertIn("calibrated_risk_probability", res_cf)

        # 5. FHIR Cardiology Export
        resp = self.client.get("/api/cardio/report/fhir/cad_ischemia")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, "application/json")

        # 6. Dataset Samples Endpoint
        resp_samples = self.client.get("/api/cardio/dataset_samples")
        self.assertEqual(resp_samples.status_code, 200)
        samples_data = json.loads(resp_samples.data)
        self.assertIn("samples", samples_data)
        self.assertGreaterEqual(len(samples_data["samples"]), 4)

        # 7. Single Patient Custom Prediction (Positive CVD Case)
        pt_pos = {
            "age": 55, "gender": "Male", "sbp": 160, "dbp": 100, "pulse": 85,
            "bmi": 31.0, "cholesterol": 260, "glucose": 130, "smoke": 1, "active": 0,
            "ground_truth_label": 1
        }
        resp_pred = self.client.post("/api/cardio/predict_custom", json=pt_pos)
        self.assertEqual(resp_pred.status_code, 200)
        pred_data = json.loads(resp_pred.data)
        self.assertTrue(pred_data["is_cvd_positive"])
        self.assertEqual(pred_data["prediction_status"], "CVD Positive")
        self.assertTrue(pred_data["ground_truth_matched"])
        self.assertIn("calibrated_risk_percent", pred_data)
        self.assertIn("quantum_state_amps", pred_data)
        self.assertIn("shap_attributions", pred_data)
        self.assertIn("counterfactuals", pred_data)

        # 8. Single Patient Custom Prediction (Healthy Normal Case)
        pt_neg = {
            "age": 42, "gender": "Female", "sbp": 112, "dbp": 74, "pulse": 68,
            "bmi": 22.0, "cholesterol": 165, "glucose": 88, "smoke": 0, "active": 1,
            "ground_truth_label": 0
        }
        resp_pred_neg = self.client.post("/api/cardio/predict_custom", json=pt_neg)
        self.assertEqual(resp_pred_neg.status_code, 200)
        pred_neg_data = json.loads(resp_pred_neg.data)
        self.assertFalse(pred_neg_data["is_cvd_positive"])
        self.assertEqual(pred_neg_data["prediction_status"], "Healthy / Negative")
        self.assertTrue(pred_neg_data["ground_truth_matched"])

        # 9. Download Sample Batch CSV
        resp_sample_csv = self.client.get("/api/cardio/download_sample_batch_csv")
        self.assertEqual(resp_sample_csv.status_code, 200)
        self.assertIn(b"ap_hi;ap_lo;cholesterol", resp_sample_csv.data)

        # 10. Evaluation Dashboard (ROC & Confusion Matrix)
        resp_eval = self.client.get("/api/cardio/evaluation_dashboard")
        self.assertEqual(resp_eval.status_code, 200)
        eval_data = json.loads(resp_eval.data)
        self.assertIn("confusion_matrix", eval_data)
        self.assertIn("roc_curve", eval_data)
        self.assertIn("computational_efficiency", eval_data)
        self.assertAlmostEqual(eval_data["roc_curve"]["auc"], 0.8382, places=3)

        # 11. Batch Dataset Upload & Prediction
        import io
        csv_file = io.BytesIO(resp_sample_csv.data)
        upload_data = {
            "file": (csv_file, "test_batch.csv")
        }
        resp_upload = self.client.post(
            "/api/cardio/upload_dataset",
            data=upload_data,
            content_type="multipart/form-data"
        )
        self.assertEqual(resp_upload.status_code, 200)
        up_res = json.loads(resp_upload.data)
        self.assertEqual(up_res["total_processed"], 10)
        self.assertGreater(up_res["positive_count"], 0)
        self.assertGreater(up_res["negative_count"], 0)
        self.assertIn("results", up_res)

if __name__ == "__main__":
    unittest.main()
