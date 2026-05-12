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
        # YES24 출판사 위치: .info_pub 클래스
        pub_tag = item.select_one('.info_pub')
        
        if title_tag:
            title = title_tag.get_text(strip=True)
            publisher = pub_tag.get_text(strip=True) if pub_tag else "N/A"
            books.append({'Rank': rank, 'Title': title, 'Publisher': publisher, 'Store': 'YES24'})
            
    return books

def scrape_aladin():
    url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=1383"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = []
    items = soup.select('.ss_book_box')
    for rank, item in enumerate(items, 1):
        # 알라딘 도서 제목
        title_tag = item.select_one('a.bo3')
        
        # 알라딘 출판사 위치: 보통 제목 아래 리스트 항목 중 하나
        # ss_book_list의 세 번째 혹은 네 번째 li에 출판사가 포함됨
        info_tags = item.select('.ss_book_list li')
        publisher = "N/A"
        for info in info_tags:
            info_text = info.get_text()
            if ' | ' in info_text: # 알라딘은 '저자 | 출판사 | 날짜' 형식임
                parts = info_text.split(' | ')
                if len(parts) >= 2:
                    publisher = parts[1].strip()
                    break

        if title_tag:
            title = title_tag.get_text(strip=True)
            books.append({'Rank': rank, 'Title': title, 'Publisher': publisher, 'Store': 'Aladin'})
            
    return books

def save_to_csv(data, filename):
    if not data:
        print(f"{filename} - 데이터 없음")
        return
        
    keys = data[0].keys()
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"{filename} 저장 완료")

if __name__ == "__main__":
    today = datetime.now().strftime("%Y%m%d")
    
    # YES24
    yes24_data = scrape_yes24()
    save_to_csv(yes24_data, f'yes24_bestseller_{today}.csv')
    
    # 3~10초 랜덤 딜레이
    time.sleep(random.uniform(3, 10))
    
    # 알라딘
    aladin_data = scrape_aladin()
    save_to_csv(aladin_data, f'aladin_bestseller_{today}.csv')
