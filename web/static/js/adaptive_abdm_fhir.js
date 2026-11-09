/**
 * LensCode – Adaptive QuantaMed
 * ABDM Sandbox Integration & HL7 FHIR R4 Bundle Engine (Phase 2)
 */

(function (window) {
  'use strict';

  class ABDMFHIREngine {
    /**
     * Validates 14-digit ABHA Number format: XX-XXXX-XXXX-XXXX
     */
    validateABHANumber(abha) {
      if (!abha) return { valid: false, message: "ABHA number cannot be empty." };
      const cleaned = abha.replace(/[-\s]/g, '');
      if (!/^\d{14}$/.test(cleaned)) {
        return { valid: false, message: "ABHA Number must be exactly 14 numeric digits." };
      }
      return { valid: true, cleaned, formatted: this.formatABHANumber(cleaned) };
    }

    /**
     * Formats 14 raw digits into XX-XXXX-XXXX-XXXX
     */
    formatABHANumber(digits) {
      const d = digits.replace(/\D/g, '').slice(0, 14);
      const parts = [];
      if (d.length > 0) parts.push(d.slice(0, 2));
      if (d.length > 2) parts.push(d.slice(2, 6));
      if (d.length > 6) parts.push(d.slice(6, 10));
      if (d.length > 10) parts.push(d.slice(10, 14));
      return parts.join('-');
    }

    /**
     * Field-level masking: shows only last 4 digits
     */
    maskABHANumber(abha) {
      if (!abha) return "XX-XXXX-XXXX-0000";
      const cleaned = abha.replace(/[-\s]/g, '');
      if (cleaned.length < 4) return "XX-XXXX-XXXX-XXXX";
      const last4 = cleaned.slice(-4);
      return `XX-XXXX-XXXX-${last4}`;
    }

    /**
     * Generates a complete HL7 FHIR R4 Bundle from current case state
     */
    generateFHIRBundle(state) {
      const now = new Date().toISOString();
      const patient = state.currentPatient;
      const scan = state.currentScan;
      const result = state.analysisResult;
      const report = state.report;
      const review = state.doctorReview;
      const abdm = state.abdm;

      const reportUUID = `urn:uuid:report-${report.id.toLowerCase()}`;
      const patientUUID = `urn:uuid:patient-${patient.patientId.toLowerCase()}`;
      const practitionerUUID = `urn:uuid:practitioner-${abdm.hprId.toLowerCase()}`;
      const orgUUID = `urn:uuid:org-${abdm.facilityId.toLowerCase()}`;
      const encounterUUID = `urn:uuid:encounter-${report.accessionNumber.toLowerCase()}`;
      const imagingStudyUUID = `urn:uuid:imagingstudy-${report.studyId.toLowerCase()}`;
      const obsUUID = `urn:uuid:obs-findings-${report.id.toLowerCase()}`;

      const bundle = {
        resourceType: "Bundle",
        id: `bundle-${report.id.toLowerCase()}`,
        meta: {
          versionId: "1",
          lastUpdated: now,
          profile: ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DiagnosticReportRecord"]
        },
        identifier: {
          system: "https://healthid.ndhm.gov.in",
          value: report.id
        },
        type: "document",
        timestamp: now,
        entry: [
          // 1. DiagnosticReport (Primary Resource)
          {
            fullUrl: reportUUID,
            resource: {
              resourceType: "DiagnosticReport",
              id: report.id.toLowerCase(),
              status: report.status === "Digitally Signed" ? "final" : "preliminary",
              category: [
                {
                  coding: [
                    {
                      system: "http://terminology.hl7.org/CodeSystem/v2-0074",
                      code: "RAD",
                      display: "Radiology / Diagnostic Imaging"
                    }
                  ]
                }
              ],
              code: {
                coding: [
                  {
                    system: "http://loinc.org",
                    code: "18748-4",
                    display: "Diagnostic Imaging Study Report"
                  }
                ],
                text: `${scan.modality.toUpperCase()} Adaptive AI Assisted Clinical Analysis`
              },
              subject: {
                reference: patientUUID,
                display: `${patient.name} (${this.maskABHANumber(patient.abhaNumber)})`
              },
              encounter: {
                reference: encounterUUID
              },
              effectiveDateTime: now,
              issued: now,
              performer: [
                {
                  reference: practitionerUUID,
                  display: review.signerName || abdm.hprName
                },
                {
                  reference: orgUUID,
                  display: abdm.facilityName
                }
              ],
              result: [
                {
                  reference: obsUUID,
                  display: result.primaryDiagnosis
                }
              ],
              imagingStudy: [
                {
                  reference: imagingStudyUUID
                }
              ],
              conclusion: result.primaryDiagnosis,
              conclusionCode: [
                {
                  coding: [
                    {
                      system: "http://snomed.info/sct",
                      code: "57054005",
                      display: result.primaryDiagnosis
                    }
                  ]
                }
              ]
            }
          },

          // 2. Patient
          {
            fullUrl: patientUUID,
            resource: {
              resourceType: "Patient",
              id: patient.patientId.toLowerCase(),
              identifier: [
                {
                  type: {
                    coding: [{ system: "http://terminology.hl7.org/CodeSystem/v2-0203", code: "MR", display: "Medical Record Number" }]
                  },
                  system: "https://healthid.ndhm.gov.in",
                  value: this.maskABHANumber(patient.abhaNumber)
                },
                {
                  type: {
                    coding: [{ system: "http://terminology.hl7.org/CodeSystem/v2-0203", code: "PI", display: "Patient Internal Identifier" }]
                  },
                  value: patient.uhid
                }
              ],
              name: [
                {
                  use: "official",
                  text: patient.name
                }
              ],
              gender: patient.gender.toLowerCase(),
              birthDate: `${2026 - patient.age}-01-01`
            }
          },

          // 3. Practitioner
          {
            fullUrl: practitionerUUID,
            resource: {
              resourceType: "Practitioner",
              id: abdm.hprId.toLowerCase(),
              identifier: [
                {
                  system: "https://hpr.ndhm.gov.in",
                  value: abdm.hprId
                }
              ],
              name: [
                {
                  use: "official",
                  text: review.signerName || abdm.hprName
                }
              ]
            }
          },

          // 4. Organization
          {
            fullUrl: orgUUID,
            resource: {
              resourceType: "Organization",
              id: abdm.facilityId.toLowerCase(),
              identifier: [
                {
                  system: "https://hfr.ndhm.gov.in",
                  value: abdm.facilityId
                }
              ],
              name: abdm.facilityName
            }
          },

          // 5. Encounter
          {
            fullUrl: encounterUUID,
            resource: {
              resourceType: "Encounter",
              id: report.accessionNumber.toLowerCase(),
              status: "finished",
              class: {
                system: "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                code: "AMB",
                display: "ambulatory"
              },
              subject: {
                reference: patientUUID
              }
            }
          },

          // 6. Observation (Biomarkers & Measurements)
          {
            fullUrl: obsUUID,
            resource: {
              resourceType: "Observation",
              id: `obs-${report.id.toLowerCase()}`,
              status: "final",
              category: [
                {
                  coding: [
                    {
                      system: "http://terminology.hl7.org/CodeSystem/observation-category",
                      code: "imaging",
                      display: "Imaging"
                    }
                  ]
                }
              ],
              code: {
                coding: [
                  {
                    system: "http://snomed.info/sct",
                    code: "363679005",
                    display: "Imaging finding"
                  }
                ],
                text: result.primaryDiagnosis
              },
              subject: {
                reference: patientUUID
              },
              valueString: result.primaryDiagnosis,
              component: Object.entries(result.findings[0]?.measurements || {}).map(([key, val]) => ({
                code: { text: key },
                valueString: String(val)
              }))
            }
          },

          // 7. Provenance (Explicit AI Attribution)
          {
            fullUrl: `urn:uuid:provenance-${report.id.toLowerCase()}`,
            resource: {
              resourceType: "Provenance",
              id: `prov-${report.id.toLowerCase()}`,
              target: [{ reference: reportUUID }],
              recorded: now,
              activity: {
                coding: [
                  {
                    system: "http://terminology.hl7.org/CodeSystem/v3-DocumentCompletion",
                    code: "AU",
                    display: "authenticated"
                  }
                ]
              },
              agent: [
                {
                  type: {
                    coding: [{ system: "http://terminology.hl7.org/CodeSystem/provenance-participant-type", code: "author" }]
                  },
                  who: { display: `LensCode Adaptive QuantaMed AI Engine (${result.provenance})` }
                },
                {
                  type: {
                    coding: [{ system: "http://terminology.hl7.org/CodeSystem/provenance-participant-type", code: "verifier" }]
                  },
                  who: { reference: practitionerUUID, display: review.signerName }
                }
              ]
            }
          }
        ]
      };

      return bundle;
    }

    /**
     * Structural Validator for FHIR R4 Bundle
     */
    validateFHIRBundle(bundle) {
      const errors = [];
      const warnings = [];

      if (!bundle || typeof bundle !== 'object') {
        return { isValid: false, errors: ["Empty or invalid JSON payload."], warnings: [] };
      }

      if (bundle.resourceType !== "Bundle") {
        errors.push("Root resource must have 'resourceType': 'Bundle'.");
      }
      if (!bundle.type) {
        errors.push("Bundle missing required 'type' field (expected 'document').");
      }
      if (!bundle.id) {
        errors.push("Bundle missing required 'id'.");
      }
      if (!Array.isArray(bundle.entry) || bundle.entry.length === 0) {
        errors.push("Bundle must contain at least one resource in 'entry'.");
      } else {
        const foundUrls = new Set();
        bundle.entry.forEach((entry, idx) => {
          if (!entry.resource) {
            errors.push(`Entry #${idx} missing 'resource' object.`);
          } else {
            const r = entry.resource;
            if (!r.resourceType) errors.push(`Entry #${idx} missing 'resourceType'.`);
            if (!r.id) errors.push(`Entry #${idx} (${r.resourceType}) missing 'id'.`);
          }
          if (entry.fullUrl) foundUrls.add(entry.fullUrl);
        });

        // Check reference integrity
        const report = bundle.entry.find(e => e.resource?.resourceType === "DiagnosticReport");
        if (report) {
          const subRef = report.resource.subject?.reference;
          if (subRef && !foundUrls.has(subRef)) {
            warnings.push(`DiagnosticReport subject reference '${subRef}' not resolved within bundle entries.`);
          }
        }
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings,
        entryCount: bundle.entry ? bundle.entry.length : 0
      };
    }

    /**
     * Generates ABDM Consent Artifact (JSON)
     */
    generateConsentArtifact(patient, purpose = "Care Management (CAREMGT)") {
      const now = new Date();
      const expiry = new Date(now.getTime() + 90 * 24 * 60 * 60 * 1000); // 90 days validity

      return {
        schemaVersion: "v1.0",
        consentId: `CA-2026-ABDM-${Math.floor(10000 + Math.random() * 90000)}`,
        createdAt: now.toISOString(),
        patient: {
          id: patient.abhaAddress || `${patient.name.toLowerCase().replace(/\s+/g, '')}@abdm`
        },
        consentManager: {
          id: "sbx-abdm"
        },
        purpose: {
          code: "CAREMGT",
          text: purpose
        },
        hip: {
          id: "IN091002",
          name: "LensCode Demo Hospital & Research Centre"
        },
        hiu: {
          id: "IN091005",
          name: "Apex Clinical Tele-Diagnostics"
        },
        requester: {
          name: patient.referringDoctor || "Dr. Sunita Rao, MS",
          identifier: {
            type: "HPR",
            value: "HPR-IN-2026-88194"
          }
        },
        hiTypes: ["DiagnosticReport", "ImagingStudy", "Observation"],
        permission: {
          accessMode: "VIEW",
          dateRange: {
            from: new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000).toISOString(),
            to: now.toISOString()
          },
          dataEraseAt: expiry.toISOString(),
          frequency: {
            unit: "HOUR",
            value: 1,
            repeats: 0
          }
        }
      };
    }
  }

  window.AdaptiveABDMFHIR = new ABDMFHIREngine();

})(window);
