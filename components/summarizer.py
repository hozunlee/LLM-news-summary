import os
import httpx
from dotenv import load_dotenv

load_dotenv()
PPLX_API_KEY = os.getenv("PPLX_API_KEY")

# API 요청을 위한 헤더를 정의합니다.
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {PPLX_API_KEY}",
    "content-type": "application/json"
}

async def summarize_text(article: str) -> str:
    """
    주어진 텍스트를 요약하는 함수입니다.
    

    Args:
        article (str): 요약할 텍스트

    Returns:
        str: 요약된 텍스트
    """
    
    prompt = f"""
    다음 뉴스 기사를 기반으로 텍스트를 쉽게 요약하여 분석합니다. 
    답변은 1. 2. 3. 으로 핵심을 알려주고 마지막으로 결론과 앞으로의 전망을 알려주세요.
    
    기사: {article}
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json={
                    "model": "sonar",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"[ERROR] {response.status_code} - {response.text}"
    except Exception as e:
        return f"[ERROR] 요약 생성 중 오류: {str(e)}"



async def summarize_article_with_LLM(article: str):
    print("\n[ 요약을 진행합니다.]")
    AI_summary = await summarize_text(article)
    return AI_summary
