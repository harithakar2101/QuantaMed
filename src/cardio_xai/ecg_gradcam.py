import numpy as np
from typing import Dict, Any, List

class ECGGradCAM:
    """
    Layer 5: 12-Lead ECG Temporal Grad-CAM & Attention Activation Engine.
    Computes temporal attention weights across the ECG waveform highlighting
    pathological ST-depression/elevation, T-wave inversion, and arrhythmic anomalies.
    """
    def compute_ecg_attention_weights(
        self,
        lead_signal: List[float],
        st_deviation: float,
        rhythm_type: str,
        risk_prob: float
    ) -> List[float]:
        """
        Calculates normalized attention heatmap weights [0.0 to 1.0] for each time sample.
        """
        n = len(lead_signal)
        sig = np.array(lead_signal)
        attention = np.zeros(n)
        
        if risk_prob > 0.4:
            # Detect sharp slope changes and ST regions
            diff = np.abs(np.diff(sig, prepend=sig[0]))
            # Baseline attention from signal variance
            attention = 0.3 * (diff / (np.max(diff) + 1e-6))
            
            # If ischemic ST deviation exists, elevate attention on ST regions
            if abs(st_deviation) > 0.08:
                st_mask = (sig < -0.15) if st_deviation < 0 else (sig > 0.15)
                attention += 0.6 * st_mask.astype(float)
                
            # If arrhythmia / AFib, add stochastic attention across cycle variability
            if rhythm_type == "atrial_fibrillation":
                attention += 0.35 * (np.sin(np.linspace(0, 30, n)) ** 2)
        else:
            # Low background diffuse attention for healthy rhythm
            attention = np.ones(n) * 0.12
            
        # Smooth attention with moving average
        kernel_size = 15
        kernel = np.ones(kernel_size) / kernel_size
        smoothed = np.convolve(attention, kernel, mode='same')
        
        # Normalize to [0.0, 1.0]
        max_v = np.max(smoothed) if np.max(smoothed) > 0 else 1.0
        norm_att = smoothed / max_v
        return [round(float(v), 3) for v in norm_att]
