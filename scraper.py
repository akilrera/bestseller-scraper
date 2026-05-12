import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import random

# 공통 헤더 (봇 차단 방지용)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

def scrape_yes24():
    url = "https://www.yes24.com/product/category/weekbestseller?categoryNumber=001001015&pageNumber=1&pageSize=120&type=week"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = []
    items = soup.select('.itemUnit')
    for rank, item in enumerate(items, 1):
        title_tag = item.select_one('.gd_name')
        if title_tag:
            title = title_tag.get_text(strip=True)
            books.append({'Rank': rank, 'Title': title, 'Store': 'YES24'})
    return books

def scrape_aladin():
    url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=1383"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = []
    items = soup.select('.ss_book_box')
    for rank, item in enumerate(items, 1):
        title_tag = item.select_one('a.bo3')
        if title_tag:
            title = title_tag.get_text(strip=True)
            books.append({'Rank': rank, 'Title': title, 'Store': 'Aladin'})
    return books

def save_to_csv(data, filename):
    if not data:
        return
    keys = data[0].keys()
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    today = datetime.now().strftime("%Y%m%d")
    
    # YES24 수집
    yes24_data = scrape_yes24()
    save_to_csv(yes24_data, f'yes24_bestseller_{today}.csv')
    
    # 3~10초 랜덤 딜레이 (사람처럼 보이게 하기)
    time.sleep(random.uniform(3, 10))
    
    # 알라딘 수집
    aladin_data = scrape_aladin()
    save_to_csv(aladin_data, f'aladin_bestseller_{today}.csv')
