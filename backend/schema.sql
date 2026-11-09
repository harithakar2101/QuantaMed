-- ============================================================================
-- LensCode – Adaptive QuantaMed
-- PostgreSQL Production Database Schema (CDSCO & ABDM M3 Compliant)
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Synthetic Patients
CREATE TABLE IF NOT EXISTS patients (
    patient_id VARCHAR(64) PRIMARY KEY,
    uhid VARCHAR(64) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    age INT NOT NULL CHECK (age >= 0),
    gender VARCHAR(32) NOT NULL,
    abha_number VARCHAR(32),
    abha_address VARCHAR(128),
    clinical_history TEXT,
    primary_indication TEXT,
    referring_specialist VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_abha ON patients(abha_number);
CREATE INDEX idx_patients_uhid ON patients(uhid);

-- 2. Scans & Multi-Modal Acquisition
CREATE TABLE IF NOT EXISTS scans (
    scan_id VARCHAR(64) PRIMARY KEY,
    patient_id VARCHAR(64) NOT NULL REFERENCES patients(patient_id) ON DELETE RESTRICT,
    modality VARCHAR(32) NOT NULL, -- fundus, oct, ecg, chest_xray, breast_us, head_ct
    source_type VARCHAR(32) DEFAULT 'upload', -- upload, dicom, sample, camera, ecg_csv
    file_path TEXT,
    file_size_bytes BIGINT,
    dimensions_json JSONB, -- width, height, color_channels
    device_model VARCHAR(128),
    acquisition_parameters JSONB,
    acquired_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scans_patient ON scans(patient_id);
CREATE INDEX idx_scans_modality ON scans(modality);

-- 3. Scan Quality Gating Evaluations
CREATE TABLE IF NOT EXISTS quality_evaluations (
    evaluation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scan_id VARCHAR(64) NOT NULL REFERENCES scans(scan_id) ON DELETE CASCADE,
    modality VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL, -- ACCEPT, RETAKE, EXPERT_REVIEW
    overall_quality_score NUMERIC(5, 2) NOT NULL,
    tenengrad_sharpness NUMERIC(8, 2),
    michelson_contrast NUMERIC(8, 2),
    noise_estimate NUMERIC(8, 2),
    completeness_score NUMERIC(5, 2),
    is_out_of_distribution BOOLEAN DEFAULT FALSE,
    ood_divergence_score NUMERIC(6, 4),
    metrics_breakdown JSONB NOT NULL,
    recommendation_text TEXT,
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quality_scan ON quality_evaluations(scan_id);

-- 4. Clinical Reports
CREATE TABLE IF NOT EXISTS clinical_reports (
    report_id VARCHAR(64) PRIMARY KEY,
    accession_number VARCHAR(64) UNIQUE NOT NULL,
    study_id VARCHAR(64) NOT NULL,
    scan_id VARCHAR(64) NOT NULL REFERENCES scans(scan_id) ON DELETE RESTRICT,
    patient_id VARCHAR(64) NOT NULL REFERENCES patients(patient_id) ON DELETE RESTRICT,
    modality VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'Draft', -- Draft, Under Review, Doctor Approved, Digitally Signed, Released to Patient, Revoked
    primary_diagnosis TEXT NOT NULL,
    confidence NUMERIC(5, 4) NOT NULL,
    epistemic_uncertainty NUMERIC(6, 4) NOT NULL,
    quantum_delta_percent NUMERIC(5, 2),
    provenance VARCHAR(64) NOT NULL, -- Rule-based simulation, LLM-assisted (grounded), Backend model v1.4
    report_sha256_hash VARCHAR(64) NOT NULL,
    qr_verification_code TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    signed_at TIMESTAMP WITH TIME ZONE,
    released_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_reports_scan ON clinical_reports(scan_id);
CREATE INDEX idx_reports_patient ON clinical_reports(patient_id);
CREATE INDEX idx_reports_hash ON clinical_reports(report_sha256_hash);

-- 5. Report Versions & Findings
CREATE TABLE IF NOT EXISTS report_versions (
    version_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_id VARCHAR(64) NOT NULL REFERENCES clinical_reports(report_id) ON DELETE CASCADE,
    version_number INT NOT NULL,
    findings_json JSONB NOT NULL,
    recommendations_json JSONB,
    bilingual_summary JSONB, -- en, hi
    updated_by VARCHAR(128) NOT NULL,
    version_sha256 VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(report_id, version_number)
);

-- 6. Doctor Reviews, Caliper Edits & Overrides
CREATE TABLE IF NOT EXISTS doctor_reviews (
    review_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_id VARCHAR(64) NOT NULL REFERENCES clinical_reports(report_id) ON DELETE RESTRICT,
    doctor_id VARCHAR(128) NOT NULL,
    doctor_role VARCHAR(64) NOT NULL, -- Attending Physician, Radiologist, Resident
    hpr_id VARCHAR(64),
    action VARCHAR(32) NOT NULL, -- ACCEPT, MODIFY, OVERRIDE, REJECT
    reclassification VARCHAR(64),
    clinical_rationale TEXT NOT NULL,
    caliper_adjustments JSONB,
    signature_data_url TEXT,
    signature_sha256 VARCHAR(64),
    reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reviews_report ON doctor_reviews(report_id);
CREATE INDEX idx_reviews_doctor ON doctor_reviews(doctor_id);

-- 7. ABDM M3 Consent Artefacts
CREATE TABLE IF NOT EXISTS consent_artefacts (
    consent_id VARCHAR(64) PRIMARY KEY,
    artefact_id VARCHAR(64) UNIQUE NOT NULL,
    abha_id VARCHAR(64) NOT NULL,
    hiu_id VARCHAR(64) NOT NULL,
    hip_id VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'REQUESTED', -- REQUESTED, GRANTED, DENIED, REVOKED, EXPIRED
    purpose_code VARCHAR(32) NOT NULL DEFAULT 'CAREV',
    data_types TEXT[] NOT NULL,
    valid_from TIMESTAMP WITH TIME ZONE NOT NULL,
    valid_to TIMESTAMP WITH TIME ZONE NOT NULL,
    digital_signature_digest VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_consent_abha ON consent_artefacts(abha_id);

-- 8. Cryptographic Hash-Chained Audit Ledger
CREATE TABLE IF NOT EXISTS audit_ledger (
    block_index BIGINT PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    actor VARCHAR(128) NOT NULL,
    role VARCHAR(64) NOT NULL,
    action VARCHAR(64) NOT NULL,
    payload_json JSONB NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    block_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_action ON audit_ledger(action);
CREATE INDEX idx_audit_hash ON audit_ledger(block_hash);

-- Verification view to check block chain continuity
CREATE OR REPLACE VIEW v_audit_integrity AS
SELECT 
    b.block_index,
    b.timestamp,
    b.actor,
    b.action,
    b.previous_hash,
    b.block_hash,
    LAG(b.block_hash, 1, '0000000000000000000000000000000000000000000000000000000000000000') 
        OVER (ORDER BY b.block_index) AS expected_previous_hash,
    CASE 
        WHEN b.previous_hash = LAG(b.block_hash, 1, '0000000000000000000000000000000000000000000000000000000000000000') 
            OVER (ORDER BY b.block_index) THEN TRUE 
        ELSE FALSE 
    END AS is_chain_valid
FROM audit_ledger b;
