import urllib.request
import re
import json

def get_yt_details(vid):
    url = f'https://www.youtube.com/watch?v={vid}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    
    m_title = re.search(r'<meta name="title" content="([^"]+)">', html)
    m_desc = re.search(r'<meta name="description" content="([^"]+)">', html)
    short_desc = re.findall(r'"shortDescription":"(.*?)(?<!\\)"', html)
    
    # Check for captions
    captions = []
    caption_tracks = re.findall(r'"captionTracks":(\[.*?\])', html)
    caption_text = ""
    if caption_tracks:
        try:
            tracks = json.loads(caption_tracks[0])
            for track in tracks:
                t_url = track.get('baseUrl')
                if t_url:
                    c_req = urllib.request.Request(t_url, headers={'User-Agent': 'Mozilla/5.0'})
                    c_xml = urllib.request.urlopen(c_req).read().decode('utf-8', errors='ignore')
                    lines = re.findall(r'<text[^>]*>(.*?)</text>', c_xml)
                    caption_text = " ".join(lines)
                    break
        except Exception as e:
            caption_text = f"Error: {e}"

    return {
        'title': m_title.group(1) if m_title else '',
        'meta_desc': m_desc.group(1) if m_desc else '',
        'short_desc': short_desc[0] if short_desc else '',
        'captions': caption_text[:3000]
    }

print("=== VIDEO 1 (nnZ876i31S8) ===")
print(json.dumps(get_yt_details('nnZ876i31S8'), indent=2))
print("\n=== VIDEO 2 (OwmYENkDz0Q) ===")
print(json.dumps(get_yt_details('OwmYENkDz0Q'), indent=2))
