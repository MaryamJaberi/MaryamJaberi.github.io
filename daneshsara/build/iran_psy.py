# -*- coding: utf-8 -*-
"""Iran notes for the psychology wiki (national epidemiology) and the concept→note map.
Writes iran/*.json, data/psy/iran_map.json, and sets `iran` on the mapped psy concept files."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
def S(title, url=''): return {'title': title, 'url': url}
imhs = S('Sharifi, V., Amin-Esmaeili, M., Hajebi, A., Motevalian, A., Radgoodarzi, R., Hefazi, M., & Rahimi-Movaghar, A. (2015). Twelve-month prevalence and correlates of psychiatric disorders in Iran: The Iranian Mental Health Survey, 2011. Archives of Iranian Medicine, 18(2), 76–84.', 'https://pubmed.ncbi.nlm.nih.gov/25644794/')
drug = S('Amin-Esmaeili, M., Rahimi-Movaghar, A., Sharifi, V., et al. (2016). Epidemiology of illicit drug use disorders in Iran: Prevalence, correlates, comorbidity and service utilization results from the Iranian Mental Health Survey. Addiction, 111(10), 1836–1847.', 'https://doi.org/10.1111/add.13453')
who = S('World Health Organization (2021). Suicide worldwide in 2019: Global Health Estimates.', 'https://www.who.int/publications/i/item/9789240026643')
whr = S('Helliwell, J. F., Layard, R., Sachs, J. D., De Neve, J.-E., Aknin, L. B., & Wang, S. (Eds.) (2024). World Happiness Report 2024. Wellbeing Research Centre, University of Oxford.', 'https://worldhappiness.report/ed/2024/')
NOTES = [
 {'id': 'iran:mental-disorder-prevalence', 'domain': 'psy', 'question': {'fa': 'چند درصد ایرانیان در یک سال اختلال روانی دارند؟', 'en': 'What share of Iranians have a mental disorder in a given year?'},
  'finding': {'fa': 'پیمایش ملی سلامت روان ایران (۱۳۹۰، ۷٬۸۸۶ نفر ۱۵ تا ۶۴ ساله، مصاحبهٔ تشخیصی): ۲۳٫۶ درصد در دوازده ماه گذشته دست‌کم یک اختلال روانی داشتند؛ اختلال‌های اضطرابی (۱۵٫۶٪) و خلقی (۱۴٫۱٪) شایع‌ترین؛ زنان، شهرنشینان، بیکاران و مطلقه‌ها بیشتر در معرض.', 'en': 'Iranian Mental Health Survey (2011, 7,886 people aged 15–64, diagnostic interview): 23.6 percent had at least one mental disorder in the past twelve months; anxiety (15.6%) and mood disorders (14.1%) most common; women, urban residents, the unemployed and the divorced at higher risk.'},
  'year': 2011, 'method': 'national household survey, CIDI diagnostic interview', 'grade': 'A', 'contested': False, 'source': [imhs], 'fields': ['psychiatry'], 'concepts': ['psy:anxiety', 'psy:dx'], 'capability': [2, 5]},
 {'id': 'iran:drug-use-disorders', 'domain': 'psy', 'question': {'fa': 'اختلال مصرف مواد غیرقانونی در ایران چقدر شایع است؟', 'en': 'How common are illicit drug use disorders in Iran?'},
  'finding': {'fa': 'همان پیمایش ملی: شیوع دوازده‌ماههٔ اختلال مصرف مواد غیرقانونی ۲٫۴۴ درصد (مردان بسیار بیشتر از زنان)؛ مواد افیونی شایع‌ترین؛ هم‌ابتلایی بالا با اختلال‌های خلقی و اضطرابی و استفاده از خدمات درمانی کم.', 'en': 'Same national survey: twelve-month prevalence of illicit drug use disorders 2.44 percent (men far more than women); opioids most common; high comorbidity with mood and anxiety disorders and low use of treatment services.'},
  'year': 2011, 'method': 'national household survey, CIDI', 'grade': 'A', 'contested': False, 'source': [drug], 'fields': ['psychiatry'], 'concepts': ['psy:addiction', 'psy:opioids'], 'capability': [2, 6]},
 {'id': 'iran:suicide-rate', 'domain': 'psy', 'question': {'fa': 'نرخ خودکشی در ایران در مقایسه با جهان چقدر است؟', 'en': 'How does Iran\'s suicide rate compare with the world?'},
  'finding': {'fa': 'برآورد سازمان جهانی بهداشت (۲۰۱۹): نرخ سن‌استاندهٔ خودکشی ایران حدود ۵ در صد هزار، کمتر از میانگین جهانی (حدود ۹)؛ اما ثبت ناقص و انگ، برآوردها را کمتر از واقع می‌کند و تفاوت استانی (غرب کشور بالاتر) چشمگیر است.', 'en': 'WHO estimate (2019): Iran\'s age-standardised suicide rate about 5 per 100,000, below the global mean (about 9); but under-registration and stigma depress estimates, and provincial variation (higher in the west) is marked.'},
  'year': 2019, 'method': 'WHO modelled estimate from vital registration', 'grade': 'B', 'contested': False, 'critique': 'ثبت مرگ ناشی از خودکشی در ایران کامل نیست؛ ارقام ملی را باید کمینه دانست.', 'source': [who], 'fields': ['psychiatry'], 'concepts': ['psy:crisis-mh'], 'capability': [1, 5]},
 {'id': 'iran:happiness-rank', 'domain': 'psy', 'question': {'fa': 'ایرانیان در سنجش جهانی شادکامی کجا ایستاده‌اند؟', 'en': 'Where do Iranians stand in global happiness rankings?'},
  'finding': {'fa': 'گزارش جهانی شادکامی ۲۰۲۴ (میانگین ارزیابی زندگی ۲۰۲۱–۲۰۲۳، نردبان کانتریل ۰ تا ۱۰): ایران حدود ۴٫۹ و در ردهٔ صدم از ۱۴۳ کشور؛ پایین‌تر از میانگین جهانی و پایین‌تر از همسایگانی چون ترکیه و عربستان، بالاتر از افغانستان و لبنان.', 'en': 'World Happiness Report 2024 (life evaluation averaged 2021–2023, Cantril ladder 0–10): Iran about 4.9, ranked around 100th of 143; below the world mean and below neighbours such as Turkey and Saudi Arabia, above Afghanistan and Lebanon.'},
  'year': 2024, 'method': 'Gallup World Poll, ~1,000 respondents per year', 'grade': 'B', 'contested': False, 'critique': 'یک پرسش واحد با نمونهٔ کوچک سالانه؛ رتبه‌ها سال‌به‌سال نوسان دارند و تفاوت‌های کوچک معنادار نیستند.', 'source': [whr], 'fields': ['positive'], 'concepts': ['psy:happiness-origins', 'psy:perma'], 'capability': [5, 7]},
]
os.makedirs(f'{R}/iran', exist_ok=True)
MAP = {}
for n in NOTES:
    json.dump(n, open(f"{R}/iran/{n['id'].split(':')[1]}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for c in n['concepts']: MAP.setdefault(c, n['id'])
json.dump(MAP, open(f'{R}/data/psy/iran_map.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for cid, nid in MAP.items():
    p = f"{R}/data/psy/concepts/{cid.split(':')[1]}.json"
    if os.path.exists(p):
        c = json.load(open(p, encoding='utf-8')); c['iran'] = nid
        json.dump(c, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('psy iran notes', len(NOTES), 'mapped concepts', len(MAP))
