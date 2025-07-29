import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from components.crawler import crawl_nate_news_top3
from components.summarizer import summarize_article_with_LLM

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title = "네이트 뉴스 요약 API",
    description = "네이트 뉴스를 크롤링하여 요약하는 API",
    version = "0.0.1"
)

# API 엔드포인트 정의
@app.get("/summarize-top3-sport-news", summary="네이트 스포츠 뉴스 TOP 3 기사(제목, 링크, 본문)를 크롤링하여 요약하는 API")
async def summarize_top3_sport_news():
    """
    1. 네이트 스포츠 뉴스 TOP 3 기사(제목, 링크, 본문)를 크롤링합니다.
    2. 3개의 기사 본문에 대한 요약 작업을 동시에 요청합니다.
    3. 크롤링된 데이터와 요약된 내용을 합쳐 반환합니다.
    """
    print("크롤링을 시작합니다...")
    # 1. 크롤러 실행하여 TOP 3 기사 데이터 가져오기
    top3_articles = crawl_nate_news_top3()
    
    # 에러처리
    if not top3_articles:
        raise HTTPException(status_code=500, detail="크롤링에 실패했습니다.")
    
    print(f"크롤링된 데이터: {len(top3_articles)}개의 기사를 성공적으로 수업했습니다. 요약해볼게요.")
    
    # 2. 3개의 기사 요약 작업을 비동기적으로 동시에 진행
    # 각기사의 content를 요약하는 작업을 병렬로 실행
    summary_tasks = [summarize_article_with_LLM(article['content']) for article in top3_articles]

    # asyncio.gather 를 사용해 모든 요약 태스트가 완료될 때까지 기다림
    summaries = await asyncio.gather(*summary_tasks)
    print("모든 요약 작업을 완료했습니다.")
    
    # 3. 크롤링된 데이터와 요약된 내용을 합쳐 반환
    for i, article in enumerate(top3_articles):
        article['summary'] = summaries[i]
    
    return JSONResponse(content={"results": top3_articles})


# 서버 상태 테스트 루트 엔드포인트
@app.get('/', summary='API 상태 체크')
def read_root():
    return {"message": "API가 정상적으로 작동 중입니다."}