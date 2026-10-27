import json, urllib.request, xml.etree.ElementTree as ET, datetime

FEEDS = [
    ("الجزيرة نت", "https://www.aljazeera.net/aljazeerarss/a7c186be-1baa-4bd4-9d80-a84db769f779/73d0e1b4-532f-45ef-b135-bfdff8b8cab9"),
    ("بي بي سي عربي", "https://feeds.bbci.co.uk/arabic/rss.xml"),
]

lists = []
for name, url in FEEDS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
        titles = [(i.findtext("title") or "").strip() for i in root.iter("item")]
        lists.append([{"src": name, "title": t} for t in titles if t][:8])
        print("ok", name, len(lists[-1]))
    except Exception as e:
        print("fail", name, e)

merged = []
for i in range(8):
    for lst in lists:
        if i < len(lst):
            merged.append(lst[i])

if merged:
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.datetime.utcnow().isoformat() + "Z", "items": merged}, f, ensure_ascii=False)
