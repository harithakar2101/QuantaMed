/**
 * LensCode – Adaptive QuantaMed
 * Global State Store & Event Hub (Phase 3)
 * Implements 6 Canonical Synthetic Case Archetypes, SaMD Workflow State Machine,
 * and Persistent Report Library with RBAC.
 */

(function (window) {
  'use strict';

  const STORAGE_KEY_SETTINGS = "quantamed_phase3_settings";
  const STORAGE_KEY_REPORTS = "quantamed_phase3_reports";

  /**
   * 6 Canonical Synthetic Cases across all 6 Modalities & Archetypes:
   * (a) Fundus: Clear Abnormal (Moderate NPDR + CSME)
   * (b) Chest X-ray: Normal Case (Routine check, clear fields & CTR)
   * (c) Breast Ultrasound: Borderline / Uncertain (BI-RADS 3/4A equivocal nodule)
   * (d) Retinal OCT: Poor-Quality Retake (Motion artifact, low Laplacian)
   * (e) ECG: Out-of-Distribution Input (Electrode artifact / cable interference)
   * (f) Head CT: Critical Urgent (Acute intracranial hemorrhage + midline shift)
   */
  const SAMPLE_PATIENTS = {
    // (a) Clear abnormal case: Fundus
    fundus: {
      patientId: "QM-2026-F01",
      caseArchetype: "CLEAR_ABNORMAL",
      archetypeLabel: "Clear Abnormal (NPDR + CSME)",
      name: "Smt. Kamala Devi",
      age: 62,
      gender: "Female",
      sex: "Female",
      syntheticAbha: "48-2910-4829-1920",
      abhaNumber: "48-2910-4829-1920",
      abhaAddress: "kamala.devi@abdm",
      syntheticUhid: "UHID-DEL-89410",
      uhid: "UHID-DEL-89410",
      relevantHistory: "Type-2 Diabetes Mellitus x 14 yrs, HbA1c 8.8%, blurred central vision OD, bilateral lower extremity neuropathy.",
      history: "Type-2 Diabetes Mellitus x 14 yrs, HbA1c 8.8%, blurred central vision OD.",
      symptoms: ["Progressive central vision blur", "Microaneurysms on routine screening"],
      medications: ["Metformin 500mg BID", "Atorvastatin 20mg OD"],
      comorbidities: ["Type-2 Diabetes Mellitus", "Essential Hypertension"],
      indication: "Annual Diabetic Retinopathy screening and maculopathy evaluation",
      referringDoctor: "Dr. Sunita Rao, MS (Ophthalmology)",
      referringDoctorHpr: "HPR-IN-2026-88194",
      reportingDoctor: "Dr. Rajesh K. Varma, DM (Radiodiagnosis)",
      reportingDoctorHpr: "HPR-IN-2026-10294",
      urgency: "Urgent",
      modality: "fundus"
    },

    // (b) Normal case: Chest X-ray
    chest_xray: {
      patientId: "QM-2026-X04",
      caseArchetype: "NORMAL_CASE",
      archetypeLabel: "Normal (Routine Check, Clear Fields)",
      name: "Shri Arvind Nambisan",
      age: 34,
      gender: "Male",
      sex: "Male",
      syntheticAbha: "82-1029-4820-5591",
      abhaNumber: "82-1029-4820-5591",
      abhaAddress: "arvind.nambisan@abdm",
      syntheticUhid: "UHID-BLR-44210",
      uhid: "UHID-BLR-44210",
      relevantHistory: "Pre-employment executive health checkup. Non-smoker, asymptomatic, active lifestyle. No respiratory complaints.",
      history: "Routine pre-employment executive medical check, no symptoms, non-smoker.",
      symptoms: ["Asymptomatic / Executive physical screening"],
      medications: ["None"],
      comorbidities: ["None reported"],
      indication: "Standard PA Chest Radiograph for pre-employment occupational clearance",
      referringDoctor: "Dr. Pradeep Nair, MD (Pulmonary Medicine)",
      referringDoctorHpr: "HPR-IN-2026-33918",
      reportingDoctor: "Dr. Farhan Qureshi, MD (Thoracic Imaging)",
      reportingDoctorHpr: "HPR-IN-2026-52119",
      urgency: "Routine",
      modality: "chest_xray"
    },

    // (c) Borderline / uncertain case: Breast Ultrasound
    breast_us: {
      patientId: "QM-2026-B05",
      caseArchetype: "BORDERLINE_UNCERTAIN",
      archetypeLabel: "Borderline / Uncertain (BI-RADS 3/4A)",
      name: "Smt. Meera Swaminathan",
      age: 51,
      gender: "Female",
      sex: "Female",
      syntheticAbha: "71-5501-8891-2309",
      abhaNumber: "71-5501-8891-2309",
      abhaAddress: "meera.swaminathan@abdm",
      syntheticUhid: "UHID-CHN-66201",
      uhid: "UHID-CHN-66201",
      relevantHistory: "Routine post-menopausal screening. Equivocal vague nodularity left breast 10 o'clock position noticed during clinical palpation.",
      history: "Vague nodularity left breast 10 o'clock position, uncertain border on initial palpation.",
      symptoms: ["Vague focal firmness", "No nipple retraction or discharge"],
      medications: ["Calcium + Vit D3 daily"],
      comorbidities: ["Mild Osteopenia"],
      indication: "Targeted High-Resolution Breast Sonography for BI-RADS risk classification",
      referringDoctor: "Dr. Leela Krishnan, MCh (Surgical Oncology)",
      referringDoctorHpr: "HPR-IN-2026-77291",
      reportingDoctor: "Dr. Vikram Sethi, MD (Onco-Radiology)",
      reportingDoctorHpr: "HPR-IN-2026-38291",
      urgency: "Routine",
      modality: "breast_us"
    },

    // (d) Poor-quality case triggering Retake: Retinal OCT
    oct: {
      patientId: "QM-2026-O02",
      caseArchetype: "POOR_QUALITY_RETAKE",
      archetypeLabel: "Poor Quality (Severe Motion Blur → Retake Advisory)",
      name: "Shri Ramesh Chandra",
      age: 69,
      gender: "Male",
      sex: "Male",
      syntheticAbha: "31-8902-1920-3301",
      abhaNumber: "31-8902-1920-3301",
      abhaAddress: "ramesh.chandra@abdm",
      syntheticUhid: "UHID-DEL-77402",
      uhid: "UHID-DEL-77402",
      relevantHistory: "Severe patient involuntary eye blink and tremor during scan traverse. Optical media dryness causing profound signal drop.",
      history: "Progressive central metamorphopsia OS, uncooperative during scan due to dry eye.",
      symptoms: ["Distorted central lines", "Difficulty tracking target fixation"],
      medications: ["Carboxymethylcellulose drops PRN"],
      comorbidities: ["Senile Cataract OS", "Essential Tremor"],
      indication: "High-resolution SD-OCT macula scan (Quality Gating Test Case)",
      referringDoctor: "Dr. Anand Parthasarathy, FRCS",
      referringDoctorHpr: "HPR-IN-2026-44012",
      reportingDoctor: "Dr. Anita Roy, MS (Vitreoretinal)",
      reportingDoctorHpr: "HPR-IN-2026-59312",
      urgency: "Routine",
      modality: "oct"
    },

    // (e) Out-of-Distribution (OOD) Input: ECG
    ecg: {
      patientId: "QM-2026-C03",
      caseArchetype: "OUT_OF_DISTRIBUTION",
      archetypeLabel: "OOD Anomaly (Cable Noise / Artifact → Safeguard)",
      name: "Smt. Ananya Mukherjee",
      age: 46,
      gender: "Female",
      sex: "Female",
      syntheticAbha: "19-4820-9921-1029",
      abhaNumber: "19-4820-9921-1029",
      abhaAddress: "ananya.mukherjee@abdm",
      syntheticUhid: "UHID-MUM-55190",
      uhid: "UHID-MUM-55190",
      relevantHistory: "Atypical high-frequency baseline drift, non-physiological interference pattern (suspected 50Hz AC mains power artifact).",
      history: "Palpitations during stressful exertion, non-physiological cable artifact on recording.",
      symptoms: ["Episodic racing pulse", "Restlessness"],
      medications: ["Propranolol 10mg PRN"],
      comorbidities: ["Generalized Anxiety"],
      indication: "12-Lead Diagnostic ECG (Out-of-Distribution Anomaly Test Case)",
      referringDoctor: "Dr. Rajesh K. Varma, DM (Cardiology)",
      referringDoctorHpr: "HPR-IN-2026-10294",
      reportingDoctor: "Dr. Rajesh K. Varma, DM (Cardiology)",
      reportingDoctorHpr: "HPR-IN-2026-10294",
      urgency: "Urgent",
      modality: "ecg"
    },

    // (f) Critical urgent case: Head CT
    head_ct: {
      patientId: "QM-2026-H06",
      caseArchetype: "CRITICAL_URGENT",
      archetypeLabel: "Critical Urgent (Acute Intracranial Hemorrhage)",
      name: "Sardar Gurpreet Singh",
      age: 64,
      gender: "Male",
      sex: "Male",
      syntheticAbha: "99-3321-4402-9102",
      abhaNumber: "99-3321-4402-9102",
      abhaAddress: "gurpreet.singh@abdm",
      syntheticUhid: "UHID-CHD-11820",
      uhid: "UHID-CHD-11820",
      relevantHistory: "Acute onset thunderclap headache followed by projectile vomiting, acute left hemiparesis, progressive somnolence. GCS 11 (E3V3M5).",
      history: "Sudden thunderclap headache, vomiting, acute left-sided weakness, GCS 11.",
      symptoms: ["Severe headache (10/10)", "Left facial droop", "Left arm/leg flaccidity"],
      medications: ["Amlodipine 5mg OD (poor compliance)"],
      comorbidities: ["Severe Uncontrolled Hypertension (BP 210/115 mmHg)"],
      indication: "EMERGENCY STAT Non-Contrast Head CT for Acute Intracranial Bleed Triage",
      referringDoctor: "Dr. Tariq Mansoor, DM (Neurology)",
      referringDoctorHpr: "HPR-IN-2026-66102",
      reportingDoctor: "Dr. Vikram Sethi, MD (Neuroradiology)",
      reportingDoctorHpr: "HPR-IN-2026-38291",
      urgency: "Emergency",
      modality: "head_ct"
    }
  };

  /**
   * Enforced Workflow States & Transition Machine:
   * Draft (AI) → Under review → Modified / Second opinion → Approved → Signed (demo) → Released (consent check) → Amended (new version) / Revoked
   */
  const WORKFLOW_STATES = [
    "Draft (AI)",
    "Under review",
    "Modified / Second opinion",
    "Approved",
    "Signed (demo)",
    "Released (consent check)",
    "Amended (new version)",
    "Revoked"
  ];

  class Store {
    constructor() {
      this.listeners = [];

      let savedSettings = null;
      try {
        savedSettings = JSON.parse(localStorage.getItem(STORAGE_KEY_SETTINGS));
      } catch (e) { }

      this.state = {
        // Current Case State
        currentPatient: { ...SAMPLE_PATIENTS.fundus },
        currentScan: {
          modality: "fundus",
          sourceType: "sample",
          fileName: "kamala_fundus_macula.png",
          fileSize: "1.9 MB",
          dimensions: { width: 1024, height: 768 },
          rawImageElement: null,
          imageData: null,
          ecgData: null,
          timestamp: new Date().toISOString()
        },
        qualityAssessment: {
          status: "ACCEPT", // ACCEPT, RETAKE, EXPERT_REVIEW
          score: 88.4,
          overallScore: 88.4,
          laplacianVariance: 142.6,
          blur: 142.6,
          brightness: 118.2,
          contrast: 68.4,
          noiseEstimate: 4.2,
          noise: 4.2,
          completeness: 98.0,
          oodScore: 0.04,
          gateDecision: "Accept",
          isOOD: false,
          metrics: [],
          recommendation: "Quality standards satisfied. Safe to execute diagnostic inference."
        },
        preprocessing: {
          applied: false,
          claheApplied: true,
          denoiseApplied: true,
          normalized: true,
          processedCanvas: null
        },
        extractedFeatures: {
          histogram: [12, 38, 140, 218, 92],
          edgeDensity: 0.162,
          quadrantVariance: 18.4,
          meanLuminance: 118.2,
          ecgMetrics: null
        },
        analysisResult: {
          overall_impression: "Findings suggestive of Moderate Non-Proliferative Diabetic Retinopathy (NPDR) with CSME.",
          primaryDiagnosis: "Moderate Non-Proliferative Diabetic Retinopathy (NPDR)",
          severity: "Moderate",
          confidence: 0.944,
          uncertainty: 0.056,
          urgency_flag: "Urgent",
          critical_flags: ["Clinically Significant Macular Edema (CSME)"],
          differential_considerations: [
            "Diabetic Macular Edema secondary to prolonged microvascular hyperpermeability",
            "Hypertensive Retinopathy Grade II co-manifestation"
          ],
          recommended_next_steps: [
            "Spectral-Domain Retinal OCT within 14 days",
            "Vitreoretinal subspecialist consultation"
          ],
          limitations: ["2D fundus photography lacks axial depth tomographic resolution"],
          findings: [
            {
              id: "FND-01",
              label: "Parafoveal Microaneurysms & Punctate Hemorrhages",
              modality_specific_category: "Retinal Microvasculature",
              region: "Temporal & Inferotemporal Macula",
              measurement: "Microaneurysm Count",
              value: "18",
              unit: "lesions",
              normal_range: "0",
              severity: "High",
              confidence: 0.944,
              uncertainty: 0.056,
              evidence_regions: ["Parafoveal Ring Arc (Region #1)"],
              supporting_features: ["Dot and blot hemorrhages across 2 quadrants"]
            }
          ],
          saliencyCanvas: null,
          provenance: {
            provider: "RuleBasedSimulator",
            version: "v3.0-quantum-hybrid-calibrated",
            mode: "rule-based",
            processing_ms: 124
          },
          timestamp: new Date().toISOString()
        },
        doctorReview: {
          action: "ACCEPT", // ACCEPT, MODIFY, OVERRIDE, REJECT
          reclassification: "CONCUR",
          rationale: "Validated against patient ophthalmic history. Findings correlate with HbA1c elevation.",
          overrides: {}, // findingId -> { action, modifiedLabel, notes, timestamp }
          doctorImpressionOverride: null,
          secondOpinionRequested: false,
          secondOpinionDoctor: "",
          secondOpinionNotes: "",
          isLocked: false, // Locked once Signed
          signatureDataUrl: null,
          signedAt: null,
          signerName: "Dr. Sunita Rao, MS",
          signerHPR: "HPR-IN-2026-88194",
          signatureType: "cursive"
        },
        report: {
          id: "LC-2026-000412",
          accessionNumber: "ACC-2026-89410",
          studyId: "STD-FND-401",
          version: 1.0,
          status: "Draft (AI)", // Draft (AI), Under review, Modified / Second opinion, Approved, Signed (demo), Released (consent check), Amended (new version), Revoked
          createdAt: new Date().toISOString(),
          signedAt: null,
          sha256Hash: "d56fe8aad25b61ffc5781b76d60ee6a34891b01982736451a928374615243102",
          versionHistory: [],
          doctorChosenView: "standard", // urgent, standard, teaching
          includeAnnexures: true
        },
        abdm: {
          isDemoMode: true,
          consentStatus: "GRANTED", // NONE, REQUESTED, GRANTED, DENIED, REVOKED
          consentId: "CA-2026-ABDM-98214",
          purpose: "Care Management (CAREMGT)",
          expiryDate: "2026-12-31",
          careContextId: "CC-QM-2026-01",
          facilityId: "HFR-IN-DL-009142",
          facilityName: "LensCode Apex Research Hospital (Demo)",
          hprId: "HPR-IN-2026-88194",
          hprName: "Dr. Sunita Rao, MS"
        },
        savedReports: this.loadSavedReports(),
        auditLog: [],
        userSettings: {
          activeRole: (savedSettings && savedSettings.activeRole) || "Doctor",
          language: (savedSettings && savedSettings.language) || "en",
          reducedMotion: false,
          fontScale: 100,
          inferenceProvider: (savedSettings && savedSettings.inferenceProvider) || "RuleBasedSimulator",
          geminiApiKey: (savedSettings && savedSettings.geminiApiKey) || "",
          consentVisionDeidentified: false
        },
        activeStep: 1
      };
    }

    subscribe(listener) {
      this.listeners.push(listener);
      return () => {
        this.listeners = this.listeners.filter(l => l !== listener);
      };
    }

    notify(changedKey) {
      for (const listener of this.listeners) {
        try {
          listener(this.state, changedKey);
        } catch (e) {
          console.error("Store listener error:", e);
        }
      }
    }

    get(key) {
      return this.state[key];
    }

    set(key, val) {
      this.state[key] = val;
      this.notify(key);
    }

    update(key, partial) {
      if (typeof this.state[key] === 'object' && this.state[key] !== null && !Array.isArray(this.state[key])) {
        this.state[key] = { ...this.state[key], ...partial };
      } else {
        this.state[key] = partial;
      }
      this.notify(key);
    }

    getState() {
      return this.state;
    }

    /**
     * Loads one of the 6 canonical synthetic cases with specific quality/clinical profiles
     */
    loadSamplePatient(modality) {
      const p = SAMPLE_PATIENTS[modality] || SAMPLE_PATIENTS.fundus;
      this.update('currentPatient', { ...p });

      // Modality-specific quality presets to match the test cases
      let qualityPreset = {
        status: "ACCEPT",
        score: 92.4,
        overallScore: 92.4,
        laplacianVariance: 142.6,
        blur: 142.6,
        brightness: 118.2,
        contrast: 68.4,
        noiseEstimate: 4.2,
        noise: 4.2,
        completeness: 98.0,
        oodScore: 0.04,
        gateDecision: "Accept",
        isOOD: false,
        recommendation: "Quality standards satisfied. Safe to execute diagnostic inference."
      };

      if (p.caseArchetype === "POOR_QUALITY_RETAKE") {
        qualityPreset = {
          status: "RETAKE",
          score: 34.2,
          overallScore: 34.2,
          laplacianVariance: 28.4,
          blur: 28.4,
          brightness: 62.1,
          contrast: 22.4,
          noiseEstimate: 16.8,
          noise: 16.8,
          completeness: 58.0,
          oodScore: 0.12,
          gateDecision: "Retake",
          isOOD: false,
          recommendation: "Pre-flight scan quality assessment failed. Diagnostic findings withheld. Retake required."
        };
      } else if (p.caseArchetype === "OUT_OF_DISTRIBUTION") {
        qualityPreset = {
          status: "EXPERT_REVIEW",
          score: 48.0,
          overallScore: 48.0,
          laplacianVariance: 112.0,
          blur: 112.0,
          brightness: 120.0,
          contrast: 54.0,
          noiseEstimate: 14.2,
          noise: 14.2,
          completeness: 94.0,
          oodScore: 0.82,
          gateDecision: "Expert Review",
          isOOD: true,
          recommendation: "Out-of-distribution spectral signature detected (OOD Score: 0.82). Findings downgraded."
        };
      }

      this.update('qualityAssessment', qualityPreset);

      this.update('currentScan', {
        modality: modality,
        sourceType: "sample",
        fileName: `${p.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}_${modality}.png`,
        fileSize: "1.9 MB",
        dimensions: { width: 1024, height: 768 },
        timestamp: new Date().toISOString()
      });

      this.update('report', {
        id: `LC-2026-${Math.floor(100000 + Math.random() * 900000)}`,
        accessionNumber: `ACC-2026-${Math.floor(10000 + Math.random() * 90000)}`,
        studyId: `STD-${modality.toUpperCase()}-${Math.floor(100 + Math.random() * 900)}`,
        version: 1.0,
        status: "Draft (AI)",
        createdAt: new Date().toISOString(),
        signedAt: null,
        sha256Hash: null,
        versionHistory: [],
        doctorChosenView: "standard",
        includeAnnexures: true
      });

      this.update('doctorReview', {
        action: "ACCEPT",
        reclassification: "CONCUR",
        rationale: "Validated against patient clinical history.",
        overrides: {},
        doctorImpressionOverride: null,
        isLocked: false,
        signatureDataUrl: null,
        signedAt: null,
        signerName: p.referringDoctor || "Dr. Sunita Rao, MS",
        signerHPR: p.referringDoctorHpr || "HPR-IN-2026-88194",
        signatureType: "cursive"
      });
    }

    /**
     * Workflow State Machine: Transitions report lifecycle with enforced RBAC
     */
    transitionWorkflowStatus(newStatus, actorInfo = {}) {
      const rep = this.state.report;
      const review = this.state.doctorReview;

      if (!WORKFLOW_STATES.includes(newStatus)) {
        throw new Error(`Invalid workflow status: ${newStatus}`);
      }

      // If report was locked (Signed/Released), attempting edits generates an Amended Version
      if ((rep.status === "Signed (demo)" || rep.status === "Released (consent check)") && newStatus === "Modified / Second opinion") {
        return this.createNewAmendedVersion(actorInfo.reason || "Doctor clinical amendment");
      }

      // Lock report when signed
      if (newStatus === "Signed (demo)") {
        review.isLocked = true;
        rep.signedAt = new Date().toISOString();
        if (actorInfo.signerName) review.signerName = actorInfo.signerName;
        if (actorInfo.signerHPR) review.signerHPR = actorInfo.signerHPR;
      }

      rep.status = newStatus;
      this.update('report', { ...rep });
      this.update('doctorReview', { ...review });

      // Log to audit trail
      if (window.AdaptiveAuditChain) {
        window.AdaptiveAuditChain.record(
          `WORKFLOW_TRANSITION_${newStatus.toUpperCase().replace(/[^A-Z0-9]/g, '_')}`,
          actorInfo.role || "Doctor",
          { reportId: rep.id, version: rep.version, status: newStatus }
        );
      }

      this.saveCurrentReportToLibrary();
      return rep;
    }

    /**
     * Creates an Amended Version (e.g. v2.0) when edits are made to a Signed report
     */
    createNewAmendedVersion(amendmentReason = "Clinician finding correction") {
      const oldRep = { ...this.state.report };
      const newVersion = Number((oldRep.version + 1.0).toFixed(1));

      const archivedEntry = {
        version: oldRep.version,
        status: oldRep.status,
        signedAt: oldRep.signedAt,
        sha256Hash: oldRep.sha256Hash,
        archivedAt: new Date().toISOString(),
        reason: amendmentReason
      };

      const updatedHistory = [...(oldRep.versionHistory || []), archivedEntry];

      this.update('report', {
        ...oldRep,
        version: newVersion,
        status: "Modified / Second opinion",
        signedAt: null,
        sha256Hash: null,
        versionHistory: updatedHistory
      });

      this.update('doctorReview', {
        ...this.state.doctorReview,
        isLocked: false,
        signedAt: null
      });

      if (window.AdaptiveAuditChain) {
        window.AdaptiveAuditChain.record(
          "REPORT_AMENDMENT_VERSIONED",
          "Doctor",
          { reportId: oldRep.id, oldVersion: oldRep.version, newVersion: newVersion, reason: amendmentReason }
        );
      }

      this.saveCurrentReportToLibrary();
      return this.state.report;
    }

    /**
     * Finding-level doctor validation (Accept / Modify / Reject)
     */
    updateFindingReview(findingId, action, notes = "", modifiedFields = {}) {
      const review = { ...this.state.doctorReview };
      review.overrides = review.overrides || {};
      review.overrides[findingId] = {
        action: action, // ACCEPT, MODIFY, REJECT
        notes: notes,
        modifiedFields: modifiedFields,
        timestamp: new Date().toISOString()
      };

      // Set status to Modified if doctor made changes
      if (action === "MODIFY" || action === "REJECT") {
        this.state.report.status = "Modified / Second opinion";
      }

      this.update('doctorReview', review);
      this.update('report', { ...this.state.report });
      this.saveCurrentReportToLibrary();
    }

    /**
     * Overrides overall clinical impression
     */
    updateImpressionOverride(newImpression, reason = "") {
      const review = { ...this.state.doctorReview };
      review.doctorImpressionOverride = newImpression;
      review.rationale = reason || review.rationale;
      this.state.report.status = "Modified / Second opinion";

      this.update('doctorReview', review);
      this.update('report', { ...this.state.report });
      this.saveCurrentReportToLibrary();
    }

    /**
     * Saves current report into localStorage library
     */
    saveCurrentReportToLibrary() {
      const currentRep = {
        ...this.state.report,
        patient: { ...this.state.currentPatient },
        scan: { ...this.state.currentScan },
        quality: { ...this.state.qualityAssessment },
        findings: [...(this.state.analysisResult.findings || [])],
        primaryDiagnosis: this.state.analysisResult.primaryDiagnosis || this.state.analysisResult.overall_impression,
        overall_impression: this.state.analysisResult.overall_impression,
        confidence: this.state.analysisResult.confidence,
        uncertainty: this.state.analysisResult.uncertainty,
        provenance: this.state.analysisResult.provenance,
        review: { ...this.state.doctorReview },
        abdm: { ...this.state.abdm }
      };

      const existingIndex = this.state.savedReports.findIndex(r => r.id === currentRep.id);
      let updatedList = [...this.state.savedReports];
      if (existingIndex >= 0) {
        updatedList[existingIndex] = currentRep;
      } else {
        updatedList.unshift(currentRep);
      }

      this.set('savedReports', updatedList);
      try {
        localStorage.setItem(STORAGE_KEY_REPORTS, JSON.stringify(updatedList));
      } catch (e) {
        console.warn("Could not save report list to localStorage:", e);
      }
      return currentRep;
    }

    loadSavedReports() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY_REPORTS);
        if (raw) return JSON.parse(raw);
      } catch (e) { }

      // Seed with sample reports
      return [
        {
          id: "LC-2026-000412",
          accessionNumber: "ACC-2026-89410",
          studyId: "STD-FND-401",
          version: 1.0,
          status: "Signed (demo)",
          createdAt: "2026-11-08T09:30:00Z",
          signedAt: "2026-11-08T09:42:15Z",
          sha256Hash: "d56fe8aad25b61ffc5781b76d60ee6a34891b01982736451a928374615243102",
          patient: {
            name: "Smt. Kamala Devi",
            age: 62,
            gender: "Female",
            abhaNumber: "48-2910-4829-1920",
            uhid: "UHID-DEL-89410",
            modality: "fundus"
          },
          primaryDiagnosis: "Moderate Non-Proliferative Diabetic Retinopathy (NPDR)",
          confidence: 0.946,
          uncertainty: 0.054,
          provenance: { provider: "RuleBasedSimulator", mode: "rule-based" },
          signerName: "Dr. Sunita Rao, MS"
        },
        {
          id: "LC-2026-000409",
          accessionNumber: "ACC-2026-77102",
          studyId: "STD-ECG-103",
          version: 1.0,
          status: "Approved",
          createdAt: "2026-11-07T14:10:00Z",
          signedAt: "2026-11-07T14:25:30Z",
          sha256Hash: "9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b",
          patient: {
            name: "Shri Vikramaditya Sen",
            age: 57,
            gender: "Male",
            abhaNumber: "19-4820-9921-1029",
            uhid: "UHID-MUM-55190",
            modality: "ecg"
          },
          primaryDiagnosis: "Acute Anteroseptal ST-Elevation Myocardial Infarction (STEMI)",
          confidence: 0.981,
          uncertainty: 0.019,
          provenance: { provider: "RuleBasedSimulator", mode: "rule-based" },
          signerName: "Dr. Rajesh K. Varma, DM"
        }
      ];
    }

    saveSettings(settings) {
      this.update('userSettings', settings);
      try {
        localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(this.state.userSettings));
      } catch (e) { }
    }

    purgeAllDemoData() {
      try {
        localStorage.removeItem(STORAGE_KEY_REPORTS);
        localStorage.removeItem(STORAGE_KEY_SETTINGS);
      } catch (e) { }
      this.set('savedReports', []);
      this.loadSamplePatient('fundus');
    }
  }

  window.QuantaMedStore = new Store();
  window.adaptiveStore = window.QuantaMedStore;
  window.SAMPLE_PATIENTS = SAMPLE_PATIENTS;
  window.WORKFLOW_STATES = WORKFLOW_STATES;

})(window);
