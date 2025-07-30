# Pyside6를 사용하여 GUI를 구현합니다.
# 메인 윈도우를 만들고, 내부에 위젯을 배치
# QPushButton : 최신기사 요약 하기 버튼
# QLabel : 기사 제막을 표시할 라벨
# QTextEdit : 기사 본문을 표시할 텍스트 에디터 (읽기 전용)
# QVBoxLayout : 위젯을 수직으로 배치할 레이아웃
# QWidget : 메인 윈도우의 내부 위젯을 포함할 컨테이너

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QTextEdit 
import asyncio
from PySide6.QtCore import Qt

import qasync

from components.gui.call_news import fetch_summarized_news


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        # 윈도우 기본 설정
        self.setWindowTitle("네이트 뉴스 요약기")
        self.setGeometry(100, 100, 800, 600) # (x, y, 너비, 높이)
        
        # UI 위젯 생성
        self.label = QLabel("아래 버턴을 눌러 최신 스포츠 뉴스 TOP 3 요약을 받아보세요.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter) #텍스트 가운데 정렬 
        
        self.button = QPushButton(" 뉴스 요약 불러오기 ")
        
        # 결과를 표시할 텍스트 상사 ( 읽기 전용)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        
        # 시그널 - 슬롯 연결
        self.button.clicked.connect(self.on_button_click)
        
        # 레이아웃 설정
        # QVBoxLayout : 위젯을 수직으로 배치할 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.text_edit)
        
        # 메인 윈도우의 내부 위젯을 설정
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        
    # 슬롯 함수 정의
    def on_button_click(self):
        print("버튼 클릭됨. 비동기 작업 시작.")
        self.button.setEnabled(False)
        self.text_edit.setText("최신 뉴스를 불러오는 중입니다...")
        
        # 비동기 함수를 GUI 이벤트 루프와 함께 실행
        asyncio.ensure_future(self.run_fetch_and_update_ui())
    
    async def run_fetch_and_update_ui(self):
        """비동기 작업을 실행하고, 결과로 UI를 업데이트하는 전체 흐름"""
        news_data = await fetch_summarized_news()
        
        if news_data and "results" in news_data:
          # 성공적
          formatted_text = ""
          articles = news_data["results"]
          for article in articles:
            rank = article.get("rank", "-")
            title = article.get("title", "-")
            link = article.get("link", "-")
            summary = article.get("summary", "-")
            
            ## HTML 형식으로 텍스트 꾸미기
                    # HTML 형식으로 텍스트를 꾸밉니다.
            formatted_text += f"""
            <h2 style="color:#005A9C;">{rank}위: {title}</h2>
            <p><b>링크:</b> <a href="{link}">{link}</a></p>
            <p>{summary.replace('\n', '<br>')}</p>
            <hr>
            """
            
        # QTextEdit는 간단한 HTML 태그를 지원함
          self.text_edit.setHtml(formatted_text)
          

        elif news_data and "error" in news_data:
            # 실패 시, 오류 메시지 표시
          self.text_edit.setText(news_data["error"])

        else:
            # 실패 시, 오류 메시지 표시
            error_message = news_data.get('error', '알 수 없는 오류입니다.')
            self.text_edit.setText(error_message)
        # 작업 완료 후 버튼을 다시 활성화
        self.button.setEnabled(True)
        
# 이 파일이 직접 실행될 때만 아래 코드가 동작합니다.
if __name__ == '__main__':
  # GUI 애플리 케이션의 생명주기를 관리하는 객체
    app = QApplication(sys.argv)

    # qasync를 사용하여 asyncio 이벤트 루프를 PySide6와 통합
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)


    # 메인 윈도우를 생성하고 표시
    window = MainWindow()
    window.show()
    # GUI 애플리케이션의 이벤트 루프를 실행
    with loop:
        loop.run_forever()
    sys.exit(app.exec())
    
    
