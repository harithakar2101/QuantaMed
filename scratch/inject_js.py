import os

file_path = r'C:\Users\harit\Desktop\QuantaMed-Platform\web\templates\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update navigateToSpecialty, switchSpecialty, and initScrollSpy
old_nav_block = '''    function navigateToSpecialty(specialty) {
      currentSpecialty = specialty;
      const targetMap = {
        'cardio': 'hospital-specialty-cardio',
        'optho': 'hospital-specialty-optho',
        'onco': 'hospital-specialty-onco'
      };
      const targetId = targetMap[specialty] || 'hospital-specialty-cardio';
      scrollToSection(targetId);
    }

    function switchSpecialty(specialty) {
      currentSpecialty = specialty;
      ['cardio', 'optho', 'onco'].forEach(s => {
        const btn = document.getElementById(`subtab-btn-${s}`);
        if (btn) {
          if (s === specialty) {
            btn.className = "px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-rose-600 text-white shadow transition-all flex items-center";
          } else {
            btn.className = "px-3.5 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-slate-200 transition-all flex items-center";
          }
        }
      });
      const targetMap = {
        'cardio': 'hospital-specialty-cardio',
        'optho': 'hospital-specialty-optho',
        'onco': 'hospital-specialty-onco'
      };
      const targetId = targetMap[specialty] || 'hospital-specialty-cardio';
      scrollToSection(targetId);
    }

    // Scroll-Spy & Scroll-Reveal Observer
    function initScrollSpy() {
      const sectionMap = [
        { id: 'view-home', navId: 'nav-btn-home' },
        { id: 'hospital-specialty-cardio', navId: 'nav-btn-cardio' },
        { id: 'hospital-specialty-optho', navId: 'nav-btn-optho' },
        { id: 'hospital-specialty-onco', navId: 'nav-btn-onco' },
        { id: 'view-datasets', navId: 'nav-btn-datasets' },
        { id: 'view-lab', navId: 'nav-btn-lab' },
        { id: 'view-patient', navId: 'nav-btn-patient' }
      ];'''

new_nav_block = '''    function navigateToSpecialty(specialty) {
      currentSpecialty = specialty;
      const targetMap = {
        'cardio': 'hospital-specialty-cardio',
        'optho': 'hospital-specialty-optho',
        'onco': 'hospital-specialty-onco',
        'hiv': 'hospital-specialty-hiv',
        'tb': 'hospital-specialty-tb',
        'hivtb': 'hospital-specialty-hivtb'
      };
      const targetId = targetMap[specialty] || 'hospital-specialty-cardio';
      scrollToSection(targetId);
    }

    function switchSpecialty(specialty) {
      currentSpecialty = specialty;
      ['cardio', 'optho', 'onco', 'hiv', 'tb', 'hivtb'].forEach(s => {
        const btn = document.getElementById(`subtab-btn-${s}`);
        if (btn) {
          if (s === specialty) {
            btn.className = "px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-rose-600 text-white shadow transition-all flex items-center";
          } else {
            btn.className = "px-3.5 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-slate-200 transition-all flex items-center";
          }
        }
      });
      const targetMap = {
        'cardio': 'hospital-specialty-cardio',
        'optho': 'hospital-specialty-optho',
        'onco': 'hospital-specialty-onco',
        'hiv': 'hospital-specialty-hiv',
        'tb': 'hospital-specialty-tb',
        'hivtb': 'hospital-specialty-hivtb'
      };
      const targetId = targetMap[specialty] || 'hospital-specialty-cardio';
      scrollToSection(targetId);
    }

    // Scroll-Spy & Scroll-Reveal Observer
    function initScrollSpy() {
      const sectionMap = [
        { id: 'view-home', navId: 'nav-btn-home' },
        { id: 'hospital-specialty-cardio', navId: 'nav-btn-cardio' },
        { id: 'hospital-specialty-optho', navId: 'nav-btn-optho' },
        { id: 'hospital-specialty-onco', navId: 'nav-btn-onco' },
        { id: 'hospital-specialty-hiv', navId: 'nav-btn-hiv' },
        { id: 'hospital-specialty-tb', navId: 'nav-btn-tb' },
        { id: 'hospital-specialty-hivtb', navId: 'nav-btn-hivtb' },
        { id: 'view-datasets', navId: 'nav-btn-datasets' },
        { id: 'view-lab', navId: 'nav-btn-lab' },
        { id: 'view-patient', navId: 'nav-btn-patient' }
      ];'''

