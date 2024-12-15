# Log-Analiz2


## Ümumi Baxış
Bu skript web serverin "access log" fayllarını təhlil etmək, 404 səhv kodlarına əsaslanan potensial zərərli URL-ləri aşkar etmək, həmin URL-ləri qara siyahı ilə müqayisə etmək və nəticələri müxtəlif formatlarda (TXT, CSV, JSON) saxlamaq üçün hazırlanmışdır. 

## Skriptin Əsas Xüsusiyyətləri

1. **Access log fayllarının təhlili**: Log fayllarındakı URL-lər və onların status kodları oxunur və emal edilir.
2. **404 səhvlərinin təhlili**: 404 status kodu alan URL-lər müəyyən edilir və təkrar sayları hesablanır.
3. **Nəticələrin saxlanılması**: URL-lər və onların status kodları TXT, CSV və JSON formatlarında saxlanılır.
4. **Qara siyahıdan məlumat toplama**: Selenium vasitəsilə verilmiş veb sayt üzərindən qara siyahı məlumatları toplanır.
5. **Qara siyahı ilə uyğunluğun yoxlanılması**: Log fayllarındakı URL-lər qara siyahı ilə müqayisə edilir.
6. **Xülasə hesabatı**: Ümumi nəticələr xülasə şəklində JSON faylında saxlanılır.
7. **Yükləmə barı**: Proseslərin hər biri üçün istifadəçiyə məlumat verən dinamik yükləmə barları əlavə edilmişdir.

## Fayl Strukturunun İstifadəsi
Skript çıxış fayllarını "output_files" adlı qovluqda saxlayır. Bu qovluq avtomatik olaraq yaradılır.

### Çıxış Faylları
- **`url_status_report.txt`**: Bütün URL-lərin və onların status kodlarının siyahısı.
- **`malware_candidates.csv`**: 404 status koduna əsaslanan potensial zərərli URL-lər.
- **`alert.json`**: Qara siyahı ilə uyğun gələn URL-lər.
- **`summary_report.json`**: Ümumi hesabat.

## Tələblər

Skriptin uğurla işləməsi üçün aşağıdakı proqram və kitabxanalar tələb olunur:

### Proqramlar
- **Python 3.7+**
- **Google Chrome** (və ya uyğun brauzer)
- **ChromeDriver** (Selenium üçün)

### Python Kitabxanaları
- `os`
- `re`
- `csv`
- `json`
- `collections`
- `selenium`
- `tqdm`

Python kitabxanalarını quraşdırmaq üçün:
```bash
pip install selenium tqdm
```

## İstifadə Qaydaları

### 1. Log Faylının Hazırlanması
Skript "access_log.txt" adlı faylı oxuyur. Bu faylda hər bir sətrin formatı aşağıdakı kimi olmalıdır:
```text
127.0.0.1 - - [10/Dec/2024:14:00:00 +0000] "GET /example-path HTTP/1.1" 404
```

### 2. Skripti İşlətmək
Skriptin işə salınması:
```bash
python scan.py
```

### 3. Qara Siyahının Hazırlanması
Qara siyahı məlumatları `http://127.0.0.1:8000` kimi yerli bir serverdə saxlanmalıdır və qara siyahı HTML formatında `<li>` elementləri daxilində olmalıdır.

### 4. Çıxış Fayllarına Baxış
İcra prosesi bitdikdən sonra nəticələr **"output_files"** qovluğunda saxlanılır.

## Əsas Proseslər və Onların Yerləri

### 1. **Log Faylının Analizi**
`parse_access_log` funksiyası log faylını oxuyur və URL-ləri status kodları ilə birlikdə emal edir. Nəticələr `url_status_report.txt` faylında saxlanılır.

### 2. **404 Səhvlərinin Analizi**
`count_404_urls` funksiyası 404 status koduna malik URL-ləri müəyyən edir və onların təkrar sayını hesablayır. Bu məlumatlar `malware_candidates.csv` faylında saxlanılır.

### 3. **Qara Siyahıdan Məlumat Toplanması**
`scrape_blacklist` funksiyası Selenium vasitəsilə verilmiş qara siyahıdan məlumatları toplayır.

### 4. **Qara Siyahı ilə Uyğunluğun Yoxlanılması**
`find_matching_urls` funksiyası log faylındakı URL-ləri qara siyahı ilə müqayisə edir və uyğun gələnləri `alert.json` faylına yazır.

### 5. **Xülasə Hesabatı**
`write_summary_report` funksiyası ümumi hesabatı JSON formatında `summary_report.json` faylına yazır.

## Gələcəkdə Təkmilləşdirmələr
- Log fayllarının müxtəlif formatlarının dəstəklənməsi.
- Daha ətraflı statistik analiz.
- Qara siyahı üçün digər məlumat mənbələrinin inteqrasiyası.

## Müəllif
Bu skript [Nihad](https://github.com/nihad71) tərəfindən hazırlanmışdır.

