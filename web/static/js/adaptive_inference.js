/**
 * LensCode – Adaptive QuantaMed
 * Inference Provider Interface & Multi-Model Engine (Phase 2)
 */

(function (window) {
  'use strict';

  /**
   * Deterministic Rule-Based Inference Simulator
   * Maps extracted features (contrast, edge density, quadrant variance, ECG metrics)
   * into realistic clinical findings and confidence scores.
   */
  class RuleBasedSimulator {
    constructor() {
      this.name = "RuleBasedSimulator";
      this.provenance = "Rule-based simulation";
    }

    async infer(context) {
      const { modality, extractedFeatures, quality, patient } = context;

      // Seed deterministic generator with feature signature
      const seed = Math.abs(
        (extractedFeatures.edgeDensity * 1000) +
        (extractedFeatures.quadrantVariance * 10) +
        (quality.laplacianVariance)
      );

      let primaryDiagnosis = "";
      let severity = "Moderate";
      let confidence = 0.94;
      let uncertainty = 0.05;
      let findings = [];
      let measurements = {};

      if (modality === 'fundus') {
        // High quadrant variance indicates localized macula edema/exudates
        const hasSevereExudates = extractedFeatures.quadrantVariance > 25 || seed % 2 === 0;
        primaryDiagnosis = hasSevereExudates 
          ? "Moderate Non-Proliferative Diabetic Retinopathy (NPDR) with CSME"
          : "Mild Non-Proliferative Diabetic Retinopathy (NPDR)";
        severity = hasSevereExudates ? "Moderate-Severe" : "Mild";
        confidence = Number((0.92 + (seed % 60) * 0.001).toFixed(3));
        uncertainty = Number((1.0 - confidence).toFixed(3));

        measurements = {
          microaneurysmCount: Math.round(15 + (seed % 12)),
          hardExudateAreaMm2: Number((1.8 + (seed % 15) * 0.1).toFixed(2)),
          cupToDiscRatio: Number((0.42 + (seed % 10) * 0.01).toFixed(2)),
          fovealDistanceUm: Math.round(310 + (seed % 80))
        };

        findings = [
          {
            id: "FND-01",
            label: primaryDiagnosis,
            severity: severity,
            confidence: confidence,
            uncertainty: uncertainty,
            anatomicalSite: "Posterior Pole / Macula",
            measurements: measurements,
            coordinates: [{ x: 0.48, y: 0.52, radius: 0.14 }]
          },
          {
            id: "FND-02",
            label: "Clinically Significant Macular Edema (CSME)",
            severity: "High",
            confidence: Number((confidence - 0.03).toFixed(3)),
            uncertainty: Number((uncertainty + 0.03).toFixed(3)),
            anatomicalSite: "Foveal avascular zone margin",
            measurements: { fovealDistanceUm: measurements.fovealDistanceUm, ringDiameterUm: 720 },
            coordinates: [{ x: 0.54, y: 0.49, radius: 0.09 }]
          }
        ];
      } else if (modality === 'ecg') {
        const ecg = extractedFeatures.ecgMetrics || { hr: 76, stElevationMm: 3.8 };
        const hasSTEMI = ecg.stElevationMm >= 2.0;

        primaryDiagnosis = hasSTEMI 
          ? "Acute Anteroseptal ST-Elevation Myocardial Infarction (STEMI)"
          : (ecg.isArrhythmia ? "Atrial Fibrillation with Rapid Ventricular Response" : "Normal Sinus Rhythm with Non-Specific ST-T Changes");
        severity = hasSTEMI ? "Critical" : "Moderate";
        confidence = Number((0.95 + (seed % 40) * 0.001).toFixed(3));
        uncertainty = Number((1.0 - confidence).toFixed(3));

        measurements = {
          heartRateBpm: ecg.hr,
          stElevationV2Mm: ecg.stElevationMm,
          qrsDurationMs: ecg.qrsWidthMs || 94,
          rriSDNN: ecg.rriSDNN || 34.2,
          prIntervalMs: 164
        };

        findings = [
          {
            id: "ECG-01",
            label: primaryDiagnosis,
            severity: severity,
            confidence: confidence,
            uncertainty: uncertainty,
            anatomicalSite: "Left Anterior Descending (LAD) Territory • Leads V1-V4",
            measurements: measurements,
            coordinates: [{ x: 0.35, y: 0.50, radius: 0.20 }]
          }
        ];
      } else if (modality === 'oct') {
        primaryDiagnosis = "Subretinal Fluid & Pigment Epithelial Detachment (PED)";
        severity = "High";
        confidence = 0.962;
        uncertainty = 0.038;
        measurements = { centralSubfieldThicknessUm: 465, pedHeightUm: 210, intraretinalCysts: 4 };
        findings = [
          {
            id: "OCT-01",
            label: primaryDiagnosis,
            severity: severity,
            confidence: confidence,
            uncertainty: uncertainty,
            anatomicalSite: "Sub-foveal Neurosensory Retinal Layer",
            measurements: measurements,
            coordinates: [{ x: 0.50, y: 0.44, radius: 0.15 }]
          }
        ];
      } else if (modality === 'chest_xray') {
        primaryDiagnosis = "Right Upper Lobe Cavitary Consolidation consistent with Active Tuberculosis";
        severity = "High";
        confidence = 0.954;
        uncertainty = 0.046;
        measurements = { cavityDimensionCm: 2.8, wallThicknessMm: 4.5, pleuralThickening: "Present" };
        findings = [
          {
            id: "CXR-01",
            label: primaryDiagnosis,
            severity: severity,
            confidence: confidence,
            uncertainty: uncertainty,
            anatomicalSite: "Right Apical & Subapical Zone",
            measurements: measurements,
            coordinates: [{ x: 0.68, y: 0.28, radius: 0.16 }]
          }
        ];
      } else if (modality === 'breast_us') {
        primaryDiagnosis = "Hypoechoic Spiculated Mass (BI-RADS Category 5 - Highly Suspicious of Malignancy)";
        severity = "Critical";
        confidence = 0.938;
        uncertainty = 0.062;
        measurements = { majorAxisCm: 2.1, minorAxisCm: 1.6, tallerThanWideRatio: 1.31, acousticShadowing: "Posterior" };
        findings = [
          {
            id: "BUS-01",
            label: primaryDiagnosis,
            severity: severity,
            confidence: confidence,
            uncertainty: uncertainty,
            anatomicalSite: "Left Breast 2 o'clock position (Upper Outer Quadrant)",
            measurements: measurements,
            coordinates: [{ x: 0.42, y: 0.48, radius: 0.18 }]
          }
        ];
      } else {
        // Head CT
        primaryDiagnosis = "Early Acute Ischemic Infarction (Left MCA Territory, Loss of Insular Ribbon)";
        severity = "Emergency";
        confidence = 0.942;
        uncertainty = 0.058;
        measurements = { aspectsScore: 7, sulcalEffacement: "Moderate", midlineShiftMm: 1.2 };
        findings = [
          {
            id: "HCT-01",
            label: primaryDiagnosis,
            severity: severity,
            confidence: confidence,
            uncertainty: uncertainty,
            anatomicalSite: "Left Middle Cerebral Artery (MCA) Territory",
            measurements: measurements,
            coordinates: [{ x: 0.38, y: 0.46, radius: 0.17 }]
          }
        ];
      }

      return {
        provider: this.name,
        provenance: this.provenance,
        primaryDiagnosis,
        severity,
        confidence,
        uncertainty,
        quantumDelta: 4.8,
        findings,
        measurements,
        timestamp: new Date().toISOString(),
        disclaimer: "SIMULATED AI OUTPUT – RESEARCH & DECISION SUPPORT ONLY. NOT A STANDALONE MEDICAL DIAGNOSIS."
      };
    }
  }

  /**
   * Grounded Gemini LLM Provider
   * Sends ONLY anonymized feature metrics and clinical context (NEVER PII or raw bytes)
   * to provide structured clinical reasoning.
   */
  class GeminiProvider {
    constructor(apiKey = "") {
      this.name = "GeminiProvider";
      this.provenance = "LLM-assisted (grounded Gemini)";
      this.apiKey = apiKey;
    }

    async infer(context) {
      const { modality, extractedFeatures, quality, patient } = context;

      // Check if API key is configured
      if (!this.apiKey) {
        console.warn("Gemini API key not configured. Falling back to RuleBasedSimulator.");
        const fallback = new RuleBasedSimulator();
        const res = await fallback.infer(context);
        res.provenance = "Rule-based simulation (Gemini API Key missing in Settings)";
        return res;
      }

      const prompt = `You are a clinical decision-support reasoning engine adhering strictly to SaMD Class IIa standards.
You are given quantitative feature measurements from a medical scan. You must NOT provide a definitive diagnosis or replace physician judgment.
Instead, summarize findings, confidence, and calibrated uncertainty in structured JSON format.

Patient Age: ${patient.age}, Gender: ${patient.gender}
Clinical History: ${patient.history}
Modality: ${modality}
Quality Metrics: Laplacian Sharpness ${quality.laplacianVariance}, Contrast ${quality.contrast}, Mean Exposure ${quality.brightness}
Extracted Features: Edge Density ${extractedFeatures.edgeDensity}, Spatial Variance ${extractedFeatures.quadrantVariance}

Respond ONLY with valid JSON conforming to this schema:
{
  "primaryDiagnosis": "Diagnostic Impression (e.g. Moderate NPDR / STEMI)",
  "severity": "Mild | Moderate | High | Critical",
  "confidence": 0.94,
  "uncertainty": 0.06,
  "quantumDelta": 4.8,
  "findings": [
    {
      "id": "FND-01",
      "label": "Finding description",
      "severity": "Severity",
      "confidence": 0.94,
      "uncertainty": 0.06,
      "anatomicalSite": "Anatomical location",
      "measurements": {"metric": "value"}
    }
  ],
  "limitations": ["Limitation 1", "Limitation 2"]
}`;

      try {
        const response = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${this.apiKey}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: prompt }] }],
              generationConfig: { responseMimeType: "application/json" }
            })
          }
        );

        if (!response.ok) {
          throw new Error(`Gemini API error: ${response.status}`);
        }

        const data = await response.json();
        const text = data.candidates[0].content.parts[0].text;
        const parsed = JSON.parse(text);

        return {
          provider: this.name,
          provenance: this.provenance,
          primaryDiagnosis: parsed.primaryDiagnosis,
          severity: parsed.severity || "Moderate",
          confidence: parsed.confidence || 0.92,
          uncertainty: parsed.uncertainty || 0.08,
          quantumDelta: parsed.quantumDelta || 4.8,
          findings: parsed.findings || [],
          measurements: parsed.findings[0]?.measurements || {},
          limitations: parsed.limitations || [],
          timestamp: new Date().toISOString(),
          disclaimer: "LLM-ASSISTED CLINICAL DECISION SUPPORT – GROUNDED FEATURE REASONING. NOT A STANDALONE DIAGNOSIS."
        };
      } catch (err) {
        console.error("Gemini API inference error:", err);
        const fallback = new RuleBasedSimulator();
        const res = await fallback.infer(context);
        res.provenance = "Rule-based simulation (Gemini API query failed)";
        return res;
      }
    }
  }

  /**
   * Backend Provider
   * Dispatches inferencing to local FastAPI or Flask endpoints
   */
  class BackendProvider {
    constructor(baseUrl = "") {
      this.name = "BackendProvider";
      this.provenance = "Backend model v2.0 (FastAPI)";
      this.baseUrl = baseUrl;
    }

    async infer(context) {
      const { modality, detailLevel = "standard" } = context;
      try {
        const response = await fetch(`${this.baseUrl}/api/adaptive/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            modality: modality,
            detail_level: detailLevel
          })
        });

        if (!response.ok) throw new Error(`Backend error: ${response.status}`);
        const data = await response.json();

        return {
          provider: this.name,
          provenance: this.provenance,
          primaryDiagnosis: data.primary_diagnosis,
          severity: data.findings[0]?.severity || "Moderate",
          confidence: data.overall_confidence,
          uncertainty: data.overall_uncertainty,
          quantumDelta: data.quantum_delta,
          findings: data.findings,
          measurements: data.findings[0]?.measurements || {},
          timestamp: data.timestamp,
          disclaimer: data.disclaimer
        };
      } catch (err) {
        console.warn("Backend API unavailable, using RuleBasedSimulator:", err);
        const fallback = new RuleBasedSimulator();
        const res = await fallback.infer(context);
        res.provenance = "Rule-based simulation (Backend server fallback)";
        return res;
      }
    }
  }

  // Factory selector
  class InferenceManager {
    getProvider(providerName, settings = {}) {
      if (providerName === 'GeminiProvider') {
        return new GeminiProvider(settings.geminiApiKey || "");
      } else if (providerName === 'BackendProvider') {
        return new BackendProvider("");
      }
      return new RuleBasedSimulator();
    }
  }

  window.InferenceManager = new InferenceManager();
  window.RuleBasedSimulator = RuleBasedSimulator;
  window.GeminiProvider = GeminiProvider;
  window.BackendProvider = BackendProvider;

})(window);
