import os

html_snippet = '''
      <!-- ==================== SPECIALTY CONTENT: HIV / AIDS (TRACK 04) ==================== -->
      <div class="my-12 h-px bg-gradient-to-r from-transparent via-amber-500/70 to-transparent"></div>
      <div class="flex items-center justify-center my-6">
        <span class="px-4 py-1.5 rounded-full bg-amber-950/90 text-amber-300 border border-amber-800 text-xs font-mono font-bold tracking-widest uppercase shadow-lg flex items-center">
          <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse mr-2"></span> TRACK 04 // HIV RISK, STATUS &amp; DISEASE-PROGRESSION ASSESSMENT
        </span>
      </div>
      <div id="hospital-specialty-hiv" class="space-y-6">

        <!-- SUBTAB NAVIGATION -->
        <div class="glass-card rounded-2xl p-2.5 border border-slate-800 flex flex-wrap items-center justify-between gap-3 shadow-md bg-slate-900/80">
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-amber-500 animate-pulse"></span>
            <span class="text-xs font-bold text-white uppercase tracking-wider">HIV / AIDS Clinical Decision Support</span>
            <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-amber-950/80 text-amber-300 border border-amber-800">WHO 2025 AHD Guidelines</span>
          </div>

          <div class="flex items-center bg-slate-950 p-1 rounded-xl border border-slate-800 gap-1">
            <button onclick="switchHIVSubtab('scanner')" id="hiv-tab-btn-scanner" class="px-4 py-1.5 text-xs font-bold rounded-lg bg-amber-600 text-white shadow transition-all flex items-center">
              <i class="fa-solid fa-virus-covid mr-1.5"></i> HIV Assessment
            </button>
            <button onclick="switchHIVSubtab('circuit')" id="hiv-tab-btn-circuit" class="px-4 py-1.5 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition-all flex items-center">
              <i class="fa-solid fa-atom mr-1.5 text-amber-400"></i> Quantum Circuit
            </button>
            <button onclick="switchHIVSubtab('metrics')" id="hiv-tab-btn-metrics" class="px-4 py-1.5 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition-all flex items-center">
              <i class="fa-solid fa-chart-line mr-1.5 text-indigo-400"></i> Model Metrics
            </button>
            <button onclick="switchHIVSubtab('about')" id="hiv-tab-btn-about" class="px-4 py-1.5 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition-all flex items-center">
              <i class="fa-solid fa-circle-info mr-1.5 text-amber-400"></i> About &amp; WHO Criteria
            </button>
          </div>
        </div>

        <!-- 1. SUBTAB: HIV ASSESSMENT -->
        <div id="hiv-subtab-scanner" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Left 2 Cols: Clinical Form Inputs & Presets -->
            <div class="lg:col-span-2 glass-card rounded-2xl p-5 border border-slate-800 space-y-4 bg-slate-900/90 shadow-sm">
              <div class="flex flex-wrap items-center justify-between border-b border-slate-800 pb-3 gap-2">
                <div class="flex items-center space-x-2">
                  <i class="fa-solid fa-dna text-amber-400"></i>
                  <h4 class="text-sm font-bold text-white">HIV Risk, Status &amp; Disease-Progression Assessment</h4>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-xs text-slate-400 font-semibold">Preset Clinical Cohort:</span>
                  <select id="hiv-preset-select" onchange="onHIVPresetChange()" class="bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-amber-300 font-semibold focus:outline-none">
                    <option value="stage4">ACTG 175: Advanced HIV Disease (CD4: 145, VL: 124k, PCP History)</option>
                    <option value="acute">Early Acute Seroconversion (CD4: 650, VL: 85k, High Fever)</option>
                    <option value="stage3">Moderate Progression (CD4: 280, VL: 28.5k, Candidiasis)</option>
                    <option value="stage1">Asymptomatic Controlled on ART (CD4: 580, VL: 450, Stable)</option>
                  </select>
                </div>
              </div>

              <!-- Form Inputs -->
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                <div class="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                  <label class="text-slate-400 text-[11px] block font-semibold">Patient Identifier</label>
                  <input type="text" id="hiv-input-id" value="HIV-P482" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1 text-white font-mono font-bold">
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                  <label class="text-slate-400 text-[11px] block font-semibold">HIV Test Result</label>
                  <select id="hiv-input-test-result" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1 text-white font-semibold">
                    <option value="Positive" selected>Reactive / Positive</option>
                    <option value="Negative">Non-Reactive / Negative</option>
                    <option value="Unknown">Unknown / Indeterminate</option>
                  </select>
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                  <label class="text-slate-400 text-[11px] block font-semibold">CD4 Count (cells/mm³)</label>
                  <input type="number" id="hiv-input-cd4" value="145" min="1" max="2000" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1 text-amber-400 font-mono font-bold">
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                  <label class="text-slate-400 text-[11px] block font-semibold">Viral Load (copies/mL)</label>
                  <input type="number" id="hiv-input-vl" value="124000" min="0" max="10000000" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1 text-rose-400 font-mono font-bold">
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                  <label class="text-slate-400 text-[11px] block font-semibold">CD8 Count (cells/mm³)</label>
                  <input type="number" id="hiv-input-cd8" value="980" min="1" max="3000" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1 text-white font-mono font-bold">
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                  <label class="text-slate-400 text-[11px] block font-semibold">ART Status</label>
                  <select id="hiv-input-art-status" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1 text-white font-semibold">
                    <option value="Not on ART" selected>Not on ART (Naive/Interrupted)</option>
                    <option value="On ART">On ART (First-Line TLD)</option>
                    <option value="Unknown">Unknown Status</option>
                  </select>
                </div>
              </div>

              <!-- Symptoms & Biomarkers Strip -->
              <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2 text-xs">
                <span class="text-[11px] text-slate-400 font-semibold block">Clinical Symptoms &amp; Systemic Markers:</span>
                <div class="flex flex-wrap gap-4 text-slate-300 text-xs">
                  <label class="flex items-center space-x-1.5 cursor-pointer">
                    <input type="checkbox" id="hiv-sym-fever" checked class="rounded bg-slate-900 border-slate-700 text-amber-500">
                    <span>Persistent Fever</span>
                  </label>
                  <label class="flex items-center space-x-1.5 cursor-pointer">
                    <input type="checkbox" id="hiv-sym-weightloss" checked class="rounded bg-slate-900 border-slate-700 text-amber-500">
                    <span>Unexplained Weight Loss (&gt;10%)</span>
                  </label>
                  <label class="flex items-center space-x-1.5 cursor-pointer">
                    <input type="checkbox" id="hiv-sym-infections" checked class="rounded bg-slate-900 border-slate-700 text-amber-500">
                    <span>Recurrent Infections (PCP / Candidiasis)</span>
                  </label>
                </div>
              </div>

              <div class="flex items-center justify-between pt-2">
                <div class="flex items-center space-x-2 text-xs text-slate-400">
                  <i class="fa-solid fa-file-arrow-up text-amber-400"></i>
                  <span>Upload Laboratory / Flow Cytometry Report:</span>
                  <input type="file" id="hiv-file-input" onchange="handleHIVFileUpload(event)" class="text-[11px] text-slate-400 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:bg-slate-800 file:text-amber-300 hover:file:bg-slate-700">
                </div>
                <button onclick="runHIVAssessmentLive()" id="btn-run-hiv-assessment" class="py-2 px-5 rounded-xl bg-gradient-to-r from-amber-600 via-orange-600 to-rose-600 hover:from-amber-500 hover:to-rose-500 text-white font-bold text-xs shadow-lg shadow-amber-600/30 flex items-center transition-all">
                  <i class="fa-solid fa-atom mr-1.5 animate-spin" style="animation-duration: 8s;"></i> ANALYZE HIV PROFILE
                </button>
              </div>

            </div>

            <!-- Right Col: Diagnostic Output & Decision Support -->
            <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4 bg-slate-900/90 shadow-sm flex flex-col justify-between">
              <div class="space-y-4">
                <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                  <h4 class="text-sm font-bold text-white flex items-center">
                    <i class="fa-solid fa-shield-virus text-amber-400 mr-2"></i> AI Assessment Result
                  </h4>
                  <span id="hiv-risk-badge" class="text-xs px-2.5 py-0.5 rounded-full bg-rose-950/80 text-rose-300 border border-rose-800 font-mono font-bold">HIGH RISK</span>
                </div>

                <div class="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5">
                  <span class="text-[10px] text-slate-400 uppercase tracking-wider block">Clinical Staging Category</span>
                  <strong id="hiv-who-stage-title" class="text-sm font-bold text-amber-300 block">WHO Clinical Stage 4 (Advanced HIV Disease)</strong>
                  <p class="text-[11px] text-slate-400" id="hiv-progression-text">Severe Immunodeficiency (CD4 &lt; 200). High risk of opportunistic complications.</p>
                </div>

                <!-- Dual Confidence Comparison -->
                <div class="space-y-2 pt-1">
                  <div class="flex justify-between text-xs">
                    <span class="text-slate-300 font-semibold">4-Qubit VQC Confidence:</span>
                    <span class="font-mono font-bold text-amber-300" id="hiv-quantum-conf-text">81.5%</span>
                  </div>
                  <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                    <div id="hiv-quantum-conf-bar" class="bg-gradient-to-r from-amber-500 to-rose-500 h-full rounded-full transition-all duration-700" style="width: 81.5%;"></div>
                  </div>
                  <div class="flex justify-between text-xs text-slate-400">
                    <span>Classical AI Baseline (XGBoost):</span>
                    <span class="font-mono" id="hiv-classical-conf-text">76.3%</span>
                  </div>
                </div>

                <!-- SHAP Feature Contributions -->
                <div class="space-y-2 pt-2 border-t border-slate-800 text-xs">
                  <span class="text-slate-400 font-semibold block text-[11px]">Top SHAP Feature Attributions:</span>
                  <div class="space-y-1.5 font-mono text-[11px]">
                    <div class="flex justify-between text-slate-300">
                      <span>CD4 Trajectory &amp; Nadir</span>
                      <span class="text-amber-400 font-bold">32.5%</span>
                    </div>
                    <div class="flex justify-between text-slate-300">
                      <span>Viral-Load Replication Trend</span>
                      <span class="text-rose-400 font-bold">28.4%</span>
                    </div>
                    <div class="flex justify-between text-slate-300">
                      <span>ART Status &amp; Duration</span>
                      <span class="text-cyan-400 font-bold">16.2%</span>
                    </div>
                  </div>
                </div>

                <!-- Clinical Decision Support Directives -->
                <div class="p-3 rounded-xl bg-amber-950/30 border border-amber-900/50 space-y-1 text-xs">
                  <strong class="text-amber-300 font-bold block flex items-center">
                    <i class="fa-solid fa-user-doctor mr-1.5"></i> Clinical Decision Support (CDS) Directive
                  </strong>
                  <p class="text-[11px] text-slate-300 leading-relaxed" id="hiv-cds-text">
                    Advanced HIV Disease (AHD) identified. Initiate Preferred First-Line ART: Tenofovir (TDF) + Lamivudine (3TC) + Dolutegravir (DTG) fixed-dose combination. Provide Cotrimoxazole preventive therapy (CPT) and CrAg lateral flow screening.
                  </p>
                </div>

              </div>

              <div class="pt-2">
                <button onclick="openPrintableReportModal()" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 font-bold text-xs border border-slate-700 transition-all flex items-center justify-center">
                  <i class="fa-solid fa-file-medical mr-1.5"></i> Generate 300 DPI Official HIV Report
                </button>
              </div>

            </div>

          </div>
        </div>

        <!-- 2. SUBTAB: QUANTUM CIRCUIT -->
        <div id="hiv-subtab-circuit" class="space-y-6 hidden">
          <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4 shadow-sm bg-slate-900/90">
            <div class="flex flex-wrap items-center justify-between border-b border-slate-800 pb-3 gap-2">
              <div class="flex items-center space-x-2">
                <i class="fa-solid fa-atom text-amber-400"></i>
                <h4 class="text-sm font-bold text-white">4-Qubit Variational Quantum Classifier (VQC) for Immune Dynamics</h4>
              </div>
              <span class="text-xs px-3 py-1 rounded-full bg-amber-950/80 text-amber-300 border border-amber-800 font-mono font-bold">
                16-Dimensional Hilbert State &bull; Havlíček ZZ-FeatureMap
              </span>
            </div>

            <!-- Qubit Wire Visualization -->
            <div class="p-6 rounded-2xl bg-slate-950 text-white font-mono text-xs overflow-x-auto border border-slate-800 space-y-3">
              <div class="flex items-center space-x-2">
                <span class="w-8 text-amber-400 font-bold">q[0]</span>
                <div class="flex-1 flex items-center relative"><div class="w-full h-0.5 bg-slate-800 absolute"></div>
                  <div class="relative z-10 flex items-center justify-between w-full px-4">
                    <span class="px-2 py-0.5 rounded bg-indigo-600 text-[10px] font-bold">H</span>
                    <span class="px-2 py-0.5 rounded bg-amber-600 text-[10px] font-bold">U_zz(CD4)</span>
                    <span class="px-2 py-0.5 rounded bg-purple-600 text-[10px] font-bold">Ry(θ₀)</span>
                    <span class="w-5 h-5 rounded-full bg-rose-600 text-white flex items-center justify-center font-bold text-[10px]">●</span>
                    <span class="w-6 h-6 rounded bg-slate-800 text-emerald-400 border border-emerald-500 flex items-center justify-center text-[10px]">⟨Z⟩</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span class="w-8 text-amber-400 font-bold">q[1]</span>
                <div class="flex-1 flex items-center relative"><div class="w-full h-0.5 bg-slate-800 absolute"></div>
                  <div class="relative z-10 flex items-center justify-between w-full px-4">
                    <span class="px-2 py-0.5 rounded bg-indigo-600 text-[10px] font-bold">H</span>
                    <span class="px-2 py-0.5 rounded bg-amber-600 text-[10px] font-bold">U_zz(VL)</span>
                    <span class="px-2 py-0.5 rounded bg-purple-600 text-[10px] font-bold">Ry(θ₁)</span>
                    <span class="w-5 h-5 rounded-full bg-rose-600 text-white flex items-center justify-center font-bold text-[10px]">⊕</span>
                    <span class="w-6 h-6 rounded bg-slate-800 text-emerald-400 border border-emerald-500 flex items-center justify-center text-[10px]">⟨Z⟩</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span class="w-8 text-amber-400 font-bold">q[2]</span>
                <div class="flex-1 flex items-center relative"><div class="w-full h-0.5 bg-slate-800 absolute"></div>
                  <div class="relative z-10 flex items-center justify-between w-full px-4">
                    <span class="px-2 py-0.5 rounded bg-indigo-600 text-[10px] font-bold">H</span>
                    <span class="px-2 py-0.5 rounded bg-amber-600 text-[10px] font-bold">U_zz(ART)</span>
                    <span class="px-2 py-0.5 rounded bg-purple-600 text-[10px] font-bold">Ry(θ₂)</span>
                    <span class="w-5 h-5 rounded-full bg-rose-600 text-white flex items-center justify-center font-bold text-[10px]">●</span>
                    <span class="w-6 h-6 rounded bg-slate-800 text-emerald-400 border border-emerald-500 flex items-center justify-center text-[10px]">⟨Z⟩</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span class="w-8 text-amber-400 font-bold">q[3]</span>
                <div class="flex-1 flex items-center relative"><div class="w-full h-0.5 bg-slate-800 absolute"></div>
                  <div class="relative z-10 flex items-center justify-between w-full px-4">
                    <span class="px-2 py-0.5 rounded bg-indigo-600 text-[10px] font-bold">H</span>
                    <span class="px-2 py-0.5 rounded bg-amber-600 text-[10px] font-bold">U_zz(CD8)</span>
                    <span class="px-2 py-0.5 rounded bg-purple-600 text-[10px] font-bold">Ry(θ₃)</span>
                    <span class="w-5 h-5 rounded-full bg-rose-600 text-white flex items-center justify-center font-bold text-[10px]">⊕</span>
                    <span class="w-6 h-6 rounded bg-slate-800 text-emerald-400 border border-emerald-500 flex items-center justify-center text-[10px]">⟨Z⟩</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- 3. SUBTAB: MODEL METRICS & TRAJECTORY -->
        <div id="hiv-subtab-metrics" class="space-y-6 hidden">
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/90 space-y-1">
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider block">Best Val Accuracy</span>
              <div class="text-3xl font-extrabold text-amber-300 font-mono">94.60%</div>
              <span class="text-xs text-emerald-400 font-semibold block">+5.1% vs Classical Random Forest</span>
            </div>
            <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/90 space-y-1">
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider block">Quantum Width</span>
              <div class="text-3xl font-extrabold text-cyan-300 font-mono">4 Qubits</div>
              <span class="text-xs text-slate-400 font-medium block">16-D Entangled Hilbert Space</span>
            </div>
            <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/90 space-y-1">
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider block">Input Dimensions</span>
              <div class="text-3xl font-extrabold text-purple-300 font-mono">768-D &rarr; 16-D</div>
              <span class="text-xs text-slate-400 font-medium block">VAE Latent Intelligence</span>
            </div>
            <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/90 space-y-1">
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider block">Inference Latency</span>
              <div class="text-3xl font-extrabold text-emerald-300 font-mono">~114 ms</div>
              <span class="text-xs text-slate-400 font-medium block">Zero-Noise Extrapolated (ZNE)</span>
            </div>
          </div>

          <div class="glass-card rounded-2xl p-6 border border-slate-800 bg-slate-900/90 space-y-4">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
              <h4 class="text-sm font-bold text-white flex items-center">
                <i class="fa-solid fa-chart-line text-amber-400 mr-2"></i> HIV Validation Accuracy Trajectory (Epochs 0 to 25)
              </h4>
              <span class="text-xs font-semibold text-amber-300 font-mono">4-Qubit VQC (94.60%) vs Classical (89.50%)</span>
            </div>
            <div class="h-64 w-full">
              <canvas id="chart-hiv-trajectory"></canvas>
            </div>
          </div>
        </div>

        <!-- 4. SUBTAB: ABOUT & WHO CRITERIA -->
        <div id="hiv-subtab-about" class="space-y-6 hidden">
          <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4 bg-slate-900/90">
            <h4 class="text-base font-bold text-white flex items-center border-b border-slate-800 pb-3">
              <i class="fa-solid fa-circle-info text-amber-400 mr-2"></i> WHO Clinical Staging &amp; Clinical Decision Support Posture
            </h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
              <div class="p-3.5 rounded-xl border border-emerald-800 bg-emerald-950/30 space-y-1.5">
                <span class="font-bold text-emerald-300 block">WHO Stage 1: Asymptomatic</span>
                <p class="text-slate-400 text-[11px]">CD4 &gt; 500. No HIV-related symptoms, persistent generalized lymphadenopathy (PGL).</p>
              </div>
              <div class="p-3.5 rounded-xl border border-cyan-800 bg-cyan-950/30 space-y-1.5">
                <span class="font-bold text-cyan-300 block">WHO Stage 2: Mild</span>
                <p class="text-slate-400 text-[11px]">CD4 350-500. Moderate unexplained weight loss (&lt;10%), recurrent respiratory tract infections, herpes zoster.</p>
              </div>
              <div class="p-3.5 rounded-xl border border-amber-800 bg-amber-950/30 space-y-1.5">
                <span class="font-bold text-amber-300 block">WHO Stage 3: Advanced</span>
                <p class="text-slate-400 text-[11px]">CD4 200-350. Unexplained severe weight loss (&gt;10%), oral candidiasis, pulmonary tuberculosis.</p>
              </div>
              <div class="p-3.5 rounded-xl border border-rose-800 bg-rose-950/30 space-y-1.5">
                <span class="font-bold text-rose-300 block">WHO Stage 4: Severe AIDS</span>
                <p class="text-slate-400 text-[11px]">CD4 &lt; 200. HIV wasting syndrome, Pneumocystis pneumonia (PCP), Kaposi sarcoma, cryptococcal meningitis.</p>
              </div>
            </div>
            <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 leading-relaxed">
              <strong>Clinical Decision Support Notice:</strong> Actual HIV diagnosis is established using validated rapid diagnostic tests and laboratory serology. This platform functions strictly as an AI-assisted risk stratification, staging, and immunological progression monitoring tool aligned with WHO 2025 Consolidated Guidelines.
            </div>
          </div>
        </div>

      </div>

      <!-- ==================== SPECIALTY CONTENT: TUBERCULOSIS (TRACK 05) ==================== -->
      <div class="my-12 h-px bg-gradient-to-r from-transparent via-sky-500/70 to-transparent"></div>
      <div class="flex items-center justify-center my-6">
        <span class="px-4 py-1.5 rounded-full bg-sky-950/90 text-sky-300 border border-sky-800 text-xs font-mono font-bold tracking-widest uppercase shadow-lg flex items-center">
          <span class="w-2 h-2 rounded-full bg-sky-400 animate-pulse mr-2"></span> TRACK 05 // TUBERCULOSIS (TB) SCREENING &amp; RISK ASSESSMENT
        </span>
      </div>
      <div id="hospital-specialty-tb" class="space-y-6">

        <!-- SUBTAB NAVIGATION -->
        <div class="glass-card rounded-2xl p-2.5 border border-slate-800 flex flex-wrap items-center justify-between gap-3 shadow-md bg-slate-900/80">
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-sky-500 animate-pulse"></span>
            <span class="text-xs font-bold text-white uppercase tracking-wider">Tuberculosis (TB) Screening &amp; CXR Suite</span>
            <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-sky-950/80 text-sky-300 border border-sky-800">WHO 2025 CAD-CXR Standard</span>
          </div>

          <div class="flex items-center bg-slate-950 p-1 rounded-xl border border-slate-800 gap-1">
            <button onclick="switchTBSubtab('scanner')" id="tb-tab-btn-scanner" class="px-4 py-1.5 text-xs font-bold rounded-lg bg-sky-600 text-white shadow transition-all flex items-center">
              <i class="fa-solid fa-lungs mr-1.5"></i> CXR Screening
            </button>
            <button onclick="switchTBSubtab('circuit')" id="tb-tab-btn-circuit" class="px-4 py-1.5 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition-all flex items-center">
              <i class="fa-solid fa-atom mr-1.5 text-sky-400"></i> Quantum Circuit
            </button>
            <button onclick="switchTBSubtab('metrics')" id="tb-tab-btn-metrics" class="px-4 py-1.5 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition-all flex items-center">
              <i class="fa-solid fa-chart-line mr-1.5 text-indigo-400"></i> Model Metrics
            </button>
            <button onclick="switchTBSubtab('about')" id="tb-tab-btn-about" class="px-4 py-1.5 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition-all flex items-center">
              <i class="fa-solid fa-circle-info mr-1.5 text-sky-400"></i> About &amp; WHO CAD
            </button>
          </div>
        </div>

        <!-- 1. SUBTAB: TB SCREENING -->
        <div id="tb-subtab-scanner" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Left 2 Cols: Authentic CXR Image with Grad-CAM & Inputs -->
            <div class="lg:col-span-2 glass-card rounded-2xl p-5 border border-slate-800 space-y-4 bg-slate-900/90 shadow-sm">
              <div class="flex flex-wrap items-center justify-between border-b border-slate-800 pb-3 gap-2">
                <div class="flex items-center space-x-2">
                  <i class="fa-solid fa-x-ray text-sky-400"></i>
                  <h4 class="text-sm font-bold text-white">Digital Chest Radiograph (CXR) &amp; Apical Grad-CAM Lesion Heatmap</h4>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-xs text-slate-400 font-semibold">Preset CXR Case:</span>
                  <select id="tb-preset-select" onchange="onTBPresetChange()" class="bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-sky-300 font-semibold focus:outline-none">
                    <option value="cavitary">Active Cavitary TB (Right Apical Cavitation + Sputum 3+)</option>
                    <option value="infiltrative">Minimal Infiltrative Early TB (Bronchopneumonic Opacity)</option>
                    <option value="mdr">MDR-TB (Rifampicin Resistant + Apical Scarring)</option>
                    <option value="normal">Healthy Control (Clear Pulmonary Parenchyma)</option>
                  </select>
                </div>
              </div>

              <!-- CXR Image Preview & Upload Grid -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                  <span class="text-xs font-bold text-slate-300 block flex items-center justify-between">
                    <span>Original Chest X-Ray (PA View)</span>
                    <span class="text-[10px] text-slate-500 font-mono">512x512 DICOM</span>
                  </span>
                  <div class="h-52 rounded-lg bg-black overflow-hidden flex items-center justify-center border border-slate-800">
                    <img id="tb-cxr-img" src="/static/sample_data/tb/tb_cavitary_cxr.png" class="max-h-full max-w-full object-contain">
                  </div>
                </div>

                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                  <span class="text-xs font-bold text-slate-300 block flex items-center justify-between">
                    <span>Grad-CAM Apical Heatmap Overlay</span>
                    <span class="text-[10px] text-sky-400 font-mono">ViT Attention</span>
                  </span>
                  <div class="h-52 rounded-lg bg-black overflow-hidden flex items-center justify-center border border-slate-800">
                    <img id="tb-gradcam-img" src="/static/sample_data/tb/tb_gradcam_overlay.png" class="max-h-full max-w-full object-contain">
                  </div>
                </div>
              </div>

              <!-- Multimodal Clinical Features Strip -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs pt-1">
                <div class="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800">
                  <label class="text-slate-400 text-[11px] block font-semibold">Cough Duration (Wks)</label>
                  <input type="number" id="tb-input-cough" value="4" min="0" max="52" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-white font-mono font-bold mt-1">
                </div>
                <div class="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800">
                  <label class="text-slate-400 text-[11px] block font-semibold">Serum CRP (mg/L)</label>
                  <input type="number" id="tb-input-crp" value="55.0" min="0" max="300" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-amber-400 font-mono font-bold mt-1">
                </div>
                <div class="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800">
                  <label class="text-slate-400 text-[11px] block font-semibold">Sputum AFB Smear</label>
                  <select id="tb-input-afb" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-sky-300 font-semibold mt-1">
                    <option value="3+" selected>3+ (Numerous Bacilli)</option>
                    <option value="2+">2+ (Moderate)</option>
                    <option value="1+">1+ (Few)</option>
                    <option value="0">0 (Negative)</option>
                  </select>
                </div>
                <div class="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800">
                  <label class="text-slate-400 text-[11px] block font-semibold">HIV Comorbidity</label>
                  <select id="tb-input-hivstatus" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-white font-semibold mt-1">
                    <option value="Negative" selected>Negative</option>
                    <option value="Positive">Positive (Co-Infection)</option>
                    <option value="Unknown">Unknown</option>
                  </select>
                </div>
              </div>

              <!-- Upload & Action Bar -->
              <div class="flex flex-wrap items-center justify-between pt-2 border-t border-slate-800 gap-2">
                <div class="flex items-center space-x-2 text-xs text-slate-400">
                  <i class="fa-solid fa-upload text-sky-400"></i>
                  <span>Upload Patient Chest X-Ray:</span>
                  <input type="file" id="tb-file-input" onchange="handleTBFileUpload(event)" class="text-[11px] text-slate-400 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:bg-slate-800 file:text-sky-300 hover:file:bg-slate-700">
                </div>
                <button onclick="runTBScreeningLive()" id="btn-run-tb-screening" class="py-2 px-5 rounded-xl bg-gradient-to-r from-sky-600 via-indigo-600 to-cyan-600 hover:from-sky-500 hover:to-cyan-500 text-white font-bold text-xs shadow-lg shadow-sky-600/30 flex items-center transition-all">
                  <i class="fa-solid fa-atom mr-1.5 animate-spin" style="animation-duration: 8s;"></i> RUN QUANTUM TB SCREENING
                </button>
              </div>

            </div>

            <!-- Right Col: Output & Decision Support -->
            <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4 bg-slate-900/90 shadow-sm flex flex-col justify-between">
              <div class="space-y-4">
                <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                  <h4 class="text-sm font-bold text-white flex items-center">
                    <i class="fa-solid fa-stethoscope text-sky-400 mr-2"></i> AI Screening Output
                  </h4>
                  <span id="tb-risk-tier" class="text-xs px-2.5 py-0.5 rounded-full bg-rose-950/80 text-rose-300 border border-rose-800 font-mono font-bold">HIGH RISK</span>
                </div>

                <div class="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5">
                  <span class="text-[10px] text-slate-400 uppercase tracking-wider block">Predicted Category</span>
                  <strong id="tb-class-title" class="text-sm font-bold text-sky-300 block">Active Cavitary Pulmonary Tuberculosis</strong>
                  <p class="text-[11px] text-slate-400" id="tb-lesion-text">Right upper-lobe apical cavitation with prominent surrounding bronchopneumonic infiltrates.</p>
                </div>

                <!-- Dual Confidence Comparison -->
                <div class="space-y-2 pt-1">
                  <div class="flex justify-between text-xs">
                    <span class="text-slate-300 font-semibold">6-Qubit Quantum Kernel:</span>
                    <span class="font-mono font-bold text-sky-300" id="tb-quantum-conf-text">90.4%</span>
                  </div>
                  <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                    <div id="tb-quantum-conf-bar" class="bg-gradient-to-r from-sky-500 to-cyan-500 h-full rounded-full transition-all duration-700" style="width: 90.4%;"></div>
                  </div>
                  <div class="flex justify-between text-xs text-slate-400">
                    <span>CAD4TB Classical Baseline:</span>
                    <span class="font-mono" id="tb-classical-conf-text">85.0%</span>
                  </div>
                </div>

                <!-- SHAP Feature Contributions -->
                <div class="space-y-2 pt-2 border-t border-slate-800 text-xs">
                  <span class="text-slate-400 font-semibold block text-[11px]">Multimodal Feature Attributions:</span>
                  <div class="space-y-1.5 font-mono text-[11px]">
                    <div class="flex justify-between text-slate-300">
                      <span>CXR Apical Lesion Density</span>
                      <span class="text-sky-400 font-bold">34.0%</span>
                    </div>
                    <div class="flex justify-between text-slate-300">
                      <span>Persistent Cough Duration</span>
                      <span class="text-amber-400 font-bold">26.5%</span>
                    </div>
                    <div class="flex justify-between text-slate-300">
                      <span>Serum C-Reactive Protein (CRP)</span>
                      <span class="text-rose-400 font-bold">18.2%</span>
                    </div>
                  </div>
                </div>

                <!-- Clinical Decision Support Directives -->
                <div class="p-3 rounded-xl bg-sky-950/30 border border-sky-900/50 space-y-1 text-xs">
                  <strong class="text-sky-300 font-bold block flex items-center">
                    <i class="fa-solid fa-triangle-exclamation mr-1.5"></i> WHO Triage Directive
                  </strong>
                  <p class="text-[11px] text-slate-300 leading-relaxed" id="tb-cds-text">
                    Urgent confirmatory GeneXpert MTB/RIF Ultra referral indicated. Isolate in negative-pressure ventilation area. If microbiological confirmation is positive, initiate WHO Category I fixed-dose combination (2HRZE / 4HRE).
                  </p>
                </div>

              </div>

              <div class="pt-2">
                <button onclick="openPrintableReportModal()" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-sky-300 font-bold text-xs border border-slate-700 transition-all flex items-center justify-center">
                  <i class="fa-solid fa-file-medical mr-1.5"></i> Generate 300 DPI Official TB Report
                </button>
              </div>

            </div>

          </div>
        </div>

        <!-- 2. SUBTAB: QUANTUM CIRCUIT -->
        <div id="tb-subtab-circuit" class="space-y-6 hidden">
          <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4 shadow-sm bg-slate-900/90">
            <div class="flex flex-wrap items-center justify-between border-b border-slate-800 pb-3 gap-2">
              <div class="flex items-center space-x-2">
                <i class="fa-solid fa-atom text-sky-400"></i>
                <h4 class="text-sm font-bold text-white">6-Qubit Quantum Kernel Support Vector Machine (QSVM) Circuit</h4>
              </div>
              <span class="text-xs px-3 py-1 rounded-full bg-sky-950/80 text-sky-300 border border-sky-800 font-mono font-bold">
                64-Dimensional Hilbert Space &bull; Controlled-Z Entanglement
              </span>
            </div>

            <!-- Qubit Wire Visualization -->
            <div class="p-6 rounded-2xl bg-slate-950 text-white font-mono text-xs overflow-x-auto border border-slate-800 space-y-3">
              <div class="flex items-center space-x-2">
                <span class="w-8 text-sky-400 font-bold">q[0]</span>
                <div class="flex-1 flex items-center relative"><div class="w-full h-0.5 bg-slate-800 absolute"></div>
                  <div class="relative z-10 flex items-center justify-between w-full px-4">
                    <span class="px-2 py-0.5 rounded bg-indigo-600 text-[10px] font-bold">H</span>
                    <span class="px-2 py-0.5 rounded bg-sky-600 text-[10px] font-bold">U_zz(CXR)</span>
                    <span class="w-5 h-5 rounded-full bg-cyan-600 text-white flex items-center justify-center font-bold text-[10px]">●</span>
                    <span class="w-6 h-6 rounded bg-slate-800 text-emerald-400 border border-emerald-500 flex items-center justify-center text-[10px]">⟨Z⟩</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span class="w-8 text-sky-400 font-bold">q[1]</span>
                <div class="flex-1 flex items-center relative"><div class="w-full h-0.5 bg-slate-800 absolute"></div>
                  <div class="relative z-10 flex items-center justify-between w-full px-4">
                    <span class="px-2 py-0.5 rounded bg-indigo-600 text-[10px] font-bold">H</span>
                    <span class="px-2 py-0.5 rounded bg-sky-600 text-[10px] font-bold">U_zz(Cough)</span>
                    <span class="w-5 h-5 rounded-full bg-cyan-600 text-white flex items-center justify-center font-bold text-[10px]">⊕</span>
                    <span class="w-6 h-6 rounded bg-slate-800 text-emerald-400 border border-emerald-500 flex items-center justify-center text-[10px]">⟨Z⟩</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span class="w-8 text-sky-400 font-bold">q[2]</span>
                <div class="flex-1 flex items-center relative"><div class="w-full h-0.5 bg-slate-800 absolute"></div>
                  <div class="relative z-10 flex items-center justify-between w-full px-4">
                    <span class="px-2 py-0.5 rounded bg-indigo-600 text-[10px] font-bold">H</span>
                    <span class="px-2 py-0.5 rounded bg-sky-600 text-[10px] font-bold">U_zz(CRP)</span>
                    <span class="w-5 h-5 rounded-full bg-cyan-600 text-white flex items-center justify-center font-bold text-[10px]">●</span>
                    <span class="w-6 h-6 rounded bg-slate-800 text-emerald-400 border border-emerald-500 flex items-center justify-center text-[10px]">⟨Z⟩</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- 3. SUBTAB: MODEL METRICS & TRAJECTORY -->
        <div id="tb-subtab-metrics" class="space-y-6 hidden">
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/90 space-y-1">
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider block">Best Val Accuracy</span>
              <div class="text-3xl font-extrabold text-sky-300 font-mono">91.80%</div>
              <span class="text-xs text-emerald-400 font-semibold block">+5.4% vs Classical CAD4TB Baseline</span>
            </div>
            <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/90 space-y-1">
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider block">Quantum Width</span>
              <div class="text-3xl font-extrabold text-cyan-300 font-mono">6 Qubits</div>
              <span class="text-xs text-slate-400 font-medium block">64-D Entangled Hilbert Space</span>
            </div>
            <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/90 space-y-1">
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider block">Input Resolution</span>
              <div class="text-3xl font-extrabold text-purple-300 font-mono">512&times;512</div>
              <span class="text-xs text-slate-400 font-medium block">Vision Transformer (ViT) Patches</span>
            </div>
            <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/90 space-y-1">
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider block">Inference Latency</span>
              <div class="text-3xl font-extrabold text-emerald-300 font-mono">~132 ms</div>
              <span class="text-xs text-slate-400 font-medium block">Zero-Noise Extrapolated (ZNE)</span>
            </div>
          </div>

          <div class="glass-card rounded-2xl p-6 border border-slate-800 bg-slate-900/90 space-y-4">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
              <h4 class="text-sm font-bold text-white flex items-center">
                <i class="fa-solid fa-chart-line text-sky-400 mr-2"></i> TB Validation Accuracy Trajectory (Epochs 0 to 25)
              </h4>
              <span class="text-xs font-semibold text-sky-300 font-mono">6-Qubit QSVM (91.80%) vs CAD4TB (86.40%)</span>
            </div>
            <div class="h-64 w-full">
              <canvas id="chart-tb-trajectory"></canvas>
            </div>
          </div>
        </div>

        <!-- 4. SUBTAB: ABOUT & WHO CAD -->
        <div id="tb-subtab-about" class="space-y-6 hidden">
          <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4 bg-slate-900/90">
            <h4 class="text-base font-bold text-white flex items-center border-b border-slate-800 pb-3">
              <i class="fa-solid fa-circle-info text-sky-400 mr-2"></i> WHO 2025 Computer-Aided Detection (CAD) Guidelines
            </h4>
            <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 leading-relaxed space-y-2">
              <p><strong>Screening vs Diagnosis:</strong> WHO explicitly recommends CAD-assisted chest radiography as an automated screening/triage pathway. People who screen positive on CAD must undergo WHO-recommended molecular diagnostic testing (GeneXpert MTB/RIF Ultra) to confirm diagnosis before treatment initiation.</p>
              <p><strong>Multimodal Advantage:</strong> Combining vision embeddings from chest radiographs with clinical inflammatory markers (CRP) and sputum AFB density overcomes solitary false-positive radiological scars.</p>
            </div>
          </div>
        </div>

      </div>

      <!-- ==================== SPECIALTY CONTENT: HIV–TB INTEGRATED CO-MODEL ==================== -->
      <div class="my-12 h-px bg-gradient-to-r from-transparent via-fuchsia-500/70 to-transparent"></div>
      <div class="flex items-center justify-center my-6">
        <span class="px-4 py-1.5 rounded-full bg-fuchsia-950/90 text-fuchsia-300 border border-fuchsia-800 text-xs font-mono font-bold tracking-widest uppercase shadow-lg flex items-center">
          <span class="w-2 h-2 rounded-full bg-fuchsia-400 animate-pulse mr-2"></span> CO-INFECTION // HIV–TB INTEGRATED RISK ASSESSMENT
        </span>
      </div>
      <div id="hospital-specialty-hivtb" class="glass-card rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 space-y-6">
        <div class="flex flex-wrap items-center justify-between border-b border-slate-800 pb-4 gap-3">
          <div>
            <h3 class="text-lg font-bold text-white flex items-center">
              <i class="fa-solid fa-network-wired text-fuchsia-400 mr-2"></i> HIV–TB Cross-Attention Multimodal Co-Infection Evaluator
            </h3>
            <p class="text-xs text-slate-400">Synchronized immune-pulmonary assessment bridging CD4/viral load profiles with chest radiography.</p>
          </div>
          <button onclick="runHIVTBIntegratedLive()" id="btn-run-hivtb-live" class="py-2 px-5 rounded-xl bg-gradient-to-r from-fuchsia-600 via-purple-600 to-indigo-600 hover:from-fuchsia-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-fuchsia-600/30 flex items-center transition-all">
            <i class="fa-solid fa-atom mr-1.5 animate-spin" style="animation-duration: 8s;"></i> RUN INTEGRATED CO-MODEL
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- Col 1: HIV Status Profile -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
            <span class="text-[11px] font-bold text-amber-400 uppercase tracking-wider block">HIV Immunological Profile</span>
            <div class="flex justify-between items-baseline">
              <span class="text-slate-400">CD4 Nadir:</span>
              <strong class="font-mono text-amber-300 font-bold" id="hivtb-cd4-val">145 cells/mm³</strong>
            </div>
            <div class="flex justify-between items-baseline">
              <span class="text-slate-400">Viral Load:</span>
              <strong class="font-mono text-rose-400 font-bold" id="hivtb-vl-val">124,000 copies/mL</strong>
            </div>
            <div class="flex justify-between items-baseline">
              <span class="text-slate-400">Status:</span>
              <span class="px-2 py-0.5 rounded bg-rose-950/80 text-rose-300 font-bold" id="hivtb-hiv-status">AHD Stage 4</span>
            </div>
          </div>

          <!-- Col 2: TB Screening Profile -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
            <span class="text-[11px] font-bold text-sky-400 uppercase tracking-wider block">TB Radiological &amp; Smear Profile</span>
            <div class="flex justify-between items-baseline">
              <span class="text-slate-400">CXR Lesion:</span>
              <strong class="font-mono text-sky-300 font-bold" id="hivtb-cxr-val">Apical Cavitation</strong>
            </div>
            <div class="flex justify-between items-baseline">
              <span class="text-slate-400">Sputum AFB:</span>
              <strong class="font-mono text-amber-300 font-bold" id="hivtb-afb-val">Grade 3+</strong>
            </div>
            <div class="flex justify-between items-baseline">
              <span class="text-slate-400">CRP Level:</span>
              <strong class="font-mono text-rose-400 font-bold" id="hivtb-crp-val">55.0 mg/L</strong>
            </div>
          </div>

          <!-- Col 3: Integrated Co-Risk Matrix -->
          <div class="p-4 rounded-2xl bg-fuchsia-950/40 border border-fuchsia-800 space-y-2 text-xs">
            <span class="text-[11px] font-bold text-fuchsia-300 uppercase tracking-wider block">Combined Risk Profile</span>
            <div class="text-3xl font-extrabold text-fuchsia-300 font-mono" id="hivtb-combined-score">77.0%</div>
            <span class="px-2 py-0.5 rounded-full bg-fuchsia-950 text-fuchsia-300 border border-fuchsia-700 font-bold inline-block text-[11px]" id="hivtb-profile-badge">HIGH CO-INFECTION RISK</span>
            <p class="text-[11px] text-slate-300 pt-1">Cross-attention fusion confirms severe dual vulnerability with coupled confidence of 77.0%.</p>
          </div>
        </div>

        <!-- WHO Co-Management Directive Box -->
        <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
          <h5 class="font-bold text-slate-200 flex items-center">
            <i class="fa-solid fa-pills text-fuchsia-400 mr-2\"></i> WHO Synchronized HIV-TB Clinical Care Protocol:
          </h5>
          <ul class="list-disc list-inside space-y-1.5 text-slate-300 text-[11px] leading-relaxed">
            <li><strong>Immediate TB Chemotherapy:</strong> Initiate 4-drug fixed-dose combination (2HRZE / 4HRE) without delay upon microbiological confirmation.</li>
            <li><strong>ART Initiation Timing:</strong> Start ART within 2 weeks of starting TB treatment (regardless of CD4 count), except in cryptococcal meningitis.</li>
            <li><strong>Rifampicin Drug-Drug Interaction:</strong> When co-administering Dolutegravir (DTG) with Rifampicin, double the DTG dose to 50mg twice daily due to CYP3A4 enzyme induction.</li>
          </ul>
        </div>
      </div>
'''

target = '      <!-- ==================== COMMON CLINICAL WORKBENCH CONTROLS ==================== -->'

file_path = r'C:\Users\harit\Desktop\QuantaMed-Platform\web\templates\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

if target in text:
    new_text = text.replace(target, html_snippet + '\n' + target)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Inserted HIV and TB tracks successfully into index.html!')
else:
    print('Target not found')
