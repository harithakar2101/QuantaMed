from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class ModalityEnum(str, Enum):
    FUNDUS = "fundus"
    OCT = "oct"
    ECG = "ecg"
    CHEST_XRAY = "chest_xray"
    BREAST_US = "breast_us"
    HEAD_CT = "head_ct"

class DetailLevelEnum(str, Enum):
    URGENT = "urgent"
    STANDARD = "standard"
    TEACHING = "teaching"

class QualityStatusEnum(str, Enum):
    ACCEPT = "ACCEPT"
    RETAKE = "RETAKE"
    EXPERT_REVIEW = "EXPERT_REVIEW"

class ReviewActionEnum(str, Enum):
    ACCEPT = "ACCEPT"
    MODIFY = "MODIFY"
    OVERRIDE = "OVERRIDE"
    REJECT = "REJECT"

class PatientProfile(BaseModel):
    patient_id: str = Field(..., example="QM-2026-8941")
    full_name: str = Field(..., example="Aarav Sharma")
    age: int = Field(..., example=54)
    gender: str = Field(..., example="Male")
    abha_id: Optional[str] = Field("91-4829-1029-4821@abdm", example="91-4829-1029-4821@abdm")
    clinical_history: str = Field(..., example="Type-2 Diabetes (9 yrs), persistent hypertension, exertional chest discomfort.")
    referring_specialist: Optional[str] = Field("Dr. Rajesh K. Varma, DM", example="Dr. Rajesh K. Varma, DM")

class QualityCheckRequest(BaseModel):
    modality: ModalityEnum
    image_base64: Optional[str] = None
    sample_id: Optional[str] = None

class QualityMetric(BaseModel):
    name: str
    score: float
    threshold: float
    passed: bool
    status_label: str

class QualityCheckResponse(BaseModel):
    status: QualityStatusEnum
    overall_quality_score: float
    tenengrad_sharpness: float
    contrast_michelson: float
    illumination_uniformity: float
    completeness_score: float
    ood_anomaly_score: float
    metrics: List[QualityMetric]
    recommendation_text: str
    can_proceed: bool
    flags: List[str]

class FindingItem(BaseModel):
    id: str
    label: str
    severity: str
    confidence: float
    uncertainty: float
    anatomical_site: str
    measurements: Dict[str, Any]
    coordinates: Optional[List[Dict[str, float]]] = None

class AdaptivePersonaView(BaseModel):
    level: DetailLevelEnum
    headline: str
    summary: str
    key_metrics: List[Dict[str, Any]]
    actionable_steps: List[str]
    teaching_notes: Optional[Dict[str, Any]] = None

class AnalysisRequest(BaseModel):
    scan_id: str
    modality: ModalityEnum
    detail_level: DetailLevelEnum = DetailLevelEnum.STANDARD
    patient: Optional[PatientProfile] = None
    override_quality_gate: bool = False

class AnalysisResponse(BaseModel):
    scan_id: str
    modality: ModalityEnum
    detail_level: DetailLevelEnum
    timestamp: str
    primary_diagnosis: str
    findings: List[FindingItem]
    overall_confidence: float
    overall_uncertainty: float
    quantum_delta: float
    gradcam_url: str
    original_url: str
    adaptive_views: Dict[DetailLevelEnum, AdaptivePersonaView]
    clinical_insights: List[str]
    model_limitations: List[str]
    disclaimer: str = "SIMULATED AI OUTPUT – RESEARCH AND CLINICAL DECISION SUPPORT ONLY. NOT A STANDALONE MEDICAL DIAGNOSIS."

class ChatEvidenceChip(BaseModel):
    region_id: str
    anatomical_location: str
    finding_relevance: str
    bounding_box: Optional[Dict[str, float]] = None

class AssistantMessage(BaseModel):
    sender: str
    content: str
    timestamp: str
    evidence_chips: Optional[List[ChatEvidenceChip]] = None
    suggested_followups: Optional[List[str]] = None

class AssistantQuestionRequest(BaseModel):
    scan_id: str
    modality: ModalityEnum
    question: str
    context_finding_id: Optional[str] = None
    history: Optional[List[Dict[str, str]]] = None

class DoctorReviewRequest(BaseModel):
    scan_id: str
    modality: ModalityEnum
    doctor_id: str
    doctor_role: str
    action: ReviewActionEnum
    rationale: str
    caliper_adjustments: Optional[Dict[str, Any]] = None
    corrected_diagnosis: Optional[str] = None

class DoctorReviewResponse(BaseModel):
    review_id: str
    scan_id: str
    status: str
    action: ReviewActionEnum
    immutable_audit_hash: str
    timestamp: str
    verified_by: str
    message: str

class QuantumSimulateRequest(BaseModel):
    modality: ModalityEnum
    n_qubits: int = Field(4, ge=2, le=8)
    circuit_depth: int = Field(3, ge=1, le=10)
    noise_level: float = Field(0.02, ge=0.0, le=0.2)
    use_zne_mitigation: bool = True

class QuantumSimulateResponse(BaseModel):
    qubits: int
    depth: int
    compressed_dimension: int
    bloch_vectors: List[Dict[str, float]]
    entropy: float
    purity: float
    unmitigated_accuracy: float
    mitigated_accuracy: float
    classical_baseline_accuracy: float
    quantum_advantage_delta: float
    circuit_latex: str
    backend_status: str

class EvaluationSummary(BaseModel):
    cohort_size: int
    doctor_alone: Dict[str, float]
    ai_alone: Dict[str, float]
    doctor_plus_ai: Dict[str, float]
    delta_accuracy: float
    delta_time_reduction_percent: float
    calibration_expected_vs_observed: List[Dict[str, float]]
    demographic_fairness: Dict[str, Any]
    scanner_robustness: Dict[str, Any]

# Phase 2 Verification & ABDM FHIR Models

class ReportVerificationRequest(BaseModel):
    report_id: str = Field(..., example="LC-2026-000412")
    report_payload_sha256: str = Field(..., example="7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069")
    canonical_string: Optional[str] = None

class ReportVerificationResponse(BaseModel):
    verified: bool
    computed_sha256: str
    received_sha256: str
    status: str
    message: str
    timestamp: str

class FHIRValidationRequest(BaseModel):
    fhir_bundle: Dict[str, Any]

class FHIRValidationResponse(BaseModel):
    is_valid: bool
    total_resources: int
    validated_resources: List[str]
    errors: List[str]
    warnings: List[str]
    schema_version: str = "HL7 FHIR R4 (v4.0.1)"

class ABDMConsentRequest(BaseModel):
    abha_id: str = Field(..., example="48-2910-4829-1920")
    hiu_id: str = Field("HIU-QM-DELHI-01", example="HIU-QM-DELHI-01")
    hip_id: str = Field("HIP-QM-091002", example="HIP-QM-091002")
    purpose: str = Field("CAREV", example="CAREV")
    expiry_date: str = Field("2027-11-09T23:59:59Z", example="2027-11-09T23:59:59Z")
    data_types: List[str] = Field(default_factory=lambda: ["DiagnosticReport", "Observation", "ImagingStudy"])

class ABDMConsentResponse(BaseModel):
    consent_id: str
    status: str
    artefact_id: str
    created_at: str
    expires_at: str
    message: str

class AuditVerifyRequest(BaseModel):
    blocks: List[Dict[str, Any]]

class AuditVerifyResponse(BaseModel):
    is_valid: bool
    total_blocks: int
    tampered_block_index: Optional[int] = None
    message: str
    verification_time_ms: float

