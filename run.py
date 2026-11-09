#!/usr/bin/env python3
"""
QuantaMed: National Hybrid Quantum Machine Learning Clinical Platform
Single Entry-Point Launcher for VS Code & Terminal Execution
Egreen Quanta MedTech & BioTech Healthcare Intelligence
"""

import sys
import os
import threading
import webbrowser
import time

# Ensure workspace root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Force stdout encoding safety for Windows PowerShell/CMD
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def open_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:5000")
    except Exception as e:
        print(f"[!] Could not automatically open browser: {e}")

def main():
    print("=" * 80)
    print("   QuantaMed: NATIONAL HYBRID QUANTUM MACHINE LEARNING CLINICAL PLATFORM")
    print("   Domains: Cardiology, Ophthalmology (Lenscode 2.0), Pan-Cancer Oncology")
    print("   Architecture: 7-Layer Deep Hybrid Quantum-Classical Medical Intelligence")
    print("=" * 80)
    print("   [*] Medical Scope : 12-Lead ECG + Cardiac Biomarkers (hs-cTnI, NT-proBNP)")
    print("   [*] Quantum Engine: 4-Qubit Amplitude Encoding & ZZ-Feature Entanglement")
    print("   [*] Explainer     : Grad-CAM Temporal ECG Heatmap + DiCE Counterfactuals")
    print("   [*] Standards     : HL7 FHIR R4 Bundle + ICD-11 (BA80.2, BC60.1, MC80)")
    print("-" * 80)
    print("   >> Local Web Server: http://127.0.0.1:5000")
    print("   >> API Endpoint    : http://127.0.0.1:5000/api/cardio/predict")
    print("   >> Health Check    : http://127.0.0.1:5000/api/cardio/health")
    print("=" * 80)
    print("   Starting local server... Press Ctrl+C in terminal to stop.")

    # Auto-open browser tab in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Auto-detect and install missing dependencies if run in a fresh or alternate python environment
    try:
        import flask
        import flask_cors
        import pandas
        import openpyxl
    except (ImportError, ModuleNotFoundError):
        print(f"[!] Required packages not found in Python interpreter: {sys.executable}")
        print("[*] Automatically installing dependencies from requirements.txt...")
        import subprocess
        req_file = os.path.join(BASE_DIR, "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("[+] Dependencies installed successfully!\n")

    from web.app import app
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    main()
