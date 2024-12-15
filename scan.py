import os
import re
import csv
import json
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm

# Çıxış faylları üçün əsas qovluq
OUTPUT_FOLDER = "output_files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Qovluq mövcud deyilsə, yaradılır

# Çıxış fayllarının yolları
URL_STATUS_REPORT_FILE = os.path.join(OUTPUT_FOLDER, "url_status_report.txt")
MALWARE_CANDIDATES_FILE = os.path.join(OUTPUT_FOLDER, "malware_candidates.csv")
ALERT_JSON_FILE = os.path.join(OUTPUT_FOLDER, "alert.json")
SUMMARY_REPORT_FILE = os.path.join(OUTPUT_FOLDER, "summary_report.json")

# 1. Access log-dan URL-ləri və status kodlarını çıxarmaq
def parse_access_log(log_file):
    url_status = []
    with open(log_file, 'r') as file:
        for line in tqdm(file, desc="Access log məlumatları analiz edilir"):
            match = re.search(r'(\S+) \S+ \S+ \[(.*?)\] "(.*?)" (\d{3})', line)
            if match:
                url = match.group(3).split()[1]  # URL
                status_code = match.group(4)    # Status kodu
                url_status.append((url, status_code))
    return url_status

# 2. 404 status kodu ilə URL-ləri müəyyən etmək
def count_404_urls(url_status):
    count = defaultdict(int)
    for url, status in tqdm(url_status, desc="404 URL-ləri hesablanır"):
        if status == '404':
            count[url] += 1
    return count

# 3. URL-ləri status kodları ilə fayla yazmaq
def write_url_status_report(url_status, output_file):
    with open(output_file, 'w') as file:
        for url, status in tqdm(url_status, desc="URL statusları fayla yazılır"):
            file.write(f"{url} {status}\n")
    print(f"➡ URL statusları yazıldı: {output_file}\n")

# 4. 404 URL-ləri CSV faylında yazmaq
def write_malware_candidates(counts, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['URL', '404_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url, count in tqdm(counts.items(), desc="404 URL-ləri CSV-yə yazılır"):
            writer.writerow({'URL': url, '404_count': count})
    print(f"➡ 404 URL-ləri yazıldı: {output_file}\n")

# 5. Veb scraping (Selenium ilə)
def scrape_blacklist(url):
    driver = webdriver.Chrome()
    driver.get(url)
    blacklist = []
    try:
        elements = driver.find_elements(By.XPATH, "//li")
        for element in tqdm(elements, desc="Qara siyahıdan məlumat yüklənir"):
            blacklist.append(element.text)
    finally:
        driver.quit()
    print(f"➡ Qara siyahı uğurla analiz edildi: {url}\n")
    return blacklist

# 6. URL-ləri qara siyahı ilə müqayisə etmək
def find_matching_urls(url_status, blacklist):
    matches = []
    for url, status in tqdm(url_status, desc="Qara siyahı ilə URL-lər uyğunlaşdırılır"):
        domain = re.sub(r'https?://(www\.)?', '', url).split('/')[0]
        if domain in blacklist:
            matches.append((url, status))
    return matches

# 7. JSON faylında uyğun URL-ləri yazmaq
def write_alert_json(matches, output_file):
    alerts = [{'url': url, 'status': status} for url, status in matches]
    with open(output_file, 'w') as json_file:
        json.dump(alerts, json_file, indent=4)
    print(f"➡ Uyğun URL-lər JSON formatında yazıldı: {output_file}\n")

# 8. Xülasə hesabatı yaratmaq
def write_summary_report(url_status, counts, output_file):
    summary = {
        'total_urls': len(url_status),
        'total_404': sum(counts.values()),
        'unique_404_urls': len(counts)
    }
    with open(output_file, 'w') as json_file:
        json.dump(summary, json_file, indent=4)
    print(f"➡ Xülasə hesabatı yaradıldı: {output_file}\n")

# Əsas funksiya
def main():
    log_file = 'access_log.txt'
    blacklist_url = 'http://127.0.0.1:8000'

    print("🔍 Analiz prosesi başlanır...\n")

    # 1. Access log-dan URL-ləri və status kodlarını çıxarın
    url_status = parse_access_log(log_file)

    # 2. 404 status kodu ilə URL-ləri müəyyən edin
    counts = count_404_urls(url_status)

    # 3. URL-lərin siyahısını status kodları ilə yazın
    write_url_status_report(url_status, URL_STATUS_REPORT_FILE)

    # 4. 404 URL-ləri CSV faylında yazın
    write_malware_candidates(counts, MALWARE_CANDIDATES_FILE)

    # 5. Veb scraping (Selenium ilə)
    blacklist = scrape_blacklist(blacklist_url)

    # 6. URL-ləri qara siyahı ilə müqayisə edin
    matches = find_matching_urls(url_status, blacklist)

    # 7. Uyğun URL-ləri JSON faylında yazın
    write_alert_json(matches, ALERT_JSON_FILE)

    # 8. Xülasə hesabatı yaradın
    write_summary_report(url_status, counts, SUMMARY_REPORT_FILE)

    print("✅ Analiz prosesi tamamlandı!")

if __name__ == "__main__":
    main()
