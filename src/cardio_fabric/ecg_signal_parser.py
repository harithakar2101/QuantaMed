import numpy as np
from typing import Dict, Any, List, Tuple

class ECGSignalParser:
    """
    12-Lead ECG Signal Processor and Synthesizer.
    Models leads I, II, III, aVR, aVL, aVF, V1-V6 with electrophysiological metrics.
    """
    def __init__(self, sampling_rate: int = 250):
        self.fs = sampling_rate # 250 Hz (10 sec = 2500 samples)
        self.lead_names = ["Lead I", "Lead II", "Lead III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]

    def generate_synthetic_12lead(
        self,
        duration_sec: float = 10.0,
        rhythm_type: str = "normal",
        heart_rate: float = 72.0,
        st_elevation_mv: float = 0.0,
        qtc_ms: float = 410.0
    ) -> Dict[str, Any]:
        """
        Generates calibrated 12-lead ECG signals simulating normal, ischemic, or arrhythmic rhythms.
        """
        n_samples = int(duration_sec * self.fs)
        t = np.linspace(0, duration_sec, n_samples)
        
        rr_interval_sec = 60.0 / max(heart_rate, 30.0)
        
        # Build base single-lead cardiac cycle (P-Q-R-S-T)
        lead_signals = {}
        
        # Generate R-peak trigger times
        if rhythm_type == "atrial_fibrillation":
            # Irregular R-R intervals (Lorenz plot dispersion)
            rng = np.random.RandomState(42)
            r_times = []
            cur_t = 0.3
            while cur_t < duration_sec:
                r_times.append(cur_t)
                delta = rr_interval_sec * rng.uniform(0.65, 1.45)
                cur_t += delta
        else:
            r_times = np.arange(0.3, duration_sec, rr_interval_sec)
            
        r_peaks = [int(rt * self.fs) for rt in r_times if int(rt * self.fs) < n_samples]

        # Generate each lead with standard projection matrices
        lead_gains = {
            "Lead I": 0.8, "Lead II": 1.0, "Lead III": 0.6,
            "aVR": -0.9, "aVL": 0.4, "aVF": 0.7,
            "V1": 0.5, "V2": 0.9, "V3": 1.2,
            "V4": 1.3, "V5": 1.1, "V6": 0.85
        }
        
        for lead_name, gain in lead_gains.items():
            sig = np.zeros(n_samples)
            
            for rp in r_peaks:
                # 1. P-Wave (absent in Atrial Fibrillation)
                if rhythm_type != "atrial_fibrillation":
                    p_center = rp - int(0.16 * self.fs)
                    if 0 <= p_center < n_samples:
                        p_width = int(0.04 * self.fs)
                        idx = np.arange(max(0, p_center - p_width*2), min(n_samples, p_center + p_width*2))
                        sig[idx] += 0.15 * gain * np.exp(-((idx - p_center) / (p_width + 1e-6))**2)
                        
                # 2. Q-Wave (negative defection)
                q_center = rp - int(0.03 * self.fs)
                if 0 <= q_center < n_samples:
                    q_width = int(0.015 * self.fs)
                    idx = np.arange(max(0, q_center - q_width*2), min(n_samples, q_center + q_width*2))
                    sig[idx] -= 0.20 * gain * np.exp(-((idx - q_center) / (q_width + 1e-6))**2)

                # 3. R-Peak (high amplitude)
                if 0 <= rp < n_samples:
                    r_width = int(0.02 * self.fs)
                    idx = np.arange(max(0, rp - r_width*2), min(n_samples, rp + r_width*2))
                    sig[idx] += 1.30 * gain * np.exp(-((idx - rp) / (r_width + 1e-6))**2)

                # 4. S-Wave (negative overshoot)
                s_center = rp + int(0.03 * self.fs)
                if 0 <= s_center < n_samples:
                    s_width = int(0.02 * self.fs)
                    idx = np.arange(max(0, s_center - s_width*2), min(n_samples, s_center + s_width*2))
                    sig[idx] -= 0.35 * gain * np.exp(-((idx - s_center) / (s_width + 1e-6))**2)

                # 5. ST-Segment & T-Wave
                st_center = rp + int(0.10 * self.fs)
                t_center = rp + int((qtc_ms / 1000.0 * 0.70) * self.fs)
                
                # ST deviation for ischemia (leads II, V4-V6)
                if "V" in lead_name or lead_name == "Lead II":
                    st_shift = st_elevation_mv
                else:
                    st_shift = st_elevation_mv * 0.4
                    
                if 0 <= st_center < n_samples:
                    idx = np.arange(max(0, st_center - int(0.04*self.fs)), min(n_samples, st_center + int(0.06*self.fs)))
                    sig[idx] += st_shift
                    
                # T-wave
                if 0 <= t_center < n_samples:
                    t_width = int(0.07 * self.fs)
                    t_amp = 0.35 * gain
                    if st_elevation_mv < -0.10: # Ischemic T-wave inversion
                        t_amp = -0.28 * gain
                    idx = np.arange(max(0, t_center - t_width*2), min(n_samples, t_center + t_width*2))
                    sig[idx] += t_amp * np.exp(-((idx - t_center) / (t_width + 1e-6))**2)
                    
            # Add subtle baseline physiological noise
            sig += np.random.normal(0, 0.015, n_samples)
            # Downsample for lightweight web delivery (100 Hz, 1000 points)
            step = max(1, n_samples // 1000)
            lead_signals[lead_name] = [round(float(v), 3) for v in sig[::step]]

        # Compute Electrophysiological Metrics
        rr_diffs = np.diff(r_times) * 1000.0 if len(r_times) > 1 else [rr_interval_sec * 1000.0]
        hrv_sdnn = float(np.std(rr_diffs)) if len(rr_diffs) > 1 else 35.0
        
        metrics = {
            "rhythm_diagnosis": "Atrial Fibrillation" if rhythm_type == "atrial_fibrillation" else ("Ischemic Sinus Rhythm" if abs(st_elevation_mv) > 0.1 else "Normal Sinus Rhythm"),
            "heart_rate_bpm": round(float(heart_rate), 1),
            "pr_interval_ms": 0 if rhythm_type == "atrial_fibrillation" else 162.0,
            "qrs_duration_ms": 88.0,
            "qt_interval_ms": round(qtc_ms * np.sqrt(rr_interval_sec), 1),
            "qtc_bazett_ms": round(float(qtc_ms), 1),
            "st_deviation_mv": round(float(st_elevation_mv), 2),
            "hrv_sdnn_ms": round(hrv_sdnn, 1),
            "r_peak_count": len(r_peaks)
        }

        return {
            "leads": lead_signals,
            "metrics": metrics,
            "sampling_rate_hz": self.fs
        }
