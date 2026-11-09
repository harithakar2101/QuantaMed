# -*- coding: utf-8 -*-
"""
LensCode – Adaptive QuantaMed
Phase 2 Automated Verification Suite
"""

import unittest
import json
import hashlib
from web.app import app

class TestPhase2AdaptivePlatform(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_adaptive_samples(self):
        res = self.app.get('/api/adaptive/samples')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('samples', data)
        self.assertIn('fundus', data['samples'])
        self.assertIn('ecg', data['samples'])
        self.assertIn('chest_xray', data['samples'])

    def test_02_quality_check(self):
        payload = {"modality": "fundus"}
        res = self.app.post('/api/adaptive/quality_check', 
                            data=json.dumps(payload),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('status', data)
        self.assertIn('overall_quality_score', data)
        self.assertIn('metrics', data)

    def test_03_analyze_endpoint(self):
        payload = {
            "scan_id": "SCAN-FND-401",
            "modality": "fundus",
            "detail_level": "standard",
            "patient": {
                "patient_id": "QM-2026-F01",
                "full_name": "Smt. Kamala Devi",
                "age": 62,
                "gender": "Female",
                "clinical_history": "T2DM x 14 yrs, HbA1c 8.8%"
            }
        }
        res = self.app.post('/api/adaptive/analyze',
                            data=json.dumps(payload),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['modality'], 'fundus')
        self.assertIn('findings', data)
        self.assertIn('adaptive_views', data)
        self.assertIn('urgent', data['adaptive_views'])
        self.assertIn('standard', data['adaptive_views'])
        self.assertIn('teaching', data['adaptive_views'])

    def test_04_doctor_review_and_audit(self):
        payload = {
            "scan_id": "SCAN-FND-401",
            "modality": "fundus",
            "doctor_id": "Dr. Sunita Rao, MS",
            "doctor_role": "Attending Physician",
            "action": "ACCEPT",
            "rationale": "Concur with NPDR and CSME macular findings.",
            "caliper_adjustments": {"radius": 14, "offsetX": 2, "offsetY": -1}
        }
        res = self.app.post('/api/adaptive/reviews',
                            data=json.dumps(payload),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn(data['status'], ['RECORDED', 'success'])
        self.assertTrue('immutable_audit_hash' in data or 'immutable_audit_hash' in data.get('review', {}))

        # Audit ledger check
        audit_res = self.app.get('/api/adaptive/audit')
        self.assertEqual(audit_res.status_code, 200)
        audit_data = audit_res.get_json()
        self.assertGreaterEqual(audit_data['total_events'], 1)

    def test_05_report_verify_hash(self):
        sample_text = "REPORT_PAYLOAD_TEST_CANONICAL_STRING"
        sample_hash = hashlib.sha256(sample_text.encode('utf-8')).hexdigest()
        
        payload = {
            "report_id": "LC-2026-000412",
            "report_payload_sha256": sample_hash,
            "canonical_string": sample_text
        }
        res = self.app.post('/api/report/verify_hash',
                            data=json.dumps(payload),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['verified'])
        self.assertEqual(data['status'], 'AUTHENTIC_VALIDATED')

    def test_06_fhir_validate(self):
        bundle = {
            "resourceType": "Bundle",
            "id": "bundle-qm-test",
            "type": "document",
            "entry": [
                {
                    "resource": {
                        "resourceType": "DiagnosticReport",
                        "id": "rep-001",
                        "status": "final",
                        "conclusion": "Moderate NPDR"
                    }
                }
            ]
        }
        res = self.app.post('/api/fhir/validate',
                            data=json.dumps({"fhir_bundle": bundle}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['is_valid'])
        self.assertEqual(data['total_resources'], 1)

    def test_07_abdm_consent_create(self):
        payload = {
            "abha_id": "48-2910-4829-1920",
            "hiu_id": "HIU-QM-DELHI-01",
            "purpose": "CAREV",
            "expiry_date": "2027-11-09T23:59:59Z"
        }
        res = self.app.post('/api/abdm/consent/create',
                            data=json.dumps(payload),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'GRANTED')
        self.assertIn('artefact_id', data)

    def test_08_audit_verify_chain(self):
        # Genesis block
        b0_payload = "02026-11-09T00:00:00ZDr. Sunita RaoAttending PhysicianGENESIS" + "0"*64
        b0_hash = hashlib.sha256(b0_payload.encode('utf-8')).hexdigest()
        b0 = {
            "index": 0,
            "timestamp": "2026-11-09T00:00:00Z",
            "actor": "Dr. Sunita Rao",
            "role": "Attending Physician",
            "action": "GENESIS",
            "previousHash": "0" * 64,
            "hash": b0_hash
        }

        # Block 1
        b1_payload = "12026-11-09T00:01:00ZDr. Sunita RaoAttending PhysicianACCEPT_DX" + b0_hash
        b1_hash = hashlib.sha256(b1_payload.encode('utf-8')).hexdigest()
        b1 = {
            "index": 1,
            "timestamp": "2026-11-09T00:01:00Z",
            "actor": "Dr. Sunita Rao",
            "role": "Attending Physician",
            "action": "ACCEPT_DX",
            "previousHash": b0_hash,
            "hash": b1_hash
        }

        payload = {"blocks": [b0, b1]}
        res = self.app.post('/api/audit/verify_chain',
                            data=json.dumps(payload),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['is_valid'])
        self.assertEqual(data['total_blocks'], 2)

if __name__ == '__main__':
    unittest.main()
