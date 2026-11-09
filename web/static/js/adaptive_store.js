/**
 * LensCode – Adaptive QuantaMed
 * Global State Store & Event System (Phase 2 Enhancement)
 */

(function (window) {
  'use strict';

  const STORAGE_KEY_REPORTS = 'quantamed_saved_reports_v2';
  const STORAGE_KEY_AUDIT = 'quantamed_audit_chain_v2';
  const STORAGE_KEY_SETTINGS = 'quantamed_user_settings_v2';

  // Seed data for quick loading
  const SAMPLE_PATIENTS = {
    fundus: {
      patientId: "QM-2026-F01",
      name: "Smt. Kamala Devi",
      age: 62,
      gender: "Female",
      abhaNumber: "48-2910-4829-1920",
      abhaAddress: "kamala.devi@abdm",
      uhid: "UHID-DEL-89410",
      history: "Type-2 Diabetes Mellitus x 14 yrs, HbA1c 8.8%, blurred central vision OD, bilateral lower extremity neuropathy.",
      indication: "Annual Diabetic Retinopathy screening and maculopathy evaluation",
      referringDoctor: "Dr. Sunita Rao, MS (Ophthalmology)",
      modality: "fundus"
    },
    oct: {
      patientId: "QM-2026-O02",
      name: "Shri Ramesh Chandra",
      age: 69,
      gender: "Male",
      abhaNumber: "31-8902-1920-3301",
      abhaAddress: "ramesh.chandra@abdm",
      uhid: "UHID-DEL-77402",
      history: "Progressive central metamorphopsia OS x 3 months, difficulty reading small print, no ocular trauma.",
      indication: "High-resolution SD-OCT macula B-scan for subretinal fluid assessment",
      referringDoctor: "Dr. Anand Parthasarathy, FRCS",
      modality: "oct"
    },
    ecg: {
      patientId: "QM-2026-C03",
      name: "Shri Vikramaditya Sen",
      age: 57,
      gender: "Male",
      abhaNumber: "19-4820-9921-1029",
      abhaAddress: "vikram.sen@abdm",
      uhid: "UHID-MUM-55190",
      history: "Sudden onset retrosternal crushing chest pain radiating to left shoulder and jaw x 45 min, diaphoresis, dyspnea.",
      indication: "Emergency 12-lead ECG evaluation for acute coronary syndrome triage",
      referringDoctor: "Dr. Rajesh K. Varma, DM (Cardiology)",
      modality: "ecg"
    },
    chest_xray: {
      patientId: "QM-2026-X04",
      name: "Smt. Ananya Mukherjee",
      age: 46,
      gender: "Female",
      abhaNumber: "82-1029-4820-5591",
      abhaAddress: "ananya.mukherjee@abdm",
      uhid: "UHID-KOL-33912",
      history: "Productive cough with low-grade evening pyrexia x 3 weeks, night sweats, anorexia, hemoptysis streaks.",
      indication: "Digital PA Chest Radiograph for pulmonary tuberculosis / cavitary evaluation",
      referringDoctor: "Dr. Pradeep Nair, MD (Pulmonary Medicine)",
      modality: "chest_xray"
    },
    breast_us: {
      patientId: "QM-2026-B05",
      name: "Smt. Meera Swaminathan",
      age: 51,
      gender: "Female",
      abhaNumber: "71-5501-8891-2309",
      abhaAddress: "meera.swaminathan@abdm",
      uhid: "UHID-CHN-66201",
      history: "Painless palpable solitary firm retroareolar lump left breast (Upper Outer Quadrant), noticed during self-examination.",
      indication: "High-resolution Automated Breast Ultrasound (ABUS) for BI-RADS risk classification",
      referringDoctor: "Dr. Leela Krishnan, MCh (Surgical Oncology)",
      modality: "breast_us"
    },
    head_ct: {
      patientId: "QM-2026-H06",
      name: "Sardar Gurpreet Singh",
      age: 64,
      gender: "Male",
      abhaNumber: "99-3321-4402-9102",
      abhaAddress: "gurpreet.singh@abdm",
      uhid: "UHID-CHD-11820",
      history: "Acute right-sided hemiplegia and expressive dysphasia, onset 2 hours prior to presentation in emergency triage.",
      indication: "Emergency Non-Contrast Head CT for acute ischemic vs hemorrhagic stroke differentiation",
      referringDoctor: "Dr. Tariq Mansoor, DM (Neurology)",
      modality: "head_ct"
    }
  };

  class Store {
    constructor() {
      this.listeners = [];

      // Load saved settings
      let savedSettings = null;
      try {
        savedSettings = JSON.parse(localStorage.getItem(STORAGE_KEY_SETTINGS));
      } catch (e) { }

      this.state = {
        // Current Case
        currentPatient: { ...SAMPLE_PATIENTS.fundus },
        currentScan: {
          modality: "fundus",
          sourceType: "sample",
          fileName: "kamala_fundus_macula.png",
          fileSize: "1.8 MB",
          dimensions: { width: 1024, height: 768 },
          rawImageElement: null,
          imageData: null,
          ecgData: null,
          timestamp: new Date().toISOString()
        },
        qualityAssessment: {
          status: "ACCEPT", // ACCEPT, RETAKE, EXPERT_REVIEW
          score: 88.4,
          laplacianVariance: 142.6,
          brightness: 118.2,
          contrast: 68.4,
          noiseEstimate: 4.2,
          completeness: 98.0,
          oodScore: 0.04,
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
          histogram: [],
          edgeDensity: 0.162,
          quadrantVariance: 18.4,
          meanLuminance: 118.2,
          ecgMetrics: { hr: 76, rPeaks: [48, 126, 204, 282, 360], rriSDNN: 32.4, qrsWidthMs: 94 }
        },
        analysisResult: {
          primaryDiagnosis: "Moderate Non-Proliferative Diabetic Retinopathy (NPDR)",
          severity: "Moderate",
          confidence: 0.946,
          uncertainty: 0.054,
          quantumDelta: 4.8,
          findings: [
            {
              id: "FND-01",
              label: "Moderate Non-Proliferative Diabetic Retinopathy (NPDR)",
              severity: "Moderate",
              confidence: 0.946,
              uncertainty: 0.054,
              anatomicalSite: "Posterior Pole / Macula",
              measurements: { microaneurysms: 19, hardExudatesAreaMm2: 2.4, hemorrhageQuadrants: 3 },
              coordinates: [{ x: 0.48, y: 0.52, radius: 0.14 }]
            },
            {
              id: "FND-02",
              label: "Clinically Significant Macular Edema (CSME)",
              severity: "High",
              confidence: 0.912,
              uncertainty: 0.088,
              anatomicalSite: "Foveal avascular zone margin",
              measurements: { fovealDistanceUm: 320, exudateRingDiameterUm: 740 },
              coordinates: [{ x: 0.54, y: 0.49, radius: 0.09 }]
            }
          ],
          saliencyCanvas: null,
          provenance: "Rule-based simulation",
          inferenceProvider: "RuleBasedSimulator",
          timestamp: new Date().toISOString(),
          disclaimer: "SIMULATED AI OUTPUT – RESEARCH & CLINICAL DECISION SUPPORT ONLY. NOT A STANDALONE MEDICAL DIAGNOSIS."
        },
        doctorReview: {
          action: "ACCEPT", // ACCEPT, MODIFY, OVERRIDE, REJECT, SECOND_OPINION
          reclassification: "CONCUR",
          rationale: "Validated against patient ophthalmic history. Microaneurysms and hard exudates correlate with HbA1c elevation.",
          calipers: { radius: 12, offsetX: 0, offsetY: 0 },
          secondOpinionRequested: false,
          secondOpinionDoctor: "",
          secondOpinionNotes: "",
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
          version: 1,
          status: "Draft", // Draft, Under Review, Doctor Approved, Digitally Signed, Released to Patient, Revoked
          createdAt: new Date().toISOString(),
          signedAt: null,
          sha256Hash: "d56fe8aad25b61ffc5781b76d60ee6a34891b01982736451a928374615243102",
          qrCodeData: "https://lenscode.health/verify?report=LC-2026-000412",
          history: []
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
          activeRole: (savedSettings && savedSettings.activeRole) || "Doctor", // Doctor, Radiologist, Technician, Auditor, Patient
          language: (savedSettings && savedSettings.language) || "en", // en, hi
          reducedMotion: false,
          fontScale: 110,
          inferenceProvider: (savedSettings && savedSettings.inferenceProvider) || "RuleBasedSimulator", // RuleBasedSimulator, GeminiProvider, BackendProvider
          geminiApiKey: (savedSettings && savedSettings.geminiApiKey) || ""
        },
        activeStep: 1 // 1: Intake, 2: Quality, 3: Analysis, 4: Review, 5: Report, 6: Share
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
        } catch (err) {
          console.error("Store listener error:", err);
        }
      }
    }

    set(key, value) {
      this.state[key] = value;
      this.notify(key);
    }

    update(key, partial) {
      if (typeof this.state[key] === 'object' && this.state[key] !== null) {
        this.state[key] = { ...this.state[key], ...partial };
      } else {
        this.state[key] = partial;
      }
      this.notify(key);
    }

    get(key) {
      return this.state[key];
    }

    getState() {
      return this.state;
    }

    loadSamplePatient(modality) {
      const p = SAMPLE_PATIENTS[modality] || SAMPLE_PATIENTS.fundus;
      this.update('currentPatient', { ...p });
      this.update('currentScan', {
        modality: modality,
        sourceType: "sample",
        fileName: `${p.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}_${modality}.png`,
        fileSize: "1.9 MB",
        timestamp: new Date().toISOString()
      });
      this.update('report', {
        id: `LC-2026-${Math.floor(100000 + Math.random() * 900000)}`,
        accessionNumber: `ACC-2026-${Math.floor(10000 + Math.random() * 90000)}`,
        studyId: `STD-${modality.toUpperCase()}-${Math.floor(100 + Math.random() * 900)}`,
        version: 1,
        status: "Draft",
        createdAt: new Date().toISOString(),
        signedAt: null
      });
    }

    saveCurrentReportToLibrary() {
      const currentRep = {
        ...this.state.report,
        patient: { ...this.state.currentPatient },
        scan: { ...this.state.currentScan },
        quality: { ...this.state.qualityAssessment },
        findings: [...this.state.analysisResult.findings],
        primaryDiagnosis: this.state.analysisResult.primaryDiagnosis,
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

      // Seed with initial report if none
      return [
        {
          id: "LC-2026-000412",
          accessionNumber: "ACC-2026-89410",
          studyId: "STD-FND-401",
          version: 1,
          status: "Digitally Signed",
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
          provenance: "Rule-based simulation",
          signerName: "Dr. Sunita Rao, MS"
        },
        {
          id: "LC-2026-000409",
          accessionNumber: "ACC-2026-77102",
          studyId: "STD-ECG-103",
          version: 1,
          status: "Doctor Approved",
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
          provenance: "Rule-based simulation",
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
        localStorage.removeItem(STORAGE_KEY_AUDIT);
        localStorage.removeItem(STORAGE_KEY_SETTINGS);
      } catch (e) { }
      window.location.reload();
    }
  }

  window.QuantaMedStore = new Store();
  window.SAMPLE_PATIENTS = SAMPLE_PATIENTS;

})(window);
