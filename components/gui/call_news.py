    #   fetch_summarized_news 라는 비동기 함수를 만듭니다. 이 함수는 httpx.AsyncClient를 사용하여
    # http://127.0.0.1:8000/summarize-top3-news 엔드포인트에 접속하고, 성공적으로 받아온 JSON 데이터를
    # 파이썬 딕셔너리로 반환합니다.
    
import httpx
import asyncio
    
# API 서버 주소
API_URL = "http://127.0.0.1:8000/summarize-top3-sport-news"
    
async def fetch_summarized_news():
      """
      API 서버에 비동기적으로 접속하여 요약된 뉴스 데이터를 가져옵니다.
      
      Returns:
        dict: 성공 시 서버에서 받은 JSON 데이터.
        None: 오류 발생 시.
      """
      print("API 서버에 데이터 요청을 시작합니다...")
      try:
        #  비동기 HTTP 클라이언트 생성
        async with httpx.AsyncClient() as client:
          # GET 요청을 보내고 응답을 기다린다 (60초 타임아웃)
          response = await client.get(API_URL, timeout=60.0)
          # 응답 상태 코드가 200이 아닌 경우 예외 발생
          response.raise_for_status()
          print("데이터를 성공적으로 수신했습니다.")
          return response.json()
      except httpx.HTTPStatusError as e:
        # 서버가 4xx 또는 5xx 에러를 반환한 경우
        print(f"API 서버 오류: {e.response.status_code} - {e.response.text}")
        return None
      except httpx.RequestError as e:
        # 네트워크 연결 오류 등 (서버가 실행되지 않았을 경우 등)
        print(f"네트워크 연결 오류: {e}")
        return None
      except Exception as e:
        # 그 외 예상치 못한 모든 오류
        print(f"알 수 없는 오류 발생: {e}")
        return None
      
      
# 테스트 코드
# 이 파일이 직접 실행될 때만 아래 코드가 동작합니다.

async def main_test():
  print("\n[ API 통신 테스트를 진행합니다. ]")
  data = await fetch_summarized_news()
  if data:
    print("\n--- API 통신 결과 ---")
    # 데이터 구조 확인
    import json
    print(json.dumps(data, indent=2, ensure_ascii=False))
  else:
    print("API 통신에 실패했습니다.")
  print("\nAPI 통신 테스트가 완료되었습니다.")
if __name__ == "__main__":
  # API 서버 먼저 실행 후 이코드를 실행하세요.
  # 예 : uvicorn main:app --reload
  asyncio.run(main_test())