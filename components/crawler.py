# 목표 네이트 스포치 최신 기사 1개의 제목과 본문을 가져오는 함수 완성

# 방법:
# requests와 BeautifulSoup4를 사용해 네이트 스포츠 메인 페이지의 HTML을 가져옵니다.
# CSS 선택자(Selector)를 이용해 최신 기사 1개의 URL과 제목을 추출합니다.
# 추출한 URL로 다시 requests를 보내 기사 본문 페이지의 HTML을 가져옵니다.
# 기사 본문 영역의 CSS 선택자를 찾아 텍스트만 깨끗하게 추출합니다.
# 만약 이 과정에서 JavaScript 렌더링이 필요해 데이터가 보이지 않는다면, 즉시 Selenium으로 전환하여 브라우저를 직접 제어하는 방식으로 본문을 추출합니다.
# 테스트: python crawler.py를 실행했을 때, 터미널에 기사 제목과 본문이 잘 출력되는지 확인합니다.

import requests
from bs4 import BeautifulSoup
import time


def crawl_nate_news_top3() :
    """     
    네이트 랭킹 뉴스 페이지에 접속하여 상위 3개 기사의 제목, 링크, 정제된 본문을
    가져오는 함수입니다.

    Returns:
         list: 각 기사 정보가 담긴 딕셔너리들의 리스트.
         예: [{'rank': 1, 'title': '...', 'link': '...', 'content': '...'}]
         오류 발생 시 빈 리스트를 반환합니다.
    """ 
    
    URL = "https://news.nate.com/rank/interest?sc=spo&p=day"
    try:
        response = requests.get(URL)
    except requests.exceptions.RequestException as e:
        print(f"[오류] 페이지 접속 실패: {e}")
        return []
    
    if response.status_code == 200:
        print("성공적으로 페이지에 접속했습니다.")
    print(response.text[:500])
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())

    # 4단계에서 찾은 최종 선택자를 사용하여 모든 뉴스 아이템 선택
    # 쉼표(,)로 여러 선택자를 연결
    news_items = soup.select('div.mlt01 a')
    # print(news_items)
    
    print( "네이트 뉴스 스포츠 1")

    crawled_data = []
    for index, item in enumerate(news_items, start=1):
      
      if index > 3:
        print("\n상위 3개 기사 처리를 완료했습니다.")
        break
        
      try:
        # 제목 추출 ( 양옆 공백제거 )
        title_element = item.select_one('h2.tit, strong')
        if title_element:
            title = title_element.get_text(strip=True)

            # URL 추출
            link = item['href']
            if link.startswith('//'):
                link = 'https:' + link

            
            
            # 기사 본문 페이지 접속
            article_response = requests.get(link)
            if article_response.status_code != 200:
                print(f" - [오류] 기사 접속 실패: {title}")
                continue
            
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            content_element = article_soup.select_one('div.content_view')
            content = "본문이 아직 없네욧."
            if content_element:
                # --- 본문 정제 로직 (Decomposition) ---
                # 1. 불필요한 태그(광고 div, 이미지 figure 등)를 찾아서 제거
                unwanted_tags = content_element.find_all(['div', 'figure', 'script', 'style',
      'a'])
                for tag in unwanted_tags:
                    tag.decompose()
                
                # 2. 깨끗해진 상태에서 텍스트 추출
                content = content_element.get_text(separator=' ', strip=True)[:500]

            crawled_data.append({
                'rank': index,
                'title': title,
                'link': link,
                'content': f"{content}..."
            })
            time.sleep(0.5)
        else:
            print(f" - [오류] 기사 본문을 찾을 수 없습니다: {title}")

        
      except Exception as e:
        print(f"오류: {e}")
    else:
        print(f"페이지 접속에 실패했습니다. 상태 코드: {response.status_code}")
    return crawled_data
  
  
    # 이 파일이 직접 실행될 때만 아래 코드가 동작합니다.
if __name__ == "__main__":
    print("네이트 뉴스 랭킹 TOP 3 크롤링을 시작합니다...")
 
    top3_news = crawl_nate_news_top3()
 
    if top3_news:
        print("\n--- 크롤링 결과 ---")
        for news in top3_news:
            print(f"[{news['rank']}위] {news['title']}")
            print(f"  - 링크: {news['link']}")
            print(f"  - 본문: {news['content']}\n")
        print("크롤링을 성공적으로 완료했습니다.")
    else:
        print("크롤링에 실패했거나 가져올 데이터가 없습니다.")