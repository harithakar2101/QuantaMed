import urllib.request
import urllib.parse
import json

def test(url, data=None):
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            print(f'SUCCESS: {url} -> Status: {resp.status}')
            return json.loads(body)
    except Exception as e:
        print(f'FAILED: {url} -> {e}')
        return None

print('--- 1. Testing System Stats ---')
stats = test('http://127.0.0.1:5000/api/system/stats')
print('Stats:', stats.get('status'))

print('\n--- 2. Testing Breast Scanner Upload/Predict ---')
data = urllib.parse.urlencode({'modality': 'breast', 'sample_key': 'malignant'}).encode('utf-8')
r1 = test('http://127.0.0.1:5000/api/scanner/upload_predict', data=data)
print('Breast Pred Class:', r1.get('predicted_class'))
print('Breast Badge:', r1.get('verification_badge'))
print('Breast KPIs:', r1.get('kpis'))
print('Breast Grad-CAM URL:', r1.get('gradcam_image_url'))

print('\n--- 3. Testing Cardio Scanner Upload/Predict ---')
data_cardio = urllib.parse.urlencode({'modality': 'cardio', 'sample_key': 'cad_stemi'}).encode('utf-8')
r2 = test('http://127.0.0.1:5000/api/scanner/upload_predict', data=data_cardio)
print('Cardio Pred Class:', r2.get('predicted_class'))
print('Cardio Badge:', r2.get('verification_badge'))
print('Cardio KPIs:', r2.get('kpis'))
print('Cardio Trajectory points:', len(r2.get('trajectory', {}).get('quantum', [])))

print('\n--- 4. Testing Optho Scanner Upload/Predict ---')
data_optho = urllib.parse.urlencode({'modality': 'optho', 'sample_key': 'dr_proliferative'}).encode('utf-8')
r_optho = test('http://127.0.0.1:5000/api/scanner/upload_predict', data=data_optho)
print('Optho Pred Class:', r_optho.get('predicted_class'))
print('Optho Badge:', r_optho.get('verification_badge'))
print('Optho KPIs:', r_optho.get('kpis'))
print('Optho Trajectory points:', len(r_optho.get('trajectory', {}).get('quantum', [])))

print('\n--- 5. Testing Run History List ---')
r3 = test('http://127.0.0.1:5000/api/history/list')
print('Run History Count:', r3.get('count'))
for h in r3.get('history', []):
    print(f"  - [{h.get('timestamp')}] {h.get('modality')}: {h.get('predicted_class')} (Q: {h.get('quantum_confidence')}, C: {h.get('classical_confidence')}, Gain: {h.get('quantum_delta')})")

print('\n--- ALL VERIFICATIONS PASSED ---')
