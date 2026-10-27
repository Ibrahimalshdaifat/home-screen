import json, urllib.request, xml.etree.ElementTree as ET, datetime

FEEDS = [
    ("عمون", "https://www.ammonnews.net/rss.php?type=news&id=78"),
    ("الغد", "https://alghad.com/feed"),
    ("جو 24", "https://jo24.net/feed/"),
    ("الجزيرة نت", "https://www.aljazeera.net/aljazeerarss/a7c186be-1baa-4bd4-9d80-a84db769f779/73d0e1b4-532f-45ef-b135-bfdff8b8cab9"),
    ("بي بي سي عربي", "https://feeds.bbci.co.uk/arabic/rss.xml"),
]

# ---- فلترة العناوين: تُعرض فقط الأخبار المهمة (سياسية واقتصادية واجتماعية) ----
# عنوان فيه كلمة من قائمة الاستبعاد يُحذف. وبعدها لا يُقبل إلا عنوان فيه كلمة من قائمة القبول.
# عدّل القائمتين كما تشاء: أضف كلمة لقبول أو استبعاد نوع من الأخبار.
EXCLUDE = ["نشاط ممتع", "طفلك", "وصفة", "الأبراج", "حظك", "الرياضة", "رياضي", "كرة", "الدوري", "مباراة",
           "فنان", "مسلسل", "فيلم", "أغنية", "موضة", "رجيم", "حمية", "طبخ", "آيفون", "ألعاب",
           "عيد ميلاد", "زفاف", "مهرجان", "حصالة", "نصائح", "فوائد", "أسرار"]
INCLUDE = ["الحكومة", "رئيس", "وزير", "وزارة", "مجلس", "النواب", "الأعيان", "الملك", "ولي العهد", "سياس",
           "برلمان", "انتخاب", "قرار", "اتفاق", "مفاوضات", "هدنة", "حرب", "غارات", "قصف", "عدوان", "غزة",
           "فلسطين", "الضفة", "القدس", "الأقصى", "إسرائيل", "الاحتلال", "سوريا", "لبنان", "العراق", "إيران",
           "أمريكا", "واشنطن", "الأمم المتحدة", "مجلس الأمن", "عقوبات", "الجيش", "عاجل",
           "اقتصاد", "أسعار", "سعر", "الدينار", "الدولار", "الذهب", "النفط", "موازنة", "ضريبة", "الضمان",
           "بنك", "البنك", "تضخم", "بطالة", "رواتب", "أجور", "استثمار", "الغاز", "الكهرباء", "المياه",
           "الدين", "ديون", "صادرات", "بورصة", "الأسواق",
           "تعليم", "الجامعات", "التوجيهي", "المستشفى", "الصحة", "نقابة", "الفقر", "السكن", "قانون",
           "القضاء", "محكمة", "فساد", "الأمن العام", "الدفاع المدني", "حريق", "فيضان"]

def important(title):
    if any(w in title for w in EXCLUDE):
        return False
    return any(w in title for w in INCLUDE)


lists = []
for name, url in FEEDS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
        titles = [(i.findtext("title") or "").strip() for i in root.iter("item")][:30]
        lists.append([{"src": name, "title": t} for t in titles if t and important(t)][:6])
        print("ok", name, len(lists[-1]))
    except Exception as e:
        print("fail", name, e)

merged = []
for i in range(6):
    for lst in lists:
        if i < len(lst):
            merged.append(lst[i])

if merged:
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.datetime.utcnow().isoformat() + "Z", "items": merged}, f, ensure_ascii=False)