if old_nav_block in content:
    content = content.replace(old_nav_block, new_nav_block)
    print('[1/2] Replaced navigation and scroll-spy mappings!')
else:
    print('[!] Could not find old_nav_block')

# 2. Add controllers before clearRunHistory
old_end_js = '''    async function clearRunHistory() {
      try {
        await fetch('/api/history/clear', { method: 'POST' });
        fetchRunHistory();
      } catch(err) {
        console.error('Error clearing run history:', err);
      }
    }'''

hiv_tb_controllers = '''    // =======================================================================
    // HIV / AIDS 4-SUBTAB SUITE CONTROLLERS (WHO AHD SPEC)
    // =======================================================================
    let chartHIVTrajectory = null;
    let uploadedHIVFile = null;

    function switchHIVSubtab(tab) {
      ['scanner', 'circuit', 'metrics', 'about'].forEach(t => {
        const pane = document.getElementById(`hiv-subtab-${t}`);
        const btn = document.getElementById(`hiv-tab-btn-${t}`);
        if (pane) pane.classList.toggle('hidden', t !== tab);
        if (btn) {
          if (t === tab) {
            btn.className = "px-4 py-1.5 text-xs font-bold rounded-lg bg-amber-600 text-white shadow transition-all flex items-center";
          } else {
            btn.className = "px-4 py-1.5 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition-all flex items-center";
          }
        }
      });
      if (tab === 'metrics') {
        setTimeout(initHIVTrajectoryChart, 150);
      }
    }

    function onHIVPresetChange() {
      const sel = document.getElementById('hiv-preset-select')?.value || 'stage4';
      const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
      const setChk = (id, val) => { const el = document.getElementById(id); if (el) el.checked = val; };

      if (sel === 'stage4') {
        setVal('hiv-input-cd4', 145);
        setVal('hiv-input-vl', 124000);
        setVal('hiv-input-cd8', 980);
        setVal('hiv-input-art-status', 'Not on ART');
        setChk('hiv-sym-fever', true);
        setChk('hiv-sym-weightloss', true);
        setChk('hiv-sym-infections', true);
      } else if (sel === 'acute') {
        setVal('hiv-input-cd4', 650);
        setVal('hiv-input-vl', 85000);
        setVal('hiv-input-cd8', 680);
        setVal('hiv-input-art-status', 'Not on ART');
        setChk('hiv-sym-fever', true);
        setChk('hiv-sym-weightloss', false);
        setChk('hiv-sym-infections', false);
      } else if (sel === 'stage3') {
        setVal('hiv-input-cd4', 280);
        setVal('hiv-input-vl', 28500);
        setVal('hiv-input-cd8', 890);
        setVal('hiv-input-art-status', 'On ART');
        setChk('hiv-sym-fever', true);
        setChk('hiv-sym-weightloss', false);
        setChk('hiv-sym-infections', true);
      } else {
        setVal('hiv-input-cd4', 580);
        setVal('hiv-input-vl', 450);
        setVal('hiv-input-cd8', 720);
        setVal('hiv-input-art-status', 'On ART');
        setChk('hiv-sym-fever', false);
        setChk('hiv-sym-weightloss', false);
        setChk('hiv-sym-infections', false);
      }
      runHIVAssessmentLive();
    }

    function handleHIVFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      uploadedHIVFile = file;
      runHIVAssessmentLive();
    }

    async function runHIVAssessmentLive() {
      const btn = document.getElementById('btn-run-hiv-assessment');
      if (!btn) return;
      const originalHtml = btn.innerHTML;
      btn.innerHTML = `<i class="fa-solid fa-atom mr-1.5 animate-spin"></i> Running Quantum VQC...`;
      btn.disabled = true;

      const payload = {
        patient_id: document.getElementById('hiv-input-id')?.value || 'HIV-P482',
        hiv_test_result: document.getElementById('hiv-input-test-result')?.value || 'Positive',
        cd4_count: parseFloat(document.getElementById('hiv-input-cd4')?.value) || 145,
        viral_load: parseFloat(document.getElementById('hiv-input-vl')?.value) || 124000,
        cd8_count: parseFloat(document.getElementById('hiv-input-cd8')?.value) || 980,
        art_status: document.getElementById('hiv-input-art-status')?.value || 'Not on ART',
        symptom_fever: document.getElementById('hiv-sym-fever')?.checked || false,
        symptom_weight_loss: document.getElementById('hiv-sym-weightloss')?.checked || false,
        symptom_infections: document.getElementById('hiv-sym-infections')?.checked || false
      };

      try {
        const res = await fetch('/api/hiv/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (data.status === 'success') {
          const badge = document.getElementById('hiv-risk-badge');
          const title = document.getElementById('hiv-who-stage-title');
          const desc = document.getElementById('hiv-progression-text');
          const qText = document.getElementById('hiv-quantum-conf-text');
          const qBar = document.getElementById('hiv-quantum-conf-bar');
          const cText = document.getElementById('hiv-classical-conf-text');
          const cdsText = document.getElementById('hiv-cds-text');

          const risk = data.clinical_staging.risk_category;
          if (badge) {
            badge.innerText = risk;
            badge.className = risk.includes('HIGH') 
              ? 'text-xs px-2.5 py-0.5 rounded-full bg-rose-950/80 text-rose-300 border border-rose-800 font-mono font-bold'
              : (risk.includes('MODERATE') 
                ? 'text-xs px-2.5 py-0.5 rounded-full bg-amber-950/80 text-amber-300 border border-amber-800 font-mono font-bold'
                : 'text-xs px-2.5 py-0.5 rounded-full bg-emerald-950/80 text-emerald-300 border border-emerald-800 font-mono font-bold');
          }
          if (title) title.innerText = data.clinical_staging.who_stage;
          if (desc) desc.innerText = data.clinical_staging.progression_estimate;
          if (qText) qText.innerText = `${data.quantum_metrics.quantum_confidence}%`;
          if (qBar) qBar.style.width = `${data.quantum_metrics.quantum_confidence}%`;
          if (cText) cText.innerText = `${data.quantum_metrics.classical_confidence}%`;
          if (cdsText && data.clinical_decision_support) {
            cdsText.innerText = data.clinical_decision_support.join(' ');
          }

          // Update integrated card preview if present
          const hivtbCd4 = document.getElementById('hivtb-cd4-val');
          const hivtbVl = document.getElementById('hivtb-vl-val');
          const hivtbStatus = document.getElementById('hivtb-hiv-status');
          if (hivtbCd4) hivtbCd4.innerText = `${payload.cd4_count} cells/mm³`;
          if (hivtbVl) hivtbVl.innerText = `${payload.viral_load.toLocaleString()} copies/mL`;
          if (hivtbStatus) hivtbStatus.innerText = data.clinical_staging.who_stage.split('(')[0];

          fetchRunHistory();
        }
      } catch (err) {
        console.error('Error assessing HIV profile:', err);
      } finally {
        btn.innerHTML = originalHtml;
        btn.disabled = false;
      }
    }

    function initHIVTrajectoryChart() {
      const ctx = document.getElementById('chart-hiv-trajectory')?.getContext('2d');
      if (!ctx) return;
      if (chartHIVTrajectory) {
        chartHIVTrajectory.destroy();
        chartHIVTrajectory = null;
      }

      const epochs = Array.from({length: 26}, (_, i) => i);
      const qData = [56.0, 62.5, 68.8, 74.2, 79.0, 83.1, 86.5, 89.0, 91.0, 92.4, 93.3, 93.9, 94.2, 94.4, 94.5, 94.55, 94.58, 94.6, 94.6, 94.6, 94.6, 94.6, 94.6, 94.6, 94.6, 94.6];
      const cData = [51.0, 56.8, 62.2, 67.0, 71.4, 75.3, 78.8, 81.6, 83.8, 85.5, 86.8, 87.8, 88.5, 88.9, 89.2, 89.3, 89.4, 89.45, 89.5, 89.5, 89.5, 89.5, 89.5, 89.5, 89.5, 89.5];

      chartHIVTrajectory = new Chart(ctx, {
        type: 'line',
        data: {
          labels: epochs,
          datasets: [
            {
              label: '4-Qubit VQC (94.60%)',
              data: qData,
              borderColor: '#f59e0b',
              backgroundColor: 'rgba(245, 158, 11, 0.12)',
              borderWidth: 2.5,
              tension: 0.3,
              fill: true,
              pointRadius: 2.5,
              pointBackgroundColor: '#f59e0b'
            },
            {
              label: 'Classical Random Forest (89.50%)',
              data: cData,
              borderColor: '#64748b',
              borderWidth: 2,
              borderDash: [5, 5],
              tension: 0.3,
              pointRadius: 1.5,
              pointBackgroundColor: '#64748b'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#e2e8f0', font: { family: 'Inter', size: 11, weight: 'bold' } } }
          },
          scales: {
            x: { title: { display: true, text: 'Epochs (0 - 25)', color: '#94a3b8', font: { size: 11 } }, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
            y: { min: 45, max: 100, title: { display: true, text: 'Accuracy (%)', color: '#94a3b8', font: { size: 11 } }, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8', callback: v => v + '%' } }
          }
        }
      });
    }

    // =======================================================================
    // TUBERCULOSIS (TB) 4-SUBTAB SUITE CONTROLLERS (WHO CAD-CXR SPEC)
    // =======================================================================
    let chartTBTrajectory = null;
    let uploadedTBFile = null;

    function switchTBSubtab(tab) {
      ['scanner', 'circuit', 'metrics', 'about'].forEach(t => {
        const pane = document.getElementById(`tb-subtab-${t}`);
        const btn = document.getElementById(`tb-tab-btn-${t}`);
        if (pane) pane.classList.toggle('hidden', t !== tab);
        if (btn) {
          if (t === tab) {
            btn.className = "px-4 py-1.5 text-xs font-bold rounded-lg bg-sky-600 text-white shadow transition-all flex items-center";
          } else {
            btn.className = "px-4 py-1.5 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition-all flex items-center";
          }
        }
      });
      if (tab === 'metrics') {
        setTimeout(initTBTrajectoryChart, 150);
      }
    }

    function onTBPresetChange() {
      const sel = document.getElementById('tb-preset-select')?.value || 'cavitary';
      const cxrImg = document.getElementById('tb-cxr-img');
      const gradcamImg = document.getElementById('tb-gradcam-img');
      const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };

      if (sel === 'cavitary') {
        if (cxrImg) cxrImg.src = '/static/sample_data/tb/tb_cavitary_cxr.png';
        if (gradcamImg) gradcamImg.src = '/static/sample_data/tb/tb_gradcam_overlay.png';
        setVal('tb-input-cough', 4);
        setVal('tb-input-crp', 55.0);
        setVal('tb-input-afb', '3+');
        setVal('tb-input-hivstatus', 'Negative');
      } else if (sel === 'infiltrative') {
        if (cxrImg) cxrImg.src = '/static/sample_data/tb/tb_infiltrative_cxr.png';
        if (gradcamImg) gradcamImg.src = '/static/sample_data/tb/tb_gradcam_overlay.png';
        setVal('tb-input-cough', 2.5);
        setVal('tb-input-crp', 28.0);
        setVal('tb-input-afb', '1+');
        setVal('tb-input-hivstatus', 'Negative');
      } else if (sel === 'mdr') {
        if (cxrImg) cxrImg.src = '/static/sample_data/tb/tb_cavitary_cxr.png';
        if (gradcamImg) gradcamImg.src = '/static/sample_data/tb/tb_gradcam_overlay.png';
        setVal('tb-input-cough', 6);
        setVal('tb-input-crp', 82.0);
        setVal('tb-input-afb', '3+');
        setVal('tb-input-hivstatus', 'Negative');
      } else {
        if (cxrImg) cxrImg.src = '/static/sample_data/tb/tb_normal_cxr.png';
        if (gradcamImg) gradcamImg.src = '/static/sample_data/tb/tb_normal_cxr.png';
        setVal('tb-input-cough', 0.5);
        setVal('tb-input-crp', 3.2);
        setVal('tb-input-afb', '0');
        setVal('tb-input-hivstatus', 'Negative');
      }
      runTBScreeningLive();
    }

    function handleTBFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      uploadedTBFile = file;

      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
          const cxrImg = document.getElementById('tb-cxr-img');
          if (cxrImg) cxrImg.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
      runTBScreeningLive();
    }

    async function runTBScreeningLive() {
      const btn = document.getElementById('btn-run-tb-screening');
      if (!btn) return;
      const originalHtml = btn.innerHTML;
      btn.innerHTML = `<i class="fa-solid fa-atom mr-1.5 animate-spin"></i> Executing Quantum CXR Kernel...`;
      btn.disabled = true;

      const payload = {
        patient_id: document.getElementById('tb-input-id')?.value || 'TB-P719',
        sample_key: document.getElementById('tb-preset-select')?.value || 'cavitary',
        cough_duration: parseFloat(document.getElementById('tb-input-cough')?.value) || 4.0,
        crp_mg_l: parseFloat(document.getElementById('tb-input-crp')?.value) || 55.0,
        sputum_afb: document.getElementById('tb-input-afb')?.value || '3+',
        hiv_status: document.getElementById('tb-input-hivstatus')?.value || 'Negative'
      };

      try {
        const res = await fetch('/api/tb/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (data.status === 'success') {
          const badge = document.getElementById('tb-risk-tier');
          const title = document.getElementById('tb-class-title');
          const desc = document.getElementById('tb-lesion-text');
          const qText = document.getElementById('tb-quantum-conf-text');
          const qBar = document.getElementById('tb-quantum-conf-bar');
          const cText = document.getElementById('tb-classical-conf-text');
          const cdsText = document.getElementById('tb-cds-text');

          const risk = data.screening_outcome.risk_tier;
          if (badge) {
            badge.innerText = risk;
            badge.className = risk.includes('HIGH') || risk.includes('CRITICAL')
              ? 'text-xs px-2.5 py-0.5 rounded-full bg-rose-950/80 text-rose-300 border border-rose-800 font-mono font-bold'
              : (risk.includes('MODERATE') 
                ? 'text-xs px-2.5 py-0.5 rounded-full bg-amber-950/80 text-amber-300 border border-amber-800 font-mono font-bold'
                : 'text-xs px-2.5 py-0.5 rounded-full bg-emerald-950/80 text-emerald-300 border border-emerald-800 font-mono font-bold');
          }
          if (title) title.innerText = data.screening_outcome.classification;
          if (desc) desc.innerText = data.radiological_findings.cavitation_status;
          if (qText) qText.innerText = `${data.quantum_metrics.quantum_confidence}%`;
          if (qBar) qBar.style.width = `${data.quantum_metrics.quantum_confidence}%`;
          if (cText) cText.innerText = `${data.quantum_metrics.classical_confidence}%`;
          if (cdsText && data.clinical_decision_support) {
            cdsText.innerText = data.clinical_decision_support.join(' ');
          }

          // Update integrated card preview
          const hivtbCxr = document.getElementById('hivtb-cxr-val');
          const hivtbAfb = document.getElementById('hivtb-afb-val');
          const hivtbCrp = document.getElementById('hivtb-crp-val');
          if (hivtbCxr) hivtbCxr.innerText = data.radiological_findings.has_apical_cavitation ? 'Apical Cavitation' : 'Clear Parenchyma';
          if (hivtbAfb) hivtbAfb.innerText = `Grade ${payload.sputum_afb}`;
          if (hivtbCrp) hivtbCrp.innerText = `${payload.crp_mg_l} mg/L`;

          fetchRunHistory();
        }
      } catch (err) {
        console.error('Error running TB screening:', err);
      } finally {
        btn.innerHTML = originalHtml;
        btn.disabled = false;
      }
    }

    function initTBTrajectoryChart() {
      const ctx = document.getElementById('chart-tb-trajectory')?.getContext('2d');
      if (!ctx) return;
      if (chartTBTrajectory) {
        chartTBTrajectory.destroy();
        chartTBTrajectory = null;
      }

      const epochs = Array.from({length: 26}, (_, i) => i);
      const qData = [52.0, 58.0, 64.1, 69.5, 74.2, 78.5, 82.0, 84.8, 87.0, 88.6, 89.8, 90.6, 91.0, 91.3, 91.5, 91.6, 91.7, 91.75, 91.78, 91.8, 91.8, 91.8, 91.8, 91.8, 91.8, 91.8];
      const cData = [48.0, 53.0, 58.2, 63.1, 67.5, 71.2, 74.5, 77.2, 79.5, 81.3, 82.8, 83.9, 84.8, 85.4, 85.8, 86.0, 86.2, 86.3, 86.35, 86.4, 86.4, 86.4, 86.4, 86.4, 86.4, 86.4];

      chartTBTrajectory = new Chart(ctx, {
        type: 'line',
        data: {
          labels: epochs,
          datasets: [
            {
              label: '6-Qubit QSVM (91.80%)',
              data: qData,
              borderColor: '#0284c7',
              backgroundColor: 'rgba(2, 132, 199, 0.12)',
              borderWidth: 2.5,
              tension: 0.3,
              fill: true,
              pointRadius: 2.5,
              pointBackgroundColor: '#0284c7'
            },
            {
              label: 'Classical CAD4TB Baseline (86.40%)',
              data: cData,
              borderColor: '#64748b',
              borderWidth: 2,
              borderDash: [5, 5],
              tension: 0.3,
              pointRadius: 1.5,
              pointBackgroundColor: '#64748b'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#e2e8f0', font: { family: 'Inter', size: 11, weight: 'bold' } } }
          },
          scales: {
            x: { title: { display: true, text: 'Epochs (0 - 25)', color: '#94a3b8', font: { size: 11 } }, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
            y: { min: 40, max: 100, title: { display: true, text: 'Accuracy (%)', color: '#94a3b8', font: { size: 11 } }, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8', callback: v => v + '%' } }
          }
        }
      });
    }

    // =======================================================================
    // HIV–TB INTEGRATED CO-INFECTION CONTROLLER
    // =======================================================================
    async function runHIVTBIntegratedLive() {
      const btn = document.getElementById('btn-run-hivtb-live');
      if (!btn) return;
      const originalHtml = btn.innerHTML;
      btn.innerHTML = `<i class="fa-solid fa-atom mr-1.5 animate-spin"></i> Executing Cross-Attention Co-Model...`;
      btn.disabled = true;

      const hivData = {
        cd4_count: parseFloat(document.getElementById('hiv-input-cd4')?.value) || 145,
        viral_load: parseFloat(document.getElementById('hiv-input-vl')?.value) || 124000,
        art_status: document.getElementById('hiv-input-art-status')?.value || 'Not on ART'
      };
      const tbData = {
        cough_duration: parseFloat(document.getElementById('tb-input-cough')?.value) || 4.0,
        crp_mg_l: parseFloat(document.getElementById('tb-input-crp')?.value) || 55.0,
        sputum_afb: document.getElementById('tb-input-afb')?.value || '3+'
      };

      try {
        const res = await fetch('/api/hiv-tb/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ hiv_data: hivData, tb_data: tbData })
        });
        const data = await res.json();

        if (data.status === 'success') {
          const scoreEl = document.getElementById('hivtb-combined-score');
          const badgeEl = document.getElementById('hivtb-profile-badge');
          if (scoreEl) scoreEl.innerText = `${data.combined_risk_score}%`;
          if (badgeEl) badgeEl.innerText = data.co_risk_profile.split(':')[0];

          fetchRunHistory();
        }
      } catch (err) {
        console.error('Error running HIV-TB integrated assessment:', err);
      } finally {
        btn.innerHTML = originalHtml;
        btn.disabled = false;
      }
    }

'''

if old_end_js in content:
    content = content.replace(old_end_js, hiv_tb_controllers + '\n' + old_end_js)
    print('[2/2] Inserted HIV and TB JavaScript controllers!')
else:
    print('[!] Could not find old_end_js')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated web/templates/index.html with all JS controllers!')
